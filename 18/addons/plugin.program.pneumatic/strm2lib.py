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
import os
import time
import urllib2
import re
import pickle
import string
import unicodedata

import nfo
import strm

import xbmc
import xbmcgui

from utils import log
from utils import unikeyboard
import utils

def save_strm(settings, nzbname, nzb):
    info = nfo.NfoLabels()
    info_labels = info.info_labels
    m_tvshow = Tvshow(info, settings.getSetting("strm_path_tvshow"),\
               settings.getSetting("lib_save_nfo_type_tvshow").lower(),\
               nzbname, nzb)
    m_movie = Movie(info, settings.getSetting("strm_path_movie"),\
               settings.getSetting("lib_save_nfo_type_movie").lower(),\
               (settings.getSetting("lib_save_nfo_poster").lower() == "true"),\
               (settings.getSetting("lib_save_nfo_fanart").lower() == "true"),\
               nzbname, nzb)
    if 'code' in info_labels and not 'rageid' in info_labels and not 'tvdb-show' in info_labels:
        m_movie.save()
        time.sleep(3)
        xbmc.executebuiltin('UpdateLibrary(video,' + xbmc.translatePath(m_movie.strm_path_movie) + ')')
    elif 'rageid' in info_labels:
        m_tvshow.set_rageid(info_labels['rageid'])
        m_tvshow.save()
        time.sleep(3)
        xbmc.executebuiltin('UpdateLibrary(video,' + xbmc.translatePath(m_tvshow.strm_path) + ')')
    else:
        # Ask what to do and how to save
        type = xbmcgui.Dialog().select('Select library type', ['Movie', 'TV-Show'])
        if type == 1:
            m_tvshow.save()
            time.sleep(3)
            xbmc.executebuiltin('UpdateLibrary(video,' + xbmc.translatePath(m_tvshow.strm_path) + ')')
        else:
            m_movie.save()
            time.sleep(3)
            xbmc.executebuiltin('UpdateLibrary(video,' + xbmc.translatePath(m_movie.strm_path_movie) + ')')
    return

class Tvshow:
    def __init__(self, info, strm_path_tvshow, save_nfo_type, nzbname, nzb, rageid = None):
        self.info = info
        self.strm_path = strm_path_tvshow
        self.save_nfo_type = save_nfo_type
        self.nzbname = nzbname
        self.nzb = nzb 
        self.rageid = rageid

    def set_rageid(self, rageid):
        self.rageid = rageid

    def save(self):
        show_name = None
        if self.rageid is not None:
            show_name = self.rageid_show_name(self.rageid)
            if show_name is not None:
                show_name = unicode(show_name, 'utf-8')
        if show_name is None:
            manual_name = unikeyboard(self.nzbname, 'Enter show name')
            if manual_name is None:
                log("Tvshow: save: did not recieve a name for the TV-show")
                return
            #show_name = manual_name.decode("utf_8").encode("raw_unicode_escape")
            show_name = unicode(manual_name, 'utf-8').replace('\n','')
        strm_path_show = utils.join(self.strm_path, os.path.join(remove_disallowed_filename_chars(show_name),''))
        # Check if showname folder exist in path, if not create it.
        if not utils.exists(strm_path_show):
            try:
                utils.mkdir(strm_path_show)
            except:
                log("Tvshow: save: failed to create TV-show folder %s" % strm_path_show)
                return
        # Check if tvshow.nfo is there, if not, create it.
        tv_nfo = self.info
        tv_nfo.path(strm_path_show)
        # The Episode name has to be picked up by XBMC
        # regexps
        episode_name = self.check_episode_name(self.nzbname)
        if not self.save_nfo_type == "disabled":
            if self.save_nfo_type == "minimal":
                tv_nfo.mini()
            if not utils.exists(os.path.join(strm_path_show, 'tvshow.nfo')):
                tv_nfo.save_tvshow(show_name)
            # now, save the episodename.nfo
            tv_nfo.save_episode(episode_name)
        strm.StrmFile(strm_path_show, episode_name, self.nzb).save()

    def rageid_show_name(self, rageid):
        cache = RageCache(self.strm_path)
        show_name = cache.get_show_name(rageid)
        if show_name is not None:
            return show_name
        else:
            url = "http://services.tvrage.com/tools/quickinfo.php?sid=" + rageid
            req = urllib2.Request(url)
            try:
                response = urllib2.urlopen(req)
            except urllib2.URLError, ex:
                if hasattr(ex, 'reason'):
                    print str(ex.reason) + " " + url
                    return None
                elif hasattr(ex, 'code'):
                    print str(ex.code) + " " + url.real
                    return None
            else:          
                show_name = None
                regex = re.compile("Show Name@(.*)$")
                for line in response:
                    line.rstrip()
                    r = regex.search(line)
                    if r:
                        show_name = r.groups()[0]
                        break
                response.close()
                if show_name is not None:
                    cache.set_show_name(rageid, show_name)
                return show_name

    def check_episode_name(self, nzbname):
        # foo.s01.e01, foo.s01_e01, S01E02 foo, S01 - E02
        regex = re.compile("[Ss]([0-9]+)[][ ._-]*[Ee]([0-9]+)([^\\\\/]*)$")
        r = regex.search(nzbname)
        if r is not None:
            return nzbname
        # foo.ep01, foo.EP_01
        regex = re.compile("[\\._ -]()[Ee][Pp]_?([0-9]+)([^\\\\/]*)$")
        r = regex.search(nzbname)
        if r is not None:
            return nzbname
        # foo.yyyy.mm.dd.* (byDate=true)
        regex = re.compile("([0-9]{4})[\\.-]([0-9]{2})[\\.-]([0-9]{2})")
        r = regex.search(nzbname)
        if r is not None:
            return nzbname
        # foo.mm.dd.yyyy.* (byDate=true)
        regex = re.compile("([0-9]{2})[\\.-]([0-9]{2})[\\.-]([0-9]{4})")
        r = regex.search(nzbname)
        if r is not None:
            return nzbname
        # foo.1x09* or just /1x09*
        regex = re.compile("[\\\\/\\._ \\[\\(-]([0-9]+)x([0-9]+)([^\\\\/]*)$")
        r = regex.search(nzbname)
        if r is not None:
            return nzbname
        # foo.103*, 103 foo
        regex = re.compile("[\\\\/\\._ -]([0-9]+)([0-9][0-9])([\\._ -][^\\\\/]*)$")
        r = regex.search(nzbname)
        if r is not None:
            return nzbname
        # Part I, Pt.VI
        regex = re.compile("[\\/._ -]p(?:ar)?t[_. -]()([ivx]+)([._ -][^\\/]*)$")
        r = regex.search(nzbname)
        if r is not None:
            return nzbname
        if 'season' in self.info.info_labels:
            s = str(self.info.info_labels['season'])
        else: 
            s = xbmcgui.Dialog().numeric(0, 'Season', '1')
            self.info.info_labels['season'] = s
        if 'episode' in self.info.info_labels:
            e = str(self.info.info_labels['episode'])
        else: 
            e = xbmcgui.Dialog().numeric(0, 'Episode', '1')
            self.info.info_labels['episode'] = e
        nzbname = nzbname + ".S" + s + "E" + e
        return nzbname

class RageCache:
    def __init__(self, strm_path):
        self.cache_path = utils.join(strm_path, 'rageid.cache')
        if not utils.exists(self.cache_path):
            pickle.dump( dict(), open( self.cache_path, "wb" ) )

    def get_show_name(self, rageid):
        cache_dict = pickle.load( open( self.cache_path, "rb" ) )
        if rageid in cache_dict:
            return cache_dict[rageid]
        else:
            return None

    def set_show_name(self, rageid, show_name):
        cache_dict = pickle.load( open( self.cache_path, "rb" ) )
        cache_dict[rageid] = show_name
        pickle.dump( cache_dict, open( self.cache_path, "wb" ) )

class Movie:
    def __init__(self, info, strm_path_movie, save_nfo_type, save_poster, save_fanart, nzbname, nzb):
        self.info = info
        self.strm_path_movie = strm_path_movie
        self.strm_path = utils.join(self.strm_path_movie, os.path.join(nzbname, ''))
        self.save_nfo_type = save_nfo_type
        self.save_poster = save_poster
        self.save_fanart = save_fanart
        self.nzbname = nzbname
        self.nzb = nzb

    def save(self):
        if not utils.exists(self.strm_path):
            try:
                utils.mkdir(self.strm_path)
            except:
                log("Movie: save: failed to create folder %s" % self.strm_path)
                return
        movie_nfo = self.info
        movie_nfo.path(self.strm_path)
        if not self.save_nfo_type == "disabled":
            if self.save_nfo_type == "minimal":
                movie_nfo.mini()
            else:
                movie_nfo.save()
        if self.save_poster:
            movie_nfo.save_poster()
        if self.save_fanart:
            movie_nfo.save_fanart()
        strm.StrmFile(self.strm_path, self.nzbname, self.nzb).save()

def remove_disallowed_filename_chars(filename):
    # http://stackoverflow.com/questions/295135/turn-a-string-into-a-valid-filename-in-python
    validFilenameChars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    cleanedFilename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore')
    return ''.join(c for c in cleanedFilename if c in validFilenameChars)
   