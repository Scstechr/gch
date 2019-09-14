from ..issues import execute


def Ls():
    execute([f'git ls-files'])