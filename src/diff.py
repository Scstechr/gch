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

from . import issues
from .qs import getAnswer, isExist 
from .git import *


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
        print('selected:', selected)
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
        print(f'[{pagenum+1}/{len(pages)}]')
        hr()
        if len(selected) != 2:
            ret = wait_key()
            while(1):
                if ret in ['j', 'k', 'h', 'l', 'q', '\n']:
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
        elif ret == 'q':
            if click.confirm('Do you want to exit diff hash tool?'):
                sys.exit(0)
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

def authorcheck(opt, name):
    author_str = opt.strip()
    author_str = opt.split(']')[1]
    author_str = author_str[:author_str.rfind(' :')][1:]
    if author_str == name:
        return True
    else:
        return False

def diffhash(detail, head, author):
    vsize = shutil.get_terminal_size()[1]
    hsize = shutil.get_terminal_size()[0]
    options = []
    if isExist(f'git status --short') or head:
        options += ['HEAD']
    else:
        issues.ok('Clean State')

    threshold = 100
    fstring = '(%ad) [%h] %an :%s' if hsize > threshold else '(%ad) [%h] : %s'
    dateset = 'local' if hsize > threshold else 'relative'
    options += sp.getoutput(f'git log --date={dateset} --pretty=format:"{fstring}"').split('\n')
    options = [f'{opt[:hsize-5]}...' if len(opt) > hsize - 2 else opt for opt in options]
    if author:
        ret_author = click.prompt("Name specific author", type=str)
        if len(ret_author):
            if options[0] == 'HEAD':
                options = [opt for opt in options[1:] if authorcheck(opt, ret_author)]
                options = ['HEAD'] + options
            else:
                options = [opt for opt in options if authorcheck(opt, ret_author)]
    if len(options) < 2:
        issues.warning('No log found for comparing')
        sys.exit(1)
    selected = []
    if head and 'HEAD' in options:
        selected.append('HEAD')
        options = options[1:]
    book(selected, options)

    ret_diffhash = ''
    if 'HEAD' in selected:
        ret_diffhash = selected[0] if selected[0] != 'HEAD' else selected[1]
        issues.execute([f'git diff --stat {ret_diffhash}'])
        if detail:
            issues.execute([f'git diff --ignore-blank-lines -U1 {ret_diffhash}'])
    else:
        issues.execute([f'git diff --stat {selected[0]}..{selected[1]}'])
        if detail:
            issues.execute([f'git diff --ignore-blank-lines -U1 {selected[0]}..{selected[1]}'])
    return ret_diffhash

@click.command()
@click.option('-d', '--detail', is_flag='False', help='detailed diff')
@click.option('-h', '--head', is_flag='False', help='include head')
@click.option('-a', '--author', is_flag='False', help='name specific author')
def main(detail, head, author):
    diffhash(detail, head, author)

if __name__ == '__main__':
    main()
