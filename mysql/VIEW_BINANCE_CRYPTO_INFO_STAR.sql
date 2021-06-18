CREATE VIEW VIEW_BINANCE_CRYPTO_INFO_STAR as
select * 
from BINANCE_CRYPTO_INFO as a 
where 
    (a.LongPoint_Kousotsu  > 0 or a.ShortPoint_Kousotsu > 0)
    and a.calcTime = (
        select max(b.calcTime) from BINANCE_CRYPTO_INFO as b 
        where a.pair = b.pair 
    ) 
order by a.pair,calcTime asc