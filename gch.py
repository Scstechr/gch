# !/usr/bin/env python
'''
==================
Git Commit Handler
==================
'''

from contextlib import suppress
from src import issues
from src.proc import proc
from src.parse import Parser
from src.version import CheckVersion, ShowVersion


issues.version(3)


def main():
    d = Parser()
    with suppress(IOError, EOFError, KeyboardInterrupt):
        proc(d)

    if d['check']:
        result = CheckVersion()
        ShowVersion(result.result())


if __name__ == "__main__":
    try:
        main()
    except (IOError, EOFError, KeyboardInterrupt):
        issues.abort()
