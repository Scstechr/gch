
## `-v/—verbose`
| タグ   | 用途         |  引数    | デフォルト |
| --------------- | --------------------------------- | ---- | --------------- |
| `-v`/`--verbose`   | 情報を増やすフラグ          |   -   | `False` |

### 使用例

##### ファイルの構成例

```bash
.
├── .git/
├── .gitignore
├── a.c
└── README.md
```

この状態で以前に`gch -c`/`git commit`している状態を想定します．
#### (1) `-v`のみ
```bash
$ gch -v
>> execute: git status --short
 M a.c
>> execute: git diff --stat
 a.c | 1 +
 1 file changed, 1 insertion(+)
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

>> No push
```
簡単に前回の`commit`からの差分を確認するのに有用です．
#### (1) `-c`/`—commit`
##### (a) `-v`/`—verbose`なし．
```bash
$ gch -c
>> execute: git status --short
 M a.c
>> execute: git diff --stat
 a.c | 1 +
 1 file changed, 1 insertion(+)
>> execute: git add /Users/moinaga/test
Commit Message:
```

##### (b) `-v`/`—verbose`あり．
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

#### (2)  `-d/—diff`

##### (a) `-v`/`—verbose`なし．

```bash
$ gch -d
Do you want to name specific author? [y/N]:
──────────────────────────────────────────────────────────
selected: ['HEAD', 'f6dc509']
──────────────────────────────────────────────────────────
HEAD
(19 minutes ago) [f6dc509] [c29fcc6] Scstechr add a.c
(19 minutes ago) [f504b9d] [2b34920] Scstechr remove sub


──────────────────────────────────────────────────────────
[1/1]
──────────────────────────────────────────────────────────
>> execute: git diff --stat f6dc509
 a.c | 1 +
 1 file changed, 1 insertion(+)
```

##### (b) `-v`/`—verbose`あり．

```bash
$ gch -vd
Do you want to name specific author? [y/N]:
──────────────────────────────────────────────────────────
selected: ['HEAD', 'f6dc509']
──────────────────────────────────────────────────────────
HEAD
(19 minutes ago) [f6dc509] [c29fcc6] Scstechr add a.c
(19 minutes ago) [f504b9d] [2b34920] Scstechr remove sub


──────────────────────────────────────────────────────────
[1/1]
──────────────────────────────────────────────────────────
>> execute: git diff --stat f6dc509
 a.c | 1 +
 1 file changed, 1 insertion(+)
>> execute: git diff --ignore-blank-lines -U1 f6dc509
diff --git a/a.c b/a.c
index 2b27515..a4164a4 100644
--- a/a.c
+++ b/a.c
@@ -3,2 +3,3 @@
 int main(){
+       printf("Hello World\n");
        ;

```

