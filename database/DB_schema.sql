-- MySQL dump 10.13  Distrib 5.7.17, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: bucketlist
-- ------------------------------------------------------
-- Server version	5.7.21-log

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
-- Table structure for table `tbl_user`
--

DROP TABLE IF EXISTS `tbl_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_user` (
  `user_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(255) DEFAULT NULL,
  `user_username` varchar(255) DEFAULT NULL,
  `user_password` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `user_id` (`user_id`)
);
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping routines for database 'bucketlist'
--
/*!50003 DROP PROCEDURE IF EXISTS `sp_createUser` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `sp_createUser`(
	IN p_name VARCHAR(255),
    IN p_username VARCHAR(255),
    IN p_password VARCHAR(255)
    )
BEGIN
	if ( select exists (select 1 from tbl_user where  user_username = p_username ) )
    then
		select 'Username Exists !!';
	else
		insert into tbl_user
         (user_name, user_username, user_password)
         values
         (p_name, p_username, p_password)
		;
	end if;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_validateLogin` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `sp_validateLogin`(
IN p_username VARCHAR(255)
)
BEGIN
    select * from tbl_user where user_name = p_username;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-04-12 19:50:58

DROP TABLE IF EXISTS `tbl_property_owner`;
CREATE TABLE `tbl_property_owner` (
  `owner_id`      BIGINT(20)  NOT NULL AUTO_INCREMENT,
  `owner_name`    VARCHAR(64) NOT NULL,
  `owner_surname` VARCHAR(64) NOT NULL,
  `owner_gender`  VARCHAR(12)          DEFAULT NULL,
  PRIMARY KEY (`owner_id`),
  UNIQUE KEY `owner_id` (`owner_id`)
);
INSERT INTO tbl_property_owner (owner_name, owner_surname, owner_gender) VALUES ('Zajac', 'Tobiasz', 'MALE');
INSERT INTO tbl_property_owner (owner_name, owner_surname, owner_gender) VALUES ('Nowicki', 'Slawomir', 'MALE');


DROP TABLE IF EXISTS `tbl_property`;
CREATE TABLE `tbl_property` (
  `property_id`       BIGINT(20) NOT NULL AUTO_INCREMENT,
  `property_owner_id` BIGINT(20),
  INDEX `property_owner_id__index` (`property_owner_id`),
  FOREIGN KEY (property_owner_id)
  REFERENCES tbl_property_owner (owner_id)
    ON DELETE SET NULL,
  `property_street`   VARCHAR(64),
  `property_city`     VARCHAR(64),
  `property_zip`      VARCHAR(64),
  `property_status`   INT(8),
  PRIMARY KEY (`property_id`),
  UNIQUE KEY `property_id` (`property_id`)
);
INSERT INTO tbl_property (property_owner_id, property_street, property_city, property_zip, property_status) VALUES (1, 'Dzwinska 37', 'Bialystok', '15-161', 0);
INSERT INTO tbl_property (property_owner_id, property_street, property_city, property_zip, property_status) VALUES (2, 'Maloszynska 44', 'Wroclaw', '54-014', 0);

CREATE TABLE `tbl_property_locator` (
  `locator_id`      BIGINT(20) NOT NULL AUTO_INCREMENT,
  `locator_name`    VARCHAR(255) NOT NULL,
  `locator_surname` VARCHAR(255) NOT NULL DEFAULT 'Janusz',
  `locator_gender`  VARCHAR(12)          DEFAULT NULL,
  `property_id`      BIGINT(20),
  INDEX `property_id__index` (`property_id`),
  FOREIGN KEY (property_id)
  REFERENCES tbl_property (property_id)
    ON DELETE SET NULL,
  PRIMARY KEY (`locator_id`),
  UNIQUE KEY `locator_id` (`locator_id`)
);
INSERT INTO tbl_property_locator (locator_name, locator_surname, locator_gender, property_id) VALUES ('Majewska','Zofia','FEMALE',1);
INSERT INTO tbl_property_locator (locator_name, locator_surname, locator_gender, property_id) VALUES ('Wisniewska','Brygida','FEMALE',1);
INSERT INTO tbl_property_locator (locator_name, locator_surname, locator_gender, property_id) VALUES ('Chmielewski','Bogumil','MALE',2);
INSERT INTO tbl_property_locator (locator_name, locator_surname, locator_gender, property_id) VALUES ('Kaczmarek','Beata','FEMALE',2);

commit;
