from ..issues import warning, execute, abort
from ..qs import prompt, confirm
from ..colors import R, G, Y, B, P, C, GR, BL, TH, IT, M

def Commit():
    ''' Commit '''
    commit_message = prompt("Commit Message [v:vim mode]")
    if commit_message.count('`'):
        warning(
            f'{M}{BL}`{M}{R} is not acceptable in this mode.')
        if confirm(f'Replace {M}{BL}`{M}{C} with {M}{BL}\'{M}{C}'):
            commit_message = commit_message.replace('`', "'")
            warning(
                f'{M}{BL}`{M}{R} is now replaced with {M}{BL}\'{R}...')
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

