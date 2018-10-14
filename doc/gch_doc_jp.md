# GCH: Git Commit Handler
__GCH__ (Git Commit Handler)の公式ドキュメントです.

### インストール
```bash
$ git clone https://github.com/Scstechr/usefultools.git ~/.useful
$ cd ~/.useful
$ pip install -r requirements.txt
```

#### アップデート方法
```bash
$ git pull origin master
```

### オプション
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
  -r, --reset          Reset (remove all add).           > Default: False
  --help               Show this message and exit.
```



`git clone`してインストールした後に`.bash_profile` に PATHを通した上で`alias gch='gch.py'`といった`alias`と組み合わせて使うことを推奨しています．__GCH__ で実行されるシェルのコマンドは以下のように可視化されて実行されます．
```bash
>> EXECUTE: git status --short
```
すなわち，ユーザ自身が上記のコマンドをシェルで実行することをGCHは代行しているといえます．


#### `-g` or `--gitpath`

`git --git-dir=<path>`と同様の機能を有しています．
ここで，どの`.git`を使うかパスで指定することができます．
省略した場合，`.`にある`.git`を用いて動作を行います．

##### 指定したパスに`.git`が存在しない場合

```bash
$ gch

>> WARNING!: It seems path:`<PATH>` does not have `.git` folder.
Initialize? [y/N]:
```
`y`を入力した場合 かつ `~/.gitconfig`が存在しない場合は`username`, `email`, `editor`, `diff-tool`の設定を行います．

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
その後, レポジトリの初期設定を始めます．予め`~/.gitconfig`が存在する場合は上の設定をスキップします．
この際，レポジトリ名を設定します．ここで入力したレポジトリ名は`README.md`のタイトルとして使用されます．
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
初期化と同時に`*.`を書き込んだ`.gitignore`とレポジトリ名が入った`README.md`が生成されていることがわかると思います．

##### 指定したパスに`.git`が存在する場合
###### 構成例
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

ユーザがどのフォルダにいるかで動作が異なります．
- `Main`にいた場合:
  1. `-g`が省略された場合, `Main/.git`を用います．
- `Main/tests`にいた場合:
  1. `-g`が省略された場合, `Main/test/.git`を用います.
  2. `-g ..`とパスを指定した場合， `Main/.git`を用います.

#### `-f` or `--filepath`

特定のファイルのみを `git add` したい場合， `-f <FILE>`のように指定することができます.
`-f`を省略した場合`.`の(`.gitignore`で指定されたファイルを除く)全てのファイルを`git add`します．

#### `-b` or `--branch`

`commit`に用いるブランチを指定することができます．
`-b`を省略した場合，`master`ブランチを用います．

##### ブランチの一覧例
```bash
$ git branch
* master
  test
```
上記の状態(すなわち現在のブランチが`master`ブランチ)の場合，`-b master` あるいは `-b` を省略した場合ブランチの切り替えは行われません．
一方で，`-b test`のように`commit`するブランチを指定し，かつ指定したブランチが現在のブランチと異なる場合，`BRANCH ISSUE!`が発生します．

```bash
>> BRANCH ISSUE!
Currently on branch `master` but tried to commit to branch `test`.
1: Merge branch `master` => branch `test`
2: Stay on branch `master`                   
3: Checkout to branch `test`  
Answer:
```
このような選択が必要な場合，`Ctrl-C`を実行することでGCHの動作を中断することができます．

:warning: __`merge`を実行する1つめの選択肢は，あらかじめ`merge conflict`が発生しないことが予測された場合を除き推奨されていません__.
最新版ではパッチを適用することで事前に`conflict`が発生する場合は中断できるようになりました．

3を選択した場合，前回の`commit`から変更されたファイルが存在しない場合は指定したブランチに`checkout`します．前述の条件を満たさない場合，`BRANCH ISSUE!`が発生します．この際`git diff --stat`は自動的に実行されます.

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

1, 2を選択した場合，`commit`/`stash`後に指定したブランチに`checkout`します． 3を選択した場合，`git checkout -f <BRANCH>`が実行されます．このとき，前回の`commit`から変更した箇所は全て破棄されます．

#### `-d` or `--detail`

`git diff`が詳細になるオプションを有効にします. `diff-tools`として`vimdiff`を想定しています．オプションについては実行時に確認できます．

#### `-l` or `--log`

作者が考える最善なオプションを付加された`git log`を実行します．オプションについては実行時に確認できます．

#### `-c` or `--commit`

省略した場合，`git commit`は実行されません.

#### `-r` or `--reset`

それまでに`git add`したファイルがあった場合はそれらを取り消します．
