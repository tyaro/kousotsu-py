CREATE VIEW VIEW_BINANCE_CRYPTO_INFO as
select * 
from BINANCE_CRYPTO_INFO as a 
where 
    a.calcTime = (
        select max(b.calcTime) from BINANCE_CRYPTO_INFO as b 
        where a.pair = b.pair 
    ) 
order by a.pair
