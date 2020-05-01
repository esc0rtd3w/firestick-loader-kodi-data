# -*- coding: UTF-8 -*-
# by Mafarricos
# email: MafaStudios@gmail.com
# This program is free software: GNU General Public License
import os,urllib
import links,search
from resources.libs import basic

def createstrm(name,imdbid,year,url):
	addon_id = links.link().sdp_id
	addon_path = os.path.join(links.link().installfolder,addon_id)
	addon_getsettings = links.link().getSetting("sdp_enabled")
	addon_getsettingspref = links.link().getSetting("pref_sdp_source")	
	addon_pos = links.link().getSetting("sdp_pos")
	if len(addon_pos) == 1: addon_pos = '0'+addon_pos
	srtmBasePath = links.link().strmPath
	addonplay = links.link().sdp_search

	if not os.path.exists(addon_path) and addon_getsettings == 'true': links.link().setSetting("sdp_enabled",'false')
	if addon_getsettings == 'true':
		strmPath = os.path.join(srtmBasePath,addon_pos+'.'+addon_id+'.strm')
		url = search.sdpsearch(name,imdbid)
		if url == 'MATCH':
			if addon_getsettingspref == 'All': automatic = ''
			elif addon_getsettingspref == 'Any': automatic = 'sim'
			else: automatic = addon_getsettingspref
			playurl= addonplay % (imdbid,urllib.quote_plus(name.replace(' ('+year+')','')),automatic)
			basic.writefile(strmPath,'w',playurl)