# -*- coding: UTF-8 -*-
# by Mafarricos
# email: MafaStudios@gmail.com
# This program is free software: GNU General Public License
import os,urllib
import links,search
from resources.libs import basic

def createstrm(name,imdbid,year,url):
	addon_id = links.link().rato_id
	addon_path = os.path.join(links.link().installfolder,addon_id)
	addon_getsettings = links.link().getSetting("rato_enabled")
	addon_pos = links.link().getSetting("rato_pos")
	if len(addon_pos) == 1: addon_pos = '0'+addon_pos
	srtmBasePath = links.link().strmPath
	addonplay = links.link().rato_play
	
	if not os.path.exists(addon_path) and addon_getsettings: links.link().setSetting("rato_enabled",'false')
	if addon_getsettings == 'true':
		strmPath = os.path.join(srtmBasePath,addon_pos+'.'+addon_id+'.strm')
		url = search.basic_search(links.link().rato_search,name,imdbid,year,'<span class="more-btn"><a href="(.+?)" >Ver Agora</a>','IMDB')
		if url:
			playurl = addonplay % (url,urllib.quote_plus(name))
			basic.writefile(strmPath,'w',playurl)