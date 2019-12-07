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

from resources.lib import sabutils
import sys
import xbmcgui
import xbmcplugin


BASE = sys.argv[0]
HANDLE = int(sys.argv[1])


class PageBuilder:
    def __init__(self):
        self.items = []

    def add(self, **kwargs):
        sabutils.log("PageBuilder: add: kwargs: %s" % kwargs)
        info_labels = kwargs.get('info_labels', {'title':'unknown',})
        path = kwargs.get('path', '')
        cm = kwargs.get('cm', [])
        is_folder = kwargs.get('is_folder', True)
        listitem = xbmcgui.ListItem(info_labels['title'])
        listitem_path = "%s?%s" % (BASE, path)
        listitem.setPath(listitem_path)
        listitem.setInfo(type="video", infoLabels=info_labels)
        listitem.setIconImage("DefaultFile.png")
        listitem.addContextMenuItems(cm, replaceItems=True)
        self.items.append((listitem_path, listitem, is_folder))

    def show(self):
        #items = [(url, listitem, False,)]
        sabutils.log("PageBuilder: show:")
        xbmcplugin.addDirectoryItems(HANDLE, self.items, len(self.items))
        xbmcplugin.setContent(HANDLE, 'files')
        xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_FILE)
        xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_DATE)
        xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_SIZE)
        xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_TITLE)
        xbmcplugin.endOfDirectory(HANDLE, succeeded=True, cacheToDisc=True)


class CmBuilder:
    def __init__ (self):
        self.list = []

    def add(self, title, path):
        sabutils.log("CmBuilder: add: title: %s path: %s" % (title, path))
        cm_path = "%s?%s" % (BASE, path)
        self.list.append([title , "XBMC.RunPlugin(%s)" % (cm_path)])

    def insert_cu(self, pos, title, path):
        sabutils.log("CmBuilder: insert_cu: pos: %s title: %s path: %s" % (pos, title, path))
        self.list.insert(pos, self._cu(title, path))

    def _cu(self, title, path):
        return [title , "XBMC.Container.Update(%s?%s)" % (BASE, path)]

    def add_list(self, list):
        for title, path in list:
            self.add(title, path)
