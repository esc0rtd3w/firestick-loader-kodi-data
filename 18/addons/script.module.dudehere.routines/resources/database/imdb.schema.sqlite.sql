CREATE TABLE IF NOT EXISTS "version" (
	"db_version" INTEGER DEFAULT 1 UNIQUE,
	PRIMARY KEY(db_version)
);

CREATE TABLE IF NOT EXISTS "cache" (
	"id" INTEGER PRIMARY KEY AUTOINCREMENT,
	"hash_id" TEXT UNIQUE,
	"media" TEXT,
	"url" TEXT,
	"results" TEXT,
	"ts" TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
);

CREATE VIEW IF NOT EXISTS "stale_cache" AS
	SELECT id, 
	hash_id, 
	strftime("%s",'now') -  strftime("%s",ts) > (3600 * 2) AS stale 
	FROM cache 
	WHERE stale = 1
;
