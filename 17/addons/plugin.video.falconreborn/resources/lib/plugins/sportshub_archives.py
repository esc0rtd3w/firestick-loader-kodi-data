#!/usr/bin/python
# encoding=utf8
"""

    Copyright (C) 2018 MuadDib

    ----------------------------------------------------------------------------
    "THE BEER-WARE LICENSE" (Revision 42):
    @tantrumdev wrote this file.  As long as you retain this notice you can do 
    whatever you want with this stuff. Just Ask first when not released through
    the tools and parser GIT. If we meet some day, and you think this stuff is
    worth it, you can buy him a beer in return. - Muad'Dib
    ----------------------------------------------------------------------------


"""

import base64,json,re,requests,os,traceback,urlparse
import koding
import __builtin__
import xbmc,xbmcaddon,xbmcgui
from koding import route
from resources.lib.plugin import Plugin
from resources.lib.util import dom_parser
from resources.lib.util.context import get_context_items
from resources.lib.util.xml import JenItem, JenList, display_list
from unidecode import unidecode

CACHE_TIME = 3600  # change to wanted cache time in seconds

addon_id   = xbmcaddon.Addon().getAddonInfo('id')
this_addon   = xbmcaddon.Addon(id=addon_id)
addon_fanart = xbmcaddon.Addon().getAddonInfo('fanart')
addon_icon   = xbmcaddon.Addon().getAddonInfo('icon')
User_Agent   = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'

nhl_tonight  = this_addon.getSetting('nhl_tonight')

per_page = { 'mlb':this_addon.getSetting('mlb_replay'), 'nba':this_addon.getSetting('nba_replay'),
            'nfl':this_addon.getSetting('nfl_replay'), 'nhl':this_addon.getSetting('nhl_replay'),
            'motor':this_addon.getSetting('motogp_replay'), 'soccer':this_addon.getSetting('soccer_replay') }

archives = { 'nbareplayhd':'https://nbareplayhd.com/' }

base_mail_url = 'https://my.mail.ru/cgi-bin/my/ajax?user=%s&xemail=&ajax_call=1&func_name=video.get_list&mna=&mnb=&arg_type=album_items&arg_all=1&sort=default&arg_offset=%s&arg_limit=%s'
json_cat_url = '/wp-json/wp/v2/posts/?per_page=%s&categories=%s&page=%s'
json_post_url = '/wp-json/wp/v2/posts/%s'


class SportsHub(Plugin):
    name = "sportshub_archives"

    def process_item(self, item_xml):
        if "<sportshub>" in item_xml:
            item = JenItem(item_xml)
            if "nbareplayhd/" in item.get("sportshub", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "NBAReplayHD",
                    'url': item.get("sportshub", ""),
                    'folder': True,
                    'imdb': "0",
                    'content': "files",
                    'season': "0",
                    'episode': "0",
                    'info': {},
                    'year': "0",
                    'context': get_context_items(item),
                    "summary": item.get("summary", None)
                }
            elif "sh_nfl/" in item.get("sportshub", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "NFLReplay",
                    'url': item.get("sportshub", ""),
                    'folder': True,
                    'imdb': "0",
                    'content': "files",
                    'season': "0",
                    'episode': "0",
                    'info': {},
                    'year': "0",
                    'context': get_context_items(item),
                    "summary": item.get("summary", None)
                }
            elif "sh_mlb/" in item.get("sportshub", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "MLBReplay",
                    'url': item.get("sportshub", ""),
                    'folder': True,
                    'imdb': "0",
                    'content': "files",
                    'season': "0",
                    'episode': "0",
                    'info': {},
                    'year': "0",
                    'context': get_context_items(item),
                    "summary": item.get("summary", None)
                }
            elif "sh_nhl_sc/" in item.get("sportshub", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "NHLCupArchives",
                    'url': item.get("sportshub", ""),
                    'folder': True,
                    'imdb': "0",
                    'content': "files",
                    'season': "0",
                    'episode': "0",
                    'info': {},
                    'year': "0",
                    'context': get_context_items(item),
                    "summary": item.get("summary", None)
                }
            elif "sh_moto_one/" in item.get("sportshub", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "SHMotoOne",
                    'url': item.get("sportshub", ""),
                    'folder': True,
                    'imdb': "0",
                    'content': "files",
                    'season': "0",
                    'episode': "0",
                    'info': {},
                    'year': "0",
                    'context': get_context_items(item),
                    "summary": item.get("summary", None)
                }
            elif "mru_play/" in item.get("sportshub", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "MRUPlayMedia",
                    'url': item.get("sportshub", ""),
                    'folder': True,
                    'imdb': "0",
                    'content': "files",
                    'season': "0",
                    'episode': "0",
                    'info': {},
                    'year': "0",
                    'context': get_context_items(item),
                    "summary": item.get("summary", None)
                }
            result_item["properties"] = {
                'fanart_image': result_item["fanart"]
            }
            result_item['fanart_small'] = result_item["fanart"]
            return result_item


@route(mode='NBAReplayHD', args=["url"])
def get_NBAReplayHD(url):
    xml = ""
    url = url.replace('nbareplayhd/', '') # Strip our category tag off.
    cat_item = url.split('/')
    if cat_item[1] == None or cat_item[1] == '':
        cat_item[1] = '1'
    orig_cat  = cat_item[0]
    orig_page = cat_item[1]
    url = urlparse.urljoin(archives['nbareplayhd'], (json_cat_url % (per_page['nba'], cat_item[0], cat_item[1]))) 
    try:
        response = requests.get(url).content
        results = re.compile('"id":(.+?),',re.DOTALL).findall(response)
        count = 0
        for post_id in results:
            count += 1
            try:
                url = urlparse.urljoin(archives['nbareplayhd'], ('/wp-json/wp/v2/posts/%s' % (post_id)))
                page = requests.get(url).content
                page = page.replace('\\','')
                try:
                    src = 'http:' + re.compile('src="(.+?)"',re.DOTALL).findall(page)[0]
                except:
                    continue

                title = re.compile('"title".+?"rendered":"(.+?)"',re.DOTALL).findall(page)[0]
                title = remove_non_ascii(title)
                xml += "<item>"\
                       "    <title>%s</title>"\
                       "    <link>%s</link>"\
                       "    <thumbnail>%s</thumbnail>"\
                       "</item>" % (title,src,addon_icon)
            except:
                pass
    except:
        pass

    try:
        if count == int(per_page['nba']):
            xml += "<dir>"\
                   "    <title>Next Page >></title>"\
                   "    <sportshub>nbareplayhd/%s/%s</sportshub>"\
                   "</dir>" % (orig_cat,str((int(orig_page)+1)))
    except:
        pass

    if count > 0:
        jenlist = JenList(xml)
        display_list(jenlist.get_list(), jenlist.get_content_type())


@route(mode='NFLReplay', args=["url"])
def get_NFLArchives(url):
    xml = ""
    url = url.replace('sh_nfl/', '')
    offset  = url.split('/')[0]
    account = url.split('/')[1].decode('base64')
    url = base_mail_url % (account, offset, per_page['nfl'])
    if offset == '1':
        offset = '0'
    try:
        response = requests.get(url).content
        results = json.loads(response)
        results = results[2]['items']
        for item in results:
            try:
                title = item['Title']
                meta_url = item['MetaUrl']
                icon = item['ImageUrlP']
                title = clean_mru_title(title)
                xml += "<item>"\
                       "    <title>%s</title>"\
                       "    <sportshub>mru_play/%s</sportshub>"\
                       "    <thumbnail>%s</thumbnail>"\
                       "</item>" % (title,meta_url,icon)
            except:
                failure = traceback.format_exc()
                xbmcgui.Dialog().textviewer('Item Exception',str(failure))
                pass
    except:
        failure = traceback.format_exc()
        xbmcgui.Dialog().textviewer('a',str(failure))
        pass

    try:
        xml += "<dir>"\
               "    <title>Next Page >></title>"\
               "    <sportshub>sh_nfl/%s/%s</sportshub>"\
               "</dir>" % (str(int(offset)+int(per_page['nfl'])),account.encode('base64'))
    except:
        failure = traceback.format_exc()
        xbmcgui.Dialog().textviewer('a',str(failure))
        pass

    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())


@route(mode='MLBReplay', args=["url"])
def get_MLBArchives(url):
    xml = ""
    url = url.replace('sh_mlb/', '')
    offset  = url.split('/')[0]
    account = url.split('/')[1].decode('base64')
    url = base_mail_url % (account, offset, per_page['mlb'])
    if offset == '1':
        offset = '0'
    try:
        response = requests.get(url).content
        results = json.loads(response)
        results = results[2]['items']
        for item in results:
            try:
                title = item['Title']
                meta_url = item['MetaUrl']
                icon = item['ImageUrlP']
                title = clean_mru_title(title)
                xml += "<item>"\
                       "    <title>%s</title>"\
                       "    <sportshub>mru_play/%s</sportshub>"\
                       "    <thumbnail>%s</thumbnail>"\
                       "</item>" % (title,meta_url,icon)
            except:
                continue
    except:
        pass

    try:
        xml += "<dir>"\
               "    <title>Next Page >></title>"\
               "    <sportshub>sh_mlb/%s/%s</sportshub>"\
               "</dir>" % (str(int(offset)+int(per_page['mlb'])),account.encode('base64'))
    except:
        pass

    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())


@route(mode='NHLCupArchives', args=["url"])
def get_NHLCupArchives(url):
    xml = ""
    url = url.replace('sh_nhl_sc/', '')
    offset  = url.split('/')[0]
    account = url.split('/')[1].decode('base64')
    url = base_mail_url % (account, offset, per_page['nhl'])
    if offset == '1':
        offset = '0'
    try:
        response = requests.get(url).content
        results = json.loads(response)
        results = results[2]['items']
        for item in results:
            try:
                title = item['Title']
                if 'true' in nhl_tonight:
                    pass
                else:
                    if 'nhl tonight' in title.lower():
                        continue
                meta_url = item['MetaUrl']
                icon = item['ImageUrlP']
                title = clean_mru_title(title)
                xml += "<item>"\
                       "    <title>%s</title>"\
                       "    <sportshub>mru_play/%s</sportshub>"\
                       "    <thumbnail>%s</thumbnail>"\
                       "</item>" % (title,meta_url,icon)
            except:
                failure = traceback.format_exc()
                xbmcgui.Dialog().textviewer('Item Exception',str(failure))
                pass
    except:
        failure = traceback.format_exc()
        xbmcgui.Dialog().textviewer('a',str(failure))
        pass

    try:
        xml += "<dir>"\
               "    <title>Next Page >></title>"\
               "    <sportshub>sh_nhl_sc/%s/%s</sportshub>"\
               "</dir>" % (str(int(offset)+int(per_page['nhl'])),account.encode('base64'))
    except:
        failure = traceback.format_exc()
        xbmcgui.Dialog().textviewer('a',str(failure))
        pass

    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())


@route(mode='SHMotoOne', args=["url"])
def get_SHMotoOneArchives(url):
    xml = ""
    url = url.replace('sh_moto_one/', '')
    offset  = url.split('/')[0]
    account = url.split('/')[1].decode('base64')
    url = base_mail_url % (account, offset, per_page['motor'])
    if offset == '1':
        offset = '0'
    try:
        response = requests.get(url).content
        results = json.loads(response)
        results = results[2]['items']
        for item in results:
            try:
                title = item['Title']
                meta_url = item['MetaUrl']
                icon = item['ImageUrlP']
                title = clean_mru_title(title)
                xml += "<item>"\
                       "    <title>%s</title>"\
                       "    <sportshub>mru_play/%s</sportshub>"\
                       "    <thumbnail>%s</thumbnail>"\
                       "</item>" % (title,meta_url,icon)
            except:
                failure = traceback.format_exc()
                xbmcgui.Dialog().textviewer('Item Exception',str(failure))
                pass
    except:
        failure = traceback.format_exc()
        xbmcgui.Dialog().textviewer('a',str(failure))
        pass

    try:
        xml += "<dir>"\
               "    <title>Next Page >></title>"\
               "    <sportshub>sh_moto_one/%s/%s</sportshub>"\
               "</dir>" % (str(int(offset)+int(per_page['motor'])),account.encode('base64'))
    except:
        failure = traceback.format_exc()
        xbmcgui.Dialog().textviewer('a',str(failure))
        pass

    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())

@route(mode='MRUPlayMedia', args=["url"])
def get_MRUPlayMedia(url):
    xml = ""
    url = url.replace('mru_play/', '')
    try:
        import cookielib, urllib2
        cookieJar = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar), urllib2.HTTPHandler())
        conn = urllib2.Request(url)
        connection = opener.open(conn)
        f = connection.read()
        connection.close()
        js = json.loads(f)
        for cookie in cookieJar:
            token = cookie.value
        js = js['videos']
        for el in js:
            link = 'http:'+el['url']+'|Cookie=video_key='+token
            xml += "<item>"\
                   "    <title>%s</title>"\
                   "    <link>%s</link>"\
                   "    <thumbnail>%s</thumbnail>"\
                   "</item>" % (el['key'],link,addon_icon)
    except:
        pass

    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())


def clean_mru_title(title):
    title = remove_non_ascii(title)
    title = re.sub('\[.*?]','',title)
    return title

def remove_non_ascii(text):
    try:
        text = text.decode('utf-8').replace(u'\xc2', u'A').replace(u'\xc3', u'A').replace(u'\xc4', u'A').replace('u2013','-')
    except:
        pass
    return unidecode(text)