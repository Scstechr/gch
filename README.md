# Git Commit Handler
A tool to handle git related commands

- Executes `git` related commands as such:
	- `git init`, `git commit`, `git diff`, `git add`, `git push`
- Document available: :us: [English](doc/gch_doc_en.md) / :jp: [Japanese](doc/gch_doc_jp.md)
	- :warning: It has not been updated for long time. Make an issue if any problem occurs.
- Blog Post (Japanese): [Qiita](https://qiita.com/Scstechr/items/53e3e326c4caa6dc2307) / [Qrunch](https://scstechr.qrunch.io/entries/Jmdclx72XYk2F5Pa)

## Requirements
Please install all the packages listed in `requirements.txt`.

```bash
$ git clone https://github.com/Scstechr/gch ~/.gch
$ cd ~/.gch
$ pip install -r requirements.txt
```
Also, be sure to have `Python 3.6.x` executable in any way.

## Recommendation
It is recommended to use `alias` in order to execute `gch` from anywhere.  
Add these lines in `.bash_profile`/`.bashrc`

```bash:.bash_profile
export PATH="${HOME}/.gch:$PATH"
alias gch='gch.py'
```

or

```bash:add
echo 'PATH="${HOME}/.gch:$PATH"' >> ~/.bashrc
echo 'alias gch="gch.py"' >> ~/.bash_profile
```

 and `source` it afterwards.

## How to Use

### Show help

```bash
$ gch --help
Usage: gch.py [OPTIONS]

Options:
  -c, --commit         Commit
  -p, --push           Push.
  -i, --init           Run initializer                       >Default:False
  -v, --verbose        Verbose option.                       >Default:False
  -l, --log            Git log with option.                  >Default:False
  -r, --remote TEXT    Choose which remote repo.to push.     >Default:origin
  -g, --gitpath PATH   Path of dir that contains `.git`.
                       >Default:/Users/moinaga/.gch
  -f, --filepath TEXT  Path/Regex of staging file/dir.       >Default:.
  -b, --branch TEXT    Commiting branch.                     >Default:master
  -s, --save           Save settings                         >Default:False
  -d, --diff           Open diff tool                        >Default:False
  -u, --update         Update gch                            >Default:False
  --reset              Reset all changes since last commit.  >Default:None
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




