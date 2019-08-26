from os import path
import sys
from .version import *
from . import issues

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
defaults['checkout'] = False
defaultspath = path.join(".", ".defaults.txt")
gitpath = path.join(".", ".git")
if path.exists(defaultspath):
    if not path.exists(gitpath):
        issues.execute([f'rm .defaults.txt'])
    else:
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
exp_h=f'Show this message and exit.'

gch_exp_c=f'Commit'
gch_exp_p=f'Push.'
gch_exp_i=f'Run initializer'
gch_exp_g=f'Path of dir that contains `.git`.'
gch_exp_f=f'Path/Regex of staging file/dir.'
gch_exp_b=f'Commiting branch.'
gch_exp_v=f'Verbose option.'
gch_exp_l=f'Git log with option.'
gch_exp_r=f'Reset all changes since last commit.'
gch_exp_e=f'Choose which remote repo.to push.'
gch_exp_p2=f'Fetch + Merge from {defaults["remote"]}:{defaults["branch"]}.'
gch_exp_s=f'Save settings'
gch_exp_d=f'Open diff tool'
gch_exp_v2=f'Check version of gch'
gch_exp_c2=f'Handling checkouts'

gdiff_exp_v  = f'Detailed diff.'
gdiff_exp_h  = f'Include HEAD^ from the beginning.'
gdiff_exp_a  = f'Name specific author.'
gdiff_exp_l  = f'User log ver. instead.'
gdiff_exp_v2 = f'Check version of gdiff.'

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

def ReturnArgdict(mode):
    arglist = []
    if mode:
        arglist.append(ArgSet(['-v', '--verbose', 'flag', gdiff_exp_v,  False]))
        arglist.append(ArgSet(['-h', '--head',    'flag', gdiff_exp_h,  False]))
        arglist.append(ArgSet(['-a', '--author',  'flag', gdiff_exp_a,  False]))
        arglist.append(ArgSet(['-l', '--log',     'flag', gdiff_exp_l,  False]))
        arglist.append(ArgSet(['',   '--version', 'flag', gdiff_exp_v2, False]))
    else:
        arglist.append(ArgSet(['-i', '--init',     'flag',   gch_exp_i,  defaults['init']]))
        arglist.append(ArgSet(['-v', '--verbose',  'flag',   gch_exp_v,  defaults['verbose']]))
        arglist.append(ArgSet(['-l', '--log',      'flag',   gch_exp_l,  defaults['log']]))
        arglist.append(ArgSet(['-r', '--remote',   'string', gch_exp_e,  defaults['remote']]))
        arglist.append(ArgSet(['-g', '--gitpath',  'string', gch_exp_g,  defaults['gitpath']]))
        arglist.append(ArgSet(['-f', '--filepath', 'string', gch_exp_f,  defaults['filepath']]))
        arglist.append(ArgSet(['-b', '--branch',   'string', gch_exp_b,  defaults['branch']]))
        arglist.append(ArgSet(['-c', '--commit',   'flag',   gch_exp_c,  defaults['commit']]))
        arglist.append(ArgSet(['-p', '--push',     'flag',   gch_exp_p,  defaults['push'], ]))
        arglist.append(ArgSet(['-s', '--save',     'flag',   gch_exp_s,  False]))
        arglist.append(ArgSet(['-d', '--diff',     'flag',   gch_exp_d,  defaults['diff']]))
        arglist.append(ArgSet(['',   '--checkout', 'flag',   gch_exp_c2, defaults['checkout']]))
        arglist.append(ArgSet(['',   '--reset',    'flag',   gch_exp_r,  defaults['reset']]))
        arglist.append(ArgSet(['',   '--pull',     'flag',   gch_exp_p2, defaults['pull']]))
        arglist.append(ArgSet(['',   '--version',  'flag',   gch_exp_v2, defaults['reset']]))
    arglist.append(ArgSet(['','--help', 'flag', exp_h, False]))

    argdict = {}
    for arg in arglist:
        key = arg['ProperName']
        argdict[key] = arg
        if arg['ShortName'] != '':
            key_s = arg['ShortName']
            argdict[key_s] = arg
    return argdict

def Help(mode):
    argdict = ReturnArgdict(mode)
    command = 'gdiff' if mode else 'gch'
    
    print(f"\033[1m{command} v{VERSION} (compiled: {DATE})\033[0m")
    print(f"\033[1mUsage: {command} [OPTION]\n\nOptions:\033[0m")
    for key, value in argdict.items():
        if len(key) > 1:
            string = '  '
            if len(value['ShortName']) > 0:
                string += '-' + value['ShortName'] + ', --' + value['ProperName']
            else:
                string += '--' + value['ProperName']
            string = '\033[1m' + f'{string}'.ljust(20) + f"| \033[0m{value['ExplainString']}"
            print(string)
    sys.exit()
