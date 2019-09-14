from ..issues import warning, execute, abort
from ..qs import prompt, confirm

def Commit():
    ''' Commit '''
    commit_message = prompt("Commit Message [v:vim mode]")
    if commit_message.count('`'):
        warning(
            '\033[m\033[1m`\033[m\033[91m is not acceptable in this mode.')
        if confirm('Replace \033[m\033[1m`\033[m\033[96m with \033[m\033[1m\'\033[m\033[96m'):
            commit_message = commit_message.replace('`', "'")
            warning(
                '\033[m\033[1m`\033[m\033[91m is now replaced with \033[m\033[1m\'\033[91m...')
        else:
            warning('Now entering vim mode...')
            commit_message = 'v'
    if commit_message in ['v', 'vi', 'vim']:
        execute([f'git commit'])
    else:
        if len(commit_message):
            execute([f'git commit -m "{commit_message}"'])
        else:
            abort()

