import subprocess as sp
from . import issues
from .util import *
import sys

def echo(string):
    print(string)

def prompt(string, _type=str):
    ret = input(string+': ')
    while(1):
        if type(ret) == _type:
            break
        print('\033[1A',end='')
        ret = input(string+': ')
    return ret

def getAnswer(lst):
    ''' Generates selection list and answering sequence '''
    with CursorOff():
        while(1):
            [echo(f' {chr(97+idx)}) {option}') for idx, option in enumerate(lst)]
            ans = [chr(97+idx) for idx, _ in enumerate(lst)]
        #    print("Type the answer:")
            answer = wait_key()
            if answer in ans:
                answer = ord(answer) - 97 + 1
                break
            else:
                issues.warning('Please choose right answer from above!')
    return answer

def isExist(command):
    output = sp.getoutput(command)
    flag = False if len(output) == 0 else True
    return flag

def confirm(string):
    flag = True
    ret = input(">> " +  string + ' [Y/n]:').lower()
    while(1):
        if ret in ['yes', 'y']:
            break
        if ret in ['no', 'n', '']:
            flag = False
            break
        print('\033[1A',end='')
        ret = input(string+' [Y/n]:').lower()
    return flag
