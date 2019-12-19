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
		self.key_link = random.choice(['QUl6YVN5RDd2aFpDLTYta2habTVuYlVyLTZ0Q0JRQnZWcnFkeHNz', 'QUl6YVN5Q2RiNEFNenZpVG0yaHJhSFY3MXo2Nl9HNXBhM2ZvVXd3'])
		self.key_link = '&key=%s' % base64.urlsafe_b64decode(self.key_link)
		self.search_link = 'https://www.googleapis.com/youtube/v3/search?part=id&type=video&maxResults=5&q=%s' + self.key_link
		self.youtube_watch = 'https://www.youtube.com/watch?v=%s'


	def play(self, name='', url='', windowedtrailer=0):
		try:
			url = self.worker(name, url)
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


	def worker(self, name, url):
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
			return self.search(query)


	def search(self, url):
		try:
			apiLang = control.apiLanguage().get('youtube', 'en')

			if apiLang != 'en':
				url += "&relevanceLanguage=%s" % apiLang

			result = client.request(url)

			items = json.loads(result).get('items', [])
			items = [i.get('id', {}).get('videoId') for i in items]

			for vid_id in items:
				url = self.resolve(vid_id)
				if url:
					return url
		except:
			log_utils.error()
			return

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