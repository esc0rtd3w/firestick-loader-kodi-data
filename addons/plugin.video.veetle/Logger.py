import xbmc

LOG_LEVEL = 0

DEBUG = 0
INFO = 1
WARN = 2
ERROR = 3

class Logger():

    def __init__(self, type):
        self.type = type

    def debug(self, message):
        self.log(message, xbmc.LOGDEBUG)

    def info(self, message):
        self.log(message, xbmc.LOGINFO)

    def notice(self, message):
        self.log(message, xbmc.LOGNOTICE)

    def warn(self, message):
        self.log(message, xbmc.LOGWARNING)

    def error(self, message):
        self.log(message, xbmc.LOGERROR)

    def log(self, message, level):
        if level >= LOG_LEVEL:
            xbmc.log("[plugins.video.veetle] %s: '%s'" % (self.type, message), level)

