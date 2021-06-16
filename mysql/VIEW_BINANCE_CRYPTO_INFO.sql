-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- ホスト: mariadb_host
-- 生成日時: 2021 年 6 月 16 日 14:04
-- サーバのバージョン： 10.5.10-MariaDB-1:10.5.10+maria~focal
-- PHP のバージョン: 7.4.20

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

--
-- データベース: `test_database`
--

-- --------------------------------------------------------

--
-- ビュー用の構造 `view_binance_crypto_info`
--

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`%` SQL SECURITY DEFINER VIEW `view_binance_crypto_info`  AS   (select `a`.`ID` AS `ID`,`a`.`calcTime` AS `calcTime`,`a`.`judge` AS `judge`,`a`.`pair` AS `pair`,`a`.`lastPrice` AS `lastPrice`,`a`.`kousotsuPrice0` AS `kousotsuPrice0`,`a`.`kousotsuPrice1` AS `kousotsuPrice1`,`a`.`kousotsuPrice2` AS `kousotsuPrice2`,`a`.`DevRate4Price` AS `DevRate4Price`,`a`.`EntryPointLong` AS `EntryPointLong`,`a`.`EntryPointShort` AS `EntryPointShort`,`a`.`DevRate4EMA200` AS `DevRate4EMA200`,`a`.`DevRate4EMA100` AS `DevRate4EMA100`,`a`.`DevRate4EMA50` AS `DevRate4EMA50`,`a`.`DevRate4EMA200BTC` AS `DevRate4EMA200BTC`,`a`.`ChangeRate` AS `ChangeRate`,`a`.`BTCFriendRateUp` AS `BTCFriendRateUp`,`a`.`BTCFriendRateDown` AS `BTCFriendRateDown`,`a`.`RSI14` AS `RSI14`,`a`.`RSI14BTC` AS `RSI14BTC`,`a`.`LongPoint_Kousotsu` AS `LongPoint_Kousotsu`,`a`.`ShortPoint_Kousotsu` AS `ShortPoint_Kousotsu`,`a`.`point` AS `point` from `binance_crypto_info` `a` where `a`.`calcTime` = (select max(`b`.`calcTime`) from `binance_crypto_info` `b` where `a`.`pair` = `b`.`pair`))  ;
COMMIT;
