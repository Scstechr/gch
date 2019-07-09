#!/usr/bin/env python
'''
==================
Git Log Handler
==================
'''

import click
import subprocess as sp
import sys
import cursor
import termios
import shutil

from pysrc import issues
from pysrc.qs import getAnswer, isExist 
from pysrc.git import *

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

@click.command()
@click.option('-d', '--detail', is_flag='False', help='detailed diff')
def main(detail):
#proc_return = sp.run(["cat", "sample.txt"], stdout=sp.PIPE).stdout.decode('cp932')
    options = []
    if isExist(f'git status --short'):
        options += ['HEAD']
    else:
        click.echo('Clean State')
    options += sp.getoutput('git log --date=relative --pretty=format:"(%ad) [%h] %an :%s"').split('\n')
        
    select = 0
    selected = []
    while(1):
        vsize = shutil.get_terminal_size()[1]
        print('selected:', selected) if len(selected) else print('')
        print('---------------------------------------------------')
        for idx, opt in enumerate(options):
            print('\033[2K', end='')
            if len(selected) != 2:
                print('> ', end='') if idx == select else print('', end='')
            print(opt)
        if len(selected) != 2:
            ret = wait_key()
            while(1):
                if ret in ['j', 'k', '\n']:
                    break
                else:
                    ret = wait_key()

        if ret == 'j' and select < len(options) - 1:
            select += 1
        elif ret == 'k' and select > 0:
            select -= 1
        elif ret == '\n':
            if len(selected) == 2:
                break
            else:
                if select:
                    string = options[select]
                    commit_hash = string[string.find('[')+1:string.find(']')]
                    selected.append(commit_hash)
                else:
                    selected.append('HEAD')

        print(f'\033[{len(options)+2}A', end='')

    print("show diff?[y/n]:")
    ret = wait_key()
    while(1):
        if ret == 'y':
            issues.execute([f'git add .'])
            if selected[1] == 'HEAD':
                selected[1] = selected[0]
                selected[0] = 'HEAD'
            issues.execute([f'git diff {selected[0]}..{selected[1]}'])
            #issues.execute([f'git diff --ignore-blank-lines -U1 --color-words {selected[0]}..{selected[1]}'])
            issues.execute([f'git reset'])

            break
        elif ret == 'n':
            break
        else:
            ret = wait_key()

if __name__ == '__main__':
    main()
