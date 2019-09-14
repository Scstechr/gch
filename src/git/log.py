from ..issues import execute

logcmd = 'git log --stat --oneline --graph --decorate'

def Log():
    execute([logcmd])

