import cursor
import termios
import sys
from contextlib import suppress
from urllib.parse import urlparse
from .issues import warning, execute, abort, ok
from .colors import M, GB


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


def validateRefPrint(string, lst):
    warning(f'{string} must not be included!')
    blank = ''.join([' ' for _ in range(len(string)+5)])
    _list = []
    for idx, item in enumerate(lst):
        if idx%9 == 0:
            _list.append('')
            _list[-1] += ',' + f'{GB}{item}{M}'
        else:
            _list[-1] += ',' + f'{GB}{item}{M}'
    for idx, col in enumerate(_list):
        if not idx:
            print('>>', string, ':', col[1:])
        else:
            print(blank, col[1:])


def validateRef(x):
    a = []
    control = ['\x00', '\x01', '\x02', '\x03', '\x04', '\x05', '\x06']
    control += ['\x07', '\x08', '\x09', '\x0a', '\x0b', '\x0c', '\x0d']
    control += ['\x0e', '\x0f', '\x10', '\x11', '\x12', '\x13', '\x14']
    control += ['\x15', '\x16', '\x17', '\x18', '\x19', '\x1a', '\x1b']
    control += ['\x1c', '\x1d', '\x1e', '\x1f', '\x7f']
    _control = ['\\x00', '\\x01', '\\x02', '\\x03', '\\x04', '\\x05', '\\x06']
    _control += ['\\x07', '\\t  ', '\\n  ', '\\x0a', '\\x0b', '\\x0c', '\\r  ']
    _control += ['\\x0e', '\\x0f', '\\x10', '\\x11', '\\x12', '\\x13', '\\x14']
    _control += ['\\x15', '\\x16', '\\x17', '\\x18', '\\x19', '\\x1a', '\\x1b']
    _control += ['\\x1c', '\\x1d', '\\x1e', '\\x1f', '\\x7f']
    a.append(sum([1 if x.count(r) else 0 for r in control]))
    if a[-1]:
        validateRefPrint('Control codes', _control)

    # na = not allowed
    na_char = [' ', '~', '^', ':', '?', '*', '[', '\\']
    a.append(sum([1 if x.count(r) else 0 for r in na_char]))
    if a[-1]:
        validateRefPrint('Special characters', na_char)
    na_str = ['..', '@{', '//']
    a.append(sum([1 if x.count(r) else 0 for r in na_str]))
    if a[-1]:
        validateRefPrint('Special strings', na_str)

    a.append(sum([1 if x[0] == r else 0 for r in ['.','/']]))
    if a[-1]:
        warning('')
        print(f'>> Must not start with: {M}{GB}.{M},{GB}/{M}')
    a.append(sum([1 if x[-1] == r else 0 for r in ['.','/']]))
    if a[-1]:
        warning('')
        print(f'>> Must not end with: {M}{GB}.{M},{GB}/{M},{GB}.lock{M}')

    if len(x) > 4 and x[-5:] == '.lock':
        a.append(1)
        warning('')
        print(f'>> Must not end with: {M}{GB}.{M},{GB}/{M},{GB}.lock{M}')

    if x == '@':
        a.append(1)
        warning(f'Must not be: {M}{GB}@{M}')

    if sum(a):
        print("   \u2937 `man git-check-ref-format` for more information.")
        return False
    else:
        return True

def br(string):
    ''' String Format for Branch Name '''
    return f'`{string}`'
