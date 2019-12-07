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
import xbmc
import urllib2
from xml.dom.minidom import parseString
import time
from datetime import date

class Cache:
    def __init__(self, path, seconds = 3600):
        cache_path = os.path.join(path, 'cache')
        self.seconds = seconds
        if os.path.exists(path):
            if not os.path.exists(cache_path):
                os.mkdir(cache_path)
            self.path = cache_path
            self._clear_cache()

    def fetch(self, url_in):
        url = Url(url_in, self.path, self.seconds)
        doc, e = self._retrieve_doc(url)
        if e is None:
            obj, e = self._parse_string(doc)
            if e is None:
                return obj, None
            else:
                return None, e
        else:
            return None, e


    def _retrieve_doc(self, url):
        """ Tries loading a url and returning a document"""
        # Here is where the caching begins
        if url.is_old():
            doc, e = self._load_url(url)
            if e is None:
                with open(url.cache, "wb") as out:
                    try:
                        out.write(doc)
                    except:
                        e = "Failed writing %s" % url.cache
            else:
                return None, e
        else:
            with open(url.cache, "rb") as out:
                    try:
                        doc = out.read()
                    except:
                        e = "Failed reading %s" % url.cache
                        return None, e
        return doc, None

    def _load_url(self, url):
        headers = { 'User-Agent' : 'Xbmc/12.0 (Addon; plugin.video.newznab)' }
        req = urllib2.Request(url.real, None, headers)
        try:
            response = urllib2.urlopen(req)
        except urllib2.URLError, ex:
            if hasattr(ex, 'reason'):
                print ex.reason
                e = ex.reason
                e = "%s %s" % (ex.reason, url.real)
                return None, e
            elif hasattr(ex, 'code'):
                e = "%s %s" % (ex.code, url.real)
                return None, e
        else:
            doc = response.read()
            response.close()
            return doc, None

    def _parse_string(self, xml):
        """ Tries parsing a xml document and returning a object"""
        try:
            obj = parseString(xml)
        except:
            e = "Failed parsing xml"
            return None, e
        else:
            return obj, None

    def _clear_cache(self):
        for filename in os.listdir(self.path):
            file = os.path.join(self.path, filename)
            if time.time() - os.path.getmtime(file) > self.seconds:
                # Make sure we dont remove wrong files...
                if ".tbn" in file:
                    try:
                        os.remove(file)
                    except:
                        print "failed removing cache file %s" % file

class Url:
    def __init__(self, url, cache_path, seconds = 3600):
        self.cache_name = xbmc.getCacheThumbName(url)
        self.real = url
        self.path = cache_path
        self.cache = os.path.join(self.path, self.cache_name)
        self.seconds = seconds

    def is_old(self):
        try:
            file_time = os.path.getmtime(self.cache)
        except:
            return True
        else:
            if time.time() - file_time > self.seconds:
                return True
            else:
                return False
