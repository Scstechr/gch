#!/usr/bin/env python
'''
==================
Git Diff Tool
==================
'''

MODE = 1

from src.diff import diffhash, logviewer
from src.parse import Parser
from src.version import *
from src.arg import Help
from src import issues

issues.version(3)

def main():
    d = Parser(MODE)

    verbose = d['verbose']
    head    = d['head']
    author  = d['author']
    version = d['version']

    if d['help']:
        Help(MODE)
    if d['version']:
        Version('GDIFF - Git DIFF viewer')
    if d['log']:
        logviewer(verbose, head)

    else:
        diffhash(verbose, head, author)

if __name__ == '__main__':
    try:
        main()
    except (IOError, EOFError, KeyboardInterrupt):
        issues.abort()
