import xbmc
import xbmcaddon
from dudehere.routines import *
try:
	KODI_LANGUAGE = xbmc.getLanguage()
except:
	KODI_LANGUAGE = 'English'
LANGUAGE_PATH = vfs.join(ROOT_PATH, 'resources/language/')
LANGUAGE_PATH += KODI_LANGUAGE

def i18n(id):
	return xbmcaddon.Addon().getLocalizedString(id).encode('utf-8', 'ignore')