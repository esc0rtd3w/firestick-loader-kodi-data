'''
    Ultimate Whitecream
    Copyright (C) 2015 Whitecream

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


@utils.url_dispatcher.register('90')
def TPMain():
    utils.addDir('[COLOR hotpink]Categories[/COLOR]','http://www.bubbaporn.com/channels/',93,'','')
    utils.addDir('[COLOR hotpink]Pornstars[/COLOR]','http://www.bubbaporn.com/pornstars/page1.html',95,'','')
    utils.addDir('[COLOR hotpink]Top Rated[/COLOR]','http://www.bubbaporn.com/top-rated/a/page1.html',91,'','')
    utils.addDir('[COLOR hotpink]Most Viewed[/COLOR]','http://www.bubbaporn.com/most-viewed/a/page1.html',91,'','')
    utils.addDir('[COLOR hotpink]Search[/COLOR]','http://www.bubbaporn.com/search/page1.html?q=',94,'','')
    TPList('http://www.bubbaporn.com/page1.html',1)
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('91', ['url'], ['page'])
def TPList(url, page=1):
    try:
        listhtml = utils.getHtml(url, '')
    except:
        
        return None
    match = re.compile('src="([^"]+jpg)[^<]+[^"]+"([^"]+)">([^<]+)<[^"]+[^>]+>([^\s]+)\s', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for thumb, videourl, name, duration in match:
        if thumb.startswith('//'): thumb = 'http:' + thumb
        name = utils.cleantext(name)
        videourl = "http://www.bubbaporn.com" + videourl
        name = name + " [COLOR deeppink]" + duration + "[/COLOR]"
        utils.addDownLink(name, videourl, 92, thumb, '')
    if re.search('Next &raquo;</a>', listhtml, re.DOTALL | re.IGNORECASE):
        npage = page + 1        
        url = url.replace('page'+str(page),'page'+str(npage))
        utils.addDir('Next Page ('+str(npage)+')', url, 91, '', npage)
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('92', ['url', 'name'], ['download'])
def TPPlayvid(url, name, download=None):
    videopage = utils.getHtml(url, '')
    match = re.compile('<source src="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(videopage)
    if match:
        videourl = match[0]
        if videourl.startswith('//'): videourl = 'http:' + videourl
        if download == 1:
            utils.downloadVideo(videourl, name)
        else:
            iconimage = xbmc.getInfoImage("ListItem.Thumb")
            listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
            listitem.setInfo('video', {'Title': name, 'Genre': 'Porn'})
            xbmc.Player().play(videourl, listitem)


@utils.url_dispatcher.register('93', ['url'])
def TPCat(url):
    caturl = utils.getHtml(url, '')
    match = re.compile('<img src="([^"]+)"[^<]+<[^"]+"([^"]+)">([^<]+)<', re.DOTALL | re.IGNORECASE).findall(caturl)
    for thumb, caturl, cat in match:
        caturl = "http://www.bubbaporn.com" + caturl + "page1.html"
        utils.addDir(cat, caturl, 91, thumb, 1)
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('95', ['url'], ['page'])
def TPPornstars(url, page=1):
    pshtml = utils.getHtml(url, '')
    pornstars = re.compile("""img" src='([^']+)'[^<]+<[^"]+"([^"]+)"[^>]+>([^<]+)<.*?total[^>]+>([^<]+)<""", re.DOTALL | re.IGNORECASE).findall(pshtml)
    for img, psurl, title, videos in pornstars:
        psurl = "http://www.bubbaporn.com" + psurl + "page1.html"
        title = title + " [COLOR deeppink]" + videos + "[/COLOR]" 
        utils.addDir(title, psurl, 91, img, 1)
    if re.search('Next &raquo;</a>', pshtml, re.DOTALL | re.IGNORECASE):
        npage = page + 1
        url = url.replace('page'+str(page),'page'+str(npage))
        utils.addDir('Next Page ('+str(npage)+')', url, 95, '', npage)        
    xbmcplugin.endOfDirectory(utils.addon_handle)
    

@utils.url_dispatcher.register('94', ['url'], ['keyword'])  
def TPSearch(url, keyword=None):
    searchUrl = url
    if not keyword:
        utils.searchDir(url, 94)
    else:
        title = keyword.replace(' ','+')
        searchUrl = searchUrl + title + "&s=new"
        print "Searching URL: " + searchUrl
        TPList(searchUrl, 1)
