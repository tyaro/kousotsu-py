import pandas as pd

from Technical import *
from const import *


# 高卒たんアルゴリズム
class HighSchool():
    
    # BinanceAPIクラス作ったのでそのうち書き直し
    def __init__(self):
        pass

    # 適正価格算出(日足ベース) 
    # ※ absは絶対値だお
    # 
    # 3日前の高値 ＜ 2日前の高値 ＆ 3日前の底値 ＜ 2日前の底値
    # 　-> 適正価格 ＝ 2日前の始値 ＋ abs(3日前の始値-3日前の終値) * 0.3 
    #
    # 3日前の高値 ＞ 2日前の高値 ＆ 3日前の底値 ＞ 2日前の底値
    # 　-> 適正価格 ＝ 2日前の始値 - abs(3日前の始値-3日前の終値) * 0.3
    # 
    # はらみの場合(腹減ってきたな)
    #　　2日前の始値より現在価格が上
    # 　　　-> 適正価格 ＝ 2日前の始値 ＋ abs(3日前の始値-3日前の終値) * 0.3 
    #
    #    2日前の始値より現在価格が下
    # 　　　-> 適正価格 ＝ 2日前の始値 - abs(3日前の始値-3日前の終値) * 0.3
    #
    # df(DataFrame):ローソク足データ
    @staticmethod
    def CalcReasonablePriceDayBase(df,ticker):
        # 1日の変動量計算
        df[PRICE_CHANGE_] = (df[CLOSE_] - df[OPEN_])
        # 足し引きする値を計算
        df[GAIN_VALUE_] = df[PRICE_CHANGE_] * 0.3
        # vol列を一つ後ろにずらしたものをpreVol列に入れる(前日の変動量) ※ずらすと最初のデータは無くなる(NAN)ので0埋めしておく
        df[PRE_GAIN_VALUE_] = df[GAIN_VALUE_].shift(1).fillna(0)
        # high列を一つ後ろにずらしたものをpreHigh列に入れる(前日の高値)
        df[PRE_HIGH_] = df[HIGH_].shift(1)
        # low列を一つ後ろにずらしたものをpreLow列に入れる(前日の安値)
        df[PRE_LOW_] = df[LOW_].shift(1)
        # open列を一つ後ろにずらしたものをpreOpen列に入れる(前日の始値)
        df[PRE_OPEN_] = df[OPEN_].shift(1)
        # close列を一つ後ろにずらしたものをpreClose列に入れる(前日の終値)
        df[PRE_CLOSE_] = df[CLOSE_].shift(1)

        def kousotsu(x):
            # 3日前の高値＞2日前の高値 ＆ 3日前の底値＞2日前の底値
            if x.PreHigh > x.High and x.PreLow > x.Low:
                return -1
            # 3日前の高値＜2日前の高値 ＆ 3日前の底値＜2日前の底値
            if x.PreHigh < x.High and x.PreLow < x.Low:
                return 1
            # ハラミ線の場合
            else:
                # 現在値が2日前の始値の上にある場合は足し算
                if ticker >= x.Open:
                    return 1
                # 現在値が2日前の始値の下にある場合は引き算
                else:
                    return -1

        # 和とするか差とするか演算 未だにラムダ式よくわからんちん
        df[OPERATOR_] = df.apply(lambda x:kousotsu(x),axis=1)
 
        # 適正価格演算
        df[KOUSOTSU_PRICE_0_] = df[OPEN_] + (df[PRE_GAIN_VALUE_].abs() * df[OPERATOR_])

        # 2日前の行にデータが入っているのでデータをずらす
        df[KOUSOTSU_PRICE_1_] = df[KOUSOTSU_PRICE_0_].shift(2) # 今日の朝9時の適正価格
        df[KOUSOTSU_PRICE_2_] = df[KOUSOTSU_PRICE_0_].shift(1) # 明日の朝9時の適正価格
        df[KOUSOTSU_PRICE_3_] = df[KOUSOTSU_PRICE_0_]          # 明後日の朝9時の適正価格

        #print(df.loc[:,['openTime','close','preClose','vol','preVol','operator','kousotsu']])

        return df

    # ロングショートエントリーポイント計算
    def CalcEntryPoint(df):
        # 変動率計算(終値/始値＊100)
        df = Technical.CalcChangeRate(df,CHANGE_RATE_)

        # 7日間の最大変動計算(絶対値)
        df = Technical.CalcMaxChangeRate10(df,CHANGE_RATE_,CHANGE_RATE_MAX_10DAYS_)

        # ロングエントリーポイント算出 (1 - 7日間の最大変動率/100)✕適正価格
        df[LONG_ENTRY_POINT_] = (1 - df[CHANGE_RATE_MAX_10DAYS_]/100)*df[KOUSOTSU_PRICE_1_]
        # ショートエントリーポイント算出 (1 - 7日間の最大変動率/100)✕適正価格
        df[SHORT_ENTRY_POINT_] = (1 + df[CHANGE_RATE_MAX_10DAYS_]/100)*df[KOUSOTSU_PRICE_1_]
        
        return df

    # 735氏に感謝
    '''
    735 承認済み名無しさん (ﾜｯﾁｮｲ 8530-Maj3)[sage] 2021/06/09(水) 13:36:19.19 ID:ArsdNVr20
    現在価格＞適正価格 かつ200日MA以下　→赤色　※ショート向け  
    現在価格＜適正価格 かつ200日MA以上　→緑色　※ロング向け
    みたいな色分けが出来ると、さらに使いやすくなりそうですね。
    '''
    # ジャッジメントですの
    @staticmethod
    def JudgementDesno(ticker,entryS,entryL,ema200,ema100,ema50,ema200btc):
        s = " "
        spoint = 0  # ショート狙い評価値
        lpoint = 0  # ロング狙い評価値
        # 現在値がショートエントリーポイントより上ならばショート
        if ticker > entryS:
            spoint = 1
            # EMA200 を 現在値が下回っている且つBTC建てのEMA200も下回っているなら★追加
            if 0 > ema200 and  0 > ema200btc:
                spoint = 2
                # EMA100 を 現在値が下回っているなら★追加
                if 0 > ema100:
                    spoint += 1
                # EMA50 を 現在値が下回っているなら★追加
                if 0 > ema50:
                    spoint += 1


        # 現在値がロングエントリーポイントより下ならばロング
        if ticker < entryL:
            lpoint = 1
            # EMA200 を 現在値が上回っている且つBTC建てのEMA200も上回っているなら★追加
            if 0 < ema200 and 0 < ema200btc:
                lpoint = 2
                # EMA100 を 現在値が上回っているなら★追加
                if 0 < ema100:
                    lpoint += 1
                # EMA50 を 現在値が上回っているなら★追加
                if 0 < ema50:
                    lpoint += 1
        
        # 評価ポイント表示用
        if spoint > 0:
            s = "S"
        elif lpoint > 0:
            s = "L"
        else:
            s = ""

        return s,spoint,lpoint

    # ジャッジメントですの
    @staticmethod
    def JudgementDesno2(ticker,entryS,entryL,rsi56):
        s = " "
        spoint = 0  # ショート狙い評価値
        lpoint = 0  # ロング狙い評価値
        s = " "
        spoint = 0  # ショート狙い評価値
        lpoint = 0  # ロング狙い評価値
        # 現在値がショートエントリーポイントより上ならばショート
        if ticker > entryS:
            spoint = 1
            # RSI60より下
            if rsi56 < 60:
                spoint = 2

        # 現在値がロングエントリーポイントより下ならばロング
        if ticker < entryL:
            lpoint = 1
            # RSI40より上
            if rsi56 > 40:
                lpoint = 2
        
        # 評価ポイント表示用
        if spoint > 0:
            s = "S"
        elif lpoint > 0:
            s = "L"
        else:
            s = ""

        return s,spoint,lpoint

