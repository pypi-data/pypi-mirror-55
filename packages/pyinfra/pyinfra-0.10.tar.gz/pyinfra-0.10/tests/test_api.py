# pyinfra
# File: tests/test_api.py
# Desc: tests for the pyinfra API

from inspect import currentframe, getframeinfo
from unittest import TestCase

import gevent.hub

from mock import mock_open, patch
from paramiko import (
    PasswordRequiredException,
    SSHException,
)

from pyinfra import pseudo_host, pseudo_state
from pyinfra.api import Config, State
from pyinfra.api.connect import connect_all
from pyinfra.api.exceptions import NoGroupError, NoHostError, PyinfraError
from pyinfra.api.operation import add_op
from pyinfra.api.operations import run_ops
from pyinfra.modules import files, server

from .paramiko_util import (
    FakeBuffer,
    FakeChannel,
    FakeRSAKey,
    PatchSSHTestCase,
)
from .util import make_inventory

# Don't print out exceptions inside greenlets (because here we expect them!)
gevent.hub.Hub.NOT_ERROR = (Exception,)


class TestInventoryApi(TestCase):
    def test_inventory_creation(self):
        inventory = make_inventory()

        # Check length
        self.assertEqual(len(inventory.hosts), 2)

        # Get a host
        host = inventory['somehost']
        self.assertEqual(host.data.ssh_user, 'vagrant')

        # Check our group data
        self.assertEqual(
            inventory.get_group_data('test_group'),
            {'group_data': 'hello world'},
        )

    def test_tuple_host_group_inventory_creation(self):
        inventory = make_inventory(
            hosts=[
                ('somehost', {'some_data': 'hello'}),
            ],
            tuple_group=([
                ('somehost', {'another_data': 'world'}),
            ], {
                'tuple_group_data': 'word',
            }),
        )

        # Check host data
        host = inventory['somehost']
        self.assertEqual(host.data.some_data, 'hello')
        self.assertEqual(host.data.another_data, 'world')

        # Check group data
        self.assertEqual(host.data.tuple_group_data, 'word')

    def test_host_and_group_errors(self):
        inventory = make_inventory()

        with self.assertRaises(NoHostError):
            inventory['i-dont-exist']

        with self.assertRaises(NoGroupError):
            getattr(inventory, 'i-dont-exist')


class TestSSHApi(TestCase):
    def setUp(self):
        self.fake_connect_patch = patch('pyinfra.api.connectors.ssh.SSHClient.connect')
        self.fake_connect_mock = self.fake_connect_patch.start()

        self.fake_get_transport_patch = patch('pyinfra.api.connectors.ssh.SSHClient.get_transport')
        self.fake_get_transport_patch.start()

        self.fake_agentrequesthandler_patch = patch('pyinfra.api.connectors.ssh.AgentRequestHandler')
        self.fake_agentrequesthandler_patch.start()

    def tearDown(self):
        self.fake_connect_patch.stop()
        self.fake_get_transport_patch.stop()
        self.fake_agentrequesthandler_patch.stop()

    def test_connect_all(self):
        inventory = make_inventory()
        state = State(inventory, Config())
        connect_all(state)

        self.assertEqual(len(state.active_hosts), 2)

    def test_connect_all_password(self):
        inventory = make_inventory(ssh_password='test')

        # Get a host
        somehost = inventory.get_host('somehost')
        self.assertEqual(somehost.data.ssh_password, 'test')

        state = State(inventory, Config())
        connect_all(state)

        self.assertEqual(len(state.active_hosts), 2)

    def test_connect_with_ssh_key(self):
        state = State(make_inventory(hosts=(
            ('somehost', {'ssh_key': 'testkey'}),
        )), Config())

        with patch('pyinfra.api.connectors.ssh.path.isfile', lambda *args, **kwargs: True), \
                patch('pyinfra.api.connectors.ssh.RSAKey.from_private_key_file') as fake_key_open:

            fake_key = FakeRSAKey()
            fake_key_open.return_value = fake_key

            state.deploy_dir = '/'

            connect_all(state)

            # Check the key was created properly
            fake_key_open.assert_called_with(filename='testkey')

            # And check the Paramiko SSH call was correct
            self.fake_connect_mock.assert_called_with(
                'somehost',
                allow_agent=False,
                look_for_keys=False,
                pkey=fake_key,
                timeout=10,
                username='vagrant',
            )

    def test_connect_with_ssh_key_password(self):
        state = State(make_inventory(hosts=(
            ('somehost', {'ssh_key': 'testkey', 'ssh_key_password': 'testpass'}),
        )), Config())

        with patch(
            'pyinfra.api.connectors.ssh.path.isfile',
            lambda *args, **kwargs: True,
        ), patch(
            'pyinfra.api.connectors.ssh.RSAKey.from_private_key_file',
        ) as fake_key_open:

            def fake_key_open_fail(*args, **kwargs):
                if 'password' not in kwargs:
                    raise PasswordRequiredException()

            fake_key_open.side_effect = fake_key_open_fail

            fake_key = FakeRSAKey()
            fake_key_open.return_value = fake_key

            state.deploy_dir = '/'

            connect_all(state)

            # Check the key was created properly
            fake_key_open.assert_called_with(filename='testkey', password='testpass')

    def test_connect_with_missing_ssh_key(self):
        state = State(make_inventory(hosts=(
            ('somehost', {'ssh_key': 'testkey'}),
        )), Config())

        with self.assertRaises(IOError) as e:
            connect_all(state)

        # Ensure pyinfra style IOError
        self.assertTrue(e.exception.args[0].startswith('No such private key file:'))


class TestStateApi(PatchSSHTestCase):
    def test_fail_percent(self):
        inventory = make_inventory((
            'somehost',
            ('thinghost', {'ssh_hostname': SSHException}),
            'anotherhost',
        ))
        state = State(inventory, Config(FAIL_PERCENT=1))

        # Ensure we would fail at this point
        with self.assertRaises(PyinfraError) as context:
            connect_all(state)

        self.assertEqual(context.exception.args[0], 'Over 1% of hosts failed (33%)')

        # Ensure the other two did connect
        self.assertEqual(len(state.active_hosts), 2)


class TestOperationsApi(PatchSSHTestCase):
    def test_op(self):
        inventory = make_inventory()
        somehost = inventory.get_host('somehost')
        anotherhost = inventory.get_host('anotherhost')

        state = State(inventory, Config())

        # Enable printing on this test to catch any exceptions in the formatting
        state.print_output = True
        state.print_fact_info = True
        state.print_fact_output = True

        connect_all(state)

        add_op(
            state, files.file,
            '/var/log/pyinfra.log',
            user='pyinfra',
            group='pyinfra',
            mode='644',
            sudo=True,
            sudo_user='test_sudo',
            su_user='test_su',
            ignore_errors=True,
            env={
                'TEST': 'what',
            },
        )

        op_order = state.get_op_order()

        # Ensure we have an op
        self.assertEqual(len(op_order), 1)

        first_op_hash = op_order[0]

        # Ensure the op name
        self.assertEqual(
            state.op_meta[first_op_hash]['names'],
            {'Files/File'},
        )

        # Ensure the commands
        self.assertEqual(
            state.ops[somehost][first_op_hash]['commands'],
            [
                'touch /var/log/pyinfra.log',
                'chmod 644 /var/log/pyinfra.log',
                'chown pyinfra:pyinfra /var/log/pyinfra.log',
            ],
        )

        # Ensure the meta
        meta = state.op_meta[first_op_hash]
        self.assertEqual(meta['sudo'], True)
        self.assertEqual(meta['sudo_user'], 'test_sudo')
        self.assertEqual(meta['su_user'], 'test_su')
        self.assertEqual(meta['ignore_errors'], True)

        # Ensure run ops works
        run_ops(state)

        # Ensure ops completed OK
        self.assertEqual(state.results[somehost]['success_ops'], 1)
        self.assertEqual(state.results[somehost]['ops'], 1)
        self.assertEqual(state.results[anotherhost]['success_ops'], 1)
        self.assertEqual(state.results[anotherhost]['ops'], 1)

        # And w/o errors
        self.assertEqual(state.results[somehost]['error_ops'], 0)
        self.assertEqual(state.results[anotherhost]['error_ops'], 0)

        # And with the different modes
        run_ops(state, serial=True)
        run_ops(state, no_wait=True)

    def test_file_op(self):
        inventory = make_inventory()

        state = State(inventory, Config())
        connect_all(state)

        with patch('pyinfra.modules.files.path.isfile', lambda *args, **kwargs: True):
            # Test normal
            add_op(
                state, files.put,
                {'First op name'},
                'files/file.txt',
                '/home/vagrant/file.txt',
            )

            # And with sudo
            add_op(
                state, files.put,
                'files/file.txt',
                '/home/vagrant/file.txt',
                sudo=True,
                sudo_user='pyinfra',
            )

            # And with su
            add_op(
                state, files.put,
                'files/file.txt',
                '/home/vagrant/file.txt',
                sudo=True,
                su_user='pyinfra',
            )

        op_order = state.get_op_order()

        # Ensure we have all ops
        self.assertEqual(len(op_order), 3)

        first_op_hash = op_order[0]

        # Ensure first op is the right one
        self.assertEqual(
            state.op_meta[first_op_hash]['names'],
            {'First op name'},
        )

        somehost = inventory.get_host('somehost')
        anotherhost = inventory.get_host('anotherhost')

        # Ensure first op has the right (upload) command
        self.assertEqual(
            state.ops[somehost][first_op_hash]['commands'],
            [
                ('files/file.txt', '/home/vagrant/file.txt'),
            ],
        )

        # Ensure second op has sudo/sudo_user
        self.assertEqual(state.op_meta[op_order[1]]['sudo'], True)
        self.assertEqual(state.op_meta[op_order[1]]['sudo_user'], 'pyinfra')

        # Ensure third has su_user
        self.assertEqual(state.op_meta[op_order[2]]['su_user'], 'pyinfra')

        # Check run ops works
        with patch('pyinfra.api.util.open', mock_open(read_data='test!'), create=True):
            run_ops(state)

        # Ensure ops completed OK
        self.assertEqual(state.results[somehost]['success_ops'], 3)
        self.assertEqual(state.results[somehost]['ops'], 3)
        self.assertEqual(state.results[anotherhost]['success_ops'], 3)
        self.assertEqual(state.results[anotherhost]['ops'], 3)

        # And w/o errors
        self.assertEqual(state.results[somehost]['error_ops'], 0)
        self.assertEqual(state.results[anotherhost]['error_ops'], 0)

    def test_op_hosts_limit(self):
        inventory = make_inventory()
        state = State(inventory, Config())
        connect_all(state)

        # Add op to both hosts
        add_op(state, server.shell, 'echo "hi"')

        # Add op to just the first host
        add_op(
            state, server.user,
            'somehost_user',
            hosts=inventory['somehost'],
        )

        # Ensure there are two ops
        self.assertEqual(len(state.get_op_order()), 2)

        # Ensure somehost has two ops and anotherhost only has the one
        self.assertEqual(len(state.ops[inventory.get_host('somehost')]), 2)
        self.assertEqual(len(state.ops[inventory.get_host('anotherhost')]), 1)

    def test_op_state_hosts_limit(self):
        inventory = make_inventory()
        state = State(inventory, Config())
        connect_all(state)

        # Add op to both hosts
        add_op(state, server.shell, 'echo "hi"')

        # Add op to just the first host
        with state.hosts('test_group'):
            add_op(
                state, server.user,
                'somehost_user',
            )

            # Now, also limited but set hosts to the non-limited hosts, which
            # should mean this operation applies to no hosts.
            add_op(
                state, server.user,
                'somehost_user',
                hosts=inventory.get_host('anotherhost'),
            )

        # Ensure there are three ops
        self.assertEqual(len(state.get_op_order()), 3)

        # Ensure somehost has two ops and anotherhost only has the one
        self.assertEqual(len(state.ops[inventory.get_host('somehost')]), 2)
        self.assertEqual(len(state.ops[inventory.get_host('anotherhost')]), 1)

    def test_run_once_serial_op(self):
        inventory = make_inventory()
        state = State(inventory, Config())
        connect_all(state)

        # Add a run once op
        add_op(state, server.shell, 'echo "hi"', run_once=True, serial=True)

        # Ensure it's added to op_order
        self.assertEqual(len(state.get_op_order()), 1)

        somehost = inventory.get_host('somehost')
        anotherhost = inventory.get_host('anotherhost')

        # Ensure between the two hosts we only run the one op
        self.assertEqual(len(state.ops[somehost]) + len(state.ops[anotherhost]), 1)

        # Check run works
        run_ops(state)

        self.assertEqual((
            state.results[somehost]['success_ops']
            + state.results[anotherhost]['success_ops']
        ), 1)

    def test_full_op_fail(self):
        inventory = make_inventory()
        state = State(inventory, Config())
        connect_all(state)

        add_op(state, server.shell, 'echo "hi"')

        with patch('pyinfra.api.connectors.ssh.run_shell_command') as fake_run_command:
            fake_channel = FakeChannel(1)
            fake_run_command.return_value = (
                False,
                FakeBuffer('', fake_channel),
                FakeBuffer('', fake_channel),
            )

            with self.assertRaises(PyinfraError) as e:
                run_ops(state)

            self.assertEqual(e.exception.args[0], 'No hosts remaining!')

            somehost = inventory.get_host('somehost')

            # Ensure the op was not flagged as success
            self.assertEqual(state.results[somehost]['success_ops'], 0)
            # And was flagged asn an error
            self.assertEqual(state.results[somehost]['error_ops'], 1)

    def test_ignore_errors_op_fail(self):
        inventory = make_inventory()
        state = State(inventory, Config())
        connect_all(state)

        add_op(state, server.shell, 'echo "hi"', ignore_errors=True)

        with patch('pyinfra.api.connectors.ssh.run_shell_command') as fake_run_command:
            fake_channel = FakeChannel(1)
            fake_run_command.return_value = (
                False,
                FakeBuffer('', fake_channel),
                FakeBuffer('', fake_channel),
            )

            # This should run OK
            run_ops(state)

            somehost = inventory.get_host('somehost')

            # Ensure the op was added to results
            self.assertEqual(state.results[somehost]['ops'], 1)
            self.assertEqual(state.results[somehost]['error_ops'], 1)
            # But not as a success
            self.assertEqual(state.results[somehost]['success_ops'], 0)

    def test_no_invalid_op_call(self):
        inventory = make_inventory()
        state = State(inventory, Config())
        connect_all(state)
        pseudo_state.set(state)

        state.in_op = True
        with self.assertRaises(PyinfraError):
            server.user('someuser')

        state.in_op = False
        state.in_deploy = True
        with self.assertRaises(PyinfraError):
            server.user('someuser')

    def test_op_line_numbers(self):
        inventory = make_inventory()
        state = State(inventory, Config())
        connect_all(state)

        # Add op to both hosts
        add_op(state, server.shell, 'echo "hi"')

        # Add op to just the second host - using the pseudo modules such that
        # it replicates a deploy file.
        pseudo_state.set(state)
        pseudo_host.set(inventory['anotherhost'])
        first_pseudo_hash = server.user('anotherhost_user').hash
        first_pseudo_call_line = getframeinfo(currentframe()).lineno - 1

        # Add op to just the first host - using the pseudo modules such that
        # it replicates a deploy file.
        pseudo_state.set(state)
        pseudo_host.set(inventory['somehost'])
        second_pseudo_hash = server.user('somehost_user').hash
        second_pseudo_call_line = getframeinfo(currentframe()).lineno - 1

        pseudo_state.reset()
        pseudo_host.reset()

        # Ensure there are two ops
        op_order = state.get_op_order()
        self.assertEqual(len(op_order), 3)

        # And that the two ops above were called in the expected order
        self.assertEqual(op_order[1], first_pseudo_hash)
        self.assertEqual(op_order[2], second_pseudo_hash)

        # And that they have the expected line numbers
        self.assertEqual(
            state.op_line_numbers_to_hash.get((0, first_pseudo_call_line)),
            first_pseudo_hash,
        )
        self.assertEqual(
            state.op_line_numbers_to_hash.get((0, second_pseudo_call_line)),
            second_pseudo_hash,
        )

        # Ensure somehost has two ops and anotherhost only has the one
        self.assertEqual(len(state.ops[inventory.get_host('somehost')]), 2)
        self.assertEqual(len(state.ops[inventory.get_host('anotherhost')]), 2)
