from ..issues import execute
from .status import Status

def Pull(remote, branch):
    if not Status():
        execute([f'git pull {remote} {branch}'])
    else:
        execute([f'git diff --stat'])
        print(
            f'\nTheres some changes in branch {br(current_branch)}.')
        qs = [f'Commit changes of branch {br(current_branch)}']
        qs.append(f'Stash changes of branch {br(current_branch)} ')
        answer = getAnswer(qs)
        if answer == 1:
            execute([f'git add .', f'git diff --stat'])
            Commit()
        elif answer == 2:
            execute([f'git stash'])
        execute([f'git pull {remote} {branch}'])
