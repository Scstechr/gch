import sys
import subprocess as sp
import os
import cursor
from .colors import R, G, Y, C, M


def branch():
    print(f'\n{Y}>> branch ISSUE!{M}')


def abort():
    print(f'\n{R}>> abort!\n{M}', end='', file=sys.stderr)
    cursor.show()
    sp.call('stty sane', shell=True)
    os._exit(1)
    # sys.exit(1)


def exit():
    print(f'\n{G}>> exit!{M}')
    cursor.show()
    sp.call('stty sane', shell=True)
    sys.exit(0)


def warning(string=None):
    print(f'\n{R}>> warning!: {string}{M}')


def ok(string=None):
    print(f'\n{G}>> {string}{M}')


def execute(command_list, run=True, verbose=True):
    ''' Execute bash commands through shell '''
    for command in command_list:
        if verbose:
            print(f'{C}>> execute: {command}{M}')
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
