import sys
import urllib.request as req
import urllib.error as err
from . import issues
from .colors import BL, M

VERSION = '1.42'
DATE = "2019-09-24 11:24:47 UTC"
PYTHON_VERSION = '3.7.3'
PLATFM_VERSION = 'Darwin-18.0.0-x86_64-i386-64bit'
PYINST_VERSION = '3.5'


def ShortVersion(string):
    print(f"{BL}{string} v{VERSION} (compiled: {DATE}){M}")


def Version(string):
    print(f"{BL}{string} v{VERSION} (compiled: {DATE}){M}")
    print(f"{M}BUILD INFO: {M}")
    # Python version
    version = PYTHON_VERSION
    print(f"{M} Python      :{M}", version)

    # PyInstaller version
    version = PYINST_VERSION
    print(f"{M} PyInstaller :{M}", version)

    # Platform version (Kernel)
    version = PLATFM_VERSION
    print(f"{M} Platform    :{M}", version)

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
