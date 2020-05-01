# -*- coding: UTF-8 -*-
# by Mafarricos
# email: MafaStudios@gmail.com
# This program is free software: GNU General Public License
import os,urllib
import links,search
from resources.libs import basic

def createstrm(name,imdbid,year,url):
	addon_id = links.link().stream_id
	addon_path = os.path.join(links.link().installfolder,addon_id)
	addon_getsettings = links.link().getSetting("stream_enabled")
	addon_pos = links.link().getSetting("stream_pos")
	if len(addon_pos) == 1: addon_pos = '0'+addon_pos
	srtmBasePath = links.link().strmPath
	addonplay = links.link().stream_play

	if not os.path.exists(addon_path) and addon_getsettings == 'true': links.link().setSetting("stream_enabled",'false')
	if addon_getsettings == 'true':
		qual,magnet = search.ytssearch(imdbid)
		if magnet:
			for i in range(0,len(magnet)):
				strmPath = os.path.join(srtmBasePath,addon_pos+'.'+addon_id+'.'+qual[i]+'.strm')
				playurl = addonplay % (urllib.quote_plus(magnet[i]))
				basic.writefile(strmPath,'w',playurl)