# ************************************************************
# Sequel Pro SQL dump
# Version 3408
#
# http://www.sequelpro.com/
# http://code.google.com/p/sequel-pro/
#
# Host: 127.0.0.1 (MySQL 5.1.54-log)
# Database: wuditoo
# Generation Time: 2012-04-28 05:17:01 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table activity
# ------------------------------------------------------------

DROP TABLE IF EXISTS `activity`;

CREATE TABLE `activity` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(11) unsigned DEFAULT '0',
  `action` smallint(5) unsigned DEFAULT '0',
  `created` int(11) unsigned DEFAULT '0',
  `target_id` int(11) unsigned DEFAULT '0',
  `context_id` int(11) unsigned DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `type` (`action`),
  KEY `created` (`created`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table blog
# ------------------------------------------------------------

DROP TABLE IF EXISTS `blog`;

CREATE TABLE `blog` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `title` varchar(100) DEFAULT NULL,
  `content` text,
  `created` int(11) DEFAULT NULL,
  `updated` int(11) DEFAULT NULL,
  `status` tinyint(4) DEFAULT '0',
  `comment_count` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table blog_comment
# ------------------------------------------------------------

DROP TABLE IF EXISTS `blog_comment`;

CREATE TABLE `blog_comment` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `blog_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `content` text,
  `created` int(11) DEFAULT NULL,
  `updated` int(11) DEFAULT NULL,
  `status` tinyint(4) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table followship
# ------------------------------------------------------------

DROP TABLE IF EXISTS `followship`;

CREATE TABLE `followship` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `follower_user_id` int(11) unsigned DEFAULT NULL,
  `followed_user_id` int(11) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `follower_user_id` (`follower_user_id`),
  KEY `followed_user_id` (`followed_user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table invite_key
# ------------------------------------------------------------

DROP TABLE IF EXISTS `invite_key`;

CREATE TABLE `invite_key` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(11) unsigned DEFAULT NULL,
  `hash` char(16) DEFAULT NULL,
  `used` tinyint(4) DEFAULT '0',
  `dest_user_id` int(11) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `hash` (`hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table notification
# ------------------------------------------------------------

DROP TABLE IF EXISTS `notification`;

CREATE TABLE `notification` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `operator_id` int(11) unsigned DEFAULT NULL,
  `receiver_id` int(11) unsigned DEFAULT NULL,
  `created` int(11) unsigned DEFAULT NULL,
  `target_id` int(11) unsigned DEFAULT NULL,
  `context_id` int(11) unsigned DEFAULT NULL,
  `is_new` tinyint(4) DEFAULT NULL,
  `action` smallint(5) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `receiver_id` (`receiver_id`),
  KEY `action` (`action`),
  KEY `operator_id` (`operator_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table photo
# ------------------------------------------------------------

DROP TABLE IF EXISTS `photo`;

CREATE TABLE `photo` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(11) unsigned DEFAULT NULL,
  `hash` varchar(40) DEFAULT NULL,
  `title` varchar(150) DEFAULT NULL,
  `content` varchar(4096) DEFAULT '',
  `created` int(11) DEFAULT NULL,
  `updated` int(11) DEFAULT NULL,
  `status` tinyint(11) DEFAULT '-1',
  `views_count` mediumint(11) unsigned DEFAULT '0',
  `likes_count` smallint(5) unsigned DEFAULT '0',
  `comments_count` smallint(5) unsigned DEFAULT '0',
  `karma` float(11,4) DEFAULT '0.0000',
  `width` int(11) DEFAULT NULL,
  `height` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `karma` (`karma`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table photo_comment
# ------------------------------------------------------------

DROP TABLE IF EXISTS `photo_comment`;

CREATE TABLE `photo_comment` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(11) unsigned DEFAULT NULL,
  `photo_id` int(11) unsigned DEFAULT NULL,
  `content` varchar(1024) DEFAULT NULL,
  `created` int(11) DEFAULT NULL,
  `updated` int(11) DEFAULT NULL,
  `status` tinyint(4) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table photo_exif
# ------------------------------------------------------------

DROP TABLE IF EXISTS `photo_exif`;

CREATE TABLE `photo_exif` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `photo_id` int(11) DEFAULT NULL,
  `key` varchar(50) DEFAULT NULL,
  `value` varchar(1024) DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `picture_id` (`photo_id`),
  KEY `key` (`key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table photo_like
# ------------------------------------------------------------

DROP TABLE IF EXISTS `photo_like`;

CREATE TABLE `photo_like` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(11) unsigned DEFAULT NULL,
  `photo_id` int(11) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `photo_id` (`photo_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table photo_tag
# ------------------------------------------------------------

DROP TABLE IF EXISTS `photo_tag`;

CREATE TABLE `photo_tag` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `photo_id` int(11) DEFAULT NULL,
  `tag` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `tag_name` (`tag`),
  KEY `photo_id` (`photo_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table profile
# ------------------------------------------------------------

DROP TABLE IF EXISTS `profile`;

CREATE TABLE `profile` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `country` tinyint(4) DEFAULT NULL,
  `city` tinyint(4) DEFAULT NULL,
  `town` tinyint(4) DEFAULT NULL,
  `loc` tinyint(4) DEFAULT NULL,
  `bio` varchar(1024) DEFAULT NULL,
  `link_weibo` varchar(50) DEFAULT NULL,
  `link_qq` varchar(50) DEFAULT NULL,
  `link_douban` varchar(70) DEFAULT NULL,
  `link_flickr` varchar(70) DEFAULT NULL,
  `link_blog` varchar(100) DEFAULT NULL,
  `camera` varchar(100) DEFAULT NULL,
  `lens` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table user
# ------------------------------------------------------------

DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `email` varchar(100) DEFAULT NULL,
  `username` varchar(50) DEFAULT NULL,
  `fullname` varchar(50) DEFAULT NULL,
  `password` varchar(40) DEFAULT NULL,
  `created` int(11) DEFAULT NULL,
  `status` int(11) DEFAULT '0',
  `avatar_hash` varchar(32) DEFAULT NULL,
  `level` tinyint(3) DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table user_meta
# ------------------------------------------------------------

DROP TABLE IF EXISTS `user_meta`;

CREATE TABLE `user_meta` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `key` varchar(50) DEFAULT NULL,
  `value` varchar(1024) DEFAULT '',
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id_key` (`user_id`,`key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;




/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
