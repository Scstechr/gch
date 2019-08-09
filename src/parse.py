from os import path
from platform import platform
import sys
from .arg import ReturnArgdict
import subprocess as sp
VERSION = '1.13'

PYTHON_VERSION = sys.version.split('\n')[0]
PLATFM_VERSION = platform()

string = sp.run(['PyInstaller','--version'],capture_output=True).stdout.strip()
string = string.decode('utf-8')
PYINST_VERSION = string

def Version(string):
    print(f"\033[1m{string} v{VERSION}\033[0m")
    print(f"\033[1mBUILD INFO: \033[0m")
    # Python version
    version = PYTHON_VERSION
    print(f"\033[1m Python      :\033[0m", version)

    # PyInstaller version
    version = PYINST_VERSION
    print(f"\033[1m PyInstaller :\033[0m", version)

    # Platform version (Kernel)
    version = PLATFM_VERSION
    print(f"\033[1m Platform    :\033[0m", version)

    sys.exit(0)

def Parser(mode):
    argdict = ReturnArgdict(mode)

    argv = sys.argv[1:]
    d = {}
    for idx in range(len(argv)):
        arg = argv[idx]
        if arg.count('--'):
            arg = arg[2:]
            if arg not in argdict.keys():
                print("ARG ERROR!", arg)
                sys.exit(1)
            if argdict[arg]['ArgType'] == 'flag':
                d[arg] = True
            else:
                d[arg] = argdict[arg]['Default']
                if idx+1 < len(argv) and argv[idx+1].count('-') == 0:
                    d[arg] = argv[idx+1]
        elif arg.count('-'):
            last_arg = ''
            for a in arg[1:]:
                if a not in argdict.keys():
                    print("ARG ERROR!", a)
                    sys.exit(1)
                Name = argdict[a]['ProperName']
                if argdict[Name]['ArgType'] == 'flag':
                    d[Name] = True
                else:
                    print("ARG ERROR!", a)
                    sys.exit(1)
                last_arg = a
            if idx+1 < len(argv) and not argv[idx+1].count('-'):
                Name = argdict[a]['ProperName']
                if argdict[Name]['ArgType'] != 'string':
                    print("ARG ERROR!", last_arg)
                    sys.exit(1)
                d[Name] = argv[idx+1]
    for key, val in argdict.items():
        ProperName = val['ProperName']
        if ProperName not in d.keys():
            d[ProperName] = val['Default']
    return d


if __name__ == '__main__':
    Parser()
