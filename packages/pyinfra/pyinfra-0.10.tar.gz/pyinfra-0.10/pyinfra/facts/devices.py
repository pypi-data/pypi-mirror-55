# pyinfra
# File: pyinfra/facts/devices.py
# Desc: device (nics, hdds, etc) facts

import re

from pyinfra.api import FactBase


class BlockDevices(FactBase):
    '''
    Returns a dict of (mounted) block devices:

    .. code:: python

        '/dev/sda1': {
            'available': '39489508',
            'used_percent': '3',
            'mount': '/',
            'used': '836392',
            'blocks': '40325900'
        },
        ...
    '''

    command = 'df'
    regex = r'([a-zA-Z0-9\/\-_]+)\s+([0-9]+)\s+([0-9]+)\s+([0-9]+)\s+([0-9]{1,3})%\s+([a-zA-Z\/0-9\-_]+)'
    default = dict

    def process(self, output):
        devices = {}

        for line in output:
            matches = re.match(self.regex, line)
            if matches:
                if matches.group(1) == 'none':
                    continue

                devices[matches.group(1)] = {
                    'blocks': matches.group(2),
                    'used': matches.group(3),
                    'available': matches.group(4),
                    'used_percent': matches.group(5),
                    'mount': matches.group(6),
                }

        return devices


nettools_1_regexes = [
    (
        r'^inet addr:([0-9\.]+).+Bcast:([0-9\.]+).+Mask:([0-9\.]+)$',
        ('ipv4', 'address', 'broadcast', 'netmask'),
    ),
    (
        r'^inet6 addr: ([0-9a-z:]+)\/([0-9]+) Scope:Global',
        ('ipv6', 'address', 'size'),
    ),
]

nettools_2_regexes = [
    (
        r'^inet ([0-9\.]+)\s+netmask ([0-9\.fx]+)(?:\s+broadcast ([0-9\.]+))?$',
        ('ipv4', 'address', 'netmask', 'broadcast'),
    ),
    (
        r'^inet6 ([0-9a-z:]+)\s+prefixlen ([0-9]+)',
        ('ipv6', 'address', 'size'),
    ),
]


def _parse_regexes(regexes, lines):
    data = {
        'ipv4': {},
        'ipv6': {},
    }

    for line in lines:
        for regex, groups in regexes:
            matched = False
            matches = re.match(regex, line)
            if matches:
                for i, group in enumerate(groups[1:]):
                    data[groups[0]][group] = matches.group(i + 1)

                matched = True
                break

            if matched:
                break

    return data


class NetworkDevices(FactBase):
    '''
    Gets & returns a dict of network devices:

    .. code:: python

        'eth0': {
            'ipv4': {
                'address': '127.0.0.1',
                'netmask': '255.255.255.255',
                'broadcast': '127.0.0.13'
            },
            'ipv6': {
                'size': '64',
                'address': 'fe80::a00:27ff:fec3:36f0'
            }
        },
        ...
    '''

    command = 'ifconfig'
    default = dict

    # Definition of valid interface names for Linux:
    # https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/net/core/dev.c?h=v5.1.3#n1020
    _start_regexes = [
        (
            r'^([^/: \s]+)\s+Link encap:',
            lambda lines: _parse_regexes(nettools_1_regexes, lines),
        ),
        (
            r'^([^/: \s]+): flags=',
            lambda lines: _parse_regexes(nettools_2_regexes, lines),
        ),
    ]

    def process(self, output):
        devices = {}

        # Store current matches (start lines), the handler and any lines
        matches = None
        handler = None
        line_buffer = []

        for line in output:
            matched = False

            # Look for start lines
            for regex, new_handler in self._start_regexes:
                new_matches = re.match(regex, line)

                # If we find a start line
                if new_matches:
                    matched = True

                    # Assign any current matches with current handler, reset buffer
                    if matches:
                        devices[matches.group(1)] = handler(line_buffer)
                        line_buffer = []

                    # Set new matches/handler
                    matches = new_matches
                    handler = new_handler
                    break

            if not matched:
                line_buffer.append(line)

        # Handle any left over matches
        if matches:
            devices[matches.group(1)] = handler(line_buffer)

        return devices
