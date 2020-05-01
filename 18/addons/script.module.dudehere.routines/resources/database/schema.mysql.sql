SET autocommit=0;

START TRANSACTION;

CREATE TABLE IF NOT EXISTS `version` (
	`db_version` int(11) NOT NULL DEFAULT 1,
	PRIMARY KEY(`db_version`)
);

CREATE TABLE IF NOT EXISTS `scraper_states` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`name` varchar(150) NOT NULL,
	`enabled` int(11) NOT NULL DEFAULT '1',
	PRIMARY KEY (`id`),
	UNIQUE KEY `name_UNIQUE` (`name`)
);

CREATE TABLE IF NOT EXISTS `scraper_stats` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`service` varchar(150) DEFAULT NULL,
	`host` varchar(150) DEFAULT NULL,
	`attempts` FLOAT NOT NULL DEFAULT '0',
	`resolved` FLOAT NOT NULL DEFAULT '0',
	`success` FLOAT NOT NULL DEFAULT '0',
	PRIMARY KEY (`id`),
	UNIQUE KEY `service_UNIQUE` (`service`,`host`)
);

CREATE TABLE IF NOT EXISTS `host_stats` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`service` varchar(150) DEFAULT NULL,
	`host` varchar(150) DEFAULT NULL,
	`resolved` FLOAT NOT NULL DEFAULT '0',
	`completed` FLOAT NOT NULL DEFAULT '0',
	`ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `search_results` (
	`cache_id` int(11) NOT NULL AUTO_INCREMENT,
	`hash` varchar(255) NOT NULL,
	`service` varchar(45) NOT NULL,
	`result` LONGBLOB DEFAULT NULL,
	`ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`cache_id`)
);

ALTER TABLE `search_results` CHANGE COLUMN `result` `result` LONGBLOB NULL DEFAULT NULL;

CREATE TABLE IF NOT EXISTS `playback_states` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`hash_id` varchar(75) DEFAULT NULL,
	`current` varchar(45) DEFAULT NULL,
	`total` varchar(45) DEFAULT NULL,
	PRIMARY KEY (`id`),
	UNIQUE KEY `hash_id_UNIQUE` (`hash_id`)
);

CREATE TABLE IF NOT EXISTS `host_weights` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`host` varchar(150) DEFAULT NULL,
	`weight` int(11) DEFAULT '1000',
	`disabled` tinyint(1) DEFAULT '0',
	PRIMARY KEY (`id`),
	UNIQUE KEY `host_UNIQUE` (`host`)
);

CREATE OR REPLACE VIEW `fresh_cache` AS
	SELECT 
		`search_results`.`cache_id` AS `cache_id`,
		`search_results`.`hash` AS `hash`,
		`search_results`.`service` AS `service`,
		`search_results`.`result` AS `result`,
		(timestampdiff(MINUTE, `search_results`.`ts`, NOW()) < 240) AS `fresh`
	FROM `search_results`
	WHERE (timestampdiff(MINUTE, `search_results`.`ts`, NOW()) < 240)
;
;

CREATE OR REPLACE VIEW `stale_cache` AS
	SELECT 
		`search_results`.`cache_id` AS `cache_id`,
		`search_results`.`hash` AS `hash`,
		(timestampdiff(MINUTE, `search_results`.`ts`, NOW()) > 240) AS `stale`
	FROM `search_results`
	WHERE (timestampdiff(MINUTE, `search_results`.`ts`, NOW()) > 240)
;

CREATE OR REPLACE VIEW `host_ranks` AS
	SELECT host, 
	((1000 - weight) - (10000 * disabled)) as rank, 
	weight 
	FROM host_weights 
	WHERE ((1000 - weight) - (10000 * disabled)) >= 0 
	ORDER BY weight, host ASC
;

CREATE OR REPLACE VIEW `host_scores` AS
	SELECT host, 
	sum(resolved) AS success,
	count(host) AS attempted, 
	sum(resolved) * 1.0  / count(host) AS score 
	FROM host_stats 
	GROUP BY host 
	ORDER BY score DESC
;

COMMIT;

SET autocommit=1;
