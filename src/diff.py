import subprocess as sp
import sys
import random
import string
import os

from . import issues
from .qs import getAnswer, isExist, confirm, prompt
from .git import *
from .util import *


def ch_gen(string):
    ''' returns hash of commits'''
    if string != 'HEAD':
        return string[string.find('[')+1:string.find(']')]
    else:
        return 'HEAD'


def hr():
    hsize = shutil.get_terminal_size()[0]
    print(''.join(['\u2500' for _ in range(hsize)]), flush=True)


def decorate(string):
    line = string.split(')')
    try:
        ret = f'{line[0].split("(")[0]}\033[0m({line[0].split("(")[1]})\033[0m '
        line = ')'.join(line[1:])
        line = line.split(']')
        chash = f'{line[0][2:]}'
        ret += f'\033[30G\033[31m{line[0][1:]}]\033[0m '
        line = ']'.join(line[1:])
        line = line.split('>')
        ret += f'\033[36m{line[0][1:]}>\033[0m'
        line = '>'.join(line[1:])
        ret += f'\033[3m{line}\033[0m'
    except:
        ret = string
        chash = ''
        if string.count('HEAD'):
            chash = 'HEAD'

    ast = ret.find('*') + 1
    ret = ret[:ast].replace('*', '\033[1m*\033[0m') + ret[ast:]
    return ret, chash


def setlength():
    vsize = shutil.get_terminal_size()[1]
    hsize = shutil.get_terminal_size()[0]
    width = hsize - 10
    return int(vsize-8), width


def contpage(verbose, selected, option):
    lpp, width = setlength()
    select = 0
    pagenum = 0
    start = 0
    end = lpp if len(option) > lpp else len(option)
    check = [idx for idx, _ in enumerate(option) if _.count('*')]
    while(1):
        lpp, width = setlength()
        hr()
        print('\033[2K\033[92mSELECTED:', selected, end='\033[0m ')
        print('| \033[91m[VERBOSE]\033[0m') if verbose else print()
        hr()
        for idx, line in enumerate(option[start:end]):
            print('\033[2K\033[0m', end='')
            print('> ', end='') if start+idx == select else print('  ', end='')
            line = line if len(line) < width else f'{line[:int(width)]} ...'
            orig = line
            line, chash = decorate(line)
            if chash in selected:
                print(f'\033[2m{orig}\033[0m')
            else:
                print(line)
            #print(line, end='\033[0m\n')
        if len(option) < lpp:
            for i in range(lpp-len(option)):
                print('\033[2K')

        hr()
        print(f'| \033[93m[hj]:[\u2190\u2193]', end='')
        print(f',q:QUIT,v:VERBOSE,s/Enter:SELECT\033[0m')
        hr()
        if len(selected) == 2:
            break
        ret = wait_key()
        while(1):
            if ret in ['j', 'k', 'v', 'q', 's', '\n']:
                break
            else:
                ret = wait_key()

        if ret == 'j':
            if select < len(option) - 1:
                select += 1
            k = 0
            while(option[select].count('*') == 0):
                select += 1
                k += 1
            if select >= end and end < len(option):
                end += 1 + k
                start += 1 + k
        elif ret == 'k':
            if select > 0:
                select -= 1
            k = 0
            while(option[select].count('*') == 0):
                select -= 1
                k += 1
            if select < start:
                end -= (1 + k)
                start -= (1 + k)
        elif ret == 'q':
            sys.exit(0)
        elif ret == 'v':
            verbose = False if verbose else True
        elif ret in ['\n', 's']:
            if len(selected) == 2:
                break
            else:
                _, chash = decorate(option[select])
                if chash not in selected:
                    selected.append(chash)
                else:
                    selected.pop()
        print(f'\033[{lpp+8}A')
    return verbose


def gfcheck():
    lsgit = sp.getoutput('ls .git').split('\n')
    if len(lsgit) == 1:
        issues.warning('No log found!')
        sys.exit(0)


def logviewer(verbose, head):
    gfcheck()
    logcmd2 = "git log --graph --all --pretty=format:'(%cr) [%h] <%an> %s' --abbrev-commit --date=relative --decorate=full "
    options = sp.getoutput(logcmd2).split('\n')
    if len(options) < 2:
        issues.warning('No log to compare!')
        sys.exit(0)
    if isExist(f'git status --short'):
        options = ['* HEAD'] + options

    while(1):
        vsize = shutil.get_terminal_size()[1]
        hsize = shutil.get_terminal_size()[0]
        selected = []
        if head:
            selected += ['HEAD']
        with CursorOff():
            verbose = contpage(verbose, selected, options)

        ret_diffhash = execdiff(verbose, selected)

        if head:
            break
        else:
            if confirm('\nDo you want to exit diff hash tool?'):
                sys.exit(0)
            else:
                for i in range(vsize):
                    print(f'\033[2K', end='')

    return ret_diffhash


def page(verbose, selected, pages):
    select = 0
    pagenum = 0
    while(1):
        lpp, width = setlength()
        hr()
        pagelen = len(pages[pagenum])
        print('\033[2K\033[92mSELECTED:', selected, end='\033[0m ')
        print('| \033[91m[VERBOSE]\033[0m') if verbose else print()
        hr()
        for idx, opt in enumerate(pages[pagenum]):
            if len(opt) > width:
                opt = opt[:width-5] + '...'
            line, chash = decorate(opt)
            print('\033[2K', end='')
            print('>', end=' ') if idx == select else print(' ', end=' ')
            if chash in selected:
                print(f'\033[2m{opt}\033[0m')
            else:
                print(line)
        for i in range(lpp-pagelen):
            print('\033[2K')
        hr()
        print(f'[{pagenum+1}/{len(pages)}]', end=' ')
        print(f'| \033[93m[hjkl]:[\u2190\u2193\u2191\u2192]', end='')
        print(f',q:QUIT,v:VERBOSE,s/Enter:SELECT\033[0m')
        hr()
        if len(selected) != 2:
            ret = wait_key()
            while(1):
                if ret in ['j', 'k', 'h', 'l', 'q', 'v', 's', '\n']:
                    break
                else:
                    ret = wait_key()

        if ret == 'j':
            if select < pagelen - 1:
                select += 1
            elif pagenum < len(pages) - 1:
                pagenum += 1
                select = 0
        elif ret == 'k':
            if select > 0:
                select -= 1
            elif pagenum > 0:
                pagenum -= 1
                select = lpp - 1
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
        elif ret in ['\n', 's']:
            if len(selected) == 2:
                break
            else:
                chash = ch_gen(pages[pagenum][select])
                if chash not in selected:
                    selected.append(chash)
                else:
                    selected.pop()

        print(f'\033[{lpp+6}A', end='')
    return verbose


def book(verbose, selected, options):
    lpp, width = setlength()
    pages = []
    if len(options) > lpp:
        for i in range(0, len(options), lpp):
            pages.append(options[i:i+lpp])
    else:
        pages = [options]
    return page(verbose, selected, pages)


def execdiff(verbose, selected):
    ret_diffhash = ''
    if 'HEAD' in selected:
        ret_diffhash = selected[0] if selected[0] != 'HEAD' else selected[1]
        issues.execute([f'git diff --stat {ret_diffhash}'])
        if verbose:
            issues.execute(
                [f'git diff --ignore-blank-lines -U1 {ret_diffhash}'])
    else:
        issues.execute([f'git diff --stat {selected[0]}..{selected[1]}'])
        if verbose:
            issues.execute(
                [f'git diff --ignore-blank-lines -U1 {selected[0]}..{selected[1]}'])
    return ret_diffhash


def diffhash(verbose, head, author):
    gfcheck()
    ret_diffhash = ''
    if author:
        ret_author = prompt("Name specific author", _type=str)
    while(1):
        vsize = shutil.get_terminal_size()[1]
        hsize = shutil.get_terminal_size()[0]
        options = []
        if isExist(f'git status --short') or head:
            options += ['HEAD']

        threshold = 100
        randstr = ''.join(
            [random.choice(string.ascii_letters + string.digits) for i in range(8)])
        fstring = randstr.join(['(%ad)', '[%h]', '<%an>', '%s'])
        dateset = 'local' if hsize > threshold else 'relative'
        options += sp.getoutput(
            f'git log --date={dateset} --pretty=format:"{fstring}"').split('\n')
        if len(options) < 2:
            issues.warning('No log to compare!')
            sys.exit(0)
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

        ret_diffhash = execdiff(verbose, selected)
        if head:
            break
        else:
            if confirm('\nDo you want to exit diff hash tool?'):
                sys.exit(0)
            else:
                for i in range(vsize):
                    print(f'\033[2K\033[1A', end='')

    return ret_diffhash
