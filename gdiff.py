#!/usr/bin/env python
'''
==================
Git Diff Tool
==================
'''

from src import issues
from src.arg import Help
from src.version import Version
from src.parse import Parser
from src.diff import diffhash, logviewer
MODE = 1


issues.version(3)


def main():
    d = Parser(MODE)

    verbose = d['verbose']
    head = d['head']
    author = d['author']
    version = d['version']

    if d['help']:
        Help(MODE)
    elif d['log']:
        logviewer(verbose, head)
    elif version:
        Version('GDIFF - Git DIFF viewer')
    else:
        diffhash(verbose, head, author)


if __name__ == '__main__':
    try:
        main()
    except (IOError, EOFError, KeyboardInterrupt):
        issues.abort()
