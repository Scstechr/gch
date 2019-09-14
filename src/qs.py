import subprocess as sp
from contextlib import suppress
from .util import CursorOff, wait_key
from . import issues
from .colors import R, G, Y, B, P, C, GR, BL, TH, IT, M


def cinput(string):
    ret = ''
    with suppress(KeyboardInterrupt):
        ret = input(string + ': ')

    return ret


def prompt(string, _type=str):
    ret = cinput(string)
    while(1):
        if type(ret) == _type:
            break
        print('1A', end='')
        ret = cinput(string)
    return ret


def getAnswer(lst, exit=False):
    ''' Generates selection list and answering sequence '''
    with CursorOff():
        if exit:
            lst.append("exit")
        while(1):
            [print(f' {chr(97+idx)}) {option}')
             for idx, option in enumerate(lst)]
            ans = [chr(97 + idx) for idx, _ in enumerate(lst)]
        #    print("Type the answer:")
            answer = wait_key()
            if answer in ans:
                answer = ord(answer) - 97 + 1
                break
            elif answer is None:
                issues.abort()
            else:
                print(f"What you entered: `{answer}`")
                issues.warning('Please choose right answer from above!')
        if answer == len(lst) and exit:
            issues.exit()
    return answer


def isExist(command):
    output = sp.getoutput(command)
    flag = False if len(output) == 0 else True
    return flag


def confirm(string):
    flag = True
    with suppress(KeyboardInterrupt):
        ret = input(f"m{C}>> " + string + f' [Y/n]:{M}').lower()
        while(1):
            if ret in ['yes', 'y']:
                break
            if ret in ['no', 'n', '']:
                flag = False
                break
            print('1A', end='')
            ret = input(string + ' [Y/n]:').lower()
    return flag
