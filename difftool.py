#!/usr/bin/env python
'''
==================
Git Diff Tool
==================
'''

import click

from src.diff import diffhash

@click.command()
@click.option('-v', '--verbose', is_flag='False', help='detailed diff')
@click.option('-h', '--head', is_flag='False', help='include head')
@click.option('-a', '--author', is_flag='False', help='name specific author')
def main(verbose, head, author):
    diffhash(verbose, head, author)

if __name__ == '__main__':
    main()
