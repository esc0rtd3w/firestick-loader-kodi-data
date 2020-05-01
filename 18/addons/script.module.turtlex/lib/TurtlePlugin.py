'''
Created on Oct 16, 2011

@author: ajju
'''
from TurtleContainer import Container
from common import ExceptionHandler, Logger, HttpUtils, XBMCInterfaceUtils
import urllib2
import sys
import xbmcplugin  # @UnresolvedImport

__addon_id__ = None
__addon_ver__ = None

def start(addon_id, addon_ver=None):
    try:
        Logger.logDebug(sys.argv)
        global __addon_id__
        __addon_id__ = addon_id
        __addon_ver__ = addon_ver
        
        containerObj = Container(addon_id=addon_id, addon_ver=addon_ver)
        action_id = containerObj.getTurtleRequest().get_action_id()
        containerObj.performAction(action_id)
    except urllib2.URLError, e:
        Logger.logFatal(e)
        XBMCInterfaceUtils.displayDialogMessage('Unable to connect', 'Please choose a different source if available in add-on.', 'Website used in add-on is down, try to access using web browser.', 'Please share logs with developer if problem keeps coming!')
    except Exception, e:
        Logger.logFatal(e)
        ExceptionHandler.handle(e)
    cleanUp()
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def cleanUp():
    try:
        containerObj = Container()
        containerObj.cleanUp()
        del containerObj
        httpClient = HttpUtils.HttpClient()
        httpClient.cleanUp()
        del httpClient
    except:
        pass
    
