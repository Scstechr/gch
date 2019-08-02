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

### Update

```bash
$ brew upgrade gch
```
## How to Use

### Show help

```bash
$ gch --help
Usage: gch [OPTION]

Options
  -i, --init        Run initializer
  -v, --verbose     Verbose option.
  -l, --log         Git log with option.
  -r, --remote      Choose which remote repo.to push.
  -g, --gitpath     Path of dir that contains `.git`.
  -f, --filepath    Path/Regex of staging file/dir.
  -b, --branch      Commiting branch.
  -c, --commit      Commit
  -p, --push        Push.
  -s, --save        Save settings
  -d, --diff        Open diff tool
  --version         Check version of gch
  --reset           Reset all changes since last commit.
  --pull            Fetch + Merge from origin:master.
  --help            Show this message and exit.
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

### Other
The [original version of gch](https://github.com/Scstechr/usefultools/blob/master/gch.py) (and its [history](https://github.com/Scstechr/usefultools/commits/master/gch.py)) as a part of [usefultools](https://github.com/Scstechr/usefultools)


