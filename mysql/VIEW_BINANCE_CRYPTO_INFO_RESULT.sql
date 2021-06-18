CREATE VIEW VIEW_BINANCE_CRYPTO_INFO_RESULT as
select * 
from BINANCE_CRYPTO_INFO as a 
where a.pair = (
        select distinct b.pair from BINANCE_CRYPTO_INFO b 
        where a.pair = b.pair 
        and date_format(curdate(),'%Y-%m-%d 09:00:00') < b.calcTime 
        and (b.LongPoint_Kousotsu  > 0 or b.ShortPoint_Kousotsu > 0)
    ) 
and date_format(curdate(),'%Y-%m-%d 09:00:00') < a.calcTime 
order by a.pair,calcTime asc