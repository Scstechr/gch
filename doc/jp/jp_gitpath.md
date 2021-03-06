## `-g`/`—gitpath PATH`
| タグ   | 用途         |  引数    | デフォルト |
| --------------- | --------------------------------- | ---- | --------------- |
| `-g`/`--gitpath`   | `.git`ディレクトリの指定          |   パス   | `.` |

#### (1) `.git`がないディレクトリで`gch`を実行した場合

`-i`/`—initialize`が実行されます．

#### (2)  現在，あるいは`-g`で指定したディレクトリに`.git`がある状態で`gch`を実行した場合

ユーザがどのフォルダにいるかで動作が異なります．
##### ファイル構成例
```bash
.
├── .git/
├── .gitignore
├── README.md
└── sub/
    ├── .git
    ├── .gitignore
    └── README.md
```

##### (A) `.`にいた場合 :

1. `-g`が省略された場合, `./.git`を用います．


##### (B)`./sub`にいた場合:
  1. `-g`が省略された場合, `./sub/.git`を用います.
  2. `-g ..`とパスを指定した場合， `./.git`を用います.
