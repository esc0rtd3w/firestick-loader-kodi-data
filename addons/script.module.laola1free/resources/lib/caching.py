# -*- coding: utf-8 -*-

import os
import string
import json
import xbmc
import xbmcvfs
import logger

class CacheManager:
	def __init__(self, path):
		if not os.path.exists(path):
			os.makedirs(path)
		self.path = path

	def clear(self):
		for file in os.listdir(self.path):
			filepath = os.path.join(self.path, file)
			try:
				if os.path.isfile(filepath):
					os.unlink(filepath)
			except Exception, e:
				logger.warn('Failed to clear cache {}', e)

	def get_filepath(self, idParts):
		joined = '-'.join(str(e) for e in idParts)
		if joined:
			joined = '-' + joined
		return xbmc.validatePath(self.path + '/cache' + joined + '.json')

	def load(self, idParts):
		idPartsNew = idParts[:-1]
		filepath = self.get_filepath(idPartsNew)

		while not os.path.isfile(filepath) and len(idPartsNew) > 0:
			del idPartsNew[-1]
			filepath = self.get_filepath(idPartsNew)

		if not os.path.isfile(filepath):
			return None

		logger.debug('Read from "{}"', filepath)

		file = xbmcvfs.File(filepath, 'r')
		obj = json.load(file)
		file.close()

		return self.get_child(obj, idParts[len(idPartsNew):])

	def get_child(self, list, idParts):
		logger.debug("id: {}, list: {}", idParts, list)

		if len(list) == 0:
			return None

		parent = list[idParts[0]]

		if len(idParts) == 1:
			return parent

		if parent and 'children' in parent:
			return self.get_child(parent['children'], idParts[1:])

		return None


	def store(self, obj, parentIdParts = []):
		filepath = self.get_filepath(parentIdParts)

		file = xbmcvfs.File(filepath, 'w')
		json.dump(obj, file)
		file.close()
