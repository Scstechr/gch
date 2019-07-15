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

### Click Runtime Error:
There exists an Runtime error such as:
```bash
$ gch
Traceback (most recent call last):
  File "gch.py", line 177, in <module>
  File "site-packages/click/core.py", line 764, in __call__
  File "site-packages/click/core.py", line 696, in main
  File "site-packages/click/_unicodefun.py", line 124, in _verify_python3_env
RuntimeError: Click will abort further execution because Python 3 was configured to use ASCII as encoding for the environment. Consult https://click.palletsprojects.com/en/7.x/python3/ for mitigation steps.

This system lists a couple of UTF-8 supporting locales that
you can pick from.  The following suitable locales were
discovered: af_ZA.UTF-8, am_ET.UTF-8, be_BY.UTF-8, bg_BG.UTF-8, ca_ES.UTF-8, cs_CZ.UTF-8, da_DK.UTF-8, de_AT.UTF-8, de_CH.UTF-8, de_DE.UTF-8, el_GR.UTF-8, en_AU.UTF-8, en_CA.UTF-8, en_GB.UTF-8, en_IE.UTF-8, en_NZ.UTF-8, en_US.UTF-8, es_ES.UTF-8, et_EE.UTF-8, eu_ES.UTF-8, fi_FI.UTF-8, fr_BE.UTF-8, fr_CA.UTF-8, fr_CH.UTF-8, fr_FR.UTF-8, he_IL.UTF-8, hr_HR.UTF-8, hu_HU.UTF-8, hy_AM.UTF-8, is_IS.UTF-8, it_CH.UTF-8, it_IT.UTF-8, ja_JP.UTF-8, kk_KZ.UTF-8, ko_KR.UTF-8, lt_LT.UTF-8, nl_BE.UTF-8, nl_NL.UTF-8, no_NO.UTF-8, pl_PL.UTF-8, pt_BR.UTF-8, pt_PT.UTF-8, ro_RO.UTF-8, ru_RU.UTF-8, sk_SK.UTF-8, sl_SI.UTF-8, sr_YU.UTF-8, sv_SE.UTF-8, tr_TR.UTF-8, uk_UA.UTF-8, zh_CN.UTF-8, zh_HK.UTF-8, zh_TW.UTF-8
[1044] Failed to execute script gch
```
To fix this, execute commands below:
```bash
$ export LC_ALL=en_US.utf-8
$ export LANG=en_US.utf-8
```
Because of this issue, `click` is planed to be replaced with `argparse` in the near future.
## How to Use

### Show help

```bash
$ gch --help
Usage: gch [OPTIONS]

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
  --version            Check version of gch                  >Default:False
  --reset              Reset all changes since last commit.  >Default:False
  --pull               Fetch + Merge from <origin> <master>. >Default:False
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




