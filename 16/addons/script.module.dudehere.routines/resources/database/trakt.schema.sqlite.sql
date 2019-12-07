CREATE TABLE IF NOT EXISTS "version" (
	"db_version" INTEGER DEFAULT 1 UNIQUE,
	PRIMARY KEY(db_version)
);

CREATE TABLE IF NOT EXISTS "my_favorites"(
	"favorite_id" INTEGER PRIMARY KEY AUTOINCREMENT,
	"media" TEXT,
	"trakt_id" TEXT,
	"cache" BLOB,
	UNIQUE (media, trakt_id)
);

CREATE TABLE IF NOT EXISTS "activities" (
	"id" INTEGER PRIMARY KEY AUTOINCREMENT,
	"activity" TEXT UNIQUE,
	"ts" TIMESTAMP
);

CREATE TABLE IF NOT EXISTS "activity_cache" (
	"id" INTEGER PRIMARY KEY AUTOINCREMENT,
	"activity" TEXT UNIQUE,
	"cache" TEXT
);

CREATE TABLE IF NOT EXISTS "request_cache" (
	"request_id" INTEGER PRIMARY KEY AUTOINCREMENT,
	"url" TEXT UNIQUE,
	"results" TEXT,
	"ts" TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
);


CREATE TABLE IF NOT EXISTS "id_table" (
	"id" INTEGER PRIMARY KEY AUTOINCREMENT,
	"media_type" TEXT,
	"trakt_id" INTEGER,
	"slug" TEXT,
	"tvdb_id" INTEGER,
	"imdb_id" TEXT,
	"tmdb_id" INTEGER,
	"tvrage_id" INTEGER,
	"tvmaze_id" INTEGER,
	"season" INTEGER,
	"episode" INTEGER,
	"show_tvdb_id" INTEGER,
	UNIQUE(media_type, trakt_id) ON CONFLICT IGNORE
);

CREATE TABLE IF NOT EXISTS metadata_activities (
	"activity_id" INTEGER PRIMARY KEY AUTOINCREMENT,
	"media_id" TEXT,
	"media" TEXT,
	"ts" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	UNIQUE ("media_id", "media") ON CONFLICT REPLACE
);

CREATE TABLE IF NOT EXISTS metadata_episodes (
	"episode_id" INTEGER PRIMARY KEY AUTOINCREMENT,
	"trakt_id" TEXT UNIQUE,
	"updated_at" TIMESTAMP,
	"metadata" TEXT
);

CREATE TABLE IF NOT EXISTS metadata_movies (
	"movie_id" INTEGER PRIMARY KEY AUTOINCREMENT,
	"trakt_id" TEXT UNIQUE,
	"slug" TEXT UNIQUE,
	"imdb_id" TEXT UNIQUE,
	"tmdb_id" TEXT,
	"updated_at" TIMESTAMP,
	"metadata" TEXT
);

CREATE TABLE IF NOT EXISTS "metadata_credits" (
	"credit_id" INTEGER PRIMARY KEY AUTOINCREMENT,
	"trakt_id" INTEGER UNIQUE,
	"media" TEXT,
	"credits" BLOB
);

CREATE TABLE IF NOT EXISTS metadata_shows (
	"show_id" INTEGER PRIMARY KEY AUTOINCREMENT,
	"trakt_id" TEXT UNIQUE,
	"slug" TEXT UNIQUE,
	"imdb_id" TEXT UNIQUE,
	"tvdb_id" TEXT,
	"tmdb_id" TEXT,
	"updated_at" TIMESTAMP,
	"metadata" TEXT
);

CREATE TABLE IF NOT EXISTS "fanart_episodes" (
	"episode_id" INTEGER PRIMARY KEY AUTOINCREMENT,
	"trakt_id" INTEGER UNIQUE,
	"screenshot" TEXT
);

CREATE TABLE IF NOT EXISTS "fanart_movies" (
	"movie_id" INTEGER PRIMARY KEY AUTOINCREMENT,
	"trakt_id" INTEGER UNIQUE,
	"logo" TEXT,
	"clearlogo" TEXT,
	"fanart" TEXT,
	"poster" TEXT,
	"banner" TEXT
);

CREATE TABLE IF NOT EXISTS "fanart_people" (
	"people_id" INTEGER PRIMARY KEY AUTOINCREMENT,
	"tmdb_id" INTEGER UNIQUE,
	"image" TEXT
);

CREATE TABLE IF NOT EXISTS "fanart_seasons" (
	"season_id" INTEGER PRIMARY KEY AUTOINCREMENT,
	"tvdb_id" TEXT,
	"season" INTEGER,
	"poster" TEXT,
	UNIQUE (tvdb_id, season)
);

CREATE TABLE IF NOT EXISTS "fanart_shows" (
	"show_id" INTEGER PRIMARY KEY AUTOINCREMENT,
	"trakt_id" INTEGER UNIQUE,
	"logo" TEXT,
	"clearlogo" TEXT,
	"fanart" TEXT,
	"poster" TEXT,
	"banner" TEXT
);

CREATE TABLE IF NOT EXISTS "tvmaze_episodes" (
	"id" INTEGER PRIMARY KEY AUTOINCREMENT,
	"tvdb_id" INTEGER,
	"tvmaze_id" INTEGER,
	"season" INTEGER,
	"episode" INTEGER,
	"screenshot" TEXT,
	UNIQUE (tvdb_id, season, episode) ON CONFLICT IGNORE
);

CREATE TABLE IF NOT EXISTS "sync_states"(
	"id" INTEGER PRIMARY KEY AUTOINCREMENT,
	"name" TEXT,
	"slug" TEXT UNIQUE,
	"addon" TEXT,
	"sync" INTEGER DEFAULT 1
);

CREATE VIEW IF NOT EXISTS "fresh_fanart" AS
	SELECT activity_id, 
	media_id, 
	media, 
	strftime("%s",'now') -  strftime("%s",ts) < (3600 * 24) AS fresh 
	FROM metadata_activities 
;

CREATE VIEW IF NOT EXISTS "stale_cache" AS
	SELECT id, 
	hash_id, 
	strftime("%s",'now') -  strftime("%s",ts) > (3600 * 2) AS stale 
	FROM cache 
	WHERE stale = 1
;
