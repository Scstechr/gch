import subprocess as sp
from ..issues import warning, execute, abort, ok
from ..util import CursorOff, wait_key, B
from ..qs import getAnswer, prompt, isExist, confirm
from .checkout import Checkout
from ..colors import R, G, Y, B, P, C, GR, BL, TH, IT, M


def Branch():
    if isExist('git branch'):
        execute([f'git branch'])
        current_branch, branch_list = getBranch(lst=True)
        with CursorOff():
            options = ['(c) checkout']
            options.append('(r) rename')
            options.append('(n) new branch')
            options.append('(d) delete')
            print(f"\n{BL}Options:{M}\n {' '.join(options)} (e) exit")
            answer = wait_key()
            while 1:
                if answer in ['c', 'r', 'n', 'd', 'e']:
                    break
                answer = wait_key()
        if answer == 'c':
            ok('Checking out branch!')
            checkoutBranch()
        elif answer == 'r':
            ok('Renaming current branch!')
            renameBranch()
        elif answer == 'n':
            ok('Making new branch!')
            newBranch(branch_list)
        elif answer == 'd':
            deleteBranch()
    else:
        warning('Branch not found!')
        branch = 'master'
    branch = getBranch()
    ok(f'Branch set to {B(branch)}')
    return branch


def checkoutBranch():
    current_branch, branch_list = getBranch(lst=True)
    branch_list.append('Make new branch')
    branch = [b for b in branch_list if b != current_branch]
    if len(branch) == 1:
        if confirm(f"Make new branch?"):
            newBranch(branch_list)
    else:
        print(f'\n{M}{BL}Which branch do you want to checkout?{M}')
        answer = getAnswer(branch)
        if answer == len(branch):
            newBranch(branch_list)
        else:
            Checkout(current_branch, branch[answer-1])

def getBranch(lst=False):
    ''' Returns current branch name w or w/o branch list '''
    output = sp.getoutput('git branch').split('\n')
    current_branch = ''.join(branch[2:]
                             for branch in output if branch[0] == '*')
    branch_list = [branch[2:] for branch in output]
    if lst:
        return current_branch, branch_list
    else:
        return current_branch


def setBranch(branch, filepath):
    current_branch, branch_list = getBranch(lst=True)
    if branch not in branch_list:
        warning(f'Branch {B(branch)} not found.')
        qs = [f'Make new branch {B(branch)}               ']
        qs.append(f'Stay on current branch {B(current_branch)}')
        answer = getAnswer(qs)
        if answer == 1:
            execute([f'git checkout -b {branch}'])
        else:
            print(f'Commiting branch set to {B(current_branch)}')
            branch = current_branch
    else:
        print(
            f'Currently on branch {B(current_branch)} but tried to commit to branch {B(branch)}.')
        qs = [f'Merge branch {B(current_branch)} => branch {B(branch)}']
        qs.append(f'Stay on branch {B(current_branch)}                   ')
        qs.append(f'Checkout to branch {B(branch)}                       ')
        answer = getAnswer(qs)
        if answer == 2:
            print(f'Committing branch is now set to {B(current_branch)}')
            branch = current_branch
        else:
            Checkout(current_branch, branch)
            if answer == 1:
                execute(
                    [f'git format-patch {branch}..{current_branch} --stdout | git apply --check'])
                if isExist('git format-patch {branch}..{current_branch} --stdout | git apply --check'):
                    execute([f'git merge {current_branch}'])
                else:
                    warning(
                        "Aborting Merge because conflict is likely to occur.")
                    abort()

    return branch


def newBranch(branch_list):
    while 1:
        new_branch = prompt(
            '\nEnter new branch name (spaces will be replaced with `-`)').replace(' ', '-')
        if new_branch in branch_list:
            warning(f'Branch `{new_branch}` already exists!')
        else:
            ok(f'\bBranch `{new_branch}` successfully created!')
            if confirm(f'Checkout to `{new_branch}`'):
                execute([f'git checkout -b {new_branch}'])
            else:
                execute([f'git branch {new_branch}'])
            break


def renameBranch():
    current_branch, branch_list = getBranch(lst=True)
    while 1:
        new_branch = prompt(
            '\n\033[2KEnter new branch name (spaces will be replaced with `-`)').replace(' ', '-')

        if new_branch in branch_list:
            warning(f'Branch `{new_branch}` already exists!')
        else:
            execute([f'git branch -m {new_branch}'])
            ok(f'Branch `{current_branch}` is now `{new_branch}`')
            break


def deleteBranch():
    current_branch, branch_list = getBranch(lst=True)
    print(f'\nCurrently on branch: {B(current_branch)}...\n')

    branch_list = [branch for branch in branch_list]
    print(f"Which branch do you want to delete?:\n")
    answer = getAnswer(branch_list, exit=False) - 1
    branch = branch_list[answer]
    if branch == 'master':
        warning('You cannot delete master branch via gch.')
    else:
        if branch == current_branch:
            msg = f"You tried to delete branch you are currently on!"
            warning(msg)
            next_list = [b for b in branch_list if b != current_branch]
            print(
                f"Please choose the branch to checkout before deleting {B(branch)}:\n")
            answer = getAnswer(next_list, exit=False) - 1
            Checkout(current_branch, next_list[answer])
        if confirm(f"Delete branch {B(branch)}?"):
            out = sp.getoutput([f'git branch --delete {branch}'])
            if out.count('error'):
                warning('Could not delete branch since its not fully merged.')
                if confirm(f"Delete branch {B(branch)} anyway?"):
                    execute([f'git branch -D {branch}'])
                    ok('You deleted branch!')
                else:
                    ok('Branch not deleted.')
            else:
                execute([f'git branch --delete {branch}'], run=False)
                ok('You deleted branch!')

