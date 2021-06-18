# kousotsu-py
高卒たん理論をPythonで実装するスレより

・Docker と Gitをインストールしますん

・コンソールやターミナルで作業ディレクトリに異動します


・下記コマンドでGitからクローンをとります
　※カレントディレクトリにkousotsu-pyディレクトリができます

```
git clone https://github.com/tyaro/kousotsu-py.git
```

・`cd kousotsu-py` でディレクトリの中に入ります


・下記コマンドでDocker環境をビルドします

```
docker-compose build
```

・下記コマンドでDocker環境を立ち上げます。
　※初回は色々自動的にダウンロードされます

```
docker-compose up -d
```

Docker環境にインストールされるのは下記になります。
- mariadb ← データベース
- phpmyadmin ← データベース操作用
- nginx ← Web サーバ
- redis ← 今回使わないけど将来用
- python3 ← Python実行環境

・Docker のアプリ上で kousotsu-py が動いていることを確認します。

https://i.imgur.com/ngRmVpi.png

・phpmyadminをブラウザから開きます

https://i.imgur.com/v4OsgXw.png

・左のツリーで test_database を選択して右のペイン上部にあるSQLを選びます。

・kousotsu-py/mysql ディレクトリの中にある TABLE_BINANCE_CRYPTO_INFO.sql の中味をコピーして貼り付け

https://i.imgur.com/P9DVxHQ.png

・右下の実行ボタンを押すとテーブルができます

https://i.imgur.com/MH8KL3B.png

・出てこない場合は更新ボタンを押してみて下さい
https://i.imgur.com/p49ySzq.png

・下記ファイルも同様に貼り付け実行します。
- VIEW_BINANCE_CRYPTO_INFO.sql
- VIEW_BINANCE_CRYPTO_INFO_RESULT.sql
- VIEW_BINANCE_CRYPTO_INFO_STAR.sql

・Viewができます
https://i.imgur.com/J4uJj0r.png

・コンソールかターミナル上で下記コマンドを実行してpython実行環境に入ります。

```
docker container exec -it python3 /bin/bash
```

・無事 python実行環境に入れたら下記コマンドを実行します。
```
python HighSchool_V6.py
```

・なんか動き出します。

https://i.imgur.com/omiUmAl.png

・DBに順番に書き込まれているのでブラウザでphpmyadminを見に行きます。

https://i.imgur.com/IBrtlir.png

・ズボンを脱ぎます。

・たまにエラーがでて終了していますが、エラー処理とか皆無なので
　落ち着いてもういっかい実行したらだいたいいけます。

https://i.imgur.com/i0q004Q.png

・靴下ははいたままでお願いします。

・成功しました
https://i.imgur.com/dTkjnzz.png

・下記コマンドを実行してJSONファイルを生成します。

```
python JsonOutput.py 
```

・パンツを脱ぎます。

・nginx をブラウザで開きます。

https://i.imgur.com/9wKn6yG.png


・なんかでたああああああああ
https://i.imgur.com/77eKmca.png


以上で自分のPCで高卒たんページを表示させようを終わります。


自動実行とかは入れていないので各自いれて遊んでみて下さい。
