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

    Changelog:
        2018.7.2:
            - Added Clear Cache function
            - Minor update on fetch cache returns


        2018.6.29:
            - Added caching to primary menus (Cache time is 3 hours)

        2018-05-13:
            Updated for handling JS "Load More" changes.

    Usage Examples:

    <dir>
        <title>Featured Podcasts</title>
        <podcastone>pcocategory/featured-podcasts</podcastone>
    </dir>

    <dir>
        <title>New Podcasts</title>
        <podcastone>pcocategory/new-podcasts</podcastone>
    </dir>

    <dir>
        <title>Arts</title>
        <podcastone>pcocategory/arts-podcasts</podcastone>
    </dir>

    <dir>
        <title>Comedy</title>
        <podcastone>pcocategory/comedy-podcasts</podcastone>
    </dir>

    <dir>
        <title>Education</title>
        <podcastone>pcocategory/education-podcasts</podcastone>
    </dir>

    <dir>
        <title>Games and Hobbies</title>
        <podcastone>pcocategory/games-and-hobbies-podcasts</podcastone>
    </dir>

    <dir>
        <title>Government and Organizations</title>
        <podcastone>pcocategory/government-and-organizations-podcasts</podcastone>
    </dir>

    <dir>
        <title>Health</title>
        <podcastone>pcocategory/health-podcasts</podcastone>
    </dir>

    <dir>
        <title>Kids and Family</title>
        <podcastone>pcocategory/kids-and-family-podcasts</podcastone>
    </dir>

    <dir>
        <title>Music</title>
        <podcastone>pcocategory/music-podcasts</podcastone>
    </dir>

    <dir>
        <title>News and Politics</title>
        <podcastone>pcocategory/news-and-politics-podcasts</podcastone>
    </dir>

    <dir>
        <title>Religion and Spirituality</title>
        <podcastone>pcocategory/religion-and-spirituality-podcasts</podcastone>
    </dir>

    <dir>
        <title>Science and Medicine</title>
        <podcastone>pcocategory/science-and-medicine-podcasts</podcastone>
    </dir>

    <dir>
        <title>Society and Culture</title>
        <podcastone>pcocategory/society-and-culture-podcasts</podcastone>
    </dir>

    <dir>
        <title>Sports and Recreation</title>
        <podcastone>pcocategory/sports-and-recreation-podcasts</podcastone>
    </dir>

    <dir>
        <title>Technology and Business</title>
        <podcastone>pcocategory/technology-and-business-podcasts</podcastone>
    </dir>

    <dir>
        <title>TV and Film</title>
        <podcastone>pcocategory/tv-and-film-podcasts</podcastone>
    </dir>

    <dir>
        <title>Heather Dubrows World</title>
        <podcastone>pcoshow/heather-dubrows-world</podcastone>
    </dir>




"""

import __builtin__
import base64,time
import json,re,requests,os,traceback,urlparse
import koding
import xbmc,xbmcaddon,xbmcgui
from koding import route
from resources.lib.plugin import Plugin
from resources.lib.util import dom_parser
from resources.lib.util.context import get_context_items
from resources.lib.util.xml import JenItem, JenList, display_list
from unidecode import unidecode

CACHE_TIME = 10800  # change to wanted cache time in seconds

addon_fanart = xbmcaddon.Addon().getAddonInfo('fanart')
addon_icon   = xbmcaddon.Addon().getAddonInfo('icon')
User_Agent   = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'

pcobase_link = 'https://www.podcastone.com/'
pcoplay_link = 'https://www.podcastone.com/downloadsecurity?url=%s'
pcoepisodes_link = 'https://www.podcastone.com/pg/jsp/program/pasteps_cms.jsp?size=1000&amountToDisplay=1000&page=1&infiniteScroll=true&progID=%s&showTwitter=false&pmProtect=false&displayPremiumEpisodes=false&startAt=0'

class WatchCartoon(Plugin):
    name = "podcastone"

    def process_item(self, item_xml):
        if "<podcastone>" in item_xml:
            item = JenItem(item_xml)
            if "pcocategory/" in item.get("podcastone", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "PCOCats",
                    'url': item.get("podcastone", ""),
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
            elif "pcoshow/" in item.get("podcastone", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "PCOShow",
                    'url': item.get("podcastone", ""),
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
            elif "pcoepisode/" in item.get("podcastone", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "PCOEpisode",
                    'url': item.get("podcastone", ""),
                    'folder': False,
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

    def clear_cache(self):
        dialog = xbmcgui.Dialog()
        if dialog.yesno(xbmcaddon.Addon().getAddonInfo('name'), "Clear PodcastOne Plugin Cache?"):
            koding.Remove_Table("pcastone_com_plugin")

@route(mode='PCOCats', args=["url"])
def get_pcocats(url):
    pins = ""
    url = url.replace('pcocategory/', '') # Strip our category tag off.
    url = urlparse.urljoin(pcobase_link, url)

    xml = fetch_from_db(url)
    if not xml:
        xml = ""
        try:
            html = requests.get(url).content

            div_list = re.compile('<div class="podcast-container flex no-wrap" data-program-name="(.+?)">(.+?)</a></div>',re.DOTALL).findall(html)
            for show_title, content in div_list:
                try:
                    show_url = re.compile('href="(.+?)"',re.DOTALL).findall(content)[0]
                    show_url = show_url.replace('/','')
                    if 'viewProgram' in show_url:
                        url = urlparse.urljoin(pcobase_link, show_url)
                        html = requests.get(url).content
                        more_ep_block = re.compile('<div class="col-xs-12">(.+?)</div>',re.DOTALL).findall(html)[0]
                        show_url = re.compile('href="(.+?)"',re.DOTALL).findall(more_ep_block)[0].replace('/','').replace('?showAllEpisodes=true','')
                    show_icon = urlparse.urljoin(pcobase_link, re.compile('<img src="(.+?)"',re.DOTALL).findall(content)[0])
                    xml += "<dir>"\
                           "    <title>%s</title>"\
                           "    <podcastone>pcoshow/%s</podcastone>"\
                           "    <thumbnail>%s</thumbnail>"\
                           "    <summary>%s</summary>"\
                           "</dir>" % (show_title,show_url,show_icon,show_title)
                except:
                    continue
        except:
            pass

        save_to_db(xml, url)

    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type(), pins)


@route(mode='PCOShow', args=["url"])
def get_pcoshow(url):
    pins = ""
    url = url.replace('pcoshow/', '') # Strip our show tag off.
    url = urlparse.urljoin(pcobase_link, url)
    url = url + '?showAllEpisodes=true'

    xml = fetch_from_db(url)
    if not xml:
        xml = ""
        try:
            html = requests.get(url).content
            prog_id = re.compile('progID: (.+?),',re.DOTALL).findall(html)[0]
            url = pcoepisodes_link % (prog_id)
            html = requests.get(url).content

            # https://www.podcastone.com/pg/jsp/program/pasteps_cms.jsp?size=1000&amountToDisplay=1000&page=1&infiniteScroll=true&progID=1181&showTwitter=false&pmProtect=false&displayPremiumEpisodes=false&startAt=0
            past_episodes = dom_parser.parseDOM(html, 'div', attrs={'class':'flex no-wrap align-center'})
            for episode in past_episodes:
                try:
                    ep_link, ep_title = re.compile('<h3 class="dateTime"><a href="(.+?)" style="color:inherit;">(.+?)</a>',re.DOTALL).findall(episode)[0]
                    ep_page  = urlparse.urljoin(pcobase_link, ep_link)
                    ep_icon  = re.compile('img src="(.+?)"',re.DOTALL).findall(episode)[0]
                    xml += "<item>"\
                           "    <title>%s</title>"\
                           "    <podcastone>pcoepisode/%s</podcastone>"\
                           "    <thumbnail>%s</thumbnail>"\
                           "    <summary>%s</summary>"\
                           "</item>" % (ep_title,ep_page,ep_icon,ep_title)
                except:
                    continue
        except:
            pass

        save_to_db(xml, url)

    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type(), pins)


@route(mode='PCOEpisode', args=["url"])
def get_pcoepisode(url):
    xml = ""
    url = url.replace('pcoepisode/', '') # Strip our episode tag off.

    try:
        html = requests.get(url).content
        episode_item = dom_parser.parseDOM(html, 'div', attrs={'class': 'media-player'})[0]
        episode_item2 = dom_parser.parseDOM(html, 'div', attrs={'class': 'letestepi'})[0]
        ep_icon = dom_parser.parseDOM(episode_item2, 'img', attrs={'class': 'img-responsive'}, ret='src')[0]
        ep_title = dom_parser.parseDOM(html, 'title')[0].replace('PodcastOne: ','')
        play_url = re.compile('href="(.+?)"',re.DOTALL).findall(episode_item)[0].replace("\n","").replace('/downloadsecurity?url=', '')
        url = pcoplay_link % play_url
        item = xbmcgui.ListItem(label=ep_title, path=url, iconImage=ep_icon, thumbnailImage=ep_icon)
        item.setInfo( type="Video", infoLabels={ "Title": ep_title } )
        import resolveurl
        koding.Play_Video(url,showbusy=False,ignore_dp=True,item=item,resolver=resolveurl)
    except:
        pass


def save_to_db(item, url):
    if not item or not url:
        return False
    try:
        koding.reset_db()
        koding.Remove_From_Table(
            "pcastone_com_plugin",
            {
                "url": url
            })

        koding.Add_To_Table("pcastone_com_plugin",
                            {
                                "url": url,
                                "item": base64.b64encode(item),
                                "created": time.time()
                            })
    except:
        return False


def fetch_from_db(url):
    koding.reset_db()
    pcastone_plugin_spec = {
        "columns": {
            "url": "TEXT",
            "item": "TEXT",
            "created": "TEXT"
        },
        "constraints": {
            "unique": "url"
        }
    }
    koding.Create_Table("pcastone_com_plugin", pcastone_plugin_spec)
    match = koding.Get_From_Table(
        "pcastone_com_plugin", {"url": url})
    if match:
        match = match[0]
        if not match["item"]:
            return None
        created_time = match["created"]
        if created_time and float(created_time) + CACHE_TIME >= time.time():
            match_item = match["item"]
            try:
                result = base64.b64decode(match_item)
            except:
                return None
            return result
        else:
            return None
    else:
        return None


def replaceHTMLCodes(txt):
    txt = re.sub("(&#[0-9]+)([^;^0-9]+)", "\\1;\\2", txt)
    try:
        import html.parser as html_parser
    except:
        import HTMLParser as html_parser
    txt = html_parser.HTMLParser().unescape(txt)
    txt = html_parser.HTMLParser().unescape(txt)
    txt = txt.replace("&quot;", "\"")
    txt = txt.replace("&amp;", "&")
    txt = txt.strip()
    return txt