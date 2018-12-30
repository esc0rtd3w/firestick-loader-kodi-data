"""
 Copyright (c) 2010, 2011, 2012 Popeye

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

import re
import os
import htmlentitydefs
import urllib
import xbmc
import xbmcgui
import xbmcaddon
import xbmcvfs
import time
import math
import stat
import tempfile
from sabnzbd import Nzf
import rarfile

__settings__ = xbmcaddon.Addon(id='plugin.program.pneumatic')
__icon__ = __settings__.getAddonInfo("icon")
__userdata__ = xbmc.translatePath(__settings__.getAddonInfo("profile"))

DEBUG_LOG = (__settings__.getSetting("debug_log").lower() == "true")

SAB_ADMIN_DIR = "__ADMIN__"
SAB_ADMIN_ATTRIB_FILE = "SABnzbd_attrib"

RE_PART_X = r'(\S*?\.part\d{1,3}\.rar)'
RE_PART01_X = '(\S*?\.part0{0,2}1\.rar)'
RE_R_X = r'(\S*?\.[rs]\d{2,3})$'
RE_RAR_X = r'(\S*?\.rar)'
RE_PART = '\.part\d{2,3}\.rar$'
RE_PART01 = '\.part0{1,2}1\.rar$'
RE_R = '\.[rs]\d{2,3}$'
RE_MOVIE = '\.avi$|\.mkv$|\.iso$|\.img$|\.mp4$'
# https://github.com/sabnzbd/sabnzbd/blob/develop/sabnzbd/constants.py#L142
RE_SAMPLE = r'((^|[\W_])sample\d*[\W_])|(-s\.)'
RE_MKV = '\.mkv$|\.mp4$'
RE_HTML = '&(\w+?);'

RAR_HEADER = "Rar!\x1a\x07\x00"
RAR_MIN_SIZE = 10485760.00

def write_fake(file_list, folder):
    log("write_fake: file_list: %s folder: %s" % (file_list, folder))
    for filebasename in file_list:
        filename = join(folder, filebasename)
        if not exists(filename):
            # make 7 byte file with a rar header
            try:
                write_local(filename, RAR_HEADER, 'wb')
            except:
                write_remote(filename, RAR_HEADER, 'wb')
            log("write_fake: write filename: %s" % filename)
        # Clean out 7 byte files if present
        else:
            if size(filename) == 7:
                delete(filename)
                log("write_fake: delete filename: %s" % filename)
                filename_one = join(folder, ("%s.1" % filebasename))
                if exists(filename_one):
                    rename(filename_one, filename)
                    log("write_fake: rename: %s/%s" % (filename_one, filename))
                filename_one_rar = join(folder, filebasename.replace(".rar", ".1.rar"))
                if exists(filename_one_rar) and filebasename.endswith(".rar"):
                    rename(filename_one_rar, filename)
                    log("write_fake: rename: %s/%s" % (filename_one_rar, filename))
    return

def remove_fake(file_list, folder):
    log("remove_fake: file_list: %s folder: %s" % (file_list, folder))
    for filebasename in file_list:
        filename = join(folder, filebasename)
        if exists(filename):
            if size(filename) == 7:
                delete(filename)
                log("remove_fake: delete filename: %s" % filename)
                filename_one = join(folder, ("%s.1" % filebasename))
                if exists(filename_one):
                    rename(filename_one, filename)
                    log("remove_fake: rename: %s/%s" % (filename_one, filename))
                filename_one_rar = join(folder, filebasename.replace(".rar", ".1.rar"))
                if exists(filename_one_rar) and filebasename.endswith(".rar"):
                    rename(filename_one_rar, filename)
                    log("write_fake: rename: %s/%s" % (filename_one_rar, filename))
    return

def sorted_rar_nzf_file_list(nzf_list):
    file_list = []
    if len(nzf_list) > 0:
        for nzf in nzf_list:
            partrar = re.findall(RE_PART, nzf.filename)
            rrar = re.findall(RE_R, nzf.filename)
            if ((nzf.filename.endswith(".rar") and not partrar) or partrar or rrar) and float(nzf.bytes) > RAR_MIN_SIZE:
                file_list.append(nzf)
            else:
                partrar_x = re.search(RE_PART_X, nzf.filename)
                rrar_x = re.search(RE_R_X, nzf.filename)
                rarrar_x = re.search(RE_RAR_X, nzf.filename)
                out = None
                if (rarrar_x and not partrar_x):
                    out = rarrar_x.group(1)
                elif partrar_x:
                    out = partrar_x.group(1)
                elif rrar_x:
                    out = rrar_x.group(1)
                if out is not None and float(nzf.bytes) > RAR_MIN_SIZE:
                    nzf.filename = out
                    file_list.append(nzf)
        if len(file_list) > 1:
            file_list.sort(key=lambda x: x.filename)
    return file_list

def sorted_movie_nzf_file_list(nzf_list):
    file_list = []
    if len(nzf_list) > 0:
        for nzf in nzf_list:
            movie = re.findall(RE_MOVIE, nzf.filename)
            if movie:
                file_list.append(nzf)
        if len(file_list) > 1:
            file_list.sort(key=lambda x: x.filename)
    return file_list

def sorted_multi_arch_nzf_list(nzf_list):
    file_list = []
    for nzf in nzf_list:
        partrar_x = re.findall(RE_PART_X, nzf.filename)
        part01rar_x = re.findall(RE_PART01_X, nzf.filename)
        rarrar_x = re.search(RE_RAR_X, nzf.filename)
        # No small sub archives
        if ((rarrar_x and not partrar_x) or part01rar_x) and float(nzf.bytes) > RAR_MIN_SIZE:
            file_list.append(nzf)
    if len(file_list) > 1:
        file_list.sort(key=lambda x: x.filename)
    return file_list

def nzf_diff_list(list_a, list_b):
    nzf_list = list(set(list_a)-set(list_b))
    nzf_list.sort(key=lambda x: x.filename)
    return nzf_list

def list_dir(folder):
    log("list_dir: folder: %s" % folder)
    file_list = []
    for filename in listdir_files(folder):
        row = []
        row.append(filename)
        bytes = size(join(folder,filename))
        row.append(bytes)
        log("list_dir: row: %s" % row)
        file_list.append(row)
    return file_list

def dir_to_nzf_list(folder):
    log("dir_to_nzf_list: folder: %s " % folder)
    nzf_list = []
    file_list = list_dir(folder)
    for filename, bytes in file_list:
        nzf = Nzf(filename=filename, bytes=bytes)
        nzf_list.append(nzf)
    return nzf_list

def dir_exists(folder, nzo_id):
    log("dir_exists: folder: %s nzo_id: %s" % (folder, nzo_id))
    if exists_incomplete(folder):
        if nzo_id is None:
            # Clean out a failed SABnzbd folder removal
            if xbmcgui.Dialog().yesno("Pneumatic", "Clear out failed folder: \"%s\"" % os.path.basename(folder)):
                for sub_dir in listdir_dirs(folder):
                    sub_dir_path = join(folder, sub_dir)
                    for sub_file in listdir_files(sub_dir_path):
                        sub_file_path = join(sub_dir_path, sub_file)
                        log("dir_exists: delete: sub_file_path: %s" % sub_file_path)
                        delete(sub_file_path)
                    log('dir_exists: rmdir: sub_dir_path: %s' % sub_dir_path)
                    rmdir(sub_dir_path)
                for file in listdir_files(folder):
                    sub_file_path = join(folder, file)
                    log("dir_exists: delete: sub_file_path: %s" % sub_file_path)
                    delete(sub_file_path)
                log('dir_exists: rmdir: folder: %s' % folder)
                rmdir(folder)
                return False
        return True
    else:
        return False

def rar_filenames(folder, file):
    log("rar_filenames: folder: %s file: %s" % (folder, file))
    temp = tempfile.NamedTemporaryFile('wb', delete=False)
    # read only 1024000 bytes of the remote rar
    buffer = read(join(folder, file), 'rb', 1024000)
    # write it local for rar inspection 
    temp.write(buffer)
    temp_path = temp.name
    temp.close()
    rf = rarfile.RarFile(temp_path)
    delete(temp_path)
    movie_file_list = rf.namelist()
    log("rar_filenames: movie_file_list: %s" % movie_file_list)
    for f in rf.infolist():
        if f.compress_type != 48:
            notification("Compressed rar!")
            log("rar_filenames: Compressed rar")
    return movie_file_list

def is_movie_mkv(movie_list):
    log("is_movie_mkv: movie_list: %s" % movie_list)
    mkv = False
    for movie in movie_list:
        if re.search(RE_MKV, movie, re.IGNORECASE):
            mkv = True
            log("is_movie_mkv: movie is mkv: %s" % movie)
        else:
            log("is_movie_mkv: movie is not mkv: %s" % movie)
    return mkv

def no_sample_list(movie_list):
    log("no_sample_list: movie_list: %s" % movie_list)
    outList = movie_list[:]
    for i in range(len(movie_list)):
        match_sample = re.search(RE_SAMPLE, movie_list[i], re.IGNORECASE)
        match_movie = re.search(RE_MOVIE, movie_list[i], re.IGNORECASE)
        if match_sample or not match_movie:
            outList.remove(movie_list[i])
            log("no_sample_list: outList.remove: %s" % movie_list[i])
    #TODO sort this out.
    #if len(outList) == 0:
        # We return sample if it's the only file left 
    #    outList.append(movie_list[0])
    #   log("no_sample_list: outList.append: %s" % movie_list[0])
    return outList
  
def rarpath_fixer(folder, file):
    log("rarpath_fixer: folder: %s file: %s" % (folder, file))
    filepath = join(folder, file)
    filepath = quote(filepath)
    filepath = filepath.replace(".","%2e")
    filepath = filepath.replace("-","%2d")
    filepath = filepath.replace(":","%3a")
    filepath = filepath.replace("\\","%5c")
    filepath = filepath.replace("/","%2f")
    log("rarpath_fixer: filepath: %s" % filepath)
    return filepath
    
# FROM plugin.video.youtube.beta  -- converts the request url passed on by xbmc to our plugin into a dict  
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

def sort_filename(filename_list):
    log("sort_filename: filename_list: %s" % filename_list)
    outList = filename_list[:]
    if len(filename_list) == 1:
        return outList
    else:
        for i in range(len(filename_list)):
            match = re.search(RE_MOVIE, filename_list[i], re.IGNORECASE)
            if not match:
                outList.remove(filename_list[i])
        if len(outList) == 0:
            outList.append(filename_list[0])
        log("sort_filename: outList: %s" % outList)
        return outList

def descape_entity(m, defs=htmlentitydefs.entitydefs):
    # callback: translate one entity to its ISO Latin value
    try:
        return defs[m.group(1)]
    except KeyError:
        return m.group(0) # use as is

def descape(string):
    pattern = re.compile(RE_HTML)
    return pattern.sub(descape_entity, string)

def pass_setup_test(result, incomplete):
    log("pass_setup_test: result: %s incomplete: %s" % (result, incomplete))
    pass_test = True
    if result == "ip":
        error = "Wrong ip-number or port"
    if result == "apikey":
        error = "Wrong API key"
    #if result == "restart":
    #    error = "Please restart SABnzbd, allow_streaming"
    if not result == "ok":
        xbmcgui.Dialog().ok('Pneumatic - SABnzbd error:', error)
        pass_test = False
    filename = ['plugin.program.pneumatic.test.rar']
    if not incomplete:
            pass_test = False
            xbmcgui.Dialog().ok('Pneumatic', 'No incomplete folder configured')
    try:
        write_fake(filename, incomplete)
    except:
        pass_test = False
        xbmcgui.Dialog().ok('Pneumatic - failed to write test file', 'in incomplete folder')
        log("pass_setup_test: failed to write test file")
    try:
        remove_fake(filename, incomplete)
    except:
        pass_test = False
        xbmcgui.Dialog().ok('Pneumatic - failed to remove test file', 'in incomplete folder')
        log("pass_setup_test: failed to remove test file")
    return pass_test
    
def short_string(input):
    chars = len(input)
    if chars < 52:
        return input
    else:
        output = input[0:33] + "...  ..." + input[(chars-11):(chars)]
        return output

def wait_for_rar_label(nzo, nzf, time_then):
    if nzf is None:
        mb = 1
        mbleft = 0
    else:
        mb = float(nzf.mb)
        mbleft = float(nzf.mbleft)
    s = time.time() - time_then
    if mbleft > 0:
        percent = math.floor(((mb-mbleft)/mb)*100)
    else:
        percent = 100
    if nzo.is_in_queue:
        label = "%.0fs | %.2fMB | %sB/s | Total ETA: %s" % (s, mbleft, nzo.speed, nzo.timeleft)
    else:
        label = "This item is missing from the SABnzb queue"
    return int(percent), label

def notification(label, duration=500, icon=__icon__):
    xbmc.executebuiltin('Notification("Pneumatic", "%s", %s, %s)' % (label,duration, icon))
    
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
    temp = tempfile.NamedTemporaryFile(mode, delete=False)
    result = temp.write(buffer)
    temp_name = temp.name
    temp.close()
    copy(temp_name, file)
    delete(temp_name)
    return result

def copy(source, target):
    return xbmcvfs.copy(source, target)

def delete(file):
    return xbmcvfs.delete(file)

def exists(path):
    # path is a file or folder
    result = xbmcvfs.exists(xbmc.validatePath(path))
    return result == 1

def exists_incomplete(folder):
    incomplete_admin_dir = os.path.join(folder, os.path.join(SAB_ADMIN_DIR, SAB_ADMIN_ATTRIB_FILE))
    return exists(incomplete_admin_dir)

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
                print "plugin.program.pneumatic:"
                print repr(txt)
        # At this point we are sure txt is a unicode string.
        # Reencode to utf-8 because in many xbmc versions log doesn't admit unicode.
        message = u'plugin.program.pneumatic: %s' % txt
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
