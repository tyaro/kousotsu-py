# -*- coding: utf-8 -*-
import mysql.connector as mydb
import pandas as pd
import sqlalchemy as sa
import json
from datetime import date,datetime
import pprint
import csv

# date, datetimeの変換関数
def json_serial(obj):
    # 日付型の場合を文字列に変換します
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()

# CSVファイルからJSONへ
def csv2json(csvFile,jsonFile):
    dataList = []
    with open(csvFile, 'r',encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            dataList.append(row)
    with open(jsonFile, 'w',encoding='utf-8') as f:
        json.dump(dataList, f,ensure_ascii=False,indent=4)
    

if __name__ == "__main__":
    host = 'localhost',
    port = '3306',
    user = 'docker',
    password = 'docker',
    database = 'test_database'

    # SQLへのコネクションの作成
    # ユーザー名・パスワードはMySQLのものを。
    # databaseにはデータベース名を。
    conn=mydb.connect(
        host = 'localhost',
        port = '3306',
        user = 'docker',
        password = 'docker',
        database = 'test_database'
    )

    # コネクションが切れた時に再接続してくれるよう設定
    conn.ping(reconnect=True)

    # 接続できているかどうか確認
    print(conn.is_connected())
    
    cur = conn.cursor()
    
    # Trueと表示されれば、正常に接続できています
    sql = 'SELECT * ,ShortPoint_Kousotsu + LongPoint_Kousotsu as STAR  FROM VIEW_BINANCE_CRYPTO_INFO'
    cur.execute(sql)
    rows = cur.fetchall()
    cur.execute("DESC VIEW_BINANCE_CRYPTO_INFO")
    colName = cur.fetchall()
    cur.close()
    conn.close()

    header = [
        "計算時刻",
        "★★判断★★",
        "通貨ペア",
        "現在価格",
        "適正価格(今日)",
        "適正価格(明日)",
        "適正価格(明後日)",
        "適正価格乖離率",
        "ロングエントリ推奨価格",
        "ショートエントリ推奨価格",
        "EMA(200)",
        "EMA(100)",
        "EMA(50)",
        "EMA(200)BTC建て",
        "価格変動率",
        "BTC連動率上昇",
        "BTC連動率下落",
        "RSI(14)",
        "RSI(14)BTC建て",
        "ロング評価",
        "ショート評価",
        "小数点位置",
        "STAR"
        ]

    csvFile = 'csv/binance_crypto_info.csv'
    jsonFile = 'json/binance_crypto_info.json'

    # CSVに保存
    with open(csvFile,'w') as f:
        writer = csv.writer(f)
        l = []
        for i,col in enumerate(colName):
            if i > 0:
                l.append(col[0])

        writer.writerow(header)
        for row in rows:
            l2 = []
            for j,value in enumerate(row):
                if j > 0:
                    l2.append(value)
            writer.writerow(l2)

    csv2json(csvFile,jsonFile)

