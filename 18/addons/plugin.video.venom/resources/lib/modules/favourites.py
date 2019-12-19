# -*- coding: utf-8 -*-

import json, os, xbmc, xbmcaddon

try:
	from sqlite3 import dbapi2 as database
except:
	from pysqlite2 import dbapi2 as database

from resources.lib.modules import control

addonInfo = xbmcaddon.Addon().getAddonInfo
dataPath = xbmc.translatePath(addonInfo('profile')).decode('utf-8')
favouritesFile = os.path.join(dataPath, 'favourites.db')
progressFile = os.path.join(dataPath, 'progress.db')
notificationSound = False if control.setting('notification.sound') == 'false' else True


def getFavourites(content):
	try:
		dbcon = database.connect(favouritesFile)
		dbcur = dbcon.cursor()
		dbcur.execute("SELECT * FROM %s" % content)
		items = dbcur.fetchall()
		items = [(i[0].encode('utf-8'), eval(i[1].encode('utf-8'))) for i in items]
	except:
		items = []

	dbcon.close()
	return items


def getProgress(content):
	try:
		dbcon = database.connect(progressFile)
		dbcur = dbcon.cursor()
		dbcur.execute("SELECT * FROM %s" % content)
		items = dbcur.fetchall()
		items = [(i[0].encode('utf-8'), eval(i[1].encode('utf-8'))) for i in items]
	except:
		items = []

	dbcon.close()
	return items


def addFavourite(meta, content):
	try:
		item = dict()
		meta = json.loads(meta)
		# print "META DUMP FAVOURITES %s" % meta

		try:
			id = meta['imdb']
		except:
			id = meta['tvdb']

		if 'title' in meta: title = item['title'] = meta['title']
		if 'tvshowtitle' in meta: title = item['title'] = meta['tvshowtitle']
		if 'year' in meta: item['year'] = meta['year']
		if 'tvshowyear' in meta: item['tvshowyear'] = meta['tvshowyear']
		if 'poster' in meta: item['poster'] = meta['poster']
		if 'fanart' in meta: item['fanart'] = meta['fanart']
		if 'clearart' in meta: item['clearart'] = meta['clearart']
		if 'clearlogo' in meta: item['clearlogo'] = meta['clearlogo']
		if 'discart' in meta: item['discart'] = meta['discart']
		if 'imdb' in meta: item['imdb'] = meta['imdb']
		if 'tmdb' in meta: item['tmdb'] = meta['tmdb']
		if 'tvdb' in meta: item['tvdb'] = meta['tvdb']

		control.makeFile(dataPath)
		dbcon = database.connect(favouritesFile)
		dbcur = dbcon.cursor()
		dbcur.execute("CREATE TABLE IF NOT EXISTS %s (""id TEXT, ""items TEXT, ""UNIQUE(id)"");" % content)
		dbcur.execute("DELETE FROM %s WHERE id = '%s'" % (content, id))
		dbcur.execute("INSERT INTO %s Values (?, ?)" % content, (id, repr(item)))
		dbcur.connection.commit()
		dbcon.close()

		control.refresh()
		control.notification(title = title, message = 'Added to Favorites', icon = 'INFO', sound = notificationSound)
	except:
		return


def addEpisodes(meta, content):
	try:
		item = dict()
		meta = json.loads(meta)
		content = "episode"

		try:
			id = meta['imdb']
			if id == '' or id is None:
				id = meta['tvdb']
		except:
			id = meta['episodeIDS']['trakt']

		if 'title' in meta: title = item['title'] = meta['title']
		if 'tvshowtitle' in meta: title = item['tvshowtitle'] = meta['tvshowtitle']
		if 'year' in meta: item['year'] = meta['year']
		if 'tvshowyear' in meta: item['tvshowyear'] = meta['tvshowyear']
		if 'poster' in meta: item['poster'] = meta['poster']
		if 'fanart' in meta: item['fanart'] = meta['fanart']
		if 'clearart' in meta: item['clearart'] = meta['clearart']
		if 'clearlogo' in meta: item['clearlogo'] = meta['clearlogo']
		if 'imdb' in meta: item['imdb'] = meta['imdb']
		if 'tmdb' in meta: item['tmdb'] = meta['tmdb']
		if 'tvdb' in meta: item['tvdb'] = meta['tvdb']
		if 'episodeIDS' in meta: item['episodeIDS'] = meta['episodeIDS']
		if 'episode' in meta: item['episode'] = meta['episode']
		if 'season' in meta: item['season'] = meta['season']
		if 'premiered' in meta: item['premiered'] = meta['premiered']
		if 'original_year' in meta: item['original_year'] = meta['original_year']

		control.makeFile(dataPath)
		dbcon = database.connect(favouritesFile)
		dbcur = dbcon.cursor()
		dbcur.execute("CREATE TABLE IF NOT EXISTS %s (""id TEXT, ""items TEXT, ""UNIQUE(id)"");" % content)
		dbcur.execute("DELETE FROM %s WHERE id = '%s'" % (content, id))
		dbcur.execute("INSERT INTO %s Values (?, ?)" % content, (id, repr(item)))
		dbcur.connection.commit()
		dbcon.close()

		control.refresh()
		control.notification(title = title, message = 'Added to Favorites', icon = 'INFO', sound = notificationSound)
	except:
		return


def deleteFavourite(meta, content):
	try:
		meta = json.loads(meta)
		if 'title' in meta:
			title = meta['title']
		if 'tvshowtitle' in meta:
			title = meta['tvshowtitle']

		dbcon = database.connect(favouritesFile)
		dbcur = dbcon.cursor()
		dbcur.execute("DELETE FROM %s WHERE id = '%s'" % (content, meta['imdb']))
		dbcur.execute("DELETE FROM %s WHERE id = '%s'" % (content, meta['tvdb']))
		dbcur.execute("DELETE FROM %s WHERE id = '%s'" % (content, meta['tmdb']))
		dbcur.connection.commit()
		dbcon.close()

		control.refresh()
		control.notification(title = title, message = 'Removed From Favorites', icon = 'INFO', sound = notificationSound)
	except:
		return


def deleteProgress(meta, content):
	try:
		meta = json.loads(meta)

		dbcon = database.connect(progressFile)
		dbcur = dbcon.cursor()
		dbcur.execute("DELETE FROM %s WHERE id = '%s'" % (content, meta['imdb']))
		dbcur.execute("DELETE FROM %s WHERE id = '%s'" % (content, meta['tvdb']))
		dbcur.execute("DELETE FROM %s WHERE id = '%s'" % (content, meta['tmdb']))
		dbcur.connection.commit()
		dbcon.close()

		control.refresh()
	except:
		return
