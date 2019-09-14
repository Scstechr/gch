import subprocess as sp
from ..issues import warning, execute, abort
from ..qs import getAnswer

def B(string):
    ''' String Format for Branch Name '''
    return f'`\033[3m{string}\033[m`'



def getCurrentBranch(lst=False):
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
    current_branch, branch_list = getCurrentBranch(lst=True)
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
            checkoutBranch(branch)
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
