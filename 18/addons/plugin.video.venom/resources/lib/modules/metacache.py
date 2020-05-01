# -*- coding: utf-8 -*-

import time

try:
	from sqlite3 import dbapi2 as database
except:
	from pysqlite2 import dbapi2 as database
from resources.lib.modules import control
from resources.lib.modules import log_utils


def fetch(items, lang = 'en', user=''):
	try:
		t2 = int(time.time())

		if not control.existsPath(control.dataPath):
			control.makeFile(control.dataPath)

		dbcon = database.connect(control.metacacheFile)
		dbcur = dbcon.cursor()
		dbcur.execute("CREATE TABLE IF NOT EXISTS meta (""imdb TEXT, ""tmdb TEXT, ""tvdb TEXT, ""lang TEXT, ""user TEXT, ""item TEXT, ""time TEXT, ""UNIQUE(imdb, tmdb, tvdb, lang, user)"");")
		dbcur.connection.commit()
	except:
		log_utils.error()
		try:
			dbcon.close()
		except:
			pass
		return items

	for i in range(0, len(items)):
		try:
			# First lookup by TVDb and IMDb, since there are some incorrect shows on Trakt that have the same IMDb ID, but different TVDb IDs (eg: Gotham, Supergirl).
			try:
				dbcur.execute("SELECT * FROM meta WHERE (imdb = '%s' and tvdb = '%s' and lang = '%s' and user = '%s' and not imdb = '0' and not tvdb = '0')" % (items[i].get('imdb', '0'), items[i].get('tvdb', '0'), lang, user))
				match = dbcur.fetchone()
				t1 = int(match[6])
			except:
				# Lookup both IMDb and TMDb for more accurate match.
				try:
					dbcur.execute("SELECT * FROM meta WHERE (imdb = '%s' and tmdb = '%s' and lang = '%s' and user = '%s' and not imdb = '0' and not tmdb = '0')" % (items[i].get('imdb', '0'), items[i].get('tmdb', '0'), lang, user))
					match = dbcur.fetchone()
					t1 = int(match[6])
				except:
					# Last resort single ID lookup.
					try:
						dbcur.execute("SELECT * FROM meta WHERE (imdb = '%s' and lang = '%s' and user = '%s' and not imdb = '0') OR (tmdb = '%s' and lang = '%s' and user = '%s' and not tmdb = '0') OR (tvdb = '%s' and lang = '%s' and user = '%s' and not tvdb = '0')" % (items[i].get('imdb', '0'), lang, user, items[i].get('tmdb', '0'), lang, user, items[i].get('tvdb', '0'), lang, user))
						match = dbcur.fetchone()
						t1 = int(match[6])
					except:
						pass

			if match is not None:
				update = (abs(t2 - t1) / 3600) >= 720
				if update is True:
					continue

				item = eval(match[5].encode('utf-8'))
				item = dict((k, v) for k, v in item.iteritems() if v != '0')

				items[i].update(item)
				items[i].update({'metacache': True})
		except:
			log_utils.error()
			pass

	try:
		dbcon.close()
	except:
		pass
	return items


def insert(meta):
	try:
		if not control.existsPath(control.dataPath):
			control.makeFile(control.dataPath)
		dbcon = database.connect(control.metacacheFile)
		dbcur = dbcon.cursor()
		dbcur.execute("CREATE TABLE IF NOT EXISTS meta (""imdb TEXT, ""tmdb TEXT, ""tvdb TEXT, ""lang TEXT, ""user TEXT, ""item TEXT, ""time TEXT, ""UNIQUE(imdb, tmdb, tvdb, lang, user)"");")
		t = int(time.time())
		for m in meta:
			if "user" not in m:
				m["user"] = ''
			if "lang" not in m:
				m["lang"] = 'en'
			i = repr(m['item'])
			try:
				dbcur.execute("INSERT OR REPLACE INTO meta Values (?, ?, ?, ?, ?, ?, ?)", (m.get('imdb', '0'), m.get('tmdb', '0'), m.get('tvdb', '0'), m['lang'], m['user'], i, t))
			except:
				pass
		dbcur.connection.commit()
	except:
		log_utils.error()
		pass
	try:
		dbcon.close()
	except:
		pass
	return


def local(items, link, poster, fanart):
	try:
		# dbcon = database.connect(control.metaFile())
		dbcon = database.connect(control.metacacheFile)
		dbcur = dbcon.cursor()
		args = [i['imdb'] for i in items]
		dbcur.execute('SELECT * FROM mv WHERE imdb IN (%s)' % ', '.join(list(map(lambda arg:  "'%s'" % arg, args))))
		data = dbcur.fetchall()
	except:
		return items

	for i in range(0, len(items)):
		try:
			item = items[i]
			match = [x for x in data if x[1] == item['imdb']][0]
			try:
				if poster in item and item[poster] != '0':
					raise Exception()
				if match[2] == '0':
					raise Exception()
				items[i].update({poster: link % ('300', '/%s.jpg' % match[2])})
			except:
				pass
			try:
				if fanart in item and item[fanart] != '0':
					raise Exception()
				if match[3] == '0':
					raise Exception()
				items[i].update({fanart: link % ('1280', '/%s.jpg' % match[3])})
			except:
				pass
		except:
			pass

	dbcon.close()
	return items