__GCH__ (Git Commit Handler, 以下:`gch`)  の公式ドキュメントです.

[TOC]

# インストール
```bash
$ git clone https://github.com/Scstechr/usefultools.git ~/.useful
$ cd ~/.useful
$ pip install -r requirements.txt
```

# 推奨の使用方法

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

## オプション
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

# `gch`を用いた場合の一連の流れ

必要なら`-g`/`—gitpath`で`.git`ディレクトリのパスを指定してください．(デフォルト:`.`)[(詳細)](https://github.com/Scstechr/gch/blob/master/doc/jp/jp_gitpath.md)


## (0) `init`
`-g`で指定したパスに`.git`がない場合は初期化(`-i`/`--initialize`)が実行されます．

## (1) `-c`/`—commit`で`commit`する．[(詳細)](https://github.com/Scstechr/gch/blob/master/doc/jp/jp_commit_filepath.md)
必要に応じて`-b`/`-f`/`-g`を併用してください．
- `-b`/`--branch`で`commit`するブランチを指定．(デフォルト:`master`)[(詳細)](https://github.com/Scstechr/gch/blob/master/doc/jp/jp_branch.md)
- `-f`/`--filepath`で`add`するファイル/パスを指定．(デフォルト:`.`)
- `-g`/`—gitpath`で`.git`ディレクトリのパスを指定．(デフォルト:`.`)

## (2) `-p`/`—push`で`push`する．
必要に応じて`-b`/`-r`/`-g`を併用してください．[(詳細)](https://github.com/Scstechr/gch/blob/master/doc/jp/jp_push_remote.md)
- `-b`/`--branch`で`push`するブランチを指定．(デフォルト:`master`)[(詳細)](https://github.com/Scstechr/gch/blob/master/doc/jp/jp_branch.md)
- `-r`/`--remote`で`push`する`remote`レポジトリを指定．(デフォルト:`origin`)
- `-g`/`—gitpath`で`.git`ディレクトリのパスを指定．(デフォルト:`.`)

さらに，以下を使い分けることでさらに効率よく`git`が使えます．
##　その他
### `git`関連
- `-l`/`—log`で`git log`表示．（`vim`を`CTRL-C`で抜けると`reset`が必要）[(詳細)](https://github.com/Scstechr/gch/blob/master/doc/jp/jp_log.md)
- `-d`/`—diff`で`git diff`用のツールを起動．[(詳細)](https://github.com/Scstechr/gch/blob/master/doc/jp/jp_diff.md)
- `—reset`で`git reset`用のツールを起動．[(詳細)](https://github.com/Scstechr/gch/blob/master/doc/jp/jp_reset.md)
- `—pull`で`git pull`をする（非推奨）．

### `gch`関連
- `-s`/`--save`で直前の設定を`.defaults.txt`に保存．[(詳細)](https://github.com/Scstechr/gch/blob/master/doc/jp/jp_other.md)
- `-v`/`--verbose`で情報量を増やす．[(詳細)](https://github.com/Scstechr/gch/blob/master/doc/jp/jp_verbose.md)
- `-u`/`—update`で`gch`自体をアップデートする．[(詳細)](https://github.com/Scstechr/gch/blob/master/doc/jp/jp_other.md)
- `-—help`で`gch`の全てのオプションを表示する．
