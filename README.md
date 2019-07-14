# Git Commit Handler
A tool to handle git related commands

- Execute `git` related commands such as:
	- `git init`, `git commit`, `git diff`, `git add`, `git push`
- Documents available in: :us: [English](doc/gch_doc_en.md) / :jp: [Japanese](doc/gch_doc_jp.md)
	- :warning: Note that English version has not been updated for a long time.
- Blog Post (Japanese): [Qiita](https://qiita.com/Scstechr/items/53e3e326c4caa6dc2307) / [Qrunch](https://scstechr.qrunch.io/entries/Jmdclx72XYk2F5Pa)

## Install

```bash
$ brew tap scstechr/gch
$ brew install gch
```

## How to Use

### Show help

```bash
$ gch --help
Usage: gch.py [OPTIONS]

Options:
  -i, --init           Run initializer                       >Default:False
  -v, --verbose        Verbose option.                       >Default:False
  -l, --log            Git log with option.                  >Default:False
  -r, --remote TEXT    Choose which remote repo.to push.     >Default:origin
  -g, --gitpath PATH   Path of dir that contains `.git`.     >Default:.
  -f, --filepath TEXT  Path/Regex of staging file/dir.       >Default:.
  -b, --branch TEXT    Commiting branch.                     >Default:master
  -c, --commit         Commit
  -p, --push           Push.
  -s, --save           Save settings                         >Default:False
  -d, --diff           Open diff tool                        >Default:False
  -u, --update         Update gch                            >Default:False
  --reset              Reset all changes since last commit.  >Default:False
  --pull               Pull from <origin> <master>.          >Default:False
  --help               Show this message and exit.
```
### Simple command

```bash
$ gch -c
```

or 

```bash
$ gch --commit
```

This command executes `git status --short`, `git diff --stat`, `git add .` etc.  
(shown as a blue line while executed)  
Also, adds everything except configured in `.gitignore` or `gch -f` command.  

### Linked commands

Commands can be executed together in the manner below:

```bash
$ gch -cp
```

This executes `git commit` and `git push`.

#### Further example

##### `gch -cp -r localhost`
`commit`, then `push` to the remote called `localhost`.
##### `gch -cp -b test -d`
Shows `diff` first, then `commit` and `push`.




