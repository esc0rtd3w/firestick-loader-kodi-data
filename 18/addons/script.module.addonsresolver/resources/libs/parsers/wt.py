# -*- coding: UTF-8 -*-
# by Mafarricos
# email: MafaStudios@gmail.com
# This program is free software: GNU General Public License
import os,urllib
import links,search
from resources.libs import basic

def createstrm(name,imdbid,year,url):
	addon_id = links.link().wt_id
	addon_path = os.path.join(links.link().installfolder,addon_id)
	addon_getsettings = links.link().getSetting("wt_enabled")
	addon_pos = links.link().getSetting("wt_pos")
	if len(addon_pos) == 1: addon_pos = '0'+addon_pos
	srtmBasePath = links.link().strmPath
	addonplay = links.link().wt_play

	if not os.path.exists(addon_path) and addon_getsettings == 'true': links.link().setSetting("wt_enabled",'false')
	if addon_getsettings == 'true':
		strmPath = os.path.join(srtmBasePath,addon_pos+'.'+addon_id+'.strm')
		url = search.basic_search(links.link().wt_search,name,imdbid,year,'<a href="(.+?)" class="movie-name">','NameYear')
		if url:
			playurl = addonplay % (urllib.quote_plus(links.link().wt_base % url),urllib.quote_plus(name))
			basic.writefile(strmPath,'w',playurl)