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
-- テーブルの構造 `BINANCE_CRYPTO_INFO`
--

CREATE TABLE `BINANCE_CRYPTO_INFO` (
  `ID` bigint(20) UNSIGNED NOT NULL,
  `calcTime` datetime DEFAULT NULL COMMENT '計算時刻',
  `judge` text NOT NULL,
  `pair` varchar(20) NOT NULL COMMENT '通貨ペア',
  `lastPrice` double DEFAULT NULL COMMENT '最終価格',
  `kousotsuPrice0` double DEFAULT NULL COMMENT '本日9時の適正価格',
  `kousotsuPrice1` double DEFAULT NULL COMMENT '翌日9時の適正価格',
  `kousotsuPrice2` double DEFAULT NULL COMMENT '翌々日9時の適正価格',
  `DevRate4Price` float DEFAULT NULL COMMENT '適正価格との乖離率',
  `EntryPointLong` double DEFAULT NULL COMMENT 'ロングエントリー推奨価格',
  `EntryPointShort` double DEFAULT NULL COMMENT 'ショートエントリー推奨価格',
  `DevRate4EMA200` float DEFAULT NULL COMMENT 'EMA200との乖離率',
  `DevRate4EMA100` float DEFAULT NULL COMMENT 'EMA100との乖離率',
  `DevRate4EMA50` float DEFAULT NULL COMMENT 'EMA50との乖離率',
  `DevRate4EMA200BTC` float DEFAULT NULL COMMENT 'EMA200(BTC建て)との乖離率',
  `ChangeRate` float DEFAULT NULL COMMENT 'その日の変動率',
  `BTCFriendRateUp` float DEFAULT NULL COMMENT 'BTC連動率UP側',
  `BTCFriendRateDown` float DEFAULT NULL COMMENT 'BRC連動率DOWN側',
  `RSI14` float NOT NULL COMMENT 'RSI(14)',
  `RSI14BTC` float NOT NULL COMMENT 'RSI(14)BTC建て',
  `LongPoint_Kousotsu` int(11) NOT NULL COMMENT '高卒たんアルゴリズムロングオススメポイント',
  `ShortPoint_Kousotsu` int(11) NOT NULL COMMENT '高卒たんアルゴリズムショートオススメポイント',
  `point` int(11) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- ダンプしたテーブルのインデックス
--

--
-- テーブルのインデックス `BINANCE_CRYPTO_INFO`
--
ALTER TABLE `BINANCE_CRYPTO_INFO`
  ADD PRIMARY KEY (`ID`);

--
-- ダンプしたテーブルの AUTO_INCREMENT
--

--
-- テーブルの AUTO_INCREMENT `BINANCE_CRYPTO_INFO`
--
ALTER TABLE `BINANCE_CRYPTO_INFO`
  MODIFY `ID` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;
COMMIT;
