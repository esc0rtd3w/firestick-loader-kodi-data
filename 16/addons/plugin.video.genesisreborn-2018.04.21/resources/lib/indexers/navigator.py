# -*- coding: utf-8 -*-

'''
    genesisreborn Add-on
    Copyright (C) 2016 genesisreborn

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


import os,sys,urlparse

from resources.lib.modules import control
from resources.lib.modules import trakt


sysaddon = sys.argv[0] ; syshandle = int(sys.argv[1]) ; ()

artPath = control.artPath() ; addonFanart = control.addonFanart()

imdbCredentials = False if control.setting('imdb.user') == '' else True

traktCredentials = trakt.getTraktCredentialsInfo()

traktIndicators = trakt.getTraktIndicatorsInfo()

queueMenu = control.lang(32065).encode('utf-8')


class navigator:
    def root(self):
        self.addDirectoryItem('Created by JP Hightek', 'ShowChangelog', 'icon.png', 'DefaultFolder.png')
        self.addDirectoryItem('Genesis Reborn Custom Viewtype', 'viewsNavigator', 'icon.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem('Genesis Reborn Movies', 'movieNavigator', 'movies.png', 'DefaultMovies.png')
        self.addDirectoryItem('Genesis Reborn TV Shows', 'tvNavigator', 'channels.png', 'DefaultTVShows.png')
        self.addDirectoryItem('My Genesis Reborn Library', 'libraryNavigator', 'tools.png', 'DefaultAddonProgram.png')

        if not control.setting('lists.widget') == '0':
            self.addDirectoryItem('My Genesis Reborn Movies (Trakt/Imdb)', 'mymovieNavigator', 'mymovies.png', 'DefaultVideoPlaylists.png')
            self.addDirectoryItem('My Genesis Reborn TV Shows (Trakt/Imdb)', 'mytvNavigator', 'mymovies.png', 'DefaultVideoPlaylists.png')

        if not control.setting('movie.widget') == '0':
            self.addDirectoryItem('Genesis Reborn New Movies', 'movieWidget', 'latest-movies.png', 'DefaultRecentlyAddedMovies.png')

        if (traktIndicators == True and not control.setting('tv.widget.alt') == '0') or (traktIndicators == False and not control.setting('tv.widget') == '0'):
            self.addDirectoryItem('Genesis Reborn New TV Shows', 'tvshows&url=premiere', 'years.png', 'DefaultRecentlyAddedEpisodes.png')

        self.addDirectoryItem('Genesis Reborn Channels', 'channels', 'channels.png', 'DefaultMovies.png')

        self.addDirectoryItem('Genesis Reborn Tools', 'toolNavigator', 'tools.png', 'DefaultAddonProgram.png')

        downloads = True if control.setting('downloads') == 'true' and (len(control.listDir(control.setting('movie.download.path'))[0]) > 0 or len(control.listDir(control.setting('tv.download.path'))[0]) > 0) else False
        if downloads == True:
            self.addDirectoryItem(32009, 'downloadNavigator', 'downloads.png', 'DefaultFolder.png')

        self.addDirectoryItem('Genesis Reborn Search Menu', 'searchNavigator', 'search.png', 'DefaultFolder.png')
        
        self.addDirectoryItem('Join The Private Facebook Group Called - Jesus Box Media Support & Addons', 'ShowChangelog', 'icon.png', 'DefaultFolder.png')

        self.endDirectory()


    def movies(self, lite=False):
        self.addDirectoryItem('Genesis Reborn Movie Library', control.setting('library.movie'), 'movies.png', 'DefaultMovies.png', isAction=False)       
        self.addDirectoryItem('Genesis Reborn Genres', 'movieGenres', 'genres.png', 'DefaultMovies.png')
        self.addDirectoryItem('Genesis Reborn Trending', 'movies&url=trending', 'trending.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Genesis Reborn Years', 'movieYears', 'years.png', 'DefaultMovies.png')
        self.addDirectoryItem('Genesis Reborn People', 'moviePersons', 'people.png', 'DefaultMovies.png')
        #self.addDirectoryItem(32014, 'movieLanguages', 'languages.png', 'DefaultMovies.png')
        self.addDirectoryItem('Genesis Reborn Ratings', 'movieCertificates', 'certificates.png', 'DefaultMovies.png')
        self.addDirectoryItem('Genesis Reborn Most Populars', 'movies&url=popular', 'populars.png', 'DefaultMovies.png')
        self.addDirectoryItem('Genesis Reborn Highly Rated', 'movies&url=views', 'most-viewed.png', 'DefaultMovies.png')
        self.addDirectoryItem('Genesis Reborn Box Office', 'movies&url=boxoffice', 'oscars.png', 'DefaultFolder.png')
        #self.addDirectoryItem('Genesis Reborn Most Voted', 'movies&url=tmdboscars', 'oscars.png', 'DefaultMovies.png')
        self.addDirectoryItem('Genesis Reborn In Theaters', 'movies&url=theaters', 'in-theaters.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Genesis Reborn Featured', 'movies&url=featured', 'featured.png', 'DefaultRecentlyAddedMovies.png')

        if lite == False:
            if not control.setting('lists.widget') == '0':
                self.addDirectoryItem('My Genesis Reborn Trakt/Imdb', 'mymovieliteNavigator', 'mymovies.png', 'DefaultVideoPlaylists.png')

            self.addDirectoryItem('Genesis Reborn People Search', 'moviePerson', 'people-search.png', 'DefaultMovies.png')
            self.addDirectoryItem('Genesis Reborn Movie Search', 'movieSearch', 'search.png', 'DefaultMovies.png')

        self.endDirectory()


    def mymovies(self, lite=False):
        self.accountCheck()

        if traktCredentials == True and imdbCredentials == True:
            self.addDirectoryItem(32032, 'movies&url=traktcollection', 'trakt.png', 'DefaultMovies.png', queue=True, context=(32551, 'moviesToLibrary&url=traktcollection'))
            self.addDirectoryItem(32033, 'movies&url=traktwatchlist', 'trakt.png', 'DefaultMovies.png', queue=True, context=(32551, 'moviesToLibrary&url=traktwatchlist'))
            self.addDirectoryItem(32034, 'movies&url=imdbwatchlist', 'imdb.png', 'DefaultMovies.png', queue=True)

        elif traktCredentials == True:
            self.addDirectoryItem(32032, 'movies&url=traktcollection', 'trakt.png', 'DefaultMovies.png', queue=True, context=(32551, 'moviesToLibrary&url=traktcollection'))
            self.addDirectoryItem(32033, 'movies&url=traktwatchlist', 'trakt.png', 'DefaultMovies.png', queue=True, context=(32551, 'moviesToLibrary&url=traktwatchlist'))

        elif imdbCredentials == True:
            self.addDirectoryItem(32032, 'movies&url=imdbwatchlist', 'imdb.png', 'DefaultMovies.png', queue=True)
            self.addDirectoryItem(32033, 'movies&url=imdbwatchlist2', 'imdb.png', 'DefaultMovies.png', queue=True)

        if traktCredentials == True:
            self.addDirectoryItem(32035, 'movies&url=traktfeatured', 'trakt.png', 'DefaultMovies.png', queue=True)

        elif imdbCredentials == True:
            self.addDirectoryItem(32035, 'movies&url=featured', 'imdb.png', 'DefaultMovies.png', queue=True)

        if traktIndicators == True:
            self.addDirectoryItem(32036, 'movies&url=trakthistory', 'trakt.png', 'DefaultMovies.png', queue=True)

        self.addDirectoryItem(32039, 'movieUserlists', 'userlists.png', 'DefaultMovies.png')

        if lite == False:
            self.addDirectoryItem(32031, 'movieliteNavigator', 'movies.png', 'DefaultMovies.png')
            self.addDirectoryItem(32028, 'moviePerson', 'people-search.png', 'DefaultMovies.png')
            self.addDirectoryItem(32010, 'movieSearch', 'search.png', 'DefaultMovies.png')

        self.endDirectory()


    def tvshows(self, lite=False):
        self.addDirectoryItem('Genesis Reborn TV Show Library', control.setting('library.tv'), 'movies.png', 'DefaultTVShows.png', isAction=False)
        self.addDirectoryItem('Genesis Reborn Genres', 'tvGenres', 'genres.png', 'DefaultTVShows.png')
        self.addDirectoryItem('Genesis Reborn Selections', 'tvshows&url=rating', 'populars.png', 'DefaultTVShows.png')
        self.addDirectoryItem('Genesis Reborn Networks', 'tvNetworks', 'networks.png', 'DefaultTVShows.png')
        self.addDirectoryItem('Genesis Reborn Languages', 'tvLanguages', 'trending.png', 'DefaultTVShows.png')
        self.addDirectoryItem('Genesis Reborn Ratings', 'tvCertificates', 'certificates.png', 'DefaultTVShows.png')
        self.addDirectoryItem('Genesis Reborn Trending', 'tvshows&url=trending', 'trending.png', 'DefaultRecentlyAddedEpisodes.png')
        self.addDirectoryItem('Genesis Reborn Most Popular', 'tvshows&url=popular', 'most-viewed.png', 'DefaultTVShows.png')
        self.addDirectoryItem('Genesis Reborn Most Voted', 'tvshows&url=views', 'most-viewed.png', 'DefaultTVShows.png')
        self.addDirectoryItem('Genesis Reborn On TV Today', 'tvshows&url=airing', 'airing-today.png', 'DefaultTVShows.png')
        #self.addDirectoryItem('Genesis Reborn Returning Shows', 'tvshows&url=active', 'years.png', 'DefaultTVShows.png')
        self.addDirectoryItem('Genesis Reborn New Shows', 'tvshows&url=premiere', 'featured.png', 'DefaultTVShows.png')
        self.addDirectoryItem('Genesis Reborn TV Guide', 'calendar&url=added', 'airing-today.png', 'DefaultRecentlyAddedEpisodes.png', queue=True)
        self.addDirectoryItem('Genesis Reborn TV Calendar', 'calendars', 'networks.png', 'DefaultRecentlyAddedEpisodes.png')

        if lite == False:
            if not control.setting('lists.widget') == '0':
                self.addDirectoryItem('Genesis Reborn Trakt/Imdb', 'mytvliteNavigator', 'airing-today.png', 'DefaultVideoPlaylists.png')

            self.addDirectoryItem('Genesis Reborn People Search', 'tvPerson', 'people-search.png', 'DefaultTVShows.png')
            self.addDirectoryItem('Genesis Reborn TV Show Search', 'tvSearch', 'search.png', 'DefaultTVShows.png')

        self.endDirectory()


    def mytvshows(self, lite=False):
        self.accountCheck()

        if traktCredentials == True and imdbCredentials == True:
            self.addDirectoryItem(32032, 'tvshows&url=traktcollection', 'trakt.png', 'DefaultTVShows.png', context=(32551, 'tvshowsToLibrary&url=traktcollection'))
            self.addDirectoryItem(32033, 'tvshows&url=traktwatchlist', 'trakt.png', 'DefaultTVShows.png', context=(32551, 'tvshowsToLibrary&url=traktwatchlist'))
            self.addDirectoryItem(32034, 'tvshows&url=imdbwatchlist', 'imdb.png', 'DefaultTVShows.png')

        elif traktCredentials == True:
            self.addDirectoryItem(32032, 'tvshows&url=traktcollection', 'trakt.png', 'DefaultTVShows.png', context=(32551, 'tvshowsToLibrary&url=traktcollection'))
            self.addDirectoryItem(32033, 'tvshows&url=traktwatchlist', 'trakt.png', 'DefaultTVShows.png', context=(32551, 'tvshowsToLibrary&url=traktwatchlist'))

        elif imdbCredentials == True:
            self.addDirectoryItem(32032, 'tvshows&url=imdbwatchlist', 'imdb.png', 'DefaultTVShows.png')
            self.addDirectoryItem(32033, 'tvshows&url=imdbwatchlist2', 'imdb.png', 'DefaultTVShows.png')

        if traktCredentials == True:
            self.addDirectoryItem(32035, 'tvshows&url=traktfeatured', 'trakt.png', 'DefaultTVShows.png')

        elif imdbCredentials == True:
            self.addDirectoryItem(32035, 'tvshows&url=trending', 'imdb.png', 'DefaultMovies.png', queue=True)

        if traktIndicators == True:
            self.addDirectoryItem(32036, 'calendar&url=trakthistory', 'trakt.png', 'DefaultTVShows.png', queue=True)
            self.addDirectoryItem(32037, 'calendar&url=progress', 'trakt.png', 'DefaultRecentlyAddedEpisodes.png', queue=True)
            self.addDirectoryItem(32038, 'calendar&url=mycalendar', 'trakt.png', 'DefaultRecentlyAddedEpisodes.png', queue=True)

        self.addDirectoryItem(32040, 'tvUserlists', 'userlists.png', 'DefaultTVShows.png')

        if traktCredentials == True:
            self.addDirectoryItem(32041, 'episodeUserlists', 'userlists.png', 'DefaultTVShows.png')

        if lite == False:
            self.addDirectoryItem(32031, 'tvliteNavigator', 'tvshows.png', 'DefaultTVShows.png')
            self.addDirectoryItem(32028, 'tvPerson', 'people-search.png', 'DefaultTVShows.png')
            self.addDirectoryItem(32010, 'tvSearch', 'search.png', 'DefaultTVShows.png')

        self.endDirectory()


    def tools(self):
        self.addDirectoryItem(32043, 'openSettings&query=0.0', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32044, 'openSettings&query=3.1', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32045, 'openSettings&query=1.0', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32046, 'openSettings&query=6.0', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32047, 'openSettings&query=2.0', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32556, 'libraryNavigator', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32049, 'viewsNavigator', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32050, 'clearSources', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32052, 'clearCache', 'tools.png', 'DefaultAddonProgram.png')

        self.endDirectory()

    def library(self):
        self.addDirectoryItem(32557, 'openSettings&query=4.0', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32558, 'updateLibrary&query=tool', 'library_update.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32559, control.setting('library.movie'), 'movies.png', 'DefaultMovies.png', isAction=False)
        self.addDirectoryItem(32560, control.setting('library.tv'), 'tvshows.png', 'DefaultTVShows.png', isAction=False)

        if trakt.getTraktCredentialsInfo():
            self.addDirectoryItem(32561, 'moviesToLibrary&url=traktcollection', 'trakt.png', 'DefaultMovies.png')
            self.addDirectoryItem(32562, 'moviesToLibrary&url=traktwatchlist', 'trakt.png', 'DefaultMovies.png')
            self.addDirectoryItem(32563, 'tvshowsToLibrary&url=traktcollection', 'trakt.png', 'DefaultTVShows.png')
            self.addDirectoryItem(32564, 'tvshowsToLibrary&url=traktwatchlist', 'trakt.png', 'DefaultTVShows.png')

        self.endDirectory()

    def downloads(self):
        movie_downloads = control.setting('movie.download.path')
        tv_downloads = control.setting('tv.download.path')

        if len(control.listDir(movie_downloads)[0]) > 0:
            self.addDirectoryItem(32001, movie_downloads, 'movies.png', 'DefaultMovies.png', isAction=False)
        if len(control.listDir(tv_downloads)[0]) > 0:
            self.addDirectoryItem(32002, tv_downloads, 'tvshows.png', 'DefaultTVShows.png', isAction=False)

        self.endDirectory()


    def search(self):
        self.addDirectoryItem(32001, 'movieSearch', 'search.png', 'DefaultMovies.png')
        self.addDirectoryItem(32002, 'tvSearch', 'search.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32029, 'moviePerson', 'people-search.png', 'DefaultMovies.png')
        self.addDirectoryItem(32030, 'tvPerson', 'people-search.png', 'DefaultTVShows.png')

        self.endDirectory()


    def views(self):
        try:
            control.idle()

            items = [ (control.lang(32001).encode('utf-8'), 'movies'), (control.lang(32002).encode('utf-8'), 'tvshows'), (control.lang(32054).encode('utf-8'), 'seasons'), (control.lang(32038).encode('utf-8'), 'episodes') ]

            select = control.selectDialog([i[0] for i in items], control.lang(32049).encode('utf-8'))

            if select == -1: return

            content = items[select][1]

            title = control.lang(32059).encode('utf-8')
            url = '%s?action=addView&content=%s' % (sys.argv[0], content)

            poster, banner, fanart = control.addonPoster(), control.addonBanner(), control.addonFanart()

            item = control.item(label=title)
            item.setInfo(type='Video', infoLabels = {'title': title})
            item.setArt({'icon': poster, 'thumb': poster, 'poster': poster, 'banner': banner})
            item.setProperty('Fanart_Image', fanart)

            control.addItem(handle=int(sys.argv[1]), url=url, listitem=item, isFolder=False)
            control.content(int(sys.argv[1]), content)
            control.directory(int(sys.argv[1]), cacheToDisc=True)

            from resources.lib.modules import views
            views.setView(content, {})
        except:
            return


    def accountCheck(self):
        if traktCredentials == False and imdbCredentials == False:
            control.idle()
            control.infoDialog(control.lang(32042).encode('utf-8'), sound=True, icon='WARNING')
            sys.exit()


    def infoCheck(self, version):
        try:
            control.infoDialog('www.tvaddons.ag', control.lang(32074).encode('utf-8'), time=5000, sound=False)
            return '1'
        except:
            return '1'


    def clearCache(self):
        control.idle()
        yes = control.yesnoDialog(control.lang(32056).encode('utf-8'), '', '')
        if not yes: return
        from resources.lib.modules import cache
        cache.cache_clear()
        control.infoDialog(control.lang(32057).encode('utf-8'), sound=True, icon='INFO')


    def addDirectoryItem(self, name, query, thumb, icon, context=None, queue=False, isAction=True, isFolder=True):
        try: name = control.lang(name).encode('utf-8')
        except: pass
        url = '%s?action=%s' % (sysaddon, query) if isAction == True else query
        thumb = os.path.join(artPath, thumb) if not artPath == None else icon
        cm = []
        if queue == True: cm.append((queueMenu, 'RunPlugin(%s?action=queueItem)' % sysaddon))
        if not context == None: cm.append((control.lang(context[0]).encode('utf-8'), 'RunPlugin(%s?action=%s)' % (sysaddon, context[1])))
        item = control.item(label=name)
        item.addContextMenuItems(cm)
        item.setArt({'icon': thumb, 'thumb': thumb})
        if not addonFanart == None: item.setProperty('Fanart_Image', addonFanart)
        control.addItem(handle=syshandle, url=url, listitem=item, isFolder=isFolder)


    def endDirectory(self):
        control.content(syshandle, 'addons')
        control.directory(syshandle, cacheToDisc=True)


