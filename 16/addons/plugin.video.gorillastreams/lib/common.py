# -*- coding: latin-1 -*-

import os


#------------------------------------------------------------------------------
# xbmc related
#------------------------------------------------------------------------------
import xbmc, xbmcaddon

__settings__ = xbmcaddon.Addon(id='plugin.video.gorillastreams')
__icon__ = xbmcaddon.Addon(id='plugin.video.gorillastreams').getAddonInfo('icon')
translate = __settings__.getLocalizedString
log = xbmc.log
enable_debug = True
language = xbmc.getLanguage

def getSetting(name):
    return __settings__.getSetting(name)

def setSetting(name, value):
    __settings__.setSetting(id=name, value=value)

def showNotification(title, message, timeout=2000, icon=__icon__):
    def clean(s):
        return str(s.encode('utf-8', 'ignore'))
    command = ''
    if icon:
        command = 'Notification(%s,%s,%s,%s)' % (clean(title), clean(message), timeout, icon)
    else:
        command = 'Notification(%s,%s,%s)' % (clean(title), clean(message), timeout)
    xbmc.executebuiltin(command)

def runPlugin(url):
    xbmc.executebuiltin('XBMC.RunPlugin(' + url +')')

#------------------------------------------------------------------------------
# dialogs
#------------------------------------------------------------------------------
from dialogs.dialogQuestion import DialogQuestion
from dialogs.dialogBrowser import DialogBrowser
from dialogs.dialogInfo import DialogInfo
from dialogs.dialogError import DialogError

from utils.xbmcUtils import getKeyboard

def ask(question):
    diaQuestion = DialogQuestion()
    return diaQuestion.ask(question)

def showInfo(message):
    diaInfo = DialogInfo()
    diaInfo.show(message)   

def showError(message):
    diaError = DialogError()
    diaError.show(message)

def browseFolders(head):
    diaFolder = DialogBrowser()
    return diaFolder.browseFolders(head)

def showOSK(defaultText='', title='', hidden=False):
    return getKeyboard(defaultText, title, hidden)

    

#------------------------------------------------------------------------------
# web related
#------------------------------------------------------------------------------
from utils.regexUtils import parseTextToGroups
from utils.webUtils import CachedWebRequest

def getHTML(url, form_data='', referer='', ignoreCache=False, demystify=False):
    cookiePath = xbmc.translatePath(os.path.join(Paths.cacheDir, 'cookies.lwp'))
    request = CachedWebRequest(cookiePath, Paths.cacheDir)
    return request.getSource(url, form_data, referer, ignoreCache, demystify)


def parseWebsite(source, regex, referer='', variables=[]):
    def parseWebsiteToGroups(url, regex, referer=''):
        data = getHTML(url, None, referer)
        return parseTextToGroups(data, regex)

    groups = parseWebsiteToGroups(source, regex, referer)

    if variables == []:
        if groups:
            return groups[0]
        else:
            return ''
    else:
        resultArr = {}
        i = 0
        for v in variables:
            if groups:
                resultArr[v] = groups[i]
            else:
                resultArr[v] = ''
            i += 1
        return resultArr





#------------------------------------------------------------------------------
# classes with constants
#------------------------------------------------------------------------------
class Paths:
    rootDir = xbmc.translatePath(__settings__.getAddonInfo('path')).decode('utf-8')

    cacheDir = os.path.join(rootDir, 'cache')
    resDir = os.path.join(rootDir, 'resources')
    imgDir = os.path.join(resDir, 'images')
    modulesDir = os.path.join(resDir, 'modules')
    catchersDir = os.path.join(resDir,'catchers')
    dictsDir = os.path.join(resDir,'dictionaries')

    pluginFanart = os.path.join(rootDir, 'fanart.jpg')
    defaultVideoIcon = os.path.join(imgDir, 'video.png')
    defaultCategoryIcon = os.path.join(imgDir, 'folder.png')    

    pluginDataDir = xbmc.translatePath(__settings__.getAddonInfo('profile')).decode('utf-8')
    favouritesFolder = os.path.join(pluginDataDir, 'favourites')
    favouritesFile = os.path.join(favouritesFolder, 'favourites.cfg')
    customModulesDir = os.path.join(pluginDataDir, 'custom')
    customModulesFile = os.path.join(customModulesDir, 'custom.cfg')
    
    catchersRepo = 'https://github.com/MusterGit/Dragon Streams-catchers/tree/master/catchers'
    modulesRepo = 'https://github.com/MusterGit/Dragon Streams-modules/tree/master/modules'
    customModulesRepo = 'http://xbmc-development-with-passion.googlecode.com/svn/branches/custom/'
    
    xbmcFavouritesFile = xbmc.translatePath( 'special://profile/favourites.xml' )
