# -*- coding: utf-8 -*-

import re
import xbmc

# LOGDEBUG = 0
# LOGNOTICE = 2
# LOGINFO = 1
# LOGWARNING = 3
# LOGERROR = 4
# LOGSEVERE = 5
# LOGFATAL = 6
# LOGNONE = 7

addon_debug_enabled = False

class Counter:
	def __init__(self):
		self.count = -1

	def increment(self, matchObject):
		self.count += 1
		return '{' + str(self.count) + '}'

def info(message, *arguments):
	log(message, arguments, xbmc.LOGNOTICE, 'INFO')

def error(message, *arguments):
	log(message, arguments, xbmc.LOGERROR, 'ERROR')

def notice(message, *arguments):
	log(message, arguments, xbmc.LOGNOTICE, 'NOTICE')

def debug(message, *arguments):
	log(message, arguments, xbmc.LOGDEBUG, 'DEBUG')
	# maybe write the debug log stuff also in a variable to be able to write
	# it when the exception gets handled in default.py or add a debug log setting to addon settings

def warn(message, *arguments):
	log(message, arguments, xbmc.LOGWARNING, 'WARNING')

def log(message, arguments, level, label):
	try:
		try:
			message = message.format(*arguments)
		except ValueError:
			c = Counter()
			message = re.compile('\\{\\}').sub(c.increment, message).format(*arguments)

		if not addon_debug_enabled:
			xbmc.log(message, level)
		else:
			xbmc.log(label + ' - ' + message, xbmc.LOGNOTICE)

	except:
		print 'Logging failed ' + label + ': "' + message + '" args: ' + str(arguments)
