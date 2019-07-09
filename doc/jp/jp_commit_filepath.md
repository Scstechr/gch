## `-c`/`—commit`, `-f`/`filepath PATH`

- `-c`/`--commit` は`commit`に用いられるフラグ（引数無し）．
- `-f`/`--file` は`add`するパスの指定に用いられる．引数はパス．

### 使用例

##### ファイルの構成例

```bash
.
├── .git/
├── .gitignore
├── a.c
├── b.txt
└── README.md
```

単に`gch -c`する場合を考えます．
このとき，`git add .`, `git commit`が実行されます．

```bash
$ gch -c
>> execute: git status --short
 M .gitignore
 M a.c
?? b.txt
>> execute: git diff --stat
 .gitignore | 1 +
 a.c        | 1 +
 2 files changed, 2 insertions(+)
>> execute: git add .
Commit Message: add lines to a.c. add b.txt.
>> execute: git commit -m "add lines to a.c. add b.txt."
[master a0c369e] add lines to a.c. add b.txt.
 3 files changed, 3 insertions(+)
 create mode 100644 b.txt

>> No push
```

次に，`-f`/`--filepath`で`stage`するファイルを指定します．

```bash
$ gch -c -f b.txt
>> execute: git status --short
 M .gitignore
 M a.c
?? b.txt
>> execute: git diff --stat
 .gitignore | 1 +
 a.c        | 1 +
 2 files changed, 2 insertions(+)
>> execute: git add ./b.txt
Commit Message: add b.txt
>> execute: git commit -m "add b.txt"
[master 79f16c1] add b.txt
 1 file changed, 1 insertion(+)
 create mode 100644 b.txt

>> No push
```

今度は`b.txt`のみが`add`され，他のファイルが`unstage`されました．  
実際，`a.c`と`.gitignore`は変更があったにもかかわらず`commit`されませんでした．
```bash
$ git status --short
 M .gitignore
 M a.cz
```

#### `-v`/`—verbose`あり．

```bash
$ gch -vc
>> execute: git status --short
M  a.c
>> execute: git diff --stat
>> execute: git add .
>> execute: git diff --cached --ignore-all-space --ignore-blank-lines
diff --git a/a.c b/a.c
index 2b27515..a4164a4 100644
--- a/a.c
+++ b/a.c
@@ -1,5 +1,6 @@
 #include <stdio.h>

 int main(){
+       printf("Hello World\n");
        ;
 }
>> execute: git reset
Unstaged changes after reset:
M	a.c
>> execute: git add /Users/moinaga/test
Commit Message:
```

`-v`/`--verbose`をつけることで情報を増やすことができます．
差分などを見てから`commit`したいときなどに有用です．

