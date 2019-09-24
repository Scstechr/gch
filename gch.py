# !/usr/bin/env python
'''
==================
Git Commit Handler
==================
'''

from concurrent.futures import ThreadPoolExecutor as Executor
from contextlib import suppress
from src import issues
from src.proc import proc
from src.parse import Parser
from src.version import CheckVersion, ShowVersion
DEBUG = True


issues.version(3)


def main():
    d = Parser()
    # proc(d)
    result = None
    with suppress(IOError, EOFError, KeyboardInterrupt):
        with Executor() as executor:
            if d['check']:
                result = executor.submit(CheckVersion)
            executor.submit(proc, d)

    if d['check'] and result:
        ShowVersion(result.result())


if __name__ == "__main__":
    try:
        main()
    except (IOError, EOFError, KeyboardInterrupt):
        issues.abort()
