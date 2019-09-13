import sys
import urllib.request as req
import urllib.error as err
from . import issues

VERSION = '1.35'
DATE = "2019-09-13 15:48:27 UTC"
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
        latest = text.split('tag_name')[1].split(',')[
            0].replace('":"v', '')[:-1]
        if VERSION != latest:
            return 0, latest
        else:
            return 1

    except (err.HTTPError, err.URLError):
        return 2


def ShowVersion(i, latest=''):
    if i == 0:
        msg = f"[UPDATE] Update to v.{latest} found!\n"
        msg += "   \u2937 `brew upgrade gch` for updating `gch`."
        issues.ok(msg)
    elif i == 1:
        msg = f"[UPDATE] `gch` is up-to-date\n"
        issues.ok(msg)
    elif i == 2:
        msg = f"[UPDATE] No internet connection"
        issues.warning(msg)
    else:
        msg = f"Undefined flag for ShowVersion()"
        issues.warning(msg)
