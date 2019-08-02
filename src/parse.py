from os import path
import sys
from .arg import ReturnArgdict
VERSION = '1.20'

def Version(string):
    print(string, f"v{VERSION}")
    print("Build    : Python 3.6.8, PyInstaller 3.5")
    print("Platform : Darwin-16.7.0-x86_64-i386-64bit")
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
