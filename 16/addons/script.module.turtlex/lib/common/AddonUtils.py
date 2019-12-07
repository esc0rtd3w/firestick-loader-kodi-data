'''
Created on Nov 23, 2011

@author: ajju
'''
from BeautifulSoup import BeautifulStoneSoup
import os
import xbmc #@UnresolvedImport
import base64
import pickle
import re
try:
    import json
except ImportError:
    import simplejson as json

ADDON_SRC_DATA_FOLDER = 'data'
ADDON_SRC_COOKIE_FOLDER = 'cookies'
ADDON_RESOURCES_FOLDER = 'resources'
ADDON_ART_FOLDER = 'resources/art'

def getCompleteFilePath(baseDirPath, extraDirPath=None, filename=None, makeDirs=False):
    filepath = baseDirPath
    if extraDirPath != None:
        filepath = os.path.join(xbmc.translatePath(filepath), extraDirPath)
    if makeDirs and not doesFileExist(filepath):
        os.makedirs(filepath, mode=0777)
    if filename != None:
        filepath = os.path.join(xbmc.translatePath(filepath), filename)
    return filepath


def doesFileExist(filepath):
    return os.path.exists(filepath)

def deleteFile(filepath):
    if os.path.exists(filepath):
        os.remove(filepath)

def getJsonFileObj(filepath):
    if doesFileExist(filepath):
        fc = open(filepath, 'r')
        jsonObj = json.load(fc, encoding='utf-8')
        fc.close()
        return jsonObj
    else:
        return None
    
    
def saveObjToJsonFile(filepath, obj):
    fc = open(filepath, 'w')
    status = json.dump(obj, fc, encoding='utf-8')
    fc.close()
    return status


def getBeautifulSoupObj(filepath):
    if doesFileExist(filepath):
        fc = open(filepath, 'r')
        beautiful_soup = BeautifulStoneSoup(fc.read(), convertEntities=BeautifulStoneSoup.XML_ENTITIES)
        fc.close()
        return beautiful_soup
    else:
        return None


def getFileLastModifiedTime(filepath):
    if doesFileExist(filepath):
        return os.path.getmtime(filepath)
    else:
        return None

def getBoldString(string):
    return '[B]' + string + '[/B]'

def getBoldItalicString(string):
    return '[B][I]' + string + '[/I][/B]'

def getItalicString(string):
    return '[I]' + string + '[/I]'

def encodeData(data):
    return base64.b64encode(pickle.dumps(data))

def decodeData(data):
    return pickle.loads(base64.b64decode(data))

# Parse p,a,c,k,e,d string for video URL
def parsePackedValue(p, a, c, k):
    while(c >= 1):
        c = c - 1
        if(k[c]):
            
            baseNStr = baseNencode(c, a)
            p = re.sub('\\b' + baseNStr + '\\b', k[c], p)
            
    return p



def baseNencode(number, N):
    if not isinstance(number, (int, long)):
        raise TypeError('number must be an integer')
    if number < 0:
        raise ValueError('number must be positive')

    alphabet = '0123456789abcdefghijklmnopqrstuvwxyz'[0:N]

    baseN = ''
    while number:
        number, i = divmod(number, N)
        baseN = alphabet[i] + baseN

    return baseN or alphabet[0]

def baseNdecode(number, N):
    return int(number, N)     
