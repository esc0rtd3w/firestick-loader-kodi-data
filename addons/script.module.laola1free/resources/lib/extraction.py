# -*- coding: utf-8 -*-

import urllib2
import string
import time
import re
from urlparse import urljoin
from bs4 import BeautifulSoup
import logger

class Extractor:
	def __init__(self, baseurl, settings):
		self.baseurl = baseurl
		self.settings = settings

	def get_soup(self, additional_remove=None):
		if self.settings.htmlstripping():
			remove = r'<head.*</head>|<!--.*?-->|<script.*?</script>|<footer.*?</footer>'
			if additional_remove:
				remove = remove + r'|' + additional_remove

			source = urllib2.urlopen(self.baseurl)
			html = source.read()
			beforelen = len(html)
			html = re.sub(r'\s+', ' ', html, flags = re.MULTILINE)
			html = re.sub(remove, '', html, flags = re.IGNORECASE)
			logger.debug('HTML data length stripping - before: {} - after: {}', beforelen, len(html))

			return BeautifulSoup(html, 'html.parser')
		else:
			logger.debug('No HTML data length stripping')
			return BeautifulSoup(urllib2.urlopen(self.baseurl), 'html.parser')

	def get_text(self, item):
		return item.get_text().strip().encode('utf-8')

	def get_url(self, url):
		return urljoin(self.baseurl, url.encode('utf-8'))

	def days1970(self, datetime):
		# days since 1.1.1970 -> close enough
		return 365 * (datetime.tm_year - 1970) + datetime.tm_yday

	def days_between(self, time1, time2):
		return self.days1970(time2) - self.days1970(time1)

	def determine_icon(self, s):
		if 'volley' in s or 'handball' in s:
			return 'resource:icons/volleyball.png'
		if 'football' in s:
			return 'resource:icons/soccer.png'
		if 'hockey' in s:
			return 'resource:icons/hockey.png'
		if 'basketball' in s:
			return 'resource:icons/basketball.png'
		if 'motorsports' in s:
			return 'resource:icons/motorsport.png'
		if 'tennis' in s:
			return 'resource:icons/tennis.png'
		if 'all' in s:
			return 'resource:icons/gymnastics.png'
		return 'DefaultFolder.png'

	def extract_channels(self, nodes):
		items = []
		for child in nodes:
			if child.span is not None and child.ul is not None:
				children = self.extract_channels(child.ul.find_all('li', recursive=False))
				if children:
					item = {
						'label': self.get_text(child.span),
						'children': children,
						'type': 'channel'
					}

					if child.span.i:
						item['image'] = self.determine_icon(' '.join(child.span.i['class']))
						logger.debug('Using {} as icon for {}', item['image'], item['label'])

					items.append(item)
					continue

			if child.a is not None:
				link = child.a
				text = self.get_text(link)
				if not text:
					continue

				item = {
					'label': text,
					'url': self.get_url(link['href']),
					'type': 'channel'
				}

				if link.img:
					item['image'] = self.get_url(link.img['src'])
					logger.debug('Using {} as icon for {}', item['image'], item['label'])

				items.append(item)

		return items

	def extract_live_block(self, parent):
		link = self.first(parent, '.meta a.live')

		return {
			'label': self.get_text(link.span) + ' ([COLOR red]' + self.get_text(link.i) + '[/COLOR])',
			'type': 'live-block',
			'url': self.get_url(link['href'])
		}

	def extract_blocks(self, parent):
		list = []
		for node in parent.select('.teaser-wrapper'):
			title = node.select('.teaser-title')[0]

			if title.a is not None and title.a.h2 is not None:
				item = {
					'label': self.get_text(title.a.h2),
					'url': self.get_url(title.a['href']),
					'type': 'block'
				}

				imagenode = self.first(node, '.teaser-list .teaser img')
				if imagenode:
					item['image'] = self.get_url(imagenode['src'])

				list.append(item)
				continue

			if title.h2 is not None:
				children = self.extract_videos(node)

				if children:
					list.append({
						'label': self.get_text(title.h2),
						'children': children,
						'image': self.get_url(node.select('.teaser-list .teaser img')[0]['src']),
						'type': 'block'
					})

		return list

	def extract_live_videos(self, parent):
		now = time.localtime()
		livelimit = self.settings.livelimit()

		list = []
		for item in parent.select('.list-day .item'):
			live = False
			h2s = item.select('.heading h2')
			if not h2s:
				logger.debug('No heading found for {}', self.minify(item))
				continue

			datas = item.select('.badge a > div')

			if datas:
				data = datas[0]

				if int(data['data-sstatus'].encode('utf-8')) == 4:
					live = True
					date = '[COLOR red]LIVE[/COLOR] - '
				else:
					# 2016-1-30-20-30-00
					date = data['data-nstreamstart'].encode('utf-8')
					datetime = time.strptime(date, '%Y-%m-%d-%H-%M-%S')
			else:
				infos = item.select('.info > dl')

				if not infos:
					logger.debug('No time information for {}', self.minify(item))
					continue

				startlabel = infos[0].find(text='Streamstart:')
				if not startlabel:
					logger.debug('No start label in {}', self.minify(item))
					continue;

				start = startlabel.parent.find_next_siblings('dd', limit=1)[0]

				# 19.03.2016 18:00
				date = self.get_text(start).split(' ', 1)[-1]
				datetime = time.strptime(date, '%d.%m.%Y %H:%M')

			if not live:
				daysfromnow = self.days_between(now, datetime)
				if livelimit and daysfromnow >= livelimit:
					break

				if daysfromnow < 7:
					date = '[B]' + time.strftime('%a, %H:%M', datetime) + '[/B] - '
				else:
					date = '[B]' + time.strftime('%a, %d.%m. - %H:%M', datetime) + '[/B] - '

			video = {
				'label': date + self.get_text(h2s[0]),
				'url': self.get_url(item.select('a')[0]['href']),
				'type': 'video'
			}

			image = self.first(item, '.logo img')
			if image:
				video['image'] = self.get_url(image['src'])

			sport = self.first(item, '.sport i[class]')
			if sport:
				for cl in sport['class']:
					if cl.startswith('ico-sports-'):
						video['sport'] = cl[11:]

			list.append(video)

		return list

	def extract_next_page_link(self, parent):
		nexts = parent.select('.paging .next')
		if nexts and 0 < len(nexts):
			return {
				'label': 'More...',
				'url': self.get_url(nexts[0].find_parent('a')['href']),
				'type': 'block'
			}

		return None

	def extract_videos(self, parent):
		children = []
		for teaser in parent.select('.teaser-list .teaser a'):
			badge = self.first(teaser, '.date')
			if not badge:
				badge = self.first(teaser, '.badge')

			date = self.get_text(badge)

			if 'live' in badge['class']:
				# Fri 19.02.2016  19:10
				date = date[4:]
				datetime = time.strptime(date, '%d.%m.%Y  %H:%M')
				starttime = ' - [COLOR red]' + time.strftime('%H:%M', datetime) + '[/COLOR]'
			else:
				# 10.01.2016
				datetime = time.strptime(self.get_text(badge), '%d.%m.%Y')
				starttime = ''

			date = '[B]' + time.strftime('%a, %d.%m.%Y', datetime) + '[/B] - '

			children.append({
				'label': date + self.get_text(teaser.find('p', recursive=False)) + starttime,
				'url': self.get_url(teaser['href']),
				'image': self.get_url(teaser.select('img')[0]['src']),
				'type': 'video'
			})

		return children

	def first(self, parent, selector):
		nodes = parent.select(selector)

		if len(nodes) == 0:
			return None

		return nodes[0]

	def minify(self, input):
		return re.sub('[\r\n ]+', ' ', str(input))

	def get_channels(self):
		soup = self.get_soup(r'<main.*?</main>')
		try:
			return [self.extract_live_block(soup)] + self.extract_channels(soup.select('.quick-browse .level1 > li'))
		except:
			logger.error('Failed to extract channels from url "{}" - html: {}', self.baseurl, self.minify(soup))
			raise

	def get_blocks(self):
		soup = self.get_soup(r'<header.*?</header>')
		try:
			return self.extract_blocks(soup)
		except:
			logger.error('Failed to extract blocks from url "{}" - html: {}', self.baseurl, self.minify(soup))
			raise

	def get_live_videos(self):
		soup = self.get_soup(r'<header.*?</header>')
		try:
			return self.extract_live_videos(soup)
		except:
			logger.error('Failed to extract live videos from url "{}" - html: {}', self.baseurl, self.minify(soup))
			raise

	def get_videos(self):
		soup = self.get_soup(r'<header.*?</header>')
		try:
			videos = self.extract_videos(soup)
			next = self.extract_next_page_link(soup)
			if next:
				videos.append(next)

			return videos
		except:
			logger.error('Failed to extract videos from url "{}" - html: {}', self.baseurl, self.minify(soup))
			raise