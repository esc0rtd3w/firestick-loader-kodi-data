# -*- coding: utf-8 -*-

from resources.lib.xswift2 import plugin
import requests, xbmc

client_key = plugin.get_setting('fanart.apikey', str)
base_url = "http://webservice.fanart.tv/v3/%s/%s"
api_key = "ac3aa6a86ba7518c9e0e198af71a3017"
language = xbmc.getLanguage(xbmc.ISO_639_1)

def get_query_lang(art, lang, season_num=False):
    if art is None:
        return ''
    if not any(i['lang'] == lang for i in art):
        lang = 'en'
    try: 
        temp = []
        
        if season_num:
            for i in art:
                if 'season' in i:
                    if i['season'] == 'all':
                        temp.append(i)
                    elif int(i['season']) == int(season_num):
                        temp.append(i)
                else:
                    temp.append(i)
        else:
            for i in art:
                if 'season' in i:
                    if i['season'] == 'all':
                        temp.append(i)
                else:
                    temp.append(i)
        
        art = temp
    
        result = [(x['url'], x['likes']) for x in art if x.get('lang') == lang]
        result = [(x[0], x[1]) for x in result]
        result = sorted(result, key=lambda x: int(x[1]), reverse=True)
        result = [x[0] for x in result][0]
        result = result
    except:
        result = ''
    if not 'http' in result:
        result = ''

    return result

def get_query(art):
    if art is None: return ''
    try:
        result = [(x['url'], x['likes']) for x in art]
        result = [(x[0], x[1]) for x in result]
        result = sorted(result, key=lambda x: int(x[1]), reverse=True)
        result = [x[0] for x in result][0]
        result = result.encode('utf-8')

    except:
        result = ''
    if not 'http' in result: result = ''

    return result

@plugin.cached(TTL=60*24*7, cache='Fanart')
def get(remote_id, query, season):

    type = query
    
    if type in ['tv', 'show', 'season', 'episode']:
        query = 'tv'
    elif type == 'movies':
        query = 'movies'
    
    art = base_url % (query, remote_id)
    headers = {'client-key': client_key, 'api-key': api_key}

    art = requests.get(art, headers=headers).json()
    
    if type == 'movies':
        meta = {'poster': get_query_lang(art.get('movieposter'), language),
                'fanart': get_query_lang(art.get('moviebackground'), language),
                'banner': get_query_lang(art.get('moviebanner'), language),
                'clearlogo': get_query_lang(art.get('movielogo', []) + art.get('hdmovielogo', []), language),
                'landscape': get_query_lang(art.get('moviethumb'), language)}
    elif type in ['season', 'episode']:
        meta = {'poster': get_query_lang(art.get('seasonposter'), language, season_num=season),
                'fanart': get_query_lang(art.get('showbackground'), language, season_num=season),
                'banner': get_query_lang(art.get('seasonbanner'), language, season_num=season),
                'clearart': get_query_lang(art.get('clearart', []) + art.get('hdclearart', []), language),
                'clearlogo': get_query_lang(art.get('hdtvlogo', []) + art.get('clearlogo', []), language),
                'landscape': get_query_lang(art.get('seasonthumb'), language, season_num=season)}
    elif type in ['tv', 'show']:
        meta = {'poster': get_query_lang(art.get('tvposter'), language),
                'fanart': get_query_lang(art.get('showbackground'), language),
                'banner': get_query_lang(art.get('tvbanner'), language),
                'clearart': get_query_lang(art.get('clearart', []) + art.get('hdclearart', []), language),
                'clearlogo': get_query_lang(art.get('hdtvlogo', []) + art.get('clearlogo', []), language),
                'landscape': get_query_lang(art.get('tvthumb'), language)}

    return meta
