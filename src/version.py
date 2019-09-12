import subprocess as sp
import sys
import urllib.request as req
import urllib.error as err
from . import issues

VERSION = '1.33'
DATE = "2019-09-10 15:57:09 UTC"
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

def CheckVersion():
    url = "https://api.github.com/repos/Scstechr/gch/releases/latest"
    try:
        text = req.urlopen(url).read().decode('utf-8')
        latest = text.split('tag_name')[1].split(',')[0].replace('":"v','')[:-1]
        if VERSION != latest:
            msg = f"Update to v.{latest} found!\n"
            msg += "   \u2937 `brew upgrade gch` for updating `gch`."
            issues.ok(msg)

    except (err.HTTPError, err.URLError):
        pass

