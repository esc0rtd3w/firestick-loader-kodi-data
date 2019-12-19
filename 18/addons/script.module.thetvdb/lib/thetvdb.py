#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
    Kodi Helper Module for accessing TheTvDb API
    Includes the most common actions including a few special ones for Kodi use
    Full series and episode data is mapped into Kodi compatible format
'''
import requests
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import xbmc
import xbmcgui
import xbmcaddon
from datetime import timedelta, date
from operator import itemgetter
try:
    import simplejson as json
except ImportError:
    import json
from simplecache import use_cache, SimpleCache
import arrow
import urllib
import re

# set some parameters to the requests module
requests.packages.urllib3.disable_warnings()
SES = requests.Session()
RETRIES = Retry(total=5, backoff_factor=2, status_forcelist=[500, 502, 503, 504])
SES.mount('http://', HTTPAdapter(max_retries=RETRIES))
SES.mount('https://', HTTPAdapter(max_retries=RETRIES))

ADDON_ID = "script.module.thetvdb"
KODI_LANGUAGE = xbmc.getLanguage(xbmc.ISO_639_1)
KODI_VERSION = int(xbmc.getInfoLabel("System.BuildVersion").split(".")[0])
if KODI_VERSION > 16:
    KODI_TV_PROPS = '"file", "title", "year", "imdbnumber", "art", "genre", "cast", "studio", "uniqueid"'
else:
    KODI_TV_PROPS = '"file", "title", "year", "imdbnumber", "art", "genre", "cast", "studio"'
CLASSIFICATION_REGEX = re.compile(
    r"(?:^| \| )(Scripted|Mini-Series|Documentary|Animation|Game Show|Reality|Talk Show|Variety)( \| |$)")


class TheTvDb(object):
    '''Our main class'''
    _win = None
    _addon = None
    _token = None
    cache = None
    api_key = 'A7613F5C1482A540'  # default api key
    days_ahead = 120
    ignore_cache = False
    _close_called = False

    def __init__(self, api_key=None):
        '''Initialize our Module'''
        if api_key:
            self.api_key = api_key
        self.cache = SimpleCache()
        self._win = xbmcgui.Window(10000)
        self._addon = xbmcaddon.Addon(ADDON_ID)
        addonversion = self._addon.getAddonInfo('version').decode("utf-8")
        self.cache.global_checksum = "%s%s" % (addonversion, KODI_LANGUAGE)
        self._log_msg("Initialized")

    def close(self):
        '''Cleanup Kodi cpython classes'''
        self._close_called = True
        self.cache.close()
        del self._win
        del self._addon
        self._log_msg("Exited")

    def __del__(self):
        '''make sure close is called'''
        if not self._close_called:
            self.close()

    def get_data(self, endpoint, prefer_localized=False):
        '''grab the results from the api'''
        data = {}
        url = 'https://api.thetvdb.com/' + endpoint
        headers = {'Content-Type': 'application/json',
                   'Accept': 'application/json',
                   'User-agent': 'Mozilla/5.0', 'Authorization': 'Bearer %s' % self._get_token()}
        if prefer_localized:
            headers["Accept-Language"] = KODI_LANGUAGE
        try:
            response = requests.get(url, headers=headers, timeout=20)
            if response and response.content and response.status_code == 200:
                data = json.loads(response.content.decode('utf-8', 'replace'))
            elif response.status_code == 401:
                # token expired, refresh it and repeat our request
                self._log_msg("Token expired, refreshing...")
                headers['Bearer'] = self._get_token(True)
                response = requests.get(url, headers=headers, timeout=5)
                if response and response.content and response.status_code == 200:
                    data = json.loads(response.content.decode('utf-8', 'replace'))
            if data.get("data"):
                data = data["data"]
        except Exception as exc:
            self._log_msg("Exception in get_data --> %s" % repr(exc), xbmc.LOGERROR)
        return data

    @use_cache(60)
    def get_series_posters(self, seriesid, season=None):
        '''retrieves the URL for the series poster, prefer season poster if season number provided'''
        if season:
            images = self.get_data("series/%s/images/query?keyType=season&subKey=%s" % (seriesid, season))
        else:
            images = self.get_data("series/%s/images/query?keyType=poster" % (seriesid))
        return self.process_images(images)

    @use_cache(60)
    def get_series_fanarts(self, seriesid, landscape=False):
        '''retrieves the URL for the series fanart image'''
        if landscape:
            images = self.get_data("series/%s/images/query?keyType=fanart&subKey=text" % (seriesid))
        else:
            images = self.get_data("series/%s/images/query?keyType=fanart&subKey=graphical" % (seriesid))
        return self.process_images(images)

    @staticmethod
    def process_images(images):
        '''helper to sort and correct the images as the api output is rather messy'''
        result = []
        if images:
            for image in images:
                if image["fileName"] and not image["fileName"].endswith("/"):
                    if image["fileName"].startswith("http://"): 
                        image["fileName"] = image["fileName"].replace("http://", "https://")
                    elif not image["fileName"].startswith("https://"):
                        image["fileName"] = "https://thetvdb.com/banners/" + image["fileName"]
                    image_score = image["ratingsInfo"]["average"] * image["ratingsInfo"]["count"]
                    image["score"] = image_score
                    result.append(image)
        return [item["fileName"] for item in sorted(result, key=itemgetter("score"), reverse=True)]

    @use_cache(7)
    def get_episode(self, episodeid, seriesdetails=None):
        '''
            Returns the full information for a given episode id.
            Usage: specify the episode ID: TheTvDb().get_episode(episodeid)
        '''
        episode = self.get_data("episodes/%s" % episodeid, True)
        # we prefer localized content but if that fails, fallback to default
        if episode and not episode.get("overview"):
            episode = self.get_data("episodes/%s" % episodeid)
        if episode:
            if not seriesdetails and "seriesid" in episode:
                seriesdetails = self.get_series(episode["seriesid"])
            elif not seriesdetails and "seriesId" in episode:
                seriesdetails = self.get_series(episode["seriesId"])
            episode = self._map_episode_data(episode, seriesdetails)
        return episode

    @use_cache(14)
    def get_series(self, seriesid):
        '''
            Returns a series record that contains all information known about a particular series id.
            Usage: specify the serie ID: TheTvDb().get_series(seriesid)
        '''
        seriesinfo = self.get_data("series/%s" % seriesid, True)
        # we prefer localized content but if that fails, fallback to default
        if not seriesinfo.get("overview"):
            seriesinfo = self.get_data("series/%s" % seriesid)
        return self._map_series_data(seriesinfo)

    @use_cache(7)
    def get_series_by_imdb_id(self, imdbid=""):
        '''get full series details by providing an imdbid'''
        items = self.get_data("search/series?imdbId=%s" % imdbid)
        if items:
            return self.get_series(items[0]["id"])
        else:
            return {}

    @use_cache(3)
    def get_continuing_series(self):
        '''
            only gets the continuing series,
            based on which series were recently updated as there is no other api call to get that information
        '''
        recent_series = self.get_recently_updated_series()
        continuing_series = []
        for recent_serie in recent_series:
            seriesinfo = self.get_series(recent_serie["id"])
            if seriesinfo and seriesinfo.get("status", "") == "Continuing":
                continuing_series.append(seriesinfo)
        return continuing_series

    @use_cache(60)
    def get_series_actors(self, seriesid):
        '''
            Returns actors for the given series id.
            Usage: specify the series ID: TheTvDb().get_series_actors(seriesid)
        '''
        return self.get_data("series/%s/actors" % seriesid)

    @use_cache(30)
    def get_series_episodes(self, seriesid):
        '''
            Returns all episodes for a given series.
            Usage: specify the series ID: TheTvDb().get_series_episodes(seriesid)
            Note: output is only summary of episode details (non kodi formatted)
        '''
        all_episodes = []
        page = 1
        while True:
            # get all episodes by iterating over the pages
            data = self.get_data("series/%s/episodes?page=%s" % (seriesid, page))
            if not data:
                break
            else:
                all_episodes += data
                page += 1
        return all_episodes

    @use_cache(14)
    def get_last_season_for_series(self, seriesid):
        '''get the last season for the series'''
        highest_season = 0
        summary = self.get_series_episodes_summary(seriesid)
        if summary:
            for season in summary["airedSeasons"]:
                if int(season) > highest_season:
                    highest_season = int(season)
        return highest_season

    @use_cache(1)
    def get_last_episode_for_series(self, seriesid):
        '''
            Returns the last aired episode for a given series
            Usage: specify the series ID: TheTvDb().get_last_episode_for_series(seriesid)
        '''
        # somehow the absolutenumber is broken in the api so we have to get this info the hard way
        highest_season = self.get_last_season_for_series(seriesid)
        while not highest_season == -1:
            season_episodes = self.get_series_episodes_by_query(seriesid, "airedSeason=%s" % highest_season)
            season_episodes = sorted(season_episodes, key=lambda k: k.get('airedEpisodeNumber', 0), reverse=True)

            highest_eps = (arrow.get("1970-01-01").date(), 0)
            if season_episodes:
                for episode in season_episodes:
                    if episode["firstAired"]:
                        airdate = arrow.get(episode["firstAired"]).date()
                        if (airdate < date.today()) and (airdate > highest_eps[0]):
                            highest_eps = (airdate, episode["id"])
                if highest_eps[1] != 0:
                    return self.get_episode(highest_eps[1])
            # go down one season untill we reach a match (there may be already announced seasons in the seasons list)
            highest_season -= 1
        self._log_msg("No last episodes found for series %s" % seriesid)
        return None

    @use_cache(7)
    def get_series_episodes_by_query(self, seriesid, query=""):
        '''
            This route allows the user to query against episodes for the given series.
            The response is an array of episode records that have been filtered down to basic information.
            Usage: specify the series ID: TheTvDb().get_series_episodes_by_query(seriesid)
            You must specify one or more fields for the query (combine multiple with &):
            absolutenumber=X --> Absolute number of the episode
            airedseason=X --> Aired season number
            airedepisode=X --> Aired episode number
            dvdseason=X --> DVD season number
            dvdepisode=X --> DVD episode number
            imdbid=X --> IMDB id of the series
            Note: output is only summary of episode details (non kodi formatted)
        '''
        all_episodes = []
        page = 1
        while True:
            # get all episodes by iterating over the pages
            data = self.get_data("series/%s/episodes/query?%s&page=%s" % (seriesid, query, page))
            if not data:
                break
            else:
                all_episodes += data
                page += 1
        return all_episodes

    @use_cache(7)
    def get_series_episodes_summary(self, seriesid):
        '''
            Returns a summary of the episodes and seasons available for the series.
            Note: Season 0 is for all episodes that are considered to be specials.

            Usage: specify the series ID: TheTvDb().get_series_episodes_summary(seriesid)
        '''
        return self.get_data("series/%s/episodes/summary" % (seriesid))

    @use_cache(8)
    def search_series(self, query="", prefer_localized=False):
        '''
            Allows the user to search for a series based the name.
            Returns an array of results that match the query.
            Usage: specify the query: TheTvDb().search_series(searchphrase)

            Available parameter:
            prefer_localized --> True if you want to set the current kodi language as preferred in the results
        '''
        return self.get_data("search/series?name=%s" % query, prefer_localized)

    @use_cache(7)
    def get_recently_updated_series(self):
        '''
            Returns all series that have been updated in the last week
        '''
        day = 24 * 60 * 60
        utc_date = date.today() - timedelta(days=7)
        cur_epoch = (utc_date.toordinal() - date(1970, 1, 1).toordinal()) * day
        return self.get_data("updated/query?fromTime=%s" % cur_epoch)

    def get_unaired_episodes(self, seriesid):
        '''
            Returns the unaired episodes for the specified seriesid
            Usage: specify the series ID: TheTvDb().get_unaired_episodes(seriesid)
        '''
        next_episodes = []
        seriesinfo = self.get_series(seriesid)
        if seriesinfo and seriesinfo.get("status", "") == "Continuing":
            highest_season = self.get_last_season_for_series(seriesid)
            episodes = self.get_series_episodes_by_query(seriesid, "airedSeason=%s" % highest_season)
            episodes = sorted(episodes, key=lambda k: k.get('airedEpisodeNumber', 0))
            for episode in episodes:
                if episode["firstAired"] and episode["episodeName"]:
                    airdate = arrow.get(episode["firstAired"]).date()
                    if airdate >= date.today() and (airdate <= (date.today() + timedelta(days=self.days_ahead))):
                        # if airdate is today or (max X days) in the future add to our list
                        episode = self.get_episode(episode["id"], seriesinfo)
                        if episode:  # apparently some episode id's are reported that do not exist
                            next_episodes.append(episode)
        # return our list sorted by episode
        return sorted(next_episodes, key=lambda k: k.get('episode', ""))

    def get_nextaired_episode(self, seriesid):
        '''
            Returns the first next airing episode for the specified seriesid
            Usage: specify the series ID: TheTvDb().get_nextaired_episode(seriesid)
        '''
        next_episodes = self.get_unaired_episodes(seriesid)
        if next_episodes:
            return next_episodes[0]
        else:
            return None

    def get_unaired_episode_list(self, seriesids):
        '''
            Returns the next airing episode for each specified seriesid
            Usage: specify the series ID: TheTvDb().get_unaired_episode_list(list of seriesids)
        '''
        next_episodes = []
        for seriesid in seriesids:
            episodes = self.get_unaired_episodes(seriesid)
            if episodes and episodes[0] is not None:
                next_episodes.append(episodes[0])
        # return our list sorted by date
        return sorted(next_episodes, key=lambda k: k.get('firstAired', ""))

    def get_kodishows(self, continuing_only=False):
        '''
            get all tvshows in the kodi library and make sure we have a valid tvdb id
            returns combined tvshow details
        '''
        kodi_series = self._get_kodi_json('VideoLibrary.GetTvShows', '{"properties": [ %s ] }' % KODI_TV_PROPS)
        all_series = []
        monitor = xbmc.Monitor()
        if kodi_series and kodi_series.get("tvshows"):
            for kodi_serie in kodi_series["tvshows"]:
                if monitor.abortRequested() or self._close_called:
                    break
                tvdb_details = self._parse_kodi_show(kodi_serie)
                if tvdb_details and "tvdb_status" in tvdb_details:
                    if not continuing_only or (continuing_only and tvdb_details["tvdb_status"] == "Continuing"):
                        all_series.append(tvdb_details)
        del monitor
        return all_series

    def get_kodishows_details(self, continuing_only=False):
        '''
            returns full info for each tvshow in the kodi library
            returns both kodi and tvdb info combined, including next-/last episode
        '''
        result = []
        monitor = xbmc.Monitor()
        for series_info in self.get_kodishows(continuing_only=continuing_only):
            if monitor.abortRequested() or self._close_called:
                break
            details = self.get_kodishow_details(series_info["title"], serie_details=series_info)
            if details:
                result.append(series_info)
        del monitor
        return result

    def get_kodishows_airingtoday(self):
        '''
            returns full info for each tvshow in the kodi library that airs today
        '''
        result = []
        monitor = xbmc.Monitor()
        for series_info in self.get_kodishows(continuing_only=True):
            if monitor.abortRequested() or self._close_called:
                break
            details = self.get_kodishow_details(series_info["title"], serie_details=series_info)
            if details and details.get("next_episode"):
                airdate = arrow.get(details["next_episode"]["firstaired"]).date()
                if airdate == date.today():
                    result.append(series_info)
        del monitor
        return sorted(result, key=lambda k: k.get('airtime', ""))

    @use_cache(2)
    def get_kodishow_details(self, title, serie_details=None):
        '''get full details for the kodi serie in library - search by title (as in kodi db)'''
        result = None
        if not serie_details and title:
            # get kodi details by title
            filter_str = '"filter": {"operator": "is", "field": "title", "value": "%s"}' % title
            kodi_series = self._get_kodi_json('VideoLibrary.GetTvShows',
                                              '{"properties": [ %s ], %s }' % (KODI_TV_PROPS, filter_str))
            if kodi_series and kodi_series.get("tvshows"):
                kodi_details = kodi_series["tvshows"][0]
                serie_details = self._parse_kodi_show(kodi_details)
        if serie_details:
            # append next airing episode details
            serie_details["next_episode"] = self.get_nextaired_episode(serie_details["tvdb_id"])
            # append last episode details
            serie_details["last_episode"] = self.get_last_episode_for_series(serie_details["tvdb_id"])
            result = serie_details
        return result

    def get_kodi_unaired_episodes(self, single_episode_per_show=True, include_last_episode=False, tvshows_ids=None):
        '''
            Returns the next unaired episode for all continuing tv shows in the Kodi library
            single_episode_per_show: Only return a single episode (next unaired) for each show, defaults to True.
            include_last_episode: Also include the last aired episode in the listing for each show.
        '''
        kodi_series = self.get_kodishows(True)
        next_episodes = []
        if tvshows_ids:
            kodi_series = [ tvshow for tvshow in kodi_series if tvshow["tvshowid"] in tvshows_ids ]
        for kodi_serie in kodi_series:
            serieid = kodi_serie["tvdb_id"]
            if single_episode_per_show:
                episodes = [self.get_nextaired_episode(serieid)]
            else:
                episodes = self.get_unaired_episodes(serieid)
            if include_last_episode:
                episodes.append(self.get_last_episode_for_series(serieid))
            for next_episode in episodes:
                if next_episode:
                    # make the json output kodi compatible
                    next_episodes.append(self._map_kodi_episode_data(kodi_serie, next_episode))
        # return our list sorted by date
        return sorted(next_episodes, key=lambda k: k.get('firstaired', ""))

    def _map_episode_data(self, episode_details, seriesdetails=None):
        '''maps full episode data from tvdb to kodi compatible format'''
        result = {}
        result["art"] = {}
        if episode_details.get("filename"):
            result["art"]["thumb"] = "https://thetvdb.com/banners/" + episode_details["filename"]
            result["thumbnail"] = result["art"]["thumb"]
        result["title"] = episode_details["episodeName"]
        result["label"] = "%sx%s. %s" % (episode_details["airedSeason"],
                                         episode_details["airedEpisodeNumber"], episode_details["episodeName"])
        result["season"] = episode_details["airedSeason"]
        result["episode"] = episode_details["airedEpisodeNumber"]
        result["firstaired"] = episode_details["firstAired"]
        result["writer"] = episode_details["writers"]
        result["director"] = episode_details["directors"]
        result["gueststars"] = episode_details["guestStars"]
        result["rating"] = episode_details["siteRating"]
        # make sure we have a decimal in the rating
        if len(str(result["rating"])) == 1:
            result["rating"] = "%s.0" % result["rating"]
        result["plot"] = episode_details["overview"]
        result["airdate"] = self._get_local_date(episode_details["firstAired"])
        result["airdate.long"] = self._get_local_date(episode_details["firstAired"], True)
        result["airdate.label"] = "%s (%s)" % (result["label"], result["airdate"])
        result["seriesid"] = episode_details["seriesId"]
        # append seriesinfo to details if provided
        if seriesdetails:
            result["tvshowtitle"] = seriesdetails["title"]
            result["showtitle"] = seriesdetails["title"]
            result["network"] = seriesdetails["network"]
            result["studio"] = seriesdetails["studio"]
            result["genre"] = seriesdetails["genre"]
            result["classification"] = seriesdetails["classification"]
            result["tvshow.firstaired"] = seriesdetails["firstaired"]
            result["tvshow.status"] = seriesdetails["status"]
            result["airtime"] = seriesdetails["airtime"]
            result["airday"] = seriesdetails["airday"]
            result["airday.int"] = seriesdetails["airday.int"]
            result["airdatetime"] = "%s %s" % (result["airdate"], result["airtime"])
            result["airdatetime.label"] = "%s - %s %s" % (result["airdatetime"],
                                                          xbmc.getLocalizedString(145), result["network"])
            result["art"]["tvshow.poster"] = seriesdetails["art"].get("poster", "")
            result["art"]["tvshow.landscape"] = seriesdetails["art"].get("landscape", "")
            result["art"]["tvshow.fanart"] = seriesdetails["art"].get("fanart", "")
            result["art"]["tvshow.banner"] = seriesdetails["art"].get("banner", "")
            try:
                result["runtime"] = int(seriesdetails["runtime"]) * 60
            except Exception:
                pass
            season_posters = self.get_series_posters(episode_details["seriesId"], episode_details["airedSeason"])
            if season_posters:
                result["art"]["season.poster"] = season_posters[0]
            result["library"] = seriesdetails.get("library", "")
            result["file"] = seriesdetails.get("file", "")
            result["year"] = seriesdetails.get("year", "")
        return result

    def _map_kodi_episode_data(self, kodi_tvshow_details, episode_details):
        '''combine kodi tvshow details with tvdb episode details'''
        result = episode_details
        # add images from kodi series details
        for key, value in kodi_tvshow_details["art"].items():
            result["art"]["tvshow.%s" % key] = self._get_clean_image(value)
        result["art"]["season.poster"] = episode_details.get("season.poster", "")
        result["tvshowtitle"] = kodi_tvshow_details["title"]
        result["showtitle"] = kodi_tvshow_details["title"]
        result["studio"] = kodi_tvshow_details["studio"]
        result["genre"] = kodi_tvshow_details["genre"]
        result["cast"] = kodi_tvshow_details["cast"]
        result["kodi_tvshowid"] = kodi_tvshow_details["tvshowid"]
        result["episodeid"] = -1
        result["file"] = "videodb://tvshows/titles/%s/" % kodi_tvshow_details["tvshowid"]
        result["type"] = "episode"
        result["DBTYPE"] = "episode"
        result["isFolder"] = True
        return result

    def _map_series_data(self, showdetails):
        '''maps the tvdb data to more kodi compatible format'''
        result = {}
        if showdetails:
            result["title"] = showdetails["seriesName"]
            result["status"] = showdetails["status"]
            result["tvdb_status"] = showdetails["status"]
            result["tvdb_id"] = showdetails["id"]
            result["network"] = showdetails["network"]
            result["studio"] = [showdetails["network"]]
            local_airday, local_airday_short, airday_int = self._get_local_weekday(showdetails["airsDayOfWeek"])
            result["airday"] = local_airday
            result["airday.short"] = local_airday_short
            result["airday.int"] = airday_int
            result["airtime"] = self._get_local_time(showdetails["airsTime"])
            result["airdaytime"] = "%s %s (%s)" % (result["airday"], result["airtime"], result["network"])
            result["airdaytime.short"] = "%s %s" % (result["airday.short"], result["airtime"])
            result["airdaytime.label"] = "%s %s - %s %s" % (result["airday"],
                                                            result["airtime"],
                                                            xbmc.getLocalizedString(145),
                                                            result["network"])
            result["airdaytime.label.short"] = "%s %s - %s %s" % (
                result["airday.short"],
                result["airtime"],
                xbmc.getLocalizedString(145),
                result["network"])
            result["votes"] = showdetails["siteRatingCount"]
            result["rating.tvdb"] = showdetails["siteRating"]
            # make sure we have a decimal in the rating
            if len(str(result["rating.tvdb"])) == 1:
                result["rating.tvdb"] = "%s.0" % result["rating.tvdb"]
            result["rating"] = result["rating.tvdb"]
            result["votes.tvdb"] = showdetails["siteRatingCount"]
            try:
                result["runtime"] = int(showdetails["runtime"]) * 60
            except Exception:
                pass
            result["plot"] = showdetails["overview"]
            result["genre"] = showdetails["genre"]
            classification = CLASSIFICATION_REGEX.search("/".join(showdetails["genre"])) if isinstance(showdetails["genre"], list) else None
            result["classification"] = classification.group(1) if classification else 'Scripted'
            result["firstaired"] = showdetails["firstAired"]
            result["imdbnumber"] = showdetails["imdbId"]
            # artwork
            result["art"] = {}
            fanarts = self.get_series_fanarts(showdetails["id"])
            if fanarts:
                result["art"]["fanart"] = fanarts[0]
                result["art"]["fanarts"] = fanarts
            landscapes = self.get_series_fanarts(showdetails["id"], True)
            if landscapes:
                result["art"]["landscapes"] = landscapes
                result["art"]["landscape"] = landscapes[0]
            posters = self.get_series_posters(showdetails["id"])
            if posters:
                result["art"]["posters"] = posters
                result["art"]["poster"] = posters[0]
            if showdetails.get("banner"):
                result["art"]["banner"] = "https://thetvdb.com/banners/" + showdetails["banner"]
        return result

    def _parse_kodi_show(self, kodi_details):
        ''' get tvdb series details by providing kodi showdetails'''
        tvdb_details = None
        result = None
        if kodi_details["imdbnumber"] and kodi_details["imdbnumber"].startswith("tt"):
            # lookup serie by imdbid
            tvdb_details = self.get_series_by_imdb_id(kodi_details["imdbnumber"])
        elif kodi_details["imdbnumber"]:
            # assume imdbid in kodidb is already tvdb id
            tvdb_details = self.get_series(kodi_details["imdbnumber"])
        if not tvdb_details and "uniqueid" in kodi_details:
            # kodi 17+ uses the uniqueid field to store the imdb/tvdb number
            for value in kodi_details["uniqueid"]:
                if value.startswith("tt"):
                    tvdb_details = self.get_series_by_imdb_id(value)
                elif value:
                    tvdb_details = self.get_series(value)
                if tvdb_details:
                    break
        if not tvdb_details:
            # lookup series by name as fallback
            tvdb_search = self.search_series(kodi_details["title"])
            if tvdb_search:
                tvdb_details = self.get_series(tvdb_search[0]["id"])
        if tvdb_details:
            # combine kodi tvshow details with tvdb series details
            result = kodi_details
            # append images from tvdb details
            for key, value in tvdb_details["art"].items():
                if value and not result["art"].get(key):
                    result["art"][key] = value
            # combine info from both dicts
            for key, value in tvdb_details.items():
                if value and not result.get(key):
                    result[key] = value
            result["isFolder"] = True
            result["tvdb_status"] = tvdb_details["status"]
            result["library"] = "videodb://tvshows/titles/%s/" % kodi_details["tvshowid"]
        return result

    @staticmethod
    def _log_msg(msg, level=xbmc.LOGDEBUG):
        '''logger to kodi log'''
        if isinstance(msg, unicode):
            msg = msg.encode("utf-8")
        xbmc.log('{0} --> {1}'.format(ADDON_ID, msg), level=level)

    @staticmethod
    def _get_clean_image(image):
        '''helper to strip all kodi tags/formatting of an image path/url'''
        if not image or isinstance(image, list):
            return image
        if image and "image://" in image:
            image = image.replace("image://", "")
            image = urllib.unquote(image.encode("utf-8"))
            if image.endswith("/"):
                image = image[:-1]
        if not isinstance(image, unicode):
            image = image.decode("utf8")
        return image

    def _get_token(self, refresh=False):
        '''get jwt token for api'''
        # get token from memory cache first
        if self._token and not refresh:
            return self._token
        token = self._win.getProperty("script.module.thetvdb.token").decode('utf-8')
        if token and not refresh:
            return token

        # refresh previous token
        prev_token = self._addon.getSetting("token")
        if prev_token:
            url = 'https://api.thetvdb.com/refresh_token'
            headers = {'Content-Type': 'application/json', 'Accept': 'application/json',
                       'User-agent': 'Mozilla/5.0', 'Authorization': 'Bearer %s' % prev_token}
            response = requests.get(url, headers=headers)
            if response and response.content and response.status_code == 200:
                data = json.loads(response.content.decode('utf-8', 'replace'))
                token = data["token"]
            if token:
                self._win.setProperty("script.module.thetvdb.token", token)
                self._token = token
                return token

        # do first login to get initial token
        url = 'https://api.thetvdb.com/login'
        payload = {'apikey': self.api_key}
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'User-agent': 'Mozilla/5.0'}
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        if response and response.content and response.status_code == 200:
            data = json.loads(response.content.decode('utf-8', 'replace'))
            token = data["token"]
            self._addon.setSetting("token", token)
            self._win.setProperty("script.module.thetvdb.token", token)
            self._token = token
            return token
        else:
            self._log_msg("Error getting JWT token!", xbmc.LOGWARNING)
            return None

    @staticmethod
    def _get_kodi_json(method, params):
        '''helper to get data from the kodi json database'''
        json_response = xbmc.executeJSONRPC('{ "jsonrpc": "2.0", "method" : "%s", "params": %s, "id":1 }'
                                            % (method, params.encode("utf-8")))
        jsonobject = json.loads(json_response.decode('utf-8', 'replace'))
        if 'result' in jsonobject:
            jsonobject = jsonobject['result']
        return jsonobject

    def _get_local_time(self, timestr):
        '''returns the correct localized representation of the time provided by the api'''
        result = ""
        try:
            if timestr and ":" in timestr:
                timestr = timestr.replace(".", ":")
                if "H" in xbmc.getRegion('time'):
                    time_format = "HH:mm"
                else:
                    time_format = "h:mm A"
                if " AM" in timestr or " PM" in timestr:
                    result = arrow.get(timestr, 'h:mm A').format(time_format, locale=KODI_LANGUAGE)
                elif " am" in timestr or " pm" in timestr:
                    result = arrow.get(timestr, 'h:mm a').format(time_format, locale=KODI_LANGUAGE)
                elif "AM" in timestr or "PM" in timestr:
                    result = arrow.get(timestr, 'h:mmA').format(time_format, locale=KODI_LANGUAGE)
                elif "am" in timestr or "pm" in timestr:
                    result = arrow.get(timestr, 'h:mma').format(time_format, locale=KODI_LANGUAGE)
                elif len(timestr.split(":")[0]) == 1:
                    result = arrow.get(timestr, 'h:mm').format(time_format, locale=KODI_LANGUAGE)
                else:
                    result = arrow.get(timestr, 'HH:mm').format(time_format, locale=KODI_LANGUAGE)
        except Exception as exc:
            self._log_msg(str(exc), xbmc.LOGWARNING)
            return timestr
        return result

    def _get_local_date(self, datestr, long_date=False):
        '''returns the localized representation of the date provided by the api'''
        result = ""
        try:
            if long_date:
                result = arrow.get(datestr).strftime(xbmc.getRegion('datelong'))
            else:
                result = arrow.get(datestr).strftime(xbmc.getRegion('dateshort'))
        except Exception as exc:
            self._log_msg("Exception in _get_local_date: %s" % exc)
        return result

    def _get_local_weekday(self, weekday):
        '''returns the localized representation of the weekday provided by the api'''
        if not weekday:
            return ("", "", 0)
        day_name = weekday
        day_name_short = day_name[:3]
        day_int = 0
        try:
            locale = arrow.locales.get_locale(KODI_LANGUAGE)
            day_names = {"monday": 1, "tuesday": 2, "wednesday": 3, "thurday": 4,
                         "friday": 5, "saturday": 6, "sunday": 7}
            day_int = day_names.get(weekday.lower(), 0)
            if day_int:
                day_name = locale.day_name(day_int).capitalize()
                day_name_short = locale.day_abbreviation(day_int).capitalize()
        except Exception as exc:
            self._log_msg(str(exc))
        return (day_name, day_name_short, day_int)
