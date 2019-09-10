import sys
import subprocess as sp
from .qs import echo
import os
import cursor


def branch():
    echo(f'\n\033[93m>> branch ISSUE!\033[0m')


def abort():
    echo(f'\n\033[91m>> abort!\n\033[0m', end='')
    cursor.show()
    sp.call('stty sane', shell=True)
    os._exit(1)
    # sys.exit(1)


def exit():
    echo(f'\n\033[92m>> exit!\033[0m')
    cursor.show()
    sp.call('stty sane', shell=True)
    sys.exit(0)


def warning(string=None):
    echo(f'\n\033[91m>> warning!: {string}\033[0m')


def ok(string=None):
    echo(f'\n\033[92m>> {string}\033[0m')


def execute(command_list, run=True, verbose=True):
    ''' Execute bash commands through shell '''
    for command in command_list:
        if verbose:
            echo(f'\033[94m>> execute: {command}\033[0m')
        if run:
            sp.run(command, shell=True)


def version(version):
    import six
    try:
        version = int(version)
        if not six.PY3:
            sp.call('echo "Error! Please use Python 3.X"', shell=True)
            sys.exit()
    except ValueError:
        sys.exit()
