# -*- coding: utf-8 -*-

'''
    NBA On-demand Addon
    Copyright (C) 2014 lambda

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import urllib,urllib2,re,os,threading,datetime,time,base64,xbmc,xbmcplugin,xbmcgui,xbmcaddon,xbmcvfs,HTMLParser,array
from operator import itemgetter
from urlresolver.hmf import HostedMediaFile
try:
    from sqlite3 import dbapi2 as database
except:
    from pysqlite2 import dbapi2 as database
try:
    import CommonFunctions as common
except:
    import commonfunctionsdummy as common
try:
    import json
except:
    import simplejson as json


action              = None
language            = xbmcaddon.Addon().getLocalizedString
setSetting          = xbmcaddon.Addon().setSetting
getSetting          = xbmcaddon.Addon().getSetting
addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")
addonDesc           = language(30450).encode("utf-8")
dataPath            = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo("profile")).decode("utf-8")
addonIcon           = os.path.join(addonPath,'icon.png')
addonArt            = os.path.join(addonPath,'resources/art')
addonFanart         = os.path.join(addonPath,'fanart.jpg')
addonNext           = os.path.join(addonPath,'resources/art/videos_next.png')
addonSettings       = os.path.join(dataPath,'settings.db')
addonCache          = os.path.join(dataPath,'cache.db')


class main:
    def __init__(self):
        global action
        index().container_data()
        params = {}
        splitparams = sys.argv[2][sys.argv[2].find('?') + 1:].split('&')
        for param in splitparams:
            if (len(param) > 0):
                splitparam = param.split('=')
                key = splitparam[0]
                try:    value = splitparam[1].encode("utf-8")
                except: value = splitparam[1]
                params[key] = value

        try:        action = urllib.unquote_plus(params["action"])
        except:     action = None
        try:        url = urllib.unquote_plus(params["url"])
        except:     url = None
        try:        meta = urllib.unquote_plus(params["meta"])
        except:     meta = None
        try:        query = urllib.unquote_plus(params["query"])
        except:     query = None


        if action == None:                          root().get()
        elif action == 'cache_clear_list':          index().cache_clear_list()
        elif action == 'item_play':                 contextMenu().item_play()
        elif action == 'item_random_play':          contextMenu().item_random_play()
        elif action == 'item_queue':                contextMenu().item_queue()
        elif action == 'playlist_open':             contextMenu().playlist_open()
        elif action == 'settings_open':             contextMenu().settings_open()
        elif action == 'view_videos':               contextMenu().view('videos')
        elif action == 'pages_games':               pages().games('livetv_nba')
        elif action == 'pages_highlights':          pages().highlights('livetv_nba')
        elif action == 'pages_teams':               pages().teams('livetv_nba_teams')
        elif action == 'videos':                    videos().get(url)
        elif action == 'videos_all':                videos().get2(url)
        elif action == 'videos_added':              videos().root('livetv_nba')
        elif action == 'videos_parts':              videoparts().get(url, meta)
        elif action == 'play':                      resolver().run(url)

class getUrl(object):
    def __init__(self, url, close=True, proxy=None, post=None, mobile=False, referer=None, cookie=None, output='', timeout='10'):
        if not proxy == None:
            proxy_handler = urllib2.ProxyHandler({'http':'%s' % (proxy)})
            opener = urllib2.build_opener(proxy_handler, urllib2.HTTPHandler)
            opener = urllib2.install_opener(opener)
        if output == 'cookie' or not close == True:
            import cookielib
            cookie_handler = urllib2.HTTPCookieProcessor(cookielib.LWPCookieJar())
            opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
            opener = urllib2.install_opener(opener)
        if not post == None:
            request = urllib2.Request(url, post)
        else:
            request = urllib2.Request(url,None)
        if mobile == True:
            request.add_header('User-Agent', 'Mozilla/5.0 (iPhone; CPU; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7')
        else:
            request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0')
        if not referer == None:
            request.add_header('Referer', referer)
        if not cookie == None:
            request.add_header('Cookie', cookie)
        response = urllib2.urlopen(request, timeout=int(timeout))
        if output == 'cookie':
            result = str(response.headers.get('Set-Cookie'))
        elif output == 'geturl':
            result = response.geturl()
        else:
            result = response.read()
        if close == True:
            response.close()
        self.result = result

class uniqueList(object):
    def __init__(self, list):
        uniqueSet = set()
        uniqueList = []
        for n in list:
            if n not in uniqueSet:
                uniqueSet.add(n)
                uniqueList.append(n)
        self.list = uniqueList

class Thread(threading.Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)
    def run(self):
        self._target(*self._args)

class player(xbmc.Player):
    def __init__ (self):
        xbmc.Player.__init__(self)

    def run(self, url):
        item = xbmcgui.ListItem(path=url)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)

    def onPlayBackStarted(self):
        return

    def onPlayBackEnded(self):
        return

    def onPlayBackStopped(self):
        return

class index:
    def infoDialog(self, str, header=addonName):
        try: xbmcgui.Dialog().notification(header, str, addonIcon, 3000, sound=False)
        except: xbmc.executebuiltin("Notification(%s,%s, 3000, %s)" % (header, str, addonIcon))

    def okDialog(self, str1, str2, header=addonName):
        xbmcgui.Dialog().ok(header, str1, str2)

    def selectDialog(self, list, header=addonName):
        select = xbmcgui.Dialog().select(header, list)
        return select

    def yesnoDialog(self, str1, str2, header=addonName, str3='', str4=''):
        answer = xbmcgui.Dialog().yesno(header, str1, str2, '', str4, str3)
        return answer

    def getProperty(self, str):
        property = xbmcgui.Window(10000).getProperty(str)
        return property

    def setProperty(self, str1, str2):
        xbmcgui.Window(10000).setProperty(str1, str2)

    def clearProperty(self, str):
        xbmcgui.Window(10000).clearProperty(str)

    def addon_status(self, id):
        check = xbmcaddon.Addon(id=id).getAddonInfo("name")
        if not check == addonName: return True

    def container_refresh(self):
        xbmc.executebuiltin('Container.Refresh')

    def container_data(self):
        if not xbmcvfs.exists(dataPath):
            xbmcvfs.mkdir(dataPath)

    def container_view(self, content, viewDict):
        try:
            skin = xbmc.getSkinDir()
            record = (skin, content)
            dbcon = database.connect(addonSettings)
            dbcur = dbcon.cursor()
            dbcur.execute("SELECT * FROM views WHERE skin = '%s' AND view_type = '%s'" % (record[0], record[1]))
            view = dbcur.fetchone()
            view = view[2]
            if view == None: raise Exception()
            xbmc.executebuiltin('Container.SetViewMode(%s)' % str(view))
        except:
            try:
                id = str(viewDict[skin])
                xbmc.executebuiltin('Container.SetViewMode(%s)' % id)
            except:
                pass

    def cache(self, function, timeout, *args):
        try:
            response = None

            f = repr(function)
            f = re.sub('.+\smethod\s|.+function\s|\sat\s.+|\sof\s.+', '', f)

            import hashlib
            a = hashlib.md5()
            for i in args: a.update(str(i))
            a = str(a.hexdigest())
        except:
            pass

        try:
            dbcon = database.connect(addonCache)
            dbcur = dbcon.cursor()
            dbcur.execute("SELECT * FROM rel_list WHERE func = '%s' AND args = '%s'" % (f, a))
            match = dbcur.fetchone()

            response = eval(match[2].encode('utf-8'))

            t1 = int(re.sub('[^0-9]', '', str(match[3])))
            t2 = int(datetime.datetime.now().strftime("%Y%m%d%H%M"))
            update = abs(t2 - t1) >= int(timeout*60)
            if update == False:
                return response
        except:
            pass

        try:
            r = function(*args)
            if (r == None or r == []) and not response == None:
                return response
            elif (r == None or r == []):
                return r
        except:
            return

        try:
            r = repr(r)
            t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            dbcur.execute("CREATE TABLE IF NOT EXISTS rel_list (""func TEXT, ""args TEXT, ""response TEXT, ""added TEXT, ""UNIQUE(func, args)"");")
            dbcur.execute("DELETE FROM rel_list WHERE func = '%s' AND args = '%s'" % (f, a))
            dbcur.execute("INSERT INTO rel_list Values (?, ?, ?, ?)", (f, a, r, t))
            dbcon.commit()
        except:
            pass

        try:
            return eval(r.encode('utf-8'))
        except:
            pass

    def cache_clear_list(self):
        try:
            dbcon = database.connect(addonCache)
            dbcur = dbcon.cursor()
            dbcur.execute("DROP TABLE IF EXISTS rel_list")
            dbcur.execute("VACUUM")
            dbcon.commit()

            index().infoDialog(language(30303).encode("utf-8"))
        except:
            pass

    def rootList(self, rootList):
        if rootList == None or len(rootList) == 0: return

        total = len(rootList)
        for i in rootList:
            try:
                try: name = language(i['name']).encode("utf-8")
                except: name = i['name']

                image = '%s/%s' % (addonArt, i['image'])

                root = i['action']
                u = '%s?action=%s' % (sys.argv[0], root)
                try: u += '&url=%s' % urllib.quote_plus(i['url'])
                except: pass
                if u == '': raise Exception()

                cm = []

                item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
                item.setInfo(type="Video", infoLabels={"title": name, "plot": addonDesc})
                item.setProperty("Fanart_Image", addonFanart)
                item.addContextMenuItems(cm, replaceItems=False)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

        xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)

    def videoList(self, videoList):
        if videoList == None or len(videoList) == 0: return

        total = len(videoList)
        for i in videoList:
            try:
                name, url, image, date, genre, plot, title, show = i['name'], i['url'], i['image'], i['date'], i['genre'], i['plot'], i['title'], i['show']

                try: fanart = i['fanart']
                except: fanart = '0'

                meta = {'name': name, 'title': title, 'studio': show, 'premiered': date, 'genre': genre, 'plot': plot, 'image': image, 'fanart': fanart}

                sysmeta = urllib.quote_plus(json.dumps(meta))
                sysurl = urllib.quote_plus(url)

                if fanart == '0': fanart = addonFanart
                if image == '0': image = addonFanart
                if show == '0': meta.update({'studio': addonName})
                if plot == '0': meta.update({'plot': addonDesc})
                meta = dict((k,v) for k, v in meta.iteritems() if not v == '0')

                u = '%s?action=videos_parts&url=%s&meta=%s' % (sys.argv[0], sysurl, sysmeta)

                cm = []
                cm.append((language(30401).encode("utf-8"), 'RunPlugin(%s?action=item_play)' % (sys.argv[0])))
                cm.append((language(30403).encode("utf-8"), 'RunPlugin(%s?action=item_queue)' % (sys.argv[0])))
                cm.append((language(30404).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                cm.append((language(30406).encode("utf-8"), 'RunPlugin(%s?action=view_videos)' % (sys.argv[0])))
                cm.append((language(30405).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))

                item = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=image)
                item.setProperty("Fanart_Image", fanart)
                item.setInfo(type="Video", infoLabels = meta)
                item.setProperty("Video", "true")
                item.setProperty("IsPlayable", "true")
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

        try:
            next = videoList[0]['next']
            if next == '': raise Exception()
            name, url, image = language(30361).encode("utf-8"), next, addonNext
            u = '%s?action=videos&url=%s' % (sys.argv[0], urllib.quote_plus(url))
            item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
            item.setInfo( type="Video", infoLabels={"title": name, "plot": addonDesc})
            item.setProperty("Fanart_Image", addonFanart)
            item.addContextMenuItems([], replaceItems=False)
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,isFolder=True)
        except:
            pass

        xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
        xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)
        for i in range(0, 200):
            if xbmc.getCondVisibility('Container.Content(episodes)'):
                return index().container_view('videos', {'skin.confluence' : 504})
            xbmc.sleep(100)

    def videopartList(self, videopartList):
        if videopartList == None or len(videopartList) == 0: return

        total = len(videopartList)
        for i in videopartList:
            try:
                name, url = i['name'], i['url']
                meta = json.loads(i['meta'])
                image, fanart, show, plot = meta['image'], meta['fanart'], meta['studio'], meta['plot']

                sysurl = urllib.quote_plus(url)

                if fanart == '0': fanart = addonFanart
                if image == '0': image = addonFanart
                if show == '0': meta.update({'studio': addonName})
                if plot == '0': meta.update({'plot': addonDesc})
                meta = dict((k,v) for k, v in meta.iteritems() if not v == '0')

                u = '%s?action=play&url=%s' % (sys.argv[0], sysurl)

                cm = []
                cm.append((language(30401).encode("utf-8"), 'RunPlugin(%s?action=item_play)' % (sys.argv[0])))
                cm.append((language(30403).encode("utf-8"), 'RunPlugin(%s?action=item_queue)' % (sys.argv[0])))
                cm.append((language(30404).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                cm.append((language(30406).encode("utf-8"), 'RunPlugin(%s?action=view_videos)' % (sys.argv[0])))
                cm.append((language(30405).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))

                item = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=image)
                item.setProperty("Fanart_Image", fanart)
                item.setInfo(type="Video", infoLabels = meta)
                item.setProperty("Video", "true")
                item.setProperty("IsPlayable", "true")
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=False)
            except:
                pass

        xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
        xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)
        for i in range(0, 200):
            if xbmc.getCondVisibility('Container.Content(episodes)'):
                return index().container_view('videos', {'skin.confluence' : 504})
            xbmc.sleep(100)

class contextMenu:
    def item_play(self):
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        xbmc.executebuiltin('Action(Queue)')
        playlist.unshuffle()
        xbmc.Player().play(playlist)

    def item_random_play(self):
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        xbmc.executebuiltin('Action(Queue)')
        playlist.shuffle()
        xbmc.Player().play(playlist)

    def item_queue(self):
        xbmc.executebuiltin('Action(Queue)')

    def playlist_open(self):
        xbmc.executebuiltin('ActivateWindow(VideoPlaylist)')

    def settings_open(self, id=addonId):
        xbmc.executebuiltin('Addon.OpenSettings(%s)' % id)

    def view(self, content):
        try:
            skin = xbmc.getSkinDir()
            skinPath = xbmc.translatePath('special://skin/')
            xml = os.path.join(skinPath,'addon.xml')
            file = xbmcvfs.File(xml)
            read = file.read().replace('\n','')
            file.close()
            try: src = re.compile('defaultresolution="(.+?)"').findall(read)[0]
            except: src = re.compile('<res.+?folder="(.+?)"').findall(read)[0]
            src = os.path.join(skinPath, src)
            src = os.path.join(src, 'MyVideoNav.xml')
            file = xbmcvfs.File(src)
            read = file.read().replace('\n','')
            file.close()
            views = re.compile('<views>(.+?)</views>').findall(read)[0]
            views = [int(x) for x in views.split(',')]
            for view in views:
                label = xbmc.getInfoLabel('Control.GetLabel(%s)' % (view))
                if not (label == '' or label == None): break
            record = (skin, content, str(view))
            dbcon = database.connect(addonSettings)
            dbcur = dbcon.cursor()
            dbcur.execute("CREATE TABLE IF NOT EXISTS views (""skin TEXT, ""view_type TEXT, ""view_id TEXT, ""UNIQUE(skin, view_type)"");")
            dbcur.execute("DELETE FROM views WHERE skin = '%s' AND view_type = '%s'" % (record[0], record[1]))
            dbcur.execute("INSERT INTO views Values (?, ?, ?)", record)
            dbcon.commit()
            viewName = xbmc.getInfoLabel('Container.Viewmode')
            index().infoDialog('%s%s%s' % (language(30301).encode("utf-8"), viewName, language(30302).encode("utf-8")))
        except:
            return

class root:
    def get(self):
        rootList = []
        rootList.append({'name': 30501, 'image': 'videos_latest.png', 'action': 'videos_added'})
        rootList.append({'name': 30502, 'image': 'videos_games.png', 'action': 'pages_games'})
        rootList.append({'name': 30503, 'image': 'videos_highlights.png', 'action': 'pages_highlights'})
        rootList.append({'name': 30504, 'image': 'videos_teams.png', 'action': 'pages_teams'})
        index().rootList(rootList)

class link:
    def __init__(self):
        self.livetv_base = 'http://livetv.sx'
        self.livetv_nba = 'http://livetv.sx/enx/videotourney/3'
        self.livetv_nhl = 'http://livetv.sx/enx/videotourney/2'
        self.livetv_nba_teams = 'http://livetv.sx/enx/leagueresults/3/'
        self.livetv_nhl_teams = 'http://livetv.sx/enx/leagueresults/2/'

class pages:
    def __init__(self):
        self.list = []

    def games(self, url):
        self.list = self.livetv_list(url)
        for i in range(0, len(self.list)): self.list[i].update({'image': 'videos_games.png', 'action': 'videos'})
        index().rootList(self.list)

    def highlights(self, url):
        self.list = self.livetv_list(url)
        for i in range(0, len(self.list)): self.list[i].update({'image': 'videos_highlights.png', 'action': 'videos_all'})
        index().rootList(self.list)

    def teams(self, url):
        self.list = index().cache(self.livetv_list2, 24, url)
        for i in range(0, len(self.list)): self.list[i].update({'image': 'videos_teams.png', 'action': 'videos_all'})
        index().rootList(self.list)

    def livetv_list(self, url):
        base = getattr(link(), url)

        for i in range(0, 12):
            year = (datetime.datetime.utcnow() - datetime.timedelta(days = i*30)).strftime("%Y")
            month = (datetime.datetime.utcnow() - datetime.timedelta(days = i*30)).strftime("%m")
            monthDict = {'01': 'January', '02': 'February', '03': 'March', '04': 'April', '05': 'May', '06': 'June', '07': 'July', '08': 'August', '09': 'September', '10': 'October', '11': 'November', '12' : 'December'}

            name = '%s %s' % (monthDict[month], year)
            if any(name == i['name'] for i in self.list): continue
            name = name.encode('utf-8')

            url = '%s/%s%s/' % (base, year, month)
            url = url.encode('utf-8')

            self.list.append({'name': name, 'url': url})

        return self.list

    def livetv_list2(self, url):
        try:
            url = getattr(link(), url)
            result = getUrl(url, timeout='30').result
            result = result.decode('iso-8859-1').encode('utf-8')
            result = result.replace('\n','')

            pages = re.compile('(<a href="/enx/team/.+?">.+?</a>)').findall(result)
        except:
            return

        for page in pages:
            try:
                name = common.parseDOM(page, "a")[0]
                name = re.sub('<.+?>|</.+?>', '', name)
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(page, "a", ret="href")[0]
                url = re.sub('/calendar/', '/video/', url)
                url = '%s%s' % (link().livetv_base, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                self.list.append({'name': name, 'url': url})
            except:
                pass

        try:
            self.list = [i for n,i in enumerate(self.list) if i not in self.list[:n]]
            self.list = sorted(self.list, key=itemgetter('name'))
        except:
            pass

        return self.list

class videos:
    def __init__(self):
        self.list = []

    def root(self, url):
        url = getattr(link(), url)
        self.list = index().cache(self.livetv_list, 1, url)
        index().videoList(self.list)

    def get(self, url):
        self.list = index().cache(self.livetv_list, 1, url)
        try: self.list = [i for i in self.list if i['type'] == 'games']
        except: return
        index().videoList(self.list)

    def get2(self, url):
        self.list = index().cache(self.livetv_list, 1, url)
        index().videoList(self.list)

    def livetv_list(self, url):
        try:
            result = getUrl(url, timeout='30').result
            result = result.decode('iso-8859-1').encode('utf-8')
            result = result.replace('\n','')

            videos = common.parseDOM(result, "table", attrs = { "height": "27" })
        except:
            return

        for video in videos:
            try:
                title = re.compile('<b>(.+?)</b>').findall(video)
                title = [i for i in title if '&ndash;' in i or '-' in i][-1]
                title = title.split('<b>')[-1]
                title = title.replace('&ndash;', '-')
                title = common.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                dateDict = {'January': '01', 'February': '02', 'March': '03', 'April': '04', 'May': '05', 'June': '06', 'July': '07', 'August': '08', 'September': '09', 'October': '10', 'November': '11', 'December' : '12'}

                try:
                    date = common.parseDOM(video, "span", attrs = { "class": "date" })[0]
                    date = re.findall('(\d+)[.](\d+)[.](\d+)', date, re.I)[0]
                    date = '%s-%s-%s' % ('20' + '%02d' % int(date[2]), '%02d' % int(date[1]), '%02d' % int(date[0]))
                except:
                    year = common.parseDOM(result, "a", attrs = { "class": "mwhite" })
                    year = [i for i in year if i.isdigit()][0]
                    date = result.split(video.encode('utf-8'))[0]
                    date = date.split('#2862a8')[-1]
                    date = re.compile('<b>(\d+?)\s(.+?),\s.+?</b>').findall(date)[0]
                    date = '%s-%s-%s' % (year, dateDict[date[1]], '%02d' % int(date[0]))

                name = '%s (%s)' % (title, date)
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = []
                u = [('Full match record', ''), ('First Half', ' (1)'), ('Second Half', ' (2)'), ('First Period', ' (1)'), ('Second Period', ' (2)'), ('Third Period', ' (3)'), ('Fourth Period', ' (4)'), ('First Part', ' (1)'), ('Second Part', ' (2)'), ('Third Part', ' (3)'), ('Fourth Part', ' (4)'), ('Highlights', ' (Highlights)'), ('Long Highlights', ' (Long Highlights)')]
                uDict, uList = dict(u), [i[0] for i in u]
                u = re.compile('href="(.+?)">(.+?)<').findall(video)
                u = [i for i in u if i[1] in uList]
                u.sort(key=lambda x: uList.index(x[1]))
                for i in u: url.append({'name': title + uDict[i[1]], 'url': link().livetv_base + i[0]})
                if len(url) == 0: raise Exception()
                if len(url) == 1 and uDict['Highlights'] in url[0]['name']: type = 'highlights'
                else: type = 'games'
                url = json.dumps(url)
                url = url.encode('utf-8')

                plot = '%s\n%s' % (title, date)
                try: plot += '\n%s' % re.compile('<b>(\d+?:\d+?)</b>').findall(video)[0]
                except: pass
                plot = common.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': '0', 'date': date, 'genre': 'Sports', 'plot': plot, 'title': title, 'show': '0', 'type': type})
            except:
                pass

        try:
            self.list = [i for n,i in enumerate(self.list) if i not in self.list[:n]]
            self.list = sorted(self.list, key=itemgetter('date'))
            self.list = self.list[::-1]
        except:
            pass

        return self.list

class videoparts:
    def __init__(self):
        self.list = []

    def get(self, url, meta=''):
        self.list = self.livetv_list(url, meta)
        index().videopartList(self.list)

    def livetv_list(self, url, meta):
        try:
            result = json.loads(url)
            for i in result: self.list.append({'name': i['name'], 'url': i['url'], 'meta': meta})
        except:
            pass

        return self.list

class resolver:
    def run(self, url):
        try:
            url = self.livetv(url)
            if url is None: raise Exception()

            player().run(url)
            return url
        except:
            index().infoDialog(language(30304).encode("utf-8"))
            return

    def livetv(self, url):
        try:
            result = getUrl(url, timeout='30').result
            result = result.replace('\n','')
            result = re.sub(r'<script.+?</script>', '', result, flags=re.DOTALL)
            
            try:
                url = re.search("data-config\s*=\s*(?:\'|\")(.+?)(?:\'|\")", result).groups()[0]
            except:    
                url = common.parseDOM(result, "iframe", ret="src")[0]
                
            if '=http' in url: url = re.search("=(https?://.+)", url).groups()[0]
            elif url.startswith("//"): url = 'http:%s' % url
            
            if 'video.nhl.com' in url: url = self.nhl(url)
            else: url = HostedMediaFile(url=url).resolve()
            return url
        except:
            return
            
    def nhl(self, url):
        try:
            url = url.split("playlist=")[-1]
            url = 'http://video.nhl.com/videocenter/servlets/playlist?ids=%s&format=json' % url
            result = getUrl(url).result
            url = re.compile('"publishPoint":"(.+?)"').findall(result)[0]
            return url
        except:
            return
            

main()