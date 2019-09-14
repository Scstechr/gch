import cursor
import termios
import sys
from contextlib import suppress
from urllib.parse import urlparse


class CursorOff(object):
    def __enter__(self):
        cursor.hide()

    def __exit__(self, *args):
        cursor.show()


def wait_key():
    ''' Wait for a key press on the console and return it. '''
    with suppress(KeyboardInterrupt):
        result = None
        fd = sys.stdin.fileno()

        oldterm = termios.tcgetattr(fd)
        newattr = termios.tcgetattr(fd)
        newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
        termios.tcsetattr(fd, termios.TCSANOW, newattr)

        result = sys.stdin.read(1)
        termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)

    return result


def validateURL(x):
    try:
        result = urlparse(x)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


