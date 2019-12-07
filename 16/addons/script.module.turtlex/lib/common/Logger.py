
import logging
import xbmc  # @UnresolvedImport

def logInfo(message):
    if type(message) is not str:
        message = str(message)
    xbmc.log(message, xbmc.LOGINFO)

def logDebug(message):
    if type(message) is not str:
        message = str(message)
    xbmc.log(message, xbmc.LOGDEBUG)
    
def logError(message):
    logging.exception(message)
    
def logFatal(message):
    logging.exception(message)
    
def logNotice(message):
    if type(message) is not str:
        message = str(message)
    xbmc.log(message, xbmc.LOGNOTICE)
    
def logSevere(message):
    logging.exception(message)

def logWarning(message):
    if type(message) is not str:
        if type(message) is Exception:
            logging.exception(message)
            return
        message = str(message)
    xbmc.log(message, xbmc.LOGWARNING)
        

