DROP TABLE IF EXISTS `tbl_user`;
CREATE TABLE `tbl_user` (
  `user_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(255) DEFAULT NULL,
  `user_username` varchar(255) DEFAULT NULL,
  `user_password` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `user_id` (`user_id`)
);

DROP PROCEDURE IF EXISTS `sp_createUser`;
DELIMITER ;;
CREATE PROCEDURE `sp_createUser`(
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

DROP PROCEDURE IF EXISTS `sp_validateLogin`;
DELIMITER ;;
CREATE PROCEDURE `sp_validateLogin`(
IN p_username VARCHAR(255)
)
BEGIN
    select * from tbl_user where user_name = p_username;
END ;;
DELIMITER ;


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
