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

def ch_gen(string):
    ''' returns hash of commits'''
    if string != 'HEAD':
        return string[string.find('[')+1:string.find(']')]
    else:
        return 'HEAD'

def hr():
    hsize = shutil.get_terminal_size()[0]
    print(''.join(['\u2500' for _ in range(hsize)]),flush=True)

def page(selected, pages, pagenum):
    vsize = shutil.get_terminal_size()[1]
    hsize = shutil.get_terminal_size()[0]
    lpp = int(vsize / 2); #lines per page
    select = 0
    while(1):
        hr()
        print('selected:', selected) if len(selected) else print('')
        hr()
        pagelen = len(pages[pagenum])
        if select > pagelen:
            select = pagelen - 1;
        for idx, opt in enumerate(pages[pagenum]):
            commit_hash = ch_gen(opt)
            print('\033[2K', end='')
            if len(selected) != 2:
                print('> ', end='') if idx == select else print('', end='')
            if commit_hash in selected:
                print('\033[2m', opt, '\033[0m')
            else:
                print(opt)
        for i in range(lpp-pagelen):
            print('\033[2K')
        hr()
        print(f'\t[{pagenum+1}/{len(pages)}]')
        hr()
        if len(selected) != 2:
            ret = wait_key()
            while(1):
                if ret in ['j', 'k', 'h', 'l', '\n']:
                    break
                else:
                    ret = wait_key()

        if ret == 'j' and select < pagelen - 1:
            select += 1
        elif ret == 'k' and select > 0:
            select -= 1
        elif ret == 'h' and pagenum > 0:
            pagenum -= 1
        elif ret == 'l' and pagenum < len(pages) - 1:
            pagenum += 1
        elif ret == '\n':
            if len(selected) == 2:
                break
            else:
                commit_hash = ch_gen(pages[pagenum][select])
                if commit_hash not in selected:
                    selected.append(commit_hash)

        print(f'\033[{lpp+6}A', end='')
        
def book(selected, options):
    vsize = shutil.get_terminal_size()[1]
    lpp = int(vsize / 2); #lines per page
    pages = []
    if len(options) > lpp:
        for i in range(0, len(options), lpp):
            pages.append(options[i:i+lpp])
    else:
        pages = [options]
    page(selected, pages, 0)

@click.command()
@click.option('-d', '--detail', is_flag='False', help='detailed diff')
@click.option('-h', '--head', is_flag='False', help='include head')
def diffhash(detail, head):
    vsize = shutil.get_terminal_size()[1]
    hsize = shutil.get_terminal_size()[0]
    options = []
    if isExist(f'git status --short'):
        options += ['HEAD']
    else:
        click.echo('Clean State')

    threshold = 100
    fstring = '(%ad) [%h] %an :%s' if hsize > threshold else '(%ad) [%h] : %s'
    dateset = 'local' if hsize > threshold else 'relative'
    options += sp.getoutput(f'git log --date={dateset} --pretty=format:"{fstring}"').split('\n')
    options = [f'{opt[:hsize-5]}...' if len(opt) > hsize - 2 else opt for opt in options]
    selected = []
    if head and 'HEAD' in options:
        selected.append('HEAD')
        options = options[1:]
    book(selected, options)

    diffhash = ''
    if 'HEAD' in selected:
        diffhash = selected[0] if selected[0] != 'HEAD' else selected[1]
        issues.execute([f'git diff --stat {diffhash}'])
        if detail:
            issues.execute([f'git diff --ignore-blank-lines -U1 {diffhash}'])
    else:
        issues.execute([f'git diff --stat {selected[0]}..{selected[1]}'])
        if detail:
            issues.execute([f'git diff --ignore-blank-lines -U1 {selected[0]}..{selected[1]}'])
    return diffhash

if __name__ == '__main__':
    getdiffhash()
