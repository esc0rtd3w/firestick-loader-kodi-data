import sys
import os

from xbmcswift2 import xbmc

from meta import plugin, import_tmdb, LANG
from meta.utils.text import equals

from language import get_string as _

from settings import SETTING_STYLE, SETTING_STYLE_CUSTOM_FOLDER, SETTING_BACKGROUND, SETTING_BACKGROUND_CUSTOM_FOLDER 

def caller_name():
    return sys._getframe(2).f_code.co_name
    
def caller_args():
    import inspect
    caller = inspect.stack()[2][0]
    args, _, _, values = inspect.getargvalues(caller)
    return dict([(i, values[i]) for i in args])

def get_icon_path(icon_name):
    if plugin.get_setting(SETTING_STYLE, unicode) != "Custom": return os.path.join('https://raw.githubusercontent.com/OpenELEQ/Style/master/MetalliQ/', plugin.get_setting(SETTING_STYLE, unicode).lower() + "/" , icon_name+".png")
    else: return os.path.join(plugin.get_setting(SETTING_STYLE_CUSTOM_FOLDER, unicode), icon_name+".png")

def get_background_path():
    if plugin.get_setting(SETTING_BACKGROUND, unicode) == "Matching": return os.path.join('https://raw.githubusercontent.com/OpenELEQ/Style/master/MetalliQ/backgrounds/', str(plugin.get_setting(SETTING_STYLE, unicode).lower()) + ".png")
    elif plugin.get_setting(SETTING_BACKGROUND, unicode) == "Custom": return os.path.join(plugin.get_setting(SETTING_BACKGROUND_CUSTOM_FOLDER, unicode), "fanart.png")
    else: return os.path.join('https://raw.githubusercontent.com/OpenELEQ/Style/master/MetalliQ/backgrounds/', str(plugin.get_setting(SETTING_BACKGROUND, unicode).lower()) + ".png")

def get_banner_path():
    return 'https://raw.githubusercontent.com/OpenELEQ/Style/master/MetalliQ/default/banner.jpg'

def get_genre_icon(genre_id):
    genre_id = int(genre_id)
    icons = {
        12: "genre_adventure",
        14: "genre_fantasy",
        16: "genre_animation",
        18: "genre_drama",
        27: "genre_horror",
        28: "genre_action",
        35: "genre_comedy",
        36: "genre_history",
        37: "genre_western",
        53: "genre_thriller",
        80: "genre_crime",
        99: "genre_documentary",
        878: "genre_scifi",
        9648: "genre_mystery",
        10402: "genre_music",
        10749: "genre_romance",
        10751: "genre_family",
        10752: "genre_war",
        10759: "genre_action",
        10762: "genre_kids",
        10763: "genre_news",
        10764: "genre_reality",
        10765: "genre_scifi",
        10766: "genre_soap",
        10767: "genre_talk",
        10768: "genre_war",
        10769: "genre_foreign",
        10770: "genre_tv",
    }
    
    if genre_id in icons:
        return get_icon_path(icons[genre_id])
    return "DefaultVideo.png"

def get_genres():
    result = get_base_genres()
    result.update(get_tv_genres())
    return result

@plugin.cached(TTL=60, cache="genres")
def get_tv_genres():
    result = tmdb_tv_genres()
    if not result:
        result = tmdb_tv_genres_mock()
    return result

@plugin.cached(TTL=60, cache="genres")
def get_base_genres():
    result = tmdb_movie_genres()
    if not result:
        result = tmdb_movie_genres_mock()
    return result
    
@plugin.cached(TTL=None, cache="genres")
def tmdb_movie_genres():
    import_tmdb()
    result = tmdb.Genres().list(language=LANG)
    genres= dict([(i['id'], i['name']) for i in result['genres'] \
            if i['name'] is not None])
    if genres:
        return genres
    return None

@plugin.cached(TTL=None, cache="genres")
def tmdb_tv_genres():
    import_tmdb()
    result = tmdb.Genres().list_tv(language=LANG)
    genres= dict([(i['id'], i['name']) for i in result['genres'] \
            if i['name'] is not None])
    if genres:
        return genres
    return None
    
def tmdb_movie_genres_mock():
    mock = [
        {
          "id": 28,
          "name": "Action"
        },
        {
          "id": 12,
          "name": "Adventure"
        },
        {
          "id": 16,
          "name": "Animation"
        },
        {
          "id": 35,
          "name": "Comedy"
        },
        {
          "id": 80,
          "name": "Crime"
        },
        {
          "id": 99,
          "name": "Documentary"
        },
        {
          "id": 18,
          "name": "Drama"
        },
        {
          "id": 10751,
          "name": "Family"
        },
        {
          "id": 14,
          "name": "Fantasy"
        },
        {
          "id": 10769,
          "name": "Foreign"
        },
        {
          "id": 36,
          "name": "History"
        },
        {
          "id": 27,
          "name": "Horror"
        },
        {
          "id": 10402,
          "name": "Music"
        },
        {
          "id": 9648,
          "name": "Mystery"
        },
        {
          "id": 10749,
          "name": "Romance"
        },
        {
          "id": 878,
          "name": "Science Fiction"
        },
        {
          "id": 10770,
          "name": "TV Movie"
        },
        {
          "id": 53,
          "name": "Thriller"
        },
        {
          "id": 10752,
          "name": "War"
        },
        {
          "id": 37,
          "name": "Western"
        }
      ]
    return dict([(i['id'], i['name'], i['properties']) for i in mock])


def tmdb_tv_genres_mock():
    mock = [
        {
          "id": 10759,
          "name": "Action & Adventure"
        },
        {
          "id": 16,
          "name": "Animation"
        },
        {
          "id": 35,
          "name": "Comedy"
        },
        {
          "id": 99,
          "name": "Documentary"
        },
        {
          "id": 18,
          "name": "Drama"
        },
        {
          "id": 10761,
          "name": "Education"
        },
        {
          "id": 10751,
          "name": "Family"
        },
        {
          "id": 10762,
          "name": "Kids"
        },
        {
          "id": 9648,
          "name": "Mystery"
        },
        {
          "id": 10763,
          "name": "News"
        },
        {
          "id": 10764,
          "name": "Reality"
        },
        {
          "id": 10765,
          "name": "Sci-Fi & Fantasy"
        },
        {
          "id": 10766,
          "name": "Soap"
        },
        {
          "id": 10767,
          "name": "Talk"
        },
        {
          "id": 10768,
          "name": "War & Politics"
        },
        {
          "id": 37,
          "name": "Western"
        }
      ]
      
    return dict([(i['id'], i['name']) for i in mock])
