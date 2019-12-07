# coding: utf-8
# Name:        play.py
# Author:      Mancuniancol
# Created on:  28.11.2016
# Licence:     GPL v.3: http://www.gnu.org/copyleft/gpl.html
"""
Collect information for a Video using IMDB ID
"""
import json
import os
import xbmc
import xbmcaddon
import xbmcgui
from re import search
from shutil import rmtree
from urllib import quote_plus

from browser import Browser
from ehp import Html
from storage import Storage


def find_imdb(title=None):
    """
    Get imdb from title
    :param title: title of the video
    :type title: str or None
    :return: imdb id
    """
    imdb = Storage.open('imdb')
    title = title.lower()
    result = imdb.get(title, None)
    if not result:
        url = 'https://www.google.ca/search?q=%s+imdb' % title.replace(' ', '+')
        if Browser.open(url):
            imdb_search = search('(tt[0-9]+)', Browser.content)

            if imdb_search:
                result = imdb_search.group(1)

    imdb[title] = result
    imdb.close()
    return result


class Video:
    """
    Main class
    """
    _episodes_base_url = 'http://m.imdb.com/title/%s/episodes/?season=%s'
    _base_url = 'http://m.imdb.com/title/%s'
    _counter = 0
    _p_dialog = None
    _percent = 0
    imdb_id = None
    thetvdb_id = None
    is_movie = True
    title = None
    year = None
    seasons_episodes = dict()

    def __init__(self):
        pass

    @classmethod
    def _notify(cls, value=0, message=''):
        """
        Progress Background Notification
        :param value: percentage
        :type value: int
        :param message: message to display
        :type message: str
        :return:
        """
        if not cls._p_dialog:
            cls._p_dialog = xbmcgui.DialogProgressBG()
            cls._p_dialog.create('Magnetizer to library', message)

        else:
            cls._percent += value
            if cls._percent > 100:
                cls._percent = 100
            cls._p_dialog.update(cls._percent, message)

    @classmethod
    def _close_notify(cls):
        """
        Close Notification
        :return:
        """
        if cls._p_dialog:
            cls._p_dialog.close()
            xbmc.sleep(100)
            del cls._p_dialog
            cls._p_dialog = None

    @classmethod
    def _read_episodes(cls, season_value='1'):
        """
        Open the m.imdb page in the specific season and return web page content
        :param season_value: season to search
        :type season_value: str
        :return: str with the web page content
        """
        if not cls.imdb_id:
            return '<html></html>'

        url = cls._episodes_base_url % (cls.imdb_id, season_value)
        cls._notify(5, 'Reading episodes')
        Browser.open(url)
        return Browser.content

    @classmethod
    def _read_title_year(cls):
        """
        Get the title and year from the stored imdb_id
        :return: nothing
        """
        url = cls._base_url % cls.imdb_id
        cls._notify(5, 'Getting Title and Year')
        Browser.open(url)
        cls._counter += 1
        dom = Html().feed(Browser.content)
        if not dom:
            return

        title = dom.find_once('h1')()
        cls.title = ' '.join(title.split())
        s = cls.title + '()'
        cls.year = s[s.find("(") + 1:s.find(")")]
        cls.is_movie = 'Episode Guide' not in Browser.content
        if not cls.is_movie:
            cls.thetvdb_id = cls._get_thetvdb_id(cls.imdb_id)
            s = cls.title + '()'
            cls.title = s[:s.find("(") - 1]

    @classmethod
    def _new_info(cls, tv_show=None):
        """
        Parse the web page to get the new episodes and seasons from specific tv_show
        :param tv_show:
        :return:
        """
        if not tv_show:
            tv_show = dict()

        old_seasons = tv_show.keys()
        max_season = str(max(int(x) for x in old_seasons + ['1']))
        html = cls._read_episodes(max_season)
        dom = Html().feed(html)
        seasons = dom.find_all('li', ('class', 'season_box'))
        new_seasons = list()

        for season_tag in seasons:
            new_seasons.append(season_tag(tag='a', attribute='season_number'))

        difference = list(set(new_seasons) - set(old_seasons))
        if max_season not in difference:
            difference.append(max_season)

        # only check last season and new seasons
        for season_tag in seasons:
            season = season_tag(tag='a', attribute='season_number')
            if season in difference:
                tv_show[season] = []
                if not html:
                    html = cls._read_episodes(season)

                dom = Html().feed(html)
                episodes = dom.find_once('div', ('id', 'eplist')).find_all('span', ('class', 'text-large'))
                for episode in episodes:
                    tv_show[season].append(episode().split('.')[0])

                html = None

        return tv_show

    @classmethod
    def _get_thetvdb_id(cls, imdb_id=None):
        """
        Find thetvdb id from imdb_id
        :param imdb_id: imdb of the tv show
        :type imdb_id: str
        :return: thetvdb id
        """
        result = None
        if imdb_id:
            request = 'http://thetvdb.com/api/GetSeriesByRemoteID.php?imdbid=%s' % imdb_id
            cls._notify(5, 'Getting tvthedb id')
            if Browser.open(request):
                s = Browser.content
                result = s[s.find("<seriesid>") + 10:s.find("</seriesid>")]

        return result

    @classmethod
    def _is_new_movie(cls, imdb_id=None):
        """
        Check if the movie exists in Kodi's database
        :param imdb_id: imdb of the movie
        :type imdb_id: str
        :return: bool, True is the movie exists.  False, otherwise.
        """
        cls._notify(5, 'Finding if it is new')
        if not imdb_id:
            return False

        request = {"jsonrpc": "2.0",
                   "method": "VideoLibrary.GetMovies",
                   "id": "libMovies",
                   "params": {
                       "properties": ["title", "imdbnumber", "year"]
                   }}
        movies = json.loads(xbmc.executeJSONRPC(json.dumps(request)))["result"].get("movies", [])
        result = True
        for movie in movies:
            if imdb_id in movie['imdbnumber']:
                result = False
                break

        cls._notify(5, 'New movie' if result else 'No new movie')

        return result

    @classmethod
    def _is_new_episode(cls, thetvdb_id=None, season=None, episode=None):
        """
        Check if the episode exists in Kodi's database
        :param thetvdb_id: imdb of the tv show
        :type thetvdb_id: str
        :param season: number of the season of the episode
        :type season: str
        :param episode: number of the episode
        :type episode: str
        :return: bool, True is the episode exists.  False, otherwise.
        """
        cls._notify(5, 'Finding if it is new')
        if not thetvdb_id or not season or not episode:
            return False

        request = {"jsonrpc": "2.0",
                   "method": "VideoLibrary.GetTVShows",
                   "id": "libTvShows",
                   "params": {
                       "properties": ["title", "imdbnumber"]
                   }}

        tv_shows = json.loads(xbmc.executeJSONRPC(json.dumps(request))).get("result", {}).get("tvshows", [])
        result = True

        for show in tv_shows:
            if thetvdb_id in show['imdbnumber']:
                # Found id show in Kodi database
                tv_show_id = show['tvshowid']
                request = {"jsonrpc": "2.0",
                           "method": "VideoLibrary.GetEpisodes",
                           "id": "1",
                           "params": {"tvshowid": tv_show_id,
                                      "sort": {"method": "episode"},
                                      "filter": {
                                          "and": [{"field": "episode", "operator": "is", "value": episode},
                                                  {"field": "season", "operator": "is", "value": season}]
                                      },
                                      "properties": ["title", "playcount", "season", "episode"],
                                      "limits": {"end": 1}}
                           }
                episodes = json.loads(xbmc.executeJSONRPC(json.dumps(request))).get("result", {}).get("episodes", [])
                result = len(episodes) == 0

        cls._notify(1, 'New episode' if result else 'No new episode')

        return result

    @staticmethod
    def _create_strm(path, clean_title, title, link):
        """
        Create the strm file
        :param path: main path for movie or tv shows
        :type path: str
        :param clean_title: the title of the movie or tv show
        :type clean_title: str
        :param title: title of the movie or episode (S00E00 format)
        :type title: str
        :param link: link to call magnetizer
        :type link: str
        """
        folder = os.path.join(path, clean_title)
        try:
            if not os.path.exists(folder):
                os.makedirs(folder)

            filename = os.path.join(folder, title + '.strm')
            with open(filename, "w") as text_file:
                text_file.write(link)

        except Exception as e:
            print "Error: %s" % repr(e)

    @staticmethod
    def _create_nfo(path, clean_title, video_id=None):
        """
        Create the nfo in the main folder
        :param path: main path for movie or tv shows
        :type path: str
        :param clean_title: the title of the movie or tv show
        :type clean_title: str
        :param video_id: imdb or thetvdb id from video
        :type video_id: str
        :return:
        """
        try:
            if video_id:
                folder = os.path.join(path, clean_title)
                if os.path.exists(folder):
                    if video_id.startswith('tt'):
                        filename = os.path.join(folder, clean_title + '.nfo')
                        with open(filename, "w") as text_file:
                            text_file.write("http://www.imdb.com/title/%s/" % video_id)

                    else:
                        filename = os.path.join(folder, 'tvshow.nfo')
                        with open(filename, "w") as text_file:
                            text_file.write('http://thetvdb.com/?tab=series&id=%s' % video_id)

        except Exception as e:
            print "Error: %s" % repr(e)

    @classmethod
    def info(cls, imdb_id=None):
        """
        Collect title, is_movie, season_episodes and year from video
        :param imdb_id: imdb id from video
        :type imdb_id: str
        :return:
        """
        cls.imdb_id = imdb_id
        if not imdb_id:
            cls._notify(100, 'Not imdb id')
            cls._close_notify()
            return False

        cls._notify(5, 'Gathering information')
        # check the storage
        information = Storage.open('library', ttl=None)
        # continue
        video = information.get(imdb_id, {imdb_id: None})
        if video[imdb_id]:
            cls.title = video[imdb_id]['title']
            cls.is_movie = video[imdb_id]['is_movie']
            cls.year = video[imdb_id]['year']
            cls.thetvdb_id = video[imdb_id]['thetvdb_id']
            cls.seasons_episodes = video[imdb_id]['seasons_episodes']

        else:
            cls._read_title_year()
            video[imdb_id] = dict()
            video[imdb_id]['title'] = cls.title
            video[imdb_id]['is_movie'] = cls.is_movie
            video[imdb_id]['year'] = cls.year
            video[imdb_id]['thetvdb_id'] = cls.thetvdb_id
            video[imdb_id]['seasons_episodes'] = cls.seasons_episodes

        if not cls.is_movie:
            # it needs to update information show
            cls.seasons_episodes = cls._new_info(cls.seasons_episodes)
            video[imdb_id]['seasons_episodes'] = cls.seasons_episodes

        # save in storage
        information[cls.imdb_id] = video
        information.close()
        cls._close_notify()

        return True

    @classmethod
    def add_to_library(cls, imdb_id):
        """
        Add a video to the library
        :param imdb_id: imdb id from video
        :type imdb_id: str
        :return:
        """
        if not imdb_id:
            cls._notify(100, 'Not imdb id')
            cls._close_notify()
            return False

        # if not cls.title:
        #     cls._notify(100, 'Not Title')
        #     cls._close_notify()
        #     return False

        cls.info(imdb_id)
        cls._notify(5, 'Creating strm')
        if cls.is_movie:
            folder = xbmc.translatePath(xbmcaddon.Addon().getSetting('movies_folder'))
            payload = '?search=movie&imdb=%s&title=%s&year=%s' % (imdb_id, quote_plus(cls.title), cls.year)
            link = 'plugin://script.module.magnetic%s' % payload
            if cls._is_new_movie(imdb_id):
                cls._create_strm(folder, cls.title, cls.title, link)
                cls._notify(5, 'Creating nfo')
                cls._create_nfo(folder, cls.title, cls.imdb_id)

        else:
            folder = xbmc.translatePath(xbmcaddon.Addon().getSetting('shows_folder'))
            for season in cls.seasons_episodes:
                for episode in cls.seasons_episodes[season]:
                    episode_title = '%s S%02dE%02d' % (cls.title, int(season), int(episode))
                    payload = '?search=episode&title=%s&season=%s&episode=%s' % (quote_plus(cls.title), season, episode)
                    link = 'plugin://script.module.magnetic%s' % payload
                    if cls._is_new_episode(cls.thetvdb_id, season, episode):
                        cls._create_strm(folder, cls.title, episode_title, link)

            cls._notify(5, 'Creating nfo')
            cls._create_nfo(folder, cls.title, cls.thetvdb_id)

        cls._notify(100, 'Done')
        cls._percent = 0
        cls._close_notify()

        return True

    @classmethod
    def update_subscription(cls):
        """
        Check the list of tv shows and update the strm files
        :return:
        """
        tv_shows = Storage.open('subscriptions', ttl=None)
        for imdb_id in tv_shows:
            cls.add_to_library(imdb_id)

        if not xbmc.getCondVisibility('Library.IsScanningVideo'):
            xbmc.executebuiltin('XBMC.UpdateLibrary(video)')  # update the library with the new information

        tv_shows.close()

    @staticmethod
    def add_subscription(imdb_id):
        """
        Add tv show to the subscription list
        :param imdb_id: imdb id from video
        :type imdb_id: str
        :return: True if succeed. False, otherwise.
        """
        if not imdb_id:
            return False

        tv_shows = Storage.open('subscriptions', ttl=None)
        tv_shows[imdb_id] = 'x'
        tv_shows.close()

        return True

    @staticmethod
    def remove_subscription(imdb_id, remove=True):
        """
        Remove tv show to the subscription list
        :param remove: if the files will be removed or not
        :type remove: bool
        :param imdb_id: imdb id from video
        :type imdb_id: str
        :return: True if succeed. False, otherwise.
        """
        if not imdb_id:
            return False

        tv_shows = Storage.open('subscriptions', ttl=None)
        del tv_shows[imdb_id]
        tv_shows.close()
        if remove:
            folder = xbmc.translatePath(xbmcaddon.Addon().getSetting('shows_folder'))
            if os.path.exists(folder):
                rmtree(folder)

        return True

    @staticmethod
    def is_subscribed(imdb_id):
        """
        Return is the tv show is the subscription list
        :param imdb_id: imdb id from video
        :type imdb_id: str
        :return: True is in the list. False, otherwise.
        """
        if not imdb_id:
            return False

        tv_shows = Storage.open('subscriptions', ttl=None)
        result = imdb_id in tv_shows
        tv_shows.close()

        return result
