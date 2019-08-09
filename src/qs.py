import subprocess as sp
from . import issues
import sys

def echo(string):
    print(string)

def prompt(string, _type=str):
    try:
        ret = input(string+': ')
    except (KeyboardInterrupt, EOFError):
        issues.abort()
    while(1):
        if type(ret) == _type:
            break
        print('\033[1A',end='')
        try:
            ret = input(string+': ')
        except (KeyboardInterrupt, EOFError):
            issues.abort()
    return ret

def getAnswer(lst):
    ''' Generates selection list and answering sequence '''
    while(1):
        [echo(f'{idx+1}: {option}') for idx, option in enumerate(lst)]
        answer = prompt('Answer')
        try:
            answer = int(answer)
            if answer > 0 and answer <= len(lst):
                break
            issues.warning('Please choose right answer from below:')
        except:
            issues.warning('Please enter integer!')
    return answer

def isExist(command):
    output = sp.getoutput(command)
    flag = False if len(output) == 0 else True
    return flag

def confirm(string):
    flag = True
    try:
        ret = input(string+' [Y/n]:').lower()
        while(1):
            if ret in ['yes', 'y']:
                break
            if ret in ['no', 'n', '']:
                flag = False
                break
            print('\033[1A',end='')
            ret = input(string+' [Y/n]:').lower()
    except (KeyboardInterrupt, EOFError):
        issues.abort()
    return flag


