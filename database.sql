-- MySQL dump 10.13  Distrib 5.7.17, for Linux (x86_64)
--
-- Host: localhost    Database: app_adimsayar
-- ------------------------------------------------------
-- Server version	5.7.17-0ubuntu0.16.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `ad_ad`
--

DROP TABLE IF EXISTS `ad_ad`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ad_ad` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) DEFAULT NULL,
  `btype` int(10) unsigned NOT NULL,
  `text` longtext,
  `locale` varchar(8) NOT NULL,
  `date_time` datetime NOT NULL,
  `impression` int(10) unsigned NOT NULL,
  `click` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ad_ad_tags`
--

DROP TABLE IF EXISTS `ad_ad_tags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ad_ad_tags` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ad_id` int(11) NOT NULL,
  `tag_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ad_id` (`ad_id`,`tag_id`),
  KEY `ad_ad_tags_51c59e2f` (`ad_id`),
  KEY `ad_ad_tags_3747b463` (`tag_id`)
) ENGINE=MyISAM AUTO_INCREMENT=85 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ad_tag`
--

DROP TABLE IF EXISTS `ad_tag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ad_tag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  `cnt` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_425ae3c4` (`group_id`),
  KEY `auth_group_permissions_1e014c8f` (`permission_id`)
) ENGINE=MyISAM AUTO_INCREMENT=171 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_message`
--

DROP TABLE IF EXISTS `auth_message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_message` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `message` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `auth_message_403f60f` (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=67693 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  KEY `auth_permission_1bb8f392` (`content_type_id`)
) ENGINE=MyISAM AUTO_INCREMENT=205 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(75) NOT NULL,
  `password` varchar(128) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `last_login` datetime NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=MyISAM AUTO_INCREMENT=222397 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `auth_user_groups_403f60f` (`user_id`),
  KEY `auth_user_groups_425ae3c4` (`group_id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `auth_user_user_permissions_403f60f` (`user_id`),
  KEY `auth_user_user_permissions_1e014c8f` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `badges_badge`
--

DROP TABLE IF EXISTS `badges_badge`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `badges_badge` (
  `id` varchar(255) NOT NULL,
  `level` varchar(1) NOT NULL,
  `icon` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `badges_badgetouser`
--

DROP TABLE IF EXISTS `badges_badgetouser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `badges_badgetouser` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `badge_id` varchar(255) NOT NULL,
  `user_id` int(11) NOT NULL,
  `created` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `badges_badgetouser_7f24a4dc` (`badge_id`),
  KEY `badges_badgetouser_403f60f` (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=67707 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `body_info_bodyinfo`
--

DROP TABLE IF EXISTS `body_info_bodyinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `body_info_bodyinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `gender` varchar(255) NOT NULL,
  `date_time` datetime NOT NULL,
  `age` int(10) unsigned NOT NULL,
  `weight` int(10) unsigned NOT NULL,
  `weight_float` double DEFAULT NULL,
  `weight_goal` double DEFAULT NULL,
  `weight_goal_duration` int(10) unsigned DEFAULT NULL,
  `height` int(10) unsigned NOT NULL,
  `lifestyle` varchar(3) DEFAULT NULL,
  `bmr` decimal(5,2) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `body_info_bodyinfo_403f60f` (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=14939 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `contact_contact`
--

DROP TABLE IF EXISTS `contact_contact`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `contact_contact` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `from_email` varchar(75) NOT NULL,
  `system_email` varchar(75) NOT NULL,
  `subject` varchar(200) NOT NULL,
  `message` varchar(1000) NOT NULL,
  `auto_replied` tinyint(1) NOT NULL,
  `answered` tinyint(1) NOT NULL,
  `send_error` tinyint(1) NOT NULL,
  `error_email` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=638 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `content_actionmsg`
--

DROP TABLE IF EXISTS `content_actionmsg`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `content_actionmsg` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `odemeid` varchar(72) NOT NULL,
  `tutar` varchar(72) NOT NULL,
  `date_time` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `content_content`
--

DROP TABLE IF EXISTS `content_content`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `content_content` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(72) NOT NULL,
  `page` varchar(72) NOT NULL,
  `text` longtext,
  `date_time` datetime NOT NULL,
  `locale` varchar(8) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=116 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `content_news`
--

DROP TABLE IF EXISTS `content_news`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `content_news` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `text` longtext,
  `name` varchar(255) NOT NULL,
  `date_time` datetime NOT NULL,
  `locale` varchar(8) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `content_tweet`
--

DROP TABLE IF EXISTS `content_tweet`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `content_tweet` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `message` varchar(140) DEFAULT NULL,
  `when` int(10) unsigned NOT NULL,
  `time` time DEFAULT NULL,
  `dom` int(10) unsigned DEFAULT NULL,
  `mon` int(10) unsigned DEFAULT NULL,
  `dow` int(10) unsigned DEFAULT NULL,
  `locale` varchar(8) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=140 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `core_city`
--

DROP TABLE IF EXISTS `core_city`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `core_city` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `country_id` int(11) NOT NULL,
  `name` varchar(64) NOT NULL,
  `cnt` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `core_city_534dd89` (`country_id`)
) ENGINE=MyISAM AUTO_INCREMENT=9275 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `core_country`
--

DROP TABLE IF EXISTS `core_country`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `core_country` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `shortcode` varchar(16) NOT NULL,
  `cnt` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=113 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `core_isp`
--

DROP TABLE IF EXISTS `core_isp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `core_isp` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  `cnt` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=646 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `core_location`
--

DROP TABLE IF EXISTS `core_location`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `core_location` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `country_id` int(11) NOT NULL,
  `city_id` int(11) NOT NULL,
  `lon` varchar(32) NOT NULL,
  `lan` varchar(32) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `core_location_534dd89` (`country_id`),
  KEY `core_location_586a73b5` (`city_id`)
) ENGINE=MyISAM AUTO_INCREMENT=1226 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `core_profile`
--

DROP TABLE IF EXISTS `core_profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `core_profile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `date` datetime NOT NULL,
  `country` varchar(2) DEFAULT NULL,
  `latitude` decimal(10,6) DEFAULT NULL,
  `longitude` decimal(10,6) DEFAULT NULL,
  `location` varchar(255) NOT NULL,
  `firstname` varchar(255) NOT NULL,
  `surname` varchar(255) NOT NULL,
  `gender` varchar(255) NOT NULL,
  `birthdate` date DEFAULT NULL,
  `height` int(11) DEFAULT NULL,
  `weight` int(11) DEFAULT NULL,
  `age` int(11) DEFAULT NULL,
  `lifestyle` varchar(3) DEFAULT NULL,
  `total_step` bigint(20) NOT NULL,
  `send_mail` tinyint(1) NOT NULL,
  `ip_addr` varchar(32) DEFAULT 'null',
  `user_location_id` int(11) DEFAULT NULL,
  `isp_id` int(11) DEFAULT NULL,
  `overload_site` int(11) DEFAULT '1',
  `diet_id` int(11) DEFAULT NULL,
  `nickname_is_set` tinyint(1) NOT NULL DEFAULT '0',
  `send_mail_weekly` tinyint(1) NOT NULL DEFAULT '1',
  `send_mail_weight_update` tinyint(1) NOT NULL DEFAULT '1',
  `send_mail_won_badge` tinyint(1) NOT NULL DEFAULT '1',
  `send_mail_messages` tinyint(1) NOT NULL DEFAULT '1',
  `send_mail_diet` tinyint(1) NOT NULL DEFAULT '1',
  `send_mail_news` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=219934 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `core_profile_tags`
--

DROP TABLE IF EXISTS `core_profile_tags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `core_profile_tags` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `profile_id` int(11) NOT NULL,
  `tag_id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `device2_device2`
--

DROP TABLE IF EXISTS `device2_device2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `device2_device2` (
  `device_id` varchar(255) NOT NULL,
  `date_registered` datetime NOT NULL,
  `swversion` varchar(32) DEFAULT NULL,
  `appversion` varchar(8) DEFAULT NULL,
  `serial_number` varchar(64) DEFAULT NULL,
  `imei` varchar(32) DEFAULT NULL,
  `sensivity` int(10) unsigned NOT NULL,
  `manufacturer_id` int(11) DEFAULT NULL,
  `model_id` int(11) DEFAULT NULL,
  `product_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`device_id`),
  KEY `device2_device2_4ac7f441` (`manufacturer_id`),
  KEY `device2_device2_500cf89a` (`model_id`),
  KEY `device2_device2_44bdf3ee` (`product_id`),
  KEY `device2_device2_403f60f` (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `device2_manufacturer`
--

DROP TABLE IF EXISTS `device2_manufacturer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `device2_manufacturer` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `cnt` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=139 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `device2_model`
--

DROP TABLE IF EXISTS `device2_model`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `device2_model` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `manufacturer_id` int(11) DEFAULT NULL,
  `cnt` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `device2_model_4ac7f441` (`manufacturer_id`)
) ENGINE=MyISAM AUTO_INCREMENT=1296 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `device2_product`
--

DROP TABLE IF EXISTS `device2_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `device2_product` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `cnt` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=1529 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `diet_atom`
--

DROP TABLE IF EXISTS `diet_atom`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `diet_atom` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `diet_id` int(11) NOT NULL,
  `when` int(10) unsigned NOT NULL,
  `time` time DEFAULT NULL,
  `dom` int(10) unsigned DEFAULT NULL,
  `mon` int(10) unsigned DEFAULT NULL,
  `dow` int(10) unsigned DEFAULT NULL,
  `message` longtext NOT NULL,
  `url` varchar(200) DEFAULT NULL,
  `sound` int(10) unsigned DEFAULT NULL,
  `done` tinyint(1) NOT NULL,
  `points` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `diet_atom_5f4f896a` (`diet_id`)
) ENGINE=MyISAM AUTO_INCREMENT=129 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `diet_diet`
--

DROP TABLE IF EXISTS `diet_diet`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `diet_diet` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `diet_definition_id` int(11) NOT NULL,
  `start_date` datetime DEFAULT NULL,
  `finish_date` datetime DEFAULT NULL,
  `initial_weight` int(10) unsigned DEFAULT NULL,
  `current_weight` int(10) unsigned DEFAULT NULL,
  `target_weight` int(10) unsigned DEFAULT NULL,
  `datetime` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `diet_diet_403f60f` (`user_id`),
  KEY `diet_diet_3f114c0b` (`diet_definition_id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `diet_dietdefinition`
--

DROP TABLE IF EXISTS `diet_dietdefinition`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `diet_dietdefinition` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  `desc` longtext NOT NULL,
  `group` int(10) unsigned NOT NULL,
  `rating` int(10) unsigned NOT NULL,
  `diet_rate` int(11) DEFAULT NULL,
  `rate_count` int(11) DEFAULT NULL,
  `price` varchar(8) NOT NULL,
  `coupons` varchar(128) NOT NULL,
  `datetime` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_403f60f` (`user_id`),
  KEY `django_admin_log_1bb8f392` (`content_type_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3222 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_label` (`app_label`,`model`)
) ENGINE=MyISAM AUTO_INCREMENT=69 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_3da3d3d8` (`expire_date`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_site`
--

DROP TABLE IF EXISTS `django_site`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_site` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `login_customuser`
--

DROP TABLE IF EXISTS `login_customuser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `login_customuser` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(128) NOT NULL,
  `last_login` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mailing_element`
--

DROP TABLE IF EXISTS `mailing_element`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mailing_element` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `mailing_id` int(11) NOT NULL,
  `order` int(10) unsigned NOT NULL,
  `content` varchar(255) DEFAULT NULL,
  `function` varchar(255) DEFAULT NULL,
  `params` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `mailing_element_5904ac78` (`mailing_id`)
) ENGINE=MyISAM AUTO_INCREMENT=218 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mailing_mailing`
--

DROP TABLE IF EXISTS `mailing_mailing`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mailing_mailing` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `mail_type` int(10) unsigned NOT NULL,
  `when` int(10) unsigned NOT NULL,
  `target_date` datetime DEFAULT NULL,
  `dom` int(10) unsigned DEFAULT NULL,
  `mon` int(10) unsigned DEFAULT NULL,
  `dow` int(10) unsigned DEFAULT NULL,
  `recipient_group` int(10) unsigned NOT NULL,
  `recipient` varchar(256) DEFAULT NULL,
  `template` varchar(512) DEFAULT NULL,
  `subject` varchar(512) DEFAULT NULL,
  `show_ads` tinyint(1) NOT NULL,
  `read_count` int(10) unsigned DEFAULT NULL,
  `revisit_count` int(10) unsigned DEFAULT NULL,
  `spam_count` int(10) unsigned DEFAULT NULL,
  `unsubscribe_count` int(10) unsigned DEFAULT NULL,
  `user_delete_count` int(10) unsigned DEFAULT NULL,
  `recipient_count` int(10) unsigned DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `completed` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=56 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mailing_userreadmail`
--

DROP TABLE IF EXISTS `mailing_userreadmail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mailing_userreadmail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `mailing_id` int(11) NOT NULL,
  `date_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `mailing_userreadmail_403f60f` (`user_id`),
  KEY `mailing_userreadmail_5904ac78` (`mailing_id`)
) ENGINE=MyISAM AUTO_INCREMENT=129353 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `meas_caloriessuggestion`
--

DROP TABLE IF EXISTS `meas_caloriessuggestion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `meas_caloriessuggestion` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `suggestion` varchar(1024) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=33 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `meas_dietsuggestion`
--

DROP TABLE IF EXISTS `meas_dietsuggestion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `meas_dietsuggestion` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `suggestion` varchar(1024) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=33 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `meas_hourlystepavg`
--

DROP TABLE IF EXISTS `meas_hourlystepavg`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `meas_hourlystepavg` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `date_time` datetime NOT NULL,
  `steps` varchar(1024) NOT NULL,
  `total` int(11) NOT NULL,
  `calories` double NOT NULL,
  `device_id` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `meas_hourlystepavg_403f60f` (`user_id`),
  KEY `meas_hourlystepavg_5b7abc50` (`device_id`)
) ENGINE=MyISAM AUTO_INCREMENT=5929 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `meas_step`
--

DROP TABLE IF EXISTS `meas_step`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `meas_step` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `date_time` datetime NOT NULL,
  `steps` varchar(1024) NOT NULL,
  `steps2` varchar(2048) DEFAULT NULL,
  `am` varchar(512) DEFAULT NULL,
  `total` int(11) NOT NULL,
  `calories` double NOT NULL,
  `device_id` int(11) DEFAULT NULL,
  `device2_id` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `meas_step_403f60f` (`user_id`),
  KEY `meas_step_5b7abc50` (`device_id`),
  KEY `meas_step_346837f` (`device2_id`)
) ENGINE=MyISAM AUTO_INCREMENT=1843445 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `poll_answer`
--

DROP TABLE IF EXISTS `poll_answer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `poll_answer` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `question_id` int(11) NOT NULL,
  `answer` varchar(255) NOT NULL,
  `count` int(10) unsigned NOT NULL,
  `profile_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `poll_answer_1f92e550` (`question_id`),
  KEY `poll_answer_141c6eec` (`profile_id`)
) ENGINE=MyISAM AUTO_INCREMENT=142 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `poll_question`
--

DROP TABLE IF EXISTS `poll_question`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `poll_question` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `question` longtext NOT NULL,
  `answer_type` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=38 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `poll_useranswer`
--

DROP TABLE IF EXISTS `poll_useranswer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `poll_useranswer` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `question_id` int(11) NOT NULL,
  `answer_id` int(11) NOT NULL,
  `date_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `poll_useranswer_403f60f` (`user_id`),
  KEY `poll_useranswer_1f92e550` (`question_id`),
  KEY `poll_useranswer_2c9474d0` (`answer_id`)
) ENGINE=MyISAM AUTO_INCREMENT=5219 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `score_point`
--

DROP TABLE IF EXISTS `score_point`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `score_point` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `action_date` datetime NOT NULL,
  `action_name` varchar(8) NOT NULL,
  `action_param` varchar(255) DEFAULT NULL,
  `points_earned` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `score_point_403f60f` (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3672350 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `score_userscore`
--

DROP TABLE IF EXISTS `score_userscore`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `score_userscore` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `score` int(11) DEFAULT NULL,
  `xscore` int(11) DEFAULT NULL,
  `high_score` int(11) DEFAULT NULL,
  `last_week_score` int(11) DEFAULT NULL,
  `score_rank` int(11) DEFAULT NULL,
  `xscore_rank` int(11) DEFAULT NULL,
  `last_week_score_rank` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `score_userscore_403f60f` (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=42492 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `social_auth_association`
--

DROP TABLE IF EXISTS `social_auth_association`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `social_auth_association` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `server_url` varchar(255) NOT NULL,
  `handle` varchar(255) NOT NULL,
  `secret` varchar(255) NOT NULL,
  `issued` int(11) NOT NULL,
  `lifetime` int(11) NOT NULL,
  `assoc_type` varchar(64) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `social_auth_nonce`
--

DROP TABLE IF EXISTS `social_auth_nonce`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `social_auth_nonce` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `server_url` varchar(255) NOT NULL,
  `timestamp` int(11) NOT NULL,
  `salt` varchar(40) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `social_auth_usersocialauth`
--

DROP TABLE IF EXISTS `social_auth_usersocialauth`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `social_auth_usersocialauth` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `provider` varchar(32) NOT NULL,
  `uid` varchar(255) NOT NULL,
  `extra_data` longtext NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `provider` (`provider`,`uid`),
  KEY `social_auth_usersocialauth_403f60f` (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=2566 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `statistics_agevsuser`
--

DROP TABLE IF EXISTS `statistics_agevsuser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `statistics_agevsuser` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `stat_time` datetime NOT NULL,
  `age` int(10) unsigned NOT NULL,
  `num_of_boys` int(10) unsigned NOT NULL,
  `num_of_girls` int(10) unsigned NOT NULL,
  `num_of_users` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=3278 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `statistics_avgdailystep`
--

DROP TABLE IF EXISTS `statistics_avgdailystep`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `statistics_avgdailystep` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `stat_time` datetime NOT NULL,
  `girls_average` int(10) unsigned NOT NULL,
  `boys_average` int(10) unsigned NOT NULL,
  `users_average` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `statistics_bmivsuser`
--

DROP TABLE IF EXISTS `statistics_bmivsuser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `statistics_bmivsuser` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `stat_time` datetime NOT NULL,
  `bmi` varchar(8) NOT NULL,
  `num_of_girls` int(10) unsigned NOT NULL,
  `num_of_boys` int(10) unsigned NOT NULL,
  `num_of_users` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=201 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `statistics_dailystatistics`
--

DROP TABLE IF EXISTS `statistics_dailystatistics`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `statistics_dailystatistics` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `stat_time` datetime NOT NULL,
  `active_users` varchar(32) NOT NULL,
  `total_steps` varchar(128) NOT NULL,
  `total_clories` varchar(128) NOT NULL,
  `total_users` varchar(32) NOT NULL,
  `fb_users` varchar(32) NOT NULL,
  `email_users` varchar(32) NOT NULL,
  `num_of_girls` varchar(32) NOT NULL,
  `num_of_boys` varchar(32) NOT NULL,
  `ad_income_android` varchar(32) NOT NULL,
  `ad_request` varchar(32) NOT NULL,
  `ad_click` varchar(32) NOT NULL,
  `install_android` varchar(32) NOT NULL,
  `page_visit` varchar(32) NOT NULL,
  `fb_visit` varchar(32) NOT NULL,
  `total_client_requests` varchar(32) NOT NULL,
  `android_client_requests` varchar(32) NOT NULL,
  `iphone_client_requests` varchar(32) NOT NULL,
  `new_total_dev` varchar(32) NOT NULL,
  `new_apple_dev` varchar(32) NOT NULL,
  `new_other_dev` varchar(32) NOT NULL,
  `reserved4` varchar(32) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=1839 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `statistics_dailystats`
--

DROP TABLE IF EXISTS `statistics_dailystats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `statistics_dailystats` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date_time` datetime NOT NULL,
  `num_User` int(11) NOT NULL,
  `num_UserDisabled` int(11) NOT NULL,
  `num_UserNoEmail` int(11) NOT NULL,
  `num_UserRegFb` int(11) NOT NULL,
  `num_UserRegEmail` int(11) NOT NULL,
  `num_BodyInfo` int(11) NOT NULL,
  `num_Step` int(11) NOT NULL,
  `num_StepTotal` int(11) NOT NULL,
  `num_StepAvg` int(11) NOT NULL,
  `num_BadgeToUser` int(11) NOT NULL,
  `num_Point` int(11) NOT NULL,
  `num_Device2` int(11) NOT NULL,
  `num_UserAnswer` int(11) NOT NULL,
  `num_Venue` int(11) NOT NULL,
  `num_Checkin` int(11) NOT NULL,
  `num_SupportReq` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `statistics_httpreq`
--

DROP TABLE IF EXISTS `statistics_httpreq`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `statistics_httpreq` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `req` varchar(1024) NOT NULL,
  `resp` varchar(5) NOT NULL,
  `cause` varchar(32) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=73898 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `statistics_statistics`
--

DROP TABLE IF EXISTS `statistics_statistics`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `statistics_statistics` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `stat_time` datetime NOT NULL,
  `total_users` varchar(32) NOT NULL,
  `total_active_users` varchar(128) NOT NULL,
  `fb_users` varchar(32) NOT NULL,
  `email_users` varchar(32) NOT NULL,
  `total_steps` varchar(128) NOT NULL,
  `total_get` varchar(128) NOT NULL,
  `total_clories` varchar(128) NOT NULL,
  `number_of_users` varchar(32) NOT NULL,
  `number_of_girls` varchar(32) NOT NULL,
  `number_of_boys` varchar(32) NOT NULL,
  `average_age` varchar(8) NOT NULL,
  `average_weight` varchar(8) NOT NULL,
  `average_height` varchar(8) NOT NULL,
  `average_daily_steps` varchar(8) NOT NULL,
  `total_android_install` varchar(32) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tinyurl_tinyurl`
--

DROP TABLE IF EXISTS `tinyurl_tinyurl`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tinyurl_tinyurl` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `url` varchar(200) NOT NULL,
  `hash` varchar(32) NOT NULL,
  `clicks` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `hash` (`hash`)
) ENGINE=MyISAM AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `userprofile_avatar`
--

DROP TABLE IF EXISTS `userprofile_avatar`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `userprofile_avatar` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `image` varchar(100) NOT NULL,
  `user_id` int(11) NOT NULL,
  `date` datetime NOT NULL,
  `valid` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`valid`),
  KEY `userprofile_avatar_403f60f` (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=27 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `userprofile_emailvalidation`
--

DROP TABLE IF EXISTS `userprofile_emailvalidation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `userprofile_emailvalidation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `email` varchar(75) NOT NULL,
  `key` varchar(70) NOT NULL,
  `created` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  UNIQUE KEY `key` (`key`)
) ENGINE=MyISAM AUTO_INCREMENT=1530 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `venue_checkin`
--

DROP TABLE IF EXISTS `venue_checkin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `venue_checkin` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `venue_id` varchar(128) NOT NULL,
  `points` int(10) unsigned NOT NULL,
  `date_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `venue_checkin_403f60f` (`user_id`),
  KEY `venue_checkin_778b8634` (`venue_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `venue_venue`
--

DROP TABLE IF EXISTS `venue_venue`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `venue_venue` (
  `venue_id` varchar(128) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `icon` varchar(255) DEFAULT NULL,
  `description` longtext,
  `category_id` int(11) DEFAULT NULL,
  `mayor_id` int(11) DEFAULT NULL,
  `lat` double DEFAULT NULL,
  `lon` double DEFAULT NULL,
  `points` int(10) unsigned DEFAULT NULL,
  `checkins` int(10) unsigned DEFAULT NULL,
  `likes` int(10) unsigned DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `page_rank` int(10) unsigned DEFAULT NULL,
  `date_time` datetime NOT NULL,
  PRIMARY KEY (`venue_id`),
  KEY `venue_venue_42dc49bc` (`category_id`),
  KEY `venue_venue_2453ffeb` (`mayor_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `venue_venuecategory`
--

DROP TABLE IF EXISTS `venue_venuecategory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `venue_venuecategory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  `icon` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-01-24 18:18:29
