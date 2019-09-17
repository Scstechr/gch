from ..qs import confirm, getAnswer
from ..issues import execute
from ..util import br
from .commit import Commit
from .status import Status

def Checkout(current_branch, branch):
    if not Status():
        execute([f'git checkout {branch}'])
    else:
        execute([f'git diff --stat'])
        print(
            f'\nTheres some changes in branch {br(current_branch)}.')
        qs = [f'Commit changes of branch {br(current_branch)}']
        qs.append(f'Stash changes of branch {br(current_branch)} ')
        qs.append(f'Force Checkout to branch {br(branch)}        ')
        answer = getAnswer(qs)
        if answer == 1:
            execute([f'git add .', f'git diff --stat'])
            Commit()
            execute([f'git checkout {branch}'])
        elif answer == 2:
            execute([f'git stash', f'git checkout {branch}'])
        else:
            execute([f'git checkout -f {branch}'])
