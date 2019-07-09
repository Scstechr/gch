##  `-l`/`--log`

| タグ         | 用途            | 引数 | デフォルト |
| ------------ | --------------- | ---- | ---------- |
| `-l`/`--log` | `git log`をする | -    | `False`    |

`git log`を実行します．

```bash
$ gch -l
>> execute: git status --short
>> execute: git log --stat --oneline --graph --decorate
* db69b12 (HEAD -> develop) change b.txt
|  b.txt | 1 -
|  1 file changed, 1 deletion(-)
*   f8a9f41 Merge branch 'master' of https://github.com/Scstechr/testr
|\
| * 4a9cc45 (origin/master) Create newfile
| |  newfile | 1 +
| |  1 file changed, 1 insertion(+)
* | 09b9d7c add localnew
|/
|    localnew.txt | 1 +
|    1 file changed, 1 insertion(+)
* 7728e23 change b.txt
|  b.txt | 1 +
|  1 file changed, 1 insertion(+)
* e881006 add b
|  b.txt | 1 +
|  1 file changed, 1 insertion(+)
* f6dc509 add a.c
|  a.c | 5 +++++
|  1 file changed, 5 insertions(+)
* f504b9d remove sub
   .gitignore | 1 +
   README.md  | 1 +
   2 files changed, 2 insertions(+)
```

今後機能を追加していく予定です．