import os
import sys
import re
import string
import unicodedata
import xbmc
import xbmcgui
import xbmcvfs


class VFSClass:
	def __init__(self, root='/', debug=False):
		self.debug = debug
		self.root = root
	
	def _resolve_path(self, path):
		return path.replace('/', os.sep)	

	def confirm(self, msg='', msg2='', msg3=''):
		dialog = xbmcgui.Dialog()
		return dialog.yesno(msg, msg2, msg3)

	def open(self, path, mode='r'):
		try:
			return xbmcvfs.File(path, mode)
		except Exception, e:
			xbmc.log('******** VFS error: %s' % e)
			return False

	def read_file(self, path, soup=False, json=False, mode=''):
		#try:
		if mode=='b':
			file = self.open(path, 'rb')
		else:
			file = self.open(path, 'r')
		content=file.read()
		file.close()
		if soup:
			from BeautifulSoup import BeautifulSoup, Tag, NavigableString
			soup = BeautifulSoup(content)
			return soup
		elif json:
			try: 
				import simplejson as json
			except ImportError: 
				import json
			return json.loads(content)
		else:
			return content
		#except IOError, e:
		#	xbmc.log('******** VFS error: %s' % e)
		#	return None

	def write_file(self, path, content, mode='w', json=False):
		try:
			if json: 
				import json
				content = json.dumps(content)

			if mode=='b':
				file = self.open(path, 'wb')
			else:
				file = self.open(path, 'w')
			file.write(content)
			file.close()
			return True
		except IOError, e:
			xbmc.log('******** VFS error: %s' % e)
			return False
	
	def clean_file_name(self, filename):
		filename = unicode(filename)
		validFilenameChars = "-_.() %s%s" % (string.ascii_letters, string.digits)
		cleanedFilename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore')
		return ''.join(c for c in cleanedFilename if c in validFilenameChars)
		
	def touch(self, path):
		try:
			if self.exists(path):
				self.open(path, 'r')
				return True
			else:
				self.open(path, 'w')
				return True
		except Exception, e:
			xbmc.log('******** VFS error: %s' % e)
			return False


	def get_stat(self, path):
		return xbmcvfs.Stat(path)

	def get_size(self, path):
		return xbmcvfs.Stat(path).st_size()

	def get_mtime(self, path):
		return xbmcvfs.Stat(path).st_mtime()
	
	def get_ctime(self, path):
		return xbmcvfs.Stat(path).st_ctime()
	
	def get_atime(self, path):
		return xbmcvfs.Stat(path).st_atime()
	
	def path_parts(self, path):
		from urlparse import urlparse
		temp = urlparse(path)
		filename, file_extension = os.path.splitext(temp[2])
		result = {"scheme": temp[0], "host": temp[1], "path": filename, "extension": file_extension.replace('.', '')}
		return result
		
	def exists(self, path):
		return xbmcvfs.exists(path)

	def ls(self, path, pattern=None, inlcude_path=False):
		try:
			if pattern:
				s = re.compile(pattern)
				folders = []
				files = []
				temp = xbmcvfs.listdir(path)
				for test in temp[0]:
					if s.search(str(test)):
						if inlcude_path: test = self.join(path, test)
						folders.append(test)
				for test in temp[1]:
					if s.search(str(test)):
						if inlcude_path: test = self.join(path, test)
						files.append(test)
				return [folders, files]
			else:
				return xbmcvfs.listdir(path)
		except Exception, e:
			xbmc.log('******** VFS error: %s' % e)
			return False

	def mkdir(self, path, recursive=False):
		if self.exists(path):
			if self.debug:
				xbmc.log('******** VFS mkdir notice: %s exists' % path)
			return False
		if recursive:
			try:
				return xbmcvfs.mkdirs(path)
			except Exception, e:
				xbmc.log('******** VFS error: %s' % e)
				return False
		else:
			try:
				return xbmcvfs.mkdir(path)
			except Exception, e:
				xbmc.log('******** VFS error: %s' % e)
				return False

	def rmdir(self, path, quiet=False):
		if not self.exists(path):
			if self.debug:
				xbmc.log('******** VFS rmdir notice: %s does not exist' % path)
			return False
		if not quiet:
			msg = 'Remove Directory'
			msg2 = 'Please confirm directory removal!'
			if not self.confirm(msg, msg2, path): return False
		try:		
			xbmcvfs.rmdir(path)
		except Exception, e:
			xbmc.log('******** VFS error: %s' % e)

	def rm(self, path, quiet=False, recursive=False):
		if not self.exists(path):
			if self.debug:
				xbmc.log('******** VFS rmdir notice: %s does not exist' % path)
			return False
		if not quiet:
			msg = 'Confirmation'
			msg2 = 'Please confirm directory removal!'
			if not self.confirm(msg, msg2, path): return False

		if not recursive:
			try:
				xbmcvfs.delete(path)
			except Exception, e:
				xbmc.log('******** VFS error: %s' % e)
		else:
			dirs,files = self.ls(path)
			for f in files:
				rm = os.path.join(xbmc.translatePath(path), f)
				try:
					xbmcvfs.delete(rm)
				except Exception, e:
					xbmc.log('******** VFS error: %s' % e)
			for d in dirs:
				subdir = os.path.join(xbmc.translatePath(path), d)
				self.rm(subdir, quiet=True, recursive=True)
			try:			
				xbmcvfs.rmdir(path)
			except Exception, e:
				xbmc.log('******** VFS error: %s' % e)
	
	def rename(self, src, dest, quiet=False):
		if not quiet:
			msg = 'Confirmation'
			msg2 = 'Please confirm rename file!'
			if not self.confirm(msg, msg2, src): return False
		xbmcvfs.rename(src, dest)
		
	def cp(self, src, dest):
		return xbmcvfs.copy(src, dest)

	def mv(self, src, dest):
		cp = self.cp(src, dest)
		if cp:
			rm = self.rm(src, quiet=True)
		else: return False
		return rm
	
	def translate_path(self, path):
		return xbmc.translatePath( path )

	def join(self, path, filename, preserve=False):
		path = path.replace('/', os.sep)
		if not preserve:
			translatedpath = os.path.join(xbmc.translatePath( path ), ''+filename+'')
		else:
			translatedpath = os.path.join(path, ''+filename+'')
		return translatedpath
