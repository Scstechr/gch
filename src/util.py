import cursor
import termios
import shutil
import sys
from . import issues
from contextlib import suppress

class CursorOff(object):
    def __enter__(self):
        cursor.hide()
#        vsize = shutil.get_terminal_size()[1]
#        print(f'\33[{vsize};0f', end='')
#        for i in range(vsize+1):
#            print(f'\033[1F\033[2K', end ='')
         
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
    if not result:
        raise KeyboardInterrupt

    return result
