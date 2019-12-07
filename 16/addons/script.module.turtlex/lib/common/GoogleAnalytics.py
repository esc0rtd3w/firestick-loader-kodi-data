'''
Created on May 19, 2013

@author: ajju
'''

from common.Singleton import SingletonClass
import datetime
import os
import re
import time
import xbmc  # @UnresolvedImport
from common import Logger

class GAClient(SingletonClass):
    
    def __initialize__(self, addon_context):
        self.addon_context = addon_context
        self.addon_version = (addon_context.addon_ver if addon_context.addon_ver is not None else "0.0.0") + "_" + addon_context.turtle_ver
        self.addon_name = addon_context.addon_id.replace('plugin.video.', '') + '_' + self.addon_version
        if addon_context.addon.getSetting('ga_visitor') == '':
            from random import randint
            addon_context.addon.setSetting('ga_visitor', str(randint(0, 0x7fffffff)))
        self.ua_track = ''
    
    
    def __parseDate(self, dateString):
        try:
            return datetime.datetime.fromtimestamp(time.mktime(time.strptime(dateString.encode('utf-8', 'replace'), "%Y-%m-%d %H:%M:%S")))
        except:
            return datetime.datetime.today() - datetime.timedelta(days=1)  # force update
    
    
    def reportAppLaunch(self):
        
        secsInHour = 60 * 60
        threshold = 2 * secsInHour
    
        now = datetime.datetime.today()
        prev = self.__parseDate(self.addon_context.addon.getSetting('ga_time'))
        delta = now - prev
        nDays = delta.days
        nSecs = delta.seconds
    
        doUpdate = (nDays > 0) or (nSecs > threshold)
        if not doUpdate:
            return
    
        self.addon_context.addon.setSetting('ga_time', str(now).split('.')[0])
        self.APP_LAUNCH()
    
                    
    def __send_request_to_google_analytics(self, utm_url):
        ua = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
        import urllib2
        try:
            if self.addon_context.addon.getSetting('ga_enabled') == 'true': #default is disabled
                req = urllib2.Request(utm_url, None, {'User-Agent':ua})
                response = urllib2.urlopen(req)
                print response.read()
                response.close()
        except Exception, e:
            Logger.logError(e)
            Logger.logDebug ("GA fail: %s" % utm_url)
    
    def reportAction(self, action_id):
        if action_id is not None:
            if action_id.startswith("snap_"):
                if action_id is 'snap_and_download_video':
                    self.GA("None", "Download")
                else:
                    return
            elif action_id is not "__start__":
                self.GA("None", action_id)
                
    def reportContentUsage(self, addon, contentTitle):
        if addon is not None and contentTitle is not None:
            self.GA(addon, contentTitle)
           
    def GA(self, group, name):
            try:
                from random import randint
                from urllib import  quote
                VISITOR = self.addon_context.addon.getSetting('ga_visitor')
                utm_gif_location = "http://www.google-analytics.com/__utm.gif"
                if not group == "None":
                        utm_track = utm_gif_location + "?" + \
                                "utmwv=" + self.addon_version + \
                                "&utmn=" + str(randint(0, 0x7fffffff)) + \
                                "&utmt=" + "event" + \
                                "&utme=" + quote("5(" + self.addon_name + "*" + group + "*" + name + ")") + \
                                "&utmp=" + quote(self.addon_name) + \
                                "&utmac=" + self.ua_track + \
                                "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR, VISITOR, "2"])
                        try:
                            Logger.logDebug("============================ POSTING TRACK EVENT ============================")
                            self.__send_request_to_google_analytics(utm_track)
                        except Exception, e:
                            Logger.logError(e)
                            Logger.logDebug("============================  CANNOT POST TRACK EVENT ============================")
                if name == "None":
                        utm_url = utm_gif_location + "?" + \
                                "utmwv=" + self.addon_version + \
                                "&utmn=" + str(randint(0, 0x7fffffff)) + \
                                "&utmp=" + quote(self.addon_name) + \
                                "&utmac=" + self.ua_track + \
                                "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR, VISITOR, "2"])
                else:
                    if group == "None":
                        utm_url = utm_gif_location + "?" + \
                                "utmwv=" + self.addon_version + \
                                "&utmn=" + str(randint(0, 0x7fffffff)) + \
                                "&utmp=" + quote(self.addon_name + "/" + name) + \
                                "&utmac=" + self.ua_track + \
                                "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR, VISITOR, "2"])
                    else:
                        utm_url = utm_gif_location + "?" + \
                                "utmwv=" + self.addon_version + \
                                "&utmn=" + str(randint(0, 0x7fffffff)) + \
                                "&utmp=" + quote(self.addon_name + "/" + group + "/" + name) + \
                                "&utmac=" + self.ua_track + \
                                "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR, VISITOR, "2"])
                                
                Logger.logDebug("============================ POSTING ANALYTICS ============================")
                self.__send_request_to_google_analytics(utm_url)
                
            except Exception, e:
                Logger.logError(e)
                Logger.logDebug("================  CANNOT POST TO ANALYTICS  ================")
                
                
    def APP_LAUNCH(self):
            versionNumber = int(xbmc.getInfoLabel("System.BuildVersion")[0:2])
            '''
            if versionNumber < 12:
                if xbmc.getCondVisibility('system.platform.osx'):
                    if xbmc.getCondVisibility('system.platform.atv2'):
                        log_path = '/var/mobile/Library/Preferences'
                    else:
                        log_path = os.path.join(os.path.expanduser('~'), 'Library/Logs')
                elif xbmc.getCondVisibility('system.platform.ios'):
                    log_path = '/var/mobile/Library/Preferences'
                elif xbmc.getCondVisibility('system.platform.windows'):
                    log_path = xbmc.translatePath('special://home')
                elif xbmc.getCondVisibility('system.platform.linux'):
                    log_path = xbmc.translatePath('special://home/temp')
                else:
                    log_path = xbmc.translatePath('special://logpath')
                log = os.path.join(log_path, 'kodi.log')
                if not os.path.exists(log):
                    log = os.path.join(log_path, 'xbmc.log')
                logfile = open(log, 'r').read()
                match = re.compile('Starting XBMC \((.+?) Git:.+?Platform: (.+?)\. Built.+?').findall(logfile)
            elif versionNumber > 11:
                Logger.logDebug('======================= more than ====================')
                log_path = xbmc.translatePath('special://logpath')
                log = os.path.join(log_path, 'xbmc.log')
                logfile = open(log, 'r').read()
                match = re.compile('Starting XBMC \((.+?) Git:.+?Platform: (.+?)\. Built.+?').findall(logfile)
            else:
                logfile = 'Starting XBMC (Unknown Git:.+?Platform: Unknown. Built.+?'
                match = re.compile('Starting XBMC \((.+?) Git:.+?Platform: (.+?)\. Built.+?').findall(logfile)
            Logger.logDebug('==========================   ' + self.addon_name + ' ' + self.addon_version + '  ==========================')
            
            from random import randint
            
            from urllib import quote
            VISITOR = self.addon_context.addon.getSetting('ga_visitor')
            for build, PLATFORM in match:
                if re.search('12', build[0:2], re.IGNORECASE): 
                    build = "Frodo" 
                if re.search('11', build[0:2], re.IGNORECASE): 
                    build = "Eden" 
                if re.search('13', build[0:2], re.IGNORECASE): 
                    build = "Gotham" 
                Logger.logDebug(build)
                Logger.logDebug(PLATFORM)
                utm_gif_location = "http://www.google-analytics.com/__utm.gif"
                utm_track = utm_gif_location + "?" + \
                        "utmwv=" + self.addon_version + \
                        "&utmn=" + str(randint(0, 0x7fffffff)) + \
                        "&utmt=" + "event" + \
                        "&utme=" + quote("5(APP LAUNCH*" + build + "*" + PLATFORM + ")") + \
                        "&utmp=" + quote(self.addon_name) + \
                        "&utmac=" + self.ua_track + \
                        "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR, VISITOR, "2"])
                try:
                    Logger.logDebug("============================ POSTING APP LAUNCH TRACK EVENT ============================")
                    self.__send_request_to_google_analytics(utm_track)
                except Exception, e:
                    Logger.logError(e)
                    Logger.logDebug("============================  CANNOT POST APP LAUNCH TRACK EVENT ============================")
            '''
