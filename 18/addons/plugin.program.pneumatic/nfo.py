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
import xbmc
import math
import re
import os
from xml.dom.minidom import parseString, Document, _write_data, Node, Element

from utils import log
import utils

class NfoLabels:
    def __init__(self, nfo_path = None):
        info_labels = {
            'size' : unicode(xbmc.getInfoLabel( "ListItem.Size" ), 'utf-8'),
            'tvshowtitle': unicode(xbmc.getInfoLabel( "ListItem.TvShowTitle" ), 'utf-8'),
            'title': unicode(xbmc.getInfoLabel( "ListItem.Title" ), 'utf-8'),
            'genre': unicode(xbmc.getInfoLabel( "ListItem.Genre" ), 'utf-8'),
            'plot': unicode(xbmc.getInfoLabel( "ListItem.Plot" ), 'utf-8'),
            'rating': float(unicode(xbmc.getInfoLabel( "ListItem.Rating" ), 'utf-8') or "0"),
            'aired': unicode(xbmc.getInfoLabel( "ListItem.Premiered" ), 'utf-8'),
            'mpaa': unicode(xbmc.getInfoLabel( "ListItem.MPAA" ), 'utf-8'),
            'duration': unicode(xbmc.getInfoLabel( "ListItem.Duration" ), 'utf-8'),
            'studio': unicode(xbmc.getInfoLabel( "ListItem.Studio" ), 'utf-8'),
            'cast': unicode(xbmc.getInfoLabel( "ListItem.Cast" ), 'utf-8'),
            'writer': unicode(xbmc.getInfoLabel( "ListItem.Writer" ), 'utf-8'),
            'director': unicode(xbmc.getInfoLabel( "ListItem.Director" ), 'utf-8'),
            'season': int(xbmc.getInfoLabel( "ListItem.Season" ) or "-1"),
            'episode': int(xbmc.getInfoLabel( "ListItem.Episode" ) or "-1"),
            'year': int(xbmc.getInfoLabel( "ListItem.Year" ) or "-1"),
            }
        # Clear empty keys
        for key in info_labels.keys():
            if(info_labels[key] == -1):
                del info_labels[key]
            try:
                if (len(info_labels[key])<1):
                    del info_labels[key]
            except:
                pass
        try:
            info_labels['size'] = self._size_to_bytes(info_labels['size'])
        except:
           pass
        try:
            code = self._code_from_plot(info_labels['plot'])
            if code:
                info_labels['code'] = code
        except:
            pass
        try:
            rageid = self._rageid_from_plot(info_labels['plot'])
            if rageid:
                info_labels['rageid'] = rageid
        except:
            pass
        try:
            tvdb = self._tvdb_from_plot(info_labels['plot'])
            if tvdb:
                info_labels['tvdb-show'] = tvdb
        except:
            pass
        try:
            info_labels['cast'] = info_labels['cast'].split('\n')
        except:
            pass
        if not 'title' in info_labels:
            if nfo_path:
                info_labels['title'] = os.path.basename(nfo_path)
            else:
                info_labels['title'] = 'Unknown'
        self.info_labels = info_labels
        self.fanart = unicode(xbmc.getInfoImage( "Listitem.Property(Fanart_Image)" ), 'utf-8')
        self.thumbnail = unicode(xbmc.getInfoImage( "ListItem.Thumb" ), 'utf-8')
        self.nfo_path = nfo_path
        self.is_mini = False

    def path(self, nfo_path):
        self.nfo_path = nfo_path

    def _size_to_bytes(self, size_str):
        conversion = {'K' : 1024,
                      'M' : 1048576,
                      'G' : 1073741824,}
        RE_GMK = ('(\w[GMK]?)B')
        RE_DIGIT = ('(\d*\.?\d*)')
        re_obj_gmk = re.compile(RE_GMK)
        re_obj_digit = re.compile(RE_DIGIT)
        gmk = re_obj_gmk.search(size_str)
        unit = 1
        if gmk:
            unit = conversion[gmk.groups()[0]]
        digit = re_obj_digit.search(size_str)
        if digit:
            size = int(math.floor((float(digit.groups()[0]) * unit)))
        else:
            size = 0
        return size

    def _code_from_plot(self, plot):
        RE_CODE = ('imdb:(t*\d*)')
        re_obj_code = re.compile(RE_CODE)
        code = re_obj_code.search(plot).groups()
        if code:
            code = code[0]
            return code
        else:
            return None

    def _rageid_from_plot(self, plot):
        RE_RAGE = ('rage:(\d*)')
        re_obj_rage = re.compile(RE_RAGE)
        rage = re_obj_rage.search(plot).groups()
        if rage:
            rage = rage[0]
            return rage
        else:
            return None

    def _tvdb_from_plot(self, plot):
        RE_TVDB = ('tvdb:(\d*)')
        re_obj_tvdb = re.compile(RE_TVDB)
        tvdb = re_obj_tvdb.search(plot).groups()
        if tvdb:
            tvdb = tvdb[0]
            return tvdb
        else:
            return None

    def mini(self, bool = True):
        self.is_mini = bool

    def save(self, type = 'movie', filename = 'movie.nfo'):
        """Saves XBMC .nfo xml data.
        
        type is a string of 'movie' or 'tvshow' or 'episodedetails'
        """
        filepath = utils.join(self.nfo_path, filename)
        if self.is_mini and type == 'movie' and 'code' in self.info_labels:
            doc = 'http://www.imdb.com/title/%s' % self.info_labels['code']
            self.write_doc(filepath, doc)
        if self.is_mini and type == 'tvshow' and 'tvdb-show' in self.info_labels:
            doc = 'http://thetvdb.com/index.php?tab=series&id=%s' % self.info_labels['tvdb-show']
            self.write_doc(filepath, doc)
        else:
            self.write_doc(filepath, self.to_xml(type))
    
    def write_doc(self, filepath, doc):
        try: 
            utils.write(filepath, doc, 'wb')
        except:
            log("write_doc: failed to create .nfo file: %s" % \
                     xbmc.translatePath(filepath))
    
    def to_xml(self, type):
        """Creates XBMC .nfo xml data.
        
        type is a string of 'movie' or 'tvshow' or 'episodedetails'
        """
        # from http://www.postneo.com/projects/pyxml/
        doc = Document()
        base = doc.createElement(type)
        doc.appendChild(base)
        for key, value in self.info_labels.iteritems():
            if (key == 'size') or (key == 'season') or (key == 'episode') or (key == 'year') or (key == 'rating'):
                value = str(value)
            if type != 'movie' and key == 'plot':
                continue
            if type == 'tvshow' and (key == 'size' or key == 'aired'):
                continue
            if type == 'episodedetails':   
                if key == 'title' and 'tvshowtitle' in self.info_labels:
                    continue
                if 'tvshowtitle' in key:
                    key = 'title'
                if key == 'season' and not 'episode' in self.info_labels:
                    continue
                if key == 'episode' and not 'season' in self.info_labels:
                    continue
            else:
                if key == 'season' or key == 'episode' or key == 'tvshowtitle':
                    continue
            if key == 'code':
                if type == 'movie':
                    key = 'id'
                else:
                    continue
            if  key == 'tvdb-show':
                if type != 'movie':
                    key = 'id'
                else:
                    continue
            if key == 'cast' and type != 'tvshow':
                for actor in value:
                    actor_element = doc.createElement('actor')
                    name_element = doc.createElement('name')
                    actor_element.appendChild(name_element)
                    name_element.appendChild(doc.createTextNode(actor.lstrip()))
                    base.appendChild(actor_element)
            else:
                element = doc.createElement(key)
                element.appendChild(doc.createTextNode(value))
                base.appendChild(element)
        doc = doc.toprettyxml(indent="  ", encoding='utf-8')
        return doc
            
    def writexml(self, writer, indent="", addindent="", newl=""):
        # http://ronrothman.com/public/leftbraned/xml-dom-minidom-toprettyxml-and-silly-whitespace/
        writer.write(indent+"<" + self.tagName)
        attrs = self._get_attributes()
        a_names = attrs.keys()
        a_names.sort()
        for a_name in a_names:
            writer.write(" %s=\"" % a_name)
            _write_data(writer, attrs[a_name].value)
            writer.write("\"")
        if self.childNodes:
            if len(self.childNodes) == 1 \
              and self.childNodes[0].nodeType == Node.TEXT_NODE:
                writer.write(">")
                self.childNodes[0].writexml(writer, "", "", "")
                writer.write("</%s>%s" % (self.tagName, newl))
                return
            writer.write(">%s" % (newl))
            for node in self.childNodes:
                node.writexml(writer, indent+addindent, addindent, newl)
            writer.write("%s</%s>%s" % (indent, self.tagName, newl))
        else:
            writer.write("/>%s" % (newl))

    # monkey patch to fix whitespace issues with toprettyxml
    Element.writexml = writexml

    def save_tvshow(self, show_name):
        if not 'tvshowtitle' in self.info_labels:
            self.info_labels['tvshowtitle'] = self.info_labels['title']
        self.info_labels['title'] = show_name
        self.save('tvshow', 'tvshow.nfo')

    def save_episode(self, nzbname):
        nzbname = nzbname + '.nfo'
        self.save('episodedetails', nzbname)

    def save_poster(self):
        thumbnail_dest = utils.join(self.nfo_path, 'folder.jpg')
        try:
            utils.copy(xbmc.translatePath(self.thumbnail), thumbnail_dest)
            log("save_poster: wrote: %s" %  xbmc.translatePath(thumbnail_dest))
        except:
            log("save_poster: failed to write: %s from: %s" %  \
                    (xbmc.translatePath(self.thumbnail), xbmc.translatePath(thumbnail_dest)))

    def save_fanart(self):
        cached_fanart = xbmc.getCacheThumbName(self.fanart).replace('.tbn', '')
        cached_fanart = "special://profile/Thumbnails/%s/%s.jpg" % (cached_fanart[0], cached_fanart)
        fanart_dest = utils.join(self.nfo_path, 'fanart.jpg')
        try:
            utils.copy(xbmc.translatePath(cached_fanart), xbmc.translatePath(fanart_dest))
            log("save_fanart: wrote: %s from: %s" % \
                    (xbmc.translatePath(fanart_dest), xbmc.translatePath(cached_fanart)))
        except:
            log("save_fanart: failed to write: %s from: %s" % \
                    (xbmc.translatePath(fanart_dest), xbmc.translatePath(cached_fanart)))

class ReadNfoLabels:
    def __init__(self, nfo_path):
        self.nfo_path = nfo_path
        filename_movie = utils.join(self.nfo_path, ('movie.nfo'))
        filename_tvshow = utils.join(self.nfo_path, ('episode.nfo'))
        self.is_episode = False
        if utils.exists(filename_movie):
            filename = filename_movie
        elif utils.exists(filename_tvshow):
            filename = filename_tvshow
            self.is_episode = True
        try:
            out = parseString(utils.read(filename, 'r'))
        except:
            log(("ReadNfoLabels: could not open: %s.nfo") % \
                    (xbmc.translatePath(self.nfo_path)))
            out = None
        if out:
            self.info_labels = self._get_info_labels(out)
        else:
            self.info_labels = {'title': os.path.basename(self.nfo_path)}
        self.thumbnail = utils.join(self.nfo_path, 'folder.jpg')
        self.fanart = utils.join(self.nfo_path, 'fanart.jpg')

    def _get_info_labels(self, doc):
        info_labels = dict()
        items = doc.getElementsByTagName("movie")
        if not items:
            items = doc.getElementsByTagName("tvshow")
        if not items:
            items = doc.getElementsByTagName("episodedetails")
        for item in items:
            info_labels['size'] = int(self._get_node_value(item, "size") or "-1")
            if self.is_episode:
                info_labels['tvshowtitle'] = (unicode(self._get_node_value(item, "title"), 'utf-8') or "")
                info_labels['title'] = unicode(os.path.basename(xbmc.translatePath(self.nfo_path)), 'utf-8')
            else:
                info_labels['tvshowtitle'] = (unicode(self._get_node_value(item, "tvshowtitle"), 'utf-8') or "")
                info_labels['title'] = (unicode(self._get_node_value(item, "title"), 'utf-8'))
            info_labels['genre'] = unicode(self._get_node_value(item, "genre"), 'utf-8')
            info_labels['plot'] = unicode(self._get_node_value(item, "plot"), 'utf-8')
            info_labels['rating'] = float(unicode(self._get_node_value(item, "rating"), 'utf-8') or "0")
            info_labels['aired'] = unicode(self._get_node_value(item, "aired"), 'utf-8')
            info_labels['mpaa'] = unicode(self._get_node_value(item, "mpaa"), 'utf-8')
            info_labels['duration'] = unicode(self._get_node_value(item, "duration"), 'utf-8')
            info_labels['studio'] = unicode(self._get_node_value(item, "studio"), 'utf-8')
            info_labels['cast'] = []
            for cast in item.getElementsByTagName("actor"):
                info_labels['cast'].append(unicode(self._get_node_value(cast, "name"), 'utf-8'))
            info_labels['writer'] = unicode(self._get_node_value(item, "writer"), 'utf-8')
            info_labels['director'] = unicode(self._get_node_value(item, "director"), 'utf-8')
            info_labels['season'] = int(self._get_node_value(item, "season") or "-1")
            info_labels['episode'] = int(self._get_node_value(item, "episode") or "-1")
        # Clear empty keys
        for key in info_labels.keys():
            if(info_labels[key] == -1):
                del info_labels[key]
            try:
                if (len(info_labels[key])<1):
                    del info_labels[key]
            except:
                pass
        return info_labels

    def _get_node_value(self, parent, name, ns=""):
        if ns:
            try:
                return parent.getElementsByTagNameNS(ns, name)[0].childNodes[0].data.encode('utf-8')
            except:
                return ""
        else:
            try:
                return parent.getElementsByTagName(name)[0].childNodes[0].data.encode('utf-8')            
            except:
                return ""