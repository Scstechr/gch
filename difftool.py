#!/usr/bin/env python
'''
==================
Git Diff Tool
==================
'''

import click

from src.diff import diffhash, logviewer

@click.command()
@click.option('-v', '--verbose', is_flag='False', help='detailed diff')
@click.option('-h', '--head', is_flag='False', help='include head')
@click.option('-a', '--author', is_flag='False', help='name specific author')
@click.option('-l', '--log', is_flag='False', help='user log ver. instead')
def main(verbose, head, author, log):
    if log:
        logviewer(verbose, head)

    else:
        diffhash(verbose, head, author)

if __name__ == '__main__':
    main()
