'''
    Ultimate Whitecream
    Copyright (C) 2018 holisticdioxide

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
'''

import re

import xbmcplugin
from resources.lib import utils

addon = utils.addon

@utils.url_dispatcher.register('640')
def v7_main():
    utils.addDir('[COLOR hotpink]Studios[/COLOR]','http://www.vidz7.com/category/', 644, '', '')
    utils.addDir('[COLOR hotpink]Tags[/COLOR]','http://www.vidz7.com/tags/', 644, '', '')
    utils.addDir('[COLOR hotpink]Search[/COLOR]','http://www.vidz7.com/', 645, '', '')
    v7_list('http://www.vidz7.com/')


@utils.url_dispatcher.register('641', ['url'], ['page', 'search'])
def v7_list(url, page=None, search=None):
    orig_url = str(url)
    if page:
        page_end = 'page/' + str(page) + '/' if url.endswith('/') else '/page/' + str(page) + '/'
        url += page_end
    else:
        page = 1
    sort = '?orderby=date' if url.endswith('/') else '/?orderby=date'
    url += sort
    url = url + search if search else url
    try:
        listhtml = utils.getHtml(url)
    except Exception as e:
        return None
    match = re.compile('''class='thumb-wrapp'.*?href='([^']+)'.*?"([^"]+)".*?class='vl'(.*?)class="duration">(.*?)</div>.*?class='hp'[^>]+>([^<]+)<''', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for videopage, img, hd, duration, name in match:
        hd = ' [COLOR orange]HD[/COLOR] ' if 'HD' in hd else ' '
        name = utils.cleantext(name) + hd + duration.strip()
        utils.addDownLink(name, videopage, 642, img, '')
    pages_html = re.compile('<div class="buttons">(.*?)</div', re.DOTALL | re.IGNORECASE).findall(listhtml)[0]
    pages = re.compile('<a[^>]+>(.*?)</a', re.DOTALL | re.IGNORECASE).findall(pages_html)
    pages = [int(p.replace('&nbsp;', '').replace('...', '').strip()) for p in pages]
    max_page = max(pages)
    if page < max_page:
        utils.addDir('Next Page (' + str(page + 1) + ')' , orig_url, 641, '', page + 1, search)
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('644', ['url']) 
def v7_cat(url):
    listhtml = utils.getHtml(url, 'http://www.vidz7.com/')
    match = re.compile('li><a href="([^"]+)">(.*?)</a><span>([^<]+)<', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for catpage, name, nr in match:
        name = utils.cleantext(name) + ' [COLOR orange]' + nr.strip() + '[/COLOR]'
        utils.addDir(name, catpage, 641, '', 1)
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('645', ['url'], ['keyword'])
def v7_search(url, keyword=None):
    if not keyword:
        utils.searchDir(url, 645)
    else:
        keyword = '&s=' + keyword.replace(' ','+')
        v7_list(url, None, keyword)


@utils.url_dispatcher.register('642', ['url', 'name'], ['download'])
def v7_play(url, name, download=None):
    utils.kodilog(url)
    vp = utils.VideoPlayer(name, download=download, regex='''src\s*=\s*["']([^'"]+)''')
    vp.play_from_site_link(url)
