# -*- coding: utf-8 -*-

import sys
import base64
import json
import random
import re
import urllib

from resources.lib.modules import client
from resources.lib.modules import control
from resources.lib.modules import log_utils


class Trailer:
	def __init__(self):
		self.base_link = 'https://www.youtube.com'
		self.ytkey_link = control.addon('plugin.video.youtube').getSetting('youtube.api.key')
		self.rckey_link = random.choice(['AIzaSyA0LiS7G-KlrlfmREcCAXjyGqa_h_zfrSE', 'AIzaSyBOXZVC-xzrdXSAmau5UM3rG7rc8eFIuFw'])
		if self.ytkey_link != '':
			self.key_link = '&key=%s' % self.ytkey_link
		else:
			self.key_link = '&key=%s' % self.rckey_link
		self.search_link = 'https://www.googleapis.com/youtube/v3/search?part=id&type=video&maxResults=5&q=%s' + self.key_link
		# self.search_link = 'https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&maxResults=5&q=%s' + self.key_link
		self.youtube_watch = 'https://www.youtube.com/watch?v=%s'


	def play(self, type='', name='', year='', url='', imdb='', windowedtrailer=0):
		try:
			url = self.worker(type, name, year, url, imdb)
			if not url:
				return
			title = control.infoLabel('ListItem.Title')
			if not title:
				title = control.infoLabel('ListItem.Label')
			icon = control.infoLabel('ListItem.Icon')
			item = control.item(label=title, iconImage=icon, thumbnailImage=icon, path=url)
			item.setInfo(type="video", infoLabels={'title': title})
			item.setProperty('IsPlayable', 'true')
			control.refresh()
			control.resolve(handle=int(sys.argv[1]), succeeded=True, listitem=item)
			if windowedtrailer == 1:
				control.sleep(1000)
				while control.player.isPlayingVideo():
					control.sleep(1000)
				control.execute("Dialog.Close(%s, true)" % control.getCurrentDialogId)
		except:
			log_utils.error()


	def worker(self, type, name, year, url, imdb):
		try:
			if url.startswith(self.base_link):
				url = self.resolve(url)
				if not url:
					raise Exception()
				return url
			elif not url.startswith('http'):
				url = self.youtube_watch % url
				url = self.resolve(url)
				if not url:
					raise Exception()
				return url
			else:
				raise Exception()
		except:
			query = name + ' trailer'
			query = self.search_link % urllib.quote_plus(query)
			return self.search(query, type, name, year, imdb)


	def search(self, url, type, name, year, imdb):
		try:
			apiLang = control.apiLanguage().get('youtube', 'en')
			if apiLang != 'en':
				url += "&relevanceLanguage=%s" % apiLang
			result = client.request(url, error=True)
			if 'error' in result:
				items = json.loads(result).get('error', []).get('errors', [])
				log_utils.log('message = %s' % str(items[0].get('message')), __name__, log_utils.LOGDEBUG)
				items = self.trakt_trailer(type, name, year, imdb)
			else:
				items = json.loads(result).get('items', [])
				items = [i.get('id', {}).get('videoId') for i in items]
			for vid_id in items:
				url = self.resolve(vid_id)
				if url:
					return url
		except:
			log_utils.error()
			return


	def trakt_trailer(self, type, name, year, imdb):
		from resources.lib.modules import trakt
		#check if this needs .replace(' ', '-') between title spaces
		id = (name.lower() + '-' + year) if imdb == '0' else imdb
		if type == 'movie':
			item = trakt.getMovieSummary(id)
		else:
			item = trakt.getTVShowSummary(id)
		try:
			trailer_id = item.get('trailer').split('v=')
			trailer_id = [trailer_id[1]]
		except:
			trailer_id = ''
		return trailer_id


	def resolve(self, url):
		try:
			id = url.split('?v=')[-1].split('/')[-1].split('?')[0].split('&')[0]
			result = client.request(self.youtube_watch % id)
			message = client.parseDOM(result, 'div', attrs={'id': 'unavailable-submessage'})
			message = ''.join(message)
			alert = client.parseDOM(result, 'div', attrs={'id': 'watch7-notification-area'})
			if len(alert) > 0:
				raise Exception()
			if re.search('[a-zA-Z]', message):
				raise Exception()
			url = 'plugin://plugin.video.youtube/play/?video_id=%s' % id
			return url
		except:
			log_utils.error()
			return