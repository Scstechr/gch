### Requirements
Please install all the packages listed in `requirements.txt`.

```bash
git clone https://github.com/Scstechr/usefultools ~/.useful
cd ~/.useful
pip install -r requirements.txt
```
Also, be sure you have `Python 3.6.x` executable in any way.

### List of tools

| name | filename | description |
|:-----|:---------|:------------|
| Git Commit Handler |`gch.py` | Handles git commands |
| GCC Compiler + | `gcc.py` | Additional capability for compiling C codes |
| Auto-Executor | `ae.py` | Automatically executes given command |
| Color Check | `colors.py` | Displays list of colors to pick |

#### Git Commit Handler
```bash
Usage: gch.py [OPTIONS]

Options:
  -i, --init           run initializer or not.               >Default:False
  -d, --detail         Detailed diff.                        >Default:False
  -l, --log            Git log with option.                  >Default:False
  -c, --commit         Commit or not.                        >Default:False
  -r, --remote TEXT    Choose which remote repo.to push.     >Default:origin
  -p, --push           Push or not.                          >Default:False
  -g, --gitpath PATH   Path of dir that contains `.git`.     >Default:.
  -f, --filepath TEXT  Path/Regex of staging file/dir.       >Default:.
  -b, --branch TEXT    Commiting branch.                     >Default:master
  -s, --save           Save settings                         >Default:False
  --reset              Reset all changes since last commit.  >Default:False
  --pull               git pull origin master                >Default:False
  --help               Show this message and exit.
```
- Executes `git` related commands as such:
	- `git init`, `git commit`, `git diff`, `git add`, `git push`
- Document available: :us: [English](doc/gch_doc_en.md) / :jp: [Japanese](doc/gch_doc_jp.md)
	- :warning: It has not been updated for long time. Make an issue if any problem occurs.

#### GCC Compiler
```bash
$ gcc --help
Usage: gcc.py [OPTIONS] FILENAME

Options:
  -d, --debug  LLDB MODE TRIGGER
  -r, --run    RUN AFTER COMPILE
  --help       Show this message and exit.
```
- Compiles C codes with options below and generates output file in form of `<something>.out`.

```bash
-O3 -Wall -mtune=native -march=native -o <output>
```

- If debug mode is triggered, it compiles C codes with additional options listed below.
Runs LLDB after compiling is done.

```bash
-pg -g -fprofile-arcs -ftest-coverage
```

Also, if `gcc-7` is executable, it uses instead of normal `gcc` (which might be alias of `clang`).


#### Auto-Executor
```bash
$ ./ae.py --help
Usage: ae.py [OPTIONS] EXECUTE SLEEP

Options:
  -r, --rep INTEGER  Maximum Repetition. Default set to Infinit.
  --help             Show this message and exit.
```
- Automatically executes the command with some time gap in between.
- Able to set number of repetition.

```bash
$ ./ae.py 'ls' 2

1st 2018-03-09 22:50:49 >> EXECUTE: ls

LICENSE			ae.py			requirements.txt
README.md		colors.py
__pycache__		gch.py

2nd 2018-03-09 22:50:51 >> EXECUTE: ls

LICENSE			ae.py			requirements.txt
README.md		colors.py
__pycache__		gch.py

3rd 2018-03-09 22:50:53 >> EXECUTE: ls

LICENSE			ae.py			requirements.txt
README.md		colors.py
__pycache__		gch.py

...(Ctrl-C to stop)
```

### Recommended settings:
Add these lines in `.bash_profile` and `source` it afterwards.

```bash:.bash_profile
export "PATH=${HOME}/.useful:$PATH"
alias gch='gch.py'
alias gcc='gcc.py' # be careful of this alias setting.
alias ae='ae.py'
alias col='colors.py'
```



