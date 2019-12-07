# -*- coding: utf-8 -*-

'''
#:::'##::::'#######:::'######::'##::::::::'#######::'##:::::'##:'##::: ##::'######::
#:'####:::'##.... ##:'##... ##: ##:::::::'##.... ##: ##:'##: ##: ###:: ##:'##... ##:
#:.. ##:::..::::: ##: ##:::..:: ##::::::: ##:::: ##: ##: ##: ##: ####: ##: ##:::..::
#::: ##::::'#######:: ##::::::: ##::::::: ##:::: ##: ##: ##: ##: ## ## ##:. ######::
#::: ##::::...... ##: ##::::::: ##::::::: ##:::: ##: ##: ##: ##: ##. ####::..... ##:
#::: ##:::'##:::: ##: ##::: ##: ##::::::: ##:::: ##: ##: ##: ##: ##:. ###:'##::: ##:
#:'######:. #######::. ######:: ########:. #######::. ###. ###:: ##::. ##:. ######::
#:......:::.......::::......:::........:::.......::::...::...:::..::::..:::......:::

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

import os, sys, urllib2, urlparse
import xbmc, xbmcaddon, xbmcgui

from resources.lib.modules import control
from resources.lib.modules import trakt
from resources.lib.modules import cache

sysaddon = sys.argv[0] ; syshandle = int(sys.argv[1])
artPath = control.artPath() ; addonFanart = control.addonFanart()

imdbCredentials = False if control.setting('imdb.user') == '' else True

traktCredentials = trakt.getTraktCredentialsInfo()
traktIndicators = trakt.getTraktIndicatorsInfo()

queueMenu = control.lang(32065).encode('utf-8')

class navigator:
    ADDON_ID      = xbmcaddon.Addon().getAddonInfo('id')
    HOMEPATH      = xbmc.translatePath('special://home/')
    ADDONSPATH    = os.path.join(HOMEPATH, 'addons')
    THISADDONPATH = os.path.join(ADDONSPATH, ADDON_ID)
    NEWSFILE      = ''
    LOCALNEWS     = os.path.join(THISADDONPATH, 'newsinfo.txt')

    def root(self):
        self.addDirectoryItem('Help / Information / Credits', 'newsNavigator', 'help.png', 'DefaultAddonProgram.png')
        if self.getMenuEnabled('navi.monthlyclown') == True:
            self.addDirectoryItem('[B][COLORred]13Clowns[/COLOR] Favorites[/B]', 'movies&url=clowns', 'icon.png', 'DefaultRecentlyAddedMovies.png')
        
        if self.getMenuEnabled('navi.monthlyspotlight') == True:
            self.addDirectoryItem('[B][COLOR yellow]Monthly Spotlight[/COLOR][/B]', 'movies&url=spotlight', 'spotlight.png', 'DefaultRecentlyAddedMovies.png')
        
        self.addDirectoryItem(32001, 'movieNavigator', 'movies.png', 'DefaultMovies.png')
        
        self.addDirectoryItem(32002, 'tvNavigator', 'tvshows.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.cartoons') == True:
            self.addDirectoryItem('Cartoons', 'tvshows&url=cartoons', 'cartoons.png', 'DefaultTVShows.png')
        
        if self.getMenuEnabled('navi.docu') == True:
            self.addDirectoryItem(32631, 'docuHeaven', 'documentaries.png', 'DefaultMovies.png')
        
        if self.getMenuEnabled('navi.yt') == True:
            self.addDirectoryItem('You Tube Videos', 'youtube', 'youtube.png', 'youtube.png')
        
        if not control.setting('lists.widget') == '0':
            self.addDirectoryItem(32003, 'mymovieNavigator', 'mymovies.png', 'DefaultVideoPlaylists.png')
            self.addDirectoryItem(32004, 'mytvNavigator', 'mytvshows.png', 'DefaultVideoPlaylists.png')

        if not control.setting('movie.widget') == '0':
            self.addDirectoryItem(32005, 'movieWidget', 'latest-movies.png', 'DefaultRecentlyAddedMovies.png')

        if (traktIndicators == True and not control.setting('tv.widget.alt') == '0') or (traktIndicators == False and not control.setting('tv.widget') == '0'):
            self.addDirectoryItem(32006, 'tvWidget', 'latest-episodes.png', 'DefaultRecentlyAddedEpisodes.png')

        self.addDirectoryItem(32008, 'toolNavigator', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem('Choose Scraper Package', 'openSettings&query=3.0', 'tools.png', 'DefaultAddonProgram.png')
        
        downloads = True if control.setting('downloads') == 'true' and (len(control.listDir(control.setting('movie.download.path'))[0]) > 0 or len(control.listDir(control.setting('tv.download.path'))[0]) > 0) else False
        if downloads == True:
            self.addDirectoryItem(32009, 'downloadNavigator', 'downloads.png', 'DefaultFolder.png')
               
        self.endDirectory()

    def furk(self):
        self.addDirectoryItem('User Files', 'furkUserFiles', 'mytvnavigator.png', 'mytvnavigator.png')
        self.addDirectoryItem('Search', 'furkSearch', 'search.png', 'search.png')
        self.endDirectory()
   
    def getMenuEnabled(self, menu_title):
        is_enabled = control.setting(menu_title).strip()
        if (is_enabled == '' or is_enabled == 'false'): return False
        return True

# News and Info
    def news_local(self):
            r = open(self.LOCALNEWS)
            compfile = r.read()
            self.showText('Help / Information', compfile)

    def showText(self, heading, text):
        id = 10147
        xbmc.executebuiltin('ActivateWindow(%d)' % id)
        xbmc.sleep(500)
        win = xbmcgui.Window(id)
        retry = 50
        while (retry > 0):
            try:
                xbmc.sleep(10)
                retry -= 1
                win.getControl(1).setLabel(heading)
                win.getControl(5).setText(text)
                quit()
                return
            except: pass

    def movies(self, lite=False):
        if self.getMenuEnabled('navi.actor') == True:
            self.addDirectoryItem('Actor Collections', 'collectionActors', 'boxsets.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.boxsets') == True:
            self.addDirectoryItem('Boxset Collections', 'collectionBoxset', 'boxsets.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.xmas') == True:
            self.addDirectoryItem('Christmas Collections', 'collections&url=xmasmovies', 'boxsets.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.kids') == True:
            self.addDirectoryItem('Kids Collections', 'collectionKids', 'boxsets.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.superhero') == True:
            self.addDirectoryItem('Superhero Collections', 'collectionSuperhero', 'boxsets.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.car') == True:
            self.addDirectoryItem('Car Movie Collections', 'collections&url=carmovies', 'boxsets.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.fiftys') == True:
            self.addDirectoryItem('50s Movies 1950 - 1959', 'movies&url=fiftys', 'years.png', 'DefaultRecentlyAddedMovies.png')
        if self.getMenuEnabled('navi.sixtys') == True:
            self.addDirectoryItem('60s Movies 1960 - 1969', 'movies&url=sixtys', 'years.png', 'DefaultRecentlyAddedMovies.png')
        if self.getMenuEnabled('navi.seventys') == True:
            self.addDirectoryItem('70s Movies 1970 - 1979', 'movies&url=seventys', 'years.png', 'DefaultRecentlyAddedMovies.png')
        if self.getMenuEnabled('navi.eightys') == True:
            self.addDirectoryItem('80s Movies 1980 - 1989', 'movies&url=eightys', 'years.png', 'DefaultRecentlyAddedMovies.png')
        if self.getMenuEnabled('navi.ninetys') == True:
            self.addDirectoryItem('90s Movies 1990 - 1999', 'movies&url=ninetys', 'years.png', 'DefaultRecentlyAddedMovies.png')
        if self.getMenuEnabled('navi.moviegenre') == True:
            self.addDirectoryItem(32011, 'movieGenres', 'genres.png', 'DefaultMovies.png')
        #if self.getMenuEnabled('navi.movieyears') == True:
            #self.addDirectoryItem(32012, 'movieYears', 'years.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.moviepersons') == True:
            self.addDirectoryItem(32013, 'moviePersons', 'people.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.movielanguages') == True:
            self.addDirectoryItem(32014, 'movieLanguages', 'languages.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.moviecerts') == True:
            self.addDirectoryItem(32015, 'movieCertificates', 'certificates.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.movietrending') == True:
            self.addDirectoryItem(32017, 'movies&url=trending', 'people-watching.png', 'DefaultRecentlyAddedMovies.png')
        if self.getMenuEnabled('navi.moviepopular') == True:
            self.addDirectoryItem(32018, 'movies&url=popular', 'most-popular.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.movieviews') == True:
            self.addDirectoryItem(32019, 'movies&url=views', 'most-voted.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.movieboxoffice') == True:
            self.addDirectoryItem(32020, 'movies&url=boxoffice', 'box-office.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.movieoscars') == True:
            self.addDirectoryItem(32021, 'movies&url=oscars', 'oscar-winners.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.movietheaters') == True:
            self.addDirectoryItem(32022, 'movies&url=theaters', 'in-theaters.png', 'DefaultRecentlyAddedMovies.png')
        if self.getMenuEnabled('navi.moviewidget') == True:
            self.addDirectoryItem(32005, 'movieWidget', 'latest-movies.png', 'DefaultRecentlyAddedMovies.png')

        if lite == False:
            if not control.setting('lists.widget') == '0':
                self.addDirectoryItem(32003, 'mymovieliteNavigator', 'mymovies.png', 'DefaultVideoPlaylists.png')

            self.addDirectoryItem(32028, 'moviePerson', 'people-search.png', 'DefaultMovies.png')
            self.addDirectoryItem(32010, 'movieSearch', 'search.png', 'DefaultMovies.png')

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
        if self.getMenuEnabled('navi.tvGenres') == True:
            self.addDirectoryItem(32011, 'tvGenres', 'genres.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.tvNetworks') == True:
            self.addDirectoryItem(32016, 'tvNetworks', 'networks.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.tvLanguages') == True:
            self.addDirectoryItem(32014, 'tvLanguages', 'languages.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.tvCertificates') == True:
            self.addDirectoryItem(32015, 'tvCertificates', 'certificates.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.tvTrending') == True:
            self.addDirectoryItem(32017, 'tvshows&url=trending', 'people-watching.png', 'DefaultRecentlyAddedEpisodes.png')
        if self.getMenuEnabled('navi.tvPopular') == True:
            self.addDirectoryItem(32018, 'tvshows&url=popular', 'most-popular.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.tvRating') == True:
            self.addDirectoryItem(32023, 'tvshows&url=rating', 'highly-rated.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.tvViews') == True:
            self.addDirectoryItem(32019, 'tvshows&url=views', 'most-voted.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.tvAiring') == True:
            self.addDirectoryItem(32024, 'tvshows&url=airing', 'airing-today.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.tvActive') == True:
            self.addDirectoryItem(32025, 'tvshows&url=active', 'returning-tvshows.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.tvPremier') == True:
            self.addDirectoryItem(32026, 'tvshows&url=premiere', 'new-tvshows.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.tvAdded') == True:
            self.addDirectoryItem(32006, 'calendar&url=added', 'latest-episodes.png', 'DefaultRecentlyAddedEpisodes.png', queue=True)
        if self.getMenuEnabled('navi.tvCalendar') == True:
            self.addDirectoryItem(32027, 'calendars', 'calendar.png', 'DefaultRecentlyAddedEpisodes.png')

        if lite == False:
            if not control.setting('lists.widget') == '0':
                self.addDirectoryItem(32004, 'mytvliteNavigator', 'mytvshows.png', 'DefaultVideoPlaylists.png')

            self.addDirectoryItem(32028, 'tvPerson', 'people-search.png', 'DefaultTVShows.png')
            self.addDirectoryItem(32010, 'tvSearch', 'search.png', 'DefaultTVShows.png')

        self.endDirectory()

    def mytvshows(self, lite=False):
        try:
            self.accountCheck()

            if traktCredentials == True and imdbCredentials == True:

                self.addDirectoryItem(32032, 'tvshows&url=traktcollection', 'trakt.png', 'DefaultTVShows.png', context=(32551, 'tvshowsToLibrary&url=traktcollection'))
                self.addDirectoryItem(32033, 'tvshows&url=traktwatchlist', 'trakt.png', 'DefaultTVShows.png', context=(32551, 'tvshowsToLibrary&url=traktwatchlist'))
                self.addDirectoryItem(32034, 'tvshows&url=imdbwatchlist', 'imdb.png', 'DefaultTVShows.png')

            elif traktCredentials == True:
                self.addDirectoryItem("Trakt On Deck", 'calendar&url=onDeck', 'trakt.png', 'DefaultTVShows.png')
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
        except:
            print("ERROR")


    def tools(self):
        self.addDirectoryItem(32043, 'openSettings&query=0.0', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32044, 'openSettings&query=4.1', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32628, 'openSettings&query=1.0', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32045, 'openSettings&query=2.0', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32046, 'openSettings&query=7.0', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32047, 'openSettings&query=3.0', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32048, 'openSettings&query=6.0', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32556, 'libraryNavigator', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32049, 'viewsNavigator', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem('Cache Functions', 'cfNavigator', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32073, 'authTrakt', 'trakt.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32539, 'smuSettings', 'urlresolver.png', 'DefaultAddonProgram.png')

        self.endDirectory()

    def cf(self):
        self.addDirectoryItem(32050, 'clearSources', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32604, 'clearCacheSearch', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32052, 'clearCache', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32614, 'clearMetaCache', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32613, 'clearAllCache', 'tools.png', 'DefaultAddonProgram.png')

        self.endDirectory()

    def library(self):
        self.addDirectoryItem(32557, 'openSettings&query=5.0', 'tools.png', 'DefaultAddonProgram.png')
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
            control.infoDialog('', control.lang(32074).encode('utf-8'), time=5000, sound=False)
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

    def clearCacheMeta(self):
        control.idle()
        yes = control.yesnoDialog(control.lang(32056).encode('utf-8'), '', '')
        if not yes: return
        from resources.lib.modules import cache
        cache.cache_clear_meta()
        control.infoDialog(control.lang(32057).encode('utf-8'), sound=True, icon='INFO')

    def clearCacheProviders(self):
        control.idle()
        yes = control.yesnoDialog(control.lang(32056).encode('utf-8'), '', '')
        if not yes: return
        from resources.lib.modules import cache
        cache.cache_clear_providers()
        control.infoDialog(control.lang(32057).encode('utf-8'), sound=True, icon='INFO')

    def clearCacheSearch(self):
        control.idle()
        if control.yesnoDialog(control.lang(32056).encode('utf-8'), '', ''):
            control.setSetting('tvsearch', '')
            control.setSetting('moviesearch', '')
            control.infoDialog(control.lang(32057).encode('utf-8'), sound=True, icon='INFO')

    def clearCacheAll(self):
        control.idle()
        yes = control.yesnoDialog(control.lang(32056).encode('utf-8'), '', '')
        if not yes: return
        from resources.lib.modules import cache
        cache.cache_clear_all()
        control.infoDialog(control.lang(32057).encode('utf-8'), sound=True, icon='INFO')

    def addDirectoryItem(self, name, query, thumb, icon, context=None, queue=False, isAction=True, isFolder=True):
        try: name = control.lang(name).encode('utf-8')
        except: pass
        url = '%s?action=%s' % (sysaddon, query) if isAction == True else query
        thumb = os.path.join(artPath, thumb) if not artPath == None else icon
        cm = []
        cm.append(('13Clowns Settings', 'RunPlugin(%s?action=openSettings&query=(0,0))' % sysaddon))
        if queue == True: cm.append((queueMenu, 'RunPlugin(%s?action=queueItem)' % sysaddon))
        if not context == None: cm.append((control.lang(context[0]).encode('utf-8'), 'RunPlugin(%s?action=%s)' % (sysaddon, context[1])))
        item = control.item(label=name)
        item.addContextMenuItems(cm)
        item.setArt({'icon': thumb, 'thumb': thumb})
        if not addonFanart == None: item.setProperty('Fanart_Image', addonFanart)
        control.addItem(handle=syshandle, url=url, listitem=item, isFolder=isFolder)

    def collectionActors(self):
        self.addDirectoryItem('[COLOR white][B]Adam Sandler[/B][/COLOR]', 'collections&url=adamsandler', 'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[COLOR white][B]Al Pacino[/B][/COLOR]', 'collections&url=alpacino', 'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[COLOR white][B]Alan Rickman[/B][/COLOR]', 'collections&url=alanrickman', 'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[COLOR white][B]Anthony Hopkins[/B][/COLOR]', 'collections&url=anthonyhopkins', 'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[COLOR white][B]Angelina Jolie[/B][/COLOR]', 'collections&url=angelinajolie', 'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[COLOR white][B]Arnold Schwarzenegger[/B][/COLOR]', 'collections&url=arnoldschwarzenegger', 'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[COLOR white][B]Charlize Theron[/B][/COLOR]', 'collections&url=charlizetheron', 'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[COLOR white][B]Clint Eastwood[/B][/COLOR]', 'collections&url=clinteastwood', 'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[COLOR white][B]Demi Moore[/B][/COLOR]', 'collections&url=demimoore', 'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[COLOR white][B]Denzel Washington[/B][/COLOR]', 'collections&url=denzelwashington', 'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[COLOR white][B]Eddie Murphy[/B][/COLOR]', 'collections&url=eddiemurphy', 'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[COLOR white][B]Elvis Presley[/B][/COLOR]', 'collections&url=elvispresley', 'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[COLOR white][B]Gene Wilder[/B][/COLOR]', 'collections&url=genewilder', 'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[COLOR white][B]Gerard Butler[/B][/COLOR]', 'collections&url=gerardbutler', 'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[COLOR white][B]Goldie Hawn[/B][/COLOR]', 'collections&url=goldiehawn', 'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[COLOR white][B]Jason Statham[/B][/COLOR]', 'collections&url=jasonstatham', 'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[COLOR white][B]Jean-Claude Van Damme[/B][/COLOR]', 'collections&url=jeanclaudevandamme', 'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[COLOR white][B]Jeffrey Dean Morgan[/B][/COLOR]', 'collections&url=jeffreydeanmorgan', 'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[COLOR white][B]John Travolta[/B][/COLOR]', 'collections&url=johntravolta', 'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[COLOR white][B]Johnny Depp[/B][/COLOR]', 'collections&url=johnnydepp', 'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[COLOR white][B]Julia Roberts[/B][/COLOR]', 'collections&url=juliaroberts', 'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[COLOR white][B]Kevin Costner[/B][/COLOR]', 'collections&url=kevincostner', 'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[COLOR white][B]Liam Neeson[/B][/COLOR]', 'collections&url=liamneeson', 'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[COLOR white][B]Mel Gibson[/B][/COLOR]', 'collections&url=melgibson', 'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[COLOR white][B]Melissa McCarthy[/B][/COLOR]', 'collections&url=melissamccarthy', 'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[COLOR white][B]Meryl Streep[/B][/COLOR]', 'collections&url=merylstreep', 'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[COLOR white][B]Michelle Pfeiffer[/B][/COLOR]', 'collections&url=michellepfeiffer', 'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[COLOR white][B]Nicolas Cage[/B][/COLOR]', 'collections&url=nicolascage', 'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[COLOR white][B]Nicole Kidman[/B][/COLOR]', 'collections&url=nicolekidman', 'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[COLOR white][B]Paul Newman[/B][/COLOR]', 'collections&url=paulnewman', 'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[COLOR white][B]Reese Witherspoon[/B][/COLOR]', 'collections&url=reesewitherspoon', 'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[COLOR white][B]Robert De Niro[/B][/COLOR]', 'collections&url=robertdeniro', 'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[COLOR white][B]Samuel L Jackson[/B][/COLOR]', 'collections&url=samueljackson', 'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[COLOR white][B]Sean Connery[/B][/COLOR]', 'collections&url=seanconnery', 'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[COLOR white][B]Scarlett Johansson[/B][/COLOR]', 'collections&url=scarlettjohansson', 'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[COLOR white][B]Sharon Stone[/B][/COLOR]', 'collections&url=sharonstone', 'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[COLOR white][B]Sigourney Weaver[/B][/COLOR]', 'collections&url=sigourneyweaver', 'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[COLOR white][B]Steven Seagal[/B][/COLOR]', 'collections&url=stevenseagal', 'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[COLOR white][B]Tom Hanks[/B][/COLOR]', 'collections&url=tomhanks', 'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[COLOR white][B]Vin Diesel[/B][/COLOR]', 'collections&url=vindiesel', 'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[COLOR white][B]Wesley Snipes[/B][/COLOR]', 'collections&url=wesleysnipes', 'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[COLOR white][B]Will Smith[/B][/COLOR]', 'collections&url=willsmith', 'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('[COLOR white][B]Winona Ryder[/B][/COLOR]', 'collections&url=winonaryder', 'collectionactors.png', 'DefaultRecentlyAddedMovies.png')

        self.endDirectory()  

    def collectionBoxset(self):
        self.addDirectoryItem('48 Hrs. (1982-1990)', 'collections&url=fortyeighthours', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Ace Ventura (1994-1995)', 'collections&url=aceventura', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Airplane (1980-1982)', 'collections&url=airplane', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Airport (1970-1979)', 'collections&url=airport', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('American Graffiti (1973-1979)', 'collections&url=americangraffiti', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Anaconda (1997-2004)', 'collections&url=anaconda', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Analyze This (1999-2002)', 'collections&url=analyzethis', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Anchorman (2004-2013)', 'collections&url=anchorman', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Austin Powers (1997-2002)', 'collections&url=austinpowers', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Back to the Future (1985-1990)', 'collections&url=backtothefuture', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Bad Boys (1995-2003)', 'collections&url=badboys', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Bad Santa (2003-2016)', 'collections&url=badsanta', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Basic Instinct (1992-2006)', 'collections&url=basicinstinct', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Beverly Hills Cop (1984-1994)', 'collections&url=beverlyhillscop', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Big Mommas House (2000-2011)', 'collections&url=bigmommashouse', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Blues Brothers (1980-1998)', 'collections&url=bluesbrothers', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Bourne (2002-2016)', 'collections&url=bourne', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Bruce Almighty (2003-2007)', 'collections&url=brucealmighty', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Caddyshack (1980-1988)', 'collections&url=caddyshack', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Cheaper by the Dozen (2003-2005)', 'collections&url=cheaperbythedozen', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Cheech and Chong (1978-1984)', 'collections&url=cheechandchong', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Childs Play (1988-2004)', 'collections&url=childsplay', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('City Slickers (1991-1994)', 'collections&url=cityslickers', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Conan (1982-2011)', 'collections&url=conan', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Crank (2006-2009)', 'collections&url=crank', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Crocodile Dundee (1986-2001)', 'collections&url=crodiledunde', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Da Vinci Code (2006-2017)', 'collections&url=davincicode', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Daddy Day Care (2003-2007)', 'collections&url=daddydaycare', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Death Wish (1974-1994)', 'collections&url=deathwish', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Delta Force (1986-1990)', 'collections&url=deltaforce', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Die Hard (1988-2013)', 'collections&url=diehard', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Dirty Dancing (1987-2004)', 'collections&url=dirtydancing', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Dirty Harry (1971-1988)', 'collections&url=dirtyharry', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Dumb and Dumber (1994-2014)', 'collections&url=dumbanddumber', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Escape from New York (1981-1996)', 'collections&url=escapefromnewyork', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Every Which Way But Loose (1978-1980)', 'collections&url=everywhichwaybutloose', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Exorcist (1973-2005)', 'collections&url=exorcist', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('The Expendables (2010-2014)', 'collections&url=theexpendables', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Fast and the Furious (2001-2017)', 'collections&url=fastandthefurious', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Father of the Bride (1991-1995)', 'collections&url=fatherofthebride', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Fletch (1985-1989)', 'collections&url=fletch', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Friday (1995-2002)', 'collections&url=friday', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Friday the 13th (1980-2009)', 'collections&url=fridaythe13th', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Fugitive (1993-1998)', 'collections&url=fugitive', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('G.I. Joe (2009-2013)', 'collections&url=gijoe', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Get Shorty (1995-2005)', 'collections&url=getshorty', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Gettysburg (1993-2003)', 'collections&url=gettysburg', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Ghost Rider (2007-2011)', 'collections&url=ghostrider', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Ghostbusters (1984-2016)', 'collections&url=ghostbusters', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Gods Not Dead (2014-2016)', 'collections&url=godsnotdead', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Godfather (1972-1990)', 'collections&url=godfather', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Godzilla (1956-2016)', 'collections&url=godzilla', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Grown Ups (2010-2013)', 'collections&url=grownups', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Grumpy Old Men (2010-2013)', 'collections&url=grumpyoldmen', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Guns of Navarone (1961-1978)', 'collections&url=gunsofnavarone', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Halloween (1978-2009)', 'collections&url=halloween', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Hangover (2009-2013)', 'collections&url=hangover', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Hannibal Lector (1986-2007)', 'collections&url=hanniballector', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Hellraiser (1987-1996)', 'collections&url=hellraiser', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Honey I Shrunk the Kids (1989-1995)', 'collections&url=honeyishrunkthekids', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Horrible Bosses (2011-2014)', 'collections&url=horriblebosses', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Hostel (2005-2011)', 'collections&url=hostel', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Hot Shots (1991-1996)', 'collections&url=hotshots', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Independence Day (1996-2016)', 'collections&url=independenceday', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Indiana Jones (1981-2008)', 'collections&url=indianajones', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Insidious (2010-2015)', 'collections&url=insidious', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Iron Eagle (1986-1992)', 'collections&url=ironeagle', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Jack Reacher (2012-2016)', 'collections&url=jackreacher', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Jack Ryan (1990-2014)', 'collections&url=jackryan', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Jackass (2002-2013)', 'collections&url=jackass', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('James Bond (1963-2015)', 'collections&url=jamesbond', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Jaws (1975-1987)', 'collections&url=jaws', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Jeepers Creepers (2001-2017)', 'collections&url=jeeperscreepers', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('John Wick (2014-2017)', 'collections&url=johnwick', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Jumanji (1995-2005)', 'collections&url=jumanji', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Jurassic Park (1993-2015)', 'collections&url=jurassicpark', 'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Kick-Ass (2010-2013)', 'collections&url=kickass', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Kill Bill (2003-2004)', 'collections&url=killbill', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('King Kong (1933-2016)', 'collections&url=kingkong', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Lara Croft (2001-2003)', 'collections&url=laracroft', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Legally Blonde (2001-2003)', 'collections&url=legallyblonde', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Lethal Weapon (1987-1998)', 'collections&url=leathalweapon', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Look Whos Talking (1989-1993)', 'collections&url=lookwhostalking', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Machete (2010-2013)', 'collections&url=machete', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Magic Mike (2012-2015)', 'collections&url=magicmike', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Major League (1989-1998)', 'collections&url=majorleague', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Man from Snowy River (1982-1988)', 'collections&url=manfromsnowyriver', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Mask (1994-2005)', 'collections&url=mask', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Matrix (1999-2003)', 'collections&url=matrix', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('The Mechanic (2011-2016)', 'collections&url=themechanic', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Meet the Parents (2000-2010)', 'collections&url=meettheparents', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Men in Black (1997-2012)', 'collections&url=meninblack', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Mighty Ducks (1995-1996)', 'collections&url=mightyducks', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Miss Congeniality (2000-2005)', 'collections&url=misscongeniality', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Missing in Action (1984-1988)', 'collections&url=missinginaction', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Mission Impossible (1996-2015)', 'collections&url=missionimpossible', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Naked Gun (1988-1994)', 'collections&url=nakedgun', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('National Lampoon (1978-2006)', 'collections&url=nationallampoon', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('National Lampoons Vacation (1983-2015)', 'collections&url=nationallampoonsvacation', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('National Treasure (2004-2007)', 'collections&url=nationaltreasure', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Neighbors (2014-2016)', 'collections&url=neighbors', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Night at the Museum (2006-2014)', 'collections&url=nightatthemuseum', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Nightmare on Elm Street (1984-2010)', 'collections&url=nightmareonelmstreet', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Now You See Me (2013-2016)', 'collections&url=nowyouseeme', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Nutty Professor (1996-2000)', 'collections&url=nuttyprofessor', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Oceans Eleven (2001-2007)', 'collections&url=oceanseleven', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Odd Couple (1968-1998)', 'collections&url=oddcouple', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Oh, God (1977-1984)', 'collections&url=ohgod', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Olympus Has Fallen (2013-2016)', 'collections&url=olympushasfallen', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Omen (1976-1981)', 'collections&url=omen', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Paul Blart Mall Cop (2009-2015)', 'collections&url=paulblart', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Pirates of the Caribbean (2003-2017)', 'collections&url=piratesofthecaribbean', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Planet of the Apes (1968-2014)', 'collections&url=planetoftheapes', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Police Academy (1984-1994)', 'collections&url=policeacademy', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Poltergeist (1982-1988)', 'collections&url=postergeist', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Porkys (1981-1985)', 'collections&url=porkys', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Predator (1987-2010)', 'collections&url=predator', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('The Purge (2013-2016)', 'collections&url=thepurge', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Rambo (1982-2008)', 'collections&url=rambo', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('RED (2010-2013)', 'collections&url=red', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Revenge of the Nerds (1984-1987)', 'collections&url=revengeofthenerds', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Riddick (2000-2013)', 'collections&url=riddick', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Ride Along (2014-2016)', 'collections&url=ridealong', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('The Ring (2002-2017)', 'collections&url=thering', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('RoboCop (1987-1993)', 'collections&url=robocop', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Rocky (1976-2015)', 'collections&url=rocky', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Romancing the Stone (1984-1985)', 'collections&url=romancingthestone', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Rush Hour (1998-2007)', 'collections&url=rushhour', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Santa Clause (1994-2006)', 'collections&url=santaclause', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Saw (2004-2010)', 'collections&url=saw', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Sex and the City (2008-2010)', 'collections&url=sexandthecity', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Shaft (1971-2000)', 'collections&url=shaft', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Shanghai Noon (2000-2003)', 'collections&url=shanghainoon', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Sin City (2005-2014)', 'collections&url=sincity', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Sinister (2012-2015)', 'collections&url=sinister', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Sister Act (1995-1993)', 'collections&url=sisteract', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Smokey and the Bandit (1977-1986)', 'collections&url=smokeyandthebandit', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Speed (1994-1997)', 'collections&url=speed', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Stakeout (1987-1993)', 'collections&url=stakeout', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Star Trek (1979-2016)', 'collections&url=startrek', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Star Wars (1977-2015)', 'collections&url=starwars', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('The Sting (1973-1983)', 'collections&url=thesting', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Taken (2008-2014)', 'collections&url=taken', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Taxi (1998-2007)', 'collections&url=taxi', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Ted (2012-2015)', 'collections&url=ted', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Teen Wolf (1985-1987)', 'collections&url=teenwolf', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Terminator (1984-2015)', 'collections&url=terminator', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Terms of Endearment (1983-1996)', 'collections&url=termsofendearment', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Texas Chainsaw Massacre (1974-2013)', 'collections&url=texaschainsawmassacre', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('The Thing (1982-2011)', 'collections&url=thething', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Thomas Crown Affair (1968-1999)', 'collections&url=thomascrownaffair', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Transporter (2002-2015)', 'collections&url=transporter', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Under Siege (1992-1995)', 'collections&url=undersiege', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Universal Soldier (1992-2012)', 'collections&url=universalsoldier', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Wall Street (1987-2010)', 'collections&url=wallstreet', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Waynes World (1992-1993)', 'collections&url=waynesworld', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Weekend at Bernies (1989-1993)', 'collections&url=weekendatbernies', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Whole Nine Yards (2000-2004)', 'collections&url=wholenineyards', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('X-Files (1998-2008)', 'collections&url=xfiles', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('xXx (2002-2005)', 'collections&url=xxx', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Young Guns (1988-1990)', 'collections&url=youngguns', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Zoolander (2001-2016)', 'collections&url=zoolander', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Zorro (1998-2005)', 'collections&url=zorro', 'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')

        self.endDirectory()


    def collectionKids(self):
        self.addDirectoryItem('Disney Collection', 'collections&url=disneymovies', 'collectiondisney.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Kids Boxset Collection', 'collectionBoxsetKids', 'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Kids Movie Collection', 'collections&url=kidsmovies', 'collectionkids.png', 'DefaultRecentlyAddedMovies.png')

        self.endDirectory()

    def collectionBoxsetKids(self):
        self.addDirectoryItem('101 Dalmations (1961-2003)', 'collections&url=onehundredonedalmations', 'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Addams Family (1991-1998)', 'collections&url=addamsfamily', 'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Aladdin (1992-1996)', 'collections&url=aladdin', 'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Alvin and the Chipmunks (2007-2015)', 'collections&url=alvinandthechipmunks', 'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Atlantis (2001-2003)', 'collections&url=atlantis', 'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Babe (1995-1998)', 'collections&url=babe', 'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Balto (1995-1998)', 'collections&url=balto', 'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Bambi (1942-2006)', 'collections&url=bambi', 'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Beauty and the Beast (1991-2017)', 'collections&url=beautyandthebeast', 'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Beethoven (1992-2014)', 'collections&url=beethoven', 'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Brother Bear (2003-2006)', 'collections&url=brotherbear', 'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Cars (2006-2017)', 'collections&url=cars', 'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Cinderella (1950-2007)', 'collections&url=cinderella', 'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Cloudy With a Chance of Meatballs (2009-2013)', 'collections&url=cloudywithachanceofmeatballs', 'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Despicable Me (2010-2015)', 'collections&url=despicableme', 'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Finding Nemo (2003-2016)', 'collections&url=findingnemo', 'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Fox and the Hound (1981-2006)', 'collections&url=foxandthehound', 'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Free Willy (1993-2010)', 'collections&url=freewilly', 'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Ghostbusters (1984-2016)', 'collections&url=ghostbusters', 'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Gremlins (1984-2016)', 'collections&url=gremlins', 'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Happy Feet (2006-2011)', 'collections&url=happyfeet', 'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Harry Potter (2001-2011)', 'collections&url=harrypotter', 'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Home Alone (1990-2012)', 'collections&url=homealone', 'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Homeward Bound (1993-1996)', 'collections&url=homewardbound', 'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Honey, I Shrunk the Kids (1989-1997)', 'collections&url=honeyishrunkthekids', 'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Hotel Transylvania (2012-2015)', 'collections&url=hoteltransylvania', 'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('How to Train Your Dragon (2010-2014)', 'collections&url=howtotrainyourdragon', 'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Hunchback of Notre Dame (1996-2002)', 'collections&url=hunchbackofnotredame', 'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Ice Age (2002-2016)', 'collections&url=iceage', 'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Jurassic Park (1993-2015)', 'collections&url=jurassicpark', 'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Kung Fu Panda (2008-2016)', 'collections&url=kungfupanda', 'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Lady and the Tramp (1955-2001)', 'collections&url=ladyandthetramp', 'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Lilo and Stitch (2002-2006)', 'collections&url=liloandstitch', 'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Madagascar (2005-2014)', 'collections&url=madagascar', 'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Monsters Inc (2001-2013)', 'collections&url=monstersinc', 'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Mulan (1998-2004)', 'collections&url=mulan', 'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Narnia (2005-2010)', 'collections&url=narnia', 'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('New Groove (2000-2005)', 'collections&url=newgroove', 'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Open Season (2006-2015)', 'collections&url=openseason', 'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Planes (2013-2014)', 'collections&url=planes', 'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Pocahontas (1995-1998)', 'collections&url=pocahontas', 'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Problem Child (1990-1995)', 'collections&url=problemchild', 'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Rio (2011-2014)', 'collections&url=rio', 'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Sammys Adventures (2010-2012)', 'collections&url=sammysadventures', 'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Scooby-Doo (2002-2014)', 'collections&url=scoobydoo', 'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Short Circuit (1986-1988)', 'collections&url=shortcircuit', 'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Shrek (2001-2011)', 'collections&url=shrek', 'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('SpongeBob SquarePants (2004-2017)', 'collections&url=spongebobsquarepants', 'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Spy Kids (2001-2011)', 'collections&url=spykids', 'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Star Wars (1977-2015)', 'collections&url=starwars', 'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Stuart Little (1999-2002)', 'collections&url=stuartlittle', 'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Tarzan (1999-2016)', 'collections&url=tarzan', 'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Teenage Mutant Ninja Turtles (1978-2009)', 'collections&url=teenagemutantninjaturtles', 'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('The Jungle Book (1967-2003)', 'collections&url=thejunglebook', 'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('The Karate Kid (1984-2010)', 'collections&url=thekaratekid', 'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('The Lion King (1994-2016)', 'collections&url=thelionking', 'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('The Little Mermaid (1989-1995)', 'collections&url=thelittlemermaid', 'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('The Neverending Story (1984-1994)', 'collections&url=theneverendingstory', 'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('The Smurfs (2011-2013)', 'collections&url=thesmurfs', 'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Tooth Fairy (2010-2012)', 'collections&url=toothfairy', 'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Tinker Bell (2008-2014)', 'collections&url=tinkerbell', 'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Tom and Jerry (1992-2013)', 'collections&url=tomandjerry', 'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Toy Story (1995-2014)', 'collections&url=toystory', 'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('VeggieTales (2002-2008)', 'collections&url=veggietales', 'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Winnie the Pooh (2000-2005)', 'collections&url=winniethepooh', 'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Wizard of Oz (1939-2013)', 'collections&url=wizardofoz', 'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')

        self.endDirectory()


    def collectionSuperhero(self):
        self.addDirectoryItem('Avengers (2008-2017)', 'collections&url=avengers', 'collectionsuperhero.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Batman (1989-2016)', 'collections&url=batman', 'collectionsuperhero.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Captain America (2011-2016)', 'collections&url=captainamerica', 'collectionsuperhero.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Dark Knight Trilogy (2005-2013)', 'collections&url=darkknight', 'collectionsuperhero.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Fantastic Four (2005-2015)', 'collections&url=fantasticfour', 'collectionsuperhero.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Hulk (2003-2008)', 'collections&url=hulk', 'collectionsuperhero.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Iron Man (2008-2013)', 'collections&url=ironman', 'collectionsuperhero.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Spider-Man (2002-2017)', 'collections&url=spiderman', 'collectionsuperhero.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Superman (1978-2016)', 'collections&url=superman', 'collectionsuperhero.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('X-Men (2000-2016)', 'collections&url=xmen', 'collectionsuperhero.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('DC Comics Collection', 'collections&url=dcmovies', 'collectiondc.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Marvel Collection', 'collections&url=marvelmovies', 'collectionmarvel.png', 'DefaultRecentlyAddedMovies.png')
        
        self.endDirectory()


    def endDirectory(self):
        control.content(syshandle, 'addons')
        control.directory(syshandle, cacheToDisc=True)




'''
##########################################################
################NOTES###############################
#self.addDirectoryItem(32010, 'searchNavigator', 'search.png', 'DefaultFolder.png')
'''
