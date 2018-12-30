"""
    tknorris shared module
    Copyright (C) 2016 tknorris

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import functools
import log_utils
import xbmcaddon
import xbmc
import xbmcvfs
import time
import cPickle as pickle
import hashlib
import os
import shutil
import kodi
import ast
import re

try:
    from sqlite3 import dbapi2 as db, OperationalError
except ImportError:
    from pysqlite2 import dbapi2 as db, OperationalError

logger = log_utils.Logger.get_logger(__name__)
logger.disable()
addonInfo = xbmcaddon.Addon().getAddonInfo

try:
    cache_path = kodi.translate_path(os.path.join(kodi.get_profile(), 'cache'))
    if not os.path.exists(cache_path):
        os.makedirs(cache_path)
except Exception as e:
    logger.log('Failed to create cache: %s: %s' % (cache_path, e), log_utils.LOGWARNING)
    
cache_enabled = kodi.get_setting('use_cache') == 'true'
    
def reset_cache():
    try:
        shutil.rmtree(cache_path)
        return True
    except Exception as e:
        logger.log('Failed to Reset Cache: %s' % (e), log_utils.LOGWARNING)
        return False
    
def _get_func(name, args=None, kwargs=None, cache_limit=1):
    if not cache_enabled: return False, None
    now = time.time()
    max_age = now - (cache_limit * 60 * 60)
    if args is None: args = []
    if kwargs is None: kwargs = {}
    full_path = os.path.join(cache_path, _get_filename(name, args, kwargs))
    if os.path.exists(full_path):
        mtime = os.path.getmtime(full_path)
        if mtime >= max_age:
            with open(full_path, 'r') as f:
                pickled_result = f.read()
            # logger.log('Returning cached result: |%s|%s|%s| - modtime: %s max_age: %s age: %ss' % (name, args, kwargs, mtime, max_age, now - mtime), log_utils.LOGDEBUG)
            return True, pickle.loads(pickled_result)
    
    return False, None
    
def _save_func(name, args=None, kwargs=None, result=None):
    try:
        if args is None: args = []
        if kwargs is None: kwargs = {}
        pickled_result = pickle.dumps(result)
        full_path = os.path.join(cache_path, _get_filename(name, args, kwargs))
        with open(full_path, 'w') as f:
            f.write(pickled_result)
    except Exception as e:
        logger.log('Failure during cache write: %s' % (e), log_utils.LOGWARNING)

def _get_filename(name, args, kwargs):
    arg_hash = hashlib.md5(name).hexdigest() + hashlib.md5(str(args)).hexdigest() + hashlib.md5(str(kwargs)).hexdigest()
    return arg_hash

def cache_method(cache_limit):
    def wrap(func):
        @functools.wraps(func)
        def memoizer(*args, **kwargs):
            if args:
                klass, real_args = args[0], args[1:]
                full_name = '%s.%s.%s' % (klass.__module__, klass.__class__.__name__, func.__name__)
            else:
                full_name = func.__name__
                real_args = args
            in_cache, result = _get_func(full_name, real_args, kwargs, cache_limit=cache_limit)
            if in_cache:
                logger.log('Using method cache for: |%s|%s|%s| -> |%d|' % (full_name, args, kwargs, len(pickle.dumps(result))), log_utils.LOGDEBUG)
                return result
            else:
                logger.log('Calling cached method: |%s|%s|%s|' % (full_name, args, kwargs), log_utils.LOGDEBUG)
                result = func(*args, **kwargs)
                _save_func(full_name, real_args, kwargs, result)
                return result
        return memoizer
    return wrap

# do not use this with instance methods the self parameter will cause args to never match
def cache_function(cache_limit):
    def wrap(func):
        @functools.wraps(func)
        def memoizer(*args, **kwargs):
            name = func.__name__
            in_cache, result = _get_func(name, args, kwargs, cache_limit=cache_limit)
            if in_cache:
                logger.log('Using function cache for: |%s|%s|%s| -> |%d|' % (name, args, kwargs, len(pickle.dumps(result))), log_utils.LOGDEBUG)
                return result
            else:
                logger.log('Calling cached function: |%s|%s|%s|' % (name, args, kwargs), log_utils.LOGDEBUG)
                result = func(*args, **kwargs)
                _save_func(name, args, kwargs, result)
                return result
        return memoizer
    return wrap

"""
This module is used to get/set cache for every action done in the system
"""

cache_table = 'cache'


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
        if not fresh_result:
            # If the cache is old, but we didn't get fresh result, return the old cache
            if cache_result:
                return cache_result
            return None

        cache_insert(key, fresh_result)
        return ast.literal_eval(fresh_result.encode('utf-8'))
    except Exception:
        return None

def timeout(function, *args):
    try:
        key = _hash_function(function, args)
        result = cache_get(key)
        return int(result['date'])
    except Exception:
        return None


def cache_get(key):
    # type: (str, str) -> dict or None
    try:
        cursor = _get_connection_cursor()
        cursor.execute("SELECT * FROM %s WHERE key = ?" % cache_table, [key])
        return cursor.fetchone()
    except OperationalError:
        return None


def cache_insert(key, value):
    # type: (str, str) -> None
    cursor = _get_connection_cursor()
    now = int(time.time())
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS %s (key TEXT, value TEXT, date INTEGER, UNIQUE(key))"
        % cache_table
    )
    update_result = cursor.execute(
        "UPDATE %s SET value=?,date=? WHERE key=?"
        % cache_table, (value, now, key))

    if update_result.rowcount is 0:
        cursor.execute(
            "INSERT INTO %s Values (?, ?, ?)"
            % cache_table, (key, value, now)
        )

    cursor.connection.commit()


def cache_clear():
    try:
        cursor = _get_connection_cursor()

        for t in [cache_table, 'rel_list', 'rel_lib']:
            try:
                cursor.execute("DROP TABLE IF EXISTS %s" % t)
                cursor.execute("VACUUM")
                cursor.commit()
            except:
                pass
    except:
        pass


def _get_connection_cursor():
    conn = _get_connection()
    return conn.cursor()


def _get_connection():
    xbmcvfs.mkdir(xbmc.translatePath(addonInfo('profile')).decode('utf-8'))
    conn = db.connect(os.path.join(xbmc.translatePath(addonInfo('profile')).decode('utf-8'), 'cache.db'))
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
    [md5_hash.update(str(arg)) for arg in args]
    return str(md5_hash.hexdigest())


def _is_cache_valid(cached_time, cache_timeout):
    now = int(time.time())
    diff = now - cached_time
    return (cache_timeout * 3600) > diff