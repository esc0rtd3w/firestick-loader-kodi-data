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
import nfo

def save_nfo(settings, folder):
    info = nfo.NfoLabels()
    info_labels = info.info_labels
    m_episode = Episode(info, folder,\
               settings.getSetting("save_nfo_type_tvshow").lower())
    m_movie = Movie(info, folder,\
               settings.getSetting("save_nfo_type_movie").lower(),\
               (settings.getSetting("save_nfo_poster").lower() == "true"),\
               (settings.getSetting("save_nfo_fanart").lower() == "true"))
    if 'rageid' in info_labels or 'tvdb-show' in info_labels:
        m_episode.save()
    else:
        m_movie.save()
    return

class Episode:
    def __init__(self, info, folder, save_nfo_type):
        self.info = info
        self.folder = folder
        self.save_nfo_type = save_nfo_type

    def save(self):
        ep_nfo = self.info
        ep_nfo.path(self.folder)
        if not self.save_nfo_type == "disabled":
            if self.save_nfo_type == "minimal":
                ep_nfo.mini()
            ep_nfo.save_episode(os.path.join(self.folder, 'episode'))

class Movie:
    def __init__(self, info, folder, save_nfo_type, save_poster, save_fanart):
        self.info = info
        self.folder = folder
        self.save_nfo_type = save_nfo_type
        self.save_poster = save_poster
        self.save_fanart = save_fanart

    def save(self):
        movie_nfo = self.info
        movie_nfo.path(self.folder)
        if not self.save_nfo_type == "disabled":
            if self.save_nfo_type == "minimal":
                movie_nfo.mini()
            else:
                movie_nfo.save()
        if self.save_poster:
            movie_nfo.save_poster()
        if self.save_fanart:
            movie_nfo.save_fanart()
