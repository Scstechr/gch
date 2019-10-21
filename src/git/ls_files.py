from ..issues import execute
import subprocess as sp

BAR   = '\u2502'
TO    = '\u251C\u2500\u2500'
END   = '\u2514\u2500\u2500'
SPACE = '   '

LAYER = 5;

_LEVEL = [0 for _ in range(LAYER)]
_COUNT = [0, 0]

def iterateDict(d, s):
    temp = d
    for i in range(len(s)):
        temp[s[i]] = {}
        temp = temp[s[i]]

def parse(output):
    d = {}
    for line in output:
        s = line.strip().split("/")
        if len(s) < LAYER - 1:
            temp = d
            for idx, s_ in enumerate(s):
                if s_ not in temp:
                    iterateDict(temp, s[idx:])
                temp = temp[s_]
    return d

def PrintLayer(level, d, key, count):
    if key != '':
        if len(d[key].keys()):
            key += '/'
            count[0] += 1
        else:
            count[1] += 1
        if level < len(d) - 1:
            print(TO, key)
        else:
            print(END, key)

def PrintOut(temp, sp = ' ', l = 0):
    for key, val in temp.items():
        print(sp, end = '')
        PrintLayer(_LEVEL[l], temp, key, _COUNT)
        if val != {}:
            sep = BAR if _LEVEL[l] < len(temp) - 1 else ' '
            _LEVEL[l + 1] = 0;
            PrintOut(val, sp + sep + SPACE, l + 1)
        _LEVEL[l] += 1

def Ls():
    output = sp.run(['git', 'ls-files'], capture_output=True)
    output = str(output.stdout)[2:-1].split('\\n')[:-1]
    d = parse(output)
    print(' .')
    PrintOut(d)
    print(f'\n {_COUNT[0]} directory(s), {_COUNT[1]} file(s)')
