# -*- coding: utf-8 -*-

import xbmc, xbmcgui, xbmcaddon, xbmcvfs, xbmcgui
import time, datetime, calendar
import urlparse, urllib

import numbers
import json
import subprocess
import webbrowser
import sys,os,copy
import stat
import uuid
import hashlib
import shutil
import imp
import pkgutil
import re
import platform
import zipfile
import threading

from resources.lib.modules import control
from resources.lib.externals import pytz


###################################################################
#---Translation
###################################################################
class Translation(object):

	@classmethod
	def string(self, id, utf8 = True, system = False):
		if isinstance(id, (int, long)):
			# Needs ID when called from RunScript(vpn.py)
			if system: result = xbmc.getLocalizedString(id)
			else: result = xbmcaddon.Addon(System.VenomAddon).getLocalizedString(id)
		else:
			try: result = str(id)
			except: result = id
		if utf8:
			try:
				if not '•' in result: result = Converter.unicode(string = result, umlaut = True).encode('utf-8')
			except:
				result = Converter.unicode(string = result, umlaut = True).encode('utf-8')
		return result


# def formatColorInitialize(customize, type, default):
	# if customize:
		# type = 'FFA0C12C'
		# color = 'interface.color.' + type
		# try: return re.search('\\[.*\\](.*)\\[.*\\]', color, re.IGNORECASE).group(1)
		# except: return ''
	# else:
		# return default

###################################################################
#---Format
###################################################################
class Format(object):

	# ColorCustomize = tools.Settings.getBoolean('interface.color.enabled')
	ColorCustomize = False
	ColorNone = None
	ColorPrimary = 'FFA0C12C'
	ColorPrimary = 'FFFF00000'
	ColorSecondary = 'FF3C7DBF'
	ColorOrion = 'FF637385'
	ColorMain = 'FF2396FF'
	ColorAlternative = 'FF004F98'
	ColorSpecial = 'FF6C3483'
	ColorUltra = 'FF00A177'
	ColorExcellent = 'FF1E8449'
	ColorGood = 'FF668D2E'
	ColorMedium = 'FFB7950B'
	ColorPoor = 'FFBA4A00'
	ColorBad = 'FF922B21'
	ColorVenom1 = 'FFA0C12C'
	ColorVenom2 = 'FF3C7DBF'
	ColorWhite = 'FFFFFFFF'
	ColorBlack = 'FF000000'
	ColorDisabled = 'FF888888'

	Gradients = {}

	FontNewline = '[CR]'
	FontSeparator = ' • '
	FontPassword = '••••••••••'
	FontDivider = ' - '
	FontSplitInterval = 50

	@classmethod
	def settingsColorUpdate(self, type):
		setting = 'interface.color.' + type
		color = Dialog.input(title = 35235, type = Dialog.InputAlphabetic, default = self.settingsColor(Settings.getString(setting)))
		if self.colorIsHex(color):
			while len(color) < 8: color = 'F' + color
			if len(color) > 8: color = color[:8]
			Settings.set(setting, self.fontColor(color, color))
		else:
			control.notification(title = 35235, message = 35236, icon = 'ERROR')

		# If this option is disabled and the user enables it and immediately afterwards selects a color, the settings dialog is closed without being saved first.
		# Force enable it here.
		# Settings.set('interface.color.enabled', True)

	@classmethod
	def settingsColor(self, color):
		try: return re.search('\\[.*\\](.*)\\[.*\\]', color, re.IGNORECASE).group(1)
		except: return ''

	@classmethod
	def colorIsHex(self, color):
		return re.match('[0-9a-fA-F]*', color)

	@classmethod
	def colorToRgb(self, hex):
		return [int(hex[i:i+2], 16) for i in range(2,8,2)]

	@classmethod
	def colorToHex(self, rgb):
		rgb = [int(i) for i in rgb]
		return 'FF' + ''.join(['0{0:x}'.format(i) if i < 16 else '{0:x}'.format(i) for i in rgb])

	@classmethod
	def colorGradient(self, startHex, endHex, count = 10):
		key = '%s_%s_%s' % (str(startHex), str(endHex), str(count))
		if not key in Format.Gradients:
			# http://bsou.io/posts/color-gradients-with-python
			start = self.colorToRgb(startHex)
			end = self.colorToRgb(endHex)
			colors = [start]
			for i in range(1, count):
				vector = [int(start[j] + (float(i) / (count-1)) * (end[j] - start[j])) for j in range(3)]
				colors.append(vector)
			Format.Gradients[key] = [self.colorToHex(i) for i in colors]
		return Format.Gradients[key]

	@classmethod
	def colorGradientIncrease(self, count = 10):
		return self.colorGradient(Format.ColorBad, Format.ColorExcellent, count)

	@classmethod
	def colorGradientDecrease(self, count = 10):
		return self.colorGradient(Format.ColorExcellent, Format.ColorBad, count)

	@classmethod
	def colorChange(self, color, change = 10):
		if color:
			color = self.colorToRgb(color)
			color = [i + change for i in color]
			color = [min(255, max(0, i)) for i in color]
			return self.colorToHex(color)
		else:
			return None

	@classmethod
	def colorLighter(self, color, change = 10):
		return self.colorChange(color, change)

	@classmethod
	def colorDarker(self, color, change = 10):
		return self.colorChange(color, -change)

	@classmethod
	def __translate(self, label, utf8 = True):
		return Translation.string(label, utf8 = utf8)


	@classmethod
	def font(self, label, color = None, bold = None, italic = None, light = None, uppercase = None, lowercase = None, capitalcase = None, newline = None, separator = None, translate = True):
		if label is None: return label
		if translate: label = self.__translate(label)
		if label:
			if color:
				label = self.fontColor(label, color, translate = False)
			if bold:
				label = self.fontBold(label, translate = False)
			if italic:
				label = self.fontItalic(label, translate = False)
			if light:
				label = self.fontLight(label, translate = False)
			if uppercase:
				label = self.fontUppercase(label, translate = False)
			elif lowercase:
				label = self.fontLowercase(label, translate = False)
			elif capitalcase:
				label = self.fontCapitalcase(label, translate = False)
			if newline:
				label += self.fontNewline(translate = False)
			if separator:
				label += self.fontSeparator(translate = False)
			return label
		else:
			return ''

	@classmethod
	def fontColor(self, label, color, translate = True):
		if color is None: return label
		if len(color) == 6: color = 'FF' + color
		if translate: label = self.__translate(label)
		return '[COLOR ' + color + ']' + label + '[/COLOR]'

	@classmethod
	def fontBold(self, label, translate = True):
		if translate: label = self.__translate(label)
		return '[B]' + label + '[/B]'

	@classmethod
	def fontItalic(self, label, translate = True):
		if translate: label = self.__translate(label)
		return '[I]' + label + '[/I]'

	@classmethod
	def fontLight(self, label, translate = True):
		if translate: label = self.__translate(label)
		return '[LIGHT]' + label + '[/LIGHT]'

	@classmethod
	def fontUppercase(self, label, translate = True):
		if translate: label = self.__translate(label)
		return '[UPPERCASE]' + label + '[/UPPERCASE]'

	@classmethod
	def fontLowercase(self, label, translate = True):
		if translate: label = self.__translate(label)
		return '[LOWERCASE]' + label + '[/LOWERCASE]'

	@classmethod
	def fontCapitalcase(self, label, translate = True):
		if translate: label = self.__translate(label)
		return '[CAPITALIZE]' + label + '[/CAPITALIZE]'

	@classmethod
	def fontNewline(self):
		return Format.FontNewline

	@classmethod
	def fontSeparator(self, color = ColorDisabled):
		return self.fontColor(Format.FontSeparator, color = color, translate = False)

	@classmethod
	def fontDivider(self):
		return Format.FontDivider

	@classmethod
	def fontSplit(self, label, interval = None, type = None):
		if not interval: interval = Format.FontSplitInterval
		if not type: type = Format.FontNewline
		return re.sub('(.{' + str(interval) + '})', '\\1' + type, label, 0, re.DOTALL)

	@classmethod
	def color(self, label, color):
		return self.fontColor(label, color)

	@classmethod
	def bold(self, label):
		return self.fontBold(label)

	@classmethod
	def italic(self, label):
		return self.fontItalic(label)

	@classmethod
	def light(self, label):
		return self.fontLight(label)

	@classmethod
	def uppercase(self, label):
		return self.fontUppercase(label)

	@classmethod
	def lowercase(self, label):
		return self.fontLowercase(label)

	@classmethod
	def capitalcase(self, label):
		return self.fontCapitalcase(label)

	@classmethod
	def newline(self):
		return self.fontNewline()

	@classmethod
	def separator(self):
		return self.fontSeparator()

	@classmethod
	def divider(self):
		return self.fontDivider()

	@classmethod
	def split(self, label, interval = None, type = None):
		return self.fontSplit(label = label, interval = interval, type = type)



###################################################################
#---Settings
###################################################################
class Settings(object):

	Database = 'settings'
	Lock = threading.Lock()

	SettingsId = 10140

	ParameterDefault = 'default'
	ParameterValue = 'value'
	ParameterVisible = 'visible'

	CategoryCount = 11

	CategoryGeneral = 0
	CategoryInterface = 1
	CategoryScraping = 2
	CategoryProviders = 3
	CategoryAccounts = 4
	CategoryStreaming = 5
	CategoryManual = 6
	CategoryAutomation = 7
	CategoryDownloads = 8
	CategorySubtitles = 9
	CategoryLibrary = 10
	CategoryLightpack = 11

	CacheInitialized = False
	CacheEnabled = False
	CacheMainData = None
	CacheMainValues = None
	CacheUserData = None
	CacheUserValues = None

	PathDefault = 'Default'
	Paths = {
		'downloads.manual.path.combined' 		: 'special://userdata/addon_data/plugin.video.venom/Downloads/Manual/',
		'downloads.manual.path.movies'			: 'special://userdata/addon_data/plugin.video.venom/Downloads/Manual/Movies/',
		'downloads.manual.path.shows'			: 'special://userdata/addon_data/plugin.video.venom/Downloads/Manual/Shows/',
		'downloads.manual.path.documentaries'	: 'special://userdata/addon_data/plugin.video.venom/Downloads/Manual/Documentaries/',
		'downloads.manual.path.shorts'			: 'special://userdata/addon_data/plugin.video.venom/Downloads/Manual/Shorts/',
		'downloads.manual.path.other'			: 'special://userdata/addon_data/plugin.video.venom/Downloads/Manual/Other/',

		'downloads.cache.path.combined'			: 'special://userdata/addon_data/plugin.video.venom/Downloads/Cache/',
		'downloads.cache.path.movies'			: 'special://userdata/addon_data/plugin.video.venom/Downloads/Cache/Movies/',
		'downloads.cache.path.shows'			: 'special://userdata/addon_data/plugin.video.venom/Downloads/Cache/Shows/',
		'downloads.cache.path.documentaries'	: 'special://userdata/addon_data/plugin.video.venom/Downloads/Cache/Documentaries/',
		'downloads.cache.path.shorts'			: 'special://userdata/addon_data/plugin.video.venom/Downloads/Cache/Shorts/',
		'downloads.cache.path.other'			: 'special://userdata/addon_data/plugin.video.venom/Downloads/Cache/Other/',

		'library.locations.combined'			: 'special://userdata/addon_data/plugin.video.venom/Library/',
		'library.locations.movies'				: 'special://userdata/addon_data/plugin.video.venom/Library/Movies/',
		'library.locations.shows'				: 'special://userdata/addon_data/plugin.video.venom/Library/Shows/',
		'library.locations.documentaries'		: 'special://userdata/addon_data/plugin.video.venom/Library/Documentaries/',
		'library.locations.shorts'				: 'special://userdata/addon_data/plugin.video.venom/Library/Shorts/',
	}

	@classmethod
	def _database(self):
		from resources.lib.extensions import database
		return database.Database.instance(Settings.Database, default = File.joinPath(System.path(), 'resources'))

	@classmethod
	def path(self, id):
		path = self.get(id)
		if path == Settings.PathDefault or path.strip() == '' or not path:
			path = Settings.Paths[id]
		return path

	@classmethod
	def pathAddon(self):
		return File.joinPath(System.path(), 'resources', 'settings.xml')

	@classmethod
	def pathProfile(self):
		return File.joinPath(System.profile(), 'settings.xml')

	@classmethod
	def clear(self):
		File.delete(File.joinPath(System.profile(), 'settings.xml'))
		File.delete(File.joinPath(System.profile(), 'settings.db'))

	@classmethod
	def cache(self):
		# Ensures that the data always stays in memory.
		# Otherwise the "static variables" are deleted if there is no more reference to the Settings class.
		if not Settings.CacheInitialized:
			global SettingsAddon
			Settings.CacheInitialized = True
			Settings.CacheEnabled = Converter.boolean(SettingsAddon.getSetting('general.settings.cache'))
			Settings.CacheMainValues = {}
			Settings.CacheUserValues = {}

	@classmethod
	def cacheClear(self):
		# NB: Reset addon in order to clear Kodi's internal settings cache.
		# NB: Important for Reaper settings import in wizard.
		global SettingsAddon
		SettingsAddon = xbmcaddon.Addon(System.VenomAddon)

		Settings.CacheInitialized = False
		Settings.CacheEnabled = False
		Settings.CacheMainData = None
		Settings.CacheMainValues = None
		Settings.CacheUserData = None
		Settings.CacheUserValues = None

	@classmethod
	def cacheEnabled(self):
		self.cache()
		return Settings.CacheEnabled

	@classmethod
	def cacheGet(self, id, raw, database = False):
		self.cache()
		if raw:
			if Settings.CacheMainData is None:
				Settings.CacheMainData = File.readNow(self.pathAddon())
			data = Settings.CacheMainData
			values = Settings.CacheMainValues
			parameter = Settings.ParameterDefault
		else:
			if Settings.CacheUserData is None:
				Settings.CacheUserData = File.readNow(self.pathProfile())
			data = Settings.CacheUserData
			values = Settings.CacheUserValues
			parameter = Settings.ParameterValue

		if id in values: # Already looked-up previously.
			return values[id]
		elif database:
			result = self._getDatabase(id = id)
			values[id] = result
			return result
		else:
			result = self.raw(id = id, parameter = parameter, data = data)
			if result is None: # Not in the userdata settings yet. Fallback to normal Kodi lookup.
				global SettingsAddon
				result = SettingsAddon.getSetting(id)
			values[id] = result
			return result


	@classmethod
	def cacheSet(self, id, value):
		self.cache()
		Settings.CacheUserValues[id] = value


	@classmethod
	def data(self):
		data = None
		path = File.joinPath(System.path(), 'resources', 'settings.xml')
		with open(path, 'r') as file:
			data = file.read()
		return data


	@classmethod
	def set(self, id, value, cached = False):
		if isinstance(value, (dict, list, tuple)):
			from resources.lib.extensions import database
			database = self._database()
			database._insert('INSERT OR IGNORE INTO %s (id) VALUES(?);' % Settings.Database, parameters = (id,))
			database._update('UPDATE %s SET data = ? WHERE id = ?;' % Settings.Database, parameters = (Converter.jsonTo(value), id))
			if cached or self.cacheEnabled(): self.cacheSet(id = id, value = value)
		else:
			if value is True or value is False: # Use is an not ==, becasue checks type as well. Otherwise int/float might also be true.
				value = Converter.boolean(value, string = True)
			else:
				value = str(value)
			global SettingsAddon
			Settings.Lock.acquire()
			SettingsAddon.setSetting(id = id, value = value)
			Settings.Lock.release()
			if cached or self.cacheEnabled(): self.cacheSet(id = id, value = value)


	# Retrieve the values directly from the original settings instead of the saved user XML.
	# This is for internal values/settings that have a default value. If these values change, they are not propagate to the user XML, since the value was already set from a previous version.
	@classmethod
	def raw(self, id, parameter = ParameterDefault, data = None):
		try:
			if data is None: data = self.data()
			indexStart = data.find('id="%s"' % id)
			if indexStart < 0: return None
			indexStart += 4
			indexStart = data.find('"', indexStart)
			if indexStart < 0: return None
			indexEnd = data.find('/>', indexStart)
			if indexEnd < 0: indexEnd = data.find('/setting>', indexStart) # Kodi 18. Do not include the "<", since we search for it below.
			if indexEnd < 0: return None
			data = data[indexStart : indexEnd]
			indexStart = data.find(parameter + '="')
			if indexStart >= 0:
				indexStart = data.find('"', indexStart) + 1
				indexEnd = data.find('"', indexStart)
			elif parameter == Settings.ParameterValue and System.versionKodiNew():
				indexStart = data.find('>') + 1
				indexEnd = data.find('<', indexStart)
			else:
				return None
			return data[indexStart : indexEnd]
		except:
			return None


	@classmethod
	def _getDatabase(self, id):
		try:
			from resources.lib.extensions import database
			return Converter.jsonFrom(self._database()._selectValue('SELECT data FROM %s WHERE id = "%s";' % (Settings.Database, id)))
		except: return None


	# Kodi reads the settings file on every request, which is slow.
	# If the cached option is used, the settings XML is read manually once, and all requests are done from there, which is faster.
	@classmethod
	def get(self, id, raw = False, cached = True, database = False):
		if cached and self.cacheEnabled():
			return self.cacheGet(id = id, raw = raw, database = database)
		elif raw:
			return self.raw(id)
		elif database:
			return self._getDatabase(id)
		else:
			global SettingsAddon
			return SettingsAddon.getSetting(id)


	@classmethod
	def getString(self, id, raw = False, cached = True):
		return self.get(id = id, raw = raw, cached = cached)


	@classmethod
	def getBoolean(self, id, raw = False, cached = True):
		return Converter.boolean(self.get(id = id, raw = raw, cached = cached))


	@classmethod
	def getBool(self, id, raw = False, cached = True):
		return self.getBoolean(id = id, raw = raw, cached = cached)


	@classmethod
	def getNumber(self, id, raw = False, cached = True):
		return self.getDecimal(id = id, raw = raw, cached = cached)


	@classmethod
	def getDecimal(self, id, raw = False, cached = True):
		value = self.get(id = id, raw = raw, cached = cached)
		try: return float(value)
		except: return 0


	@classmethod
	def getFloat(self, id, raw = False, cached = True):
		return self.getDecimal(id = id, raw = raw, cached = cached)


	@classmethod
	def getInteger(self, id, raw = False, cached = True):
		value = self.get(id = id, raw = raw, cached = cached)
		try: return int(value)
		except: return 0


	@classmethod
	def getInt(self, id, raw = False, cached = True):
		return self.getInteger(id = id, raw = raw, cached = cached)


	@classmethod
	def getList(self, id, raw = False, cached = True):
		result = self.get(id = id, raw = raw, cached = cached, database = True)
		return [] if result is None or result == '' else result


	@classmethod
	def getObject(self, id, raw = False, cached = True):
		result = self.get(id = id, raw = raw, cached = cached, database = True)
		return None if result is None or result == '' else result



###################################################################
#---Logger
###################################################################
class Logger(object):

	TypeNotice = xbmc.LOGNOTICE
	TypeError = xbmc.LOGERROR
	TypeSevere = xbmc.LOGSEVERE
	TypeFatal = xbmc.LOGFATAL
	TypeDefault = TypeNotice

	@classmethod
	def log(self, message, message2 = None, message3 = None, message4 = None, message5 = None, name = True, parameters = None, level = TypeDefault):
		divider = ' '
		message = str(message)
		if message2: message += divider + str(message2)
		if message3: message += divider + str(message3)
		if message4: message += divider + str(message4)
		if message5: message += divider + str(message5)
		if name:
			nameValue = control.addonName().upper()
			if not name is True:
				nameValue += ' ' + name
			nameValue += ' ' + System.version()
			if parameters:
				nameValue += ' ['
				if isinstance(parameters, basestring):
					nameValue += parameters
				else:
					nameValue += ', '.join([str(parameter) for parameter in parameters])
				nameValue += ']'
			nameValue += ': '
			message = nameValue + message
		xbmc.log(message, level)

	@classmethod
	def error(self, message = None, exception = True):
		if exception:
			type, value, traceback = sys.exc_info()
			filename = traceback.tb_frame.f_code.co_filename
			linenumber = traceback.tb_lineno
			name = traceback.tb_frame.f_code.co_name
			errortype = type.__name__
			errormessage = value.message
			if message:
				message += ' -> '
			else:
				message = ''
			message += str(errortype) + ' -> ' + str(errormessage)
			parameters = [filename, linenumber, name]
		else:
			parameters = None
		self.log(message, name = 'ERROR', parameters = parameters, level = Logger.TypeError)



###################################################################
#---Icon
###################################################################
class Icon(object):

	TypeIcon = 'icon'
	TypeThumb = 'thumb'
	TypePoster = 'poster'
	TypeBanner = 'banner'
	TypeDefault = TypeIcon

	QualitySmall = 'small'
	QualityLarge = 'large'
	QualityDefault = QualityLarge

	SpecialNone = None
	SpecialQuality = 'quality'
	SpecialDonations = 'donations'
	SpecialNotifications = 'notifications'

	ThemeInitialized = False
	ThemePath = None
	ThemeIcon = None
	ThemeThumb = None
	ThemePoster = None
	ThemeBanner = None

	@classmethod
	def _initialize(self, special = SpecialNone):
		if special is False or not special == Icon.ThemeInitialized:
			Icon.ThemeInitialized = special
			if special: theme = special
			else: theme = tools.Settings.getString('interface.theme.icon').lower()

			if not theme in ['default', '-', '']:

				theme = theme.replace(' ', '').lower()
				if 'glass' in theme:
					theme = theme.replace('(', '').replace(')', '')
				else:
					index = theme.find('(')
					if index >= 0: theme = theme[:index]

				addon = tools.System.pathResources() if theme in ['white', Icon.SpecialQuality, Icon.SpecialDonations, Icon.SpecialNotifications] else tools.System.pathIcons()
				Icon.ThemePath = tools.File.joinPath(addon, 'resources', 'media', 'icons', theme)

				quality = tools.Settings.getInteger('interface.theme.icon.quality')
				if quality == 0:
					if Skin.isAeonNox():
						Icon.ThemeIcon = Icon.QualitySmall
						Icon.ThemeThumb = Icon.QualitySmall
						Icon.ThemePoster = Icon.QualityLarge
						Icon.ThemeBanner = Icon.QualityLarge
					else:
						Icon.ThemeIcon = Icon.QualityLarge
						Icon.ThemeThumb = Icon.QualityLarge
						Icon.ThemePoster = Icon.QualityLarge
						Icon.ThemeBanner = Icon.QualityLarge
				elif quality == 1:
					Icon.ThemeIcon = Icon.QualitySmall
					Icon.ThemeThumb = Icon.QualitySmall
					Icon.ThemePoster = Icon.QualitySmall
					Icon.ThemeBanner = Icon.QualitySmall
				elif quality == 2:
					Icon.ThemeIcon = Icon.QualityLarge
					Icon.ThemeThumb = Icon.QualityLarge
					Icon.ThemePoster = Icon.QualityLarge
					Icon.ThemeBanner = Icon.QualityLarge
				else:
					Icon.ThemeIcon = Icon.QualityLarge
					Icon.ThemeThumb = Icon.QualityLarge
					Icon.ThemePoster = Icon.QualityLarge
					Icon.ThemeBanner = Icon.QualityLarge

	@classmethod
	def exists(self, icon, type = TypeDefault, default = None, special = SpecialNone, quality = None):
		return tools.File.exists(self.path(icon = icon, type = type, default = default, special = special, quality = quality))

	@classmethod
	def path(self, icon, type = TypeDefault, default = None, special = SpecialNone, quality = None):
		if icon is None: return None
		self._initialize(special = special)
		if Icon.ThemePath is None:
			return default
		else:
			if quality is None:
				if type == Icon.TypeIcon: type = Icon.ThemeIcon
				elif type == Icon.TypeThumb: type = Icon.ThemeThumb
				elif type == Icon.TypePoster: type = Icon.ThemePoster
				elif type == Icon.TypeBanner: type = Icon.ThemeBanner
				else: type = Icon.ThemeIcon
			else:
				type = quality
			if not icon.endswith('.png'): icon += '.png'
			return tools.File.joinPath(Icon.ThemePath, type, icon)

	@classmethod
	def pathAll(self, icon, default = None, special = SpecialNone):
		return (
			self.pathIcon(icon = icon, default = default, special = special),
			self.pathThumb(icon = icon, default = default, special = special),
			self.pathPoster(icon = icon, default = default, special = special),
			self.pathBanner(icon = icon, default = default, special = special)
		)

	@classmethod
	def pathIcon(self, icon, default = None, special = SpecialNone):
		return self.path(icon = icon, type = Icon.TypeIcon, default = default, special = special)

	@classmethod
	def pathThumb(self, icon, default = None, special = SpecialNone):
		return self.path(icon = icon, type = Icon.TypeThumb, default = default, special = special)

	@classmethod
	def pathPoster(self, icon, default = None, special = SpecialNone):
		return self.path(icon = icon, type = Icon.TypePoster, default = default, special = special)

	@classmethod
	def pathBanner(self, icon, default = None, special = SpecialNone):
		return self.path(icon = icon, type = Icon.TypeBanner, default = default, special = special)

	@classmethod
	def select(self):
		id = tools.Extensions.IdGaiaIcons
		items = ['Default', 'White']
		getMore = Format.fontBold(Translation.string(33739))
		if tools.Extensions.installed(id):
			items.extend(['Black', 'Glass (Light)', 'Glass (Dark)', 'Shadow (Grey)', 'Fossil (Grey)', 'Navy (Blue)', 'Cerulean (Blue)', 'Sky (Blue)', 'Pine (Green)', 'Lime (Green)', 'Ruby (Red)', 'Candy (Red)', 'Tiger (Orange)', 'Pineapple (Yellow)', 'Violet (Purple)', 'Magenta (Pink)', 'Amber (Brown)'])
		else:
			items.extend([getMore])
		choice = Dialog.options(title = 33338, items = items)
		if choice >= 0:
			if items[choice] == getMore:
				choice = Dialog.option(title = 33338, message = 33741, labelConfirm = 33736, labelDeny = 33743)
				if choice:
					tools.Extensions.enable(id = id)
			else:
				tools.Settings.set('interface.theme.icon', items[choice])



###################################################################
#---Dialog
###################################################################
class Dialog(object):

	IconPlain = 'logo'
	IconInformation = 'information'
	IconWarning = 'warning'
	IconError = 'error'
	IconSuccess = 'success'

	IconNativeLogo = 'nativelogo'
	IconNativeInformation = 'nativeinformation'
	IconNativeWarning = 'nativewarning'
	IconNativeError = 'nativeerror'

	InputAlphabetic = xbmcgui.INPUT_ALPHANUM # Standard keyboard
	InputNumeric = xbmcgui.INPUT_NUMERIC # Format: #
	InputDate = xbmcgui.INPUT_DATE # Format: DD/MM/YYYY
	InputTime = xbmcgui.INPUT_TIME # Format: HH:MM
	InputIp = xbmcgui.INPUT_IPADDRESS # Format: #.#.#.#
	InputPassword = xbmcgui.INPUT_PASSWORD # Returns MD55 hash of input and the input is masked.

	# Numbers/values must correspond with Kodi
	BrowseFile = 1
	BrowseImage = 2
	BrowseDirectoryRead = 0
	BrowseDirectoryWrite = 3
	BrowseDefault = BrowseFile

	PrefixColor = Format.ColorPrimary
	PrefixBack = '« '
	PrefixNext = '» '

	IdDialogText = 10147
	IdDialogProgress = 10101
	IdDialogOk = 12002
	IdDialogNotification = 10107

	@classmethod
	def prefix(self, text, prefix, color = PrefixColor, bold = True):
		return Format.font(prefix, color = color, bold = bold, translate = False) + Translation.string(text)

	@classmethod
	def prefixBack(self, text, color = PrefixColor, bold = None):
		return self.prefix(text = text, prefix = Dialog.PrefixBack, color = color, bold = bold)

	@classmethod
	def prefixNext(self, text, color = PrefixColor, bold = None):
		return self.prefix(text = text, prefix = Dialog.PrefixNext, color = color, bold = bold)

	@classmethod
	def prefixContains(self, text):
		try: return Dialog.PrefixBack in text or Dialog.PrefixNext in text
		except: return False

	@classmethod
	def close(self, id, sleep = None):
		xbmc.executebuiltin('Dialog.Close(%s,true)' % str(id))
		if sleep: time.sleep(sleep / 1000.0)

	@classmethod
	def closeOk(self, sleep = None):
		self.close(id = self.IdDialogOk, sleep = sleep)

	@classmethod
	def closeNotification(self, sleep = None):
		self.close(id = self.IdDialogNotification, sleep = sleep)

	# Close all open dialog.
	# Sometimes if you open a dialog right after this, it also clauses. Might need some sleep to prevent this. sleep in ms.
	@classmethod
	def closeAll(self, sleep = None):
		xbmc.executebuiltin('Dialog.Close(all,true)')
		if sleep: time.sleep(sleep / 1000.0)

	@classmethod
	def closeAllProgress(self, sleep = None):
		xbmc.executebuiltin('Dialog.Close(progressdialog,true)')
		xbmc.executebuiltin('Dialog.Close(extendedprogressdialog,true)')
		if sleep: time.sleep(sleep / 1000.0)

	@classmethod
	def closeAllNative(self, sleep = None):
		xbmc.executebuiltin('Dialog.Close(virtualkeyboard,true)')
		xbmc.executebuiltin('Dialog.Close(yesnodialog,true)')
		xbmc.executebuiltin('Dialog.Close(progressdialog,true)')
		xbmc.executebuiltin('Dialog.Close(extendedprogressdialog,true)')
		xbmc.executebuiltin('Dialog.Close(sliderdialog,true)')
		xbmc.executebuiltin('Dialog.Close(okdialog,true)')
		xbmc.executebuiltin('Dialog.Close(selectdialog,true)')
		if sleep: time.sleep(sleep / 1000.0)

	@classmethod
	def aborted(self):
		return xbmc.abortRequested

	# Current window ID
	@classmethod
	def windowId(self):
		return xbmcgui.getCurrentWindowId()

	# Check if certain window is currently showing.
	@classmethod
	def windowVisible(self, id):
		return self.windowId() == id

	# Current dialog ID
	@classmethod
	def dialogId(self):
		return xbmcgui.getCurrentWindowDialogId()

	# Check if certain dialog is currently showing.
	@classmethod
	def dialogVisible(self, id):
		return self.dialogId() == id

	@classmethod
	def dialogProgressVisible(self):
		return self.dialogVisible(Dialog.IdDialogProgress)

	@classmethod
	def confirm(self, message, title = None):
		return xbmcgui.Dialog().ok(self.title(title), self.__translate(message))

	@classmethod
	def select(self, items, multiple = False, selection = None, title = None):
		return self.options(items = items, multiple = multiple, selection = selection, title = title)

	@classmethod
	def option(self, message, labelConfirm = None, labelDeny = None, title = None):
		if not labelConfirm is None:
			labelConfirm = self.__translate(labelConfirm)
		if not labelDeny is None:
			labelDeny = self.__translate(labelDeny)
		return xbmcgui.Dialog().yesno(self.title(title), self.__translate(message), yeslabel = labelConfirm, nolabel = labelDeny)

	@classmethod
	def options(self, items, multiple = False, selection = None, title = None):
		if multiple:
			try: return xbmcgui.Dialog().multiselect(self.title(title), items, preselect = selection)
			except: return xbmcgui.Dialog().multiselect(self.title(title), items)
		else:
			try: return xbmcgui.Dialog().select(self.title(title), items, preselect = selection)
			except: return xbmcgui.Dialog().select(self.title(title), items)


	# items = [(label1,callback1),(label2,callback2),...]
	# or labels = [label1,label2,...]
	@classmethod
	def context(self, items = None, labels = None):
		if items:
			labels = [i[0] for i in items]
			choice = xbmcgui.Dialog().contextmenu(labels)
			if choice >= 0: return items[choice][1]()
			else: return False
		else:
			return xbmcgui.Dialog().contextmenu(labels)

	@classmethod
	def progress(self, message = None, background = False, title = None):
		if background:
			dialog = xbmcgui.DialogProgressBG()
		else:
			dialog = xbmcgui.DialogProgress()
		if not message:
			message = ''
		else:
			message = self.__translate(message)
		title = self.title(title)
		dialog.create(title, message)
		if background:
			dialog.update(0, title, message)
		else:
			dialog.update(0, message)
		return dialog

	# verify: Existing MD5 password string to compare against.
	# confirm: Confirm password. Must be entered twice
	# hidden: Hides alphabetic input.
	# default: Default set input.
	@classmethod
	def input(self, type = InputAlphabetic, verify = False, confirm = False, hidden = False, default = None, title = None):
		default = '' if default is None else default
		if verify:
			option = xbmcgui.PASSWORD_VERIFY
			if isinstance(verify, basestring):
				default = verify
		elif confirm:
			option = 0
		elif hidden:
			option = xbmcgui.ALPHANUM_HIDE_INPUT
		else:
			option = None
		# NB: Although the default parameter is given in the docs, it seems that the parameter is not actually called "default". Hence, pass it in as an unmaed parameter.
		if option is None: result = xbmcgui.Dialog().input(self.title(title), str(default), type = type)
		else: result = xbmcgui.Dialog().input(self.title(title), str(default), type = type, option = option)

		if verify:
			return not result == ''
		else:
			return result

	@classmethod
	def inputPassword(self, verify = False, confirm = False, title = None):
		return self.input(title = title, type = Dialog.InputPassword, verify = verify, confirm = confirm)

	@classmethod
	def browse(self, type = BrowseDefault, default = None, multiple = False, mask = [], title = None):
		if default is None: default = File.joinPath(System.pathHome(), '') # Needs to end with a slash
		if mask is None: mask = []
		elif isinstance(mask, basestring): mask = [mask]
		for i in range(len(mask)):
			mask[i] = mask[i].lower()
			if not mask[i].startswith('.'):
				mask[i] = '.' + mask[i]
		mask = '|'.join(mask)
		return xbmcgui.Dialog().browse(type, self.title(title), 'files', mask, True, False, default, multiple)

	@classmethod
	def page(self, message, title = None):
		xbmc.executebuiltin('ActivateWindow(%d)' % Dialog.IdDialogText)
		time.sleep(0.5)
		window = xbmcgui.Window(Dialog.IdDialogText)
		retry = 50
		while retry > 0:
			try:
				time.sleep(0.01)
				retry -= 1
				window.getControl(1).setLabel(self.title(title))
				window.getControl(5).setText('[CR]' + message)
				break
			except: pass
		return window

	@classmethod
	def pageVisible(self):
		return self.dialogVisible(Dialog.IdDialogText)


	@classmethod
	def information(self, items, title = None, refresh = None):
		if items is None or len(items) == 0:
			return False

		def decorate(item):
			value = item['value'] if 'value' in item else None
			label = item['title'] if 'title' in item else ''
			prefix = Dialog.prefixContains(label)
			if not prefix: label = self.__translate(label)

			if value is None:
				heading = value or 'items' in item
				label = Format.font(label, bold = True, uppercase = heading, color = Format.ColorPrimary if heading else None, translate = False if prefix else True)
			else:
				if not label == '':
					if not value is None:
						label += ': '
					label = Format.font(label, bold = True, color = Format.ColorSecondary)
				if not value is None:
					label += Format.font(self.__translate(item['value']), italic = ('link' in item and item['link']))
			return label

		def create(items):
			result = []
			actions = []
			closes = []
			returns = []
			for item in items:
				if not item is None:
					if 'items' in item:
						# if not len(result) == 0:
							# result.append('')
							# actions.append(None)
							# closes.append(None)
							# returns.append(None)
						result.append(decorate(item))
						actions.append(item['action'] if 'action' in item else None)
						closes.append(item['close'] if 'close' in item else False)
						returns.append(item['return'] if 'return' in item else None)
						for i in item['items']:
							if not i is None:
								result.append(decorate(i))
								actions.append(i['action'] if 'action' in i else None)
								closes.append(i['close'] if 'close' in i else False)
								returns.append(i['return'] if 'return' in i else None)
					else:
						result.append(decorate(item))
						actions.append(item['action'] if 'action' in item else None)
						closes.append(item['close'] if 'close' in item else False)
						returns.append(item['return'] if 'return' in item else None)
			return result, actions, closes, returns

		items, actions, closes, returns = create(items)
		if any(i for i in actions):
			while True:
				choice = self.select(items = items, title = title)
				if choice < 0: break
				if actions[choice]: actions[choice]()
				if closes[choice]: break
				elif refresh: items, actions, closes, returns = create(refresh())
		elif any(i for i in returns):
			choice = self.select(items, title = title)
			if choice < 0: return None
			return returns[choice]
		else:
			return self.select(items, title = title)

	@classmethod
	def __translate(self, string):
		return Translation.string(string)

	@classmethod
	def title(self, extension = None, bold = True, titleless = False):
		title = '' if titleless else System.name().encode('utf-8')
		if not extension is None:
			if not titleless:
				title += Format.divider()
			title += self.__translate(extension)
		if bold:
			title = Format.fontBold(title)
		return title



###################################################################
#---Loader
###################################################################
class Loader(object):
	Type = None

	@classmethod
	def type(self):
		if Loader.Type is None: Loader.Type = 'busydialognocancel' if System.versionKodiNew() else 'busydialog'
		return Loader.Type

	@classmethod
	def show(self):
		xbmc.executebuiltin('ActivateWindow(%s)' % self.type())

	@classmethod
	def hide(self):
		if System.versionKodiNew(): xbmc.executebuiltin('Dialog.Close(busydialognocancel)')
		xbmc.executebuiltin('Dialog.Close(busydialog)')

	@classmethod
	def visible(self):
		if System.versionKodiNew() and xbmc.getCondVisibility('Window.IsActive(busydialognocancel)') == 1: return True
		return xbmc.getCondVisibility('Window.IsActive(busydialog)') == 1



###################################################################
#---System
###################################################################
class System(object):

	VenomAddon = 'plugin.video.venom'

	KodiVersionFull = None
	KodiVersion = None


	@classmethod
	def obfuscate(self, data, iterations = 3, inverse = True):
		if inverse:
			for i in range(iterations):
				data = Converter.base64From(data)[::-1]
		else:
			for i in range(iterations):
				data = Converter.base64To(data[::-1])
		return data


	@classmethod
	def versionKodi(self, full = False):
		if full:
			if System.KodiVersionFull is None:
				System.KodiVersionFull = self.infoLabel('System.BuildVersion')
			return System.KodiVersionFull
		else:
			if System.KodiVersion is None:
				try: System.KodiVersion = float(re.search('^\d+\.?\d+', self.infoLabel('System.BuildVersion')).group(0))
				except: pass
			return System.KodiVersion


	@classmethod
	def versionKodiNew(self):
		try: return self.versionKodi() >= 18
		except: return False


	@classmethod
	def path(self, id):
		try: addon = xbmcaddon.Addon(id)
		except: addon = None
		if addon is None:
			return ''
		else:
			return File.translatePath(addon.getAddonInfo('path').decode('utf-8'))


	@classmethod
	def id(self, id = VenomAddon):
		return xbmcaddon.Addon(id).getAddonInfo('id')


	@classmethod
	def name(self, id = VenomAddon):
		return xbmcaddon.Addon(id).getAddonInfo('name')
	# Checks version of an installed addon, used by Trakt scrobbleUpdate()


	@classmethod
	def version(self, id = VenomAddon):
		return xbmcaddon.Addon(id).getAddonInfo('version')


	# Checks if an addon is installed, trakt.py uses it
	@classmethod
	def installed(self, id):
		try:
			addon = xbmcaddon.Addon(id)
			id = addon.getAddonInfo('id')
			return not id is None and not id == ''
		except:
			return False


	@classmethod
	def execute(self, command):
		return xbmc.executebuiltin(command)



###################################################################
#---Converter
###################################################################
class Converter(object):

	Base64 = 'base64'

	@classmethod
	def roman(self, number):
		number = number.lower().replace(' ', '')
		numerals = {'i' : 1, 'v' : 5, 'x' : 10, 'l' : 50, 'c' : 100, 'd' : 500, 'm' : 1000}
		result = 0
		for i, c in enumerate(number):
			if not c in numerals:
				return None
			elif (i + 1) == len(number) or numerals[c] > numerals[number[i + 1]]:
				result += numerals[c]
			else:
				result -= numerals[c]
		return result

	@classmethod
	def boolean(self, value, string = False, none = False):
		if none and value is None:
			return value
		elif string:
			return 'true' if value else 'false'
		else:
			if value is True or value is False:
				return value
			elif isinstance(value, numbers.Number):
				return value > 0
			elif isinstance(value, basestring):
				value = value.lower()
				return value == 'true' or value == 'yes' or value == 't' or value == 'y' or value == '1'
			else:
				return False

	@classmethod
	def dictionary(self, jsonData):
		try:
			if jsonData is None: return None
			jsonData = json.loads(jsonData)

			# In case the quotes in the string were escaped, causing the first json.loads to return a unicode string.
			try: jsonData = json.loads(jsonData)
			except: pass

			return jsonData
		except:
			return jsonData

	@classmethod
	def unicode(self, string, umlaut = False):
		try:
			if string is None:
				return string
			if umlaut:
				try: string = string.replace(unichr(196), 'AE').replace(unichr(203), 'EE').replace(unichr(207), 'IE').replace(unichr(214), 'OE').replace(unichr(220), 'UE').replace(unichr(228), 'ae').replace(unichr(235), 'ee').replace(unichr(239), 'ie').replace(unichr(246), 'oe').replace(unichr(252), 'ue')
				except: pass
			return unidecode(string.decode('utf-8'))
		except:
			try: return string.encode('ascii', 'ignore')
			except: return string

	@classmethod
	def base64From(self, data, iterations = 1):
		data = str(data)
		for i in range(iterations):
			data = data.decode(Converter.Base64)
		return data

	@classmethod
	def base64To(self, data, iterations = 1):
		data = str(data)
		for i in range(iterations):
			data = data.encode(Converter.Base64).replace('\n', '')
		return data

	@classmethod
	def jsonFrom(self, data, default = None):
		try: return json.loads(data)
		except: return default

	@classmethod
	def jsonTo(self, data, default = None):
		try: return json.dumps(data)
		except: return default

	@classmethod
	def quoteFrom(self, data, default = None):
		try: return urllib.unquote_plus(data).decode('utf-8')
		except: return default

	@classmethod
	def quoteTo(self, data, default = None):
		try: return urllib.quote_plus(data)
		except: return default

	@classmethod
	def serialize(self, data):
		try:
			import pickle
			return pickle.dumps(data)
		except:
			return None

	@classmethod
	def unserialize(self, data):
		try:
			import pickle
			return pickle.loads(data)
		except:
			return None

	# Convert HTML entities to ASCII.
	@classmethod
	def htmlFrom(self, data):
		try:
			try: from HTMLParser import HTMLParser
			except: from html.parser import HTMLParser
			return str(HTMLParser().unescape(data))
		except:
			return data



###################################################################
#---Cache
###################################################################
class Cache(object):

	@classmethod
	def cache(self, function, timeout, *arguments):
		from resources.lib.modules import cache
		return cache.get(function, timeout, *arguments)


	@classmethod
	def clean(self, duration = 1209600):
		from resources.lib.modules import cache
		return cache.cache_clean(duration)

	@classmethod
	def clear(self):
		from resources.lib.modules import cache
		return cache.cache_clear()



###################################################################
#---Time
###################################################################
class Time(object):

	# Use time.clock() instead of time.time() for processing time.
	# NB: Do not use time.clock(). Gives the wrong answer in timestamp() AND runs very fast in Linux. Hence, in the stream finding dialog, for every real second, Linux progresses 5-6 seconds.
	# http://stackoverflow.com/questions/85451/python-time-clock-vs-time-time-accuracy
	# https://www.tutorialspoint.com/python/time_clock.htm

	ZoneUtc = 'utc'
	ZoneLocal = 'local'

	FormatTimestamp = None
	FormatDateTime = '%Y-%m-%d %H:%M:%S'
	FormatDate = '%Y-%m-%d'
	FormatTime = '%H:%M:%S'
	FormatTimeShort = '%H:%M'

	def __init__(self, start = False):
		self.mStart = None
		if start: self.start()

	def start(self):
		self.mStart = time.time()
		return self.mStart

	def restart(self):
		return self.start()

	def elapsed(self, milliseconds = False):
		if self.mStart is None:
			self.mStart = time.time()
		if milliseconds: return int((time.time() - self.mStart) * 1000)
		else: return int(time.time() - self.mStart)

	def expired(self, expiration):
		return self.elapsed() >= expiration

	@classmethod
	def sleep(self, seconds):
		time.sleep(seconds)

	# UTC timestamp
	@classmethod
	def timestamp(self, fixedTime = None):
		if fixedTime is None:
			# Do not use time.clock(), gives incorrect result for search.py
			return int(time.time())
		else:
			return int(time.mktime(fixedTime.timetuple()))

	@classmethod
	def format(self, timestamp = None, format = FormatDateTime):
		if timestamp is None: timestamp = self.timestamp()
		return datetime.datetime.utcfromtimestamp(timestamp).strftime(format)

	# datetime object from string
	@classmethod
	def datetime(self, string, format = FormatDateTime):
		try:
			return datetime.datetime.strptime(string, format)
		except:
			# Older Kodi Python versions do not have the strptime function.
			# http://forum.kodi.tv/showthread.php?tid=112916
			return datetime.datetime.fromtimestamp(time.mktime(time.strptime(string, format)))

	@classmethod
	def past(self, seconds = 0, minutes = 0, days = 0, format = FormatTimestamp):
		result = self.timestamp() - seconds - (minutes * 60) - (days * 86400)
		if not format == self.FormatTimestamp: result = self.format(timestamp = result, format = format)
		return result

	@classmethod
	def future(self, seconds = 0, minutes = 0, days = 0, format = FormatTimestamp):
		result = self.timestamp() + seconds + (minutes * 60) + (days * 86400)
		if not format == self.FormatTimestamp: result = self.format(timestamp = result, format = format)
		return result

	@classmethod
	def localZone(self):
		if time.daylight:
			offsetHour = time.altzone / 3600
		else:
			offsetHour = time.timezone / 3600
		return 'Etc/GMT%+d' % offsetHour

	@classmethod
	def convert(self, stringTime, stringDay = None, abbreviate = False, formatInput = FormatTimeShort, formatOutput = None, zoneFrom = ZoneUtc, zoneTo = ZoneLocal):
		result = ''
		try:
			# If only time is given, the date will be set to 1900-01-01 and there are conversion problems if this goes down to 1899.
			if formatInput == '%H:%M':
				# Use current datetime (now) in order to accomodate for daylight saving time.
				stringTime = '%s %s' % (datetime.datetime.now().strftime('%Y-%m-%d'), stringTime)
				formatNew = '%Y-%m-%d %H:%M'
			else:
				formatNew = formatInput

			if zoneFrom == Time.ZoneUtc: zoneFrom = pytz.timezone('UTC')
			elif zoneFrom == Time.ZoneLocal: zoneFrom = pytz.timezone(self.localZone())
			else: zoneFrom = pytz.timezone(zoneFrom)

			if zoneTo == Time.ZoneUtc: zoneTo = pytz.timezone('UTC')
			elif zoneTo == Time.ZoneLocal: zoneTo = pytz.timezone(self.localZone())
			else: zoneTo = pytz.timezone(zoneTo)

			timeobject = self.datetime(string = stringTime, format = formatNew)

			if stringDay:
				stringDay = stringDay.lower()
				if stringDay.startswith('mon'): weekday = 0
				elif stringDay.startswith('tue'): weekday = 1
				elif stringDay.startswith('wed'): weekday = 2
				elif stringDay.startswith('thu'): weekday = 3
				elif stringDay.startswith('fri'): weekday = 4
				elif stringDay.startswith('sat'): weekday = 5
				else: weekday = 6
				weekdayCurrent = datetime.datetime.now().weekday()
				timeobject += datetime.timedelta(days = weekday) - datetime.timedelta(days = weekdayCurrent)

			timeobject = zoneFrom.localize(timeobject)
			timeobject = timeobject.astimezone(zoneTo)

			if not formatOutput: formatOutput = formatInput

			stringTime = timeobject.strftime(formatOutput)
			if stringDay:
				if abbreviate:
					stringDay = calendar.day_abbr[timeobject.weekday()]
				else:
					stringDay = calendar.day_name[timeobject.weekday()]
				return (stringTime, stringDay)
			else:
				return stringTime
		except:
			Logger.error()
			return stringTime



###################################################################
#---File
###################################################################
class File(object):

	PrefixSpecial = 'special://'
	PrefixSamba = 'smb://'

	DirectoryHome = PrefixSpecial + 'home'
	DirectoryTemporary = PrefixSpecial + 'temp'

	@classmethod
	def freeSpace(self, path = '/'):
		free = 0
		directory = os.path.realpath(path)
		try:
			if not free:
				import shutil
				total, used, free = shutil.disk_usage(directory)
		except: pass
		try:
			if not free:
				import psutil
				free = psutil.disk_usage(directory).free
		except: pass
		try:
			if not free:
				windows = Platform.familyType() == Platform.FamilyWindows
				if windows:
					try:
						if not free:
							import ctypes
							bytes = ctypes.c_ulonglong(0)
							ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(directory), None, None, ctypes.pointer(bytes))
							free = bytes.value
					except: pass
					try:
						if not free:
							import win32file
							sectorsPerCluster, bytesPerSector, freeClusters, totalClusters = win32file.GetDiskFreeSpace(directory)
							free = sectorsPerCluster * bytesPerSector * freeClusters
					except: pass
				else:
					try:
						if not free:
							stats = os.statvfs(dirname)
							free = stats.f_bavail * stats.f_frsize
					except: pass
					try:
						if free == 0:
							stats = subprocess.Popen(['df', '-Pk', directory], stdout = subprocess.PIPE).communicate()[0]
							free = int(stats.splitlines()[1].split()[3]) * 1024
					except: pass
		except: pass
		return free

	@classmethod
	def translate(self, path):
		if path.startswith(File.PrefixSpecial):
			path = xbmc.translatePath(path)
		return path

	@classmethod
	def name(self, path):
		name = os.path.basename(os.path.splitext(path)[0])
		if name == '': name = None
		return name

	@classmethod
	def makeDirectory(self, path):
		return xbmcvfs.mkdirs(path)

	@classmethod
	def translatePath(self, path):
		return xbmc.translatePath(path)

	@classmethod
	def legalPath(self, path):
		return xbmc.makeLegalFilename(path)

	@classmethod
	def joinPath(self, path, *paths):
		return os.path.join(path, *paths)

	@classmethod
	def exists(self, path): # Directory must end with slash
		# Do not use xbmcvfs.exists, since it returns true for http links.
		if path.startswith('http:') or path.startswith('https:') or path.startswith('ftp:') or path.startswith('ftps:'):
			return os.path.exists(path)
		else:
			return xbmcvfs.exists(path)

	@classmethod
	def existsDirectory(self, path):
		if not path.endswith('/') and not path.endswith('\\'):
			path += '/'
		return xbmcvfs.exists(path)

	# If samba file or directory.
	@classmethod
	def samba(self, path):
		return path.startswith(File.PrefixSamba)

	# If network (samba or any other non-local supported Kodi path) file or directory.
	# Path must point to a valid file or directory.
	@classmethod
	def network(self, path):
		return self.samba(path) or (self.exists(path) and not os.path.exists(path))

	@classmethod
	def delete(self, path, force = True):
		try:
			# For samba paths
			try:
				if self.exists(path):
					xbmcvfs.delete(path)
			except:
				pass

			# All with force
			try:
				if self.exists(path):
					if force: os.chmod(path, stat.S_IWRITE) # Remove read only.
					return os.remove(path) # xbmcvfs often has problems deleting files
			except:
				pass

			return not self.exists(path)
		except:
			return False

	@classmethod
	def directory(self, path):
		return os.path.dirname(path)

	@classmethod
	def deleteDirectory(self, path, force = True):
		try:
			# For samba paths
			try:
				if self.existsDirectory(path):
					xbmcvfs.rmdir(path)
					if not self.existsDirectory(path):
						return True
			except:
				pass

			try:
				if self.existsDirectory(path):
					shutil.rmtree(path)
					if not self.existsDirectory(path):
						return True
			except:
				pass

			# All with force
			try:
				if self.existsDirectory(path):
					if force: os.chmod(path, stat.S_IWRITE) # Remove read only.
					os.rmdir(path)
					if not self.existsDirectory(path):
						return True
			except:
				pass

			# Try individual delete
			try:
				if self.existsDirectory(path):
					directories, files = self.listDirectory(path)
					for i in files:
						self.delete(os.path.join(path, i), force = force)
					for i in directories:
						self.deleteDirectory(os.path.join(path, i), force = force)
					try: xbmcvfs.rmdir(path)
					except: pass
					try: shutil.rmtree(path)
					except: pass
					try: os.rmdir(path)
					except: pass
			except:
				pass

			return not self.existsDirectory(path)
		except:
			Logger.error()
			return False

	@classmethod
	def size(self, path):
		return xbmcvfs.File(path).size()

	@classmethod
	def create(self, path):
		return self.writeNow(path, '')

	@classmethod
	def readNow(self, path):
		try:
			file = xbmcvfs.File(path)
			result = file.read()
			file.close()
			return result.decode('utf-8')
		except: return None

	@classmethod
	def writeNow(self, path, value):
		file = xbmcvfs.File(path, 'w')
		result = file.write(str(value.encode('utf-8')))
		file.close()
		return result

	# replaceNow(path, 'from', 'to')
	# replaceNow(path, [['from1', 'to1'], ['from2', 'to2']])
	@classmethod
	def replaceNow(self, path, valueFrom, valueTo = None):
		data = self.readNow(path)
		if not isinstance(valueFrom, list):
			valueFrom = [[valueFrom, valueTo]]
		for replacement in valueFrom:
			data = data.replace(replacement[0], replacement[1])
		self.writeNow(path, data)

	# Returns: directories, files
	@classmethod
	def listDirectory(self, path, absolute = False):
		directories, files = xbmcvfs.listdir(path)
		if absolute:
			for i in range(len(files)):
				files[i] = File.joinPath(path, files[i])
			for i in range(len(directories)):
				directories[i] = File.joinPath(path, directories[i])
		return directories, files

	@classmethod
	def copy(self, pathFrom, pathTo, bytes = None, overwrite = False, sleep = True):
		if overwrite and xbmcvfs.exists(pathTo):
			try: self.delete(path = pathTo, force = True)
			except: pass
			# This is important, especailly for Windows.
			# When deleteing a file and immediatly replacing it, the old file might still exist and the file is never replaced.
			if sleep: Time.sleep(0.1 if sleep is True else sleep)
		if bytes is None:
			return xbmcvfs.copy(pathFrom, pathTo)
		else:
			try:
				fileFrom = xbmcvfs.File(pathFrom)
				fileTo = xbmcvfs.File(pathTo, 'w')
				chunk = min(bytes, 1048576) # 1 MB
				while bytes > 0:
					size = min(bytes, chunk)
					fileTo.write(fileFrom.read(size))
					bytes -= size
				fileFrom.close()
				fileTo.close()
				return True
			except:
				return False

	@classmethod
	def copyDirectory(self, pathFrom, pathTo, overwrite = True):
		if not pathFrom.endswith('/') and not pathFrom.endswith('\\'):
			pathFrom += '/'
		if not pathTo.endswith('/') and not pathTo.endswith('\\'):
			pathTo += '/'

		# NB: Always check if directory exists before copying it on Windows.
		# If the source directory does not exist, Windows will simply copy the entire C: drive.
		if self.existsDirectory(pathFrom):
			try:
				if overwrite: File.deleteDirectory(pathTo)
				shutil.copytree(pathFrom, pathTo)
				return True
			except:
				return False
		else:
			return False

	@classmethod
	def renameDirectory(self, pathFrom, pathTo):
		if not pathFrom.endswith('/') and not pathFrom.endswith('\\'):
			pathFrom += '/'
		if not pathTo.endswith('/') and not pathTo.endswith('\\'):
			pathTo += '/'
		os.rename(pathFrom, pathTo)

	# Not for samba paths
	@classmethod
	def move(self, pathFrom, pathTo, replace = True, sleep = True):
		if pathFrom == pathTo:
			return False
		if replace:
			try: self.delete(path = pathTo, force = True)
			except: pass
			# This is important, especailly for Windows.
			# When deleteing a file and immediatly replacing it, the old file might still exist and the file is never replaced.
			# Especailly important for import Reaper's settings on inital use.
			if sleep: Time.sleep(0.1 if sleep is True else sleep)
		try:
			shutil.move(pathFrom, pathTo)
			return True
		except:
			return False


