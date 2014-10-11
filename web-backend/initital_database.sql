-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               5.5.38-0ubuntu0.14.04.1 - (Ubuntu)
-- Server OS:                    debian-linux-gnu
-- HeidiSQL Version:             8.3.0.4800
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

-- Dumping database structure for snooze
CREATE DATABASE IF NOT EXISTS `snooze` /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_bin */;
USE `snooze`;


-- Dumping structure for table snooze.charities
CREATE TABLE IF NOT EXISTS `charities` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `userid` int(10) unsigned NOT NULL,
  `charity` varchar(500) COLLATE utf8_bin NOT NULL,
  `time_added` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FK__users` (`userid`),
  CONSTRAINT `FK__users` FOREIGN KEY (`userid`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- Dumping data for table snooze.charities: ~22 rows (approximately)
/*!40000 ALTER TABLE `charities` DISABLE KEYS */;
/*!40000 ALTER TABLE `charities` ENABLE KEYS */;


-- Dumping structure for table snooze.transfers
CREATE TABLE IF NOT EXISTS `transfers` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `userid` int(10) unsigned NOT NULL,
  `charityid` int(10) unsigned NOT NULL,
  `amount` int(11) NOT NULL,
  `time_added` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_transfers_users` (`userid`),
  KEY `FK_transfers_charities` (`charityid`),
  CONSTRAINT `FK_transfers_users` FOREIGN KEY (`userid`) REFERENCES `users` (`id`),
  CONSTRAINT `FK_transfers_charities` FOREIGN KEY (`charityid`) REFERENCES `charities` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- Dumping data for table snooze.transfers: ~0 rows (approximately)
/*!40000 ALTER TABLE `transfers` DISABLE KEYS */;
/*!40000 ALTER TABLE `transfers` ENABLE KEYS */;


-- Dumping structure for table snooze.users
CREATE TABLE IF NOT EXISTS `users` (
  `id` int(10) unsigned NOT NULL,
  `email` varchar(250) COLLATE utf8_bin NOT NULL,
  `password` varchar(500) COLLATE utf8_bin NOT NULL,
  `balance` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- Dumping data for table snooze.users: ~1 rows (approximately)
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` (`id`, `email`, `password`, `balance`) VALUES
	(0, 'tysonandmat@hackzurich.ch', 'topsecret', 0);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
