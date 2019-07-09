# GCH: Git Commit Handler
__GCH__ (Git Commit Handler, 以下:`gch`)  の公式ドキュメントです.

### インストール
```bash
$ git clone https://github.com/Scstechr/usefultools.git ~/.useful
$ cd ~/.useful
$ pip install -r requirements.txt
```

### 推奨の使用方法

 `alias` を設定することで `gch` をどこからでも実行できるようにすると良いです．  

```bash:.bash_profile
export PATH="${HOME}/.gch:$PATH"
alias gch='gch.py'
```

上記を `~/.bashrc`に追加するか，下記を実行すし`source ~/.bashrc` するとできます．

```bash:add
echo 'PATH="${HOME}/.gch:$PATH"' >> ~/.bashrc
echo 'alias gch="gch.py"' >> ~/.bash_profile
```

`gch`のアップデート方法は今までよりも簡単になりました．

```bash
$ gch -u 
```

### オプション
```sh
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


`gch`で実行されるシェルのコマンドは以下のように可視化されて実行されます．

```bash
>> EXECUTE: git status --short
```
すなわち，ユーザ自身が上記のコマンドをシェルで実行することを`gch`は代行しているといえます．
実行中は`CTRL-C`で処理を中断することができます．

## `gch`を用いた場合の一連の流れ

必要なら`-g`/`—gitpath`で`.git`ディレクトリのパスを指定してください．(デフォルト:`.`)
#### (0) `init`
`-g`で指定したパスに`.git`がない場合は初期化(`-i`/`--initialize`)が実行されます．

#### (1) `-c`/`—commit`で`commit`する．
必要に応じて`-b`/`-f`/`-g`を併用してください．
- `-b`/`--branch`で`commit`するブランチを指定．(デフォルト:`master`)
- `-f`/`--filepath`で`add`するファイル/パスを指定．(デフォルト:`.`)
- `-g`/`—gitpath`で`.git`ディレクトリのパスを指定．(デフォルト:`.`)

#### (2) `-p`/`—push`で`push`する．
必要に応じて`-b`/`-r`/`-g`を併用してください．
- `-b`/`--branch`で`push`するブランチを指定．(デフォルト:`master`)
- `-r`/`--remote`で`push`する`remote`レポジトリを指定．(デフォルト:`origin`)
- `-g`/`—gitpath`で`.git`ディレクトリのパスを指定．(デフォルト:`.`)

さらに，以下を使い分けることでさらに効率よく`git`が使えます．
####　その他
##### `git`関連
- `-l`/`—log`で`git log`表示．（`vim`を`CTRL-C`で抜けると`reset`が必要）
- `-d`/`—diff`で`git diff`用のツールを起動．
- `—reset`で`git reset`用のツールを起動．
- `—pull`で`git pull`をする（非推奨）．

##### `gch`関連
- `-s`/`--save`で直前の設定を`.defaults.txt`に保存．
- `-v`/`--verbose`で情報量を増やす．
- `-u`/`—update`で`gch`自体をアップデートする．
- `-—help`で`gch`の全てのオプションを表示する．

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
最新版ではパッチを適用することで事前に`conflict`が発生する場合は中断できるようになりましたが，  
それでも100%安全とは言えないのでこのツールを用いての`merge`はコンフリクトが発生しないことが自明でない限り避けてください．

3を選択した場合，前回の`commit`から変更されたファイルが存在しない場合は指定したブランチに`checkout`します．  
前述の条件を満たさない場合，`BRANCH ISSUE!`が発生します．  
この際`git diff --stat`は自動的に実行されます.

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

1, 2を選択した場合，`commit`/`stash`後に指定したブランチに`checkout`します．  
3を選択した場合，`git checkout -f <BRANCH>`が実行されます．  
このとき，前回の`commit`から変更した箇所は全て破棄されます．