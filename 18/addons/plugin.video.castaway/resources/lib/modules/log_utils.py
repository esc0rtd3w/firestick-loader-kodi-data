import xbmc
import xbmcaddon

addon = xbmcaddon.Addon()
name = addon.getAddonInfo('name')

LOGDEBUG = xbmc.LOGDEBUG
LOGERROR = xbmc.LOGERROR
LOGFATAL = xbmc.LOGFATAL
LOGINFO = xbmc.LOGINFO
LOGNONE = xbmc.LOGNONE
LOGNOTICE = xbmc.LOGNOTICE
LOGSEVERE = xbmc.LOGSEVERE
LOGWARNING = xbmc.LOGWARNING

def log(msg, level=xbmc.LOGNOTICE):
    # override message level to force logging when addon logging turned on
    if addon.getSetting('addon_debug') == 'true' and level == xbmc.LOGDEBUG:
        level = xbmc.LOGNOTICE
    
    try:
        if isinstance(msg, unicode):
            msg = '%s (ENCODED)' % (msg.encode('utf-8'))

        xbmc.log('%s: %s' % (name, msg), level)
    except Exception as e:
        try: xbmc.log('Logging Failure: %s' % (e), level)
        except: pass  # just give up
