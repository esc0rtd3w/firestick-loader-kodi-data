# -*- coding: utf-8 -*-

import re, xbmc
import urllib, urllib2
import requests, json

from resources.lib.modules import control, client
from resources.lib.modules import log_utils

# from resolveurl import common
# from resolveurl.common import i18n
# from resolveurl.resolver import ResolveUrl, ResolverError

try:
	from resolveurl.plugins.premiumize_me import PremiumizeMeResolver
	token = PremiumizeMeResolver.get_setting('token')
except:
	pass

CLIENT_ID = '522962560'
USER_AGENT = 'ResolveURL for Kodi/%s' % control.getKodiVersion()

# Supported video formats
FORMATS = ['.aac', '.asf', '.avi', '.flv', '.m4a', '.m4v', '.mka', '.mkv', '.mp4', '.mpeg', '.nut', '.ogg']

BaseUrl = "https://www.premiumize.me/api"
DirectDownload = '%s/transfer/directdl' % BaseUrl
AccountURL = "%s/account/info" % BaseUrl
ListFolder = "%s/folder/list" % BaseUrl
ItemDetails = "%s/item/details" % BaseUrl
TransferList = "%s/transfer/list" % BaseUrl
TransferCreate = "%s/transfer/create" % BaseUrl
TransferDelete = "%s/transfer/delete" % BaseUrl
CacheCheck = '%s/cache/check' % BaseUrl


class PremiumizeMe:
	def __init__(self):
		self.hosts = []
		self.patterns = []
		self.headers = {'User-Agent': USER_AGENT, 'Authorization': 'Bearer %s' % token}


	def get_media_url(self, host, media_id, cached_only=False):
		torrent = False
		cached = self.check_cache(media_id)
		media_id_lc = media_id.lower()

		if cached:
			log_utils.log('Premiumize.me: %s is readily available to stream' % media_id, log_utils.LOGDEBUG)
			if media_id_lc.endswith('.torrent') or media_id_lc.startswith('magnet:'):
				torrent = True
		elif media_id_lc.endswith('.torrent') or media_id_lc.startswith('magnet:'):
			if self.get_setting('cached_only') == 'true' or cached_only:
				raise ResolverError('Premiumize.me: Cached torrents only allowed to be initiated')

			torrent = True
			log_utils.log('Premiumize.me: initiating transfer to cloud for %s' % media_id, log_utils.LOGDEBUG)
			self.__initiate_transfer(media_id)
			self.__clear_finished()
			# self.__delete_folder()

		link = self.__direct_dl(media_id, torrent=torrent)
		if link is not None:
			log_utils.log('Premiumize.me: Resolved to %s' % link, log_utils.LOGDEBUG)
			return link + self.append_headers(self.headers)
		raise ResolverError('Link Not Found')


	def append_headers(self, headers):
		return '|%s' % '&'.join(['%s=%s' % (key, urllib.quote_plus(headers[key])) for key in headers])


	def get_url(self, host, media_id):
		return media_id


	def get_host_and_id(self, url):
		return 'premiumize.me', url


	# @common.cache.cache_method(cache_limit=8)
	def get_all_hosters(self):
		try:
			response = request.get(list_services_path, headers=self.headers)
			result = json.loads(response)
			aliases = result.get('aliases', {})
			patterns = result.get('regexpatterns', {})

			tldlist = []
			for tlds in aliases.values():
				for tld in tlds:
					tldlist.append(tld)
			if self.get_setting('torrents') == 'true':
				tldlist.extend([u'torrent', u'magnet'])
			regex_list = []
			for regexes in patterns.values():
				for regex in regexes:
					try:
						regex_list.append(re.compile(regex))
					except:
						log_utils.log('Throwing out bad Premiumize regex: %s' % regex, log_utils.LOGDEBUG)

			log_utils.log('Premiumize.me patterns: %s regex: (%d) hosts: %s' % (patterns, len(regex_list), tldlist), log_utils.LOGDEBUG)

			return tldlist, regex_list
		except Exception as e:
			log_utils.log('Error getting Premiumize hosts: %s' % e, log_utils.LOGDEBUG)
		return [], []


	def valid_url(self, url, host):
		if url and self.get_setting('torrents') == 'true':
			url_lc = url.lower()
			if url_lc.endswith('.torrent') or url_lc.startswith('magnet:'):
				return True

		if not self.patterns or not self.hosts:
			self.hosts, self.patterns = self.get_all_hosters()

		if url:
			if not url.endswith('/'):
				url += '/'
			for pattern in self.patterns:
				if pattern.findall(url):
					return True
		elif host:
			if host.startswith('www.'):
				host = host.replace('www.', '')
			if any(host in item for item in self.hosts):
				return True

		return False


	def check_cache(self, media_id):
		try:
			url = '%s?items[]=%s' % (CacheCheck, media_id)
			# result = self.net.http_GET(url, headers=self.headers).content
			# result = requests.get(url, headers=self.headers)
			result = client.request(url, headers=self.headers)
			# log_utils.log('result = %s' % result, log_utils.LOGDEBUG)
			# log_utils.log('result = %s' % result.txt, log_utils.LOGDEBUG)
			result = json.loads(result)
			# log_utils.log('result = %s' % result, log_utils.LOGDEBUG)
			if 'status' in result:
				if result.get('status') == 'success':
					response = result.get('response', False)
					# log_utils.log('response = %s' % response, log_utils.LOGDEBUG)

					if isinstance(response, list):
						return response[0]
		except:
			import traceback
			traceback.print_exc()
			pass

		return False


	def __create_transfer(self, media_id):
		folder_id = self.__create_folder()
		if not folder_id == "":
			try:
				data = urllib.urlencode({'src': media_id, 'folder_id': folder_id})
				# response = self.net.http_POST(create_transfer_path, form_data=data, headers=self.headers).content
				response = request.post(TransferCreate, data=data, headers=self.headers).txt
				result = json.loads(response)
				if 'status' in result:
					if result.get('status') == 'success':
						log_utils.log('Transfer successfully started to the Premiumize.me cloud', log_utils.LOGDEBUG)
						return result.get('id', "")
			except:
				pass
		return ""
