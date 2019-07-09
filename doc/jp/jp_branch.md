##  `-b`/`branch STR`

| タグ   | 用途         |  引数    | デフォルト |
| --------------- | --------------------------------- | ---- | --------------- |
| `-b`/`--branch` | `commit`/`push`するブランチの指定 |    文字列  | `master` |

### 実行例
`commit`や`push`する際にブランチを指定できます．
```bash
$ gch -c -b test
$ gch -p -b develop
$ gch -cp -b master
```

下記の状態で`branch ISSUE!`が発生します.
1. 指定したブランチがなかった場合
2. 指定したブランチがあるが，現在のブランチではない場合

#### 1. 指定したブランチがなかった場合

このとき，`branch ISSUE!`が発生します．
```bash
$ gch -b develop
>> execute: git status --short

>> Clean State

>> branch ISSUE!

>> warning!: Branch `develop` not found.
1: Make new branch `develop`
2: Stay on current branch `master`
Answer:
```

1. 指定したブランチを作成しへ`checkout`する
2. 指定したブランチを無視して現在のブランチで`commit`する

1を選んだ場合，`commit`してない変更があるなしにかかわらずブランチを新たに作成して`checkout`します．
```bash
$ gch -b develop
>> execute: git status --short
 M b.txt
>> execute: git diff --stat
 b.txt | 1 -
 1 file changed, 1 deletion(-)

>> branch ISSUE!

>> warning!: Branch `develop` not found.
1: Make new branch `develop`
2: Stay on current branch `master`
Answer: 1
>> execute: git checkout -b develop
M	b.txt
Switched to a new branch 'develop'

>> No push
```

#### 2. 指定したブランチがあるが，現在のブランチではない場合
このときも，`branch ISSUE!`が発生します．
```bash
>> execute: git status --short

>> Clean State

>> branch ISSUE!
Currently on branch `develop` but tried to commit to branch `master`.
1: Merge branch `develop` => branch `master`
2: Stay on branch `develop`
3: Checkout to branch `master`
Answer:
```
1. 現在のブランチと指定したブランチを`merge`する（非推奨）
2. 指定したブランチを無視して現在のブランチで`commit`する
3. 指定したブランチへと`checkout`する．

3を選択した場合，(A)と(B)に分岐します．
##### (A) `commit`してない変更がない場合
指定したブランチへと`checkout`します．
```
Answer: 3
>> execute: git checkout master
Switched to branch 'master'
Your branch is ahead of 'origin/master' by 2 commits.
  (use "git push" to publish your local commits)

>> No push
```
##### (B) `commit`してない変更がある場合
変更についての対処を選択する必要があります．
```bash
Answer: 3

Theres some changes in branch `develop`.
>> execute: git diff --stat
 b.txt | 1 -
 1 file changed, 1 deletion(-)
1: Commit changes of branch `develop`
2: Stash changes of branch `develop`
3: Force Checkout to branch `master`
```