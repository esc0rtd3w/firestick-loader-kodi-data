#!/usr/bin/python
# -*- coding: utf-8 -*-

"""get metadata from omdb"""

from utils import get_json, formatted_number, int_with_commas, try_parse_int, KODI_LANGUAGE, ADDON_ID
from simplecache import use_cache
import arrow
import xbmc
import xbmcaddon


class Omdb(object):
    """get metadata from omdb"""
    api_key = None  # public var to be set by the calling addon

    def __init__(self, simplecache=None):
        """Initialize - optionaly provide simplecache object"""
        if not simplecache:
            from simplecache import SimpleCache
            self.cache = SimpleCache()
        else:
            self.cache = simplecache
        addon = xbmcaddon.Addon(id=ADDON_ID)
        api_key = addon.getSetting("omdbapi_apikey")
        if api_key:
            self.api_key = api_key
        del addon

    @use_cache(14)
    def get_details_by_imdbid(self, imdb_id):
        """get omdb details by providing an imdb id"""
        params = {"i": imdb_id}
        data = self.get_data(params)
        return self.map_details(data) if data else None

    @use_cache(14)
    def get_details_by_title(self, title, year="", media_type=""):
        """ get omdb details by title
            title --> The title of the media to look for (required)
            year (str/int)--> The year of the media (optional, better results when provided)
            media_type --> The type of the media: movie/tvshow (optional, better results of provided)
        """
        if "movie" in media_type:
            media_type = "movie"
        elif media_type in ["tvshows", "tvshow"]:
            media_type = "series"
        params = {"t": title, "y": year, "type": media_type}
        data = self.get_data(params)
        return self.map_details(data) if data else None

    @use_cache(14)
    def get_data(self, params):
        """helper method to get data from omdb json API"""
        base_url = 'http://www.omdbapi.com/'
        params["plot"] = "full"
        if self.api_key:
            params["apikey"] = self.api_key
            rate_limit = None
        else:
            # rate limited api key !
            params["apikey"] = "d4d53b9a"
            rate_limit = ("omdbapi.com", 2)
        params["r"] = "json"
        return get_json(base_url, params, ratelimit=rate_limit)

    @staticmethod
    def map_details(data):
        """helper method to map the details received from omdb to kodi compatible format"""
        result = {}
        for key, value in data.iteritems():
            # filter the N/A values
            if value in ["N/A", "NA"] or not value:
                continue
            if key == "Title":
                result["title"] = value
            elif key == "Year":
                try:
                    result["year"] = try_parse_int(value.split("-")[0])
                except Exception:
                    result["year"] = value
            elif key == "Rated":
                result["mpaa"] = value.replace("Rated", "")
            elif key == "Released":
                date_time = arrow.get(value, "DD MMM YYYY")
                result["premiered"] = date_time.strftime(xbmc.getRegion("dateshort"))
                try:
                    result["premiered.formatted"] = date_time.format('DD MMM YYYY', locale=KODI_LANGUAGE)
                except Exception:
                    result["premiered.formatted"] = value
            elif key == "Runtime":
                result["runtime"] = try_parse_int(value.replace(" min", "")) * 60
            elif key == "Genre":
                result["genre"] = value.split(", ")
            elif key == "Director":
                result["director"] = value.split(", ")
            elif key == "Writer":
                result["writer"] = value.split(", ")
            elif key == "Country":
                result["country"] = value.split(", ")
            elif key == "Awards":
                result["awards"] = value
            elif key == "Poster":
                result["thumbnail"] = value
                result["art"] = {}
                result["art"]["thumb"] = value
            elif key == "imdbVotes":
                result["votes.imdb"] = value
                result["votes"] = try_parse_int(value.replace(",", ""))
            elif key == "Ratings":
                for rating_item in value:
                    if rating_item["Source"] == "Internet Movie Database":
                        rating = rating_item["Value"]
                        result["rating.imdb.text"] = rating
                        rating = rating.split("/")[0]
                        result["rating.imdb"] = rating
                        result["rating"] = float(rating)
                        result["rating.percent.imdb"] = "%s" % (try_parse_int(float(rating) * 10))
                    elif rating_item["Source"] == "Rotten Tomatoes":
                        rating = rating_item["Value"]
                        result["rottentomatoes.rating.percent"] = rating
                        rating = rating.replace("%", "")
                        # this should be a dedicated rt rating instead of the meter
                        result["rottentomatoes.rating"] = rating
                        result["rating.rt"] = rating
                        result["rottentomatoes.meter"] = rating
                        result["rottentomatoesmeter"] = rating
                        rating = int(rating)
                        if rating < 60:
                            result["rottentomatoes.rotten"] = rating
                            result["rottentomatoes.image"] = "rotten"
                        else:
                            result["rottentomatoes.fresh"] = rating
                            result["rottentomatoes.image"] = "fresh"
                    elif rating_item["Source"] == "Metacritic":
                        rating = rating_item["Value"]
                        result["rating.mc.text"] = rating
                        rating = rating.split("/")[0]
                        result["metacritic.rating"] = rating
                        result["rating.mc"] = rating
                        result["metacritic.rating.percent"] = "%s" % rating
            elif key == "imdbID":
                result["imdbnumber"] = value
            elif key == "BoxOffice":
                result["boxoffice"] = value
            elif key == "DVD":
                date_time = arrow.get(value, "DD MMM YYYY")
                result["dvdrelease"] = date_time.format('YYYY-MM-DD')
                result["dvdrelease.formatted"] = date_time.format('DD MMM YYYY', locale=KODI_LANGUAGE)
            elif key == "Production":
                result["studio"] = value.split(", ")
            elif key == "Website":
                result["homepage"] = value
            elif key == "Plot":
                result["plot"] = value
                result["imdb.plot"] = value
            elif key == "Type":
                if value == "series":
                    result["type"] = "tvshow"
                else:
                    result["type"] = value
                result["media_type"] = result["type"]
        return result
