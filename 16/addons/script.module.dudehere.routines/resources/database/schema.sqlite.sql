CREATE TABLE IF NOT EXISTS "version" (
	"db_version" INTEGER DEFAULT 1 UNIQUE,
	PRIMARY KEY(db_version)
);

CREATE TABLE IF NOT EXISTS "search_results" (
	"cache_id" INTEGER PRIMARY KEY AUTOINCREMENT,
	"hash" TEXT,
	"service" TEXT,
	"result" TEXT,
	"ts" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS "scraper_states" (
	"id" INTEGER PRIMARY KEY AUTOINCREMENT,
	"name" TEXT UNIQUE,
	"enabled" INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS "scraper_stats" (
	"id" INTEGER PRIMARY KEY AUTOINCREMENT,
	"service" TEXT,
	"host" TEXT,
	"attempts" FLOAT DEFAULT (0),
	"resolved" FLOAT DEFAULT (0),
	"success" FLOAT DEFAULT (0),
	UNIQUE ("service", "host") ON CONFLICT REPLACE
);

CREATE TABLE IF NOT EXISTS "host_stats" (
	"id" INTEGER PRIMARY KEY AUTOINCREMENT,
	"service" TEXT,
	"host" TEXT,
	"resolved" INTEGER DEFAULT 0,
	"completed" INTEGER DEFAULT 0,
	"ts" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS "playback_states" (
	"id" INTEGER PRIMARY KEY AUTOINCREMENT,
	"hash_id" TEXT,
	"current" TEXT,
	"total" TEXT,
	UNIQUE ("hash_id") ON CONFLICT REPLACE
);

CREATE TABLE IF NOT EXISTS "host_weights" (
	"id" INTEGER PRIMARY KEY NOT NULL,
	"host" TEXT,
	"weight" INTEGER DEFAULT (1000),
	"disabled" INTEGER DEFAULT (0),
	UNIQUE ("host") ON CONFLICT IGNORE
);


CREATE TABLE IF NOT EXISTS "request_cache" (
	"id" INTEGER PRIMARY KEY AUTOINCREMENT,
	"url" TEXT,
	"response" BLOB,
	"ts" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	UNIQUE ("url") ON CONFLICT REPLACE
);


CREATE VIEW IF NOT EXISTS "fresh_requests" AS 
	SELECT url, 
	response 
	FROM request_cache 
	WHERE  strftime("%s","now") -  strftime("%s",ts) < 3600
;

CREATE VIEW IF NOT EXISTS "fresh_cache" AS
	SELECT cache_id, 
	hash, 
	service, 
	result,
	strftime("%s",'now') -  strftime("%s",ts) < (3600 * 4) AS fresh 
	FROM search_results 
	WHERE fresh = 1
;

CREATE VIEW IF NOT EXISTS "stale_cache" AS
	SELECT cache_id, 
	hash, 
	strftime("%s",'now') -  strftime("%s",ts) > (3600 * 4) AS stale 
	FROM search_results 
	WHERE stale = 1
;

CREATE VIEW IF NOT EXISTS "host_ranks" AS
	SELECT host, 
	((1000 - weight) - (10000 * disabled)) as rank, 
	weight 
	FROM host_weights 
	WHERE rank >= 0 
	ORDER BY weight, host ASC
;

CREATE VIEW IF NOT EXISTS "host_scores" AS
	SELECT host, 
	sum(resolved) AS success,
	count(host) AS attempted, 
	sum(resolved) * 1.0  / count(host) AS score 
	FROM host_stats 
	GROUP BY host 
	ORDER BY score DESC
;	
