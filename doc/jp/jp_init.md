## `-i`/`—init`

| タグ   | 用途         |  引数    | デフォルト |
| --------------- | --------------------------------- | ---- | --------------- |
| `-i`/`--init`   | 初期化に用いられるフラグ          |   -   | `False` |

`-g`で指定したパス(デフォルト:`.`)に`.git`ディレクトリががない場合を想定します．

```bash
.
```

この状態で`gch`を走らせると，以下のような警告がが出ます．

```bash
$ gch

>> warning!: It seems path:`.` does not have `.git` folder.
Initialize? [y/N]:
```
`y`を入力した場合 かつ `~/.gitconfig`が存在しない場合は(a)が実行されます.  

##### (a) `username`, `email`, `editor`, `diff-tool`の設定

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
この設定は別途`gch -i`を走らせることでも可能です．  
その後(b)が実行されます．

#### レポジトリの初期化 `git init`

まず，レポジトリ名を設定します．  

```bash
Initialize? [y/N]: y
Title of this repository(project): test repository
```
ここで入力したレポジトリ名は`README.md`のタイトルとして使用されます．
次に，`.git`フォルダの作成，`*.`を書き込んだ`.gitignore`，
そしてレポジトリ名が入った`README.md`が生成されます．
```bash
>> execute: git init
Initialized empty Git repository in /Users/moinaga/test/.git/
>> execute: touch .gitignore
>> execute: touch README.md
>> execute: echo ".*" >> .gitignore
>> execute: echo "# TEST REPOSITORY" >> README.md
>> execute: git add -f .gitignore
>> execute: git status --short
A  .gitignore
?? README.md
>> execute: git diff --stat

>> No push
```

##### ファイル生成後
```bash
.
├── .git/
├── .gitignore
└── README.md
```
