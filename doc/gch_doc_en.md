# GCH: Git Commit Handler
Official document of __GCH__ (Git Commit Handler).
###### Table of Contents
- [Installation](#installation)
	- [Update](#update)
- [Options](#options)
	- [`-g` or `--gitpath`](#-g-or---gitpath)
	- [`-f` or `--filepath`](#-f-or---filepath)
	- [`-b` or `--branch`](#-b-or---branch)
	- [`-d` or `--detail`](#-d-or---detail)
	- [`-l` or `--log`](#-l-or---log)
	- [`-c` or `--commit`](#-c-or---commit)
	- [`-u` or `--unstage`](#-u-or---unstage)

### Installation
```bash
$ git clone https://github.com/Scstechr/usefultools.git ~/.useful
$ cd ~/.useful
$ pip install -r requirements.txt
```

#### Update
```bash
$ git pull origin master
```


### Options
```bash
$ gch --help
Usage: gch.py [OPTIONS]

Options:
  -g, --gitpath PATH   Path of dir that contains `.git`. > Default: .
  -f, --filepath PATH  Path of staging file/diry.        > Default: .
  -b, --branch TEXT    Commiting branch.                 > Default: master
  -p, --push           Push or not.                      > Default: False
  -d, --detail         Detailed diff.                    > Default: False
  -l, --log            Git log with option.              > Default: False
  -c, --commit         Commit or not.                    > Default: False
  -u, --unstage        Unstage all files.                > Default: False
  --help               Show this message and exit.
```


Recommended to use with `alias`, such as `alias gch='gch.py'`. after exporting PATH of the cloned folder.
Every command used in this script are visible as such:
```bash
>> EXECUTE: git status --short
```

#### `-g` or `--gitpath`

The capability of this tag is that of `git --git-dir=<path>`.
With this tag, user can specify which `.git` folder to use for commit etc.
Default is set to `.`, which will be selected if `-g` was abridged.
##### If selected PATH does not have `.git` folder

```bash
$ gch

>> WARNING!: It seems path:`<PATH>` does not have `.git` folder.
Initialize? [y/N]:
```
If `~/.gitconfig` does exists before the execution of command, the following configuration of `username`, `email`, `editor`, `diff-tool` will start．

```bash
~/.gitconfig file does not exist. => Start Initialization!
username: Scstechr
email: teufelkonig@gmail.com
>> EXECUTE: git config --global user.name "Scstechr"
>> EXECUTE: git config --global user.email teufelkonig@gmail.com
Do you want to use emacs instead of vim as an editor? [y/N]: N
# using vimdiff as a merge tool
>> EXECUTE: git config --global merge.tool vimdiff
>> EXECUTE: cat ~/.gitconfig
[user]
	name = Scstechr
	email = teufelkonig@gmail.com
[merge]
	tool = vimdiff
```
After the configuration, initialization of repository/project starts.

```bash
Title of this repository(project): test_dir
>> EXECUTE: git init
Initialized empty Git repository in /Users/moinaga/test_dir/.git/
>> EXECUTE: touch .gitignore
>> EXECUTE: touch README.md
>> EXECUTE: echo ".*" >> .gitignore
>> EXECUTE: echo "# TEST_DIR" >> README.md
>> EXECUTE: git status --short
?? README.md
>> EXECUTE: git diff --stat
** no push **
```

##### If selected PATH has a `.git` folder
###### Example of File Tree
```bash
-- Main
     |--.git/
     |--tests/
     |    |--.git/  
     |    |--.gitignore  
     |    |--README.md  
     |    +--test.c
     |--.gitignore  
     |--README.md  
     +--main.c  
```

If user was in ...
- `Main`:
  1. If `-g` was abridged, it selects `Main/.git` as a target `.git` folder.
- `Main/tests`:
  1. If `-g` was abridged, it selects `Main/test/.git` as a target `.git` folder.
  2. If `-g` was set to `..` i.e. `-g ..`, it selects `Main/.git` as a target `.git` folder.

#### `-f` or `--filepath`

If user wants to `git add` only specific file, then please declare it with `-f <FILE>`. Otherwise, `git add .` will be executed by default.

#### `-b` or `--branch`

If user wants to specify committing branch, then please declare it with `-b <BRANCH>`. Otherwise, `master` branch will be used.

##### Example of Branch list
```bash
$ git branch
* master
  test
```
In the situation like above, where current branch was `master`:
- `-b master` or abridging `-b` does not make any change.
- `-b test` raises `BranchIssue` with number of choices.

```bash
>> BRANCH ISSUE!
Currently on branch `master` but tried to commit to branch `test`.
1: Merge branch `master` => branch `test`
2: Stay on branch `master`                   
3: Checkout to branch `test`  
Answer:
```
:warning:
__Merge option (1) is not recommended, since it does not take merge conflicts in consideration. `Ctrl-C` to abort.__
Newest version now applies patch before merge, which could avoid conflict.

If there are changes to commit and you choose option (3), there will be three choices to pick next.
```bash
>> BRANCH ISSUE!
Answer: 3

Theres some changes in branch `master`.
>> EXECUTE: git diff --stat
 doc/gch_doc.md | 51 ++++++++++++++++++++++++++++++++++++++++++---------
 1 file changed, 42 insertions(+), 9 deletions(-)
1: Commit changes of branch `master`
2: Stash changes of branch `master`
3: Force Checkout to branch `test`
Answer:
```
`git diff --stat` will be executed automatically.

 If you pick...
- 1, 2: `commit`/`stash` changes and `checkout`.
- 3: Execute `git checkout -f test`, ignoring all changes.

#### `-d` or `--detail`

Option for detailed `git diff`.

#### `-l` or `--log`

Display `git log` with some options.

#### `-c` or `--commit`

`git commit` with commit message.

#### `-u` or `--unstage`

`git rm -r <PATH>` if there are any staged files.

