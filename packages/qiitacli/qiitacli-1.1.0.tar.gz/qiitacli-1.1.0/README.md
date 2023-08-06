# Welcome to QiitaCLI's documentation!

[![Build Status](https://travis-ci.org/mypaceshun/qiitacli.svg?branch=master)](https://travis-ci.org/mypaceshun/qiitacli)
[![codecov](https://codecov.io/gh/mypaceshun/qiitacli/branch/master/graph/badge.svg)](https://codecov.io/gh/mypaceshun/qiitacli)
[![PyPI](https://img.shields.io/pypi/v/qiitacli)](https://pypi.org/project/qiitacli/)



Qiita CLI Client

CUIでQiitaの投稿をしたくて作ったものです。

# Install

``` console
$ pip install qiitacli
```

# Document

https://mypaceshun.github.io/qiitacli

# QuickStart

## 事前準備

* Qiitaにアカウントを作成

https://qiita.com/

* Qiita個人用アクセストークンを取得

Qiitaにログイン後、設定→アプリケーション→個人用アクセストークンのところから新しくトークンを発行する。

スコープは`read_qiita`と`write_qiita`にチェックを入れてください。

発行後アクセストークンが表示されるのでコピー **ページを離れると再度アクセストークンを表示することは出来ません**

* statusコマンドを利用してアクセストークンを保存します。

``` console
$ qiitacli status
Input your personal accesstoken: xxxxx
id              : mypaceshun
name            : shun kawai
location        : Tokyo Japan
...
```

アクセストークンはデフォルトで`$HOME/.qiitacli.secret`に保存されます。
このファイルを直接編集することでも、アクセストークンを設定出来ます。

## 記事一覧取得

``` console
$ qiitacli list -idu
id|date|title|url
c3b97c4eee490d662092|2019-10-18T19:35:23+09:00|Qiita CLI Application 作ってみた|https://qiita.com/mypaceshun/items/c3b97c4eee490d662092
ab441d26a12489d5fcbd|2019-02-01T11:37:55+09:00|ansible 〜つなぐ〜|https://qiita.com/mypaceshun/items/ab441d26a12489d5fcbd
b1f3786ce0580201a9e1|2018-12-16T07:01:55+09:00|pythonアプリケーションをrpmにパッケージング|https://qiita.com/mypaceshun/items/b1f3786ce0580201a9e1
5067561d6739cc9e5199|2018-12-19T10:58:45+09:00|specファイル大解剖|https://qiita.com/mypaceshun/items/5067561d6739cc9e5199
feedced17884d798fbbd|2016-03-14T13:03:04+09:00|XAMPPでApacheを起動しAndroidから接続|https://qiita.com/mypaceshun/items/feedced17884d798fbbd
c489327d525522de5e65|2016-02-15T10:48:32+09:00|AndroidStudio2.0をインストールしてみる|https://qiita.com/mypaceshun/items/c489327d525522de5e65
```

## 記事の投稿

``` console
$ qiitacli upload article.md
```

記事用の`Markdown`ファイルでは、YAML形式のヘッダーを利用して、タイトルやタグなどの情報を記述します。
`title`と`tags`の情報が必須で、設定が無い場合はコマンドが失敗します。

[qiitacli.md](article/qiitacli.md) を参考にしてください。

## 記事の更新

``` console
$ qiitacli update articleid article.md
```

記事を更新する際は投稿に用いた`Markdown`ファイルと同様の形式で記事用ファイルを用意してください。
また上書きするための更新対象の記事のIDが必要になります。

`list`コマンドなどを用いて更新対象の記事のIDを探してみてください。

## 記事の削除

``` console
$ qiitacli delete articleid
```

記事の削除では、削除対象の記事のIDが必要になります。

`list`コマンドなどを用いて削除対象の記事のIDを探してみてください。

# Release

[リリースノート](https://github.com/mypaceshun/qiitacli/releases)
