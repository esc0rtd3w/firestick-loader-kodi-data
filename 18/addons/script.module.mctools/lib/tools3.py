# coding: utf-8
from urllib import quote_plus

import xbmc

from ehp import *
from storage import *
from untangle import *
from xbmc_utils import *

__author__ = 'Mancuniancol'

# initialization
Html()
Browser()
storage_info = Storage(xbmc.translatePath('special://profile/addon_data/%s/' % Settings.id_addon), None)
storage_path = xbmc.translatePath('special://profile/addon_data/')
tmdb_id = xbmcaddon.Addon('script.module.mctools').getSetting('tmdb_id')


# noinspection PyBroadException
def get_playable_link(page):
    page = normalize(uncode_name(page))
    exceptions_list = storage_info["exceptions"]
    result = page
    log.debug(result)
    if 'divxatope' in page:
        page = page.replace('/descargar/', '/torrent/')
        result = page
    is_link = True
    log.debug(exceptions_list.items())
    if exceptions_list.has(result):
        return page
    if page.startswith("http") and is_link:
        # exceptions
        log.debug(result)
        # download page
        try:
            Browser.open(page)
            data = normalize(Browser.content)
            log.debug(Browser.headers)
            if 'text/html' in Browser.headers.get("content-type", ""):
                content = findall('magnet:\?[^\'"\s<>\[\]]+', data)
                if content is not None and len(content) > 0:
                    result = content[0]
                else:
                    content = findall('/download\?token=[A-Za-z0-9%]+', data)
                    if content is not None and len(content) > 0:
                        result = Settings["url_address"] + content[0]
                    else:
                        content = findall('/telechargement/[a-z0-9-_.]+', data)  # cpasbien
                        if content is not None and len(content) > 0:
                            result = Settings["url_address"] + content[0]
                        else:
                            content = findall('https?:[^\'"\s<>\[\]]+torrent', data)
                            if content is not None and len(content) > 0:
                                result = content[0]
            else:
                exceptions_list.add(search("^https?://(.*?)/", page).group(1))
                exceptions_list.sync()
        except:
            pass
    log.info(result)
    return quote_plus(page)
