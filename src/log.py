from . import issues
from .qs import getAnswer, isExist 
from .git import *

import sys
import cursor
import termios
import shutil
import random, string
import os

class CursorOff(object):
    def __enter__(self):
        cursor.hide()

    def __exit__(self, *args):
        cursor.show()

def wait_key():
    ''' Wait for a key press on the console and return it. '''
    result = None
    fd = sys.stdin.fileno()

    oldterm = termios.tcgetattr(fd)
    newattr = termios.tcgetattr(fd)
    newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
    termios.tcsetattr(fd, termios.TCSANOW, newattr)

    try:
        result = sys.stdin.read(1)
    except IOError:
        pass
    finally:
        termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)

    return result

def hr():
    hsize = shutil.get_terminal_size()[0]
    print(''.join(['\u2500' for _ in range(hsize)]),flush=True)

def decorate(string):
    hsize = shutil.get_terminal_size()[0]
    line = string if len(string) < hsize*0.8 else print(string[:int(hsize*0.95)])
    line = string.split(')')
    try:
        ret = f'{line[0].split("(")[0]}\033[32m({line[0].split("(")[1]})\033[0m '
        line = ')'.join(line[1:])
        line = line.split(']')
        chash = f'{line[0][1:]}'
        ret += f' \033[31m{line[0][1:]}]\033[0m '
        line = ']'.join(line[1:])
        line = line.split('>')
        ret += f' \033[36m{line[0][1:]}>\033[0m '
        line = '>'.join(line[1:])
        ret += f'\033[3m{line}\033[0m'
    except:
        ret = string
        chash = ''
    return ret, chash

def page(option):
    vsize = shutil.get_terminal_size()[1]
    hsize = shutil.get_terminal_size()[0]
    lpp = int(vsize / 2); #lines per page
    select = 0
    pagenum = 0
    start = 0
    end = lpp if len(option) > lpp else len(option)
    check = [idx for idx, _ in enumerate(option) if _.count('*')]
    while(1):
        hr()
        print("LOG VIEWER")
        hr()
        for idx, line in enumerate(option[start:end]):
            print('\033[2K\033[0m', end='')
            print('> ',end='') if start+idx==select else print('  ', end='')
            line, chash = decorate(line)
            print(line, end='\033[0m\n')
        hr()
        print(f'| \033[93m[hj]:[\u2190\u2193]', end = '')
        print(f',q:QUIT\033[0m\033[K',select,start,end)
        hr()
        ret = wait_key()
        while(1):
            if ret in ['j', 'k', 'l', 'h', 'q', 's', '\n']:
                break
            else:
                ret = wait_key()

        if ret == 'j':
            if select < len(option) - 1:
                select += 1
            k = 0
            while(option[select].count('*')==0):
                select+=1
                k += 1
            if select >= end and end < len(option):
                end += 1 + k
                start += 1 + k
        elif ret == 'k':
            if select > 0:
                select -= 1
            k = 0
            while(option[select].count('*')==0):
                select-=1
                k += 1
            if select < start:
                end -= (1 + k)
                start -= (1 + k)
        elif ret == 'q':
            sys.exit(0)
        print(f'\033[{lpp+7}A')

def displog():
    logcmd2 =  "git log --graph --all --pretty=format:'(%cr) [%h] <%an> %s' --abbrev-commit --date=relative --decorate=full "
    logout = sp.getoutput(logcmd2).split('\n')
    with CursorOff():
        page(logout)
