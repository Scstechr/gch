from ..issues import warning, execute
from ..qs import getAnswer, isExist, confirm, prompt
from ..diff import diffhash
from .commit import Commit
from ..colors import R, G, Y, B, P, C, GR, BL, TH, IT, M

def Reset(patch):
    warning('Options with `--hard` must be done with caution')
    opt = []
    opt.append(
        '{IT}git commit --amend{M}          > Change message of last commit')
    opt.append(
        '{IT}git reset --soft HEAD^{M}      > Undo last commit (soft)')
    opt.append(
        '{IT}git reset {R}--hard{M}{IT} HEAD^{M}      > Undo last commit')
    opt.append(
        '{IT}git reset {R}--hard{M}{IT} HEAD{M}       > Undo changes from last commit')
    opt.append(
        '{IT}git reset {R}--hard{M}{IT} <hash>{M}     > Undo changes from past commit')
    opt.append(
        '{IT}git reset {R}--hard{M}{IT} ORIG_HEAD{M}  > Undo most recent reset')
    ans = getAnswer(opt)
    if ans == 1:
        execute(['git commit --amend'])
    elif ans == 2:
        execute(['git reset --soft HEAD^'])
    elif ans == 3:
        execute(['git reset --hard HEAD^'])
    elif ans == 4:
        execute(['git reset --hard HEAD'])
    elif ans == 5:
        warning('Select hash from diff tool...')
        flag = False
        if confirm('Do you want to name specific author?'):
            flag = True
        dhash = diffhash(verbose=True, head=True, author=flag)
        while(1):
            if confirm("Is this the correct hash you want to go back?"):
                break
            dhash = diff.diffhash(verbose=True, head=True, author=flag)
        if confirm(f"Go back (reset) to {dhash}?"):
            if not isExist(f'git status --short'):
                execute([f'git reset --hard {dhash}'])
            else:
                print(f'\nTheres some changes not commited..')
                execute([f'git diff --stat'])
                qs = [f'Commit changes before reset']
                qs.append(f'Stash changes before reset')
                qs.append(f'Force Checkout before reset')
                ans = getAnswer(qs)
                if ans == 1:
                    execute([f'git add .', f'git diff --stat'])
                    Commit(patch)
                    execute([f'git reset --hard {dhash}'])
                elif ans == 2:
                    execute(
                        [f'git stash', f'git reset --hard {dhash}'])
                else:
                    execute([f'git reset --hard {dhash}'])
    elif ans == 5:
        execute([f'git reset --hard ORIG_HEAD'])

