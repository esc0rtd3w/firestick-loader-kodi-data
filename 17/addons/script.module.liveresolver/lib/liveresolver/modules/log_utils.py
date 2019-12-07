import xbmc
import xbmcaddon, sys
from addon.common.addon import Addon

my_addon = xbmcaddon.Addon()


addon = Addon('script.module.liveresolver', sys.argv)
version = addon.get_version()

LOGDEBUG = xbmc.LOGDEBUG
LOGERROR = xbmc.LOGERROR
LOGFATAL = xbmc.LOGFATAL
LOGINFO = xbmc.LOGINFO
LOGNONE = xbmc.LOGNONE
LOGNOTICE = xbmc.LOGNOTICE
LOGSEVERE = xbmc.LOGSEVERE
LOGWARNING = xbmc.LOGWARNING

def log(msg, level=xbmc.LOGDEBUG):
    # override message level to force logging when addon logging turned on
    if my_addon.getSetting('addon_debug') == 'true' and level == xbmc.LOGDEBUG:
        level = xbmc.LOGNOTICE
    
    try:
        if isinstance(msg, unicode):
            msg = '%s (ENCODED)' % (msg.encode('utf-8'))

        xbmc.log('Liveresolver %s | %s' % (version, msg), level)
    except Exception as e:
        try: xbmc.log('Logging Failure: %s' % (e), level)
        except: pass  # just give up
