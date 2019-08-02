import sys

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
        if lst[4] in ['True', 'False']:
            d['Default'] = lst[4]
        else:
            print('ERROR! on Default')
            sys.exit(1)
    else:
        d['Default'] = lst[4]

    return d

arglist = []
arglist.append(ArgSet(['-n', '--name',   'string', 'give name',   'Master']))
arglist.append(ArgSet(['-c', '--commit', 'flag',   'commiting',   'False']))
arglist.append(ArgSet(['-p', '--push',   'flag',   'push',        'False']))
arglist.append(ArgSet(['',   '--help',   'flag',   'help string', 'False']))

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

def Parse(argv):
    d = {}
    for idx in range(len(argv)):
        arg = argv[idx]
        if arg.count('--'):
            arg = arg[2:]
            if arg not in argdict.keys():
                print("ARG ERROR!", arg)
                sys.exit(1)
            if argdict[arg]['ArgType'] == 'flag':
                d[arg] = 'True'
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
                d[Name] = 'True'
                last_arg = a
            if idx+1 < len(argv) and not argv[idx+1].count('-'):
                if argdict[last_arg]['ArgType'] != 'string':
                    print("ARG ERROR!", last_arg)
                    sys.exit(1)
                d[last_arg] = argv[idx+1]
#print(argdict)
    for key, val in argdict.items():
        ProperName = val['ProperName']
        if ProperName not in d.keys():
            d[ProperName] = val['Default']
    return d

argv = sys.argv[1:]
d = Parse(argv)
Help()
print(d)

