# -*- coding: utf-8 -*-

import urllib
import xbmc
import xbmcgui
import xbmcplugin
from urlparse import urljoin
from caching import CacheManager
from extraction import Extractor
from streaming import Stream
from streaming import StreamError
import logger

class RequestHandler:
	def __init__(self, addonhandle, addonname, addonbaseurl, parameters, settings):
		self.addonname = addonname
		self.baseurl = 'http://www.laola1.tv/' + settings.language() + '-' + settings.location() + '/'
		self.addonhandle = addonhandle
		self.addonbaseurl = addonbaseurl
		self.settings = settings
		self.cacheManager = CacheManager(xbmc.translatePath('special://home/userdata/addon_data/' + self.addonname + '/cache'))

		self.type = self.get_param(parameters, 'type')
		self.url = self.get_param(parameters, 'url')

		id = self.get_param(parameters, 'id')
		if id is None:
			self.idParts = []
		else:
			self.idParts = self.split_id_parts(id)

	def build_url(self, query):
		return self.addonbaseurl + '?' + urllib.urlencode(query)

	def split_id_parts(self, id):
		sIds = id.split('-')
		return [int(i) for i in sIds]

	def join_id_parts(self, idParts):
		return '-'.join(str(e) for e in idParts)

	def full_id(self, id):
		return self.join_id_parts(self.idParts + [id])

	def get_param(self, parameters, key):
		return parameters.get(key, [None])[0]

	def add_folder(self, folder, id):
		image = 'DefaultFolder.png'

		if 'image' in folder:
			image = folder['image']
			if 'resource:' in image:
				image = xbmc.translatePath('special://home/addons/' + self.addonname + '/resources/' + image[9:])

		li = xbmcgui.ListItem(folder['label'], thumbnailImage=image, iconImage='DefaultFolder.png')
		parameters = { 'type': folder['type'], 'id': self.full_id(id) }
		if 'url' in folder:
			parameters['url'] = folder['url']

		xbmcplugin.addDirectoryItem(handle=self.addonhandle,
			url=self.build_url(parameters),
			listitem=li, isFolder=True)

	def add_video(self, video):
		image = 'DefaultVideo.png'

		if 'image' in video:
			image = video['image']

		li = xbmcgui.ListItem(video['label'], thumbnailImage=image, iconImage='DefaultVideo.png')
		li.setProperty("IsPlayable","true")
		xbmcplugin.addDirectoryItem(handle=self.addonhandle,
			url=self.build_url({ 'type': 'video', 'url': video['url'] }),
			listitem=li, isFolder=False)

	def add_all_entries(self, entries):
		id = 0
		for entry in entries:
			if entry['type'] == 'video':
				self.add_video(entry)
			else:
				self.add_folder(entry, id)

			id = id + 1

	def cache_clear(self):
		self.cacheManager.clear()

	def cache_load(self):
		return self.cacheManager.load(self.idParts)

	def cache_store(self, obj):
		self.cacheManager.store(obj, self.idParts)

	def handle(self):
		logger.error('handle() method not overridden!')

	def finish(self):
		xbmcplugin.endOfDirectory(self.addonhandle, True, False, True)


class ChannelHandler(RequestHandler):
	def fetch_home(self):
		extractor = Extractor(self.baseurl, self.settings)
		channels = extractor.get_channels()
		self.cache_clear()
		self.cacheManager.store(channels)

		return channels

	def handle(self):
		if len(self.idParts) == 0:
			channelsOrBlocks = self.fetch_home()
		else:
			channel = self.cache_load()

			if not channel:
				self.fetch_home()
				channel = self.cache_load()

			if 'children' in channel:
				channelsOrBlocks = channel['children']
			else:
				extractor = Extractor(channel['url'], self.settings)
				channelsOrBlocks = extractor.get_blocks()
				self.cache_store(channelsOrBlocks)

		self.add_all_entries(channelsOrBlocks)

class LiveBlockHandler(RequestHandler):
	def handle(self):
		block = self.cache_load()
		extractor = Extractor(block['url'], self.settings)
		videos = extractor.get_live_videos()

		livefilter = self.settings.livefilter()
		logger.debug('Filtering live streams for {}.', livefilter)
		if livefilter != 'all':
			videos = [video for video in videos if 'sport' in video and video['sport'] == livefilter]

		self.add_all_entries(videos)

class BlockHandler(RequestHandler):
	def handle(self):
		if self.url is None:
			block = self.cache_load()
		else:
			logger.debug('Load block from "{}"', self.url)
			block = { 'url': self.url }

		logger.debug('Block: {}', block)

		if 'url' in block:
			extractor = Extractor(block['url'], self.settings)
			videos = extractor.get_videos()
		else:
			videos = block['children']

		self.add_all_entries(videos)

class VideoHandler(RequestHandler):
	def handle(self):
		try:
			stream = Stream(self.url)
			#print 'Playlist: ' + stream.get_playlist()
			li = xbmcgui.ListItem(path=stream.get_url())
			li.setInfo( type="Video", infoLabels={ "Title": stream.get_title() } )
			xbmcplugin.setResolvedUrl(self.addonhandle, True, li)
		except StreamError as e:
			xbmcgui.Dialog().ok('Error', e.message)
			xbmcplugin.setResolvedUrl(self.addonhandle, False, xbmcgui.ListItem())
