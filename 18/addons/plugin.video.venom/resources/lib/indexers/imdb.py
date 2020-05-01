# -*- coding: utf-8 -*-

'''
	Venom Add-on
'''

import re, json, urlparse, datetime

from resources.lib.modules import cache
from resources.lib.modules import client
from resources.lib.modules import control
from resources.lib.modules import log_utils
from resources.lib.modules import metacache
from resources.lib.modules import trakt


class movies:
	def __init__(self):
		self.count = 40
		self.list = []
		self.meta = []

		self.datetime = (datetime.datetime.utcnow() - datetime.timedelta(hours = 5))

		self.imdb_user = control.setting('imdb.user').replace('ur', '')

		self.lang = control.apiLanguage()['trakt']

		self.tmdb_key = control.setting('tm.user')
		if self.tmdb_key == '' or self.tmdb_key is None:
			self.tmdb_key = '3320855e65a9758297fec4f7c9717698'

		self.user = str(self.imdb_user) + str(self.tmdb_key)

		self.tmdb_poster = 'https://image.tmdb.org/t/p/w500'
		self.tmdb_fanart = 'https://image.tmdb.org/t/p/w1280'

		self.tmdb_info_link = 'https://api.themoviedb.org/3/movie/%s?api_key=%s&language=%s&append_to_response=credits,release_dates,external_ids' % ('%s', self.tmdb_key, self.lang)
																	# other	"append_to_response"options		alternative_titles,videos,images
		self.tmdb_art_link = 'https://api.themoviedb.org/3/movie/%s/images?api_key=%s&include_image_language=en,%s,null' % ('%s', self.tmdb_key, self.lang)


	def imdb_list(self, url):
		try:
			for i in re.findall('date\[(\d+)\]', url):
				url = url.replace('date[%s]' % i, (self.datetime - datetime.timedelta(days = int(i))).strftime('%Y-%m-%d'))

			def imdb_watchlist_id(url):
				return client.parseDOM(client.request(url), 'meta', ret='content', attrs = {'property': 'pageId'})[0]
			if url == self.imdbwatchlist_link:
				url = cache.get(imdb_watchlist_id, 8640, url)
				url = self.imdblist_link % url
			elif url == self.imdbwatchlist2_link:
				url = cache.get(imdb_watchlist_id, 8640, url)
				url = self.imdblist2_link % url
			result = client.request(url)
			result = result.replace('\n', ' ')
			result = result.decode('iso-8859-1').encode('utf-8')

			items = client.parseDOM(result, 'div', attrs = {'class': '.+? lister-item'}) + client.parseDOM(result, 'div', attrs = {'class': 'lister-item .+?'})
			items += client.parseDOM(result, 'div', attrs = {'class': 'list_item.+?'})
		except:
			return

		try:
			# HTML syntax error, " directly followed by attribute name. Insert space in between. parseDOM can otherwise not handle it.
			result = result.replace('"class="lister-page-next', '" class="lister-page-next')

			# next = client.parseDOM(result, 'a', ret='href', attrs = {'class': '.+?ister-page-nex.+?'})
			next = client.parseDOM(result, 'a', ret='href', attrs = {'class': 'lister-page-next.+?'})

			if len(next) == 0:
				next = client.parseDOM(result, 'div', attrs = {'class': 'pagination'})[0]
				next = zip(client.parseDOM(next, 'a', ret='href'), client.parseDOM(next, 'a'))
				next = [i[0] for i in next if 'Next' in i[1]]

			next = url.replace(urlparse.urlparse(url).query, urlparse.urlparse(next[0]).query)
			next = client.replaceHTMLCodes(next)
			next = next.encode('utf-8')
		except:
			next = ''

		for item in items:
			try:
				title = client.parseDOM(item, 'a')[1]
				title = client.replaceHTMLCodes(title)
				title = title.encode('utf-8')

				originaltitle = title

				year = client.parseDOM(item, 'span', attrs = {'class': 'lister-item-year.+?'})
				year = re.findall('(\d{4})', year[0])[0]
				year = year.encode('utf-8')

				try: show = '–'.decode('utf-8') in str(year).decode('utf-8') or '-'.decode('utf-8') in str(year).decode('utf-8')
				except: show = False
				if show: raise Exception() # Some lists contain TV shows.

				if int(year) > int((self.datetime).strftime('%Y')): raise Exception()

				try: mpaa = client.parseDOM(item, 'span', attrs = {'class': 'certificate'})[0]
				except: mpaa = '0'
				if mpaa == '' or mpaa == 'NOT_RATED': mpaa = '0'
				mpaa = mpaa.replace('_', '-')
				mpaa = client.replaceHTMLCodes(mpaa)
				mpaa = mpaa.encode('utf-8')

				imdb = client.parseDOM(item, 'a', ret='href')[0]
				imdb = re.findall('(tt\d*)', imdb)[0]
				imdb = imdb.encode('utf-8')

				# parseDOM cannot handle elements without a closing tag.
				# try: poster = client.parseDOM(item, 'img', ret='loadlate')[0]
				# except: poster = '0'
				try:
					from bs4 import BeautifulSoup
					html = BeautifulSoup(item, "html.parser")
					poster = html.find_all('img')[0]['loadlate']
				except:
					poster = '0'

				if '/nopicture/' in poster: poster = '0'
				poster = re.sub('(?:_SX|_SY|_UX|_UY|_CR|_AL)(?:\d+|_).+?\.', '_SX500.', poster)
				poster = client.replaceHTMLCodes(poster)
				poster = poster.encode('utf-8')

				try: genre = client.parseDOM(item, 'span', attrs = {'class': 'genre'})[0]
				except: genre = '0'
				genre = ' / '.join([i.strip() for i in genre.split(',')])
				if genre == '': genre = '0'
				genre = client.replaceHTMLCodes(genre)
				genre = genre.encode('utf-8')

				try: duration = re.findall('(\d+?) min(?:s|)', item)[-1]
				except: duration = '0'
				duration = duration.encode('utf-8')

				rating = '0'
				try: rating = client.parseDOM(item, 'span', attrs = {'class': 'rating-rating'})[0]
				except:
					try: rating = client.parseDOM(rating, 'span', attrs = {'class': 'value'})[0]
					except:
						try: rating = client.parseDOM(item, 'div', ret='data-value', attrs = {'class': '.*?imdb-rating'})[0]
						except: pass
				if rating == '' or rating == '-': rating = '0'
				if rating == '0':
					try:
						rating = client.parseDOM(item, 'span', attrs = {'class': 'ipl-rating-star__rating'})[0]
						if rating == '' or rating == '-': rating = '0'
					except: pass
				rating = client.replaceHTMLCodes(rating)
				rating = rating.encode('utf-8')

				votes = '0'
				try: votes = client.parseDOM(item, 'span', attrs = {'name': 'nv'})[0]
				except:
					try: votes = client.parseDOM(item, 'div', ret='title', attrs = {'class': '.*?rating-list'})[0]
					except:
						try: votes = re.findall('\((.+?) vote(?:s|)\)', votes)[0]
						except: pass
				if votes == '': votes = '0'
				votes = client.replaceHTMLCodes(votes)
				votes = votes.encode('utf-8')

				try: director = re.findall('Director(?:s|):(.+?)(?:\||</div>)', item)[0]
				except: director = '0'
				director = client.parseDOM(director, 'a')
				director = ' / '.join(director)
				if director == '': director = '0'
				director = client.replaceHTMLCodes(director)
				director = director.encode('utf-8')

				try: cast = re.findall('Stars(?:s|):(.+?)(?:\||</div>)', item)[0]
				except: cast = '0'
				cast = client.replaceHTMLCodes(cast)
				cast = cast.encode('utf-8')
				cast = client.parseDOM(cast, 'a')
				if cast == []: cast = '0'

				plot = '0'
				try: plot = client.parseDOM(item, 'p', attrs = {'class': 'text-muted'})[0]
				except:
					try: plot = client.parseDOM(item, 'div', attrs = {'class': 'item_description'})[0]
					except: pass
				plot = plot.rsplit('<span>', 1)[0].strip()
				plot = re.sub('<.+?>|</.+?>', '', plot)
				if plot == '': plot = '0'
				if plot == '0':
					try:
						plot = client.parseDOM(item, 'div', attrs = {'class': 'lister-item-content'})[0]
						plot = re.sub('<p\s*class="">', '<p class="plot_">', plot)
						plot = client.parseDOM(plot, 'p', attrs = {'class': 'plot_'})[0]
						plot = re.sub('<.+?>|</.+?>', '', plot)
						if plot == '': plot = '0'
					except: pass
				plot = client.replaceHTMLCodes(plot)
				plot = plot.encode('utf-8')

				item = {}
				item = {'content': 'movie', 'title': title, 'originaltitle': originaltitle, 'year': year, 'premiered': premiered,
						'studio': '0', 'genre': genre, 'duration': duration, 'rating': rating, 'votes': votes, 'mpaa': mpaa,
						'director': director, 'writer': writer, 'cast': cast, 'plot': plot, 'tagline': tagline, 'code': tmdb,
						'imdb': imdb, 'tmdb': tmdb, 'tvdb': '0', 'poster': poster, 'poster2': '0', 'poster3': '0', 'banner': '0',
						'fanart': '0', 'fanart2': '0', 'fanart3': '0', 'clearlogo': '0', 'clearart': '0', 'landscape': '0',
						'metacache': False, 'next': next}
				meta = {}
				meta = {'imdb': imdb, 'tmdb': tmdb, 'tvdb': '0', 'lang': self.lang, 'user': self.tmdb_key, 'item': item}

				# fanart_thread = threading.Thread
				from resources.lib.indexers import fanarttv
				# extended_art = fanarttv.get_movie_art(imdb, tmdb)
				extended_art = cache.get(fanarttv.get_movie_art, 168, imdb, tmdb)
				if extended_art is not None:
					item.update(extended_art)
					meta.update(item)

				self.list.append(item)
				self.meta.append(meta)
				metacache.insert(self.meta)
			except:
				pass
		return self.list


	def imdb_person_list(self, url):
		try:
			result = client.request(url)
			result = result.decode('iso-8859-1').encode('utf-8')
			# items = client.parseDOM(result, 'div', attrs = {'class': '.+?etail'})
			items = client.parseDOM(result, 'div', attrs = {'class': '.+? lister-item'}) + client.parseDOM(result, 'div', attrs = {'class': 'lister-item .+?'})
		except:
			log_utils.error()

		for item in items:
			try:
				name = client.parseDOM(item, 'a')[1]
				name = client.replaceHTMLCodes(name)
				name = name.encode('utf-8')

				url = client.parseDOM(item, 'a', ret='href')[0]
				url = re.findall('(nm\d*)', url, re.I)[0]
				url = self.person_link % url
				url = client.replaceHTMLCodes(url)
				url = url.encode('utf-8')

				image = client.parseDOM(item, 'img', ret='src')[0]
				# if not ('._SX' in image or '._SY' in image): raise Exception()
				image = re.sub('(?:_SX|_SY|_UX|_UY|_CR|_AL)(?:\d+|_).+?\.', '_SX500.', image)
				image = client.replaceHTMLCodes(image)
				image = image.encode('utf-8')

				self.list.append({'name': name, 'url': url, 'image': image})
			except:
				pass
		return self.list


	def imdb_user_list(self, url):
		try:
			result = client.request(url)
			result = result.decode('iso-8859-1').encode('utf-8')
			items = client.parseDOM(result, 'li', attrs = {'class': 'ipl-zebra-list__item user-list'})
			# Gaia uses this but seems to break the user list
			# items = client.parseDOM(result, 'div', attrs = {'class': 'list_name'})
		except:
			pass

		for item in items:
			try:
				name = client.parseDOM(item, 'a')[0]
				name = client.replaceHTMLCodes(name)
				name = name.encode('utf-8')

				url = client.parseDOM(item, 'a', ret='href')[0]
				url = url.split('/list/', 1)[-1].strip('/')
				url = self.imdblist_link % url
				url = client.replaceHTMLCodes(url)
				url = url.encode('utf-8')

				self.list.append({'name': name, 'url': url, 'context': url})
			except:
				pass
		self.list = sorted(self.list, key=lambda k: re.sub('(^the |^a |^an )', '', k['name'].lower()))
		return self.list



	def super_info(self, i):
		try:
			if self.list[i]['metacache'] is True:
				raise Exception()

			imdb = self.list[i]['imdb']

			item = trakt.getMovieSummary(id=imdb)

			imdb = item.get('ids', {}).get('imdb', '0')
			imdb = 'tt' + re.sub('[^0-9]', '', str(imdb))

			tmdb = str(item.get('ids', {}).get('tmdb', 0))

			premiered = item.get('released', '0')
			try: premiered = re.compile('(\d{4}-\d{2}-\d{2})').findall(premiered)[0]
			except: premiered = '0'

			people = trakt.getPeople(imdb, 'movies')

			director = writer = ''
			if 'crew' in people and 'directing' in people['crew']:
				director = ', '.join([director['person']['name'] for director in people['crew']['directing'] if director['job'].lower() == 'director'])
			if 'crew' in people and 'writing' in people['crew']:
				writer = ', '.join([writer['person']['name'] for writer in people['crew']['writing'] if writer['job'].lower() in ['writer', 'screenplay', 'author']])

			cast = []
			for person in people.get('cast', []):
				cast.append({'name': person['person']['name'], 'role': person['character']})
			cast = [(person['name'], person['role']) for person in cast]

			try:
				if self.lang == 'en' or self.lang not in item.get('available_translations', [self.lang]): raise Exception()
				trans_item = trakt.getMovieTranslation(imdb, self.lang, full = True)

				title = trans_item.get('title') or title
				tagline = trans_item.get('tagline') or tagline
				plot = trans_item.get('overview') or plot
			except:
				pass

##--TMDb artwork
			try:
				if self.tmdb_key == '': raise Exception()
				art2 = client.request(self.tmdb_art_link % imdb, timeout='20', error=True)
				art2 = json.loads(art2)
			except:
				pass

			try:
				poster3 = art2['posters']
				poster3 = [(x['width'], x['file_path']) for x in poster3]
				poster3 = [x[1] for x in poster3]
				poster3 = self.tmdb_poster + poster3[0]
			except:
				poster3 = '0'

			try:
				fanart2 = art2['backdrops']
				fanart2 = [(x['width'], x['file_path']) for x in fanart2]
				fanart2 = [x[1] for x in fanart2]
				fanart2 = self.tmdb_fanart + fanart2[0]
			except:
				fanart2 = '0'


class tvshows:
	def __init__(self):
		self.count = 40
		self.list = []
		self.meta = []

		self.lang = control.apiLanguage()['tvdb']

		self.datetime = (datetime.datetime.utcnow() - datetime.timedelta(hours = 5))

		self.fanart_tv_user = control.setting('fanart.tv.user')
		if self.fanart_tv_user == '' or self.fanart_tv_user is None:
			self.fanart_tv_user = 'cf0ebcc2f7b824bd04cf3a318f15c17d'
		self.user = self.fanart_tv_user + str('')


		self.tvdb_key = 'N1I4U1paWDkwVUE5WU1CVQ=='
		self.tvdb_info_link = 'https://thetvdb.com/api/%s/series/%s/%s.xml' % (self.tvdb_key.decode('base64'), '%s', self.lang)
		self.tvdb_by_imdb = 'https://thetvdb.com/api/GetSeriesByRemoteID.php?imdbid=%s'
		self.tvdb_by_query = 'https://thetvdb.com/api/GetSeries.php?seriesname=%s'
		self.tvdb_image = 'https://thetvdb.com/banners/'
