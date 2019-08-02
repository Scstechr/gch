from os import path, chdir, getcwd
import sys

defaults = {}
defaults['init'] = False
defaults['gitpath'] = '.'
defaults['filepath'] = '.'
defaults['branch'] = 'master'
defaults['verbose'] = False
defaults['log'] = False
defaults['commit'] = False
defaults['reset'] = False
defaults['push'] = False
defaults['remote'] = 'origin'
defaults['pull'] = False
defaults['diff'] = False
defaults['version'] = False
defaultspath = path.join(".", ".defaults.txt")
if path.exists(defaultspath):
    with open(defaultspath, 'r') as readfile:
        for line in readfile:
            k, v = line.replace('\n','').split(":")
            if v != 'None':
                defaults[str(k)] = str(v)
            if v == 'True':
                defaults[str(k)] = True
            if v == 'False':
                defaults[str(k)] = False

# Explanation of the options showed in --help flag
exp_c=f'Commit'
exp_p=f'Push.'
exp_i=f'Run initializer'
exp_g=f'Path of dir that contains `.git`.'
exp_f=f'Path/Regex of staging file/dir.'
exp_b=f'Commiting branch.'
exp_v=f'Verbose option.'
exp_l=f'Git log with option.'
exp_r=f'Reset all changes since last commit.'
exp_e=f'Choose which remote repo.to push.'
exp_p2=f'Fetch + Merge from {defaults["remote"]}:{defaults["branch"]}.'
exp_s=f'Save settings'
exp_d=f'Open diff tool'
exp_v2=f'Check version of gch'
exp_h=f'Show this message and exit.'

def ArgSet(lst):
    d = {}
    if len(lst[0]) == 2 and lst[0].count('-') == 1:
        d['ShortName'] = lst[0][1:]
    elif len(lst[0]) == 0:
        d['ShortName'] = lst[0]
    else:
        print('ERROR! on ShortName')
        sys.exit(1)

    if lst[1].count('-') == 2 and lst[1][:2] == '--':
        d['ProperName'] = lst[1][2:]
    
    if lst[2] in ['string', 'flag']:
        d['ArgType'] = lst[2]

    d['ExplainString'] = lst[3]

    if d['ArgType'] == 'flag':
        if lst[4] in [True, False]:
            d['Default'] = lst[4]
        else:
            print('ERROR! on Default!', d)
            sys.exit(1)
    else:
        d['Default'] = lst[4]

    return d

arglist = []
arglist.append(ArgSet(['-i', '--init',     'flag',   exp_i,  defaults['init']]))
arglist.append(ArgSet(['-v', '--verbose',  'flag',   exp_v,  defaults['verbose']]))
arglist.append(ArgSet(['-l', '--log',      'flag',   exp_l,  defaults['log']]))
arglist.append(ArgSet(['-r', '--remote',   'string', exp_e,  defaults['remote']]))
arglist.append(ArgSet(['-g', '--gitpath',  'string', exp_g,  defaults['gitpath']]))
arglist.append(ArgSet(['-f', '--filepath', 'string', exp_f,  defaults['filepath']]))
arglist.append(ArgSet(['-b', '--branch',   'string', exp_b,  defaults['branch']]))
arglist.append(ArgSet(['-c', '--commit',   'flag',   exp_c,  defaults['commit']]))
arglist.append(ArgSet(['-p', '--push',     'flag',   exp_p,  defaults['push'], ]))
arglist.append(ArgSet(['-s', '--save',     'flag',   exp_s,  False]))
arglist.append(ArgSet(['-d', '--diff',     'flag',   exp_d,  defaults['diff']]))
arglist.append(ArgSet(['','--version',     'flag',   exp_v2, defaults['reset']]))
arglist.append(ArgSet(['','--reset',       'flag',   exp_r,  defaults['reset']]))
arglist.append(ArgSet(['','--pull',        'flag',   exp_p2, defaults['pull']]))
arglist.append(ArgSet(['-h','--help',      'flag',   exp_h,  defaults['pull']]))

argdict = {}
for arg in arglist:
    key = arg['ProperName']
    argdict[key] = arg
    if arg['ShortName'] != '':
        key_s = arg['ShortName']
        argdict[key_s] = arg

def Help():
    print("Usage: command [OPTION]\n\nOptions")
    for key, value in argdict.items():
        if len(key) > 1:
            string = '  '
            if len(value['ShortName']) > 0:
                string += '-' + value['ShortName'] + ', --' + value['ProperName']
            else:
                string += '--' + value['ProperName']
            string = f'{string}'.ljust(20) + f"{value['ExplainString']}"
            print(string)
    sys.exit()

def Parser():
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
                d[Name] = True
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
