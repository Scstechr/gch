# !/usr/bin/env python
'''
==================
Git Commit Handler
==================
'''

from src import issues
from src.proc import proc
from src.parse import Parser
MODE = 0


issues.version(3)


def main():
    d = Parser(MODE)
    proc(d)


if __name__ == "__main__":
    # main()
    try:
        main()
    except (IOError, EOFError, KeyboardInterrupt):
        issues.abort()
