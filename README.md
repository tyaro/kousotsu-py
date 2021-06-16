# kousotsu-py
高卒たん理論をPythonで実装するスレより

mysql フォルダに data initdb.d my.cnf のディレクトリを作って下さい

↓こんな感じのディレクトリ構造になります。

```
docker
|-- python
|-- mysql
|   |-- data
|   |-- initdb.d
|   |-- my.cnf
``` 
 

Dockerをインストールしたらターミナル上でディレクトリに入り下記コマンドを実行します。

```
~/docker$ docker-compose build
~/docker$ docker-compose up -d
```

するとなんというかコンテナが立ち上がります。

※mysqlフォルダにテーブルとビューを作るｓｑｌがあるのでphpmyadminからでも実行してください。

Dockerのダッシュボードからphpmyadminのコンテナのところにあるブラウザを開くするとなんか立ち上がります。

vscodeやらなんやらで python3のコンテナにアタッチして

コンソールから下記を実行するとBinanceからデータを取得してDBに書き込み始めます
```
python HighSchool_V6.py
```

というかPythonコンテナじゃなくてCentOSのコンテナにしておけばよかった・・・


