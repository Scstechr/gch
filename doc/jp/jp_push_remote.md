## `-p`/`—push`, `-r`/`remote STR`

| タグ   | 用途         |  引数    | デフォルト |
| --------------- | --------------------------------- | ---- | --------------- |
| `-p`/`--push`   | `push`に用いられるフラグ          |   -   | - |
| `-r`/`--remote` | push`する`remote`レポジトリの指定 |    文字列  | `origin` |

### 使用例

#### `-r`/`—remote`で指定した`remote`レポジトリがなかった場合

```bash
$ gch -p
```
あるいは，`remote`レポジトリを指定して
```bash
$ gch -p -r develop
```
などを実行したとき，`remote`レポジトリがみつからないなら新たに追加するかどうか聞かれます．
```
>> warning!: Remote repository `origin` not found
Add? [y/N]:
```

追加する場合はURLを入力します．

```bash
URL: https://github.com/Scstechr/testr.git
>> execute: git remote add origin https://github.com/Scstechr/testr.git
>> execute: git push -u origin master
Counting objects: 10, done.
Delta compression using up to 4 threads.
Compressing objects: 100% (6/6), done.
Writing objects: 100% (10/10), 747 bytes | 373.00 KiB/s, done.
Total 10 (delta 2), reused 0 (delta 0)
remote: Resolving deltas: 100% (2/2), done.
To https://github.com/Scstechr/testr.git
 * [new branch]      master -> master
Branch 'master' set up to track remote branch 'master' from 'origin'.
```

たとえ`commit`してない変更があっても無視して最後の`commit`を`push`します．

例として，`b.txt`に変更を加えました．

```bash
$ gch -p
>> execute: git status --short
 M b.txt
>> execute: git diff --stat
 b.txt | 1 +
 1 file changed, 1 insertion(+)
>> execute: git push -u origin master
Branch 'master' set up to track remote branch 'master' from 'origin'.
Everything up-to-date
```

最新の変更を`commit`してから`push`するには`-cp`として同時に実行します．

```bash
$ gch -cp
>> execute: git status --short
 M b.txt
>> execute: git diff --stat
 b.txt | 1 +
 1 file changed, 1 insertion(+)
>> execute: git add /Users/moinaga/test
Commit Message: change b.txt
>> execute: git commit -m "change b.txt"
[master 7728e23] change b.txt
 1 file changed, 1 insertion(+)
>> execute: git push -u origin master
Counting objects: 3, done.
Delta compression using up to 4 threads.
Compressing objects: 100% (2/2), done.
Writing objects: 100% (3/3), 301 bytes | 301.00 KiB/s, done.
Total 3 (delta 1), reused 0 (delta 0)
remote: Resolving deltas: 100% (1/1), completed with 1 local object.
To https://github.com/Scstechr/testr.git
   e881006..7728e23  master -> master
Branch 'master' set up to track remote branch 'master' from 'origin'.
```

#### `push`に失敗した場合

ローカルで新たに`commit`をし，`pull`せずに`push`しようとした場合，

```bash
$ gch -cp
>> execute: git status --short
?? localnew.txt
>> execute: git diff --stat
>> execute: git add /Users/moinaga/test
Commit Message: add localnew
>> execute: git commit -m "add localnew"
[master 09b9d7c] add localnew
 1 file changed, 1 insertion(+)
 create mode 100644 localnew.txt
>> execute: git push -u origin master
To https://github.com/Scstechr/testr.git
 ! [rejected]        master -> master (fetch first)
error: failed to push some refs to 'https://github.com/Scstechr/testr.git'
hint: Updates were rejected because the remote contains work that you do
hint: not have locally. This is usually caused by another repository pushing
hint: to the same ref. You may want to first integrate the remote changes
hint: (e.g., 'git pull ...') before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.
```

このように警告が出ます．この場合は`gch —pull`などで`remote`のブランチとローカルのブランチを`merge`する必要があります．  
`gch`ではこのような`CONFLICT`や`merge`に対してはまだ実装していないので，  
`git pull`/`git rebase`/`git merge`について調べて対処してください．

