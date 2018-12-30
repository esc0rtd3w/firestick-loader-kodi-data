'''
    Ultimate Whitecream
    Copyright (C) 2018 Whitecream, holisticdioxide

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

import xbmc
import xbmcplugin
import xbmcgui
from resources.lib import utils
 
progress = utils.progress


@utils.url_dispatcher.register('60')
def PAQMain():
    utils.addDir('[COLOR hotpink]Categories[/COLOR]','http://www.pornaq.com',63,'','')
    utils.addDir('[COLOR hotpink]Search[/COLOR]','http://www.pornaq.com/page/1/?s=',68,'','')
    PAQList('http://www.pornaq.com/page/1/',1)
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('64')
def P00Main():
    utils.addDir('[COLOR hotpink]Categories[/COLOR]','http://www.porn00.org',63,'','')
    utils.addDir('[COLOR hotpink]Search[/COLOR]','http://www.porn00.org/page/1/?s=',68,'','')
    PAQList('http://www.porn00.org/page/1/',1)
    xbmcplugin.endOfDirectory(utils.addon_handle)    


@utils.url_dispatcher.register('61', ['url'], ['page'])
def PAQList(url, page=1, onelist=None):
    if onelist:
        url = url.replace('page/1/','page/'+str(page)+'/')
    try:
        listhtml = utils.getHtml(url, '')
    except:
        
        return None
    if 'pornaq' in url:
        match = re.compile(r'<h2>\s+<a title="([^"]+)" href="([^"]+)".*?src="([^"]+)" class="attachment-primary-post-thumbnail', re.DOTALL | re.IGNORECASE).findall(listhtml)
        for name, videopage, img in match:
            name = utils.cleantext(name)
            utils.addDownLink(name, videopage, 62, img, '')
    elif 'porn00' in url:
        match = re.compile('<h2>\s+<a title="([^"]+)" href="([^"]+)".*?src="([^"]+)" class="attachment-primary-post-thumbnail', re.DOTALL | re.IGNORECASE).findall(listhtml)
        for name, videopage, img in match:
            name = utils.cleantext(name)
            utils.addDownLink(name, videopage, 62, img, '')    
    if not onelist:
        if re.search("<span class='current'>\d+?</span><span>", listhtml, re.DOTALL | re.IGNORECASE):
            npage = page + 1        
            url = url.replace('page/'+str(page)+'/','page/'+str(npage)+'/')
            utils.addDir('Next Page ('+str(npage)+')', url, 61, '', npage)
        xbmcplugin.endOfDirectory(utils.addon_handle)


def get_porn00(url):
    videopage = utils.getHtml(url)
    try:
        alternatives_div = re.compile('<div id="alternatives">(.*?)</div', re.DOTALL | re.IGNORECASE).search(videopage).group(1)
        alternatives = re.compile('''href=['"]([^'"]+)['"]''', re.DOTALL | re.IGNORECASE).findall(alternatives_div)
        for alternative in alternatives:
            videopage += utils.getHtml(alternative)
    except AttributeError:
        pass
    return '\n'.join(re.compile('<div class="video-box">(.*?)</iframe', re.DOTALL | re.IGNORECASE).findall(videopage))


def get_pornaq(url):
    videopage = utils.getHtml(url)
    return re.compile('<div class="imatge alta">(.*?)</iframe', re.DOTALL | re.IGNORECASE).search(videopage).group(1)


@utils.url_dispatcher.register('62', ['url', 'name'], ['download'])
def PPlayvid(url, name, download=None):
    vp = utils.VideoPlayer(name, download)
    vp.progress.update(25, "", "Loading video page", "")
    html = get_pornaq(url) if 'pornaq' in url else get_porn00(url)
    vp.play_from_html(html)


@utils.url_dispatcher.register('63', ['url'])
def PCat(url):
    caturl = utils.getHtml(url, '')
    cathtml = re.compile('<ul id="categorias">(.*?)</html>', re.DOTALL | re.IGNORECASE).findall(caturl)
    if 'pornaq' in url:
        match = re.compile("""<li.*?href=(?:'|")(/[^'"]+)(?:'|").*?>([^<]+)""", re.DOTALL | re.IGNORECASE).findall(cathtml[0])
    elif 'porn00' in url:
        match = re.compile("""<li.*?href=(?:'|")([^'"]+)(?:'|").*?>([^<]+)""", re.DOTALL | re.IGNORECASE).findall(cathtml[0])
    for videolist, name in match:
        if 'pornaq' in url:
            videolist = "http://www.pornaq.com" + videolist + "page/1/"
            utils.addDir(name, videolist, 61, '', 1)
        elif 'porn00' in url:
            videolist = videolist + "page/1/"
            utils.addDir(name, videolist, 61, '', 1)            
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('68', ['url'], ['keyword'])
def PSearch(url, keyword=None):
    searchUrl = url
    if not keyword:
        utils.searchDir(url, 68)
    else:
        title = keyword.replace(' ','+')
        searchUrl = searchUrl + title
        PAQList(searchUrl, 1)
