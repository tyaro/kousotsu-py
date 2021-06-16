#create view VIEW_BINANCE_CRYPTO_INFO2 as (SELECT * from BINANCE_CRYPTO_INFO2 as a where calcTime = (select max(calcTime) from BINANCE_CRYPTO_INFO2 where a.calctime = b.calctime))

# データフレームで使用するカラム名の定義

# KLINES DATA 
OPEN_TIME_ = 'OpenTime'    #開始時間
CLOSE_TIME_ = 'CloseTime'  #終了時間
OPEN_ = 'Open' # 始値
CLOSE_ = 'Close'   # 終値
HIGH_  = 'High'    # 高値
LOW_   = 'Low'     # 底値
VOLUME_ = 'Volume' # 取引量
QUOTE_ASSET_VOLUME_ = 'QuoteAssetVolume'   #
NUMBER_OF_TRADES_ = 'NumberOfTrades'   #
TAKER_BUY_BASE_ASSET_VOLUME_ = 'TakerBuyBaseAssetVolume'   #
TAKER_BUY_QUOTE_ASSET_VOLUME_ = 'TakerBuyQuoteAssetVolume' #
IGNORE_ = 'Ignore' #

# 先物 TICKER DATA
LAST_PRICE_ = 'lastPrice'
# 現物 TICKER DATA
PRICE_ = 'price'

# 高卒たんメソッドで追加されるカラム名
PRICE_CHANGE_ = 'PriceChange'
GAIN_VALUE_ = 'GainValue'
PRE_GAIN_VALUE_ = 'PreGainValue'
PRE_HIGH_ = 'PreHigh'
PRE_LOW_ = 'PreLow'
PRE_OPEN_ = 'PreOpen'
PRE_CLOSE_ = 'PreClose'
OPERATOR_ = 'Operator'
KOUSOTSU_PRICE_0_ = 'kousotsu'
KOUSOTSU_PRICE_1_ = 'kousotsu1'
KOUSOTSU_PRICE_2_ = 'kousotsu2'
KOUSOTSU_PRICE_3_ = 'kousotsu3'
LONG_ENTRY_POINT_ = 'LongEntryPoint'
SHORT_ENTRY_POINT_ = 'ShortEntryPoint'

# テクニカルで追加されるカラム名
CHANGE_RATE_ = 'ChangeRate'
CHANGE_RATE_MAX_10DAYS_ = 'ChangeRateMax10days'
UP_RATE_ = 'UpRate'
DOWN_RATE_ = 'DownRate'
EMA_200_ = 'EMA200'
EMA_100_ = 'EMA100'
EMA_50_ = 'EMA50'
RSI_56_ = 'RSI56'
FRIEND_RATE_UP_ ='FriendRateUp'
FRIEND_RATE_DOWN_ ='FriendRateDown'

CALC_TIME_ = 'CalcTime'
PAIR_ = 'Pair'


# ローソク足をAPIからとってきたときの項目名定義
KLINES_COLUMNS = [
    OPEN_TIME_,
    OPEN_,
    HIGH_,
    LOW_,
    CLOSE_,
    VOLUME_,
    CLOSE_TIME_,
    QUOTE_ASSET_VOLUME_,
    NUMBER_OF_TRADES_,
    TAKER_BUY_BASE_ASSET_VOLUME_,
    TAKER_BUY_QUOTE_ASSET_VOLUME_,
    IGNORE_
    ]


# 通貨ペア：小数点位置
# 754氏追加まじ感謝
# 840氏追加感謝感激
# 923氏ありがとうございます
# 939氏本当にありがとうございました
#'''
PairList = {
    "BTCUSDT":2, 

    "1000SHIBUSDT":6,
    "1INCHUSDT":4,

    "AAVEUSDT":2,
    "ADAUSDT":4,
    "AKROUSDT":5,
    "ALGOUSDT":4,
    "ALICEUSDT":3, 
    "ALPHAUSDT":4, 
    "ANKRUSDT":5, 
    "ATOMUSDT":3, 
    "AVAXUSDT":3, 
    "AXSUSDT":3, 

    "BAKEUSDT":4,
    "BALUSDT":3,
    "BANDUSDT":4,
    "BATUSDT":4,
    "BCHUSDT":2,
    "BELUSDT":4,
    "BLZUSDT":5,
    "BNBUSDT":2, 
    "BTCBUSD":2, 
    "BTCUSDT":2, 
    "BTSUSDT":5, 
    "BTTUSDT":6, 
    "BZRXUSDT":4, 

    "CELRUSDT":5,
    "CHRUSDT":4,
    "CHZUSDT":5,
    "COMPUSDT":2,
    "COTIUSDT":5,
    "CRVUSDT":3,
    "CTKUSDT":3,
    "CVCUSDT":5,

    "DASHUSDT":2,
    "DEFIUSDT":1,
    "DENTUSDT":6,
    "DGBUSDT":5,
    "DODOUSDT":3,
    "DOGEUSDT":5,
    "DOTUSDT":3,

    "EGLDUSDT":2, 
    "ENJUSDT":4, 
    "EOSUSDT":3, 
    "ETCUSDT":3, 
    "ETHUSDT":2, 

    "FILUSDT":3, 
    "FLMUSDT":4, 
    "FTMUSDT":5,

    "GRTUSDT":5,
    "GTCUSDT":3,

    "HBARUSDT":5,
    "HNTUSDT":3,
    "HOTUSDT":6,

    "ICPUSDT":2,
    "ICXUSDT":4,
    "IOSTUSDT":6,
    "IOTAUSDT":4,

    "KAVAUSDT":4,
    "KNCUSDT":3,
    "KSMUSDT":2,

    "LINAUSDT":5,
    "LINKUSDT":3,
    "LITUSDT":3,
    "LTCUSDT":2,
    "LRCUSDT":5,
    "LUNAUSDT":3,

    "MANAUSDT":4,
    "MATICUSDT":4,
    "MKRUSDT":1,
    "MTLUSDT":4,

    "NEARUSDT":4,
    "NEOUSDT":3,
    "NKNUSDT":3,

    "OCEANUSDT":5,
    "OGNUSDT":4,
    "OMGUSDT":4,
    "ONEUSDT":5,
    "ONTUSDT":2,
    "QTUMUSDT":3,

    "REEFUSDT":6,
    "RENUSDT":5,
    "RLCUSDT":4,
    "RSRUSDT":6,
    "RUNEUSDT":3,
    "RVNUSDT":5,

    "SANDUSDT":5,
    "SCUSDT":6,
    "SFPUSDT":4,
    "SKLUSDT":5,
    "SNXUSDT":3,
    "SOLUSDT":3,
    "SRMUSDT":3,
    "STMXUSDT":5,
    "STORJUSDT":4,
    "SUSHIUSDT":3,
    "SXPUSDT":4,

    "THETAUSDT":3,
    "TOMOUSDT":4,
    "TRBUSDT":2,
    "TRXUSDT":5,

    "UNFIUSDT":3,
    "UNIUSDT":3,
    "VETUSDT":5,
    "WAVESUSDT":3,

    "XEMUSDT":4,
    "XLMUSDT":5,
    "XMRUSDT":2,
    "XRPUSDT":4,
    "XTZUSDT":3,

    "YFIIUSDT":1,
    "YFIUSDT":0,

    "ZECUSDT":2,
    "ZENUSDT":3,
    "ZILUSDT":5,
    "ZRXUSDT":4,
}
'''
# デバッグ用
# 通貨全部回したら時間かかるねん・・・
PairList = {
    "BTCUSDT":2,
    "ALICEUSDT":3, 
}
#'''

