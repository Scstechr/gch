# !/usr/bin/env python
'''
==================
Git Commit Handler
==================
'''

from concurrent.futures import ThreadPoolExecutor as Executor
from src import issues
from src.proc import proc
from src.parse import Parser
from src.version import CheckVersion, ShowVersion
MODE = 0


issues.version(3)


def main():
    d = Parser(MODE)

    result = None
    with Executor() as executor:
        if d['check']:
            result = executor.submit(CheckVersion)
        executor.submit(proc, d)

    if d['check'] and result:
        ShowVersion(result.result())


if __name__ == "__main__":
    # main()
    try:
        main()
    except (IOError, EOFError, KeyboardInterrupt):
        issues.abort()
