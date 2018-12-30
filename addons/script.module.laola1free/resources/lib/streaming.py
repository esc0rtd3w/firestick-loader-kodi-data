# -*- coding: utf-8 -*-

import urllib2
import re
import string
import random
import time
import json
from urlparse import urljoin
from bs4 import BeautifulSoup
import logger

class StreamError(Exception):
	def __init__(self, message):
		self.message = message

class Stream:
	def __init__(self, url, min_bandwidth = 0, max_bandwidth = 999999999):
		self.title = None
		self.min_bandwidth = min_bandwidth
		self.max_bandwidth = max_bandwidth

		logger.debug('Get stream details url from "{}"', url)
		url = self.get_details_url(url)
		logger.debug('Get playlist url from "{}"', url)
		self.url = self.get_playlist_url(url)
		logger.debug('Playlist url is "{}"', self.url)

	def get_soup(self, url):
		source = urllib2.urlopen(url)
		soup = BeautifulSoup(source, 'html.parser')
		soup.current_url = source.geturl()
		return soup

	def find_error_reason(self, soup):
		countdown = soup.select('.live_countdown')
		if countdown and countdown[0]['data-nstreamstart'] and not countdown[0].find_parent('div', {'class': 'tabcontent'}):
			# 2016-3-19-20-30-00
			date = countdown[0]['data-nstreamstart'].encode('utf-8')
			datetime = time.strptime(date, '%Y-%m-%d-%H-%M-%S')
			date = '[B]' + time.strftime('%a, %H:%M', datetime) + '[/B]'
			return 'Stream not yet started![CR]Stream start: ' + date

		return 'Videoplayer not found!'

	def regex_first(self, text, regex):
		match = re.compile(regex, re.DOTALL).findall(text)
		if match:
			return match[0]
		return None

	def get_details_url(self, url):
		source = urllib2.urlopen(url)
		url = source.geturl()
		content = source.read()
		source.close()

		detailsurl = self.get_details_url_config(url, content)
		if detailsurl:
			return detailsurl

		detailsurl = self.get_details_url_default(url, content)
		if detailsurl:
			return detailsurl

		soup = BeautifulSoup(content, 'html.parser')

		if not self.title:
			self.title = soup.select('title')[0].get_text().strip().encode('utf-8')

		iframes = soup.select('iframe[src*=player]')

		if len(iframes) != 1:
			raise StreamError(self.find_error_reason(soup))

		return self.get_details_url(urljoin(url, iframes[0]['src']))

	def get_details_url_config(self, url, content):
		configurl = self.regex_first(content, 'configUrl: "(.+?)"')
		if not configurl:
			logger.info('"configUrl" not found in "{}"', url)
			return None

		if not self.title:
			self.title = self.regex_first(content, '<title>(.+?)</title>')

		videoid = self.regex_first(content, 'videoid: "(.+?)"')
		partnerid = self.regex_first(content, 'partnerid: "(.+?)"')
		language = self.regex_first(content, 'language: "(.+?)"')

		configurl = urljoin(url, configurl) + '?videoid=' + videoid + '&partnerid=' + partnerid + '&language=' + language + '&format=iphone'
		logger.info('Full config url: {}', configurl)
		source = urllib2.urlopen(configurl)
		content = json.load(source)
		source.close()

		logger.info('StreamAccess: {}', content['video']['streamAccess'])

		# Send POST request by passing the second parameter to Request(url, data)
		source = urllib2.urlopen(urllib2.Request(content['video']['streamAccess'], ''))
		content = json.load(source)
		source.close()

		return content['data']['stream-access'][0]

	def get_details_url_default(self, url, content):
		auth = self.regex_first(content, 'auth = "(.+?)"')
		if not auth:
			logger.info('"auth" not found in "{}"', url)
			return None

		if not self.title:
			self.title = self.regex_first(content, '<title>(.+?)</title>')

		streamid = self.regex_first(content, 'streamid: "(.+?)"')
		partnerid = self.regex_first(content, 'partnerid: "(.+?)"')
		portalid = self.regex_first(content, 'portalid: "(.+?)"')
		sprache = self.regex_first(content, 'sprache: "(.+?)"')
		timestamp = ''.join(re.compile('<!--.*?([0-9]{4})-([0-9]{2})-([0-9]{2}) ([0-9]{2}):([0-9]{2}):([0-9]{2}).*?-->', re.DOTALL).findall(content)[0])

		hdvideourl = 'http://www.laola1.tv/server/hd_video.php?play='+streamid+'&partner='+partnerid+'&portal='+portalid+'&v5ident=&lang='+sprache

		logger.debug('hd_video url is "{}"', hdvideourl)
		soup = self.get_soup(hdvideourl)

		return soup.videoplayer.url.text +'&timestamp='+timestamp+'&auth='+auth

	def char_gen(self, size=1, chars=string.ascii_uppercase):
		return ''.join(random.choice(chars) for x in range(size))

	def get_playlist_url(self, url):
		soup = self.get_soup(url)

		auth = soup.data.token['auth']
		url = soup.data.token['url']

		baseurl = url.replace('/z/', '/i/')
		return urljoin(baseurl, 'master.m3u8?hdnea=' + auth + '&g=' + self.char_gen(12) + '&hdcore=3.8.0')

	def get_title(self):
		return self.title

	def get_url(self):
		return self.url

	def get_playlist(self):
		streamurl = self.get_url()
		source = urllib2.urlopen(streamurl)
		master = source.read()
		source.close()

		playlist = '#EXTM3U\n'

		for header, bandwidth, url in re.compile('(BANDWIDTH=(.+?),.+?)\n(.+?)\n', re.DOTALL).findall(master):
			bandwidth = int(bandwidth)
			if self.min_bandwidth < bandwidth and bandwidth <= self.max_bandwidth:
				playlist += header + '\n' + urljoin(streamurl, url) + '\n'

		return playlist
