#!/usr/bin/env python
'''
==================
Git Diff Tool
==================
'''

VERSION = 1.6
import click

import sys
from src.diff import diffhash, logviewer

@click.command()
@click.option('-v', '--verbose', is_flag='False', help='Detailed diff.')
@click.option('-h', '--head', is_flag='False', help='Include HEAD^ from the beginning.')
@click.option('-a', '--author', is_flag='False', help='Name specific author.')
@click.option('-l', '--log', is_flag='False', help='User log ver. instead.')
@click.option('--version', is_flag='False', help='Check version of gdiff.')
def main(verbose, head, author, log, version):
    if version:
        print(" gdiff version :", VERSION)
        sys.exit(0)
    if log:
        logviewer(verbose, head)

    else:
        diffhash(verbose, head, author)

if __name__ == '__main__':
    main()
