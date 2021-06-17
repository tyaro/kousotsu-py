import datetime
import requests
import json
import time
import pandas as pd
import numpy as np
import math
import mysql.connector as mydb

from const import *
from BinanceAPI import *
from Technical import *
from HighSchool import *


class UtilFunc:
    # 乖離率計算
    # base:基準
    # value:評価対象
    @staticmethod
    def DaviationRate(base,value):
        value = round((value/base) * 100 - 100,1)
        return value


# BTCとの連動率を出すためにBTCの24時間の上昇分のEMAと下落分のEMAをDataFrameに負荷する
# 時間足ベースのDataFrameデータを使用
def GetBTCHKlinesData():
    # BTCの1時間ローソク足取得
    df = BinanceAPI.GetKlinesF("BTCUSDT",1000,'1h')

    # BTC24時間の時間当たりの上昇率/下落率 を計算する為のデータ(EMA使用)
    df = Technical.CalcUpDownRate(df,24,UP_RATE_,DOWN_RATE_)
    #df = Technical.CalcRSI(df,56,'RSI56')
    return df

# 高卒たんめそっど
# ・適正価格計算
# ・ロングとショートのエントリー価格計算
# 上記をデータフレームに追加して返す
def KousotsutanMethod(df,ticker):
    # 高卒たん理論による適正価格算出
    df = HighSchool.CalcReasonablePriceDayBase(df,ticker)

    # 高卒たん理論によるエントリーポイントを算出
    df = HighSchool.CalcEntryPoint(df)

    return df

# 現在価格と計算に使用するローソク足データをデータフレームに入れて返す
# lastPrice:現在価格
# lastPriceBTC:現在価格(BTC建て)
# dfDays: 1日ローソク足データ
# dfHours: 1時間ローソク足データ
# dfDaysBTC: 1日ビットコ建てローソク足データ
def GetBinanceData(pair):
    # BTC建てのシンボル名取得
    btcPair = pair.replace('USDT','BTC')

    #◆ 現在価格
    lastPrice = BinanceAPI.getTickerF(pair)
    #◆　BTC建て現在値
    lastPriceBTC = BinanceAPI.getTickerS(btcPair)

    #◆ 日足ローソクデータ取得    
    dfDays = BinanceAPI.GetKlinesF(pair,1500,'1d')        
    #◆ 時間足ローソクデータ取得    
    dfHours = BinanceAPI.GetKlinesF(pair,1000,'1h')

    # BTC建てデータ調査

    #◆ 現物板から日足ローソク足データ取得
    dfDaysBTC = BinanceAPI.GetKlinesS(btcPair,1500,'1d')
    # 現物板から時間足ローソク足データ取得
    dfHoursBTC = BinanceAPI.GetKlinesS(btcPair,1500,'1h')

    # 分足ローソクデータ取得    
    #dfMinutes = BinanceAPI.GetKlinesF(pair,1000,'1m')

    #print(df.loc[:,['vol','preVol','operator','kousotsu']])

    return lastPrice,lastPriceBTC,dfDays,dfHours,dfDaysBTC,dfHoursBTC


# 各種EMAを取得
# EMA(200)
# EMA(100)
# EMA(50)
# EMA(200) BTC建て
def GetEMA(df,dfBTC):
    # EMA(200)
    df = Technical.CalcEMA(df,200,EMA_200_)
    # EMA(100)
    df = Technical.CalcEMA(df,100,EMA_100_)
    # EMA(50)
    df = Technical.CalcEMA(df,50,EMA_50_)
    # EMA(200) ※BTC建て
    dfBTC = Technical.CalcEMA(dfBTC,200,EMA_200_)

    return df,dfBTC

# 4時間足のRSI(14)を計算
# ※1時間足を使用しているので疑似値
# USDT建てとBTC建て
def GetRSI(df,dfBTC):
    # RSI(14) 
    df = Technical.CalcRSI(df,56,RSI_56_)
    # RSI(14) ※BTC建て
    dfBTC = Technical.CalcRSI(dfBTC,56,RSI_56_)

    return df,dfBTC

# BTCとの連動率を計算(24時間分) EMA使用
# BTCデータフレームには既にUpRate DownRateの計算結果が入っているものとする
def GetFriendRate(df,dfBTC):
    df = Technical.CalcUpDownRate(df,24,UP_RATE_,DOWN_RATE_)
    df = Technical.CalcBTCFriendRate(dfBTC,df,UP_RATE_,DOWN_RATE_,FRIEND_RATE_UP_,FRIEND_RATE_DOWN_)
    return df

def main():
    
    conn = mydb.connect(
        host = 'mariadb_host',
        port = '3306',
        user = 'docker',
        password = 'docker',
        database = 'test_database'
    )
    cur = conn.cursor()

    dfBTCKlinesHour = GetBTCHKlinesData()

    #counter = 0

    # 通貨ペアでループ
    for pair in PairList.keys():

        dictCrypt = {}

        # 日足・時間足・日足(BTC建て)・時間足(BTC建て)取得
        lastPrice,lastPriceBTC,dfDays,dfHours,dfDaysBTC,dfHoursBTC = GetBinanceData(pair)

        # 高卒たんメソッド
        dfDays = KousotsutanMethod(dfDays,lastPrice)

        # BTC連動率計算
        dfHours = GetFriendRate(dfHours,dfBTCKlinesHour)

        # EMA計算
        dfDays,dfDaysBTC = GetEMA(dfDays,dfDaysBTC)

        # RSI(14)を計算
        #dfHours,dfHoursBTC = GetRSI(dfHours,dfHoursBTC)

        
        # 小数点位置
        point = PairList[pair]

        # 適正価格(9時更新)
        ReasonablePrice0 = round(dfDays.iloc[-1][KOUSOTSU_PRICE_1_],point) # 小数点丸め
        # 適正価格(翌日9時〜)
        ReasonablePrice1 = round(dfDays.iloc[-1][KOUSOTSU_PRICE_2_],point) # 小数点丸め
        # 適正価格(翌々日9時〜)
        ReasonablePrice2 = round(dfDays.iloc[-1][KOUSOTSU_PRICE_3_],point) # 小数点丸め

        # 適正価格との乖離率
        DevRate4RPrice = UtilFunc.DaviationRate(ReasonablePrice0,lastPrice)

        # ロングエントリー推奨価格
        EntryPointLong = round(dfDays.iloc[-1][LONG_ENTRY_POINT_],point)
        # ショートエントリー推奨価格
        EntryPointShort = round(dfDays.iloc[-1][SHORT_ENTRY_POINT_],point)

        # EMA200との乖離率
        DevRate4EMA200 = UtilFunc.DaviationRate(dfDays.iloc[-1][EMA_200_],lastPrice)
        # EMA100との乖離率
        DevRate4EMA100 = UtilFunc.DaviationRate(dfDays.iloc[-1][EMA_100_],lastPrice)
        # EMA50との乖離率
        DevRate4EMA50 = UtilFunc.DaviationRate(dfDays.iloc[-1][EMA_50_],lastPrice)

        # EMA200(BTC)との乖離率
        DevRate4EMA200BTC = UtilFunc.DaviationRate(dfDaysBTC.iloc[-1][EMA_200_],lastPriceBTC)

        # 現在の変動率
        ChangeRate = round(dfDays.iloc[-1][CHANGE_RATE_],2)

        # BTC連動率(24時間)
        BTCFriendRateUp = round(dfHours.iloc[-1][FRIEND_RATE_UP_],2)
        BTCFriendRateDown = round(dfHours.iloc[-1][FRIEND_RATE_DOWN_],2)

        # RSI(14) 4時間のRSI(14)が望ましいが1時間足ベースのRSI(56)で代用
        RSI14 = round(Technical.CalcRSI14Based4Hours(dfHours),1)
        RSI14BTC = round(Technical.CalcRSI14Based4Hours(dfHoursBTC),1)

        # ジャッジメントですの
        Judge,spoint,lpoint = HighSchool.JudgementDesno2(lastPrice,EntryPointShort,EntryPointLong,RSI14)

        l = [
             Judge.ljust(14),
             pair.ljust(14),  # 通貨ペア
             str(lastPrice).ljust(10), # 現在の価格
             str(ReasonablePrice0).ljust(10),# 適正価格
             str(ReasonablePrice1).ljust(10),# 適正価格
             str(ReasonablePrice2).ljust(10),# 適正価格
             (str(DevRate4RPrice)+'%').ljust(10), # 適正価格との乖離率
             str(EntryPointLong).ljust(10),# ロングエントリー推奨価格
             str(EntryPointShort).ljust(10), # ショートエントリー推奨価格
             (str(DevRate4EMA200)+'%').ljust(10),
             (str(DevRate4EMA100)+'%').ljust(10),
             (str(DevRate4EMA50)+'%').ljust(10), # EMA200
             (str(DevRate4EMA200BTC)+'%').ljust(10), # EMA200_BTC
             (str(ChangeRate)+'%').ljust(10),    # 価格変動率
             (str(BTCFriendRateUp)+'%').ljust(10),   # BTC連動率
             (str(BTCFriendRateDown)+'%').ljust(10), # BTC連動率
             (str(RSI14)).ljust(4)+"/"+(str(RSI14BTC).ljust(4)), # RSI(14)
            ]
        
        cryptoInfoData = {}
        time_stamp = time.strftime('%Y-%m-%d %H:%M:%S')

        cryptoInfoData['calcTime'] = time_stamp  
        cryptoInfoData['pair'] = pair  
        cryptoInfoData['lastPrice'] = lastPrice
        cryptoInfoData['kousotsuPrice0'] = ReasonablePrice0
        cryptoInfoData['kousotsuPrice1'] = ReasonablePrice1  
        cryptoInfoData['kousotsuPrice2'] = ReasonablePrice2
        cryptoInfoData['DevRate4Price'] = DevRate4RPrice
        cryptoInfoData['EntryPointLong'] = EntryPointLong
        cryptoInfoData['EntryPointShort'] = EntryPointShort
        cryptoInfoData['DevRate4EMA200'] = DevRate4EMA200
        cryptoInfoData['DevRate4EMA100'] = DevRate4EMA100
        cryptoInfoData['DevRate4EMA50'] = DevRate4EMA50
        cryptoInfoData['DevRate4EMA200BTC'] = DevRate4EMA200BTC
        cryptoInfoData['ChangeRate'] = ChangeRate
        cryptoInfoData['BTCFriendRateUp'] = BTCFriendRateUp
        cryptoInfoData['BTCFriendRateDown'] = BTCFriendRateDown
        cryptoInfoData['RSI14'] = RSI14
        cryptoInfoData['RSI14BTC'] = RSI14BTC
        cryptoInfoData['LongPoint_Kousotsu'] = lpoint
        cryptoInfoData['ShortPoint_Kousotsu'] = spoint
        cryptoInfoData['point'] = point
        cryptoInfoData['judge'] = Judge

        conn.ping(reconnect=True)

        # 接続できているかどうか確認
        print(conn.is_connected())

        s = CreateSQLCryptoInfoData(cryptoInfoData)
        cur.execute(s)
        conn.commit()

        DispData(l)

        time.sleep(2)

    cur.close()
    conn.close()


def CreateSQLCryptoInfoData(d):
    s = 'INSERT INTO BINANCE_CRYPTO_INFO('
    for key in d.keys():
        s += key + ','
    s = s[:-1] + ') VALUES ('
    for v in d.values():
        if type(v) is str:
            s += '"' + v + '"' + ','
        elif math.isnan(v):
            s += 'null' + ','
        else:
            s += str(v) + ','
    s = s[:-1] + ')'



    return s

def DispHeader(l):
    s = ""
    for value in l:
        if type(value) is str:
            s += value
        else:
            s += str(value)
    print(s)

def DispData(l):
    s = " "
    for value in l:
        if type(value) is str:
            s += value
        else:
            s += str(value)
    print(s)

if __name__ == "__main__":

    print("*************************************************************")
    print("* 高卒たん適正価格算出アルゴリズム")
    print("* version 6.0.0 Release版")
    print("* 2021/06/15")
    print("*")
    print("* from 高卒億トレプロのスレ Part.7")
    print("* https://fate.5ch.net/test/read.cgi/cryptocoin/1622951653/")
    print("*")
    print("* 高卒8億3千万デイトレーダーのプロ ◆SpJFlRrMwI 様に感謝を")
    print("*")
    print("* ★ライセンス")
    print("*  ・高卒たんに感謝するスレ民のみ使用可")
    print("*　・損失については誰も責任を負わないものとする")
    print("*　・改造改変は自由とするが、商用利用する場合はスレ民に十分なお布施を払い許可をとったら可")
    print("*　・高卒たんの一存でライセンスは改定される場合がある")
    print("*　")
    print("*************************************************************")
    print("")

    now = datetime.datetime.now() + datetime.timedelta(hours=9)
    print(now,"に計算")

    main()