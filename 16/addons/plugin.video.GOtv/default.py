# -*- coding: utf-8 -*-

'''
    GOtv XBMC Addon
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

import urllib,urllib2,re,os,threading,datetime,time,base64,xbmc,xbmcplugin,xbmcgui,xbmcaddon,xbmcvfs
from operator import itemgetter
try:    import json
except: import simplejson as json
try:    import CommonFunctions
except: import commonfunctionsdummy as CommonFunctions
try:    import StorageServer
except: import storageserverdummy as StorageServer
from metahandler import metahandlers
from metahandler import metacontainers


action              = None
common              = CommonFunctions
metaget             = metahandlers.MetaData(preparezip=False)
language            = xbmcaddon.Addon().getLocalizedString
setSetting          = xbmcaddon.Addon().setSetting
getSetting          = xbmcaddon.Addon().getSetting
addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")
addonFullId         = addonName + addonVersion
addonDesc           = language(30450).encode("utf-8")
cache               = StorageServer.StorageServer(addonFullId,1).cacheFunction
cache2              = StorageServer.StorageServer(addonFullId,24).cacheFunction
cache3              = StorageServer.StorageServer(addonFullId,720).cacheFunction
addonIcon           = os.path.join(addonPath,'icon.png')
addonFanart         = os.path.join(addonPath,'fanart.jpg')
addonArt            = os.path.join(addonPath,'resources/art')
addonPoster         = os.path.join(addonPath,'resources/art/Poster.png')
addonDownloads      = os.path.join(addonPath,'resources/art/Downloads.png')
addonGenres         = os.path.join(addonPath,'resources/art/Genres.png')
addonCalendar       = os.path.join(addonPath,'resources/art/Calendar.png')
addonLists          = os.path.join(addonPath,'resources/art/Lists.png')
addonNext           = os.path.join(addonPath,'resources/art/Next.png')
dataPath            = xbmc.translatePath('special://profile/addon_data/%s' % (addonId))
viewData            = os.path.join(dataPath,'views.cfg')
offData             = os.path.join(dataPath,'offset.cfg')
favData             = os.path.join(dataPath,'favourites.cfg')
subData             = os.path.join(dataPath,'subscriptions.cfg')


class main:
    def __init__(self):
        global action
        cacheToDisc = True
        index().container_data()
        index().settings_reset()
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
        try:        name = urllib.unquote_plus(params["name"])
        except:     name = None
        try:        url = urllib.unquote_plus(params["url"])
        except:     url = None
        try:        image = urllib.unquote_plus(params["image"])
        except:     image = None
        try:        query = urllib.unquote_plus(params["query"])
        except:     query = None
        try:        source = urllib.unquote_plus(params["source"])
        except:     source = None
        try:        provider = urllib.unquote_plus(params["provider"])
        except:     provider = None
        try:        title = urllib.unquote_plus(params["title"])
        except:     title = None
        try:        year = urllib.unquote_plus(params["year"])
        except:     year = None
        try:        date = urllib.unquote_plus(params["date"])
        except:     date = None
        try:        imdb = urllib.unquote_plus(params["imdb"])
        except:     imdb = None
        try:        tvdb = urllib.unquote_plus(params["tvdb"])
        except:     tvdb = None
        try:        genre = urllib.unquote_plus(params["genre"])
        except:     genre = None
        try:        plot = urllib.unquote_plus(params["plot"])
        except:     plot = None
        try:        show = urllib.unquote_plus(params["show"])
        except:     show = None
        try:        show_alt = urllib.unquote_plus(params["show_alt"])
        except:     show_alt = None
        try:        season = urllib.unquote_plus(params["season"])
        except:     season = None
        try:        episode = urllib.unquote_plus(params["episode"])
        except:     episode = None

        if action == None:                          root().get()
        elif action == 'root_search':               root().search()
        elif action == 'item_play':                 contextMenu().item_play()
        elif action == 'item_random_play':          contextMenu().item_random_play()
        elif action == 'item_queue':                contextMenu().item_queue()
        elif action == 'favourite_add':             contextMenu().favourite_add(favData, name, url, image, imdb, year)
        elif action == 'favourite_from_search':     contextMenu().favourite_from_search(favData, name, url, image, imdb, year)
        elif action == 'favourite_delete':          contextMenu().favourite_delete(favData, name, url)
        elif action == 'favourite_moveUp':          contextMenu().favourite_moveUp(favData, name, url)
        elif action == 'favourite_moveDown':        contextMenu().favourite_moveDown(favData, name, url)
        elif action == 'playlist_open':             contextMenu().playlist_open()
        elif action == 'settings_open':             contextMenu().settings_open()
        elif action == 'addon_home':                contextMenu().addon_home()
        elif action == 'view_tvshows':              contextMenu().view('tvshows')
        elif action == 'view_seasons':              contextMenu().view('seasons')
        elif action == 'view_episodes':             contextMenu().view('episodes')
        elif action == 'metadata_tvshows':          contextMenu().metadata('tvshow', imdb, '', '')
        elif action == 'metadata_tvshows2':         contextMenu().metadata('tvshow', imdb, '', '')
        elif action == 'metadata_seasons':          contextMenu().metadata('season', imdb, season, '')
        elif action == 'metadata_episodes':         contextMenu().metadata('episode', imdb, season, episode)
        elif action == 'playcount_tvshows':         contextMenu().playcount('tvshow', imdb, '', '')
        elif action == 'playcount_seasons':         contextMenu().playcount('season', imdb, season, '')
        elif action == 'playcount_episodes':        contextMenu().playcount('episode', imdb, season, episode)
        elif action == 'library_add':               contextMenu().library_add(name, url, image, imdb, year)
        elif action == 'library_from_search':       contextMenu().library_from_search(name, url, image, imdb, year)
        elif action == 'library_batch':             contextMenu().library_batch(url)
        elif action == 'library_delete':            contextMenu().library_delete(name, url)
        elif action == 'library_update':            contextMenu().library_update()
        elif action == 'library_service':           contextMenu().library_update(silent=True)
        elif action == 'download':                  contextMenu().download(name, url, provider)
        elif action == 'autoplay':                  contextMenu().autoplay(name, title, imdb, tvdb, year, season, episode, show, show_alt)
        elif action == 'shows_favourites':          favourites().shows()
        elif action == 'shows_subscriptions':       subscriptions().shows()
        elif action == 'episodes_subscriptions':    subscriptions().episodes()
        elif action == 'shows':                     shows().get(url)
        elif action == 'shows_userlists':           shows().get(url)
        elif action == 'shows_popular':             shows().popular()
        elif action == 'shows_rating':              shows().rating()
        elif action == 'shows_views':               shows().views()
        elif action == 'shows_active':              shows().active()
        elif action == 'shows_trending':            shows().trending()
        elif action == 'shows_search':              shows().search(query)
        elif action == 'actors_search':             actors().search(query)
        elif action == 'genres_shows':              genres().get()
        elif action == 'calendar_episodes':         calendar().get()
        elif action == 'userlists_trakt':           userlists().trakt()
        elif action == 'userlists_imdb':            userlists().imdb()
        elif action == 'seasons':                   seasons().get(url, image, year, imdb, genre, plot, show)
        elif action == 'episodes':                  episodes().get(name, url, image, year, imdb, tvdb, genre, plot, show, show_alt)
        elif action == 'episodes_calendar':         episodes().calendar(url)
        elif action == 'get_host':                  resolver().get_host(name, url, image, date, year, imdb, tvdb, genre, plot, title, show, show_alt, season, episode)
        elif action == 'play_host':                 resolver().play_host(name, url, imdb, source, provider)
        elif action == 'play':                      resolver().run(name, title, imdb, tvdb, year, season, episode, show, show_alt, url)

        if action is None:
            pass
        elif action.startswith('shows'):
            xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
            index().container_view('tvshows', {'skin.confluence' : 500})
        elif action.startswith('seasons'):
            xbmcplugin.setContent(int(sys.argv[1]), 'seasons')
            index().container_view('seasons', {'skin.confluence' : 500})
        elif action.startswith('episodes'):
            xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
            index().container_view('episodes', {'skin.confluence' : 504})
            cacheToDisc = False
        xbmcplugin.setPluginFanart(int(sys.argv[1]), addonFanart)
        xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=cacheToDisc)
        return

class getUrl(object):
    def __init__(self, url, close=True, proxy=None, post=None, mobile=False, referer=None, cookie=None, output='', timeout='10'):
        if not proxy is None:
            proxy_handler = urllib2.ProxyHandler({'http':'%s' % (proxy)})
            opener = urllib2.build_opener(proxy_handler, urllib2.HTTPHandler)
            opener = urllib2.install_opener(opener)
        if output == 'cookie' or not close == True:
            import cookielib
            cookie_handler = urllib2.HTTPCookieProcessor(cookielib.LWPCookieJar())
            opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
            opener = urllib2.install_opener(opener)
        if not post is None:
            request = urllib2.Request(url, post)
        else:
            request = urllib2.Request(url,None)
        if mobile == True:
            request.add_header('User-Agent', 'Mozilla/5.0 (iPhone; CPU; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7')
        else:
            request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36')
        if not referer is None:
            request.add_header('Referer', referer)
        if not cookie is None:
            request.add_header('cookie', cookie)
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
        self.folderPath = xbmc.getInfoLabel('Container.FolderPath')
        self.PseudoTVRunning = index().getProperty('PseudoTVRunning')
        self.loadingStarting = time.time()
        xbmc.Player.__init__(self)

    def run(self, name, url, imdb='0'):
        self.video_info(name, imdb)

        if self.folderPath.startswith(sys.argv[0]) or self.PseudoTVRunning == 'True':
            item = xbmcgui.ListItem(path=url)
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
        else:
            try:
                file = self.name + '.strm'
                file = file.translate(None, '\/:*?"<>|')

                meta = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodes", "params": {"filter":{"and": [{"field": "season", "operator": "is", "value": "%s"}, {"field": "episode", "operator": "is", "value": "%s"}]}, "properties": ["title", "plot", "votes", "rating", "writer", "firstaired", "playcount", "runtime", "director", "productioncode", "season", "episode", "originaltitle", "showtitle", "lastplayed", "fanart", "thumbnail", "file", "resume", "tvshowid", "dateadded", "uniqueid"]}, "id": 1}' % (self.season, self.episode))
                meta = unicode(meta, 'utf-8', errors='ignore')
                meta = json.loads(meta)
                meta = meta['result']['episodes']
                self.meta = [i for i in meta if i['file'].endswith(file)][0]
                meta = {'title': self.meta['title'], 'tvshowtitle': self.meta['showtitle'], 'season': self.meta['season'], 'episode': self.meta['episode'], 'writer': str(self.meta['writer']).replace("[u'", '').replace("']", '').replace("', u'", ' / '), 'director': str(self.meta['director']).replace("[u'", '').replace("']", '').replace("', u'", ' / '), 'rating': self.meta['rating'], 'duration': self.meta['runtime'], 'premiered': self.meta['firstaired'], 'plot': self.meta['plot']}
                poster = self.meta['thumbnail']
            except:
                meta = {'label': self.name, 'title': self.name}
                poster = ''
            item = xbmcgui.ListItem(path=url, iconImage="DefaultVideo.png", thumbnailImage=poster)
            item.setInfo( type="Video", infoLabels= meta )
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)

        for i in range(0, 250):
            try: self.totalTime = self.getTotalTime()
            except: self.totalTime = 0
            if not self.totalTime == 0: continue
            xbmc.sleep(1000)
        if self.totalTime == 0: return

        while True:
            try: self.currentTime = self.getTime()
            except: break
            xbmc.sleep(1000)

    def video_info(self, name, imdb):
        self.name = name
        self.content = 'episode'
        self.show = self.name.rsplit(' ', 1)[0]
        if imdb == '0': imdb = metaget.get_meta('tvshow', self.show)['imdb_id']
        self.imdb = re.sub('[^0-9]', '', imdb)
        self.season = '%01d' % int(name.rsplit(' ', 1)[-1].split('S')[-1].split('E')[0])
        self.episode = '%01d' % int(name.rsplit(' ', 1)[-1].split('E')[-1])
        self.subtitle = subtitles().get(self.name, self.imdb, self.season, self.episode)

    def offset_add(self):
        try:
            file = xbmcvfs.File(offData)
            read = file.read()
            file.close()
            write = [i.strip('\n').strip('\r') for i in read.splitlines(True) if i.strip('\r\n')]
            write.append('"%s"|"%s"|"%s"' % (self.name, self.imdb, self.currentTime))
            write = '\r\n'.join(write)
            file = xbmcvfs.File(offData, 'w')
            file.write(str(write))
            file.close()
        except:
            return

    def offset_delete(self):
        try:
            file = xbmcvfs.File(offData)
            read = file.read()
            file.close()
            write = [i.strip('\n').strip('\r') for i in read.splitlines(True) if i.strip('\r\n')]
            write = [i for i in write if not '"%s"|"%s"|"' % (self.name, self.imdb) in i]
            write = '\r\n'.join(write)
            file = xbmcvfs.File(offData, 'w')
            file.write(str(write))
            file.close()
        except:
            return

    def offset_read(self):
        try:
            self.offset = '0'
            file = xbmcvfs.File(offData)
            read = file.read()
            file.close()
            read = [i for i in read.splitlines(True) if '"%s"|"%s"|"' % (self.name, self.imdb) in i][0]
            self.offset = re.compile('".+?"[|]".+?"[|]"(.+?)"').findall(read)[0]
        except:
            return

    def change_watched(self):
        try:
            xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.SetEpisodeDetails", "params": {"episodeid" : %s, "playcount" : 1 }, "id": 1 }' % str(self.meta['episodeid']))
        except:
            metaget.change_watched(self.content, '', self.imdb, season=self.season, episode=self.episode, year='', watched=7)

    def resume_playback(self):
        offset = float(self.offset)
        if not offset > 0: return
        minutes, seconds = divmod(offset, 60)
        hours, minutes = divmod(minutes, 60)
        offset_time = '%02d:%02d:%02d' % (hours, minutes, seconds)
        yes = index().yesnoDialog('%s %s' % (language(30350).encode("utf-8"), offset_time), '', self.name, language(30351).encode("utf-8"), language(30352).encode("utf-8"))
        if yes: self.seekTime(offset)

    def onPlayBackStarted(self):
        try: self.setSubtitles(self.subtitle)
        except: pass

        if self.PseudoTVRunning == 'True': return

        if getSetting("playback_info") == 'true':
            elapsedTime = '%s %.2f seconds' % (language(30319).encode("utf-8"), (time.time() - self.loadingStarting))     
            index().infoDialog(elapsedTime, header=self.name)

        if getSetting("resume_playback") == 'true':
            self.offset_read()
            self.resume_playback()

    def onPlayBackEnded(self):
        if self.PseudoTVRunning == 'True': return
        self.change_watched()
        self.offset_delete()

    def onPlayBackStopped(self):
        if self.PseudoTVRunning == 'True': return
        if self.currentTime / self.totalTime >= .9:
            self.change_watched()
        self.offset_delete()
        self.offset_add()

class subtitles:
    def get(self, name, imdb, season, episode):
        if not getSetting("subtitles") == 'true': return
        quality = ['bluray', 'hdrip', 'brrip', 'bdrip', 'dvdrip', 'webrip', 'hdtv']
        langDict = {'Afrikaans': 'afr', 'Albanian': 'alb', 'Arabic': 'ara', 'Armenian': 'arm', 'Basque': 'baq', 'Bengali': 'ben', 'Bosnian': 'bos', 'Breton': 'bre', 'Bulgarian': 'bul', 'Burmese': 'bur', 'Catalan': 'cat', 'Chinese': 'chi', 'Croatian': 'hrv', 'Czech': 'cze', 'Danish': 'dan', 'Dutch': 'dut', 'English': 'eng', 'Esperanto': 'epo', 'Estonian': 'est', 'Finnish': 'fin', 'French': 'fre', 'Galician': 'glg', 'Georgian': 'geo', 'German': 'ger', 'Greek': 'ell', 'Hebrew': 'heb', 'Hindi': 'hin', 'Hungarian': 'hun', 'Icelandic': 'ice', 'Indonesian': 'ind', 'Italian': 'ita', 'Japanese': 'jpn', 'Kazakh': 'kaz', 'Khmer': 'khm', 'Korean': 'kor', 'Latvian': 'lav', 'Lithuanian': 'lit', 'Luxembourgish': 'ltz', 'Macedonian': 'mac', 'Malay': 'may', 'Malayalam': 'mal', 'Manipuri': 'mni', 'Mongolian': 'mon', 'Montenegrin': 'mne', 'Norwegian': 'nor', 'Occitan': 'oci', 'Persian': 'per', 'Polish': 'pol', 'Portuguese': 'por,pob', 'Portuguese(Brazil)': 'pob,por', 'Romanian': 'rum', 'Russian': 'rus', 'Serbian': 'scc', 'Sinhalese': 'sin', 'Slovak': 'slo', 'Slovenian': 'slv', 'Spanish': 'spa', 'Swahili': 'swa', 'Swedish': 'swe', 'Syriac': 'syr', 'Tagalog': 'tgl', 'Tamil': 'tam', 'Telugu': 'tel', 'Thai': 'tha', 'Turkish': 'tur', 'Ukrainian': 'ukr', 'Urdu': 'urd'}

        langs = []
        try: langs.append(langDict[getSetting("sublang1")])
        except: pass
        try: langs.append(langDict[getSetting("sublang2")])
        except: pass
        langs = ','.join(langs)

        try:
            import xmlrpclib
            server = xmlrpclib.Server('http://api.opensubtitles.org/xml-rpc', verbose=0)
            token = server.LogIn('', '', 'en', 'XBMC_Subtitles_v1')['token']
            result = server.SearchSubtitles(token, [{'sublanguageid': langs, 'imdbid': imdb, 'season': season, 'episode': episode}])['data']
            result = [i for i in result if i['SubSumCD'] == '1']
        except:
            return

        subtitles = []
        for lang in langs.split(','):
            filter = [i for i in result if lang == i['SubLanguageID']]
            if filter == []: continue
            for q in quality: subtitles += [i for i in filter if q in i['MovieReleaseName'].lower()]
            subtitles += [i for i in filter if not any(x in i['MovieReleaseName'].lower() for x in quality)]
            try: lang = xbmc.convertLanguage(lang, xbmc.ISO_639_1)
            except: pass
            break

        try:
            import zlib, base64
            content = [subtitles[0]["IDSubtitleFile"],]
            content = server.DownloadSubtitles(token, content)
            content = base64.b64decode(content['data'][0]['data'])
            content = zlib.decompressobj(16+zlib.MAX_WBITS).decompress(content)

            subtitle = xbmc.translatePath('special://temp/')
            subtitle = os.path.join(subtitle, 'TemporarySubs.%s.srt' % lang)
            file = open(subtitle, 'wb')
            file.write(content)
            file.close()

            return subtitle
        except:
            index().infoDialog(language(30317).encode("utf-8"), name)
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
        xbmc.executebuiltin("Container.Refresh")

    def container_data(self):
        if not xbmcvfs.exists(dataPath):
            xbmcvfs.mkdir(dataPath)
        if not xbmcvfs.exists(favData):
            file = xbmcvfs.File(favData, 'w')
            file.write('')
            file.close()
        if not xbmcvfs.exists(subData):
            file = xbmcvfs.File(subData, 'w')
            file.write('')
            file.close()
        if not xbmcvfs.exists(viewData):
            file = xbmcvfs.File(viewData, 'w')
            file.write('')
            file.close()
        if not xbmcvfs.exists(offData):
            file = xbmcvfs.File(offData, 'w')
            file.write('')
            file.close()

    def settings_reset(self):
        try:
            if getSetting("settings_version") == '2.6.0': return
            settings = os.path.join(addonPath,'resources/settings.xml')
            file = xbmcvfs.File(settings)
            read = file.read()
            file.close()
            for i in range (1,8): setSetting('hosthd' + str(i), common.parseDOM(read, "setting", ret="default", attrs = {"id": 'hosthd' + str(i)})[0])
            for i in range (1,16): setSetting('host' + str(i), common.parseDOM(read, "setting", ret="default", attrs = {"id": 'host' + str(i)})[0])
            setSetting('settings_version', '2.6.0')
        except:
            return

    def container_view(self, content, viewDict):
        try:
            skin = xbmc.getSkinDir()
            file = xbmcvfs.File(viewData)
            read = file.read().replace('\n','')
            file.close()
            view = re.compile('"%s"[|]"%s"[|]"(.+?)"' % (skin, content)).findall(read)[0]
            xbmc.executebuiltin('Container.SetViewMode(%s)' % str(view))
        except:
            try:
                id = str(viewDict[skin])
                xbmc.executebuiltin('Container.SetViewMode(%s)' % id)
            except:
                pass

    def rootList(self, rootList):
        total = len(rootList)
        for i in rootList:
            try:
                name = language(i['name']).encode("utf-8")
                image = '%s/%s' % (addonArt, i['image'])
                action = i['action']
                u = '%s?action=%s' % (sys.argv[0], action)

                cm = []
                if action == 'shows_trending':
                    cm.append((language(30423).encode("utf-8"), 'RunPlugin(%s?action=library_batch&url=%s)' % (sys.argv[0], action)))
                cm.append((language(30425).encode("utf-8"), 'RunPlugin(%s?action=library_update)' % (sys.argv[0])))

                item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
                item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "Plot": addonDesc } )
                item.setProperty("Fanart_Image", addonFanart)
                item.addContextMenuItems(cm, replaceItems=False)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

    def pageList(self, pageList):
        if pageList == None: return

        total = len(pageList)
        for i in pageList:
            try:
                name, url, image = i['name'], i['url'], i['image']
                sysname, sysurl, sysimage = urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(image)

                u = '%s?action=shows&url=%s' % (sys.argv[0], sysurl)

                item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
                item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "Plot": addonDesc } )
                item.setProperty("Fanart_Image", addonFanart)
                item.addContextMenuItems([], replaceItems=False)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

    def pageList2(self, pageList):
        if pageList == None: return

        total = len(pageList)
        for i in pageList:
            try:
                name, url, image = i['name'], i['url'], i['image']
                sysname, sysurl, sysimage = urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(image)

                u = '%s?action=episodes_calendar&url=%s' % (sys.argv[0], sysurl)

                cm = []
                cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))
                cm.append((language(30410).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))

                item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
                item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "Plot": addonDesc } )
                item.setProperty("Fanart_Image", addonFanart)
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

    def userList(self, userList):
        if userList == None: return

        total = len(userList)
        for i in userList:
            try:
                name, url, image = i['name'], i['url'], i['image']
                sysname, sysurl, sysimage = urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(image)

                u = '%s?action=shows_userlists&url=%s' % (sys.argv[0], sysurl)

                cm = []
                cm.append((language(30423).encode("utf-8"), 'RunPlugin(%s?action=library_batch&url=%s)' % (sys.argv[0], sysurl)))

                item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
                item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "Plot": addonDesc } )
                item.setProperty("Fanart_Image", addonFanart)
                item.addContextMenuItems(cm, replaceItems=False)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

    def nextList(self, nextList):
        try: next = nextList[0]['next']
        except: return
        if next == '': return
        name, url, image = language(30361).encode("utf-8"), next, addonNext
        sysurl = urllib.quote_plus(url)

        u = '%s?action=shows&url=%s' % (sys.argv[0], sysurl)

        item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
        item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "Plot": addonDesc } )
        item.setProperty("Fanart_Image", addonFanart)
        item.addContextMenuItems([], replaceItems=False)
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,isFolder=True)

    def downloadList(self):
        u = getSetting("downloads")
        if u == '': return
        name, image = language(30363).encode("utf-8"), addonDownloads

        item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
        item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "Plot": addonDesc } )
        item.setProperty("Fanart_Image", addonFanart)
        item.addContextMenuItems([], replaceItems=False)
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,isFolder=True)

    def showList(self, showList):
        if showList == None: return

        getmeta = getSetting("meta")
        if action == 'shows_search': getmeta = ''

        file = xbmcvfs.File(favData)
        favRead = file.read()
        file.close()
        file = xbmcvfs.File(subData)
        subRead = file.read()
        file.close()

        total = len(showList)
        for i in showList:
            try:
                name, url, image, year, imdb, genre, plot = i['name'], i['url'], i['image'], i['year'], i['imdb'], i['genre'], i['plot']
                if plot == '': plot = addonDesc
                if genre == '': genre = ' '
                title = name

                sysname, sysurl, sysimage, sysyear, sysimdb, sysgenre, sysplot = urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(image), urllib.quote_plus(year), urllib.quote_plus(imdb), urllib.quote_plus(genre), urllib.quote_plus(plot)
                u = '%s?action=seasons&url=%s&image=%s&year=%s&imdb=%s&genre=%s&plot=%s&show=%s' % (sys.argv[0], sysurl, sysimage, sysyear, sysimdb, sysgenre, sysplot, sysname)

                if getmeta == 'true':
                    meta = metaget.get_meta('tvshow', title, imdb_id=imdb)
                    meta.update({'playcount': 0, 'overlay': 0})
                    playcountMenu = language(30407).encode("utf-8")
                    if meta['overlay'] == 6: playcountMenu = language(30408).encode("utf-8")
                    metaimdb = urllib.quote_plus(re.sub('[^0-9]', '', meta['imdb_id']))
                    poster, banner = meta['cover_url'], meta['banner_url']
                    if banner == '': banner = poster
                    if banner == '': banner = image
                    if poster == '': poster = image
                else:
                    meta = {'label': title, 'title': title, 'tvshowtitle': title, 'year' : year, 'imdb_id' : imdb, 'genre' : genre, 'plot': plot}
                    poster, banner = image, image
                if getmeta == 'true' and getSetting("fanart") == 'true':
                    fanart = meta['backdrop_url']
                    if fanart == '': fanart = addonFanart
                else:
                    fanart = addonFanart

                meta.update({'art(banner)': banner, 'art(poster)': poster})

                cm = []
                cm.append((language(30413).encode("utf-8"), 'Action(Info)'))

                if action == 'shows_favourites':
                    if not '"%s"' % url in subRead: cm.append((language(30423).encode("utf-8"), 'RunPlugin(%s?action=library_add&name=%s&imdb=%s&url=%s&image=%s&year=%s)' % (sys.argv[0], sysname, sysimdb, sysurl, sysimage, sysyear)))
                    else: cm.append((language(30424).encode("utf-8"), 'RunPlugin(%s?action=library_delete&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                    if not getSetting("fav_sort") == '2': cm.append((language(30418).encode("utf-8"), 'RunPlugin(%s?action=favourite_delete&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl))) 
                    if getSetting("fav_sort") == '2': cm.append((language(30419).encode("utf-8"), 'RunPlugin(%s?action=favourite_moveUp&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                    if getSetting("fav_sort") == '2': cm.append((language(30420).encode("utf-8"), 'RunPlugin(%s?action=favourite_moveDown&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                    if getSetting("fav_sort") == '2': cm.append((language(30421).encode("utf-8"), 'RunPlugin(%s?action=favourite_delete&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                    if getmeta == 'true': cm.append((language(30415).encode("utf-8"), 'RunPlugin(%s?action=metadata_tvshows&imdb=%s)' % (sys.argv[0], metaimdb)))
                elif action == 'shows_subscriptions':
                    if not '"%s"' % url in subRead: cm.append((language(30423).encode("utf-8"), 'RunPlugin(%s?action=library_add&name=%s&imdb=%s&url=%s&image=%s&year=%s)' % (sys.argv[0], sysname, sysimdb, sysurl, sysimage, sysyear)))
                    else: cm.append((language(30424).encode("utf-8"), 'RunPlugin(%s?action=library_delete&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                    if not '"%s"' % url in favRead: cm.append((language(30417).encode("utf-8"), 'RunPlugin(%s?action=favourite_add&name=%s&imdb=%s&url=%s&image=%s&year=%s)' % (sys.argv[0], sysname, sysimdb, sysurl, sysimage, sysyear)))
                    else: cm.append((language(30418).encode("utf-8"), 'RunPlugin(%s?action=favourite_delete&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                    if getmeta == 'true': cm.append((language(30415).encode("utf-8"), 'RunPlugin(%s?action=metadata_tvshows&imdb=%s)' % (sys.argv[0], metaimdb)))
                    cm.append((language(30425).encode("utf-8"), 'RunPlugin(%s?action=library_update)' % (sys.argv[0])))
                elif action.startswith('shows_search'):
                    cm.append((language(30423).encode("utf-8"), 'RunPlugin(%s?action=library_from_search&name=%s&imdb=%s&url=%s&image=%s&year=%s)' % (sys.argv[0], sysname, sysimdb, sysurl, sysimage, sysyear)))
                    cm.append((language(30417).encode("utf-8"), 'RunPlugin(%s?action=favourite_from_search&name=%s&imdb=%s&url=%s&image=%s&year=%s)' % (sys.argv[0], sysname, sysimdb, sysurl, sysimage, sysyear)))
                else:
                    if not '"%s"' % url in subRead: cm.append((language(30423).encode("utf-8"), 'RunPlugin(%s?action=library_add&name=%s&imdb=%s&url=%s&image=%s&year=%s)' % (sys.argv[0], sysname, sysimdb, sysurl, sysimage, sysyear)))
                    else: cm.append((language(30424).encode("utf-8"), 'RunPlugin(%s?action=library_delete&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                    if not '"%s"' % url in favRead: cm.append((language(30417).encode("utf-8"), 'RunPlugin(%s?action=favourite_add&name=%s&imdb=%s&url=%s&image=%s&year=%s)' % (sys.argv[0], sysname, sysimdb, sysurl, sysimage, sysyear)))
                    else: cm.append((language(30418).encode("utf-8"), 'RunPlugin(%s?action=favourite_delete&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                    if getmeta == 'true': cm.append((language(30415).encode("utf-8"), 'RunPlugin(%s?action=metadata_tvshows2&imdb=%s)' % (sys.argv[0], metaimdb)))

                cm.append((language(30429).encode("utf-8"), 'RunPlugin(%s?action=view_tvshows)' % (sys.argv[0])))
                cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))
                cm.append((language(30410).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                cm.append((language(30411).encode("utf-8"), 'RunPlugin(%s?action=addon_home)' % (sys.argv[0])))

                if action == 'shows_search':
                    if ('"%s"' % url in favRead and '"%s"' % url in subRead): suffix = '|F|S| '
                    elif '"%s"' % url in favRead: suffix = '|F| '
                    elif '"%s"' % url in subRead: suffix = '|S| '
                    else: suffix = ''
                    name = suffix + name

                item = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=poster)
                item.setInfo( type="Video", infoLabels = meta )
                item.setProperty("IsPlayable", "true")
                item.setProperty("Video", "true")
                item.setProperty("Fanart_Image", fanart)
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

    def seasonList(self, seasonList):
        if seasonList == None: return

        try:
            year, imdb, tvdb, genre, plot, show, show_alt = seasonList[0]['year'], seasonList[0]['imdb'], seasonList[0]['tvdb'], seasonList[0]['genre'], seasonList[0]['plot'], seasonList[0]['show'], seasonList[0]['show_alt']
            if plot == '': plot = addonDesc
            if genre == '': genre = ' '

            if getSetting("meta") == 'true':
                seasons = []
                for i in seasonList: seasons.append(i['season'])
                season_meta = metaget.get_seasons(show, imdb, seasons)
                meta = metaget.get_meta('tvshow', show, imdb_id=imdb)
                banner = meta['banner_url']
            else:
                meta = {'tvshowtitle': show, 'imdb_id' : imdb, 'genre' : genre, 'plot': plot}
                banner = ''
            if getSetting("meta") == 'true' and getSetting("fanart") == 'true':
                fanart = meta['backdrop_url']
                if fanart == '': fanart = addonFanart
            else:
                fanart = addonFanart
        except:
            return

        total = len(seasonList)
        for i in range(0, int(total)):
            try:
                name, url, image = seasonList[i]['name'], seasonList[i]['url'], seasonList[i]['image']
                sysname, sysurl, sysimage, sysyear, sysimdb, systvdb, sysgenre, sysplot, sysshow, sysshow_alt = urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(image), urllib.quote_plus(year), urllib.quote_plus(imdb), urllib.quote_plus(tvdb), urllib.quote_plus(genre), urllib.quote_plus(plot), urllib.quote_plus(show), urllib.quote_plus(show_alt)
                u = '%s?action=episodes&name=%s&url=%s&image=%s&year=%s&imdb=%s&tvdb=%s&genre=%s&plot=%s&show=%s&show_alt=%s' % (sys.argv[0], sysname, sysurl, sysimage, sysyear, sysimdb, systvdb, sysgenre, sysplot, sysshow, sysshow_alt)

                if getSetting("meta") == 'true':
                    meta.update({'playcount': 0, 'overlay': 0})
                    #meta.update({'playcount': season_meta[i]['playcount'], 'overlay': season_meta[i]['overlay']})
                    poster = season_meta[i]['cover_url']
                    playcountMenu = language(30407).encode("utf-8")
                    if season_meta[i]['overlay'] == 6: playcountMenu = language(30408).encode("utf-8")
                    metaimdb, metaseason = urllib.quote_plus(re.sub('[^0-9]', '', str(season_meta[i]['imdb_id']))), urllib.quote_plus(str(season_meta[i]['season']))
                    if poster == '': poster = image
                    if banner == '': banner = poster
                    if banner == '': banner = image
                else:
                    poster, banner = image, image

                meta.update({'label': name, 'title': name, 'art(season.banner)': banner, 'art(season.poster': poster})

                cm = []
                cm.append((language(30413).encode("utf-8"), 'Action(Info)'))
                if getSetting("meta") == 'true': cm.append((language(30415).encode("utf-8"), 'RunPlugin(%s?action=metadata_seasons&imdb=%s&season=%s)' % (sys.argv[0], metaimdb, metaseason)))
                cm.append((language(30430).encode("utf-8"), 'RunPlugin(%s?action=view_seasons)' % (sys.argv[0])))
                cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))
                cm.append((language(30410).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                cm.append((language(30411).encode("utf-8"), 'RunPlugin(%s?action=addon_home)' % (sys.argv[0])))

                item = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=poster)
                item.setInfo( type="Video", infoLabels = meta )
                item.setProperty("IsPlayable", "true")
                item.setProperty("Video", "true")
                item.setProperty("Fanart_Image", fanart)
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

    def episodeList(self, episodeList):
        if episodeList == None: return

        autoplay = getSetting("autoplay")
        if index().getProperty('PseudoTVRunning') == 'True': autoplay = 'true'

        getmeta = getSetting("meta")
        if action == 'episodes_calendar': getmeta = ''

        total = len(episodeList)
        for i in episodeList:
            try:
                name, url, image, date, year, imdb, tvdb, genre, plot, title, show, show_alt, season, episode = i['name'], i['url'], i['image'], i['date'], i['year'], i['imdb'], i['tvdb'], i['genre'], i['plot'], i['title'], i['show'], i['show_alt'], i['season'], i['episode']
                if plot == '': plot = addonDesc
                if genre == '': genre = ' '

                sysname, sysurl, sysimage, sysdate, sysyear, sysimdb, systvdb, sysgenre, sysplot, systitle, sysshow, sysshow_alt, sysseason, sysepisode = urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(image), urllib.quote_plus(date), urllib.quote_plus(year), urllib.quote_plus(imdb), urllib.quote_plus(tvdb), urllib.quote_plus(genre), urllib.quote_plus(plot), urllib.quote_plus(title), urllib.quote_plus(show), urllib.quote_plus(show_alt), urllib.quote_plus(season), urllib.quote_plus(episode)

                if not autoplay == 'false':
                    u = '%s?action=play&name=%s&title=%s&imdb=%s&tvdb=%s&year=%s&season=%s&episode=%s&show=%s&show_alt=%s&url=%s&t=%s' % (sys.argv[0], sysname, systitle, sysimdb, systvdb, sysyear, sysseason, sysepisode, sysshow, sysshow_alt, sysurl, datetime.datetime.now().strftime("%Y%m%d%H%M%S%f"))
                    isFolder = False
                else:
                    u = '%s?action=get_host&name=%s&url=%s&image=%s&date=%s&year=%s&imdb=%s&tvdb=%s&genre=%s&plot=%s&title=%s&show=%s&show_alt=%s&season=%s&episode=%s' % (sys.argv[0], sysname, sysurl, sysimage, sysdate, sysyear, sysimdb, systvdb, sysgenre, sysplot, systitle, sysshow, sysshow_alt, sysseason, sysepisode)
                    isFolder = True

                if getmeta == 'true':
                    imdb = re.sub('[^0-9]', '', imdb)
                    meta = metaget.get_episode_meta(title, imdb, season, episode)
                    meta.update({'tvshowtitle': show})
                    if meta['title'] == '': meta.update({'title': title})
                    if meta['episode'] == '': meta.update({'episode': episode})
                    if meta['premiered'] == '': meta.update({'premiered': date})
                    if meta['plot'] == '': meta.update({'plot': plot})
                    playcountMenu = language(30407).encode("utf-8")
                    if meta['overlay'] == 6: playcountMenu = language(30408).encode("utf-8")
                    metaimdb, metaseason, metaepisode = urllib.quote_plus(re.sub('[^0-9]', '', str(meta['imdb_id']))), urllib.quote_plus(str(meta['season'])), urllib.quote_plus(str(meta['episode']))
                    label = str(meta['season']) + 'x' + '%02d' % int(meta['episode']) + ' . ' + meta['title']
                    if action == 'episodes_subscriptions' or action == 'episodes_calendar': label = show + ' - ' + label
                    poster = meta['cover_url']
                    if poster == '': poster = image
                else:
                    meta = {'label': title, 'title': title, 'tvshowtitle': show, 'season': season, 'episode': episode, 'imdb_id' : imdb, 'year' : year, 'premiered' : date, 'genre' : genre, 'plot': plot}
                    label = season + 'x' + '%02d' % int(episode) + ' . ' + title
                    if action == 'episodes_subscriptions' or action == 'episodes_calendar': label = show + ' - ' + label
                    poster = image
                if getmeta == 'true' and getSetting("fanart") == 'true':
                    fanart = meta['backdrop_url']
                    if fanart == '': fanart = addonFanart
                else:
                    fanart = addonFanart

                cm = []
                cm.append((language(30433).encode("utf-8"), 'RunPlugin(%s?action=autoplay&name=%s&title=%s&imdb=%s&tvdb=%s&year=%s&season=%s&episode=%s&show=%s&show_alt=%s&url=%s)' % (sys.argv[0], sysname, systitle, sysimdb, systvdb, sysyear, sysseason, sysepisode, sysshow, sysshow_alt, sysurl)))
                cm.append((language(30414).encode("utf-8"), 'Action(Info)'))
                if getmeta == 'true': cm.append((language(30415).encode("utf-8"), 'RunPlugin(%s?action=metadata_episodes&imdb=%s&season=%s&episode=%s)' % (sys.argv[0], metaimdb, metaseason, metaepisode)))
                if getmeta == 'true': cm.append((playcountMenu, 'RunPlugin(%s?action=playcount_episodes&imdb=%s&season=%s&episode=%s)' % (sys.argv[0], metaimdb, metaseason, metaepisode)))
                cm.append((language(30431).encode("utf-8"), 'RunPlugin(%s?action=view_episodes)' % (sys.argv[0])))
                cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))
                cm.append((language(30410).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                cm.append((language(30411).encode("utf-8"), 'RunPlugin(%s?action=addon_home)' % (sys.argv[0])))

                item = xbmcgui.ListItem(label, iconImage="DefaultVideo.png", thumbnailImage=poster)
                item.setInfo( type="Video", infoLabels = meta )
                item.setProperty("IsPlayable", "true")
                item.setProperty("Video", "true")
                item.setProperty("Fanart_Image", fanart)
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=isFolder)
            except:
                pass

    def sourceList(self, sourceList):
        if sourceList == None: return

        try:
            name, image, date, year, imdb, tvdb, genre, plot, title, show, show_alt, season, episode = sourceList[0]['name'], sourceList[0]['image'], sourceList[0]['date'], sourceList[0]['year'], sourceList[0]['imdb'], sourceList[0]['tvdb'], sourceList[0]['genre'], sourceList[0]['plot'], sourceList[0]['title'], sourceList[0]['show'], sourceList[0]['show_alt'], sourceList[0]['season'], sourceList[0]['episode']
            if plot == '': plot = addonDesc
            if genre == '': genre = ' '

            if getSetting("meta") == 'true':
                imdb = re.sub('[^0-9]', '', imdb)
                meta = metaget.get_episode_meta(title, imdb, season, episode)
                meta.update({'playcount': 0, 'overlay': 0})
                meta.update({'tvshowtitle': show})
                if meta['title'] == '': meta.update({'title': title})
                if meta['episode'] == '': meta.update({'episode': episode})
                if meta['premiered'] == '': meta.update({'premiered': date})
                if meta['plot'] == '': meta.update({'plot': plot})
                poster = meta['cover_url']
                if poster == '': poster = image
            else:
                meta = {'label': title, 'title': title, 'tvshowtitle': show, 'season': season, 'episode': episode, 'imdb_id' : imdb, 'year' : year, 'premiered' : date, 'genre' : genre, 'plot': plot}
                poster = image
            if getSetting("meta") == 'true' and getSetting("fanart") == 'true':
                fanart = meta['backdrop_url']
                if fanart == '': fanart = addonFanart
            else:
                fanart = addonFanart
        except:
            return

        total = len(sourceList)
        for i in sourceList:
            try:
                url, source, provider = i['url'], i['source'], i['provider']
                sysname, sysurl, sysimdb, syssource, sysprovider = urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(imdb), urllib.quote_plus(source), urllib.quote_plus(provider)

                u = '%s?action=play_host&name=%s&url=%s&imdb=%s&source=%s&provider=%s&t=%s' % (sys.argv[0], sysname, sysurl, sysimdb, syssource, sysprovider, datetime.datetime.now().strftime("%Y%m%d%H%M%S%f"))

                cm = []
                cm.append((language(30405).encode("utf-8"), 'RunPlugin(%s?action=item_queue)' % (sys.argv[0])))
                cm.append((language(30406).encode("utf-8"), 'RunPlugin(%s?action=download&name=%s&url=%s&provider=%s)' % (sys.argv[0], sysname, sysurl, sysprovider)))
                cm.append((language(30414).encode("utf-8"), 'Action(Info)'))
                cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))
                cm.append((language(30410).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                cm.append((language(30411).encode("utf-8"), 'RunPlugin(%s?action=addon_home)' % (sys.argv[0])))

                item = xbmcgui.ListItem(source, iconImage="DefaultVideo.png", thumbnailImage=poster)
                item.setInfo( type="Video", infoLabels = meta )
                item.setProperty("IsPlayable", "true")
                item.setProperty("Video", "true")
                item.setProperty("Fanart_Image", fanart)
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=False)
            except:
                pass

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

    def settings_open(self):
        xbmc.executebuiltin('Addon.OpenSettings(%s)' % (addonId))

    def addon_home(self):
        xbmc.executebuiltin('Container.Update(plugin://%s/,replace)' % (addonId))

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
                if not (label == '' or label is None): break
            file = xbmcvfs.File(viewData)
            read = file.read()
            file.close()
            write = [i.strip('\n').strip('\r') for i in read.splitlines(True) if i.strip('\r\n')]
            write = [i for i in write if not '"%s"|"%s"|"' % (skin, content) in i]
            write.append('"%s"|"%s"|"%s"' % (skin, content, str(view)))
            write = '\r\n'.join(write)
            file = xbmcvfs.File(viewData, 'w')
            file.write(str(write))
            file.close()
            viewName = xbmc.getInfoLabel('Container.Viewmode')
            index().infoDialog('%s%s%s' % (language(30301).encode("utf-8"), viewName, language(30302).encode("utf-8")))
        except:
            return

    def favourite_add(self, data, name, url, image, imdb, year):
        try:
            index().container_refresh()
            file = xbmcvfs.File(data)
            read = file.read()
            file.close()
            write = [i.strip('\n').strip('\r') for i in read.splitlines(True) if i.strip('\r\n')]
            write.append('"%s"|"%s"|"%s"|"%s"|"%s"' % (name, year, imdb, url, image))
            write = '\r\n'.join(write)
            file = xbmcvfs.File(data, 'w')
            file.write(str(write))
            file.close()
            index().infoDialog(language(30303).encode("utf-8"), name)
        except:
            return

    def favourite_from_search(self, data, name, url, image, imdb, year):
        try:
            file = xbmcvfs.File(data)
            read = file.read()
            file.close()
            if '"%s"' % url in read:
                index().infoDialog(language(30307).encode("utf-8"), name)
                return
            write = [i.strip('\n').strip('\r') for i in read.splitlines(True) if i.strip('\r\n')]
            write.append('"%s"|"%s"|"%s"|"%s"|"%s"' % (name, year, imdb, url, image))
            write = '\r\n'.join(write)
            file = xbmcvfs.File(data, 'w')
            file.write(str(write))
            file.close()
            index().infoDialog(language(30303).encode("utf-8"), name)
        except:
            return

    def favourite_delete(self, data, name, url):
        try:
            index().container_refresh()
            file = xbmcvfs.File(data)
            read = file.read()
            file.close()
            write = [i.strip('\n').strip('\r') for i in read.splitlines(True) if i.strip('\r\n')]
            write = [i for i in write if not '"%s"' % url in i]
            write = '\r\n'.join(write)
            file = xbmcvfs.File(data, 'w')
            file.write(str(write))
            file.close()
            index().infoDialog(language(30304).encode("utf-8"), name)
        except:
            return

    def favourite_moveUp(self, data, name, url):
        try:
            index().container_refresh()
            file = xbmcvfs.File(data)
            read = file.read()
            file.close()
            write = [i.strip('\n').strip('\r') for i in read.splitlines(True) if i.strip('\r\n')]
            i = write.index([i for i in write if '"%s"' % url in i][0])
            if i == 0 : return
            write[i], write[i-1] = write[i-1], write[i]
            write = '\r\n'.join(write)
            file = xbmcvfs.File(data, 'w')
            file.write(str(write))
            file.close()
            index().infoDialog(language(30305).encode("utf-8"), name)
        except:
            return

    def favourite_moveDown(self, data, name, url):
        try:
            index().container_refresh()
            file = xbmcvfs.File(data)
            read = file.read()
            file.close()
            write = [i.strip('\n').strip('\r') for i in read.splitlines(True) if i.strip('\r\n')]
            i = write.index([i for i in write if '"%s"' % url in i][0])
            if i+1 == len(write): return
            write[i], write[i+1] = write[i+1], write[i]
            write = '\r\n'.join(write)
            file = xbmcvfs.File(data, 'w')
            file.write(str(write))
            file.close()
            index().infoDialog(language(30306).encode("utf-8"), name)
        except:
            return

    def metadata(self, content, imdb, season, episode):
        try:
            if content == 'movie' or content == 'tvshow':
                metaget.update_meta(content, '', imdb, year='')
                index().container_refresh()
            elif content == 'season':
                metaget.update_episode_meta('', imdb, season, episode)
                index().container_refresh()
            elif content == 'episode':
                metaget.update_season('', imdb, season)
                index().container_refresh()
        except:
            return

    def playcount(self, content, imdb, season, episode):
        try:
            metaget.change_watched(content, '', imdb, season=season, episode=episode, year='', watched='')
            index().container_refresh()
        except:
            return

    def library_add(self, name, url, image, imdb, year, update=True, silent=False):
        try:
            file = xbmcvfs.File(subData)
            read = file.read()
            file.close()

            lib = self.library(name, url, imdb, year, check=True, silent=True)
            if (silent == False and lib == False):
                yes = index().yesnoDialog(language(30348).encode("utf-8"), language(30349).encode("utf-8"), name)
                if yes:
                    self.library(name, url, imdb, year, silent=True)
                else:
                    return
            elif lib == False:
                return

            write = [i.strip('\n').strip('\r') for i in read.splitlines(True) if i.strip('\r\n')]
            write.append('"%s"|"%s"|"%s"|"%s"|"%s"' % (name, year, imdb, url, image))
            write = '\r\n'.join(write)
            file = xbmcvfs.File(subData, 'w')
            file.write(str(write))
            file.close()
            if silent == False:
                index().container_refresh()
                index().infoDialog(language(30312).encode("utf-8"), name)
            if update == True:
                xbmc.executebuiltin('UpdateLibrary(video)')
        except:
            return

    def library_from_search(self, name, url, image, imdb, year, update=True, silent=False):
        try:
            file = xbmcvfs.File(subData)
            read = file.read()
            file.close()

            if '"%s"' % url in read:
                index().infoDialog(language(30316).encode("utf-8"), name)
                return

            lib = self.library(name, url, imdb, year, check=True, silent=True)
            if (silent == False and lib == False):
                yes = index().yesnoDialog(language(30348).encode("utf-8"), language(30349).encode("utf-8"), name)
                if yes:
                    self.library(name, url, imdb, year, silent=True)
                else:
                    return
            elif lib == False:
                return

            write = [i.strip('\n').strip('\r') for i in read.splitlines(True) if i.strip('\r\n')]
            write.append('"%s"|"%s"|"%s"|"%s"|"%s"' % (name, year, imdb, url, image))
            write = '\r\n'.join(write)
            file = xbmcvfs.File(subData, 'w')
            file.write(str(write))
            file.close()
            if silent == False:
                index().container_refresh()
                index().infoDialog(language(30312).encode("utf-8"), name)
            if update == True:
                xbmc.executebuiltin('UpdateLibrary(video)')
        except:
            return

    def library_delete(self, name, url, silent=False):
        try:
            file = xbmcvfs.File(subData)
            read = file.read()
            file.close()
            write = [i.strip('\n').strip('\r') for i in read.splitlines(True) if i.strip('\r\n')]
            write = [i for i in write if not '"%s"' % url in i]
            write = '\r\n'.join(write)
            file = xbmcvfs.File(subData, 'w')
            file.write(str(write))
            file.close()

            if silent == False:
                index().container_refresh()
                index().infoDialog(language(30313).encode("utf-8"), name)
        except:
            return

    def library_update(self, silent=False):
        if getSetting("trakt_import") == '1' and not (link().trakt_user == '' or link().trakt_password == ''):
            url = link().trakt_collection % (link().trakt_key, link().trakt_user)
            self.library_batch2(url)
        elif getSetting("trakt_import") == '2' and not (link().trakt_user == '' or link().trakt_password == ''):
            url = link().trakt_watchlist % (link().trakt_key, link().trakt_user)
            self.library_batch2(url)
        self.library_batch3()
        if getSetting("updatelibrary") == 'true':
            xbmc.executebuiltin('UpdateLibrary(video)')
        if silent == False:
            index().infoDialog(language(30314).encode("utf-8"))

    def library_batch(self, url, update=True, silent=False):
        try:
            file = xbmcvfs.File(subData)
            read = file.read()
            file.close()
        except:
            return

        if url == 'shows_trending':
            showList = shows().trending(idx=False)
        else:
            showList = shows().get(url, idx=False)

        if showList == None: return
        for i in showList:
            if xbmc.abortRequested == True: sys.exit()
            show = re.sub('\s(|[(])(UK|US|AU|\d{4})(|[)])$', '', i['name'])
            if '"%s"' % i['url'] in read:
                self.library(show, i['url'], i['imdb'], i['year'], silent=True)
            else:
                try: self.library_add(show, i['url'], i['image'], i['imdb'], i['year'], update=False, silent=True)
                except: pass
        if silent == False:
            index().infoDialog(language(30312).encode("utf-8"))
        if update == True and getSetting("updatelibrary") == 'true':
            xbmc.executebuiltin('UpdateLibrary(video)')

    def library_batch2(self, url):
        try:
            file = xbmcvfs.File(subData)
            read = file.read()
            file.close()
        except:
            return

        if url == 'shows_trending':
            showList = shows().trending(idx=False)
        else:
            showList = shows().get(url, idx=False)

        if showList == None: return
        for i in showList:
            if xbmc.abortRequested == True: sys.exit()
            show = re.sub('\s(|[(])(UK|US|AU|\d{4})(|[)])$', '', i['name'])
            if not '"%s"' % i['url'] in read:
                try: self.library_add(show, i['url'], i['image'], i['imdb'], i['year'], update=False, silent=True)
                except: pass

    def library_batch3(self):
        try:
            file = xbmcvfs.File(subData)
            read = file.read()
            file.close()
            match = re.compile('"(.+?)"[|]"(.+?)"[|]"(.+?)"[|]"(.+?)"[|]"(.+?)"').findall(read)
            for name, year, imdb, url, image in match:
                if xbmc.abortRequested == True: sys.exit()
                self.library(name, url, imdb, year, silent=True)
        except:
            return

    def library(self, name, url, imdb, year, check=False, silent=False):
        try:
            library = xbmc.translatePath(getSetting("tv_library"))
            xbmcvfs.mkdir(dataPath)
            xbmcvfs.mkdir(library)
            show = name
            seasonList = seasons().get(url, '', year, imdb, '', '', show, idx=False)
            year, tvdb = seasonList[0]['year'], seasonList[0]['tvdb']
            if tvdb == '0': return
        except:
            return

        try:
            if check == False: raise Exception()
            data = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetTVShows", "params": {"filter":{"or": [{"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}]}, "properties" : ["imdbnumber"]}, "id": 1}' % (year, str(int(year)+1), str(int(year)-1)))
            data = unicode(data, 'utf-8', errors='ignore')
            data = json.loads(data)
            data = data['result']['tvshows']
            data = [i for i in data if tvdb in i['imdbnumber']][0]
            return False
        except:
            pass

        try:
            for i in seasonList:
                season, seasonUrl, tvdb, show_alt, idx_data = i['name'], i['url'], i['tvdb'], i['show_alt'], i['idx_data']
                enc_show = show_alt.translate(None, '\/:*?"<>|')
                folder = os.path.join(library, enc_show)
                xbmcvfs.mkdir(folder)
                enc_season = season.translate(None, '\/:*?"<>|')
                seasonDir = os.path.join(folder, enc_season)
                xbmcvfs.mkdir(seasonDir)
                episodeList = episodes().get(season, seasonUrl, '', year, imdb, tvdb, '', '', show, show_alt, idx_data, idx=False)
                for i in episodeList:
                    name, title, imdb, tvdb, year, season, episode, show, show_alt, date = i['name'], i['title'], i['imdb'], i['tvdb'], i['year'], i['season'], i['episode'], i['show'], i['show_alt'], i['date']
                    sysname, systitle, sysimdb, systvdb, sysyear, sysseason, sysepisode, sysshow, sysshow_alt, sysdate = urllib.quote_plus(name), urllib.quote_plus(title), urllib.quote_plus(imdb), urllib.quote_plus(tvdb), urllib.quote_plus(year), urllib.quote_plus(season), urllib.quote_plus(episode), urllib.quote_plus(show), urllib.quote_plus(show_alt), urllib.quote_plus(date)
                    content = '%s?action=play&name=%s&title=%s&imdb=%s&tvdb=%s&year=%s&season=%s&episode=%s&show=%s&show_alt=%s&date=%s' % (sys.argv[0], sysname, systitle, sysimdb, systvdb, sysyear, sysseason, sysepisode, sysshow, sysshow_alt, sysdate)
                    enc_name = name.translate(None, '\/:*?"<>|')
                    stream = os.path.join(seasonDir, enc_name + '.strm')
                    file = xbmcvfs.File(stream, 'w')
                    file.write(str(content))
                    file.close()
            if silent == False:
                index().infoDialog(language(30311).encode("utf-8"), show)
        except:
            return

    def download(self, name, url, provider):
        try:
            property = (addonName+name)+'download'
            download = xbmc.translatePath(getSetting("downloads"))
            enc_name = name.translate(None, '\/:*?"<>|')
            xbmcvfs.mkdir(dataPath)
            xbmcvfs.mkdir(download)

            file = [i for i in xbmcvfs.listdir(download)[1] if i.startswith(enc_name + '.')]
            if not file == []: file = os.path.join(download, file[0])
            else: file = None

            if download == '':
            	yes = index().yesnoDialog(language(30341).encode("utf-8"), language(30342).encode("utf-8"))
            	if yes: contextMenu().settings_open()
            	return

            if file is None:
            	pass
            elif not file.endswith('.tmp'):
            	yes = index().yesnoDialog(language(30343).encode("utf-8"), language(30344).encode("utf-8"), name)
            	if yes:
            	    xbmcvfs.delete(file)
            	else:
            	    return
            elif file.endswith('.tmp'):
            	if index().getProperty(property) == 'open':
            	    yes = index().yesnoDialog(language(30345).encode("utf-8"), language(30346).encode("utf-8"), name)
            	    if yes: index().setProperty(property, 'cancel')
            	    return
            	else:
            	    xbmcvfs.delete(file)

            url = resolver().sources_resolve(url, provider)
            if url is None: return
            url = url.rsplit('|', 1)[0]
            ext = url.rsplit('/', 1)[-1].rsplit('?', 1)[0].rsplit('|', 1)[0].strip().lower()
            ext = os.path.splitext(ext)[1][1:]
            if ext == '' or ext == 'php': ext = 'mp4'
            stream = os.path.join(download, enc_name + '.' + ext)
            temp = stream + '.tmp'

            count = 0
            CHUNK = 16 * 1024
            request = urllib2.Request(url)
            request.add_header('User-Agent', 'Mozilla/5.0 (iPhone; CPU; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7')
            request.add_header('Cookie', 'video=true')
            response = urllib2.urlopen(request, timeout=10)
            size = response.info()["Content-Length"]

            file = xbmcvfs.File(temp, 'w')
            index().setProperty(property, 'open')
            index().infoDialog(language(30308).encode("utf-8"), name)
            while True:
            	chunk = response.read(CHUNK)
            	if not chunk: break
            	if index().getProperty(property) == 'cancel': raise Exception()
            	if xbmc.abortRequested == True: raise Exception()
            	part = xbmcvfs.File(temp)
            	quota = int(100 * float(part.size())/float(size))
            	part.close()
            	if not count == quota and count in [0,10,20,30,40,50,60,70,80,90]:
            		index().infoDialog(language(30309).encode("utf-8") + str(count) + '%', name)
            	file.write(chunk)
            	count = quota
            response.close()
            file.close()

            index().clearProperty(property)
            xbmcvfs.rename(temp, stream)
            index().infoDialog(language(30310).encode("utf-8"), name)
        except:
            file.close()
            index().clearProperty(property)
            xbmcvfs.delete(temp)
            sys.exit()
            return

    def autoplay(self, name, title, imdb, tvdb, year, season, episode, show, show_alt):
        meta = {'title': xbmc.getInfoLabel('ListItem.title'), 'tvshowtitle': xbmc.getInfoLabel('ListItem.tvshowtitle'), 'season': xbmc.getInfoLabel('ListItem.season'), 'episode': xbmc.getInfoLabel('ListItem.episode'), 'writer': xbmc.getInfoLabel('ListItem.writer'), 'director': xbmc.getInfoLabel('ListItem.director'), 'rating': xbmc.getInfoLabel('ListItem.rating'), 'duration': xbmc.getInfoLabel('ListItem.duration'), 'premiered': xbmc.getInfoLabel('ListItem.premiered'), 'plot': xbmc.getInfoLabel('ListItem.plot')}
        label, poster, fanart = xbmc.getInfoLabel('ListItem.label'), xbmc.getInfoLabel('ListItem.icon'), xbmc.getInfoLabel('ListItem.Property(Fanart_Image)')

        sysname, systitle, sysimdb, systvdb, sysyear, sysseason, sysepisode, sysshow, sysshow_alt = urllib.quote_plus(name), urllib.quote_plus(title), urllib.quote_plus(imdb), urllib.quote_plus(tvdb), urllib.quote_plus(year), urllib.quote_plus(season), urllib.quote_plus(episode), urllib.quote_plus(show), urllib.quote_plus(show_alt)
        u = '%s?action=play&name=%s&title=%s&imdb=%s&tvdb=%s&year=%s&season=%s&episode=%s&show=%s&show_alt=%s&url=play://' % (sys.argv[0], sysname, systitle, sysimdb, systvdb, sysyear, sysseason, sysepisode, sysshow, sysshow_alt)

        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        item = xbmcgui.ListItem(label, iconImage="DefaultVideo.png", thumbnailImage=poster)
        item.setInfo( type="Video", infoLabels= meta )
        item.setProperty("IsPlayable", "true")
        item.setProperty("Video", "true")
        item.setProperty("Fanart_Image", fanart)
        xbmc.Player().play(u, item)

class subscriptions:
    def __init__(self):
        self.list = []

    def shows(self):
        file = xbmcvfs.File(subData)
        read = file.read()
        file.close()
        match = re.compile('"(.+?)"[|]"(.+?)"[|]"(.+?)"[|]"(.+?)"[|]"(.+?)"').findall(read)
        for name, year, imdb, url, image in match:
            self.list.append({'name': name, 'url': url, 'image': image, 'year': year, 'imdb': imdb, 'genre': '', 'plot': ''})
        self.list = sorted(self.list, key=itemgetter('name'))
        index().showList(self.list)

    def episodes(self):
        try:
            file = xbmcvfs.File(subData)
            read = file.read()
            file.close()

            if read == '':
                index().okDialog(language(30323).encode("utf-8"), language(30324).encode("utf-8"))
            if not getSetting("subscriptions_update") == 'true':
                index().okDialog(language(30325).encode("utf-8"), language(30326).encode("utf-8"))

            imdbDict, seasons, episodes = {}, [], []
            library = xbmc.translatePath(getSetting("tv_library"))
            match = re.compile('"(.+?)"[|]"(.+?)"[|]"(.+?)"[|]"(.+?)"[|]"(.+?)"').findall(read)
            for name, year, imdb, url, image in match: imdbDict.update({imdb:image})
            shows = [os.path.join(library, i) for i in xbmcvfs.listdir(library)[0]]
            for show in shows: seasons += [os.path.join(show, i) for i in xbmcvfs.listdir(show)[0]]
            for season in seasons: episodes += [os.path.join(season, i) for i in xbmcvfs.listdir(season)[1] if i.endswith('.strm')]
        except:
            pass

        for episode in episodes:
            try:
                file = xbmcvfs.File(episode)
                read = file.read()
                read = read.encode("utf-8")
                file.close()
                if not read.startswith(sys.argv[0]): raise Exception()
                params = {}
                query = read[read.find('?') + 1:].split('&')
                for i in query: params[i.split('=')[0]] = i.split('=')[1]
                name, title, imdb, tvdb, year, season, episode, show, show_alt, date = urllib.unquote_plus(params["name"]), urllib.unquote_plus(params["title"]), urllib.unquote_plus(params["imdb"]), urllib.unquote_plus(params["tvdb"]), urllib.unquote_plus(params["year"]), urllib.unquote_plus(params["season"]), urllib.unquote_plus(params["episode"]), urllib.unquote_plus(params["show"]), urllib.unquote_plus(params["show_alt"]), urllib.unquote_plus(params["date"])
                image = imdbDict[imdb]
                sort = date.replace('-','')
                self.list.append({'name': name, 'url': name, 'image': image, 'date': date, 'year': year, 'imdb': imdb, 'tvdb': tvdb, 'genre': '', 'plot': '', 'title': title, 'show': show, 'show_alt': show_alt, 'season': season, 'episode': episode, 'sort': sort})
            except:
                pass

        self.list = sorted(self.list, key=itemgetter('sort'))
        self.list = self.list[::-1][:100]

        index().episodeList(self.list)

class favourites:
    def __init__(self):
        self.list = []

    def shows(self):
        file = xbmcvfs.File(favData)
        read = file.read()
        file.close()
        match = re.compile('"(.+?)"[|]"(.+?)"[|]"(.+?)"[|]"(.+?)"[|]"(.+?)"').findall(read)
        for name, year, imdb, url, image in match:
            if getSetting("fav_sort") == '1':
                try: status = metaget.get_meta('tvshow', name, imdb_id=imdb)['status']
                except: status = ''
            else:
                status = ''
            self.list.append({'name': name, 'url': url, 'image': image, 'year': year, 'imdb': imdb, 'genre': '', 'plot': '', 'status': status})

        if getSetting("fav_sort") == '0':
            self.list = sorted(self.list, key=itemgetter('name'))
        elif getSetting("fav_sort") == '1':
            filter = []
            self.list = sorted(self.list, key=itemgetter('name'))
            filter += [i for i in self.list if not i['status'] == 'Ended']
            filter += [i for i in self.list if i['status'] == 'Ended']
            self.list = filter

        index().showList(self.list)

class root:
    def get(self):
        rootList = []
        rootList.append({'name': 30501, 'image': 'Episodes.png', 'action': 'episodes_subscriptions'})
        rootList.append({'name': 30502, 'image': 'Calendar.png', 'action': 'calendar_episodes'})
        rootList.append({'name': 30503, 'image': 'Popular.png', 'action': 'shows_popular'})
        rootList.append({'name': 30504, 'image': 'Rating.png', 'action': 'shows_rating'})
        rootList.append({'name': 30505, 'image': 'Views.png', 'action': 'shows_views'})
        rootList.append({'name': 30506, 'image': 'Active.png', 'action': 'shows_active'})
        rootList.append({'name': 30507, 'image': 'Trending.png', 'action': 'shows_trending'})
        rootList.append({'name': 30508, 'image': 'Genres.png', 'action': 'genres_shows'})
        if not (getSetting("trakt_user") == '' or getSetting("trakt_password") == ''):
            rootList.append({'name': 30509, 'image': 'Trakt.png', 'action': 'userlists_trakt'})
        if not (getSetting("imdb_user") == ''):
            rootList.append({'name': 30510, 'image': 'IMDb.png', 'action': 'userlists_imdb'})
        rootList.append({'name': 30511, 'image': 'Favourites.png', 'action': 'shows_favourites'})
        rootList.append({'name': 30512, 'image': 'Subscriptions.png', 'action': 'shows_subscriptions'})
        rootList.append({'name': 30513, 'image': 'Search.png', 'action': 'root_search'})
        index().rootList(rootList)
        index().downloadList()

    def search(self):
        rootList = []
        rootList.append({'name': 30521, 'image': 'TVShows.png', 'action': 'shows_search'})
        rootList.append({'name': 30522, 'image': 'Actors.png', 'action': 'actors_search'})
        index().rootList(rootList)


class link:
    def __init__(self):
        self.imdb_base = 'http://www.imdb.com'
        self.imdb_akas = 'http://akas.imdb.com'
        self.imdb_mobile = 'http://m.imdb.com'
        self.imdb_genre = 'http://akas.imdb.com/genre/'
        self.imdb_title = 'http://www.imdb.com/title/tt%s/'
        self.imdb_seasons = 'http://akas.imdb.com/title/tt%s/episodes'
        self.imdb_episodes = 'http://www.imdb.com/title/tt%s/episodes?season=%s'
        self.imdb_image = 'http://i.media-imdb.com/images/SF1b61b592d2fa1b9cfb8336f160e1efcf/nopicture/medium/tv.png'
        self.imdb_genres = 'http://akas.imdb.com/search/title?title_type=tv_series,mini_series&sort=moviemeter,asc&count=25&start=1&genres=%s'
        self.imdb_popular = 'http://akas.imdb.com/search/title?title_type=tv_series,mini_series&sort=moviemeter,asc&count=25&start=1'
        self.imdb_rating = 'http://akas.imdb.com/search/title?title_type=tv_series,mini_series&sort=user_rating,desc&count=25&start=1'
        self.imdb_views = 'http://akas.imdb.com/search/title?title_type=tv_series,mini_series&sort=num_votes,desc&count=25&start=1'
        self.imdb_active = 'http://akas.imdb.com/search/title?title_type=tv_series,mini_series&production_status=active&sort=moviemeter,asc&count=25&start=1'
        self.imdb_search = 'http://akas.imdb.com/search/title?title_type=tv_series,mini_series&sort=moviemeter,asc&count=25&start=1&title=%s'
        self.imdb_actors_search = 'http://www.imdb.com/search/name?count=100&name=%s'
        self.imdb_actors = 'http://m.imdb.com/name/nm%s/filmotype/%s'

        self.imdb_userlists = 'http://akas.imdb.com/user/%s/lists?tab=all&sort=modified:desc&filter=titles'
        self.imdb_watchlist ='http://akas.imdb.com/user/%s/watchlist?sort=moviemeter,asc&mode=detail&page=1'
        self.imdb_watchadded ='http://akas.imdb.com/user/%s/watchlist?sort=date_added,desc&mode=detail&page=1'
        self.imdb_watchtitle ='http://akas.imdb.com/user/%s/watchlist?sort=alpha,asc&mode=detail&page=1'
        self.imdb_list ='http://akas.imdb.com/list/%s/?view=detail&count=100&sort=listorian:asc&start=1'
        self.imdb_user = 'ur' + getSetting("imdb_user").replace('ur', '')

        self.tvdb_base = 'http://thetvdb.com'
        self.tvdb_key = base64.urlsafe_b64decode('MUQ2MkYyRjkwMDMwQzQ0NA==')
        self.tvdb_series = 'http://thetvdb.com/api/GetSeriesByRemoteID.php?imdbid=tt%s&language=en'
        self.tvdb_series2 = 'http://thetvdb.com/api/GetSeries.php?seriesname=%s&language=en'
        self.tvdb_episodes = 'http://thetvdb.com/api/%s/series/%s/all/en.xml'
        self.tvdb_thumb = 'http://thetvdb.com/banners/_cache/'

        self.trakt_base = 'http://api.trakt.tv'
        self.trakt_key = base64.urlsafe_b64decode('YmU2NDI5MWFhZmJiYmU2MmZkYzRmM2FhMGVkYjQwNzM=')
        self.trakt_summary = 'http://api.trakt.tv/show/summary.json/%s/%s'
        self.trakt_trending = 'http://api.trakt.tv/shows/trending.json/%s'
        self.trakt_calendar = 'http://api.trakt.tv/calendar/shows.json/%s/%s/1' 
        self.trakt_user, self.trakt_password = getSetting("trakt_user"), getSetting("trakt_password")
        self.trakt_watchlist = 'http://api.trakt.tv/user/watchlist/shows.json/%s/%s'
        self.trakt_collection = 'http://api.trakt.tv/user/library/shows/collection.json/%s/%s'
        self.trakt_watched = 'http://api.trakt.tv/user/library/shows/watched.json/%s/%s'
        self.trakt_rated = 'http://api.trakt.tv/user/ratings/shows.json/%s/%s/rating/extended'
        self.trakt_lists = 'http://api.trakt.tv/user/lists.json/%s/%s'
        self.trakt_list= 'http://api.trakt.tv/user/list.json/%s/%s'

        self.tvrage_base = 'http://services.tvrage.com'
        self.tvrage_info = 'http://services.tvrage.com/feeds/full_show_info.php?sid=%s'

class actors:
    def __init__(self):
        self.list = []

    def search(self, query=None):
        if query is None:
            self.query = common.getUserInput(language(30362).encode("utf-8"), '')
        else:
            self.query = query
        if not (self.query is None or self.query == ''):
            self.query = link().imdb_actors_search % urllib.quote_plus(self.query)
            self.list = self.imdb_list(self.query)
            index().pageList(self.list)

    def imdb_list(self, url):
        try:
            result = getUrl(url).result
            result = result.decode('iso-8859-1').encode('utf-8')
            actors = common.parseDOM(result, "tr", attrs = { "class": ".+? detailed" })
        except:
            return
        for actor in actors:
            try:
                name = common.parseDOM(actor, "a", ret="title")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(actor, "a", ret="href")[0]
                url = re.findall('nm(\d*)', url, re.I)[0]
                type = common.parseDOM(actor, "span", attrs = { "class": "description" })[0]
                if 'Actress' in type: type = 'actress'
                elif 'Actor' in type: type = 'actor'
                else: raise Exception()
                url = link().imdb_actors % (url, type)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = common.parseDOM(actor, "img", ret="src")[0]
                if not ('._SX' in image or '._SY' in image): raise Exception()
                image = image.rsplit('._SX', 1)[0].rsplit('._SY', 1)[0] + '._SX500.' + image.rsplit('.', 1)[-1]
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image})
            except:
                pass

        return self.list

class genres:
    def __init__(self):
        self.list = []

    def get(self):
        #self.list = self.imdb_list()
        self.list = cache3(self.imdb_list)
        index().pageList(self.list)

    def imdb_list(self):
        try:
            result = getUrl(link().imdb_genre).result
            result = common.parseDOM(result, "div", attrs = { "class": "article" })
            result = [i for i in result if str('"tv_genres"') in i][0]
            genres = common.parseDOM(result, "td")
        except:
            return
        for genre in genres:
            try:
                name = common.parseDOM(genre, "a")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(genre, "a", ret="href")[0]
                try: url = re.compile('genres=(.+?)&').findall(url)[0]
                except: url = re.compile('/genre/(.+?)/').findall(url)[0]
                url = link().imdb_genres % url
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = addonGenres.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image})
            except:
                pass

        return self.list

class calendar:
    def __init__(self):
        self.list = []

    def get(self):
        self.list = self.trakt_list()
        index().pageList2(self.list)

    def trakt_list(self):
        now = datetime.datetime.utcnow() - datetime.timedelta(hours = 5)
        today = datetime.date(now.year, now.month, now.day)

        for i in range(0, 14):
            date = today - datetime.timedelta(days=i)
            date = str(date)
            date = date.encode('utf-8')
            image = addonCalendar.encode('utf-8')
            self.list.append({'name': date, 'url': date, 'image': image})

        return self.list

class userlists:
    def __init__(self):
        self.list = []

    def trakt(self):
        post = urllib.urlencode({'username': link().trakt_user, 'password': link().trakt_password})
        info = (link().trakt_key, link().trakt_user)
        image = addonLists.encode('utf-8')

        self.list.append({'name': language(30531).encode("utf-8"), 'url': link().trakt_watchlist % info, 'image': image})
        self.list.append({'name': language(30532).encode("utf-8"), 'url': link().trakt_collection % info, 'image': image})
        self.list.append({'name': language(30533).encode("utf-8"), 'url': link().trakt_watched % info, 'image': image})
        self.list.append({'name': language(30534).encode("utf-8"), 'url': link().trakt_rated % info, 'image': image})

        try:
            userlists = []
            result = getUrl(link().trakt_lists % info, post=post).result
            userlists = json.loads(result)
        except:
            pass

        for userlist in userlists:
            try:
                name = userlist['name']
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = userlist['slug']
                url = '%s/%s' % (link().trakt_list % info, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image})
            except:
                pass

        index().userList(self.list)

    def imdb(self):
        image = addonLists.encode('utf-8')

        self.list.append({'name': language(30541).encode("utf-8"), 'url': 'watchlist', 'image': image})
        self.list.append({'name': language(30542).encode("utf-8"), 'url': 'watchadded', 'image': image})
        self.list.append({'name': language(30543).encode("utf-8"), 'url': 'watchtitle', 'image': image})

        try:
            userlists = []
            result = getUrl(link().imdb_userlists % link().imdb_user).result
            result = result.decode('iso-8859-1').encode('utf-8')
            userlists = common.parseDOM(result, "div", attrs = { "class": "list_name" })
        except:
            pass

        for userlist in userlists:
            try:
                name = common.parseDOM(userlist, "a")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(userlist, "a", ret="href")[0]
                url = url.split('/list/', 1)[-1].replace('/', '')
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image})
            except:
                pass

        index().userList(self.list)

class shows:
    def __init__(self):
        self.list = []
        self.data = []

    def get(self, url, idx=True):
        if url.startswith(link().imdb_base) or url.startswith(link().imdb_akas):
            #self.list = self.imdb_list(url)
            self.list = cache(self.imdb_list, url)
        elif url.startswith(link().imdb_mobile):
            #self.list = self.imdb_list2(url)
            self.list = cache(self.imdb_list2, url)
        elif url.startswith(link().trakt_base):
            self.list = self.trakt_list(url)
        elif url == 'watchlist':
            self.list = self.imdb_list3(link().imdb_watchlist % link().imdb_user)
        elif url == 'watchadded':
            self.list = self.imdb_list3(link().imdb_watchadded % link().imdb_user)
        elif url == 'watchtitle':
            self.list = self.imdb_list3(link().imdb_watchtitle % link().imdb_user)
        else:
            self.list = self.imdb_list4(link().imdb_list % url)
            self.list = sorted(self.list, key=itemgetter('name'))

        if idx == False: return self.list
        index().showList(self.list)
        index().nextList(self.list)

    def popular(self):
        #self.list = self.imdb_list(link().imdb_popular)
        self.list = cache(self.imdb_list, link().imdb_popular)
        index().showList(self.list)
        index().nextList(self.list)

    def rating(self):
        #self.list = self.imdb_list(link().imdb_rating)
        self.list = cache(self.imdb_list, link().imdb_rating)
        index().showList(self.list)
        index().nextList(self.list)

    def views(self):
        #self.list = self.imdb_list(link().imdb_views)
        self.list = cache(self.imdb_list, link().imdb_views)
        index().showList(self.list)
        index().nextList(self.list)

    def active(self):
        #self.list = self.imdb_list(link().imdb_active)
        self.list = cache(self.imdb_list, link().imdb_active)
        index().showList(self.list)
        index().nextList(self.list)

    def trending(self, idx=True):
        #self.list = self.trakt_list(link().trakt_trending % link().trakt_key)
        self.list = cache2(self.trakt_list, link().trakt_trending % link().trakt_key)
        if idx == False: return self.list[:100]
        index().showList(self.list[:100])

    def search(self, query=None):
        if query is None:
            self.query = common.getUserInput(language(30362).encode("utf-8"), '')
        else:
            self.query = query
        if not (self.query is None or self.query == ''):
            self.query = link().imdb_search % urllib.quote_plus(self.query)
            self.list = self.imdb_list(self.query)
            index().showList(self.list)

    def imdb_list(self, url):
        try:
            result = getUrl(url.replace(link().imdb_base, link().imdb_akas)).result
            result = result.decode('iso-8859-1').encode('utf-8')
            shows = common.parseDOM(result, "tr", attrs = { "class": ".+?" })
        except:
            return

        try:
            next = common.parseDOM(result, "span", attrs = { "class": "pagination" })[0]
            name = common.parseDOM(next, "a")[-1]
            if 'laquo' in name: raise Exception()
            next = common.parseDOM(next, "a", ret="href")[-1]
            next = '%s%s' % (link().imdb_akas, next)
            next = common.replaceHTMLCodes(next)
            next = next.encode('utf-8')
        except:
            next = ''

        for show in shows:
            try:
                name = common.parseDOM(show, "a")[1]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                year = common.parseDOM(show, "span", attrs = { "class": "year_type" })[0]
                year = re.sub('[^0-9]', '', year)[:4]
                year = year.encode('utf-8')

                if int(year) > int((datetime.datetime.utcnow() - datetime.timedelta(hours = 5)).strftime("%Y")): raise Exception()

                url = common.parseDOM(show, "a", ret="href")[0]
                url = '%s%s' % (link().imdb_base, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                imdb = re.sub('[^0-9]', '', url.rsplit('tt', 1)[-1])
                imdb = imdb.encode('utf-8')

                try:
                    image = common.parseDOM(show, "img", ret="src")[0]
                    if not ('._SX' in image or '._SY' in image): raise Exception()
                    image = image.rsplit('._SX', 1)[0].rsplit('._SY', 1)[0] + '._SX500.' + image.rsplit('.', 1)[-1] 
                except:
                    image = link().imdb_image
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                try:
                    genre = common.parseDOM(show, "span", attrs = { "class": "genre" })
                    genre = common.parseDOM(genre, "a")
                    genre = " / ".join(genre)
                    genre = common.replaceHTMLCodes(genre)
                    genre = genre.encode('utf-8')
                except:
                    genre = ''

                try:
                    plot = common.parseDOM(show, "span", attrs = { "class": "outline" })[0]
                    plot = common.replaceHTMLCodes(plot)
                    plot = plot.encode('utf-8')
                except:
                    plot = ''

                self.list.append({'name': name, 'url': url, 'image': image, 'year': year, 'imdb': imdb, 'genre': genre, 'plot': plot, 'next': next})
            except:
                pass

        return self.list

    def imdb_list2(self, url):
        try:
            result = getUrl(url, mobile=True).result
            result = result.decode('iso-8859-1').encode('utf-8')
            shows = common.parseDOM(result, "div", attrs = { "class": "col-xs.+?" })
        except:
            return

        for show in shows:
            try:
                name = common.parseDOM(show, "span", attrs = { "class": "h3" })[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                year = common.parseDOM(show, "div", attrs = { "class": "unbold" })[0]
                if not 'series' in year.lower(): raise Exception()
                year = re.sub('[^0-9]', '', year)[:4]
                year = re.sub("\n|[(]|[)]|\s", "", year)
                year = year.encode('utf-8')

                if int(year) > int((datetime.datetime.utcnow() - datetime.timedelta(hours = 5)).strftime("%Y")): raise Exception()

                url = common.parseDOM(show, "a", ret="href")[0]
                url = re.findall('tt(\d*)', url, re.I)[0]
                url = link().imdb_title % url
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                imdb = re.sub('[^0-9]', '', url.rsplit('tt', 1)[-1])
                imdb = imdb.encode('utf-8')

                try:
                    image = common.parseDOM(show, "img", ret="src")[0]
                    if not ('_SX' in image or '_SY' in image): raise Exception()
                    image = image.rsplit('_SX', 1)[0].rsplit('_SY', 1)[0] + '_SX500.' + image.rsplit('.', 1)[-1]
                except:
                    image = link().imdb_image
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image, 'year': year, 'imdb': imdb, 'genre': '', 'plot': ''})
            except:
                pass

        return self.list

    def imdb_list3(self, url):
        try:
            URL = url.replace(link().imdb_base, link().imdb_akas)
            url = 'http://9proxy.in/b.php?u=%s&b=28' % urllib.quote_plus(urllib.unquote_plus(url))
            result = getUrl(url, referer=url).result

            try:
                threads = []
                pages = common.parseDOM(result, "div", attrs = { "class": "desc" })
                pages = [re.compile('of (\d+) titles').findall(i)[0] for i in pages][0]
                pages = (int(pages)+100)/100
                for i in range(1, int(pages)):
                    self.data.append('')
                    showsUrl = URL.replace('&page=1', '&page=%s' % str(i+1))
                    showsUrl = 'http://9proxy.in/b.php?u=%s&b=28' % urllib.quote_plus(urllib.unquote_plus(showsUrl))
                    threads.append(Thread(self.thread, showsUrl, i-1))
                [i.start() for i in threads]
                [i.join() for i in threads]
                for i in self.data: result += i
            except:
                pass

            result = result.replace('\n','')
            shows = common.parseDOM(result, "div", attrs = { "class": "lister-item mode-detail" })
        except:
            return

        for show in shows:
            try:
                name = common.parseDOM(show, "h3", attrs = { "class": "lister-item-header" })[0]
                name = common.parseDOM(name, "a")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                year = common.parseDOM(show, "span", attrs = { "class": "lister-item-year.+?" })[0]
                year = re.compile('[(](.+?)[)]').findall(year)[-1]
                if year.isdigit(): raise Exception()
                year = re.compile('(\d{4}).+').findall(year)[0]
                year = year.encode('utf-8')

                if int(year) > int((datetime.datetime.utcnow() - datetime.timedelta(hours = 5)).strftime("%Y")): raise Exception()

                imdb = common.parseDOM(show, "img", ret="data-tconst")[0]
                imdb = re.sub('[^0-9]', '', str(imdb))
                imdb = imdb.encode('utf-8')

                url = link().imdb_title % imdb
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                try:
                    image = common.parseDOM(show, "img", ret="src")[0]
                    image = urllib.unquote_plus(image)
                    image = image[image.find('?') + 1:].split('&')
                    image = [i.split('=', 1)[-1] for i in image if i.startswith('u=')][0]
                    image = 'http' + image.split('http' , 1)[-1]
                    if not ('_SX' in image or '_SY' in image): raise Exception()
                    image = image.rsplit('_SX', 1)[0].rsplit('_SY', 1)[0] + '_SX500.' + image.rsplit('.', 1)[-1]
                except:
                    image = link().imdb_image
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                try:
                    plot = common.parseDOM(show, "p", attrs = { "class": "" })[0]
                    plot = plot.rsplit('<span>', 1)[0].rsplit('<a href', 1)[0].strip()
                    plot = common.replaceHTMLCodes(plot)
                    plot = plot.encode('utf-8')
                except:
                    plot = ''

                self.list.append({'name': name, 'url': url, 'image': image, 'year': year, 'imdb': imdb, 'genre': '', 'plot': plot})
            except:
                pass

        return self.list

    def imdb_list4(self, url):
        try:
            url = url.replace(link().imdb_base, link().imdb_akas)
            result = getUrl(url).result

            try:
                threads = []
                pages = common.parseDOM(result, "div", attrs = { "class": "pagination" })[0]
                pages = re.compile('.+?\d+.+?(\d+)').findall(pages)[0]

                for i in range(1, int(pages)):
                    self.data.append('')
                    showsUrl = url.replace('&start=1', '&start=%s' % str(i*100+1))
                    threads.append(Thread(self.thread, showsUrl, i-1))
                [i.start() for i in threads]
                [i.join() for i in threads]
                for i in self.data: result += i
            except:
                pass

            result = result.replace('\n','')
            shows = common.parseDOM(result, "div", attrs = { "class": "list_item.+?" })
        except:
            return

        for show in shows:
            try:
                name = common.parseDOM(show, "a", attrs = { "onclick": ".+?" })[-1]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                year = common.parseDOM(show, "span", attrs = { "class": "year_type" })[0]
                if not 'series' in year.lower(): raise Exception()
                year = re.compile('[(](\d{4})').findall(year)[0]
                year = year.encode('utf-8')

                if int(year) > int((datetime.datetime.utcnow() - datetime.timedelta(hours = 5)).strftime("%Y")): raise Exception()

                url = common.parseDOM(show, "a", ret="href")[0]
                url = '%s%s' % (link().imdb_base, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                try:
                    image = common.parseDOM(show, "img", ret="src")[0]
                    if not ('._SX' in image or '._SY' in image): raise Exception()
                    image = image.rsplit('._SX', 1)[0].rsplit('._SY', 1)[0] + '._SX500.' + image.rsplit('.', 1)[-1]
                except:
                    image = link().imdb_image
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                imdb = re.sub('[^0-9]', '', url.rsplit('tt', 1)[-1])
                imdb = imdb.encode('utf-8')

                try:
                    plot = common.parseDOM(show, "div", attrs = { "class": "item_description" })[0]
                    plot = plot.rsplit('<span>', 1)[0].strip()
                    plot = common.replaceHTMLCodes(plot)
                    plot = plot.encode('utf-8')
                except:
                    plot = ''

                self.list.append({'name': name, 'url': url, 'image': image, 'year': year, 'imdb': imdb, 'genre': '', 'plot': plot})
            except:
                pass

        return self.list

    def trakt_list(self, url):
        try:
            post = urllib.urlencode({'username': link().trakt_user, 'password': link().trakt_password})

            result = getUrl(url, post=post).result
            result = json.loads(result)

            shows = []
            try: result = result['items']
            except: pass
            for i in result:
                try: shows.append(i['show'])
                except: pass
            if shows == []: 
                shows = result
        except:
            return

        for show in shows:
            try:
                name = show['title']
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                year = show['year']
                year = re.sub('[^0-9]', '', str(year))
                year = year.encode('utf-8')

                if int(year) > int((datetime.datetime.utcnow() - datetime.timedelta(hours = 5)).strftime("%Y")): raise Exception()

                imdb = show['imdb_id']
                imdb = re.sub('[^0-9]', '', str(imdb))
                imdb = imdb.encode('utf-8')

                url = link().imdb_title % imdb
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                try: image = show['images']['poster']
                except: image = show['poster']
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                try:
                    genre = show['genres']
                    genre = " / ".join(genre)
                    genre = common.replaceHTMLCodes(genre)
                    genre = genre.encode('utf-8')
                except:
                    genre = ''

                try:
                    plot = show['overview']
                    plot = common.replaceHTMLCodes(plot)
                    plot = plot.encode('utf-8')
                except:
                    plot = ''

                self.list.append({'name': name, 'url': url, 'image': image, 'year': year, 'imdb': imdb, 'genre': genre, 'plot': plot})
            except:
                pass

        return self.list

    def thread(self, url, i):
        try:
            result = getUrl(url, referer=url).result
            self.data[i] = result
        except:
            return

class seasons:
    def __init__(self):
        self.list = []

    def get(self, url, image, year, imdb, genre, plot, show, idx=True):
        if idx == True:
            #self.list = self.get_list(url, image, year, imdb, genre, plot, show)
            self.list = cache2(self.get_list, url, image, year, imdb, genre, plot, show)
            index().seasonList(self.list)
        else:
            self.list = self.get_list(url, image, year, imdb, genre, plot, show)
            return self.list

    def get_list(self, url, image, year, imdb, genre, plot, show):

        if imdb == '0': imdb = re.sub('[^0-9]', '', url.rsplit('tt', 1)[-1])

        try:
            try:
                result = getUrl(link().tvdb_series % imdb).result
                show_alt = common.parseDOM(result, "SeriesName")[0]
                tvdb = common.parseDOM(result, "seriesid")[0]
            except:
                result = getUrl(link().tvdb_series2 % urllib.quote_plus(show)).result
                result = common.parseDOM(result, "Series")
                result = [i for i in result if show == common.parseDOM(i, "SeriesName")[0] and year in common.parseDOM(i, "FirstAired")[0]][0]
                show_alt = common.parseDOM(result, "SeriesName")[0]
                tvdb = common.parseDOM(result, "seriesid")[0]

            show_alt = common.replaceHTMLCodes(show_alt)
            show_alt = show_alt.encode('utf-8')
            tvdb = common.replaceHTMLCodes(tvdb)
            tvdb = tvdb.encode('utf-8')
        except:
            pass

        try:
            self.list = []
            seasonList = self.tvrage_list(url, image, year, imdb, tvdb, genre, plot, show, show_alt)
            if not (seasonList == None or seasonList == []): return seasonList
        except:
            pass

        try:
            self.list = []
            seasonList = self.tvdb_list(url, image, year, imdb, tvdb, genre, plot, show, show_alt)
            if not (seasonList == None or seasonList == []): return seasonList
        except:
            pass

        try:
            self.list = []
            seasonList = self.imdb_list(url, image, year, imdb, '0', genre, plot, show, show)
            if not (seasonList == None or seasonList == []): return seasonList
        except:
            pass

    def tvrage_list(self, url, image, year, imdb, tvdb, genre, plot, show, show_alt):
        try:
            traktUrl = link().trakt_summary % (link().trakt_key, tvdb)
            result = getUrl(traktUrl).result
            result = json.loads(result)
            tvrage = result['tvrage_id']

            tvrageUrl = link().tvrage_info % tvrage
            result = getUrl(tvrageUrl).result

            seasons = common.parseDOM(result, "Season", ret="no")
            seasons = [i for i in seasons if not i == '0']
        except:
            return

        for season in seasons:
            try:
                date = common.parseDOM(result, "Season", attrs = { "no": season })[0]
                date = common.parseDOM(date, "airdate")
                date = [i for i in date if not '-00' in i][0]
                date = date.encode('utf-8')
                if date == '' or '-00' in date: raise Exception()
                if int(re.sub('[^0-9]', '', str(date)) + '0000') + 10500 > int((datetime.datetime.utcnow() - datetime.timedelta(hours = 5)).strftime("%Y%m%d%H%M")): raise Exception()

                num = '%01d' % int(season)
                num = num.encode('utf-8')

                name = '%s %s' % ('Season', num)
                name = name.encode('utf-8')

                self.list.append({'name': name, 'url': tvrageUrl, 'image': image, 'year': year, 'imdb': imdb, 'tvdb': tvdb, 'genre': genre, 'plot': plot, 'show': show, 'show_alt': show_alt, 'season': num, 'sort': '%10d' % int(num), 'idx_data': result})
            except:
                pass

        self.list = sorted(self.list, key=itemgetter('sort'))
        return self.list

    def tvdb_list(self, url, image, year, imdb, tvdb, genre, plot, show, show_alt):
        try:
            tvdbUrl = link().tvdb_episodes % (link().tvdb_key, tvdb)
            result = getUrl(tvdbUrl).result

            seasons = common.parseDOM(result, "Episode")
            seasons = [i for i in seasons if common.parseDOM(i, "EpisodeNumber")[0] == '1']
            seasons = [i for i in seasons if not common.parseDOM(i, "SeasonNumber")[0] == '0']
        except:
            return

        for season in seasons:
            try:
                date = common.parseDOM(season, "FirstAired")[0]
                date = common.replaceHTMLCodes(date)
                date = date.encode('utf-8')
                if date == '' or '-00' in date: raise Exception()
                if int(re.sub('[^0-9]', '', str(date)) + '0000') + 10500 > int((datetime.datetime.utcnow() - datetime.timedelta(hours = 5)).strftime("%Y%m%d%H%M")): raise Exception()

                num = common.parseDOM(season, "SeasonNumber")[0]
                num = '%01d' % int(num)
                num = num.encode('utf-8')

                name = '%s %s' % ('Season', num)
                name = name.encode('utf-8')

                self.list.append({'name': name, 'url': link().tvdb_base, 'image': image, 'year': year, 'imdb': imdb, 'tvdb': tvdb, 'genre': genre, 'plot': plot, 'show': show, 'show_alt': show_alt, 'season': num, 'sort': '%10d' % int(num), 'idx_data': result})
            except:
                pass

        self.list = sorted(self.list, key=itemgetter('sort'))
        return self.list

    def imdb_list(self, url, image, year, imdb, tvdb, genre, plot, show, show_alt):
        try:
            imdbUrl = link().imdb_seasons % imdb
            result = getUrl(imdbUrl).result
            result = result.decode('iso-8859-1').encode('utf-8')

            seasons = common.parseDOM(result, "select", attrs = { "id": "bySeason" })[0]
            seasons = common.parseDOM(seasons, "option", ret="value")
            seasons = [i for i in seasons if not i == '0']
            seasons = [i for i in seasons if i.isdigit()]
        except:
            return

        for season in seasons:
            try:
                num = '%01d' % int(season)
                num = num.encode('utf-8')

                name = '%s %s' % ('Season', num)
                name = name.encode('utf-8')

                url = link().imdb_episodes % (imdb, season)
                url = url.encode('utf-8')

                if season == seasons[-1]:
                    result = getUrl(url).result
                    dateDict = {'Jan.':'01', 'Feb.':'02', 'Mar.':'03', 'Apr.':'04', 'May':'05', 'Jun.':'06', 'Jul.':'07', 'Aug.':'08', 'Sep.':'09', 'Oct.':'10', 'Nov.':'11', 'Dec.':'12'}
                    date = common.parseDOM(result, "div", attrs = { "class": "airdate" })[0]
                    for i in dateDict: date = date.replace(i, dateDict[i])
                    date = re.findall('(\d+) (\d+) (\d+)', date, re.I)[0]
                    date = '%04d-%02d-%02d' % (int(date[2]), int(date[1]), int(date[0]))
                    if int(re.sub('[^0-9]', '', str(date)) + '0000') + 10500 > int((datetime.datetime.utcnow() - datetime.timedelta(hours = 5)).strftime("%Y%m%d%H%M")): raise Exception()

                self.list.append({'name': name, 'url': url, 'image': image, 'year': year, 'imdb': imdb, 'tvdb': tvdb, 'genre': genre, 'plot': plot, 'show': show, 'show_alt': show_alt, 'season': num, 'sort': '%10d' % int(num), 'idx_data': ''})
            except:
                pass

        self.list = sorted(self.list, key=itemgetter('sort'))
        return self.list

class episodes:
    def __init__(self):
        self.list = []

    def get(self, name, url, image, year, imdb, tvdb, genre, plot, show, show_alt, idx_data='', idx=True):
        if idx == True:
            #self.list = self.get_list(name, url, image, year, imdb, tvdb, genre, plot, show, show_alt, idx_data)
            self.list = cache(self.get_list, name, url, image, year, imdb, tvdb, genre, plot, show, show_alt, idx_data)
            index().episodeList(self.list)
        else:
            self.list = self.get_list(name, url, image, year, imdb, tvdb, genre, plot, show, show_alt, idx_data)
            return self.list

    def calendar(self, url):
        #self.list = self.trakt_list(url)
        self.list = cache2(self.trakt_list, url)
        index().episodeList(self.list)


    def get_list(self, name, url, image, year, imdb, tvdb, genre, plot, show, show_alt, idx_data):
        if url.startswith(link().tvrage_base):
            episodeList = self.tvrage_list(name, url, image, year, imdb, tvdb, genre, plot, show, show_alt, idx_data)
        elif url == link().tvdb_base:
            episodeList = self.tvdb_list(name, url, image, year, imdb, tvdb, genre, plot, show, show_alt, idx_data)
        else:
            episodeList = self.imdb_list(name, url, image, year, imdb, tvdb, genre, plot, show, show_alt, idx_data)
        return episodeList

    def tvrage_list(self, name, url, image, year, imdb, tvdb, genre, plot, show, show_alt, idx_data):
        try:
            season = re.sub('[^0-9]', '', name)
            season = season.encode('utf-8')

            if not idx_data == '': result = idx_data
            else: result = getUrl(url).result

            episodes = common.parseDOM(result, "Season", attrs = { "no": season })[0]
            episodes = common.parseDOM(episodes, "episode")
            episodes = [i for i in episodes if not common.parseDOM(i, "seasonnum")[0] == '00']
            episodes = [i for i in episodes if not common.parseDOM(i, "seasonnum")[0] == '0']
        except:
            return

        for episode in episodes:
            try:
                date = common.parseDOM(episode, "airdate")[0]
                date = common.replaceHTMLCodes(date)
                date = date.encode('utf-8')
                if date == '' or '-00' in date: raise Exception()
                if int(re.sub('[^0-9]', '', str(date)) + '0000') + 10500 > int((datetime.datetime.utcnow() - datetime.timedelta(hours = 5)).strftime("%Y%m%d%H%M")): raise Exception()

                title = common.parseDOM(episode, "title")[0]
                title = common.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                num = common.parseDOM(episode, "seasonnum")[0]
                num = re.sub('[^0-9]', '', '%01d' % int(num))
                num = num.encode('utf-8')

                name = show_alt + ' S' + '%02d' % int(season) + 'E' + '%02d' % int(num)
                try: name = name.encode('utf-8')
                except: pass

                try: thumb = common.parseDOM(episode, "screencap")[0]
                except: thumb = image
                thumb = common.replaceHTMLCodes(thumb)
                thumb = thumb.encode('utf-8')

                self.list.append({'name': name, 'url': name, 'image': thumb, 'date': date, 'year': year, 'imdb': imdb, 'tvdb': tvdb, 'genre': genre, 'plot': plot, 'title': title, 'show': show, 'show_alt': show_alt, 'season': season, 'episode': num, 'sort': '%10d' % int(num)})
            except:
                pass

        self.list = sorted(self.list, key=itemgetter('sort'))
        return self.list

    def tvdb_list(self, name, url, image, year, imdb, tvdb, genre, plot, show, show_alt, idx_data):
        try:
            season = re.sub('[^0-9]', '', name)
            season = season.encode('utf-8')

            tvdbUrl = link().tvdb_episodes % (link().tvdb_key, tvdb)
            if not idx_data == '': result = idx_data
            else: result = getUrl(tvdbUrl).result

            episodes = common.parseDOM(result, "Episode")
            episodes = [i for i in episodes if '%01d' % int(common.parseDOM(i, "SeasonNumber")[0]) == season]
            episodes = [i for i in episodes if not common.parseDOM(i, "EpisodeNumber")[0] == '0']
        except:
            return

        for episode in episodes:
            try:
                date = common.parseDOM(episode, "FirstAired")[0]
                date = common.replaceHTMLCodes(date)
                date = date.encode('utf-8')
                if date == '' or '-00' in date: raise Exception()
                if int(re.sub('[^0-9]', '', str(date)) + '0000') + 10500 > int((datetime.datetime.utcnow() - datetime.timedelta(hours = 5)).strftime("%Y%m%d%H%M")): raise Exception()

                title = common.parseDOM(episode, "EpisodeName")[0]
                title = common.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                num = common.parseDOM(episode, "EpisodeNumber")[0]
                num = re.sub('[^0-9]', '', '%01d' % int(num))
                num = num.encode('utf-8')

                name = show_alt + ' S' + '%02d' % int(season) + 'E' + '%02d' % int(num)
                try: name = name.encode('utf-8')
                except: pass

                thumb = common.parseDOM(episode, "filename")[0]
                if not thumb == '': thumb = link().tvdb_thumb + thumb
                else: thumb = image
                thumb = common.replaceHTMLCodes(thumb)
                thumb = thumb.encode('utf-8')

                try: desc = common.parseDOM(episode, "Overview")[0]
                except: desc = plot
                desc = common.replaceHTMLCodes(desc)
                desc = desc.encode('utf-8')

                self.list.append({'name': name, 'url': name, 'image': thumb, 'date': date, 'year': year, 'imdb': imdb, 'tvdb': tvdb, 'genre': genre, 'plot': desc, 'title': title, 'show': show, 'show_alt': show_alt, 'season': season, 'episode': num, 'sort': '%10d' % int(num)})
            except:
                pass

        self.list = sorted(self.list, key=itemgetter('sort'))
        return self.list

    def imdb_list(self, name, url, image, year, imdb, tvdb, genre, plot, show, show_alt, idx_data):
        try:
            season = re.sub('[^0-9]', '', name)
            season = season.encode('utf-8')

            result = getUrl(url.replace(link().imdb_base, link().imdb_akas)).result
            result = result.decode('iso-8859-1').encode('utf-8')

            episodes = common.parseDOM(result, "div", attrs = { "class": "list_item.+?" })
            episodes = [i for i in episodes if not common.parseDOM(i, "meta", ret="content", attrs = { "itemprop": "episodeNumber" })[0] == '0']
        except:
            return

        for episode in episodes:
            try:
                dateDict = {'Jan.':'01', 'Feb.':'02', 'Mar.':'03', 'Apr.':'04', 'May':'05', 'Jun.':'06', 'Jul.':'07', 'Aug.':'08', 'Sep.':'09', 'Oct.':'10', 'Nov.':'11', 'Dec.':'12'}
                date = common.parseDOM(episode, "div", attrs = { "class": "airdate" })[0]
                for i in dateDict: date = date.replace(i, dateDict[i])
                date = re.findall('(\d+) (\d+) (\d+)', date, re.I)[0]
                date = '%04d-%02d-%02d' % (int(date[2]), int(date[1]), int(date[0]))
                if int(re.sub('[^0-9]', '', str(date)) + '0000') + 10500 > int((datetime.datetime.utcnow() - datetime.timedelta(hours = 5)).strftime("%Y%m%d%H%M")): raise Exception()

                title = common.parseDOM(episode, "a", ret="title")[0]
                title = common.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                num = common.parseDOM(episode, "meta", ret="content", attrs = { "itemprop": "episodeNumber" })[0]
                num = re.sub('[^0-9]', '', '%01d' % int(num))
                num = num.encode('utf-8')

                name = show_alt + ' S' + '%02d' % int(season) + 'E' + '%02d' % int(num)
                try: name = name.encode('utf-8')
                except: pass

                try:
                    thumb = common.parseDOM(episode, "img", ret="src")[0]
                    if not ('_SX' in thumb or '_SY' in thumb): raise Exception()
                    thumb = re.sub('_CR.+?_', '_', re.sub('_SY.+?_', '_', re.sub('_SX.+?_', '_', thumb))) 
                except:
                    thumb = image
                thumb = common.replaceHTMLCodes(thumb)
                thumb = thumb.encode('utf-8')

                try:
                    desc = common.parseDOM(episode, "div", attrs = { "itemprop": "description" })[0]
                    if 'update=tt' in desc: raise Exception()
                except:
                    desc = plot
                desc = common.replaceHTMLCodes(desc)
                desc = desc.encode('utf-8')

                self.list.append({'name': name, 'url': name, 'image': thumb, 'date': date, 'year': year, 'imdb': imdb, 'tvdb': tvdb, 'genre': genre, 'plot': desc, 'title': title, 'show': show, 'show_alt': show_alt, 'season': season, 'episode': num, 'sort': '%10d' % int(num)})
            except:
                pass

        self.list = sorted(self.list, key=itemgetter('sort'))
        return self.list

    def trakt_list(self, date):
        try:
            traktUrl = link().trakt_calendar % (link().trakt_key, re.sub('[^0-9]', '', str(date)))
            result = getUrl(traktUrl).result
            result = json.loads(result)[0]
            episodes = result['episodes']
        except:
            return

        for episode in episodes:
            try:
                title = episode['episode']['title']
                title = common.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                season = episode['episode']['season']
                season = re.sub('[^0-9]', '', '%01d' % int(season))
                season = season.encode('utf-8')

                num = episode['episode']['number']
                num = re.sub('[^0-9]', '', '%01d' % int(num))
                num = num.encode('utf-8')

                show = episode['show']['title']
                show = common.replaceHTMLCodes(show)
                show = show.encode('utf-8')

                name = show + ' S' + '%02d' % int(season) + 'E' + '%02d' % int(num)
                try: name = name.encode('utf-8')
                except: pass

                year = episode['show']['year']
                year = re.sub('[^0-9]', '', str(year))
                year = year.encode('utf-8')

                imdb = episode['show']['imdb_id']
                imdb = re.sub('[^0-9]', '', str(imdb))
                if imdb == '': raise Exception()
                imdb = imdb.encode('utf-8')

                tvdb = episode['show']['tvdb_id']
                tvdb = re.sub('[^0-9]', '', str(tvdb))
                if tvdb == '': tvdb = '0'
                tvdb = tvdb.encode('utf-8')

                thumb = episode['episode']['images']['screen']
                if thumb == '': thumb = episode['show']['images']['poster']
                thumb = common.replaceHTMLCodes(thumb)
                thumb = thumb.encode('utf-8')

                try:
                    genre = episode['show']['genres']
                    genre = " / ".join(genre)
                    genre = common.replaceHTMLCodes(genre)
                    genre = genre.encode('utf-8')
                except:
                    genre = ''

                try:
                    desc = episode['episode']['overview']
                    if desc == '': desc = episode['show']['overview']
                    desc = common.replaceHTMLCodes(desc)
                    desc = desc.encode('utf-8')
                except:
                    desc = ''

                self.list.append({'name': name, 'url': name, 'image': thumb, 'date': date, 'year': year, 'imdb': imdb, 'tvdb': tvdb, 'genre': genre, 'plot': desc, 'title': title, 'show': show, 'show_alt': show, 'season': season, 'episode': num})
            except:
                pass

        self.list = sorted(self.list, key=itemgetter('name'))
        return self.list


class resolver:
    def __init__(self):
        self.sources_dict()
        self.sources = []

    def get_host(self, name, url, image, date, year, imdb, tvdb, genre, plot, title, show, show_alt, season, episode):
        try:
            self.sources = self.sources_get(name, title, imdb, tvdb, year, season, episode, show, show_alt, self.hostDict)
            self.sources = self.sources_filter()
            if self.sources == []: raise Exception()

            for i in range(0,len(self.sources)):
                self.sources[i].update({'name': name, 'image': image, 'date': date, 'year': year, 'imdb': imdb, 'tvdb': tvdb, 'genre': genre, 'plot': plot, 'title': title, 'show': show, 'show_alt': show_alt, 'season': season, 'episode': episode})

            index().sourceList(self.sources)
        except:
            return

    def play_host(self, name, url, imdb, source, provider):
        try:
            url = self.sources_resolve(url, provider)
            if url is None: raise Exception()

            if getSetting("playback_info") == 'true':
                index().infoDialog(source, header=name)

            player().run(name, url, imdb)
            return url
        except:
            index().infoDialog(language(30318).encode("utf-8"))
            return

    def run(self, name, title, imdb, tvdb, year, season, episode, show, show_alt, url):
        try:
            self.sources = self.sources_get(name, title, imdb, tvdb, year, season, episode, show, show_alt, self.hostDict)
            self.sources = self.sources_filter()
            if self.sources == []: raise Exception()

            autoplay = getSetting("autoplay")
            if index().getProperty('PseudoTVRunning') == 'True':
                autoplay = 'true'
            elif not xbmc.getInfoLabel('Container.FolderPath').startswith(sys.argv[0]):
                autoplay = getSetting("autoplay_library")

            if url == 'play://':
                url = self.sources_direct()
            elif not autoplay == 'true':
                url = self.sources_dialog()
            else:
                url = self.sources_direct()


            if url is None: raise Exception()
            if url == 'close://': return

            if getSetting("playback_info") == 'true':
                index().infoDialog(self.selectedSource, header=name)

            player().run(name, url, imdb)
            return url
        except:
            if not index().getProperty('PseudoTVRunning') == 'True':
                index().infoDialog(language(30318).encode("utf-8"))
            return

    def sources_get(self, name, title, imdb, tvdb, year, season, episode, show, show_alt, hostDict):
        threads = []

        global icefilms_sources
        icefilms_sources = []
        if getSetting("icefilms") == 'true':
            threads.append(Thread(icefilms().get, name, title, imdb, tvdb, year, season, episode, show, show_alt, hostDict))

        global primewire_sources
        primewire_sources = []
        if getSetting("primewire") == 'true':
            threads.append(Thread(primewire().get, name, title, imdb, tvdb, year, season, episode, show, show_alt, hostDict))

        global watchseries_sources
        watchseries_sources = []
        threads.append(Thread(watchseries().get, name, title, imdb, tvdb, year, season, episode, show, show_alt, hostDict))

        global flixanity_sources
        flixanity_sources = []
        if getSetting("flixanity") == 'true':
            threads.append(Thread(flixanity().get, name, title, imdb, tvdb, year, season, episode, show, show_alt, hostDict))

        global shush_sources
        shush_sources = []
        if getSetting("shush") == 'true':
            threads.append(Thread(shush().get, name, title, imdb, tvdb, year, season, episode, show, show_alt, hostDict))

        global ororotv_sources
        ororotv_sources = []
        if getSetting("ororotv") == 'true':
            threads.append(Thread(ororotv().get, name, title, imdb, tvdb, year, season, episode, show, show_alt, hostDict))

        global putlockertv_sources
        putlockertv_sources = []
        if getSetting("putlockertv") == 'true':
            threads.append(Thread(putlockertv().get, name, title, imdb, tvdb, year, season, episode, show, show_alt, hostDict))

        global clickplay_sources
        clickplay_sources = []
        if getSetting("clickplay") == 'true':
            threads.append(Thread(clickplay().get, name, title, imdb, tvdb, year, season, episode, show, show_alt, hostDict))

        global vkbox_sources
        vkbox_sources = []
        if getSetting("vkbox") == 'true':
            threads.append(Thread(vkbox().get, name, title, imdb, tvdb, year, season, episode, show, show_alt, hostDict))

        global istreamhd_sources
        istreamhd_sources = []
        if getSetting("istreamhd") == 'true':
            threads.append(Thread(istreamhd().get, name, title, imdb, tvdb, year, season, episode, show, show_alt, hostDict))

        global simplymovies_sources
        simplymovies_sources = []
        if getSetting("simplymovies") == 'true':
            threads.append(Thread(simplymovies().get, name, title, imdb, tvdb, year, season, episode, show, show_alt, hostDict))

        global moviestorm_sources
        moviestorm_sources = []
        if getSetting("moviestorm") == 'true':
            threads.append(Thread(moviestorm().get, name, title, imdb, tvdb, year, season, episode, show, show_alt, hostDict))

        global noobroom_sources
        noobroom_sources = []
        if getSetting("noobroom") == 'true':
            threads.append(Thread(noobroom().get, name, title, imdb, tvdb, year, season, episode, show, show_alt, hostDict))

        [i.start() for i in threads]
        [i.join() for i in threads]

        self.sources = icefilms_sources + primewire_sources + watchseries_sources + flixanity_sources + shush_sources + ororotv_sources + putlockertv_sources + vkbox_sources + clickplay_sources + istreamhd_sources + simplymovies_sources + moviestorm_sources + noobroom_sources

        return self.sources

    def sources_resolve(self, url, provider):
        try:
            if provider == 'Icefilms': url = icefilms().resolve(url)
            elif provider == 'Primewire': url = primewire().resolve(url)
            elif provider == 'Watchseries': url = watchseries().resolve(url)
            elif provider == 'Flixanity': url = flixanity().resolve(url)
            elif provider == 'Shush': url = shush().resolve(url)
            elif provider == 'OroroTV': url = ororotv().resolve(url)
            elif provider == 'PutlockerTV': url = putlockertv().resolve(url)
            elif provider == 'Clickplay': url = clickplay().resolve(url)
            elif provider == 'VKBox': url = vkbox().resolve(url)
            elif provider == 'iStreamHD': url = istreamhd().resolve(url)
            elif provider == 'Simplymovies': url = simplymovies().resolve(url)
            elif provider == 'Moviestorm': url = moviestorm().resolve(url)
            elif provider == 'Noobroom': url = noobroom().resolve(url)
            return url
        except:
            return

    def sources_filter(self):
        #hd_rank = ['VK', 'Shush', 'Firedrive', 'Movreel', 'Billionuploads', '180upload', 'Hugefiles', 'Noobroom']
        #sd_rank = ['OroroTV', 'VK', 'Firedrive', 'Putlocker', 'Sockshare', 'Mailru', 'iShared', 'Movreel', 'Played', 'Promptfile', 'Mightyupload', 'Gorillavid', 'Divxstage', 'Flashx', 'Noobroom']
        hd_rank = [getSetting("hosthd1"), getSetting("hosthd2"), getSetting("hosthd3"), getSetting("hosthd4"), getSetting("hosthd5"), getSetting("hosthd6"), getSetting("hosthd7"), getSetting("hosthd8")]
        sd_rank = [getSetting("host1"), getSetting("host2"), getSetting("host3"), getSetting("host4"), getSetting("host5"), getSetting("host6"), getSetting("host7"), getSetting("host8"), getSetting("host9"), getSetting("host10"), getSetting("host11"), getSetting("host12"), getSetting("host13"), getSetting("host14"), getSetting("host15")]

        for i in range(len(self.sources)): self.sources[i]['source'] = self.sources[i]['source'].lower()
        self.sources = sorted(self.sources, key=itemgetter('source'))

        filter = []
        for host in hd_rank: filter += [i for i in self.sources if i['quality'] == 'HD' and i['source'].lower() == host.lower()]
        for host in sd_rank: filter += [i for i in self.sources if not i['quality'] == 'HD' and i['source'].lower() == host.lower()]
        filter += [i for i in self.sources if not i['quality'] == 'HD' and not any(x == i['source'].lower() for x in [r.lower() for r in sd_rank])]
        self.sources = filter

        filter = []
        filter += [i for i in self.sources if i['quality'] == 'HD']
        filter += [i for i in self.sources if i['quality'] == 'SD']
        self.sources = filter

        if not getSetting("quality") == 'true':
            self.sources = [i for i in self.sources if not i['quality'] == 'HD']

        count = 1
        for i in range(len(self.sources)):
            self.sources[i]['source'] = ''+ str('%02d' % count) + ' | [B]' + self.sources[i]['provider'].upper() + '[/B] | ' + self.sources[i]['source'].upper() + ' | ' + self.sources[i]['quality']
            count = count + 1

        return self.sources

    def sources_dialog(self):
        try:
            sourceList, urlList, providerList = [], [], []

            for i in self.sources:
                sourceList.append(i['source'])
                urlList.append(i['url'])
                providerList.append(i['provider'])

            select = index().selectDialog(sourceList)
            if select == -1: return 'close://'

            url = self.sources_resolve(urlList[select], providerList[select])
            self.selectedSource = self.sources[select]['source']
            return url
        except:
            return

    def sources_direct(self):
        u = None

        for i in self.sources:
            try:
                if i['provider'] == 'Icefilms' and i['quality'] == 'HD': raise Exception()
                url = self.sources_resolve(i['url'], i['provider'])
                xbmc.sleep(1000)
                if url is None: raise Exception()
                if u is None: u == url

                if url.startswith('http://'):
                    request = urllib2.Request(url.rsplit('|', 1)[0])
                    request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36')
                    request.add_header('Cookie', 'video=true')
                    response = urllib2.urlopen(request, timeout=20)
                    chunk = response.read(16 * 1024)
                    response.close()
                    if 'text/html' in str(response.info()["Content-Type"]): raise Exception()

                self.selectedSource = i['source']
                return url
            except:
                pass

        return u

    def sources_dict(self):
        self.hostDict = [
        '2gb-hosting',
        'allmyvideos',
        #'180upload',
        'bayfiles',
        'bestreams',
        #'billionuploads',
        'castamp',
        #'clicktoview',
        'daclips',
        'divxstage',
        'donevideo',
        'ecostream',
        'filenuke',
        'firedrive',
        'flashx',
        'gorillavid',
        'hostingbulk',
        #'hugefiles',
        'ishared',
        'jumbofiles',
        'lemuploads',
        'limevideo',
        #'megarelease',
        'mightyupload',
        'movdivx',
        'movpod',
        'movreel',
        'movshare',
        'movzap',
        'muchshare',
        'nosvideo',
        'novamov',
        'nowvideo',
        'played',
        'playwire',
        'primeshare',
        'promptfile',
        'purevid',
        'putlocker',
        'sharerepo',
        'sharesix',
        'sockshare',
        'stagevu',
        'streamcloud',
        'thefile',
        'uploadc',
        'vidbull',
        'videobb',
        'videoweed',
        'videozed',
        #'vidhog',
        #'vidplay',
        'vidx',
        #'vidxden',
        #'watchfreeinhd',
        'xvidstage',
        'youtube',
        'yourupload',
        'youwatch',
        'zalaa'
        ]


class icefilms:
    def __init__(self):
        self.base_link = 'http://www.icefilms.info'
        self.search_link = 'http://www.icefilms.info/tv/a-z/%s'
        self.video_link = 'http://www.icefilms.info/membersonly/components/com_iceplayer/video.php?vid=%s'
        self.post_link = 'http://www.icefilms.info/membersonly/components/com_iceplayer/video.phpAjaxResp.php'

    def get(self, name, title, imdb, tvdb, year, season, episode, show, show_alt, hostDict):
        try:
            global icefilms_sources
            icefilms_sources = []

            query = show.upper()
            if query.startswith('THE '): query = query.replace('THE ', '')
            elif query.startswith('A '): query = query.replace('A ', '')
            if not query[0].isalpha(): query = '1'
            query = self.search_link % query[0]

            result = getUrl(query).result
            result = result.decode('iso-8859-1').encode('utf-8')
            url = re.compile('id=%s>.+?href=(.+?)>' % imdb).findall(result)[0]
            url = '%s%s' % (self.base_link, url)
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result
            result = result.decode('iso-8859-1').encode('utf-8')
            id = re.compile('href=/ip.php[?]v=(.+?)&>%01dx%02d' % (int(season), int(episode))).findall(result)[0]
            id = id.split('v=')[-1]
            url = self.video_link % id
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result
            result = result.decode('iso-8859-1').encode('utf-8')
            sec = re.compile('lastChild[.]value="(.+?)"').findall(result)[0]
            links = common.parseDOM(result, "div", attrs = { "class": "ripdiv" })

            import random

            try:
                hd_links = ''
                hd_links = [i for i in links if '>HD 720p<' in i][0]
                hd_links = re.compile("onclick='go[(](.+?)[)]'>Source(.+?)</a>").findall(hd_links)
            except:
                pass

            for url, host in hd_links:
                try:
                    hosts = ['movreel', 'billionuploads', '180upload', 'hugefiles']
                    host = re.sub('<span\s.+?>|</span>|#\d*:','', host)
                    host = host.strip().lower()
                    if not host in hosts: raise Exception()
                    url = 'id=%s&t=%s&sec=%s&s=%s&m=%s&cap=&iqs=&url=' % (url, id, sec, random.randrange(5, 50), random.randrange(100, 300) * -1)
                    icefilms_sources.append({'source': host, 'quality': 'HD', 'provider': 'Icefilms', 'url': url})
                except:
                    pass

            try:
                sd_links = ''
                sd_links = [i for i in links if '>DVDRip / Standard Def<' in i][0]
                sd_links = re.compile("onclick='go[(](.+?)[)]'>Source(.+?)</a>").findall(sd_links)
            except:
                pass

            for url, host in sd_links:
                try:
                    hosts = ['movreel']
                    host = re.sub('<span\s.+?>|</span>|#\d*:','', host)
                    host = host.strip().lower()
                    if not host in hosts: raise Exception()
                    url = 'id=%s&t=%s&sec=%s&s=%s&m=%s&cap=&iqs=&url=' % (url, id, sec, random.randrange(5, 50), random.randrange(100, 300) * -1)
                    icefilms_sources.append({'source': host, 'quality': 'SD', 'provider': 'Icefilms', 'url': url})
                except:
                    pass
        except:
            return

    def resolve(self, url):
        try:
            result = getUrl(self.post_link, post=url).result
            url = result.split("?url=", 1)[-1]
            url = urllib.unquote_plus(url)

            import commonresolvers
            url = commonresolvers.resolvers().get(url)
            return url
        except:
            return

class primewire:
    def __init__(self):
        self.base_link = 'http://www.primewire.ag'
        self.key_link = 'http://www.primewire.ag/index.php?search'
        self.search_link = 'http://www.primewire.ag/index.php?search_keywords=%s&key=%s&search_section=2'
        self.proxy_base_link = 'http://9proxy.in'
        self.proxy_link = 'http://9proxy.in/b.php?u=%s&b=28'

    def get(self, name, title, imdb, tvdb, year, season, episode, show, show_alt, hostDict):
        try:
            global primewire_sources
            primewire_sources = []

            try:
                result = getUrl(self.key_link).result
                key = common.parseDOM(result, "input", ret="value", attrs = { "name": "key" })[0]
                query = self.search_link % (urllib.quote_plus(re.sub('\'', '', show)), key)
            except:
                result = getUrl(self.proxy_link % urllib.quote_plus(urllib.unquote_plus(self.key_link)), referer=self.proxy_base_link).result
                key = common.parseDOM(result, "input", ret="value", attrs = { "name": "key" })[0]
                query = self.search_link % (urllib.quote_plus(re.sub('\'', '', show)), key)
                query = self.proxy_link % urllib.quote_plus(urllib.unquote_plus(query))
                self.base_link = self.proxy_base_link

            result = getUrl(query, referer=self.base_link, close=False).result
            result = result.decode('iso-8859-1').encode('utf-8')
            result = common.parseDOM(result, "div", attrs = { "class": "index_item.+?" })
            result = [i for i in result if any(x in re.compile('title="Watch (.+?)"').findall(i)[0] for x in ['(%s)' % str(year), '(%s)' % str(int(year)+1), '(%s)' % str(int(year)-1)])]
            result = uniqueList(result).list

            match = [common.parseDOM(i, "a", ret="href")[0] for i in result]
            if match == []: return
            for i in match[:5]:
                try:
                    if not i.startswith('http://'): i = '%s%s' % (self.base_link, i)
                    result = getUrl(i, referer=i).result
                    if any(x in self.cleantitle(result) for x in [str('>' + self.cleantitle(show) + '(%s)' % str(year) + '<'), str('>' + self.cleantitle(show_alt) + '(%s)' % str(year) + '<')]):
                        match2 = i
                    if any(x in self.cleantitle(result) for x in [str('>' + self.cleantitle(show) + '<'), str('>' + self.cleantitle(show_alt) + '<')]):
                        match2 = i
                    if str('tt' + imdb) in result:
                        match2 = i
                        break
                except:
                    pass

            x = match2.split('primewire.ag', 1)[-1].split('&', 1)[0]
            y = x.replace('/watch-','/tv-').replace('%2Fwatch-','%2Ftv-')
            z = '/season-%01d-episode-%01d' % (int(season), int(episode))
            if y.startswith('%2F'): y += urllib.quote_plus(z)
            else: y += z
            url = match2.replace(x,y)

            result = getUrl(url, referer=url).result
            result = result.decode('iso-8859-1').encode('utf-8')
            links = common.parseDOM(result, "tbody")

            for i in links:
                try:
                    url = common.parseDOM(i, "a", ret="href")[0]
                    url = urllib.unquote_plus(url)
                    url = re.compile('url=(.+?)&').findall(url)[0]
                    url = base64.urlsafe_b64decode(url.encode('utf-8'))
                    if 'primewire.ag' in url: raise Exception()
                    url = common.replaceHTMLCodes(url)
                    url = url.encode('utf-8')

                    host = common.parseDOM(i, "a", ret="href")[0]
                    host = urllib.unquote_plus(host)
                    host = re.compile('domain=(.+?)&').findall(host)[0]
                    host = base64.urlsafe_b64decode(host.encode('utf-8'))
                    host = host.rsplit('.', 1)[0]
                    host = [x for x in hostDict if host.lower() == x.lower()][0]
                    host = host.encode('utf-8')

                    quality = common.parseDOM(i, "span", ret="class")[0]
                    if quality == 'quality_dvd': quality = 'SD'
                    else:  raise Exception()
                    quality = quality.encode('utf-8')

                    primewire_sources.append({'source': host, 'quality': quality, 'provider': 'Primewire', 'url': url})
                except:
                    pass
        except:
            return

    def cleantitle(self, title):
        title = re.sub('\n|\s(|[(])(UK|US|AU)(|[)])$|\s(vs|v[.])\s|(:|;|-|"|,|\'|\.|\?)|\s', '', title).lower()
        return title

    def resolve(self, url):
        try:
            import commonresolvers
            url = commonresolvers.resolvers().get(url)
            return url
        except:
            return

class watchseries:
    def __init__(self):
        self.base_link = 'http://watchseries.ag'
        self.search_link = 'http://watchseries.ag/search/%s'
        self.episode_link = 'http://watchseries.ag/episode/%s_s%s_e%s.html'

    def get(self, name, title, imdb, tvdb, year, season, episode, show, show_alt, hostDict):
        try:
            global watchseries_sources
            watchseries_sources = []

            query = self.search_link % urllib.quote_plus(show)

            result = getUrl(query, referer=query).result
            result = result.decode('iso-8859-1').encode('utf-8')
            result = result.replace(' (%s)' % str(int(year) - 1), ' (%s)' % year)
            result = re.compile('href="(/serie/.+?)".+?[(]%s[)]' % year).findall(result)
            result = uniqueList(result).list

            match = [self.base_link + i for i in result]
            if match == []: return
            for i in match[:5]:
                try:
                    result = getUrl(i, referer=i).result
                    if any(x in self.cleantitle(result) for x in [str('>' + self.cleantitle(show) + '<'), str('>' + self.cleantitle(show_alt) + '<')]):
                        match2 = i
                    if str('tt' + imdb) in result:
                        match2 = i
                        break
                except:
                    pass

            url = match2.rsplit('/', 1)[-1]
            url = self.episode_link % (url, season, episode)
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url, referer=url).result
            result = common.parseDOM(result, "div", attrs = { "id": "lang_1" })[0]

            for host in hostDict:
                try:
                    links = re.compile('<span>%s</span>.+?href="(.+?)"' % host.lower()).findall(result)
                    for url in links:
                        url = '%s%s' % (self.base_link, url)
                        watchseries_sources.append({'source': host, 'quality': 'SD', 'provider': 'Watchseries', 'url': url})
                except:
                    pass
        except:
            return

    def cleantitle(self, title):
        title = re.sub('\n|\s(|[(])(UK|US|AU)(|[)])$|\s(vs|v[.])\s|(:|;|-|"|,|\'|\.|\?)|\s', '', title).lower()
        return title

    def resolve(self, url):
        try:
            result = getUrl(url, referer=url).result
            url = common.parseDOM(result, "a", ret="href", attrs = { "class": "myButton" })[0]
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            import commonresolvers
            url = commonresolvers.resolvers().get(url)
            return url
        except:
            return

class flixanity:
    def __init__(self):
        self.base_link = 'http://www.flixanity.com'
        self.search_link = 'http://www.flixanity.com/ajax/search.php?q=%s&limit=5'

    def get(self, name, title, imdb, tvdb, year, season, episode, show, show_alt, hostDict):
        try:
            global flixanity_sources
            flixanity_sources = []

            query = self.search_link % urllib.quote_plus(show)

            result = getUrl(query).result
            result = json.loads(result)
            result = [i for i in result if 'TV' in i['meta']]

            url = [i for i in result if any(x in self.cleantitle(i['title']) for x in [self.cleantitle(show), self.cleantitle(show_alt)]) and any(x in i['title'] for x in [' (%s)' % str(year), ' (%s)' % str(int(year)+1), ' (%s)' % str(int(year)-1)])]
            if len(url) == 0:
                url = [i for i in result if any(x == self.cleantitle(i['title']) for x in [self.cleantitle(show), self.cleantitle(show_alt)])]
            url = url[0]['permalink']
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result
            if not str('tt' + imdb) in result: raise Exception()

            url = common.parseDOM(result, "a", ret="href", attrs = { "class": "item" })
            url = [i for i in url if i.endswith('season/%01d/episode/%01d' % (int(season), int(episode)))][0]
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result
            result = common.parseDOM(result, "script")
            result = [i for i in result if 'var embeds' in i][0]
            result = result.replace('IFRAME', 'iframe').replace('SRC=', 'src=')
            links = common.parseDOM(result, "iframe", ret="src")
            links = [i.split('player.php?', 1)[-1] for i in links]

            for url in links:
                try:
                    host = re.compile('://(.+?)/').findall(url)[0]
                    host = host.rsplit('.', 1)[0].split('w.', 1)[-1]
                    host = [x for x in hostDict if host.lower() == x.lower()][0]

                    flixanity_sources.append({'source': host, 'quality': 'SD', 'provider': 'Flixanity', 'url': url})
                except:
                    pass
        except:
            return

    def cleantitle(self, title):
        title = re.sub('\n|\s(|[(])(UK|US|AU)(|[)])$|\s(vs|v[.])\s|(:|;|-|"|,|\'|\.|\?)|\s', '', title).lower()
        return title

    def resolve(self, url):
        try:
            import commonresolvers
            url = commonresolvers.resolvers().get(url)
            return url
        except:
            return

class shush:
    def __init__(self):
        self.base_link = 'http://www.shush.se'
        self.search_link = 'http://www.shush.se/index.php?shows'
        self.show_link = 'http://www.shush.se/index.php?showlist=%s'

    def get(self, name, title, imdb, tvdb, year, season, episode, show, show_alt, hostDict):
        try:
            global shush_sources
            shush_sources = []

            result = getUrl(self.search_link).result
            result = common.parseDOM(result, "div", attrs = { "class": "shows" })

            url = [common.parseDOM(i, "a", ret="href")[0] for i in result]
            url = [i.split('showlist=')[-1] for i in url]
            url = [i for i in url if any(x == self.cleantitle(i) for x in [self.cleantitle(show), self.cleantitle(show_alt)])][0]
            url = self.show_link % url
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result
            result = common.parseDOM(result, "div", attrs = { "class": "list" })
            result = [i for i in result if ' Season %01d Episode: %01d '% (int(season), int(episode)) in i][0]

            t = common.parseDOM(result, "a")[0]
            t = t.split(' Season %01d Episode: %01d '% (int(season), int(episode)))[-1].split(' ', 1)[-1]
            if not self.cleantitle(title.encode('utf-8').lower()) == self.cleantitle(t.encode('utf-8').lower()): return

            url = common.parseDOM(result, "a", ret="href")[0]
            url = '%s/%s' % (self.base_link, url)
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            import decrypter
            result = getUrl(url).result
            url = re.compile('proxy[.]link=shush[*](.+?)&').findall(result)[-1]
            url = decrypter.decrypter(198,128).decrypt(url,base64.urlsafe_b64decode('SkpCSzc2TmFKdU5zeGRRbWh0WHo='),'ECB').split('\0')[0]

            import commonresolvers
            if 'docs.google.com' in url:
                url = commonresolvers.resolvers().googledocs(url)
            elif 'picasaweb.google.com' in url:
                url = commonresolvers.resolvers().picasaweb(url)
            else:
                return

            if not any(x in url for x in ['&itag=22&', '&itag=37&', '&itag=38&', '&itag=45&', '&itag=84&', '&itag=102&', '&itag=120&', '&itag=121&']): return

            shush_sources.append({'source': 'Shush', 'quality': 'HD', 'provider': 'Shush', 'url': url})
        except:
            return

    def cleantitle(self, title):
        title = re.sub('\n|\s(|[(])(UK|US|AU)(|[)])$|\s(vs|v[.])\s|(:|;|-|"|,|\'|\.|\?)|\s', '', title).lower()
        return title

    def resolve(self, url):
        try:
            url = getUrl(url, output='geturl').result
            if 'requiressl=yes' in url: url = url.replace('http://', 'https://')
            else: url = url.replace('https://', 'http://')
            return url
        except:
            return

class ororotv:
    def __init__(self):
        self.base_link = 'http://ororo.tv'
        self.key_link = base64.urlsafe_b64decode('dXNlciU1QnBhc3N3b3JkJTVEPWMyNjUxMzU2JnVzZXIlNUJlbWFpbCU1RD1jMjY1MTM1NiU0MGRyZHJiLmNvbQ==')
        self.sign_link = 'http://ororo.tv/users/sign_in'

    def get(self, name, title, imdb, tvdb, year, season, episode, show, show_alt, hostDict):
        try:
            global ororotv_sources
            ororotv_sources = []

            result = getUrl(self.base_link).result

            if not "'index show'" in result:
                result = getUrl(self.sign_link, post=self.key_link, close=False).result
                result = getUrl(self.base_link).result
            result = common.parseDOM(result, "div", attrs = { "class": "index show" })

            match = [i for i in result if any(x == self.cleantitle(common.parseDOM(i, "a", attrs = { "class": "name" })[0]) for x in [self.cleantitle(show), self.cleantitle(show_alt)])]
            match2 = [i for i in match if any(x in i for x in ['>%s<' % str(year), '>%s<' % str(int(year)+1), '>%s<' % str(int(year)-1)])][0]
            url = common.parseDOM(match2, "a", ret="href")[0]
            url = '%s%s' % (self.base_link, url)
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result
            url = common.parseDOM(result, "a", ret="data-href", attrs = { "href": "#%01d-%01d" % (int(season), int(episode)) })[0]
            url = '%s%s' % (self.base_link, url)
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            ororotv_sources.append({'source': 'OroroTV', 'quality': 'SD', 'provider': 'OroroTV', 'url': url})
        except:
            return

    def cleantitle(self, title):
        title = re.sub('\n|\s(|[(])(UK|US|AU)(|[)])$|\s(vs|v[.])\s|(:|;|-|"|,|\'|\.|\?)|\s', '', title).lower()
        return title

    def resolve(self, url):
        try:
            result = getUrl(url).result

            if not "my_video" in result:
                result = getUrl(self.sign_link, post=self.key_link, close=False).result
                result = getUrl(url).result

            url = None
            try: url = common.parseDOM(result, "source", ret="src", attrs = { "type": "video/webm" })[0]
            except: pass
            try: url = url = common.parseDOM(result, "source", ret="src", attrs = { "type": "video/mp4" })[0]
            except: pass

            if url is None: return
            if not url.startswith('http://'): url = '%s%s' % (self.base_link, url)
            url = '%s|Cookie=%s' % (url, urllib.quote_plus('video=true'))

            return url
        except:
            return

class putlockertv:
    def __init__(self):
        self.base_link = 'http://putlockertvshows.me'

    def get(self, name, title, imdb, tvdb, year, season, episode, show, show_alt, hostDict):
        try:
            global putlockertv_sources
            putlockertv_sources = []

            search = 'http://www.imdbapi.com/?i=tt%s' % imdb
            search = getUrl(search).result
            search = json.loads(search)
            country = [i.strip() for i in search['Country'].split(',')]
            if 'UK' in country and not 'USA' in country: return

            result = getUrl(self.base_link).result
            result = common.parseDOM(result, "tr", attrs = { "class": "fc" })

            match = [i for i in result if any(x == self.cleantitle(common.parseDOM(i, "a")[0]) for x in [self.cleantitle(show), self.cleantitle(show_alt)])][0]
            url = common.parseDOM(match, "a", ret="href")[0]
            url = '%s%s/ifr/s%02de%02d.html' % (self.base_link, url, int(season), int(episode))
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result
            url = common.parseDOM(result, "div", ret="onclick", attrs = { "class": "badsvideo" })
            if url == []:
                url = common.parseDOM(result, "iframe", ret="src")[-1]
                url = '%s%s' % (self.base_link, url)
                result = getUrl(url).result
                url = common.parseDOM(result, "div", ret="onclick", attrs = { "class": "badsvideo" })
            url = re.compile(".*'(.+?)'").findall(url[0])[0]
            url = '%s%s' % (self.base_link, url)
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result
            url = common.parseDOM(result, "iframe", ret="src")[0]
            url = url.replace('putlocker', 'firedrive')
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            if 'firedrive' in url: source = 'Firedrive'
            elif 'mail.ru' in url: source = 'Mailru'
            else: return

            putlockertv_sources.append({'source': source, 'quality': 'SD', 'provider': 'PutlockerTV', 'url': url})
        except:
            return

    def cleantitle(self, title):
        title = re.sub('\n|\s(|[(])(UK|US|AU)(|[)])$|\s(vs|v[.])\s|(:|;|-|"|,|\'|\.|\?)|\s', '', title).lower()
        return title

    def resolve(self, url):
        try:
            import commonresolvers
            url = commonresolvers.resolvers().get(url)
            return url
        except:
            return

class clickplay:
    def __init__(self):
        self.base_link = 'http://clickplay.to'
        self.search_link = 'http://clickplay.to/search/%s'

    def get(self, name, title, imdb, tvdb, year, season, episode, show, show_alt, hostDict):
        try:
            global clickplay_sources
            clickplay_sources = []

            query = self.search_link % urllib.quote_plus(' '.join([i for i in show.split() if i not in ['The','the','A','a']]))
            result = getUrl(query).result
            result = common.parseDOM(result, "div", attrs = { "id": "video_list" })[0]
            result = result.split('</a>')

            match = [i for i in result if any(x in self.cleantitle(i) for x in [str('>' + self.cleantitle(show) + '(%s)' % str(year) + '<'), str('>' + self.cleantitle(show) + '(%s)' % str(int(year)+1) + '<'), str('>' + self.cleantitle(show) + '(%s)' % str(int(year)-1) + '<'), str('>' + self.cleantitle(show_alt) + '(%s)' % str(year) + '<'), str('>' + self.cleantitle(show_alt) + '(%s)' % str(int(year)+1) + '<'), str('>' + self.cleantitle(show_alt) + '(%s)' % str(int(year)-1) + '<')])][0]
            url = common.parseDOM(match, "a", ret="href")[0]
            url = '%sseason-%01d/episode-%01d' % (url, int(season), int(episode))
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            import decrypter
            result = getUrl(url).result
            links = re.compile('<a href="([?]link_id=.+?)".+?rel="noindex, nofollow".+?\[720p\].+?</a>').findall(result)
            u = re.compile('content="(%s.+?)"' % url).findall(result)[0]

            for i in links[:5]:
                try:
                    result = getUrl(u + i).result
                    url = re.compile('proxy[.]link=clickplay[*](.+?)"').findall(result)[-1]
                    url = decrypter.decrypter(198,128).decrypt(url,base64.urlsafe_b64decode('bW5pcUpUcUJVOFozS1FVZWpTb00='),'ECB').split('\0')[0]
                    if 'vk.com' in url:
                        import commonresolvers
                        vk = commonresolvers.resolvers().vk(url)
                        for i in vk: clickplay_sources.append({'source': 'VK', 'quality': i['quality'], 'provider': 'Clickplay', 'url': i['url']})
                    elif 'firedrive' in url:
                        clickplay_sources.append({'source': 'Firedrive', 'quality': 'HD', 'provider': 'Clickplay', 'url': url})
                    elif 'mail.ru' in url:
                        clickplay_sources.append({'source': 'Mailru', 'quality': 'SD', 'provider': 'Clickplay', 'url': url})
                except:
                    pass
        except:
            return

    def cleantitle(self, title):
        title = re.sub('\n|\s(|[(])(UK|US|AU)(|[)])$|\s(vs|v[.])\s|(:|;|-|"|,|\'|\.|\?)|\s', '', title).lower()
        return title

    def resolve(self, url):
        try:
            import commonresolvers
            url = commonresolvers.resolvers().get(url)
            return url
        except:
            return

class vkbox:
    def __init__(self):
        self.base_link = 'http://mobapps.cc'
        self.data_link = 'http://mobapps.cc/data/data_en.zip'
        self.episodes_link = 'http://mobapps.cc/api/serials/e/?h=%s&u=%s&y=%s'
        self.tv_link = 'tv_lite.json'

    def get(self, name, title, imdb, tvdb, year, season, episode, show, show_alt, hostDict):
        try:
            global vkbox_sources
            vkbox_sources = []

            search = 'http://www.imdbapi.com/?i=tt%s' % imdb
            search = getUrl(search).result
            search = json.loads(search)
            country = [i.strip() for i in search['Country'].split(',')]
            if 'UK' in country and not 'USA' in country: return

            result = self.getdata()
            #result = cache2(self.getdata)
            result = json.loads(result)

            match = [i['id'] for i in result if any(x == self.cleantitle(i['title']) for x in [self.cleantitle(show), self.cleantitle(show_alt)])][0]
            url = self.episodes_link % (match, season, episode)
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            request = urllib2.Request(url,None)
            request.add_header('User-Agent', 'android-async-http/1.4.1 (http://loopj.com/android-async-http)')
            response = urllib2.urlopen(request, timeout=10)
            result = response.read()
            response.close()
            param = re.findall('"lang":"en","apple":(\d+?),"google":(\d+?),"microsoft":"(.+?)"', result, re.I)
            num = int(match) + int(season) + int(episode)
            url = 'https://vk.com/video_ext.php?oid=%s&id=%s&hash=%s' % (str(int(param[0][0]) + num), str(int(param[0][1]) + num), param[0][2])

            import commonresolvers
            url = commonresolvers.resolvers().vk(url)
            for i in url: vkbox_sources.append({'source': 'VK', 'quality': i['quality'], 'provider': 'VKBox', 'url': i['url']})
        except:
            return

    def getdata(self):
        try:
            import zipfile, StringIO
            data = urllib2.urlopen(self.data_link, timeout=10).read()
            zip = zipfile.ZipFile(StringIO.StringIO(data))
            read = zip.open(self.tv_link)
            result = read.read()
            return result
        except:
            return

    def cleantitle(self, title):
        title = re.sub('\n|\s(|[(])(UK|US|AU)(|[)])$|\s(vs|v[.])\s|(:|;|-|"|,|\'|\.|\?)|\s', '', title).lower()
        return title

    def resolve(self, url):
        return url

class istreamhd:
    def __init__(self):
        self.base_link = 'http://istreamhd.org'
        self.login_link = 'aHR0cDovL2lzdHJlYW1oZC5vcmcvYXBpL2F1dGhlbnRpY2F0ZS5waHA='
        self.search_link = 'aHR0cDovL2lzdHJlYW1oZC5vcmcvYXBpL3NlYXJjaC5waHA='
        self.show_link = 'aHR0cDovL2lzdHJlYW1oZC5vcmcvYXBpL2dldF9zaG93LnBocA=='
        self.get_link = 'aHR0cDovL2lzdHJlYW1oZC5vcmcvYXBpL2dldF92aWRlby5waHA='
        self.mail, self.password = getSetting("istreamhd_mail"), getSetting("istreamhd_password")

    def get(self, name, title, imdb, tvdb, year, season, episode, show, show_alt, hostDict):
        try:
            global istreamhd_sources
            istreamhd_sources = []

            if (self.mail == '' or self.password == ''): raise Exception()

            post = urllib.urlencode({'e-mail': self.mail, 'password': self.password})
            result = getUrl(base64.urlsafe_b64decode(self.login_link), post=post).result
            result = json.loads(result)
            token = result['auth']['token']

            post = urllib.urlencode({'token': token, 'query': show})
            result = getUrl(base64.urlsafe_b64decode(self.search_link), post=post).result
            result = json.loads(result)
            url = result['result']['items']
            url = [i for i in url if str('tt' + imdb) in i['poster']][0]

            post = urllib.urlencode({'token': token, 'show': url['title'], 'cat_id': url['cat_id']})
            result = getUrl(base64.urlsafe_b64decode(self.show_link), post=post).result
            result = json.loads(result)
            url = result['result']['items']
            url = [i for i in url if i['season'] == str('%01d' % int(season)) and  i['episode'] == str('%01d' % int(episode))][0]
            url = url['vid_id']

            post = urllib.urlencode({'token': token, 'vid_id': url})
            result = getUrl(base64.urlsafe_b64decode(self.get_link), post=post).result
            result = json.loads(result)
            url = result['video']['url']
            url = url.replace('http://', 'https://')
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            import commonresolvers
            url = commonresolvers.resolvers().vk(url)
            for i in url: istreamhd_sources.append({'source': 'VK', 'quality': i['quality'], 'provider': 'iStreamHD', 'url': i['url']})
        except:
            return

    def resolve(self, url):
        return url

class simplymovies:
    def __init__(self):
        self.base_link = 'http://simplymovies.net'
        self.search_link = 'http://simplymovies.net/tv_shows.php?searchTerm='

    def get(self, name, title, imdb, tvdb, year, season, episode, show, show_alt, hostDict):
        try:
            global simplymovies_sources
            simplymovies_sources = []

            query = self.search_link + urllib.quote_plus(show.replace(' ', '-'))

            result = getUrl(query).result
            url = common.parseDOM(result, "div", attrs = { "class": "movieInfoHolder" })
            try: match = [i for i in url if any(x in self.cleantitle(i) for x in [str('>' + self.cleantitle(show) + '<'), str('>' + self.cleantitle(show_alt) + '<')])][0]
            except: pass
            try: match = [i for i in url if str('tt' + imdb) in i][0]
            except: pass
            url = common.parseDOM(match, "a", ret="href")[0]
            url = '%s/%s' % (self.base_link, url)
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result
            url = result.split('<h3>')
            url = [i for i in url if str('Season %01d</h3>' % int(season)) in i][-1]
            url = url.replace(':','<')
            url = re.compile('.*href="(.+?)">Episode %01d<' % int(episode)).findall(url)[0]
            url = '%s/%s' % (self.base_link, url)
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result
            url = common.parseDOM(result, "iframe", ret="src", attrs = { "class": "videoPlayerIframe" })[0]
            url = common.replaceHTMLCodes(url)
            url = url.replace('http://', 'https://')
            url = url.encode('utf-8')

            import commonresolvers
            url = commonresolvers.resolvers().vk(url)
            for i in url: simplymovies_sources.append({'source': 'VK', 'quality': i['quality'], 'provider': 'Simplymovies', 'url': i['url']})
        except:
            return

    def cleantitle(self, title):
        title = re.sub('\n|\s(|[(])(UK|US|AU)(|[)])$|\s(vs|v[.])\s|(:|;|-|"|,|\'|\.|\?)|\s', '', title).lower()
        return title

    def resolve(self, url):
        return url

class moviestorm:
    def __init__(self):
        self.base_link = 'http://moviestorm.eu'
        self.search_link = 'http://moviestorm.eu/search?q=%s'

    def get(self, name, title, imdb, tvdb, year, season, episode, show, show_alt, hostDict):
        try:
            global moviestorm_sources
            moviestorm_sources = []

            query = self.search_link % (urllib.quote_plus(show))

            result = getUrl(query).result
            url = common.parseDOM(result, "div", attrs = { "class": "movie_box" })
            url = [i for i in url if str('tt' + imdb) in i][0]
            url = common.parseDOM(url, "a", ret="href")[0]
            url = '%s?season=%01d&episode=%01d' % (url, int(season), int(episode))
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result
            result = common.parseDOM(result, "div", attrs = { "id": "searialinks" })[0]
            links = re.compile('"(http://ishared.eu/.+?)"').findall(result)

            for url in links:
                moviestorm_sources.append({'source': 'iShared', 'quality': 'SD', 'provider': 'Moviestorm', 'url': url})
        except:
            return

    def resolve(self, url):
        try:
            import commonresolvers
            url = commonresolvers.resolvers().get(url)
            return url
        except:
            return

class noobroom:
    def __init__(self):
        self.base_link = 'http://noobroom5.com'
        self.search_link = 'http://noobroom5.com/search.php?q=%s'
        self.login_link = 'http://noobroom5.com/login.php'
        self.login2_link = 'http://noobroom5.com/login2.php'
        self.mail, self.password = getSetting("noobroom_mail"), getSetting("noobroom_password")

    def get(self, name, title, imdb, tvdb, year, season, episode, show, show_alt, hostDict):
        try:
            global noobroom_sources
            noobroom_sources = []

            if (self.mail == '' or self.password == ''): raise Exception()

            search = 'http://www.imdbapi.com/?i=tt%s' % imdb
            search = getUrl(search).result
            search = json.loads(search)
            country = [i.strip() for i in search['Country'].split(',')]
            if 'UK' in country and not 'USA' in country: return

            query = self.search_link % (urllib.quote_plus(show))

            result = self.login()
            result = getUrl(query).result

            url = re.compile('(<i>TV Series</i>.+)').findall(result)[0]
            url = url.split("><a ")
            url = [i for i in url if any(x in self.cleantitle(i) for x in [str('>' + self.cleantitle(show) + '<'), str('>' + self.cleantitle(show_alt) + '<')])][0]
            url = re.compile("href='(.+?)'").findall(url)[0]
            url = '%s%s' % (self.base_link, url)
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result
            url = re.compile("<b>%01dx%02d .+?style=.+? href='(.+?)'" % (int(season), int(episode))).findall(result)[0]
            url = '%s%s' % (self.base_link, url)
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result
            links = re.compile('"file": "(.+?)"').findall(result)
            try: u = [i for i in links if 'type=flv' in i][0]
            except: pass
            try: u = [i for i in links if 'type=mp4' in i][0]
            except: pass
            url = '%s%s' % (self.base_link, u)
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            try:
                quality = 'SD'
                q = re.compile('"width": "(.+?)"').findall(result)[0]
                if int(q) > 720: quality = 'HD'
            except:
                pass

            noobroom_sources.append({'source': 'Noobroom', 'quality': quality, 'provider': 'Noobroom', 'url': url})
        except:
            return

    def login(self):
        try:
            post = urllib.urlencode({'email': self.mail, 'password': self.password})
            result = getUrl(self.login_link, close=False).result
            cookie = getUrl(self.login_link, output='cookie').result
            result = urllib2.Request(self.login2_link, post)
            result = urllib2.urlopen(result, timeout=10)
        except:
            return

    def cleantitle(self, title):
        title = re.sub('\n|\s(|[(])(UK|US|AU)(|[)])$|\s(vs|v[.])\s|(:|;|-|"|,|\'|\.|\?)|\s', '', title).lower()
        return title

    def resolve(self, url):
        try:
            result = self.login()
            try: u = getUrl(url, output='geturl').result
            except: pass
            try: u = getUrl(url.replace('&hd=0', '&hd=1'), output='geturl').result
            except: pass
            return u
        except:
            return


main()