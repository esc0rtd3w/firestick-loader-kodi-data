# -*- coding: UTF-8 -*-
# by Mafarricos
# email: MafaStudios@gmail.com
# This program is free software: GNU General Public License
import re,xbmcgui,xbmcaddon,xbmc,os,urllib,json,xbmcplugin,threading
import basic
from parsers import genesis,rato,wt,sdp,kmedia,stream,abelhas,salts,ice,yify,muchm,links

getSetting 		= links.link().getSetting
dummy_file		= links.link().dummy_file
dataPath 		= links.link().dataPath
strmPath 		= links.link().strmPath
language		= links.link().language

if not os.path.exists(dataPath): os.makedirs(dataPath)
if not os.path.exists(strmPath): os.makedirs(strmPath)
basic.removestrm(strmPath)

class play:	
	def runall(self,name,imdbid,year,url):
		threads = []
		threads.append(threading.Thread(name='genesis',target=genesis.createstrm,args=(name,imdbid,year,url, )))
		threads.append(threading.Thread(name='rato',target=rato.createstrm,args=(name,imdbid,year,url, )))
		threads.append(threading.Thread(name='wt',target=wt.createstrm,args=(name,imdbid,year,url, )))
		threads.append(threading.Thread(name='sdp',target=sdp.createstrm,args=(name,imdbid,year,url, )))
		threads.append(threading.Thread(name='kmedia',target=kmedia.createstrm,args=(name,imdbid,year,url, )))
		threads.append(threading.Thread(name='stream',target=stream.createstrm,args=(name,imdbid,year,url, )))
		threads.append(threading.Thread(name='abelhas',target=abelhas.createstrm,args=(name,imdbid,year,url, )))
		threads.append(threading.Thread(name='salts',target=salts.createstrm,args=(name,imdbid,year,url, )))
		threads.append(threading.Thread(name='ice',target=ice.createstrm,args=(name,imdbid,year,url, )))
		threads.append(threading.Thread(name='yify',target=yify.createstrm,args=(name,imdbid,year,url, )))
		threads.append(threading.Thread(name='muchm',target=muchm.createstrm,args=(name,imdbid,year,url, )))		
		[i.start() for i in threads]
		[i.join() for i in threads]	
		
	def _play(self,link,external):
		if 'icefilms' in link:
			link = basic.readoneline(link)
			xbmc.executebuiltin('activatewindow(video,'+link+')')
		else:
			if external <> 'external': xbmc.Player().play(link)
			else:
				playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
				playlist.clear()
				playlist.add(dummy_file)
				playlist.add(link)		
				xbmc.Player().play(playlist)		
				xbmc.executebuiltin('XBMC.ActivateWindow("fullscreenvideo")')
				xbmc.executebuiltin("XBMC.PlayerControl(Play)")

	def play_stream(self,name,url,imdbid,year):
		if name.split(' (')[0]: name = name.split(' (')[0]
		fromwhere = url
		choose1 = -1
		addonchoice = xbmcgui.Dialog().select
		playurl = ''
		addons = []
		paths = []
		if 'genesis' in getSetting("pref_addon").lower(): genesis.createstrm(name,imdbid,year,url)
		elif 'rato' in getSetting("pref_addon").lower(): rato.createstrm(name,imdbid,year,url)
		elif 'wareztuga' in getSetting("pref_addon").lower(): wt.createstrm(name,imdbid,year,url)
		elif 'sites_dos_portugas' in getSetting("pref_addon").lower(): sdp.createstrm(name,imdbid,year,url)
		elif 'kmedia' in getSetting("pref_addon").lower(): kmedia.createstrm(name,imdbid,year,url)
		elif 'stream' in getSetting("pref_addon").lower(): stream.createstrm(name,imdbid,year,url)
		elif 'abelhas' in getSetting("pref_addon").lower(): abelhas.createstrm(name,imdbid,year,url)
		elif 'ice' in getSetting("pref_addon").lower(): ice.createstrm(name,imdbid,year,url)
		elif 'yify' in getSetting("pref_addon").lower(): yify.createstrm(name,imdbid,year,url)
		elif 'muchm' in getSetting("pref_addon").lower(): muchm.createstrm(name,imdbid,year,url)
		elif getSetting("pref_addon") == '-': self.runall(name,imdbid,year,url)
		paths = basic.getstrm(strmPath)
		if not paths and getSetting("pref_addon") <> '-': 
			self.runall(name,imdbid,year,url)
			paths = basic.getstrm(strmPath)
			if not paths:  basic.infoDialog(language(30003))
		if paths:
			for path in paths:
				addonstring = path.split('plugin.video.')[1].replace('.strm','').upper()
				addons.append(addonstring)
			if len(addons) == 1: choose1 = 0
			else: choose1=addonchoice(language(30004),addons)
		else: basic.infoDialog(language(30003))
		if choose1 > -1: self._play(paths[choose1],fromwhere)