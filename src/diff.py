#!/usr/bin/env python
'''
==================
Git Diff Handler
==================
'''

import click
import subprocess as sp
import sys
import cursor
import termios
import shutil
import random, string
import os

from . import issues
from .qs import getAnswer, isExist 
from .git import *

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

def ch_gen(string):
    ''' returns hash of commits'''
    if string != 'HEAD':
        return string[string.find('[')+1:string.find(']')]
    else:
        return 'HEAD'

def hr():
    hsize = shutil.get_terminal_size()[0]
    print(''.join(['\u2500' for _ in range(hsize)]),flush=True)

def decorate(string):
    hsize = shutil.get_terminal_size()[0]
    line = string if len(string) < hsize*0.8 else f'{string[:int(hsize*0.95)]} ...'
    line = string.split(')')
    try:
        ret = f'{line[0].split("(")[0]}\033[0m({line[0].split("(")[1]})\033[0m '
        line = ')'.join(line[1:])
        line = line.split(']')
        chash = f'{line[0][2:]}'
        ret += f'\033[31m{line[0][1:]}]\033[0m '
        line = ']'.join(line[1:])
        line = line.split('>')
        ret += f'\033[36m{line[0][1:]}>\033[0m'
        line = '>'.join(line[1:])
        ret += f'\033[3m{line}\033[0m'
    except:
        ret = string
        chash = ''
    return ret, chash

def page(verbose, selected, pages):
    vsize = shutil.get_terminal_size()[1]
    hsize = shutil.get_terminal_size()[0]
    lpp = int(vsize / 2); #lines per page
    select = 0
    pagenum = 0
    while(1):
        hr()
        pagelen = len(pages[pagenum])
        print('\033[2K\033[92mSELECTED:', selected, end ='\033[0m ')
        print('| \033[91m[VERBOSE]\033[0m') if verbose else print()
        hr()
        for idx, opt in enumerate(pages[pagenum]):
            line, commit_hash = decorate(opt)
            if len(opt) > hsize - 4:
                opt = opt[:hsize-5] + '...'
            print('\033[2K', end='')
            print('>', end=' ') if idx == select else print(' ', end=' ')
            if commit_hash in selected:
                print(f'\033[2m{opt}\033[0m')
            else:
                print(line)
        for i in range(lpp-pagelen):
            print('\033[2K')
        hr()
        print(f'[{pagenum+1}/{len(pages)}]', end = ' ')
        print(f'| \033[93m[hjkl]:[\u2190\u2193\u2191\u2192]', end = '')
        print(f',q:QUIT,v:VERBOSE,s/Enter:SELECT\033[0m')
        hr()
        if len(selected) != 2:
            ret = wait_key()
            while(1):
                if ret in ['j', 'k', 'h', 'l', 'q', 'v', 's', '\n']:
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
            if select > len(pages[pagenum]):
               select = len(pages[pagenum]) - 1
        elif ret == 'q':
            sys.exit(0)
        elif ret == 'v':
            verbose = False if verbose else True
        elif ret in ['\n', 's'] :
            if len(selected) == 2:
                break
            else:
                commit_hash = ch_gen(pages[pagenum][select])
                if commit_hash not in selected:
                    selected.append(commit_hash)
                else:
                    selected.pop()

        print(f'\033[{lpp+6}A', end='')
    return verbose
        
def book(verbose, selected, options):
    vsize = shutil.get_terminal_size()[1]
    lpp = int(vsize / 2); #lines per page
    pages = []
    if len(options) > lpp:
        for i in range(0, len(options), lpp):
            pages.append(options[i:i+lpp])
    else:
        pages = [options]
    return page(verbose, selected, pages)

def diffhash(verbose, head, author):
    ret_diffhash = ''
    if author:
        ret_author = click.prompt("Name specific author", type=str)
    while(1):
        vsize = shutil.get_terminal_size()[1]
        hsize = shutil.get_terminal_size()[0]
        options = []
        if isExist(f'git status --short') or head:
            options += ['HEAD']

        threshold = 100
        randstr = ''.join([random.choice(string.ascii_letters + string.digits) for i in range(8)])
        fstring = randstr.join(['(%ad)','[%h]','<%an>', '%s'])
        dateset = 'local' if hsize > threshold else 'relative'
        options += sp.getoutput(f'git log --date={dateset} --pretty=format:"{fstring}"').split('\n')
        tempopt = []
        if options[0] == 'HEAD':
            tempopt.append('HEAD')
        for opt in options[len(tempopt):]:
            opt = opt.split(randstr)
            authr = opt[2][1:-1]
            optstr = ' '.join(opt)
            if author:
                if ret_author == authr:
                    tempopt.append(optstr)
            else:
                optstr = ' '.join(opt)
                tempopt.append(optstr)
        options = [opt for opt in tempopt]
        if len(options) < 2:
            issues.warning('No log found for comparing')
            sys.exit(1)
        selected = []
        if head and 'HEAD' in options:
            selected.append('HEAD')
            options = options[1:]
        with CursorOff():
            verbose = book(verbose, selected, options)

        ret_diffhash = ''

        if 'HEAD' in selected:
            ret_diffhash = selected[0] if selected[0] != 'HEAD' else selected[1]
            issues.execute([f'git diff --stat {ret_diffhash}'])
            if verbose:
                issues.execute([f'git diff --ignore-blank-lines -U1 {ret_diffhash}'])
        else:
            issues.execute([f'git diff --stat {selected[0]}..{selected[1]}'])
            if verbose:
                issues.execute([f'git diff --ignore-blank-lines -U1 {selected[0]}..{selected[1]}'])
        if head:
            break
        else:
            if click.confirm('\nDo you want to exit diff hash tool?'):
                sys.exit(0)
            else:
                for i in range(vsize):
                    print(f'\033[2K\033[1A', end='')

    return ret_diffhash

@click.command()
@click.option('-v', '--verbose', is_flag='False', help='detailed diff')
@click.option('-h', '--head', is_flag='False', help='include head')
@click.option('-a', '--author', is_flag='False', help='name specific author')
def main(verbose, head, author):
    diffhash(verbose, head, author)

if __name__ == '__main__':
    main()
