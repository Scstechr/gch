from . import issues
from os import path
from platform import platform
import sys
from .arg import ReturnArgdict


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
                next_arg = argv[idx+1]
                if len(next_arg):
                    if argv[idx+1][0] != '-' and argv[idx+1][:2] != '--':
                        d[arg] = argv[idx+1]
                else:
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
