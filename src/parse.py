from os import path
from platform import platform
import sys
from datetime import datetime
from .arg import ReturnArgdict
import subprocess as sp
VERSION = '1.16'

date = str(datetime.utcnow())[:-7] + ' UTC'

PYTHON_VERSION = sys.version.split(' ')[0]
PLATFM_VERSION = platform()

string = sp.run(['PyInstaller','--version'],capture_output=True).stdout.strip()
string = string.decode('utf-8')
PYINST_VERSION = string

def Require(arg):
    print("ARG ERROR! ", arg, "REQUIRES ADDITIONAL STRING")
    sys.exit(1)

def NotFound(arg):
    print("ARG ERROR!", arg, "NOT FOUND")
    sys.exit(1)

def Error():
    print("ARG ERROR!")
    sys.exit(1)

def Version(string):
    print(f"\033[1m{string} v{VERSION} ({date})\033[0m")
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
        if arg.count('--') == 1 and arg[:2] == '--':
            arg = arg[2:]
            if arg not in argdict.keys():
                NotFound(arg)
            if argdict[arg]['ArgType'] == 'flag':
                d[arg] = True
            else:
                d[arg] = argdict[arg]['Default']
                if idx+1 < len(argv) and argv[idx+1].count('-') == 0:
                    d[arg] = argv[idx+1]
        elif arg.count('-') == 1 and arg[0] == '-':
            last_arg = arg[-1]
            if len(arg) > 2:
                for a in arg[1:]:
                    if a not in argdict.keys():
                        NotFound(a)
                    Name = argdict[a]['ProperName']
                    if argdict[Name]['ArgType'] == 'flag':
                        d[Name] = True
                    else:
                        Require(a)
                    last_arg = a
            if idx+1 < len(argv):
                Name = argdict[last_arg]['ProperName']
                if argv[idx+1][0] != '-' and argv[idx+1][:2] != '--':
                    d[Name] = argv[idx+1]
                else:
                    if argdict[Name]['ArgType'] != 'string':
                        d[Name] = True
                    else:
                        Require(last_arg)
    for key, val in argdict.items():
        ProperName = val['ProperName']
        if ProperName not in d.keys():
            d[ProperName] = val['Default']
    return d


if __name__ == '__main__':
    Parser()
