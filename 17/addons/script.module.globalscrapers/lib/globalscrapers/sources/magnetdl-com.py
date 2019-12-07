import xbmc
import xbmcaddon
import re
import urllib
import urlparse
from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import proxy
from resources.lib.modules import torrent

class source:
	def __init__(self):
		self.priority = 1
		self.language = ['en']
		self.domains = ['magnetdl.com']
		self.base_link = 'http://www.magnetdl.com'
		self.search_link = '/%s/%s/%s/'
		
		privateToken = xbmcaddon.Addon('plugin.video.resistance').getSetting('private.rd.enable')
		if privateToken == 'true':
			self.token = xbmcaddon.Addon('plugin.video.resistance').getSetting('private.rd.api')
		else:
			self.token = xbmcaddon.Addon('script.realdebrid.mod').getSetting('rd_access')

	def movie(self, imdb, title, localtitle, aliases, year):
		if xbmc.getCondVisibility('System.HasAddon(script.realdebrid.mod)'):
			try:
				title = cleantitle.geturl(title)
				url = '%s-%s' % (title,year)
				return url
			except:
				return
			
	def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
		if xbmc.getCondVisibility('System.HasAddon(script.realdebrid.mod)'):
			try:
				url = cleantitle.geturl(tvshowtitle)
				return url
			except:
				return
 
	def episode(self, url, imdb, tvdb, title, premiered, season, episode):
		try:
			if not url: return
			season = '%02d' % int(season)
			episode = '%02d' % int(episode)
			url = '%s-s%se%s' % (url,str(season),str(episode))
			return url
		except:
			return

	def sources(self, url, hostDict, hostprDict):
		try:
			sources = []
			q = url
			
			try: # Page 1
				page = '1'
				url = self.base_link + self.search_link % (q[0],q,page)
				r = client.request(url)
				match = re.compile('href="magnet\:\?xt=urn\:btih\:(.+?)&').findall(r)
				for url in match: 
					torrenturl = url
					
					# Find infohash
					hash = url
					url = 'https://api.real-debrid.com/rest/1.0/torrents/instantAvailability/%s?auth_token=%s' % (hash,self.token)
						
					# Check availability
					r = client.request(url)
					r = r.replace('	','').replace('\n','').replace('[','').replace(']','').replace('\/','/').replace('{','')
					r = r.replace('"rd": ',',')
					match = re.compile(',"(.+?)": "filename": "(.+?)"').findall(r)
					for id,filename in match:
						quality = torrent.qualityCheck(filename)
						torrenturl = 'magnet:?xt=urn:btih:' + hash
						# Check video isn't sample
						for check in torrent.check_filename:
							if check in filename:
								if '.mkv' in filename or '.mp4' in filename or '.flv' in filename or '.avi' in filename:
									url = 'url="%s"&filename="%s"&id="%s"' % (torrenturl,filename,id)
									sources.append({'source': 'Torrent','info': filename,'quality': quality,'language': 'en','url': url,'direct': False,'debridonly': False})
			except: return
			
			try: # Page 2
				page = '2'
				url = self.base_link + self.search_link % (q[0],q,page)
				r = client.request(url)
				match = re.compile('href="magnet\:\?xt=urn\:btih\:(.+?)&').findall(r)
				for url in match: 
					torrenturl = url
					
					# Find infohash
					hash = url
					url = 'https://api.real-debrid.com/rest/1.0/torrents/instantAvailability/%s?auth_token=%s' % (hash,self.token)
						
					# Check availability
					r = client.request(url)
					r = r.replace('	','').replace('\n','').replace('[','').replace(']','').replace('\/','/').replace('{','')
					r = r.replace('"rd": ',',')
					match = re.compile(',"(.+?)": "filename": "(.+?)"').findall(r)
					for id,filename in match:
						quality = torrent.qualityCheck(filename)
						torrenturl = 'magnet:?xt=urn:btih:' + hash
						# Check video isn't sample
						for check in torrent.check_filename:
							if check in filename:
								if '.mkv' in filename or '.mp4' in filename or '.flv' in filename or '.avi' in filename:
									url = 'url="%s"&filename="%s"&id="%s"' % (torrenturl,filename,id)
									sources.append({'source': 'Torrent','info': filename,'quality': quality,'language': 'en','url': url,'direct': False,'debridonly': False})
			except: return

		except Exception:
			return
		return sources

	def resolve(self, url):
		match = re.compile('url="(.+?)"&filename="(.+?)"&id="(.+?)"').findall(url)
		# Fetch magnet link
		for url,filename,id in match:
			
			id = id
			filename = filename.replace('[','').replace(']','').replace('(','').replace(')','')
			magnetLink = urllib.quote_plus(url)
			
			# Pass on to script.realdebrid.mod...
			import xbmc
			if id == '1': xbmc.executebuiltin('RunPlugin(plugin://script.realdebrid.mod/?fanart=na&icon=na&mode=4&name=na&poster=na&link='+magnetLink+'&url)')
			if id == '2': xbmc.executebuiltin('RunPlugin(plugin://script.realdebrid.mod/?fanart=na&icon=na&mode=14&name=na&poster=na&link='+magnetLink+'&url)')
			if id == '3': xbmc.executebuiltin('RunPlugin(plugin://script.realdebrid.mod/?fanart=na&icon=na&mode=15&name=na&poster=na&link='+magnetLink+'&url)')
			if id == '4': xbmc.executebuiltin('RunPlugin(plugin://script.realdebrid.mod/?fanart=na&icon=na&mode=16&name=na&poster=na&link='+magnetLink+'&url)')
			if id == '5': xbmc.executebuiltin('RunPlugin(plugin://script.realdebrid.mod/?fanart=na&icon=na&mode=17&name=na&poster=na&link='+magnetLink+'&url)')
			if id == '6': xbmc.executebuiltin('RunPlugin(plugin://script.realdebrid.mod/?fanart=na&icon=na&mode=18&name=na&poster=na&link='+magnetLink+'&url)')
			if id == '7': xbmc.executebuiltin('RunPlugin(plugin://script.realdebrid.mod/?fanart=na&icon=na&mode=19&name=na&poster=na&link='+magnetLink+'&url)')
			if id == '8': xbmc.executebuiltin('RunPlugin(plugin://script.realdebrid.mod/?fanart=na&icon=na&mode=20&name=na&poster=na&link='+magnetLink+'&url)')
			if id == '9': xbmc.executebuiltin('RunPlugin(plugin://script.realdebrid.mod/?fanart=na&icon=na&mode=21&name=na&poster=na&link='+magnetLink+'&url)')
			if id == '10': xbmc.executebuiltin('RunPlugin(plugin://script.realdebrid.mod/?fanart=na&icon=na&mode=22&name=na&poster=na&link='+magnetLink+'&url)')
			
			import time
			time.sleep(3)
					
			api = 'https://api.real-debrid.com/rest/1.0/torrents?auth_token=%s' % self.token
			r = client.request(api)
			r = r.replace('	','').replace('\n','').replace('[','').replace(']','').replace('\/','/').replace('(','').replace(')','')
			match = re.compile('"filename": "'+filename+'","hash": ".+?","bytes": .+?,"host": ".+?","split": .+?,"progress": 100,"status": "downloaded","added": ".+?","links": "https://real-debrid\.com/d/(.+?)"').findall(r)
			for url in match: 
				url = 'plugin://script.realdebrid.mod/?url=https://real-debrid.com/d/%s&mode=5&name=Real-Debrid&icon=none&fanart=none&poster=none' % url
				return url
