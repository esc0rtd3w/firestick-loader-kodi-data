"""
 Copyright (c) 2013 Popeye

 Permission is hereby granted, free of charge, to any person
 obtaining a copy of this software and associated documentation
 files (the "Software"), to deal in the Software without
 restriction, including without limitation the rights to use,
 copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the
 Software is furnished to do so, subject to the following
 conditions:

 The above copyright notice and this permission notice shall be
 included in all copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
 OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
 HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
 WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
 OTHER DEALINGS IN THE SOFTWARE.
"""

import os
import urllib
import urllib2
import stat
import xbmc
import xbmcaddon
import xbmcvfs


__settings__ = xbmcaddon.Addon(id='plugin.program.sabnzbd')
__icon__ = __settings__.getAddonInfo("icon")
__userdata__ = xbmc.translatePath(__settings__.getAddonInfo("profile"))

DEBUG_LOG = (__settings__.getSetting("debug_log").lower() == "true")
UA_HEADER = 'Xbmc/14.0 (Addon; plugin.program.sabnzbd)'

def container_refresh():
    xbmc.sleep(500)
    xbmc.executebuiltin("Container.Refresh")

def parent_dir():
    xbmc.executebuiltin("Action(ParentDir)")

def get_parameters(parameterString):
    log("get_parameters: parameterString: %s" % parameterString)
    commands = {}
    splitCommands = parameterString[parameterString.find('?')+1:].split('&')
    for command in splitCommands: 
        if (len(command) > 0):
            splitCommand = command.split('=')
            name = splitCommand[0]
            try:
                value = splitCommand[1]
            except:
                value = ""
            commands[name] = value
    log("get_parameters: commands: %s" % commands)
    return commands

def pass_setup_test(result):
    log("pass_setup_test:")
    pass_test = True
    if result == "ip":
        result = "Wrong ip-number or port"
    if result == "apikey":
        result = "Wrong API key"
    if not result == "ok":
        notification(result, 1000)
        pass_test = False
    log("pass_setup_test: %s" % result)
    return pass_test

def notification(label, duration=500, icon=__icon__):
    xbmc.executebuiltin('Notification("SABnzbd", "%s", %s, %s)' % (label,duration, icon))
    
def quote(name):
    if isinstance(name, unicode):
        return urllib.quote(name.encode('utf-8'))
    else:
        return urllib.quote(name)

def quote_plus(name):
    if isinstance(name, unicode):
        return urllib.quote_plus(name.encode('utf-8'))
    else:
        return urllib.quote_plus(name)

def unquote(name):
    if isinstance(name, unicode):
        return urllib.unquote(name)
    else:
        return unicode(urllib.unquote(name), 'utf-8')

def unquote_plus(name):
    if isinstance(name, unicode):
        return urllib.unquote_plus(name)
    else:
        return unicode(urllib.unquote_plus(name), 'utf-8')

def join(path1, path2):
    path = os.path.join(path1, path2)
    return xbmc.validatePath(path)

def read(file, mode='r', bytes=None):
    try:
        fd = xbmcvfs.File(file, mode)
    except:
        fd = open(file, mode)
    if bytes is not None:
        buffer = fd.read(bytes)
    else:
        buffer = fd.read()
    fd.close()
    return buffer

def size(file):
    try:
        fd = xbmcvfs.File(file)
        size_out = fd.size()
        fd.close()
    except:
        size_out = os.stat(file).st_size
    return size_out

def write(file, buffer, mode='w'):
    try:
        result = write_remote(file, buffer, mode)
        return result
    except:
        result = write_local(file, buffer, mode)
        return result

def write_local(file, buffer, mode='w'):
    fd = open(file, mode)
    result = fd.write(buffer)
    fd.close()
    return result

def write_remote(file, buffer, mode='w'):
    fd = xbmcvfs.File(file, mode)
    result = fd.write(buffer)
    fd.close()
    return result

def copy(source, target):
    return xbmcvfs.copy(source, target)

def delete(file):
    return xbmcvfs.delete(file)

def exists(path):
    # path is a file or folder
    return xbmcvfs.exists(path)

def isfile(path):
    try:
        return stat.S_ISREG(xbmcvfs.Stat(path).st_mode())
    except:
        return os.path.isfile(path)

def isdir(path):
    try:
        return stat.S_ISDIR(xbmcvfs.Stat(path).st_mode())
    except:
        return os.path.isdir(path)

def listdir(path):
    try:
        dirs, files = xbmc_listdir(path)
    except:
        dirs = [f for f in os.listdir(path) if os.path.isdir(join(path,f))]
        files =[f for f in os.listdir(path) if os.path.isfile(join(path,f))]
    return dirs, files

def listdir_dirs(path):
    try:
        dirs, files = xbmc_listdir(path)
    except:
        dirs = [f for f in os.listdir(path) if os.path.isdir(join(path,f))]
    return dirs

def listdir_files(path):
    try:
        dirs, files = xbmc_listdir(path)
    except:
        files = [f for f in os.listdir(path) if os.path.isfile(join(path,f))]
    return files

def xbmc_listdir(path):
    dirs, files = xbmcvfs.listdir(path)
    dirs = [unicode(f, "raw_unicode_escape") for f in dirs]
    files = [unicode(f, "raw_unicode_escape") for f in files]
    return dirs, files

def mkdir(path):
    return xbmcvfs.mkdir(path)

def mkdirs(path):
    # Will create all folders in path if needed
    try:
        xbmcvfs.mkdirs(path)
    except:
        os.makedirs(path)
    return

def rename(file, name):
    return xbmcvfs.rename(file, name)

def rmdir(path):
    return xbmcvfs.rmdir(path)

def log(txt, level=xbmc.LOGDEBUG):
    if DEBUG_LOG:
        level = xbmc.LOGNOTICE
    # Modified from http://forum.xbmc.org/showthread.php?tid=144677
    # Log admits both unicode strings and str encoded with "utf-8" (or ascii). will fail with other str encodings.
    if txt is not None:
        if isinstance (txt,str):
            try:
                txt = txt.decode("utf-8") #if it is str we assume it's "utf-8" encoded.
            except:
                print "plugin.program.sabnzbd:"
                print repr(txt)
        # At this point we are sure txt is a unicode string.
        # Reencode to utf-8 because in many xbmc versions log doesn't admit unicode.
        message = u'plugin.program.sabnzbd: %s' % txt
        xbmc.log(msg=message.encode("utf-8"), level=level)

#From old undertexter.se plugin    
def unikeyboard(default, message):
    log("unikeyboard: default: %s message: %s" % (default, message))
    keyboard = xbmc.Keyboard(default, message)
    keyboard.doModal()
    if (keyboard.isConfirmed()):
        txt = keyboard.getText()
        log("unikeyboard: getText: %s" % txt)
        return txt
    else:
        return None

def load_url(url, req=None, notificationMsg=None):
        log("SABnzbd: load_url: url: %s" % url)
        if req is None:
            req = urllib2.Request(url)
        req.add_header('User-Agent', UA_HEADER)
        doc = None
        try:
            response = urllib2.urlopen(req)
        except urllib2.URLError, ex:
            msg = None
            if hasattr(ex, 'reason'):
                log("SABnzbd: load_url: reason: %s unable to load url: %s" % \
                          (ex.reason, url))
                msg = ex.reason
            elif hasattr(ex, 'code'):
                log("SABnzbd: _load_url: reason: %s unable to load url: %s" % \
                          (ex.code, url))
                msg = ex.code
            if msg is None:
                msg = "SABnzbd unknown communication error"
            notification("%s %s" % (msg, url))
            if notificationMsg is not None:
                notification(notificationMsg)
        else:
            doc = response.read()
            response.close()
        return doc

