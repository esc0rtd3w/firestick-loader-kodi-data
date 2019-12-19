# -*- coding: utf-8 -*-

import os
import hashlib
import xbmc
import xbmcvfs
import xbmcgui
import xbmcaddon
import threading

try:
	from sqlite3 import dbapi2 as database
except:
	from pysqlite2 import dbapi2 as database

DatabaseInstances = {}
DatabaseLocks = {}
DatabaseLocksCustom = {}


class Database(object):
	Timeout = 20
	Extension = '.db'


	def __init__(self, name, addon = None, default = None, path = None, connect = True):
		try:
			self.mAddon = addon
			self.mDatabase = None
			if name is None: name = hashlib.sha256(path).hexdigest().upper()
			global DatabaseLocks
			if not name in DatabaseLocks:
				DatabaseLocks[name] = threading.Lock()
			self.mLock = DatabaseLocks[name]
			global DatabaseLocksCustom
			if not name in DatabaseLocksCustom:
				DatabaseLocksCustom[name] = threading.Lock()
			self.mLockCustom = DatabaseLocksCustom[name]
			if path is None:
				if not name.endswith(Database.Extension): name += Database.Extension
				self.mPath = os.path.join(xbmc.translatePath(self._addon().getAddonInfo('profile').decode('utf-8')), name)
				if default and not xbmcvfs.exists(self.mPath): xbmcvfs.copy(os.path.join(default, name), self.mPath)
			else:
				if not path.endswith(Database.Extension): path += Database.Extension
				self.mPath = path
			if connect: self._connect()
		except Exception as error:
			xbmc.log('Venom ERROR [Database]: ' + str(error), xbmc.LOGERROR)


	def __del__(self):
		self._close()


	@classmethod
	def instance(self, name, default = None, create = None):
		global DatabaseInstances
		if not name in DatabaseInstances:
			DatabaseInstances[name] = Database(name = name, default = default)
			if not create is None: DatabaseInstances[name]._create(create)
		return DatabaseInstances[name]


	def _lock(self):
		self.mLockCustom.acquire()


	def _unlock(self):
		if self.mLockCustom.locked():
			self.mLockCustom.release()


	def _connect(self):
		try:
			# When the addon is launched for the first time after installation, an error occurs, since the addon userdata directory does not exist yet and the database file is written to that directory.
			# If the directory does not exist yet, create it.
			xbmcvfs.mkdirs(os.path.dirname(os.path.abspath(self.mPath)))
			# SQLite does not allow database objects to be used from multiple threads. Explicitly allow multi threading.
			try: self.mConnection = database.connect(self.mPath, check_same_thread = False, timeout = Database.Timeout)
			except: self.mConnection = database.connect(self.mPath, timeout = Database.Timeout)
			self.mDatabase = self.mConnection.cursor()
			self._initialize()
			return True
		except:
			return False


	def _addon(self):
		if self.mAddon:
			return xbmcaddon.Addon(self.mAddon)
		else:
			return xbmcaddon.Addon()


	def _initialize(self):
		pass


	def _list(self, items):
		if not type(items) in [list, tuple]:
			items = [items]
		return items


	def _close(self):
		try: self.mConnection.close()
		except: pass


	def _null(self):
		return 'NULL'


	def _commit(self):
		try:
			self.mConnection.commit()
			return True
		except:
			return False


	def _execute(self, query, parameters = None):
		try:
			self.mLock.acquire()
			if parameters is None: self.mDatabase.execute(query)
			else: self.mDatabase.execute(query, parameters)
			return True
		except Exception as error:
			xbmc.log('Venom ERROR [Database]: ' + str(error), xbmc.LOGERROR)
			return False
		finally:
			self.mLock.release()


	# query must contain %s for table name.
	# tables can be None, table name, or list of tables names.
	# If tables is None, will retrieve all tables in the database.
	def _executeAll(self, query, tables = None, parameters = None):
		result = True
		if tables is None:
			tables = self._tables()
		tables = self._list(tables)
		for table in tables:
			result = result and self._execute(query % table, parameters = parameters)
		return result


	def _tables(self):
		return self._selectValues('SELECT name FROM sqlite_master WHERE type IS "table"')


	def _create(self, query, parameters = None, commit = True):
		result = self._execute(query, parameters = parameters)
		if result and commit:
			result = self._commit()
		return result


	def _createAll(self, query, tables, parameters = None, commit = True):
		result = self._executeAll(query, tables, parameters = parameters)
		if result and commit:
			result = self._commit()
		return result


	# Retrieves a list of rows.
	# Each row is a tuple with all the return values.
	# Eg: [(row1value1, row1value2), (row2value1, row2value2)]
	def _select(self, query, parameters = None):
		self._execute(query, parameters = parameters)
		return self.mDatabase.fetchall()


	# Retrieves a single row.
	# Each row is a tuple with all the return values.
	# Eg: (row1value1, row1value2)
	def _selectSingle(self, query, parameters = None):
		self._execute(query, parameters = parameters)
		return self.mDatabase.fetchone()


	# Retrieves a list of single values from rows.
	# Eg: [row1value1, row1value2]
	def _selectValues(self, query, parameters = None):
		try:
			result = self._select(query, parameters = parameters)
			return [i[0] for i in result]
		except:
			return []


	# Retrieves a signle value from a single row.
	# Eg: row1value1
	def _selectValue(self, query, parameters = None):
		try:
			return self._selectSingle(query, parameters = parameters)[0]
		except:
			return None


	# Checks if the value exists, such as an ID.
	def _exists(self, query, parameters = None):
		return len(self._select(query, parameters = parameters)) > 0


	def _insert(self, query, parameters = None, commit = True):
		result = self._execute(query, parameters = parameters)
		if result and commit:
			result = self._commit()
		return result


	def _update(self, query, parameters = None, commit = True):
		result = self._execute(query, parameters = parameters)
		if result and commit:
			result = self._commit()
		return result


	# Deletes specific row in table.
	# If table is none, assumes it was already set in the query
	def _delete(self, query, table = None, parameters = None, commit = True):
		if not table is None:
			query = query % table
		result = self._execute(query, parameters = parameters)
		if result and commit:
			result = self._commit()
		return result


	# Deletes all rows in table.
	# tables can be None, table name, or list of tables names.
	# If tables is None, deletes all rows in all tables.
	def _deleteAll(self, tables = None, parameters = None, commit = True):
		result = self._executeAll('DELETE FROM %s;', tables, parameters = parameters)
		if result and commit:
			result = self._commit()
		return result


	# Drops single table.
	def _drop(self, table, parameters = None, commit = True):
		result = self._execute('DROP TABLE IF EXISTS %s;' % table, parameters = parameters)
		if result and commit:
			result = self._commit()
		return result


	# Drops all tables.
	def _dropAll(self, parameters = None, commit = True):
		result = self._executeAll('DROP TABLE IF EXISTS %s;', parameters = parameters)
		if result and commit:
			result = self._commit()
		return result


	# tables can be None, table name, or list of tables names.
	# If tables is provided, only clears the specific table(s), otherwise clears all tables.
	def clear(self, tables = None, confirm = False):
		title = self._addon().getAddonInfo('name') + ' - ' + self._addon().getLocalizedString(33013).encode('utf-8')
		message = self._addon().getLocalizedString(33042).encode('utf-8')
		if not confirm or xbmcgui.Dialog().yesno(title, message):
			self._deleteAll(tables)
			if confirm:
				message = self._addon().getLocalizedString(33043).encode('utf-8')
				icon = xbmc.translatePath(xbmcaddon.Addon('script.gaia.resources').getAddonInfo('path').decode('utf-8'))
				icon = os.path.join(icon, 'resources', 'media', 'notifications', 'information.png')
				xbmcgui.Dialog().notification(title, message, icon = icon)
