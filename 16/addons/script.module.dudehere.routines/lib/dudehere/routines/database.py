import sys
import re
import xbmc
import xbmcaddon
import os
from dudehere.routines import *
import plugin
IGNORE_UNIQUE_ERRORS = True
from vfs import VFSClass
from threading import Lock

class DatabaseClass:
	__connected = False
	lock = Lock()
	def __init__(self, quiet=False, version=1):
		self.quiet=quiet
		self._unique_str = 'column (.)+ is not unique$'

	def commit(self, quiet=False):
		if self.db_type == 'sqlite' and quiet is False:
			plugin.log("Commiting to %s" % self.db_file, LOG_LEVEL.VERBOSE)
		elif quiet is False:
			plugin.log("Commiting to %s on %s" % (self.dbname, self.host), LOG_LEVEL.VERBOSE)
		try:
			self.lock.acquire(True)	
			self.DBH.commit()
		except:
			pass
		finally:
			self.lock.release()
			

	def disconnect(self):
		if self.db_type == 'sqlite':
			#plugin.log("Disconnecting from %s" % self.db_file, LOG_LEVEL.VERBOSE)
			self.DBC.close()
		else:
			#plugin.log("Disconnecting from %s on %s" % (self.dbname, self.host), LOG_LEVEL.VERBOSE)
			self.DBC.close()
		self.__connected = False

	def connect(self, quiet=False):
		if self.__connected is False: 
			self._connect(quiet=quiet)

	def check_version(self, previous, current):
		if not re.search('\d+\.\d+\.\d+', str(previous)): return True
		p = previous.split('.')
		c = current.split('.')
		if int(p[0]) < int(c[0]): return True
		if int(p[1]) < int(c[1]): return True
		if int(p[2]) < int(c[2]): return True
		return False
	
	def do_init(self):
		if plugin.get_setting(self.init_flag) != 'true': return True
		current = 1 if (plugin.get_setting(self.version_flag) == 'false' or plugin.get_setting(self.version_flag) == '') else int(plugin.get_setting(self.version_flag))
		if self.verify_version and current < self.db_version: return True
		return False
	
	def dict_factory(self, cursor, row):
		d = {}
		for idx, col in enumerate(cursor.description):
			d[col[0]] = row[idx]
		return d

	def query(self, SQL, data=None,force_double_array=False, silent=False):
		try:
			self.lock.acquire(True)
			if data:
				self.DBC.execute(SQL, data)
			else:
				self.DBC.execute(SQL)
			rows = self.DBC.fetchall()
			if(len(rows)==1 and not force_double_array):
				return rows[0]
			else:
				return rows
		except Exception, e:
			if 'no such table: version' not in str(e).lower():
				plugin.raise_error("Database error", e)
			plugin.log("Database query error: %s" % e)
			plugin.log("Database query error: %s" % SQL)
			return []
		finally:
			self.lock.release()

	def query_assoc(self, SQL, data=None, force_double_array=False, silent=False):
		try:
			self.lock.acquire(True)
			self.DBH.row_factory = self.dict_factory
			cur = self.DBH.cursor()
			if data:
				cur.execute(SQL, data)
			else:
				cur.execute(SQL)
			rows = cur.fetchall()
			cur.close()
			if(len(rows)==1 and not force_double_array):
				return rows[0]
			else:
				return rows
		except Exception, e:
			if 'no such table: version' not in str(e).lower():
				plugin.raise_error("Database error", e)
			plugin.log("Database query error: %s" % e)
			plugin.log("Database query error: %s" % SQL)
			return []
		finally:
			self.lock.release()
		
	def execute(self, SQL, data=[], silent=False):
		if SQL.startswith('REPLACE INTO'): SQL = 'INSERT OR ' + SQL
		try:
			self.lock.acquire(True)
			if data:
				self.DBC.execute(SQL, data)
			else:
				self.DBC.execute(SQL)
			try:
				self.lastrowid = self.DBC.lastrowid
			except:
				self.lastrowid = None
		except Exception, e:
			if IGNORE_UNIQUE_ERRORS and re.match(self._unique_str, str(e)):
				if silent is False:
					plugin.raise_error("Database error", e)
				plugin.log("Database execute error: %s" % e)
				plugin.log("Database execute error: %s" % SQL)
		finally:
			self.lock.release()

	def execute_many(self, SQL, data, silent=False):
		if SQL.startswith('REPLACE INTO'): SQL = 'INSERT OR ' + SQL
		try:
			self.lock.acquire(True)
			self.DBC.executemany(SQL, data)
		except Exception, e:
			if IGNORE_UNIQUE_ERRORS and re.match(self._unique_str, str(e)):
				if silent is False:
					plugin.raise_error("Database error", e)
				plugin.log("Database execute error: %s" % e)
				plugin.log("Database execute error: %s" % SQL)
		finally:
			self.lock.release()
	
	def run_script(self, sql_file, commit=True):
		if VFSClass().exists(sql_file):
			full_sql = VFSClass().read_file(sql_file)
			sql_stmts = full_sql.split(';')
			for SQL in sql_stmts:
				if SQL is not None and len(SQL.strip()) > 0:
					self.execute(SQL)
					print SQL
			if commit: self.commit()
			return True
		else:
			return False
				
class SQLiteDatabase(DatabaseClass):
	def __init__(self, db_file='', version=1, quiet=False, init_flag='database_sqlite_init', version_flag='database_sqlite_version', connect=True, check_version=True):
		self.quiet=quiet
		self._unique_str = 'column (.)+ is not unique$'
		self.db_type = 'sqlite'
		self.lastrowid = None
		self.db_file = db_file
		self.init_flag = init_flag
		self.version_flag = version_flag
		self.db_version = version
		self.verify_version = check_version
		if connect:
			self._connect()
			

	def _connect(self, quiet=False):
		vfs = VFSClass()
		if not self.quiet and not quiet:
			plugin.log("Connecting to " + self.db_file, LOG_LEVEL.VERBOSE)
		try:
			from sqlite3 import dbapi2 as database
			if not self.quiet and not quiet:
				plugin.log("%s loading sqlite3 as DB engine" % ADDON_NAME)
		except:
			from pysqlite2 import dbapi2 as database
			if not self.quiet and not quiet:
				plugin.log("%s loading pysqlite2 as DB engine"  % ADDON_NAME)
		if not self.quiet and not quiet:
			plugin.log("Connecting to SQLite on: " + self.db_file)
		directory = os.path.dirname(self.db_file)
		if not vfs.exists(directory): vfs.mkdir(directory)
		self.DBH = database.connect(self.db_file, check_same_thread=False)
		try:
			self.DBC = self.DBH.cursor()
		except Exception, e:
			plugin.raise_error("SqlLite Error", e)
			sys.exit()
		self.__connected = True
		'''if plugin.get_setting(self.init_flag) != 'true' or (self.check_version(plugin.get_setting('version'), VERSION) and self.verify_version):
			self._initialize()
		'''
		if self.do_init(): self._initialize()
		
		
class MySQLDatabase(DatabaseClass):
	def __init__(self, host, dbname, username, password, port, version=1, quiet=False, init_flag='database_mysql_init', version_flag='database_mysql_version', connect=True, check_version=True):
		self.quiet=quiet
		self._unique_str = '1062: Duplicate entry'
		self.db_type = 'mysql'
		self.lastrowid = None
		self.host = host
		self.dbname = dbname
		self.username=username
		self.password = password
		self.port = port
		self.init_flag = init_flag
		self.version_flag = version_flag
		self.db_version = version
		self.verify_version = check_version
		if connect:
			self._connect()

	def check_connection(self):
		try:
			self.lock.acquire(True)
			self.DBH.ping(reconnect=True, attempts=1, delay=0)
		except Exception, e:
			plugin.log("Failed Test")
			plugin.log(e)
		finally:
			self.lock.release()

	def _connect(self, quiet=False):
		try:	
			import mysql.connector as database
			if not self.quiet and not quiet:
				plugin.log("%s loading mysql.connector as DB engine" % ADDON_NAME)
			dsn = {
					"database": self.dbname,
					"host": self.host,
					"port": int(self.port),
					"user": str(self.username),
					"password": str(self.password),
					"buffered": True
			}
			self.DBH = database.connect(**dsn)
		except Exception, e:
			plugin.log('****** %s SQL ERROR: %s' % (ADDON_NAME, e))
			plugin.raise_error("MySQL Error", e)
			sys.exit()
		self.DBC = self.DBH.cursor()
		self.__connected = True
		if self.do_init(): self._initialize()
	
	def execute(self, SQL, data=[], silent=False):
		self.check_connection()
		try:
			self.lock.acquire(True)
			if data:
				SQL = SQL.replace('?', '%s')
				self.DBC.execute(SQL, data)
			else:
				self.DBC.execute(SQL)
			try:
				self.lastrowid = self.DBC.lastrowid
			except:
				self.lastrowid = None
		except Exception, e:
			if IGNORE_UNIQUE_ERRORS and re.match(self._unique_str, str(e)):
				if silent is False:
					plugin.raise_error("Database error", e)
				plugin.log("Database execute error: %s" % e)
				plugin.log("Database execute error: %s" % SQL)
		finally:
			self.lock.release()		

	def execute_many(self, SQL, data, silent=False):
		self.check_connection()
		try:
			self.lock.acquire(True)
			SQL = SQL.replace('?', '%s')
			self.DBC.executemany(SQL, data)
		except Exception, e:
			if IGNORE_UNIQUE_ERRORS and re.match(self._unique_str, str(e)):
				if silent is False:
					plugin.raise_error("Database error", e)
				plugin.log("Database execute error: %s" % e)
				plugin.log("Database execute error: %s" % SQL)
		finally:
			self.lock.release()		

	def query(self, SQL, data=None, force_double_array=False, silent=False):
		self.check_connection()
		try:
			self.lock.acquire(True)
			if data:
				SQL = SQL.replace('?', '%s')
				self.DBC.execute(SQL, data)
			else:
				self.DBC.execute(SQL)
			rows = self.DBC.fetchall()
			if(len(rows)==1 and not force_double_array):
				return rows[0]
			else:
				return rows
		except Exception, e:
			error_msg = "Database query error: %s" % e
			if silent is False:
				plugin.raise_error("Database error", e)
			plugin.log(error_msg)
			plugin.log("Database query error: %s" % SQL)
			plugin.log(data)
			return []
		finally:
			self.lock.release()
		
	def query_assoc(self, SQL, data=None, force_double_array=False, silent=False):
		self.check_connection()
		try:
			self.lock.acquire(True)
			if data:
				SQL = SQL.replace('?', '%s')
				self.DBC.execute(SQL, data)
			else:
				self.DBC.execute(SQL)
			rows = self.DBC.fetchall()
			if(len(rows)==1 and not force_double_array):
				d = {}
				for idx, col in enumerate(self.DBC.column_names):
					d[col] = rows[0][idx]
				return d
			else:
				set = []
				for row in rows:
					d = {}
					for idx, col in enumerate(self.DBC.column_names):
						d[col] = row[idx]
					set.append(d)
				return set
		except Exception, e:
			error_msg = "Database query error: %s" % e
			if silent is False:
				plugin.raise_error("Database error", e)
			plugin.log(error_msg)
			plugin.log("Database query error: %s" % SQL)
			plugin.log(data)
			return []
		finally:
			self.lock.release()