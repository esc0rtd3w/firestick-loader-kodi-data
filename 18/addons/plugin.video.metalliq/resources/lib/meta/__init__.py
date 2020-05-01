from xbmcswift2 import Plugin, xbmc
from settings import SETTING_LANGUAGE_ID, SETTING_TVDB_API

plugin = Plugin()

if plugin.get_setting(SETTING_LANGUAGE_ID, unicode) == "system": LANG = xbmc.getLanguage(xbmc.ISO_639_1,)
else: LANG = plugin.get_setting(SETTING_LANGUAGE_ID, unicode)

TVDB_API = plugin.get_setting(SETTING_TVDB_API, str)

def import_tmdb():
    """ Lazy import tmdb """
    import tmdbsimple
    __builtins__["tmdb"] = tmdbsimple
    
def import_tvdb():
    """ Lazy import tmdb """
    if 'tvdb' not in __builtins__:
        __builtins__['tvdb'] = create_tvdb()

def create_tvdb(language=LANG):
    from tvdb_api import Tvdb
    if len(TVDB_API) == 16:
        try:
            TVDB_KEY = TVDB_API
        except:
            TVDB_KEY = "0629B785CE550C8D"
    else:
        TVDB_KEY = "0629B785CE550C8D"
    return Tvdb(TVDB_KEY, language=language, cache=plugin.storage_path)
