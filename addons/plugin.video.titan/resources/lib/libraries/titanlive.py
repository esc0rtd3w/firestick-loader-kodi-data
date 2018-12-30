# -*- coding: utf-8 -*-

'''
    Titan Add-on
    Copyright (C) 2016 SchisM

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


import xbmc
import re,sys,urllib,urllib2,urlparse,base64,urlresolver,random,xbmcgui,xbmcplugin
import threading
from t0mm0.common.addon import Addon
global loop
loop = 1
xbmcPlayer = xbmc.Player()
addon_id = 'plugin.video.titan'
addon = Addon(addon_id, sys.argv)

def fetch_random(url):
		link = open_url(url)
		dp = xbmcgui.DialogProgress()
		dp.create("Opening", 'Please wait')
		dp.update(0)
		count=0
		random_all = []
		if max_list != '':
			try:
				match=re.compile('name=(.+?)\s*thumb=(.+?)\s*URL=(.+?)\s*player=').findall(link)
				for name,thumb,url in match: random_all.append([name,thumb,url])
				for name,thumb,url in random_all:
					if count < float(max_list):
						index = random.randrange(1, len(random_all))
						addlink = random_all[index][2]
						addname = random_all[index][0]
						addthumb = random_all[index][1]
						count+=1
						progress = (float(count) / float(max_list)) * 100
						dp.update(int(progress), 'Populating 24/7 List: ', addname)
						url = urlresolver.HostedMediaFile(addlink).resolve()
						if url:
							randomitem.append([addname,addthumb,url])
			except: pass
def fetch_hifi(url):
		link = open_url(url)
		dp = xbmcgui.DialogProgress()
		dp.create("Opening", 'Please wait')
		dp.update(0)
		count=0
		random_all_hifi = []
		if max_list != '':
			try:
				match2=re.compile('name=(.+?)\s*URL=(.+?)\s*thumb=(.+?)\s*player=').findall(link)
				for name,url,thumb in match2: random_all_hifi.append([name,url,thumb])
				for name,url,thumb in random_all_hifi:
					if count < float(max_list):
						index = random.randrange(1, len(random_all_hifi))
						addlink = random_all_hifi[index][1]
						addname = random_all_hifi[index][0]
						addthumb = random_all_hifi[index][2]
						count+=1
						progress = (float(count) / float(max_list)) * 100
						dp.update(int(progress), 'Populating 24/7 List: ', addname)
						url = urlresolver.HostedMediaFile(addlink).resolve()
						if url:
							randomitem_two.append([addname,url,addthumb])
			except: pass
def randomtv(url):
	global randomitem ; randomitem = []
	global randomitem_two ; randomitem_two = []
	global max_list
	randomurl = [url] 
	max_list = '10'
	keyboard = xbmc.Keyboard(max_list, 'MAX ITEMS TO WATCH:')
	keyboard.doModal()
	if keyboard.isConfirmed(): max_list = keyboard.getText()
	threads = [threading.Thread(target=fetch_random, args=(url,)) for url in randomurl]
	for thread in threads:thread.start()
	for thread in threads: thread.join()
	threads_hifi = [threading.Thread(target=fetch_hifi, args=(url,)) for url in randomurl]
	for thread in threads_hifi:thread.start()
	for thread in threads_hifi: thread.join()
	ret_url = []
	playlist = xbmc.PlayList(0)
	playlist.clear()
	for name, thumb, url in randomitem:
			playlink = url
			playname = name
			playthumb = thumb
			liz=xbmcgui.ListItem(playname, iconImage=playthumb, thumbnailImage=playthumb); liz.setInfo( type="Video", infoLabels={ "Title": playname} )
			playlist.add( url=str(playlink), listitem=liz )
	for name, url, thumb in randomitem_two:
			playlink = url
			playname = name
			playthumb = thumb
			liz=xbmcgui.ListItem(playname, iconImage=playthumb, thumbnailImage=playthumb); liz.setInfo( type="Video", infoLabels={ "Title": playname} )
			playlist.add( url=str(playlink), listitem=liz )
	xbmc.Player().play( playlist )
	addLink('Press back to exit','',1,'','')

def addLink(name,url,mode,iconimage,description=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage='')
        
        liz.setProperty("IsPlayable","true")
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
def open_url(url):
        # url=url.replace(' ','%20')
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        return link

