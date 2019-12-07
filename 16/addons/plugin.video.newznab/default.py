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

import sys
import urllib
import re
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
import os
import pickle
import time
from email.utils import parsedate

import cache

__settings__ = xbmcaddon.Addon(id='plugin.video.newznab')
__language__ = __settings__.getLocalizedString

USERDATA_PATH = xbmc.translatePath(__settings__.getAddonInfo("profile"))
CACHE_TIME = int(__settings__.getSetting("cache_time"))*60
CACHE = cache.Cache(USERDATA_PATH, CACHE_TIME)

PNEUMATIC = "plugin://plugin.program.pneumatic"

NS_REPORT = "http://www.newzbin.com/DTD/2007/feeds/report/"
NS_NEWZNAB = "http://www.newznab.com/DTD/2010/feeds/attributes/"

MODE_PNEUMATIC_PLAY = "play"
MODE_PNEUMATIC_DOWNLOAD = "download"
MODE_PNEUMATIC_INCOMPLETE = "incomplete"
MODE_PNEUMATIC_LOCAL = "local"
MODE_PNEUMATIC_SAVE_STRM = "save_strm"

MODE_INDEX = "index"
MODE_HIDE = "hide"
MODE_CART = "cart"
MODE_CART_DEL = "cart_del"
MODE_CART_ADD = "cart_add"
MODE_SEARCH = "search"
MODE_SEARCH_RAGEID = "search_rageid"
MODE_SEARCH_IMDB = "search_imdb"
MODE_FAVORITES = "favorites"
MODE_FAVORITES_TOP = "favorites_top"
MODE_FAVORITE_ADD = "favorites_add"
MODE_FAVORITE_DEL = "favorites_del"

MODE_NEWZNAB = "newznab"
MODE_NEWZNAB_SEARCH = "newznab&newznab=search"
MODE_NEWZNAB_SEARCH_RAGEID = "newznab&newznab=search_rageid"
MODE_NEWZNAB_SEARCH_IMDB = "newznab&newznab=search_imdb"
MODE_NEWZNAB_MYCART = "newznab&newznab=mycart"
MODE_NEWZNAB_MYSHOWS = "newznab&newznab=myshows"
MODE_NEWZNAB_MYMOVIES = "newznab&newznab=mymovies"

def get_http_string(index):
    if __settings__.getSetting("newznab_https_%s" % index).lower() == "true":
        return "https://"
    else:
        return "http://"

def site_caps(index):
    url = get_http_string(index) + __settings__.getSetting("newznab_siteapi_%s" % index) + "/api?t=caps" + \
          "&apikey=" + __settings__.getSetting("newznab_key_%s" % index)
    doc, state = load_xml(url)
    if doc and not state:
        table = []
        for category in doc.getElementsByTagName("category"):
            row = []
            row.append(category.getAttribute("name"))
            row.append(category.getAttribute("id"))
            table.append(row)
            if category.getElementsByTagName("subcat"):
                for subcat in category.getElementsByTagName("subcat"):
                    row = []
                    row.append((" - " + subcat.getAttribute("name")))
                    row.append(subcat.getAttribute("id"))
                    table.append(row)
        return table
    else:
        return None

def newznab(index, params = None):
    newznab_rss = (get_http_string(index) + __settings__.getSetting("newznab_siterss_%s" % index) +
                   "/rss?dl=1&num=100&i=" + __settings__.getSetting("newznab_id_%s" % index) + "&r=" +
                   __settings__.getSetting("newznab_key_%s" % index))
    newznab_search_api = (get_http_string(index) + __settings__.getSetting("newznab_siteapi_%s" % index) +
                          "/api?dl=1&limit=100&extended=1&apikey=" + __settings__.getSetting("newznab_key_%s" % index))
    hide_cat = __settings__.getSetting("newznab_hide_cat_%s" % index)
    if params:
        get = params.get
        catid = get("catid")
        newznab_id = get("newznab")
        url = get("url")
        if url:
            url_out = urllib.unquote_plus(url)
        else:
            url_out = None
        get_offset = get("offset")
        if newznab_id:
            if newznab_id == "mycart":
                url_out = newznab_rss + "&t=-2"
            if newznab_id == "myshows":
                url_out = newznab_rss + "&t=-3"
            if newznab_id == "mymovies":
                url_out = newznab_rss + "&t=-4"
            if newznab_id == "search":
                search_term = search(__settings__.getSetting("newznab_name_%s" % index), index)
                if search_term:
                    url_out = (newznab_search_api + "&t=search" + "&cat=" + catid + "&q="
                    + search_term + "&extended=1")
            if newznab_id == "search_rageid":
                rageid = get('rageid')
                url_out = (newznab_search_api + "&t=tvsearch" + "&rid=" + rageid + "&extended=1")
                if catid:
                    url_out = url_out + "&cat=" + catid
            if newznab_id == "search_imdb":
                imdb = get('imdb')
                url_out = (newznab_search_api + "&t=movie" + "&imdbid=" + imdb + "&extended=1")
        elif catid:
            url_out = "%s&t=search&cat=%s" % (newznab_search_api, catid)
            #
            key = "&catid=" + catid
            add_posts({'title' : 'Search...',}, index, url=key, mode=MODE_NEWZNAB_SEARCH)
        if url_out:
            offset = list_feed_newznab(url_out, index)
            if offset is not None and not '/rss?' in url_out:
                if offset >= 100:
                    offset_url = re.search(r'&offset=(\d{1,3})', url_out, re.IGNORECASE|re.DOTALL)
                    if offset_url:
                        offset_new = int(offset_url.group(1)) + 100
                        next_url = re.sub(r'(&offset=)\d{1,3}', r'\g<1>%s' % str(offset_new), url_out)
                    else:
                        next_url = '%s&offset=100' % url_out
                    next_url = "&url=%s" % urllib.quote_plus(next_url)
                    add_posts({'title' : "Next..",}, index, url=next_url, mode=MODE_NEWZNAB)
        the_end(catid)
    else:
        table = site_caps(index)
        if table is not None:
            for name, m_catid in table:
                if not re.search(hide_cat, m_catid, re.IGNORECASE) or not hide_cat:
                    key = "&catid=" + str(m_catid)
                    add_posts({'title' : name,}, index, url=key, mode=MODE_NEWZNAB)
        add_posts({'title' : "My Cart",}, index, mode=MODE_NEWZNAB_MYCART)
        add_posts({'title' : "My Shows",}, index, mode=MODE_NEWZNAB_MYSHOWS)
        add_posts({'title' : "My Movies",}, index, mode=MODE_NEWZNAB_MYMOVIES)
        add_posts({'title' : "Search Favorites",}, index, mode=MODE_FAVORITES_TOP)
        the_end()
    return

def list_feed_newznab(feedUrl, index):
    doc, state = load_xml(feedUrl)
    if doc and not state:
        url_params = get_parameters(feedUrl)
        t = url_params.get('t', None)
        q = url_params.get('q', None)
        if 't=-2' in feedUrl:
            mode = MODE_CART
        elif t == 'search' and q is not None:
            mode = MODE_SEARCH
            search_url = urllib.quote_plus(feedUrl)
            search_term = q
        elif 't=tvsearch' in feedUrl:
            mode = MODE_SEARCH_RAGEID
            search_url = urllib.quote_plus(feedUrl)
        elif 't=movie' in feedUrl:
            mode = MODE_SEARCH_IMDB
        else:
            mode = MODE_PNEUMATIC_PLAY
        items = doc.getElementsByTagName("item")
        offset = len(items)
        for item in items:
            info_labels = dict()
            info_labels['title'] = get_node_value(item, "title")
            #trailer_name, trailer_year = xbmc.getCleanMovieTitle(info_labels['title'])
            #trailer = "%s %s" % (trailer_name, trailer_year)
            #info_labels['trailer'] = "plugin://plugin.video.newznab/?mode=trailer&trailer=%s" % urllib.quote_plus(trailer)
            attribs = dict()
            for attr in item.getElementsByTagName("newznab:attr"):
                attribs[attr.getAttribute("name")] = attr.getAttribute("value")
            usenetdate = attribs.get('usenetdate', 'Fri, 13 Feb 2009 23:31:30 +0000')
            time_tuple = parsedate(usenetdate)
            info_labels['date'] = time.strftime("%d.%m.%Y", time_tuple)
            info_labels['dateadded'] = time.strftime("%Y-%m-%d %H:%M:%S", time_tuple)
            info_labels['videocodec'] = attribs.get('video', "")
            resolution = attribs.get('resolution', "0x0 0:0")
            RE_RESOLUTION = r'(\d+)x(\d+) (.+:.+)'
            res_res = re.search(RE_RESOLUTION, resolution)
            info_labels['videoresolutionwidth'] = res_res.group(1)
            info_labels['videoresolutionheight'] = res_res.group(2)
            info_labels['videoaspect'] = res_res.group(3)
            info_labels['size'] = int(attribs.get('size', 0))
            info_labels['rating'] = float(attribs.get('imdbscore', 0))
            info_labels['originaltitle'] = attribs.get('imdbtitle', info_labels['title'])
            info_labels['tagline'] = attribs.get('imdbtagline', "")
            info_labels['plot'] = attribs.get('imdbplot', "")
            info_labels['year'] = attribs.get('imdbyear', "")
            info_labels['director'] = attribs.get('imdbdirector', "").replace("|", ", ")
            info_labels['cast'] = list(tuple((attribs.get('imdbactors', "").replace("|", ", ").split(","))))
            info_labels['genre'] = attribs.get('genre', "").replace("|", ", ")
            info_labels['code'] = attribs.get('imdb', None)
            if info_labels['code'] is not None:
                info_labels['code'] = "tt%s" % info_labels['code']
                # Append imdb id to the plot. Picked up by plugin.program.pneumatic
                text = "%s imdb:%s" % (info_labels['plot'], info_labels['code'])
                info_labels['plot'] = text
            info_labels['rageid'] = attribs.get('rageid', None)
            if info_labels['rageid'] is not None:
                # Append rageid to the plot. Picked up by plugin.program.pneumatic
                text = "%s rage:%s" % (info_labels['plot'], info_labels['rageid'])
                info_labels['plot'] = text
            regex = re.compile("([1-9]?\d$)")
            try:
                info_labels['season'] = int(regex.findall(attribs['season'])[0])
            except:
                pass
            try:
                info_labels['episode'] = int(regex.findall(attribs['episode'])[0])
            except:
                pass
            try:
                info_labels['tvshowtitle'] = attribs['tvtitle']
            except:
                pass
            aired = attribs.get('tvairdate', None)
            if aired is not None:
                time_tuple = parsedate(aired)
                info_labels['aired'] = time.strftime("%Y-%m-%d", time_tuple)
            try:
                info_labels['category'] = attribs['category']
            except:
                pass
            nzb = get_node_value(item, "link")
            thumb = attribs.get('coverurl', "")
            info_labels['backdropcoverurl'] = attribs.get('backdropcoverurl', "")
            is_hd = (False, True)[re.search("(720p|1080p)", info_labels['title'], re.IGNORECASE) is not None]
            if is_hd:
                info_labels['overlay'] = 8
                info_labels['videoresolutionheight'] = "720"
                info_labels['videoaspectratio'] = "16:9"
                info_labels['videocodec'] = "x264"
            nzb = "&nzb=" + urllib.quote_plus(nzb) + "&nzbname=" + urllib.quote_plus(info_labels['title'])
            if mode == MODE_SEARCH:
                nzb = nzb + "&search_url=" + search_url + "&search_term=" + search_term
            if mode == MODE_SEARCH_RAGEID:
                nzb = nzb + "&search_url=" + search_url
            # Clear empty keys
            for key in info_labels.keys():
                if(info_labels[key] == -1) or info_labels[key] is None:
                    del info_labels[key]
                try:
                    if (len(info_labels[key])<1):
                        del info_labels[key]
                except:
                    pass
            add_posts(info_labels, index, url=nzb, mode=mode, thumb=thumb)
        return offset
    else:
        if state == "site":
            xbmc.executebuiltin('Notification("Newznab","Site down")')
        else:
            xbmc.executebuiltin('Notification("Newznab","Malformed result")')
    return None

def add_posts(info_labels, index, **kwargs):
    url = ''
    if 'url' in kwargs:
        url = kwargs['url']
    mode = ''
    if 'mode' in kwargs:
        mode = kwargs['mode']
    thumb = ''
    if 'thumb' in kwargs:
        thumb = kwargs['thumb']
    folder = True
    if 'folder' in kwargs:
        folder = kwargs['folder']
    listitem=xbmcgui.ListItem(info_labels['title'], iconImage="DefaultVideo.png", thumbnailImage=thumb)
    fanart = info_labels.get('backdropcoverurl', "") #thumb.replace('-cover','-backdrop')
    listitem.setProperty("Fanart_Image", fanart)
    ###
    # if 'videoresolution' in info_labels:
    #    listitem.addStreamInfo('video', {'codec': info_labels['videocodec'],
    #                                     'height': info_labels['videoresolution'],
    #                                     'aspect': info_labels['videoaspectratio']})
    #    listitem.addStreamInfo('audio', {'channels': 7, 'codec' : 'dts'})
    ###
    if mode == MODE_NEWZNAB:
        cm = []
        cm.append(cm_build("Hide", MODE_HIDE, url, index))
        listitem.addContextMenuItems(cm, replaceItems=True)
    if mode == MODE_PNEUMATIC_PLAY or mode == MODE_CART or mode == MODE_SEARCH or\
       mode == MODE_SEARCH_RAGEID or mode == MODE_SEARCH_IMDB:
        mode_out = mode
        cm = []
        if (xbmcaddon.Addon(id='plugin.program.pneumatic').getSetting("auto_play").lower() == "true"):
            folder = False
        cm_url_download = PNEUMATIC + '?mode=' + MODE_PNEUMATIC_DOWNLOAD + url
        cm.append(("Download", "XBMC.RunPlugin(%s)" % (cm_url_download)))
        cm_url_strm = PNEUMATIC + '?mode=' + MODE_PNEUMATIC_SAVE_STRM + url
        cm.append(("Save to XBMC library", "XBMC.RunPlugin(%s)" % (cm_url_strm)))
        if mode == MODE_CART:
            cm.append(cm_build("Remove from cart", MODE_CART_DEL, url, index))
            mode_out = MODE_PNEUMATIC_PLAY
        else:
            cm_mode = MODE_CART_ADD
            cm.append(cm_build("Add to cart", MODE_CART_ADD, url, index))
        if mode == MODE_SEARCH:
            cm.append(cm_build("Add to search favorites", MODE_FAVORITE_ADD, url, index))
            mode_out = MODE_PNEUMATIC_PLAY
        if mode == MODE_SEARCH_RAGEID:
            cm.append(cm_build("Add to search favorites", MODE_FAVORITE_ADD, url, index))
            mode_out = MODE_PNEUMATIC_PLAY
        if 'rageid' in info_labels:
            if mode != MODE_SEARCH_RAGEID:
                url_search_rage = '&rageid=' + info_labels['rageid']
                cm.append(("Search for this show", "XBMC.Container.Update(%s?mode=%s%s&index=%s)" %\
                          (sys.argv[0], MODE_NEWZNAB_SEARCH_RAGEID, url_search_rage, index)))
            if mode == MODE_SEARCH_RAGEID:
                url_search_rage = '&rageid=' + info_labels['rageid'] + "&catid=" + info_labels['category']
                cm.append(("Search for this quality", "XBMC.Container.Update(%s?mode=%s%s&index=%s)" %\
                          (sys.argv[0], MODE_NEWZNAB_SEARCH_RAGEID, url_search_rage, index)))
        if 'imdb' in info_labels:
            url_search_imdb = '&imdb=' + info_labels['imdb']
            cm.append(("Search for this movie", "XBMC.Container.Update(%s?mode=%s%s&index=%s)" %\
                     (sys.argv[0], MODE_NEWZNAB_SEARCH_IMDB, url_search_imdb, index)))
        if mode == MODE_SEARCH_IMDB:
            mode_out = MODE_PNEUMATIC_PLAY
        listitem.addContextMenuItems(cm, replaceItems=True)
        xurl = "%s?mode=%s" % (PNEUMATIC,mode_out)
    elif mode == MODE_FAVORITES:
        cm = []
        cm.append(cm_build("Remove from search favorites", MODE_FAVORITE_DEL, url, index))
        listitem.addContextMenuItems(cm, replaceItems=True)
        xurl = "%s?mode=%s&index=%s" % (sys.argv[0], MODE_NEWZNAB, index)
    elif mode == MODE_PNEUMATIC_INCOMPLETE:
        xurl = "%s?mode=%s" % (PNEUMATIC,mode)
    elif mode == MODE_PNEUMATIC_LOCAL:
        xurl = "%s?mode=%s" % (PNEUMATIC,mode)
    else:
        xurl = "%s?mode=%s&index=%s" % (sys.argv[0], mode, index)
    xurl = xurl + url
    listitem.setInfo(type="Video", infoLabels=info_labels)
    listitem.setPath(xurl)
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=xurl, listitem=listitem, isFolder=folder)

def cm_build(label, mode, url, index):
    command = "XBMC.RunPlugin(%s?mode=%s%s&index=%s)" % (sys.argv[0], mode, url, index)
    out = (label, command)
    return out

def hide_cat(index, params):
    get = params.get
    catid = get("catid")
    re_cat = '(\d)000'
    hide_cat = __settings__.getSetting("newznab_hide_cat_%s" % index)
    if re.search(re_cat, catid, re.IGNORECASE):
        regex = re.compile(re_cat,re.IGNORECASE)
        new_cat = regex.findall(catid)[0] + "\d\d\d"
        if hide_cat:
            new_cat = new_cat + "|" +  hide_cat
    else:
        new_cat = catid
        if hide_cat:
            new_cat = new_cat + "|" +  hide_cat
    __settings__.setSetting("newznab_hide_cat_%s" % index, new_cat)
    xbmc.executebuiltin("Container.Refresh")
    return

def cart_del(index, params):
    get = params.get
    nzb = get("nzb")
    re_id = 'nzb%2F(d*b*.*)\.nzb'
    regex = re.compile(re_id,re.IGNORECASE)
    id = regex.findall(nzb)[0]
    url = get_http_string(index) + __settings__.getSetting("newznab_siteapi_%s" % index) +\
          "/api?t=cartdel&apikey=" + __settings__.getSetting("newznab_key_%s" % index) +\
          "&id=" + id
    xbmc.executebuiltin('Notification("Newznab","Removing from cart")')
    load_xml(url)
    xbmc.executebuiltin("Container.Refresh")
    return

def cart_add(index, params):
    get = params.get
    nzb = get("nzb")
    re_id = 'nzb%2F(d*b*.*)\.nzb'
    regex = re.compile(re_id,re.IGNORECASE)
    id = regex.findall(nzb)[0]
    url = get_http_string(index) + __settings__.getSetting("newznab_siteapi_%s" % index) +\
          "/api?t=cartadd&apikey=" + __settings__.getSetting("newznab_key_%s" % index) +\
          "&id=" + id
    xbmc.executebuiltin('Notification("Newznab","Adding to cart")')
    load_xml(url)
    return

# FROM plugin.video.youtube.beta  -- converts the request url passed on by xbmc to our plugin into a dict
def get_parameters(parameterString):
    commands = {}
    splitCommands = parameterString[parameterString.find('?')+1:].split('&')
    for command in splitCommands:
        if (len(command) > 0):
            splitCommand = command.split('=')
            name = splitCommand[0]
            value = splitCommand[1]
            commands[name] = value
    return commands

def get_node_value(parent, name, ns=""):
    if ns:
        return parent.getElementsByTagNameNS(ns, name)[0].childNodes[0].data.encode('utf-8')
    else:
        return parent.getElementsByTagName(name)[0].childNodes[0].data.encode('utf-8')

def load_xml(url):
    #TODO add logging
    return CACHE.fetch(url)

def search(dialog_name, index):
    searchString = unikeyboard(__settings__.getSetting( "latestSearch" ), ('Search ' +\
                   __settings__.getSetting("newznab_name_%s" % index)) )
    if searchString == "":
        xbmcgui.Dialog().ok('Newznab','Missing text')
    elif searchString:
        latestSearch = __settings__.setSetting( "latestSearch", searchString )
        #The XBMC onscreen keyboard outputs utf-8 and this need to be encoded to unicode
    encodedSearchString = urllib.quote_plus(searchString.decode("utf_8").encode("raw_unicode_escape"))
    return encodedSearchString

#From old undertexter.se plugin
def unikeyboard(default, message):
    keyboard = xbmc.Keyboard(default, message)
    keyboard.doModal()
    if (keyboard.isConfirmed()):
        return keyboard.getText()
    else:
        return ""

def favorites(index):
    # http://wiki.python.org/moin/UsingPickle
    favorite_filename = "favorite_" + index + ".p"
    favorite = os.path.join(USERDATA_PATH, favorite_filename)
    try:
        favorite_dict = pickle.load( open( favorite, "rb" ) )
    except:
        return
    for key, value in favorite_dict.iteritems():
        info_labels = dict()
        info_labels['title'] = key
        url = "&url=" + value
        add_posts(info_labels, index, url=url, mode=MODE_FAVORITES)
    the_end()


def favorite_add(index, params):
    get = params.get
    search_term = get('search_term')
    search_url = get('search_url')
    nzbname = get('nzbname')
    if search_term is None and nzbname is not None:
        search_term = nzbname
    else:
        search_term = ''
    key = ''
    while len(key) < 1:
        key = unikeyboard(search_term, 'Favorite name')
    favorite_filename = "favorite_" + index + ".p"
    favorite = os.path.join(USERDATA_PATH, favorite_filename)
    try:
        favorite_dict = pickle.load( open( favorite, "rb" ) )
    except:
        favorite_dict = dict()
    favorite_dict[key] = search_url
    pickle.dump( favorite_dict, open( favorite, "wb" ) )
    return

def favorite_del(index):
    key = xbmc.getInfoLabel( "ListItem.Title" )
    favorite_filename = "favorite_" + index + ".p"
    favorite = os.path.join(USERDATA_PATH, favorite_filename)
    favorite_dict = pickle.load( open( favorite, "rb" ) )
    del favorite_dict[key]
    pickle.dump( favorite_dict, open( favorite, "wb" ) )
    xbmc.executebuiltin("Container.Refresh")
    return

def get_index_list():
    index_list = []
    for i in range(1, 6):
        if __settings__.getSetting("newznab_id_%s" % i):
            index_list.append(i)
    return index_list

def show_site_list(index_list):
    for index in index_list:
        add_posts({'title': __settings__.getSetting("newznab_name_%s" % index)}, index, mode=MODE_INDEX)
    add_posts({'title' : 'Browse local NZB\'s'}, 0, mode=MODE_PNEUMATIC_LOCAL)
    add_posts({'title' : 'Incomplete',}, 0, mode=MODE_PNEUMATIC_INCOMPLETE)
    the_end()
    return

def play_trailer(**kwargs):
    url = "plugin://plugin.video.youtube/?path=/root/search&feed=search&search=%s" % kwargs['trailer']
    try:
        xbmc.executebuiltin("XBMC.Container.Update(%s)" % url)
    except:
        pass

def the_end(catid = "1000"):
    # cat_id 5000 => episodes
    # cat_id 2000 => movies
    # cat_id 6000 => movies (xxx)
    # cat_id 3000 => albums
    # cat_id x => files
    # content: files, songs, artists, albums, movies, tvshows, episodes, musicvideos
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_UNSORTED)
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_FILE)
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_DATE)
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_SIZE)
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_TITLE)
    if catid is not None:
        if catid.startswith("2"):
            xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        if catid.startswith("3"):
            xbmcplugin.setContent(int(sys.argv[1]), 'albums')
        if catid.startswith("5"):
            xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
            xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_EPISODE)
    else:
        xbmcplugin.setContent(int(sys.argv[1]), 'files')
    xbmcplugin.endOfDirectory(int(sys.argv[1]), succeeded=True, cacheToDisc=True)

if (__name__ == "__main__" ):
    if not (__settings__.getSetting("firstrun") and __settings__.getSetting("newznab_id_1")
        and __settings__.getSetting("newznab_key_1")):
        __settings__.openSettings()
        __settings__.setSetting("firstrun", '1')
    if (not sys.argv[2]):
        index_list = get_index_list()
        if len(index_list) == 1:
            newznab('1')
        elif len(index_list) >= 1:
            show_site_list(index_list)
        else:
            __settings__.openSettings()
    else:
        params = get_parameters(sys.argv[2])
        get = params.get
        if get("mode")== MODE_INDEX:
            newznab(get("index"))
        if get("mode")== MODE_NEWZNAB:
            newznab(get("index"), params)
        if get("mode")== MODE_HIDE:
            hide_cat(get("index"), params)
        if get("mode")== MODE_CART_DEL:
            cart_del(get("index"), params)
        if get("mode")== MODE_CART_ADD:
            cart_add(get("index"), params)
        if get("mode")== MODE_FAVORITES_TOP:
            favorites(get("index"))
        if get("mode")== MODE_FAVORITE_ADD:
            favorite_add(get("index"), params)
        if get("mode")== MODE_FAVORITE_DEL:
            favorite_del(get("index"))
        if get("mode")== "trailer":
            play_trailer(**params)
