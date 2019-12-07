SET autocommit=0;

START TRANSACTION;

CREATE TABLE IF NOT EXISTS `version` (
	`db_version` int(11) NOT NULL DEFAULT 1,
	PRIMARY KEY(`db_version`)
);

CREATE TABLE IF NOT EXISTS `activities` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`activity` varchar(150) NOT NULL,
	`ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`id`),
	UNIQUE KEY `activity_UNIQUE` (`activity`)
);

CREATE TABLE IF NOT EXISTS `activity_cache` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`activity` varchar(150) NOT NULL,
	`cache` LONGBLOB DEFAULT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `request_cache` (
	`request_id` int(11) NOT NULL AUTO_INCREMENT,
	`url` varchar(250) NOT NULL,
	`results` LONGBLOB DEFAULT NULL,
	`ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`request_id`),
	UNIQUE KEY `url_UNIQUE` (`url`)
);

CREATE TABLE IF NOT EXISTS `id_table` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`media_type` VARCHAR(45) NULL,
	`trakt_id` INT NOT NULL,
	`slug` VARCHAR(255) DEFAULT NULL,
	`imdb_id` VARCHAR(45) DEFAULT NULL,
	`tmdb_id` INT DEFAULT NULL,
	`tvdb_id` INT DEFAULT NULL,
	`tvrage_id` INT DEFAULT NULL,
	`tvmaze_id` INT DEFAULT NULL,
	`season` INT DEFAULT NULL,
	`episode` INT DEFAULT NULL,
	`show_tvdb_id` INT DEFAULT NULL,
	PRIMARY KEY (`id`),
	UNIQUE INDEX `media_UNIQUE` (`media_type`, `trakt_id` ASC)
);

CREATE TABLE IF NOT EXISTS `my_favorites` (
	`favorite_id` INT NOT NULL AUTO_INCREMENT,
	`media` VARCHAR(45) NULL,
	`trakt_id` INT NOT NULL,
	`cache` LONGBLOB NULL,
	PRIMARY KEY (`favorite_id`),
	UNIQUE INDEX `media_UNIQUE` (`media`, `media` ASC)
);

CREATE TABLE IF NOT EXISTS `metadata_activities` (
	`activity_id` INT NOT NULL AUTO_INCREMENT,
	`media_id` VARCHAR(45) NULL,
	`media` VARCHAR(45) NULL,
	`ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`activity_id`),
	UNIQUE INDEX `media_UNIQUE` (`media_id`, `media` ASC)
);

CREATE TABLE IF NOT EXISTS `metadata_credits` (
	`credit_id` INT NOT NULL AUTO_INCREMENT,
	`trakt_id` VARCHAR(45) NULL,
	`media` VARCHAR(45) NULL,
	`credits` LONGBLOB NULL,
	PRIMARY KEY (`credit_id`),
	UNIQUE INDEX `trakt_id_UNIQUE` (`trakt_id` ASC)
);

CREATE TABLE IF NOT EXISTS `metadata_episodes` (
	`episode_id` INT NOT NULL AUTO_INCREMENT,
	`trakt_id` VARCHAR(45) NULL,
	`updated_at` TIMESTAMP NULL,
	`metadata` LONGBLOB NULL,
	PRIMARY KEY (`episode_id`),
	UNIQUE INDEX `trakt_id_UNIQUE` (`trakt_id` ASC)
);

CREATE TABLE IF NOT EXISTS `metadata_movies` (
	`movie_id` INT NOT NULL AUTO_INCREMENT,
	`trakt_id` VARCHAR(45) NULL,
	`slug` VARCHAR(125) NULL,
	`imdb_id` VARCHAR(45) NULL,
	`tmdb_id` VARCHAR(45) NULL,
	`updated_at` TIMESTAMP NULL,
	`metadata` LONGBLOB NULL,
	PRIMARY KEY (`movie_id`),
	UNIQUE INDEX `trakt_id_UNIQUE` (`trakt_id` ASC),
	UNIQUE INDEX `slug_UNIQUE` (`slug` ASC),
	UNIQUE INDEX `imdb_UNIQUE` (`imdb_id` ASC)
);

CREATE TABLE IF NOT EXISTS `metadata_shows` (
	`show_id` INT NOT NULL AUTO_INCREMENT,
	`trakt_id` VARCHAR(45) NULL,
	`slug` VARCHAR(125) NULL,
	`imdb_id` VARCHAR(45) NULL,
	`tvdb_id` VARCHAR(45) NULL,
	`tmdb_id` VARCHAR(45) NULL,
	`updated_at` TIMESTAMP NULL,
	`metadata` LONGBLOB NULL,
	PRIMARY KEY (`show_id`),
	UNIQUE INDEX `trakt_id_UNIQUE` (`trakt_id` ASC),
	UNIQUE INDEX `slug_UNIQUE` (`slug` ASC),
	UNIQUE INDEX `imdb_UNIQUE` (`imdb_id` ASC)
);

CREATE TABLE IF NOT EXISTS `fanart_seasons` (
	`season_id` INT NOT NULL AUTO_INCREMENT,
	`tvdb_id` INT NOT NULL,
	`season` INT NULL,
	`poster` VARCHAR(255) NULL,
	PRIMARY KEY (`season_id`),
	UNIQUE INDEX `season_UNIQUE` (`tvdb_id`, `season` ASC)
);

CREATE TABLE IF NOT EXISTS `fanart_episodes` (
	`episode_id` INT NOT NULL AUTO_INCREMENT,
	`trakt_id` INT NOT NULL,
	`screenshot` VARCHAR(255) NULL,
	PRIMARY KEY (`episode_id`),
	UNIQUE INDEX `trakt_UNIQUE` (`trakt_id` ASC)
);

CREATE TABLE IF NOT EXISTS `fanart_people` (
	`people_id` INT NOT NULL AUTO_INCREMENT,
	`tmdb_id` INT NOT NULL,
	`image` VARCHAR(255) NULL,
	PRIMARY KEY (`people_id`),
	UNIQUE INDEX `tmdb_UNIQUE` (`tmdb_id` ASC)
);

CREATE TABLE IF NOT EXISTS `fanart_shows` (
	`show_id` INT NOT NULL AUTO_INCREMENT,
	`trakt_id` INT NOT NULL,
	`logo` VARCHAR(255) NULL,
	`clearlogo` VARCHAR(255) NULL,
	`fanart` VARCHAR(255) NULL,
	`poster` VARCHAR(255) NULL,
	`banner` VARCHAR(255) NULL,
	PRIMARY KEY (`show_id`),
	UNIQUE INDEX `trakt_UNIQUE` (`trakt_id` ASC)
);

CREATE TABLE IF NOT EXISTS `fanart_movies` (
	`movie_id` INT NOT NULL AUTO_INCREMENT,
	`trakt_id` INT NOT NULL,
	`logo` VARCHAR(255) NULL,
	`clearlogo` VARCHAR(255) NULL,
	`fanart` VARCHAR(255) NULL,
	`poster` VARCHAR(255) NULL,
	`banner` VARCHAR(255) NULL,
	PRIMARY KEY (`movie_id`),
	UNIQUE INDEX `trakt_UNIQUE` (`trakt_id` ASC)
);

CREATE TABLE IF NOT EXISTS `tvmaze_episodes` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`tvdb_id` INT NULL,
	`tvmaze_id` INT NULL,
	`season` INT NULL,
	`episode` INT NULL,
	`screenshot` VARCHAR(255) NULL,
	PRIMARY KEY (`id`),
	UNIQUE INDEX `tvdb_id_UNIQUE` (`tvdb_id`, `season`, `episode` ASC)
);

CREATE TABLE IF NOT EXISTS `sync_states`(
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`name` varchar(255) NOT NULL,
	`slug` varchar(100) NOT NULL,
	`addon` varchar(75) NOT NULL,
	`sync` int(11) NOT NULL DEFAULT '1',
	PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `request_cache` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`url` VARCHAR(255) NULL,
	`response` LONGBLOB NULL,
	`ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	UNIQUE INDEX `url_UNIQUE` (`url` ASC)
);

CREATE OR REPLACE VIEW `fresh_requests` AS
	SELECT url, 
	response,
	(timestampdiff(MINUTE, `metadata_activities`.`ts`, NOW()) < 60) AS `fresh` 
	FROM request_cache
	WHERE (timestampdiff(MINUTE, `metadata_activities`.`ts`, NOW()) < 60)
;	

CREATE OR REPLACE VIEW `fresh_fanart` AS
	SELECT activity_id, 
	media_id,
	media,
	(timestampdiff(MINUTE, `metadata_activities`.`ts`, NOW()) < 1440) AS `fresh` 
	FROM metadata_activities 
;

CREATE OR REPLACE VIEW `stale_cache` AS
	SELECT id, 
	hash_id, 
	(timestampdiff(MINUTE, `cache`.`ts`, NOW()) > 120) AS `stale` 
	FROM cache 
	WHERE (timestampdiff(MINUTE, `cache`.`ts`, NOW()) > 120)
;

COMMIT;

SET autocommit=1;