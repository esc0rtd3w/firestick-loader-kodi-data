# -*- coding: utf-8 -*-

'''
	Venom Add-on
'''

import re, zipfile
import StringIO, urllib, urllib2
import time
import requests

from resources.lib.modules import cache
from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import control
from resources.lib.modules import log_utils

lang = control.apiLanguage()['tvdb']

self.tvdb_key = 'N1I4U1paWDkwVUE5WU1CVQ=='
imdb_user = control.setting('imdb.user').replace('ur', '')
user = str(imdb_user) + str(api_key)

baseUrl = 'https://thetvdb.com'
info_link = '%s/api/%s/series/%s/%s.xml' % (baseUrl, api_key.decode('base64'), '%s', '%s')
zip_link = '%s/api/%s/series/%s/all/%s.zip' % (baseUrl, api_key.decode('base64'), '%s', '%s')
by_imdb = '%s/api/GetSeriesByRemoteID.php?imdbid=%s' % (baseUrl, '%s')
by_seriesname = '%s/api/GetSeries.php?seriesname=%s' % (baseUrl, '%s')
imageUrl = '%s/banners/' % baseUrl


def getZip(tvdb):
	url = zip_link % (tvdb, lang)
	try:
		data = requests.get(url).content
		zip = zipfile.ZipFile(StringIO.StringIO(data))

		result = zip.read('%s.xml' % lang)
		artwork = zip.read('banners.xml')
		actors = zip.read('actors.xml')
		zip.close()

		return (result, artwork, actors)
	except:
		return None


def parseAll(tvdb):
	try:
		dupe = client.parseDOM(result, 'SeriesName')[0]
		dupe = re.compile('[***]Duplicate (\d*)[***]').findall(dupe)

		if len(dupe) > 0:
			tvdb = str(dupe[0]).encode('utf-8')

			url = zip_link % (tvdb, 'en')
			data = requests.get(url).content
			zip = zipfile.ZipFile(StringIO.StringIO(data))

			result = zip.read('en.xml')
			artwork = zip.read('banners.xml')
			actors = zip.read('actors.xml')
			zip.close()

		# if lang != 'en':
			# url = zip_link % (tvdb, lang)
			# data = requests.get(url).content
			# zip = zipfile.ZipFile(StringIO.StringIO(data))

			# result2 = zip.read('%s.xml' % lang)
			# zip.close()
		# else:
			# result2 = result

		artwork = artwork.split('<Banner>')
		artwork = [i for i in artwork if '<Language>en</Language>' in i and '<BannerType>season</BannerType>' in i]
		artwork = [i for i in artwork if not 'seasonswide' in re.findall('<BannerPath>(.+?)</BannerPath>', i)[0]]

		result = result.split('<Episode>')
		# result2 = result2.split('<Episode>')

		item = result[0]
		# item2 = result2[0]

		episodes = [i for i in result if '<EpisodeNumber>' in i]

		if control.setting('tv.specials') == 'true':
			episodes = [i for i in episodes]
		else:
			episodes = [i for i in episodes if not '<SeasonNumber>0</SeasonNumber>' in i]
			episodes = [i for i in episodes if not '<EpisodeNumber>0</EpisodeNumber>' in i]

		seasons = [i for i in episodes if '<EpisodeNumber>1</EpisodeNumber>' in i]
		counts = seasonCountParse(seasons = seasons, episodes = episodes)

		# locals = [i for i in result2 if '<EpisodeNumber>' in i]
		locals = [i for i in result if '<EpisodeNumber>' in i]

		result = ''
		# result2 = ''

		if limit == '':
			episodes = []
		elif limit == '-1':
			seasons = []
		else:
			episodes = [i for i in episodes if '<SeasonNumber>%01d</SeasonNumber>' % int(limit) in i]
			seasons = []
		try:
			poster = client.parseDOM(item, 'poster')[0]
		except:
			poster = ''
		if poster != '':
			poster = imageUrl + poster
		else:
			poster = '0'
		poster = client.replaceHTMLCodes(poster)
		poster = poster.encode('utf-8')

		try:
			banner = client.parseDOM(item, 'banner')[0]
		except:
			banner = ''
		if banner != '':
			banner = imageUrl + banner
		else:
			banner = '0'
		banner = client.replaceHTMLCodes(banner)
		banner = banner.encode('utf-8')

		try:
			fanart = client.parseDOM(item, 'fanart')[0]
		except:
			fanart = ''
		if fanart != '':
			fanart = imageUrl + fanart
		else:
			fanart = '0'
		fanart = client.replaceHTMLCodes(fanart)
		fanart = fanart.encode('utf-8')

		if poster != '0':
			pass
		elif fanart != '0':
			poster = fanart
		elif banner != '0':
			poster = banner

		if banner != '0':
			pass
		elif fanart != '0':
			banner = fanart
		elif poster != '0':
			banner = poster

		try:
			status = client.parseDOM(item, 'Status')[0]
		except:
			status = ''
		if status == '':
			status = 'Ended'
		status = client.replaceHTMLCodes(status)
		status = status.encode('utf-8')

		try:
			studio = client.parseDOM(item, 'Network')[0]
		except:
			studio = ''
		if studio == '':
			studio = '0'
		studio = client.replaceHTMLCodes(studio)
		studio = studio.encode('utf-8')

		try:
			genre = client.parseDOM(item, 'Genre')[0]
		except:
			genre = ''
		genre = [x for x in genre.split('|') if x != '']
		genre = ' / '.join(genre)
		if genre == '':
			genre = '0'
		genre = client.replaceHTMLCodes(genre)
		genre = genre.encode('utf-8')

		try:
			duration = client.parseDOM(item, 'Runtime')[0]
		except:
			duration = ''
		if duration == '':
			duration = '0'
		duration = client.replaceHTMLCodes(duration)
		duration = duration.encode('utf-8')

		try:
			rating = client.parseDOM(item, 'Rating')[0]
			rating = client.replaceHTMLCodes(rating)
			rating = rating.encode('utf-8')
		except:
			rating = '0'

		try:
			votes = client.parseDOM(item, 'RatingCount')[0]
			votes = client.replaceHTMLCodes(votes)
			votes = votes.encode('utf-8')
		except:
			votes = '0'

		try:
			mpaa = client.parseDOM(item, 'ContentRating')[0]
			mpaa = client.replaceHTMLCodes(mpaa)
			mpaa = mpaa.encode('utf-8')
		except:
			mpaa = '0'

		actors = getActors(tvdb)
		castandart = parseActors(actors)



		try:
			label = client.parseDOM(item2, 'SeriesName')[0]
		except:
			label = '0'
		label = client.replaceHTMLCodes(label)
		label = label.encode('utf-8')

		try:
			plot = client.parseDOM(item2, 'Overview')[0]
		except:
			plot = ''
		if plot == '':
			plot = '0'
		plot = client.replaceHTMLCodes(plot)
		plot = plot.encode('utf-8')

		unaired = ''

	except:
		log_utils.error()
		pass

	for item in seasons:
		try:
			premiered = client.parseDOM(item, 'FirstAired')[0]
			if premiered == '' or '-00' in premiered: premiered = '0'
			premiered = client.replaceHTMLCodes(premiered)
			premiered = premiered.encode('utf-8')

			# Show Unaired items.
			if status.lower() == 'ended':
				pass
			elif premiered == '0':
				continue
			elif int(re.sub('[^0-9]', '', str(premiered))) > int(re.sub('[^0-9]', '', str(today_date))):
				unaired = 'true'
				if showunaired != 'true':
					continue

			# # Show Unaired items.
			# if status.lower() == 'ended':
				# pass
			# elif premiered == '0':
				# unaired = 'true'
				# pass
			# elif premiered != '0':
				# if int(re.sub('[^0-9]', '', str(premiered))) > int(re.sub('[^0-9]', '', str(today_date))):
					# unaired = 'true'
					# if showunaired != 'true':
						# continue

			season = client.parseDOM(item, 'SeasonNumber')[0]
			season = '%01d' % int(season)
			season = season.encode('utf-8')

			thumb = [i for i in artwork if client.parseDOM(i, 'Season')[0] == season]
			try:
				thumb = client.parseDOM(thumb[0], 'BannerPath')[0]
			except:
				thumb = ''
			if thumb != '':
				thumb = imageUrl + thumb
			else:
				thumb = '0'
			thumb = client.replaceHTMLCodes(thumb)
			thumb = thumb.encode('utf-8')
			if thumb == '0':
				thumb = poster

			try:
				seasoncount = counts[season]
			except:
				seasoncount = None

			list.append({'season': season, 'seasoncount': seasoncount, 'tvshowtitle': tvshowtitle, 'label': label, 'year': year,
										'premiered': premiered, 'status': status, 'studio': studio, 'genre': genre, 'duration': duration,
										'rating': rating, 'votes': votes, 'mpaa': mpaa, 'castandart': castandart, 'plot': plot, 'imdb': imdb,
										'tmdb': tmdb, 'tvdb': tvdb, 'tvshowid': imdb, 'poster': poster, 'banner': banner, 'fanart': fanart,
										'thumb': thumb, 'unaired': unaired})

		except:
			log_utils.error()
			pass

	for item in episodes:
		try:
			premiered = client.parseDOM(item, 'FirstAired')[0]
			if premiered == '' or '-00' in premiered:
				premiered = '0'
			premiered = client.replaceHTMLCodes(premiered)
			premiered = premiered.encode('utf-8')

			# Show Unaired items.
			if status.lower() == 'ended':
				pass
			elif premiered == '0':
				continue

			elif int(re.sub('[^0-9]', '', str(premiered))) > int(re.sub('[^0-9]', '', str(today_date))):
				unaired = 'true'
				if showunaired != 'true':
					continue

			# # Show Unaired items.
			# if status.lower() == 'ended':
				# pass
			# elif premiered == '0':
				# unaired = 'true'
				# pass
			# elif premiered != '0':
				# if int(re.sub('[^0-9]', '', str(premiered))) > int(re.sub('[^0-9]', '', str(today_date))):
					# unaired = 'true'
					# if showunaired != 'true':
						# continue

			season = client.parseDOM(item, 'SeasonNumber')[0]
			season = '%01d' % int(season)
			season = season.encode('utf-8')

			episode = client.parseDOM(item, 'EpisodeNumber')[0]
			episode = re.sub('[^0-9]', '', '%01d' % int(episode))
			episode = episode.encode('utf-8')

# ### episode IDS
			episodeIDS = {}
			if control.setting('enable.upnext') == 'true':
				episodeIDS = trakt.getEpisodeSummary(imdb, season, episode, full=False) or {}
				if episodeIDS != {}:
					episodeIDS = episodeIDS.get('ids', {})
##------------------

			title = client.parseDOM(item, 'EpisodeName')[0]
			title = client.replaceHTMLCodes(title)
			title = title.encode('utf-8')

			try:
				thumb = client.parseDOM(item, 'filename')[0]
			except:
				thumb = ''
			if thumb != '':
				thumb = imageUrl + thumb
			else:
				thumb = '0'
			thumb = client.replaceHTMLCodes(thumb)
			thumb = thumb.encode('utf-8')

			if thumb != '0':
				pass
			elif fanart != '0':
				thumb = fanart.replace(imageUrl, tvdb_poster)
			elif poster != '0':
				thumb = poster

			season_poster = [i for i in artwork if client.parseDOM(i, 'Season')[0] == season]
			try:
				season_poster = client.parseDOM(season_poster[0], 'BannerPath')[0]
			except:
				season_poster = ''
			if season_poster != '':
				season_poster = imageUrl + season_poster
			else:
				season_poster = '0'
			season_poster = client.replaceHTMLCodes(season_poster)
			season_poster = season_poster.encode('utf-8')
			if season_poster == '0':
				season_poster = poster
			# log_utils.log('season_poster = %s for tvshowtitle = %s' % (season_poster, tvshowtitle), __name__, log_utils.LOGDEBUG)

			try:
				rating = client.parseDOM(item, 'Rating')[0]
			except:
				rating = ''
			if rating == '':
				rating = '0'
			rating = client.replaceHTMLCodes(rating)
			rating = rating.encode('utf-8')

			try:
				director = client.parseDOM(item, 'Director')[0]
			except:
				director = ''
			director = [x for x in director.split('|') if x != '']
			director = ' / '.join(director)
			if director == '':
				director = '0'
			director = client.replaceHTMLCodes(director)
			director = director.encode('utf-8')

			try:
				writer = client.parseDOM(item, 'Writer')[0]
			except:
				writer = ''
			writer = [x for x in writer.split('|') if x != '']
			writer = ' / '.join(writer)
			if writer == '':
				writer = '0'
			writer = client.replaceHTMLCodes(writer)
			writer = writer.encode('utf-8')

			try:
				local = client.parseDOM(item, 'id')[0]
				local = [x for x in locals if '<id>%s</id>' % str(local) in x][0]
			except:
				local = item

			label = client.parseDOM(local, 'EpisodeName')[0]
			if label == '':
				label = '0'
			label = client.replaceHTMLCodes(label)
			label = label.encode('utf-8')

			try:
				episodeplot = client.parseDOM(local, 'Overview')[0]
			except:
				episodeplot = ''
			if episodeplot == '':
				episodeplot = '0'
			if episodeplot == '0':
				episodeplot = plot
			episodeplot = client.replaceHTMLCodes(episodeplot)
			try:
				episodeplot = episodeplot.encode('utf-8')
			except:
				pass

			try:
				seasoncount = counts[season]
			except:
				seasoncount = None

			list.append({'title': title, 'label': label, 'seasoncount': seasoncount, 'season': season, 'episode': episode, 'tvshowtitle': tvshowtitle, 'year': year,
							'premiered': premiered, 'status': status, 'studio': studio, 'genre': genre, 'duration': duration, 'rating': rating, 'votes': votes, 'mpaa': mpaa,
							'director': director, 'writer': writer, 'castandart': castandart, 'plot': episodeplot, 'imdb': imdb, 'tmdb': tmdb, 'tvdb': tvdb, 'poster': poster, 'banner': banner,
							'fanart': fanart, 'thumb': thumb, 'season_poster': season_poster, 'unaired': unaired, 'episodeIDS': episodeIDS})

			# meta = {}
			# meta = {'imdb': imdb, 'tmdb': tmdb, 'tvdb': tvdb, 'lang': lang, 'user': user, 'item': item}

			# list.append(item)
			# metacache.insert(meta)

		except:
			log_utils.error()
			pass
	return list


def parseSeasonInfo(tvdb, season):


def parseEpisodeInfo(tvdb, episode):
	try:
		result, artwork, actors = getZip(tvdb)


		result = result.split('<Episode>')
		item = [x for x in result if '<EpisodeNumber>' in x]
		item2 = result[0]

		num = [x for x,y in enumerate(item) if re.compile('<SeasonNumber>(.+?)</SeasonNumber>').findall(y)[0] == str(i['snum']) and re.compile('<EpisodeNumber>(.+?)</EpisodeNumber>').findall(y)[0] == str(i['enum'])][-1]
		item = [y for x,y in enumerate(item) if x > num][0]

		artwork = artwork.split('<Banner>')
		artwork = [x for x in artwork if '<Language>en</Language>' in x and '<BannerType>season</BannerType>' in x]
		artwork = [x for x in artwork if not 'seasonswide' in re.findall('<BannerPath>(.+?)</BannerPath>', x)[0]]

		premiered = client.parseDOM(item, 'FirstAired')[0]

		# try:
			# episodeIDS = i['episodeIDS']
		# except:
			# episodeIDS = {}

		status = client.parseDOM(item2, 'Status')[0]

		unaired = ''

		if status.lower() == 'ended':
			pass
		elif premiered == '0':
			raise Exception()
		elif int(re.sub('[^0-9]', '', str(premiered))) > int(re.sub('[^0-9]', '', str(self.today_date))):
			unaired = 'true'
			if control.setting('showunaired') != 'true':
				raise Exception()

		title = client.parseDOM(item, 'EpisodeName')[0]
		title = client.replaceHTMLCodes(title)
		title = title.encode('utf-8')

		season = client.parseDOM(item, 'SeasonNumber')[0]
		season = '%01d' % int(season)

		if control.setting('tv.specials') == 'false' and season == '0':
			raise Exception()

		episode = client.parseDOM(item, 'EpisodeNumber')[0]
		episode = re.sub('[^0-9]', '', '%01d' % int(episode))

		seasoncount = '0'
		# seasoncount = seasons.Seasons.seasonCountParse(season=season, items=result)
		# log_utils.log('seasoncount = %s for title = %s' % (str(seasoncount), str(title)), __name__, log_utils.LOGDEBUG)

		# tvshowtitle = i['tvshowtitle']
		# year = str(i.get('year'))
		# imdb, tmdb, tvdb = i['imdb'], i['tmdb'], i['tvdb']

		poster = client.parseDOM(item2, 'poster')[0]
		if poster and poster != '':
			poster = self.imageUrl + poster
		else: poster = '0'

		season_poster = [x for x in artwork if client.parseDOM(x, 'Season')[0] == season]
		try:
			season_poster = client.parseDOM(season_poster[0], 'BannerPath')[0]
		except:
			season_poster = ''
		if season_poster != '':
			season_poster = self.imageUrl + season_poster
		else:
			season_poster = '0'
		season_poster = client.replaceHTMLCodes(season_poster)
		season_poster = season_poster.encode('utf-8')

		banner = client.parseDOM(item2, 'banner')[0]
		if banner and banner != '':
			banner = self.imageUrl + banner
		else: banner = '0'

		fanart = client.parseDOM(item2, 'fanart')[0]
		if fanart and fanart != '':
			fanart = self.imageUrl + fanart
		else: fanart = '0'

		thumb = client.parseDOM(item, 'filename')[0]
		if thumb and thumb != '':
			thumb = self.imageUrl + thumb
		else: thumb = '0'

		if poster != '0':
			pass
		elif fanart != '0':
			poster = fanart
		elif banner != '0':
			poster = banner

		if banner != '0':
			pass
		elif fanart != '0':
			banner = fanart
		elif poster != '0':
			banner = poster

		if thumb != '0':
			pass
		elif fanart != '0':
			thumb = fanart.replace(self.imageUrl, self.tvdb_poster)
		elif poster != '0':
			thumb = poster

		studio = client.parseDOM(item2, 'Network')[0]

		genre = client.parseDOM(item2, 'Genre')[0]
		genre = [x for x in genre.split('|') if x != '']
		genre = ' / '.join(genre)

		duration = client.parseDOM(item2, 'Runtime')[0]

		rating = client.parseDOM(item, 'Rating')[0]
		votes = client.parseDOM(item2, 'RatingCount')[0]

		mpaa = client.parseDOM(item2, 'ContentRating')[0]

		director = client.parseDOM(item, 'Director')[0]
		director = [x for x in director.split('|') if x != '']
		director = (' / '.join(director)).encode('utf-8')
		director = client.replaceHTMLCodes(director)

		writer = client.parseDOM(item, 'Writer')[0]
		writer = [x for x in writer.split('|') if x != '']
		writer = (' / '.join(writer)).encode('utf-8')
		writer = client.replaceHTMLCodes(writer)

		castandart = parseActors(actors)

		plot = client.parseDOM(item, 'Overview')[0]
		if not plot:
			plot = client.parseDOM(item2, 'Overview')[0]
		plot = client.replaceHTMLCodes(plot)
		plot = plot.encode('utf-8')

		values = {'title': title, 'seasoncount': seasoncount, 'season': season, 'episode': episode,
						'year': year, 'tvshowtitle': tvshowtitle, 'tvshowyear': year, 'premiered': premiered,
						'status': status, 'studio': studio, 'genre': genre,
						'duration': duration, 'rating': rating, 'votes': votes, 'mpaa': mpaa, 'director': director,
						'writer': writer, 'castandart': castandart, 'plot': plot, 'imdb': imdb, 'tmdb': tmdb, 'tvdb': tvdb,
						'poster': poster, 'season_poster': season_poster,  'banner': banner, 'fanart': fanart, 'thumb': thumb,
						'snum': i['snum'], 'enum': i['enum'], 'unaired': unaired}

		if not direct:
			values['action'] = 'episodes'

		if 'airday' in i and i['airday'] is not None and i['airday'] != '':
			values['airday'] = i['airday']
		if 'airtime' in i and i['airtime'] is not None and i['airtime'] != '':
			values['airtime'] = i['airtime']
		if 'airzone' in i and i['airzone'] is not None and i['airzone'] != '':
			values['airzone'] = i['airzone']
		self.list.append(values)

		return self.list


	except:
		pass








def parseSeasonPoster(artwork, season):
	try:
		season_poster = [x for x in artwork if client.parseDOM(x, 'Season')[0] == season]
		season_poster = client.parseDOM(season_poster[0], 'BannerPath')[0]

		# if season_poster != '' or season_poster is not None:
			# season_poster = imageUrl + season_poster

		season_poster = imageUrl + season_poster or None
		season_poster = client.replaceHTMLCodes(season_poster)
		season_poster = season_poster.encode('utf-8')
		return season_poster
	except:
		return None


def getSeries_by_id(tvdb):
	url = info_link % (tvdb, lang)
	items = []

	try:
		item = client.request(url, timeout='10', error = True)

		if item is None:
			raise Exception()

		imdb = client.parseDOM(item, 'IMDB_ID')[0]

		title = client.parseDOM(item, 'SeriesName')[0]
		title = client.replaceHTMLCodes(title)
		title = title.encode('utf-8')

		year = client.parseDOM(item, 'FirstAired')[0]
		year = re.compile('(\d{4})').findall(year)[0]

		premiered = client.parseDOM(item, 'FirstAired')[0]

		studio = client.parseDOM(item, 'Network')[0]

		genre = client.parseDOM(item, 'Genre')[0]
		genre = [x for x in genre.split('|') if x != '']
		genre = ' / '.join(genre)

		duration = client.parseDOM(item, 'Runtime')[0]

		rating = client.parseDOM(item, 'Rating')[0]

		votes = client.parseDOM(item, 'RatingCount')[0]

		mpaa = client.parseDOM(item, 'ContentRating')[0]

		plot = client.parseDOM(item, 'Overview')[0]
		plot = client.replaceHTMLCodes(plot)
		try: plot = plot.encode('utf-8')
		except: pass

		status = client.parseDOM(item, 'Status')[0]
		if not status:
			status = 'Ended'

		poster = client.parseDOM(item, 'poster')[0]
		if poster and poster != '':
			poster = imageUrl + poster
		else: poster = '0'

		banner = client.parseDOM(item, 'banner')[0]
		if banner and banner != '':
			banner = imageUrl + banner
		else: banner = '0'

		fanart = client.parseDOM(item, 'fanart')[0]
		if fanart and fanart != '':
			fanart = imageUrl + fanart
		else: fanart = '0'


		items.append({'extended': True, 'title': title, 'year': year, 'imdb': imdb, 'tmdb': tmdb, 'tvdb': tvdb, 'premiered': premiered, 'studio': studio, 'genre': genre, 'duration': duration,
					'rating': rating, 'votes': votes, 'mpaa': mpaa, 'castandart': castandart, 'plot': plot, 'status': status, 'poster': poster, 'poster2': '0', 'poster3': '0', 'banner': banner,
					'banner2': '0', 'fanart': fanart, 'fanart2': '0', 'fanart3': '0', 'clearlogo': '0', 'clearart': '0', 'landscape': fanart, 'metacache': False})

		# meta = {'imdb': imdb, 'tmdb': tmdb, 'tvdb': tvdb, 'lang': lang, 'user': user, 'item': item}

		return items

	except:
		return None


def getBanners(tvdb):
	url = info_link % (tvdb, 'banners')
	try:
		artwork = client.request(url, timeout='10', error=True)

		if artwork is None:
			raise Exception()

		artwork = artwork.split('<Banner>')
		artwork = [i for i in artwork if '<Language>en</Language>' in i and '<BannerType>season</BannerType>' in i]
		artwork = [i for i in artwork if not 'seasonswide' in re.findall('<BannerPath>(.+?)</BannerPath>', i)[0]]
		return artwork

	except:
		return None


def parseBanners(artwork):



def getActors(tvdb):
	url = info_link % (tvdb, 'actors')
	try:
		actors = client.request(url, timeout='10', error=True)
		if actors is None:
			raise Exception()
		return actors
	except:
		return None


def parseActors(actors):
	castandart = []
	try:
		if actors is None:
			raise Exception()

		import xml.etree.ElementTree as ET
		tree = ET.ElementTree(ET.fromstring(actors))
		root = tree.getroot()
		for actor in root.iter('Actor'):
			person = [name.text for name in actor]
			image = person[1]
			name = person[2]
			try: name = client.replaceHTMLCodes(person[2])
			except: pass
			role = person[3]
			try: role = client.replaceHTMLCodes(person[3])
			except: pass
			try:
				try:
					castandart.append({'name': name.encode('utf-8'), 'role': role.encode('utf-8'), 'thumbnail': ((imageUrl + image) if image is not None else '0')})
				except:
					castandart.append({'name': name, 'role': role, 'thumbnail': ((imageUrl + image) if image is not None else '0')})
			except:
				castandart = []
			if len(castandart) == 150: break

		return castandart

	except:
		return None


def getSeries_ByIMDB(title, year, imdb):
	try:
		url = by_imdb % imdb
		result = requests.get(url).content
		result = re.sub(r'[^\x00-\x7F]+', '', result)
		result = client.replaceHTMLCodes(result)
		result = client.parseDOM(result, 'Series')
		result = [(client.parseDOM(x, 'SeriesName'), client.parseDOM(x, 'FirstAired'), client.parseDOM(x, 'seriesid'), client.parseDOM(x, 'AliasNames')) for x in result]
		years = [str(year), str(int(year)+1), str(int(year)-1)]
		item = [(x[0], x[1], x[2], x[3]) for x in result if cleantitle.get(title) == cleantitle.get(str(x[0][0])) and any(y in str(x[1][0]) for y in years)]
		if item == []:
			item = [(x[0], x[1], x[2], x[3]) for x in result if cleantitle.get(title) == cleantitle.get(str(x[3][0]))]
		if item == []:
			item = [(x[0], x[1], x[2], x[3]) for x in result if cleantitle.get(title) == cleantitle.get(str(x[0][0]))]
		if item == []:
			return None
		tvdb = item[0][2]
		tvdb = tvdb[0] or '0'
		return tvdb
	except:
		log_utils.error()
		pass


def getSeries_ByName(title, year):
	try:
		url = by_seriesname % (urllib.quote_plus(title))
		result = requests.get(url).content
		result = re.sub(r'[^\x00-\x7F]+', '', result)
		result = client.replaceHTMLCodes(result)
		result = client.parseDOM(result, 'Series')
		result = [(client.parseDOM(x, 'SeriesName'), client.parseDOM(x, 'FirstAired'), client.parseDOM(x, 'seriesid'), client.parseDOM(x, 'IMDB_ID'), client.parseDOM(x, 'AliasNames')) for x in result]
		years = [str(year), str(int(year)+1), str(int(year)-1)]
		item = [(x[0], x[1], x[2], x[3], x[4]) for x in result if cleantitle.get(title) == cleantitle.get(str(x[0][0])) and any(y in str(x[1][0]) for y in years)]
		if item == []:
			item = [(x[0], x[1], x[2], x[3], x[4]) for x in result if cleantitle.get(title) == cleantitle.get(str(x[4][0]))]
		if item == []:
			item = [(x[0], x[1], x[2], x[3], x[4]) for x in result if cleantitle.get(title) == cleantitle.get(str(x[0][0]))]
		if item == []:
			return None
		if tvdb == '0':
			tvdb = item[0][2]
			tvdb = tvdb[0] or '0'
		if imdb == '0':
			imdb = item[0][3]
			imdb = imdb[0] or '0'
		return (tvdb, imdb)
	except:
		log_utils.error()
		pass
