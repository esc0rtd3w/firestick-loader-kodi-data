# -*- coding: utf-8 -*-
"""
    Plugin for TvMaze
    Copyright (C) 2018, TonyH

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    -------------------------------------------------------------

    Version:
        2018-08-19
            - TV Calendar added. See example below
        2018-05-14
            Latest version to include with a Jen Release

    Usage Examples:


    <dir>
    <title>All Networks</title>
    <tvmaze>country/all</tvmaze>
    </dir>

    -------------------------------------------------------------

    TV CALENDAR usage
    <dir>
        <title>TV Calendar</title>
        <tvmaze>calendar</tvmaze>
    </dir>
    -------------------------------------------------------------
    <dir>
    <title>Unites States Networks</title>
    <tvmaze>country/United States/1</tvmaze>
    </dir>

    For other countries, replace United States with the country name you prefer.
    List of Countries:

        Afghanistan
        Albania
        Argentina
        Armenia
        Australia
        Austria
        Azerbaijan
        Belarus
        Belgium
        Bosnia and Herzegovina
        Brazil
        Bulgaria
        Canada
        Chile
        China
        Colombia
        Croatia
        Cyprus
        Czech Republic
        Denmark
        Estonia
        Finland
        France
        French Polynesia
        Georgia
        Germany
        Greece
        Hong Kong
        Hungary
        Iceland
        India
        Indonesia
        Iran, Islamic Republic of
        Iraq
        Ireland
        Israel
        Italy
        Japan
        Kazakhstan
        Korea, Democratic People&#039;s Republic of
        Korea, Republic of
        Latvia
        Lebanon
        Lithuania
        Malaysia
        Maldives
        Mexico
        Moldova, Republic of
        Netherlands
        New Zealand
        Norway
        Pakistan
        Peru
        Philippines
        Poland
        Portugal
        Puerto Rico
        Qatar
        Romania
        Russian Federation
        Saudi Arabia
        Serbia
        Singapore
        Slovenia
        South Africa
        Spain
        Sweden
        Switzerland
        Taiwan, Province of China
        Thailand
        Turkey
        Ukraine
        United Arab Emirates
        United Kingdom
        United States
        Venezuela, Bolivarian Republic of

    -------------------------------------------------------------

    <dir>
    <title>ABC Network shows</title>
    <tvmaze>network/3/1</tvmaze>
    </dir>     

    Change the number 3 to the id of the network you want.
    I cant find a list of all networks with thier id's so for
    other networks please refer to the website,
    https://www.tvmaze.com/networks
    find the network your looking for, click it and 
    the id will be in the url. Example:
    https://www.tvmaze.com/networks/4/fox
    where 4 is the show id. So the tag for Fox would be:

    <dir>
    <title>Fox Network shows</title>
    <tvmaze>network/4/1</tvmaze>
    </dir>     

    -------------------------------------------------------------

    <dir>
    <title>Web Channels</title>
    <tvmaze>web_channel/1</tvmaze>
    </dir>

    --------------------------------------------------------------

"""    

import requests,re,json,os
import datetime
import __builtin__
import xbmc, xbmcaddon
from koding import route
from resources.lib.plugin import Plugin
from resources.lib.util.context import get_context_items
from resources.lib.util.xml import JenItem, JenList, display_list
from unidecode import unidecode

CACHE_TIME = 3600  # change to wanted cache time in seconds

TMDB_api_key = __builtin__.tmdb_api_key
addon_fanart = xbmcaddon.Addon().getAddonInfo('fanart')
addon_icon = xbmcaddon.Addon().getAddonInfo('icon')
User_Agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'

class TVMAZE(Plugin):
    name = "tvmaze"

    def process_item(self, item_xml):
        if "<tvmaze>" in item_xml:
            item = JenItem(item_xml)
            if "country/" in item.get("tvmaze", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "country",
                    'url': item.get("tvmaze", ""),
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
            elif "network/" in item.get("tvmaze", ""):
                item = JenItem(item_xml)
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "network",
                    'url': item.get("tvmaze", ""),
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
            elif "show/" in item.get("tvmaze", ""):
                item = JenItem(item_xml)
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "show",
                    'url': item.get("tvmaze", ""),
                    'folder': True,
                    'imdb': "0",
                    'content': "tvshows",
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
            elif "season/" in item.get("tvmaze", ""):
                item = JenItem(item_xml)
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "season",
                    'url': item.get("tvmaze", ""),
                    'folder': True,
                    'imdb': "0",
                    'content': "seasons",
                    'season': "0",
                    'episode': "0",
                    'info': {},
                    'year': "0",
                    'context': {},
                    "summary": item.get("summary", None)
                }
                result_item["properties"] = {
                    'fanart_image': result_item["fanart"]
                }
                result_item['fanart_small'] = result_item["fanart"]
                return result_item
            elif "web_channel/" in item.get("tvmaze", ""):
                item = JenItem(item_xml)
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "web_channel",
                    'url': item.get("tvmaze", ""),
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
            elif "calendar" in item.get("tvmaze", ""):
                item = JenItem(item_xml)
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "calendar",
                    'url': item.get("tvmaze", ""),
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
            elif "day" in item.get("tvmaze", ""):
                item = JenItem(item_xml)
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "day_episode",
                    'url': item.get("tvmaze", ""),
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

@route(mode='country', args=["url"])
def get_country(url):
    xml = ""
    if "all" in url:
        html = "https://www.tvmaze.com/networks"
        html2 = requests.get(html).content
        block = re.compile('<option value=""></option>(.+?)</select>',re.DOTALL).findall(html2)
        match = re.compile('<option value="(.+?)">(.+?)</option>',re.DOTALL).findall(str(block))
        for number, country in match:
            xml += "<dir>"\
                   "<title>%s</title>"\
                   "<tvmaze>country/%s/1</tvmaze>"\
                   "</dir>" % (country, country)

        jenlist = JenList(xml)
        display_list(jenlist.get_list(), jenlist.get_content_type())
    else:
        last = url.split("/")[-2]
        num = url.split("/")[-1]
        html = "https://www.tvmaze.com/networks"
        html2 = requests.get(html).content
        block = re.compile('<option value=""></option>(.+?)</select>',re.DOTALL).findall(html2)
        match = re.compile('<option value="(.+?)">(.+?)</option>',re.DOTALL).findall(str(block))
        for number, country in match:
            if country == last:
                html3 = "https://www.tvmaze.com/networks?Network%5Bcountry_enum%5D="+number+"&Network%5Bsort%5D=1&page="+num
                html4 = requests.get(html3).content
                match = re.compile('<div class="card primary grid-x">.+?<a href="(.+?)".+?<img src="(.+?)".+?<a href=".+?">(.+?)</a>',re.DOTALL).findall(html4)
                for link, image, name in match:
                    link = link.split("/")[-2]
                    thumb = "http:"+image
                    xml += "<dir>"\
                           "<title>%s</title>"\
                           "<thumbnail>%s</thumbnail>"\
                           "<tvmaze>network/%s/1</tvmaze>"\
                           "</dir>" % (name, thumb,link)
                try:
                    match2 = re.compile('<ul class="pagination">.+?<li class="current"><a href="(.+?)"',re.DOTALL).findall(html4)[0]
                    page = match2.split(";")[-1]
                    page = page.replace("page=","")
                    page = int(page)
                    next_page = page+1
                    xml += "<dir>"\
                           "<title>[COLOR dodgerblue]Next Page >>[/COLOR]</title>"\
                           "<tvmaze>country/%s/%s</tvmaze>"\
                           "<thumbnail>http://www.clker.com/cliparts/a/f/2/d/1298026466992020846arrow-hi.png</thumbnail>"\
                           "</dir>" % (last, next_page)
                except:
                    pass
        jenlist = JenList(xml)
        display_list(jenlist.get_list(), jenlist.get_content_type())

@route(mode='web_channel', args=["url"])
def get_web_channel(url):
    xml = ""
    #last = url.split("/")[-2]
    num = url.split("/")[-1]
    html = "https://www.tvmaze.com/webchannels?WebChannel%5Bcountry_enum%5D=&WebChannel%5Bsort%5D=1&page="+num
    html2 = requests.get(html).content
    match = re.compile('<div class="card primary grid-x">.+?<a href="(.+?)".+?<img src="(.+?)".+?<a href=".+?">(.+?)</a>',re.DOTALL).findall(html2)
    for link, image, name in match:
        link = link.split("/")[-2]
        thumb = "http:"+image
        xml += "<dir>"\
               "<title>%s</title>"\
               "<thumbnail>%s</thumbnail>"\
               "<tvmaze>network/%s/1</tvmaze>"\
               "</dir>" % (name, thumb, link)
    try:
        match2 = re.compile('<ul class="pagination">.+?<li class="current"><a href="(.+?)"',re.DOTALL).findall(html2)[0]
        page = match2.split(";")[-1]
        page = page.replace("page=","")
        page = int(page)
        next_page = page+1
        xml += "<dir>"\
               "<title>[COLOR dodgerblue]Next Page >>[/COLOR]</title>"\
               "<tvmaze>web_channel/%s</tvmaze>"\
               "<thumbnail>http://www.clker.com/cliparts/a/f/2/d/1298026466992020846arrow-hi.png</thumbnail>"\
               "</dir>" % (next_page)
    except:
        pass
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())



@route(mode='network', args=["url"])
def get_network(url):
    xml = ""
    last = url.split("/")[-2]
    num = url.split("/")[-1]
    html = "https://www.tvmaze.com/shows?Show%5Bnetwork_id%5D="+last+"&page="+num
    html2= requests.get(html).content
    match = re.compile('<div class="card primary grid-x">.+?<a href="(.+?)".+?<img src="(.+?)".+?<a href=".+?">(.+?)</a>',re.DOTALL).findall(html2)
    for link, image, name in match:
        link = link.split("/")[-2]
        thumb = "http:"+image
        xml += "<dir>"\
               "<title>%s</title>"\
               "<thumbnail>%s</thumbnail>"\
               "<tvmaze>show/%s/%s</tvmaze>"\
               "</dir>" % (name, thumb, name, link)
    try:
        match2 = re.compile('<ul class="pagination">.+?<li class="current"><a href="(.+?)"',re.DOTALL).findall(html2)[0]
        page = match2.split(";")[-1]
        page = page.replace("page=","")
        page = int(page)
        next_page = page+1
        xml += "<dir>"\
               "<title>[COLOR dodgerblue]Next Page >>[/COLOR]</title>"\
               "<tvmaze>network/%s/%s</tvmaze>"\
               "<thumbnail>http://www.clker.com/cliparts/a/f/2/d/1298026466992020846arrow-hi.png</thumbnail>"\
               "</dir>" % (last, next_page)
    except:
        pass
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())

@route(mode='show', args=["url"])
def get_show(url):
    xml = ""
    tv_title = url.split("/")[-2]
    tv_title = remove_non_ascii(tv_title)
    Title = remove_non_ascii(tv_title)
    Title = Title.lower()
    Title = Title.encode('utf8')
    Title = Title.replace(" ", "%20")
    html = "https://api.themoviedb.org/3/search/tv?api_key=%s&language=en-US&query=%s&page=1" % (TMDB_api_key, Title)
    html2 = requests.get(html).json()
    result = html2['results'][0]
    tmdb_id = result['id']
    date = result['first_air_date']
    year = date.split("-")[0]
    fanart = result['backdrop_path']
    fanart = fanart.replace("/", "")
    tmdb_fanart = "https://image.tmdb.org/t/p/original/"+str(fanart)
    url3 = "https://api.themoviedb.org/3/tv/%s/external_ids?api_key=%s&language=en-US" % (tmdb_id, TMDB_api_key)
    html4 = requests.get(url3).json()
    imdb = html4['imdb_id']
    tvdb = html4['tvdb_id']
    url2 = "https://api.themoviedb.org/3/tv/%s?api_key=%s&language=en-US" % (tmdb_id, TMDB_api_key)
    html3 = requests.get(url2).json()
    seas = html3['seasons']
    for seasons in seas:
        thumb = seasons['poster_path']
        thumb = "https://image.tmdb.org/t/p/original"+str(thumb)
        title = remove_non_ascii(seasons["name"])
        sea_num = seasons['season_number']
        sea_year = seasons['air_date']
        xml += "<dir>"\
               "<title>%s</title>"\
               "<year>%s</year>"\
               "<thumbnail>%s</thumbnail>"\
               "<fanart>%s</fanart>"\
               "<tvmaze>season/%s/%s/%s/%s/%s/%s/%s</tvmaze>"\
               "</dir>" % (title, year, thumb, tmdb_fanart, year, tv_title, fanart, imdb, tvdb, tmdb_id, sea_num)

    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())


@route(mode='season', args=["url"])
def get_season(url):
    xml = ""
    sea_num = url.split("/")[-1]
    sea_num = str(sea_num)
    tmdb_id = url.split("/")[-2]
    tvdb = url.split("/")[-3]
    imdb = url.split("/")[-4]
    fanart = url.split("/")[-5]
    tv_title = url.split("/")[-6]
    year = url.split("/")[-7]
    tmdb_fanart = "https://image.tmdb.org/t/p/original/"+str(fanart)
    html = "https://api.themoviedb.org/3/tv/%s/season/%s?api_key=%s&language=en-US" % (tmdb_id, sea_num, TMDB_api_key)
    html2 = requests.get(html).json()
    eps = html2['episodes']
    for episodes in eps:
        epi_num = episodes['episode_number']
        thumb = episodes['still_path']
        thumb = "https://image.tmdb.org/t/p/original"+str(thumb)
        title = episodes['name']
        title = remove_non_ascii(title)
        premiered = episodes['air_date']
        xml += "<item>"\
              "<title>%s</title>"\
              "<meta>"\
              "<imdb>%s</imdb>"\
              "<tvdb>%s</tvdb>"\
              "<content>episode</content>"\
              "<tvshowtitle>%s</tvshowtitle>"\
              "<year>%s</year>"\
              "<title>%s</title>"\
              "<premiered>%s</premiered>"\
              "<season>%s</season>"\
              "<episode>%s</episode>"\
              "</meta>"\
              "<link>"\
              "<sublink>search</sublink>"\
              "<sublink>searchsd</sublink>"\
              "</link>"\
              "<thumbnail>%s</thumbnail>"\
              "<fanart>%s</fanart>"\
              "</item>" % (title, imdb, tvdb, tv_title, year, title, premiered, sea_num, epi_num, thumb, tmdb_fanart)


    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())


@route(mode='calendar')
def calendars():
    calendar_link = 'http://api.tvmaze.com/schedule?date=%s'
    xml = ""
    m = "January|February|March|April|May|June|July|August|September|October|November|December".encode('utf-8').split('|')
    try:
        months = [(m[0], 'January'), (m[1], 'February'), (m[2], 'March'), (m[3], 'April'), (m[4], 'May'),
                  (m[5], 'June'), (m[6], 'July'), (m[7], 'August'), (m[8], 'September'), (m[9], 'October'),
                  (m[10], 'November'), (m[11], 'December')]
    except:
        months = []

    d = "Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday".encode('utf-8').split('|')
    try:
        days = [(d[0], 'Monday'), (d[1], 'Tuesday'), (d[2], 'Wednesday'), (d[3], 'Thursday'), (d[4], 'Friday'),
                (d[5], 'Saturday'), (d[6], 'Sunday')]
    except:
        days = []

    for i in range(0, 30):
        try:
            date_time = (datetime.datetime.utcnow() - datetime.timedelta(hours=5))
            name = (date_time - datetime.timedelta(days=i))
            name = ("[B]%s[/B] : %s" % (name.strftime('%A'), name.strftime('%d %B'))).encode('utf-8')
            for m in months: name = name.replace(m[1], m[0])
            for d in days: name = name.replace(d[1], d[0])
            try:
                name = name.encode('utf-8')
            except:
                pass

            url = calendar_link % (date_time - datetime.timedelta(days=i)).strftime('%Y-%m-%d')
            xml +="<item>"\
                  "<title>%s</title>"\
                  "<tvmaze>%s|day</tvmaze>"\
                  "<thumbnail>%s</thumbnail>"\
                  "<fanart>%s</fanart>"\
                  "</item>" % (name, url, addon_icon, addon_fanart)
        except:
            pass

    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())


@route(mode='day_episode', args=['url'])
def tvmaze_list(url):
    import traceback
    xml = ""
    url = url.split('|')[0]
    try:
        result = requests.get(url).content
        items = json.loads(result)
    except:
        return

    for item in items:
        try:
            title = item['name']
            title = remove_non_ascii(title)

            season = item['season']
            if not season: season = '0'

            episode = item['number']
            if not episode: episode = '0'

            tvshowtitle = item['show']['name']
            tvshowtitle = remove_non_ascii(tvshowtitle)

            year = item['show']['premiered']
            year = re.findall('(\d{4})', year)[0]
            year = year.encode('utf-8')

            imdb = item['show']['externals']['imdb']
            if imdb is None or imdb == '':
                imdb = '0'
            else:
                imdb = 'tt' + re.sub('[^0-9]', '', str(imdb))
            imdb = imdb.encode('utf-8')

            tvdb = item['show']['externals']['thetvdb']
            if tvdb is None or tvdb == '': continue
            tvdb = re.sub('[^0-9]', '', str(tvdb))
            tvdb = tvdb.encode('utf-8')

            try:
                poster = item['show']['image']['original']
            except:
                poster = '0'
            if poster is None or poster == '':
                poster = '0'
            poster = poster.encode('utf-8')

            try:
                thumb1 = item['show']['image']['original']
            except:
                thumb1 = '0'
            try:
                thumb2 = item['image']['original']
            except:
                thumb2 = '0'
            if thumb2 is None or thumb2 == '0':
                thumb = thumb1
            else:
                thumb = thumb2
            if thumb is None or thumb == '': thumb = '0'
            thumb = thumb.encode('utf-8')

            premiered = item['airdate']
            try:
                premiered = re.findall('(\d{4}-\d{2}-\d{2})', premiered)[0]
            except:
                premiered = '0'
            premiered = premiered.encode('utf-8')

            final_title = '{0} - {1}x{2} - {3}' .format(tvshowtitle, season, episode, title)
            xml += "<item>" \
                   "<title>%s</title>"\
                   "<meta>" \
                   "<imdb>%s</imdb>" \
                   "<tvdb>%s</tvdb>" \
                   "<content>episode</content>" \
                   "<tvshowtitle>%s</tvshowtitle>" \
                   "<year>%s</year>" \
                   "<title>%s</title>" \
                   "<premiered>%s</premiered>" \
                   "<season>%s</season>" \
                   "<episode>%s</episode>" \
                   "</meta>" \
                   "<link>" \
                   "<sublink>search</sublink>" \
                   "<sublink>searchsd</sublink>" \
                   "</link>" \
                   "<thumbnail>%s</thumbnail>" \
                   "<fanart>%s</fanart>" \
                   "</item>" % (final_title, imdb, tvdb, tvshowtitle, year, title,
                                premiered, int(season), int(episode), thumb, poster)


        except Exception:
            import xbmcgui
            failure = traceback.format_exc()
            xbmcgui.Dialog().textviewer('Exception', str(failure))

    xml = remove_non_ascii(xml)
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())


# def get_network(url):
#     html = requests.get(url).content
#     match = re.compile('<div class="card primary grid-x">.+?<a href="(.+?)".+?<img src="(.+?)".+?<a href=".+?">(.+?)</a>',re.DOTALL).findall(html4)
#     for link, image, name in match:
#         link = link.split("/")[-2]
#         thumb = "http:"+image
#         xml = "<dir>"\
#                "<title>%s</title>"\
#                "<thumbnail>%s</thumbnail>"\
#                "</dir>" % (name, thumb)
#         return xml               



def remove_non_ascii(text):
    return unidecode(text)
           


       


                            

