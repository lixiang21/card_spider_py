CREATE TABLE `cards` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name_cn` varchar(255) NOT NULL DEFAULT '',
  `name_jp` varchar(255) NOT NULL DEFAULT '',
  `name_us` varchar(255) NOT NULL DEFAULT '',
  `category` varchar(128) NOT NULL DEFAULT '',
  `code` int(11) NOT NULL DEFAULT '0',
  `race` varchar(128) NOT NULL DEFAULT '',
  `property` varchar(128) NOT NULL DEFAULT '',
  `level` int(11) NOT NULL DEFAULT '0',
  `atk` int(11) NOT NULL,
  `def` int(11) NOT NULL,
  `desc` varchar(512) NOT NULL DEFAULT '',
  `status` int(11) NOT NULL DEFAULT '0',
  `url` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;