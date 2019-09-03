# GCH: Git Commit Handler
[![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)][license]

[license]: https://github.com/Scstechr/gch/blob/master/LICENSE

A tool to handle git related commands such as: `git init`, `git commit`, `git diff`, `git add`, `git push`

## Overview
This tool makes it easier to execute certain `git` commands from terminal. Also, this `gch` aims for beginners of `git` by showing actual commands executed in specific color.

- Documents available in: :us: [English](doc/gch_doc_en.md) / :jp: [Japanese](doc/gch_doc_jp.md)
- Blog Post (Japanese): [Qiita](https://qiita.com/Scstechr/items/53e3e326c4caa6dc2307) / [Qrunch](https://scstechr.qrunch.io/entries/Jmdclx72XYk2F5Pa)

## Install

```bash
$ brew tap scstechr/gch
$ brew install gch
```
### Update

```bash
$ brew update; brew upgrade gch
```
## How to Use

### Show help

```bash
$ gch --help
gch v1.29 (compiled: 2019-09-03 13:37:12 UTC)
Usage: gch [OPTION]

Options:
  -i, --init        | Run initializer
  -v, --verbose     | Verbose option.
  -l, --log         | Git log with option.
  -r, --remote      | Choose which remote repo.to push.
  -g, --gitpath     | Path of dir that contains `.git`.
  -f, --filepath    | Path/Regex of staging file/dir.
  -b, --branch      | Commiting branch.
  -c, --commit      | Commit
  -p, --push        | Push.
  -s, --save        | Save settings
  -d, --diff        | Open diff tool
  --checkout        | Handling checkouts
  --reset           | Reset all changes since last commit.
  --pull            | Fetch + Merge from origin:master.
  --ls              | List up tracking files/directories
  --version         | Check version of gch
  -h, --help        | Show this message and exit.
```
### Simple command

```bash
$ gch -c
```

or equivalently,

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

### Developer's Note

- First developed under name of `comm.py` in [this commit](https://github.com/Scstechr/usefultools/commit/a24a413469f3a85c7325b09281fada7e3f031aa7#diff-e39ecf62d7a2fafe884171d619b2030c) ([view history](https://github.com/Scstechr/usefultools/commits/b66ba9beaf659d786e4897c3624e9e9b2facff43/comm.py)).
- Then, it changed its name to `gch.py` in [this commit](https://github.com/Scstechr/usefultools/commit/b66ba9beaf659d786e4897c3624e9e9b2facff43#diff-e39ecf62d7a2fafe884171d619b2030c).

- The [original version of gch](https://github.com/Scstechr/usefultools/blob/master/gch.py) (and its [history](https://github.com/Scstechr/usefultools/commits/master/gch.py)) was a part of [usefultools](https://github.com/Scstechr/usefultools).


