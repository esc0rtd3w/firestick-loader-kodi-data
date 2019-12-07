# -*- coding: UTF-8 -*-
#######################################################################
 # ----------------------------------------------------------------------------
 # "THE BEER-WARE LICENSE" (Revision 42):
 # @Daddy_Blamo wrote this file.  As long as you retain this notice you
 # can do whatever you want with this stuff. If we meet some day, and you think
 # this stuff is worth it, you can buy me a beer in return. - Muad'Dib
 # ----------------------------------------------------------------------------
#######################################################################

# Addon Name: Placenta
# Addon id: plugin.video.placenta
# Addon Provider: Mr.Blamo

import urlparse, urllib

from resources.lib.modules import cache
from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import utils


def _getAniList(url):
    try:
        url = urlparse.urljoin('https://anilist.co', '/api%s' % url)
        return client.request(url, headers={'Authorization': '%s %s' % cache.get(_getToken, 1), 'Content-Type': 'application/x-www-form-urlencoded'})
    except:
        pass


def _getToken():
    result = urllib.urlencode({'grant_type': 'client_credentials', 'client_id': 'placenta-po0z6', 'client_secret': 'WHMhfUXcXb0q5iKjUIGssQu'})
    result = client.request('https://anilist.co/api/auth/access_token', post=result, headers={'Content-Type': 'application/x-www-form-urlencoded'}, error=True)
    result = utils.json_loads_as_str(result)
    return result['token_type'], result['access_token']


def getAlternativTitle(title):
    try:
        t = cleantitle.get(title)

        r = _getAniList('/anime/search/%s' % title)
        r = [(i.get('title_romaji'), i.get('synonyms', [])) for i in utils.json_loads_as_str(r) if cleantitle.get(i.get('title_english', '')) == t]
        r = [i[1][0] if i[0] == title and len(i[1]) > 0 else i[0] for i in r]
        r = [i for i in r if i if i != title][0]
        return r
    except:
        pass
