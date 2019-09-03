import sys, subprocess as sp
from .qs import echo
import os

def branch():
    echo(f'\n\033[93m>> branch ISSUE!\033[0m')

def abort():
    echo(f'\n\033[91m>> abort!\n\033[0m')
    os._exit(0)
    #sys.exit(1)

def warning(string=None):
    echo(f'\n\033[91m>> warning!: {string}\033[0m')

def ok(string=None):
    echo(f'\n\033[92m>> {string}\033[0m')

def execute(command_list, run=True, verbose=True):
    ''' Execute bash commands through shell '''
    for command in command_list:
        if verbose:
            echo(f'\033[94m>> execute: {command}\033[0m')
        if run == True:
            sp.run(command, shell=True)

def version(version):
    import six
    try:
        version = int(version)
        if not six.PY3:
            sp.call('echo "VERSION ERROR! PLEASE USE PYTHON 3.6.X or later"'\
                    , shell=True)
            sys.exit()
    except:
        sys.exit()
