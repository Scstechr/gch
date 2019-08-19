from . import issues
from os import path
from platform import platform
import sys
from .arg import ReturnArgdict

VERSION = '1.21'
DATE = "2019-08-19 UTC"
PYTHON_VERSION = '3.7.3'
PLATFM_VERSION = 'Darwin-18.0.0-x86_64-i386-64bit'
PYINST_VERSION = '3.5'

def Require(arg):
    f = 'Argument "\033[3m' + arg + '\033[0m\033[91m" requires additional string.'
    issues.warning(f)
    sys.exit(1)

def NotFound(arg):
    f = 'Argument "\033[3m' + arg + '\033[0m\033[91m" not found.'
    issues.warning(f)
    sys.exit(1)

def Error():
    f = "Argument error!"
    issues.warning(f)
    sys.exit(1)

def Version(string):
    print(f"\033[1m{string} v{VERSION} (compiled: {DATE})\033[0m")
    print(f"\033[0mBUILD INFO: \033[0m")
    # Python version
    version = PYTHON_VERSION
    print(f"\033[0m Python      :\033[0m", version)

    # PyInstaller version
    version = PYINST_VERSION
    print(f"\033[0m PyInstaller :\033[0m", version)

    # Platform version (Kernel)
    version = PLATFM_VERSION
    print(f"\033[0m Platform    :\033[0m", version)

    sys.exit(0)

def genname(argdict, arg):
    names = '-' + argdict[arg]['ShortName']
    names += '/--' + argdict[arg]['ProperName']
    return names

def DictSet(d, argdict, argv, arg, idx):
    if arg not in argdict.keys():
        if len(arg) > 1:
            NotFound('--' + arg)
        else:
            NotFound('-' + arg)
    else:
        names = genname(argdict, arg)
        arg = argdict[arg]['ProperName']
        if argdict[arg]['ArgType'] == 'flag':
            d[arg] = True
        else:
            d[arg] = argdict[arg]['Default']
            if idx+1 < len(argv):
                if argv[idx+1][0] != '-' and argv[idx+1][:2] != '--':
                    d[arg] = argv[idx+1]
            else:
                Require(names)

def Parser(mode):
    argdict = ReturnArgdict(mode)

    argv = sys.argv[1:]
    d = {}
    for idx in range(len(argv)):
        arg = argv[idx]
        if arg.count('--') == 1 and arg[:2] == '--':
            DictSet(d, argdict, argv, arg[2:], idx)
        elif arg.count('-') == 1 and arg[0] == '-':
            arg = [a for a in arg[1:]]
            sarg = [a for a in arg if argdict[a]['ArgType'] == 'string']
            if len(sarg) > 1:
                Error()
            if len(sarg) == 1 and argdict[arg[-1]]['ArgType'] != 'string':
                Error()
            
            for a in arg:
                DictSet(d, argdict, argv, a, idx)
    for key, val in argdict.items():
        ProperName = val['ProperName']
        if ProperName not in d.keys():
            d[ProperName] = val['Default']
    return d


if __name__ == '__main__':
    Parser()
