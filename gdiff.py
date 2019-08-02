#!/usr/bin/env python
'''
==================
Git Diff Tool
==================
'''

from src.diff import diffhash, logviewer
from src.parse import Parser, Version
from src.arg import Help
from src import issues

MODE = 1

issues.version(3)

def main():
    d = Parser(MODE)
    verbose = d['verbose']
    head    = d['head']
    author  = d['author']
    if d['help']:
        Help(MODE)
    if d['version']:
        Version('GDIFF - Git DIFF viewer')
    if d['log']:
        logviewer(verbose, head)

    else:
        diffhash(verbose, head, author)

if __name__ == '__main__':
    main()
