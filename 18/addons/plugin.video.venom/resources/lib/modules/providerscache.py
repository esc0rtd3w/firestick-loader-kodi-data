# -*- coding: utf-8 -*-

'''
	Venom Add-on
'''

import ast
import hashlib
import re
import time

from resources.lib.modules import control
from resources.lib.modules import log_utils

try:
	from sqlite3 import dbapi2 as db, OperationalError
except ImportError:
	from pysqlite2 import dbapi2 as db, OperationalError

cache_table = 'cache'
notificationSound = False if control.setting('notification.sound') == 'false' else True


def get(function, duration, *args):
	# type: (function, int, object) -> object or None
	"""
	Gets cached value for provided function with optional arguments, or executes and stores the result
	:param function: Function to be executed
	:param duration: Duration of validity of cache in hours
	:param args: Optional arguments for the provided function
	"""

	try:
		key = _hash_function(function, args)
		cache_result = cache_get(key)

		if cache_result:
			if _is_cache_valid(cache_result['date'], duration):
				return ast.literal_eval(cache_result['value'].encode('utf-8'))

		fresh_result = repr(function(*args))

		cache_insert(key, fresh_result)

		# Sometimes None is returned as a string instead of the special value None.
		invalid = False
		try:
			if not fresh_result:
				invalid = True
			elif fresh_result == 'None' or fresh_result == '' or fresh_result == '[]' or fresh_result == '{}':
				invalid = True
			elif len(fresh_result) == 0:
				invalid = True
		except: pass

		# If the cache is old, but we didn't get fresh result, return the old cache
		# if not fresh_result:
		if invalid:
			if cache_result:
				return ast.literal_eval(cache_result['value'].encode('utf-8'))
			else:
				return None

		return ast.literal_eval(fresh_result.encode('utf-8'))
	except:
		log_utils.error()
		return None


def cache_get(key):
	try:
		cursor = _get_connection_cursor()
		cursor.execute("SELECT * FROM %s WHERE key = ?" % cache_table, [key])
		results = cursor.fetchone()
		cursor.close()
		return results
	except:
		try:
			cursor.close()
		except:
			pass
		return None


def cache_insert(key, value):
	try:
		cursor = _get_connection_cursor()
		now = int(time.time())

		cursor.execute("CREATE TABLE IF NOT EXISTS %s (key TEXT, value TEXT, date INTEGER, UNIQUE(key))" % cache_table)

		update_result = cursor.execute("UPDATE %s SET value=?,date=? WHERE key=?" % cache_table, (value, now, key))

		if update_result.rowcount is 0:
			cursor.execute("INSERT INTO %s Values (?, ?, ?)" % cache_table, (key, value, now))

		cursor.connection.commit()
	except:
		log_utils.error()
		pass
	cursor.close()


def cache_clear_providers():
	cursor = _get_connection_cursor()
	for t in ['cache', 'rel_src', 'rel_url']:
		try:
			cursor.execute("DROP TABLE IF EXISTS %s" % t)
			cursor.execute("VACUUM")
			cursor.connection.commit()
		except:
			log_utils.error()
			pass
	cursor.close()


def _get_connection_cursor():
	conn = _get_connection()
	return conn.cursor()


def _get_connection():
	control.makeFile(control.dataPath)
	conn = db.connect(control.providercacheFile)
	conn.row_factory = _dict_factory
	return conn


def _dict_factory(cursor, row):
	d = {}
	for idx, col in enumerate(cursor.description):
		d[col[0]] = row[idx]
	return d


def _hash_function(function_instance, *args):
	return _get_function_name(function_instance) + _generate_md5(args)


def _get_function_name(function_instance):
	return re.sub('.+\smethod\s|.+function\s|\sat\s.+|\sof\s.+', '', repr(function_instance))


def _generate_md5(*args):
	md5_hash = hashlib.md5()
	try:
		[md5_hash.update(str(arg)) for arg in args]
	except:
		[md5_hash.update(str(arg).encode('utf-8')) for arg in args]
	return str(md5_hash.hexdigest())


def _is_cache_valid(cached_time, cache_timeout):
	now = int(time.time())
	diff = now - cached_time
	return (cache_timeout * 3600) > diff

