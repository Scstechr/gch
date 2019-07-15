## `-d`/`—diff`
| タグ   | 用途         |  引数    | デフォルト |
| --------------- | --------------------------------- | ---- | --------------- |
| `-d`/`--diff`   | `gch`版`diff-tool`を起動するフラグ          |   -   | `False` |

`gch`から簡易版`gdiff`を起動することができます．  
完全な`gdiff`は以下の引数を持ちます．
```bash
$ gdiff --help
Usage: gdiff [OPTIONS]

Options:
  -v, --verbose  Detailed diff.
  -h, --head     Include HEAD^ from the beginning.
  -a, --author   Name specific author.
  -l, --log      User log ver. instead.
  --version      Check version of gdiff.
  --help         Show this message and exit.
```

| タグ   | 用途         |  引数    | デフォルト |
| --------------- | --------------------------------- | ---- | --------------- |
| `-v`/`--verbose`   | 情報量を増やすフラグ．         |   -   | `False` |
| `-h`/`--head`   | `HEAD`がある場合にそれと他の`commit`を比較する．         |   -   | `False` |
| `-a`/`--author`   | 特定の著者を指定するフラグ．         |   -   | `False` |
| `-l`/`--log`   | Logviewerを使う．         |   -   | `False` |
| `--version`   | `gdiff`のバージョン確認         |   -   | `False` |

このうち，`-v`/`--verbose`は`gch`から起動した場合は設定が共有されます．  
これはColumnViewer, Logviewerのどちらにおいても途中から`v`を押すことで有効にできます．  
また， どちらもターミナルの大きさで表示される内容が変化します．

### ColumnViewer (デフォルト)
それぞれ`(時刻)` `コミットのハッシュ` `ツリーのハッシュ` `著者` `コミットメッセージ` の順に表示されます．
```bash
$ gdiff
───────────────────────────────────────────────────────────────────
selected: []
───────────────────────────────────────────────────────────────────
  (55 minutes ago) [db69b12] [0f19859] Scstechr change b.txt
> (2 hours ago) [f8a9f41] [26fd660] Scstechr Merge branch 'mas...
  (2 hours ago) [09b9d7c] [93b3209] Scstechr add localnew
  (2 hours ago) [7728e23] [c3abdd3] Scstechr change b.txt
  (3 hours ago) [e881006] [2018977] Scstechr add b
  (3 hours ago) [f6dc509] [c29fcc6] Scstechr add a.c
  (3 hours ago) [f504b9d] [2b34920] Scstechr remove sub


───────────────────────────────────────────────────────────────────
[1/1] | [hjkl]:[←↓↑→],q:QUIT,v:VERBOSE,s/Enter:SELECT
───────────────────────────────────────────────────────────────────


```
移動には`hjkl`(←↓↑→），決定は`Enter`が使われます．  
選択した場合，その行が灰色になり，二つ選択すると`diff`が表示されます．
```bash
───────────────────────────────────────────────────────────────────
selected: ['db69b12', 'f8a9f41']
───────────────────────────────────────────────────────────────────
  (58 minutes ago) [db69b12] [0f19859] Scstechr change b.txt
  (2 hours ago) [f8a9f41] [26fd660] Scstechr Merge branch 'mas...
  (2 hours ago) [09b9d7c] [93b3209] Scstechr add localnew
  (2 hours ago) [4a9cc45] [49bbd1c] Masaru Oinaga Create newfile
  (2 hours ago) [7728e23] [c3abdd3] Scstechr change b.txt
  (3 hours ago) [e881006] [2018977] Scstechr add b
  (4 hours ago) [f6dc509] [c29fcc6] Scstechr add a.c
  (4 hours ago) [f504b9d] [2b34920] Scstechr remove sub


───────────────────────────────────────────────────────────────────
[1/1] | [hjkl]:[←↓↑→],q:QUIT,v:VERBOSE,s/Enter:SELECT
───────────────────────────────────────────────────────────────────
>> execute: git diff --stat db69b12..f8a9f41
 b.txt | 1 +
 1 file changed, 1 insertion(+)
```

`-v`/`--verbose`フラグを有効にすることで`diff`が詳細になります．
```bash
>> execute: git diff --stat db69b12..f8a9f41
 b.txt | 1 +
 1 file changed, 1 insertion(+)
>> execute: git diff --ignore-blank-lines -U1 db69b12..f8a9f41
diff --git a/b.txt b/b.txt
index cd94258..127927a 100644
--- a/b.txt
+++ b/b.txt
@@ -1 +1,2 @@
 I wanna be your gentleman
+Finding a way of life
```

### LogViewer

```bash
$ gdiff -l
───────────────────────────────────────────────────────────────────
SELECTED: []
───────────────────────────────────────────────────────────────────
> * (6 minutes ago) [48d9a27] <Masaru Oinaga> Update README.md
  * (11 hours ago) [d2f10f7] <Masaru Oinaga> Update README.md
  *   (16 hours ago) [233633d] <Scstechr> Merge branch 'master...
  |\
  | * (16 hours ago) [123efc8] <Masaru Oinaga> Update gch_doc_...
  | * (16 hours ago) [e39096d] <Masaru Oinaga> Update README.md
  * | (16 hours ago) [ef51dfb] <Scstechr> fix pull
  * | (16 hours ago) [a061df9] <Scstechr> delete build.sh
  |/
  * (19 hours ago) [bd842cf] <Scstechr> display versions with ...
  * (19 hours ago) [51cde09] <Scstechr> remove checkout option
  * (19 hours ago) [c69b5a6] <Scstechr> add build.sh. remove u...
  * (21 hours ago) [4f2e646] <Scstechr> mv difftool -> gdiff
  * (21 hours ago) [039aa2d] <Scstechr> erase dist, build
───────────────────────────────────────────────────────────────────
| [hj]:[←↓],q:QUIT,v:VERBOSE,s/Enter:SELECT
───────────────────────────────────────────────────────────────────
```

終了するには選択画面中に`q`を押すか
```bash
Do you want to exit diff hash tool? [y/N]:
```
上記の質問で`y`を選択してください．
