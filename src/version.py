import sys

VERSION = '1.29'
DATE = "2019-09-03 11:02:30 UTC"
PYTHON_VERSION = '3.7.3'
PLATFM_VERSION = 'Darwin-18.0.0-x86_64-i386-64bit'
PYINST_VERSION = '3.5'

def ShortVersion(string):
    print(f"\033[1m{string} v{VERSION} (compiled: {DATE})\033[0m")

def Version(string):
    print(f"\033[1m{string} v{VERSION} (compiled: {DATE})\033[0m")
    print(f"\033[0mBUILD INFO: \033[0m")
    # Python version
    version = PYTHON_VERSION
    print(f"\033[0m Python      :\033[0m", version)

    # PyInstaller version
    version = PYINST_VERSION
    print(f"\033[0m PyInstaller :\033[0m", version)

    # Platform version (Kernel)
    version = PLATFM_VERSION
    print(f"\033[0m Platform    :\033[0m", version)

    sys.exit(0)
