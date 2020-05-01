# -*- coding: UTF-8 -*-
# by Mafarricos
# email: MafaStudios@gmail.com
# This program is free software: GNU General Public License
import os,urllib
import links,search
from resources.libs import basic

def createstrm(name,imdbid,year,url):
	addon_id = links.link().yify_id
	addon_path = os.path.join(links.link().installfolder,addon_id)
	addon_getsettings = links.link().getSetting("yify_enabled")
	addon_pos = links.link().getSetting("yify_pos")
	addonplay = links.link().yify_play	
	if len(addon_pos) == 1: addon_pos = '0'+addon_pos
	srtmBasePath = links.link().strmPath

	if not os.path.exists(addon_path) and addon_getsettings == 'true': links.link().setSetting("yify_enabled",'false')
	if addon_getsettings == 'true':
		strmPath = os.path.join(srtmBasePath,addon_pos+'.'+addon_id+'.strm')
		searchresponse = '"title":"%s","link":"(.+?)","post_content":".+?","image":".+?","year":"%s"' % (name,year)		
		url = search.basic_search(links.link().yify_search,name,imdbid,year,searchresponse,'Name')
		if url:
			playurl = addonplay % (urllib.quote_plus(name+' ('+year+')'),urllib.quote_plus(url))
			basic.writefile(strmPath,'w',playurl)