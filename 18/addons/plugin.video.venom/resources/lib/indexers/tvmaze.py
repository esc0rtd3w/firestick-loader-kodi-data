# -*- coding: utf-8 -*-

'''
	Venom Add-on
'''

import re
import urllib
# import json
import datetime
import requests

from resources.lib.modules import cache
from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import control
from resources.lib.modules import log_utils
from resources.lib.modules import metacache
from resources.lib.modules import workers


networks_this_season = [
			('A&E', '/networks/29/ae', 'https://i.imgur.com/xLDfHjH.png'),
			('ABC', '/networks/3/abc', 'https://i.imgur.com/qePLxos.png'),
			('Acorn TV', '/webchannels/129/acorn-tv', 'https://i.imgur.com/YMtys7n.png'),
			('Adult Swim', '/networks/10/adult-swim', 'https://i.imgur.com/jCqbRcS.png'),
			('Amazon', '/webchannels/3/amazon', 'https://i.imgur.com/ru9DDlL.png'),
			('AMC', '/networks/20/amc', 'https://i.imgur.com/ndorJxi.png'),
			('Animal Planet', '/networks/92/animal-planet', 'https://i.imgur.com/olKc4RP.png'),
			('Apple TV+', '/webchannels/310/apple-tv', 'https://i.imgur.com/HjEYPad.png'),
			('AT-X', '/networks/167/at-x', 'https://i.imgur.com/JshJYGN.png'),
			('Audience', '/networks/31/audience-network', 'https://i.imgur.com/5Q3mo5A.png'),
			('BBC America', '/networks/15/bbc-america', 'https://i.imgur.com/TUHDjfl.png'),
			('BBC One', '/networks/12/bbc-one', 'https://i.imgur.com/u8x26te.png'),
			('BBC Two', '/networks/37/bbc-two', 'https://i.imgur.com/SKeGH1a.png'),
			('BBC Three', '/webchannels/71/bbc-three', 'https://i.imgur.com/SDLeLcn.png'),
			('BBC Four', '/networks/51/bbc-four', 'https://i.imgur.com/PNDalgw.png'),
			('BET', '/networks/56/bet', 'https://i.imgur.com/ZpGJ5UQ.png'),
			('Blackpills', '/webchannels/186/blackpills', 'https://i.imgur.com/8zzNqqq.png'),
			('Brat', '/webchannels/274/brat', 'https://i.imgur.com/x2aPEx1.png'),
			('Bravo', '/networks/52/bravo', 'https://i.imgur.com/TmEO3Tn.png'),
			('Cartoon Network', '/networks/11/cartoon-network', 'https://i.imgur.com/zmOLbbI.png'),
			('CBC', '/networks/36/cbc', 'https://i.imgur.com/unQ7WCZ.png'),
			('CBS', '/networks/2/cbs', 'https://i.imgur.com/8OT8igR.png'),
			('Channel 4', '/networks/45/channel-4', 'https://i.imgur.com/6ZA9UHR.png'),
			('Channel 5', '/networks/135/channel-5', 'https://i.imgur.com/5ubnvOh.png'),
			('Cinemax', '/networks/19/cinemax', 'https://i.imgur.com/zWypFNI.png'),
			('CNBC', '/networks/93/cnbc', 'https://i.imgur.com/ENjlkvv.png'),
			('Comedy Central', '/networks/23/comedy-central', 'https://i.imgur.com/ko6XN77.png'),
			('Crackle', '/webchannels/4/crackle', 'https://i.imgur.com/53kqZSY.png'),
			('CTV', '/networks/48/ctv', 'https://i.imgur.com/qUlyVHz.png'),
			('CuriosityStream', '/webchannels/188/curiositystream', 'https://i.imgur.com/5wJsQdi.png'),
			('CW', '/networks/5/the-cw', 'https://i.imgur.com/Q8tooeM.png'),
			('CW Seed', '/webchannels/13/cw-seed', 'https://i.imgur.com/nOdKoEy.png'),
			('DC Universe', '/webchannels/187/dc-universe', 'https://i.imgur.com/bhWIubn.png'),
			('Discovery Channel', '/networks/66/discovery-channel', 'https://i.imgur.com/8UrXnAB.png'),
			('Discovery ID', '/networks/89/investigation-discovery', 'https://i.imgur.com/07w7BER.png'),
			('Disney+', '/webchannels/287/disney', 'https://i.postimg.cc/SQ8fG2qF/435560.jpg'),
			('Disney Channel', '/networks/78/disney-channel', 'https://i.imgur.com/ZCgEkp6.png'),
			('Disney Junior', '/networks/1039/disney-junior', 'https://i.imgur.com/EqPPq5S.png'),
			('Disney XD', '/networks/25/disney-xd', 'https://i.imgur.com/PAJJoqQ.png'),
			('E! Entertainment', '/networks/43/e', 'https://i.imgur.com/3Delf9f.png'),
			('E4', '/networks/41/e4', 'https://i.imgur.com/frpunK8.png'),
			# ('Fearnet', '/networks/466/fearnet', 'https://i.imgur.com/CdJ6fZt.png'),
			('FOX', '/networks/4/fox', 'https://i.imgur.com/6vc0Iov.png'),
			('Freeform', '/networks/26/freeform', 'https://i.imgur.com/f9AqoHE.png'),
			('Fusion', '/networks/187/fusion', 'https://i.imgur.com/NPxic1M.png'),
			('FX', '/networks/13/fx', 'https://i.imgur.com/aQc1AIZ.png'),
			('Hallmark', '/networks/50/hallmark-channel', 'https://i.imgur.com/zXS64I8.png'),
			# ('Hallmark Movies & Mysteries', '/networks/252/hallmark-movies-mysteries', 'https://static.tvmaze.com/uploads/images/original_untouched/13/34664.jpg'),
			('HBO', '/networks/8/hbo', 'https://i.imgur.com/Hyu8ZGq.png'),
			('HGTV', '/networks/192/hgtv', 'https://i.imgur.com/INnmgLT.png'),
			('History Channel', '/networks/53/history', 'https://i.imgur.com/LEMgy6n.png'),
			# ('H2', '/networks/74/h2', 'https://i.imgur.com/OvkmoDA.png'),
			('Hulu', '/webchannels/2/hulu', 'https://i.imgur.com/gvHOZgC.png'),
			('ITV', '/networks/35/itv', 'https://i.imgur.com/5Hxp5eA.png'),
			('Lifetime', '/networks/18/lifetime', 'https://i.imgur.com/tvYbhen.png'),
			('MTV', '/networks/22/mtv', 'https://i.imgur.com/QM6DpNW.png'),
			('National Geographic', '/networks/42/national-geographic-channel', 'https://i.imgur.com/XCGNKVQ.png'),
			('NBC', '/networks/1/nbc', 'https://i.imgur.com/yPRirQZ.png'),
			('Netflix', '/webchannels/1/netflix', 'https://i.imgur.com/jI5c3bw.png'),
			('Nickelodeon', '/networks/27/nickelodeon', 'https://i.imgur.com/OUVoqYc.png'),
			('Nicktoons', '/networks/73/nicktoons', 'https://i.imgur.com/890wBrw.png'),
			('Oxygen', '/networks/79/oxygen', 'https://i.imgur.com/uFCQvbR.png'),
			('PBS', '/networks/85/pbs', 'https://i.imgur.com/r9qeDJY.png'),
			# ('Playboy TV', '/networks/1035/playboy-tv', 'https://static.tvmaze.com/uploads/images/original_untouched/46/115366.jpg'),
			('Showcase', '/networks/270/showcase', 'https://i.postimg.cc/CKN3Ph8S/66074.jpg'),
			('Showtime', '/networks/9/showtime', 'https://i.imgur.com/SawAYkO.png'),
			('Sky1', '/networks/63/sky-1', 'https://i.imgur.com/xbgzhPU.png'),
			('Starz', '/networks/17/starz', 'https://i.imgur.com/Z0ep2Ru.png'),
			('Sundance', '/networks/33/sundance-tv', 'https://i.imgur.com/qldG5p2.png'),
			('Syfy', '/networks/16/syfy', 'https://i.imgur.com/9yCq37i.png'),
			('TBS', '/networks/32/tbs', 'https://i.imgur.com/RVCtt4Z.png'),
			('TLC', '/networks/80/tlc', 'https://i.imgur.com/c24MxaB.png'),
			('TNT', '/networks/14/tnt', 'https://i.imgur.com/WnzpAGj.png'),
			('Travel Channel', '/networks/82/travel-channel', 'https://i.imgur.com/mWXv7SF.png'),
			('TruTV', '/networks/84/trutv', 'https://i.imgur.com/HnB3zfc.png'),
			('TV Land', '/networks/57/tvland', 'https://i.imgur.com/1nIeDA5.png'),
			('TV One', '/networks/224/tv-one', 'https://i.imgur.com/gGCTa8s.png'),
			('USA', '/networks/30/usa-network', 'https://i.imgur.com/Doccw9E.png'),
			('VH1', '/networks/55/vh1', 'https://i.imgur.com/IUtHYzA.png'),
			('Viceland', '/networks/1006/viceland', 'https://i.imgur.com/sLNNqEY.png'),
			('WGN', '/networks/28/wgn-america', 'https://i.imgur.com/TL6MzgO.png'),
			('WWE Network', '/webchannels/15/wwe-network', 'https://i.imgur.com/JjbTbb2.png')
			# ('YouTube', '/webchannels/21/youtube', 'https://i.imgur.com/ZfewP1Y.png'),
			# ('YouTube Premium', '/webchannels/43/youtube-premium', 'https://static.tvmaze.com/uploads/images/medium_landscape/160/401362.jpg')
		]

networks_view_all = [
			('A&E', '/shows?Show[network_id]=29&page=1', 'https://i.imgur.com/xLDfHjH.png'),
			('ABC', '/shows?Show[network_id]=3&page=1', 'https://i.imgur.com/qePLxos.png'),
			('Acorn TV', '/shows?Show[network_id]=129&page=1', 'https://i.imgur.com/YMtys7n.png'),
			('Adult Swim', '/shows?Show[network_id]=10&page=1', 'https://i.imgur.com/jCqbRcS.png'),
			('Amazon', '/shows?Show[webChannel_id]=3&page=1', 'https://i.imgur.com/ru9DDlL.png'),
			('AMC', '/shows?Show[network_id]=20&page=1', 'https://i.imgur.com/ndorJxi.png'),
			('Animal Planet', '/shows?Show[network_id]=92&page=1', 'https://i.imgur.com/olKc4RP.png'),
			('Apple TV+', '/shows?Show[webChannel_id]=310&page=1', 'https://i.imgur.com/HjEYPad.png'),
			('AT-X', '/shows?Show[network_id]=167&page=1', 'https://i.imgur.com/JshJYGN.png'),
			('Audience', '/shows?Show[network_id]=31&page=1', 'https://i.imgur.com/5Q3mo5A.png'),
			('BBC America', '/shows?Show[network_id]=15&page=1', 'https://i.imgur.com/TUHDjfl.png'),
			('BBC One', '/shows?Show[network_id]=12&page=1', 'https://i.imgur.com/u8x26te.png'),
			('BBC Two', '/shows?Show[network_id]=37&page=1', 'https://i.imgur.com/SKeGH1a.png'),
			('BBC Three', '/shows?Show[network_id]=71&page=1', 'https://i.imgur.com/SDLeLcn.png'),
			('BBC Four', '/shows?Show[network_id]=51&page=1', 'https://i.imgur.com/PNDalgw.png'),
			('BET', '/shows?Show[network_id]=56&page=1', 'https://i.imgur.com/ZpGJ5UQ.png'),
			('Blackpills', '/shows?Show[webChannel_id]=186&page=1', 'https://i.imgur.com/8zzNqqq.png'),
			('Brat', '/shows?Show[webChannel_id]=274&page=1', 'https://i.imgur.com/x2aPEx1.png'),
			('Bravo', '/shows?Show[network_id]=52&page=1', 'https://i.imgur.com/TmEO3Tn.png'),
			('Cartoon Network', '/shows?Show[network_id]=11&page=1', 'https://i.imgur.com/zmOLbbI.png'),
			('CBC', '/shows?Show[network_id]=36&page=1', 'https://i.imgur.com/unQ7WCZ.png'),
			('CBS', '/shows?Show[network_id]=2&page=1', 'https://i.imgur.com/8OT8igR.png'),
			('CNBC', '/shows?Show[network_id]=93&page=1', 'https://i.imgur.com/ENjlkvv.png'),
			('Channel 4', '/shows?Show[network_id]=45&page=1', 'https://i.imgur.com/6ZA9UHR.png'),
			('Channel 5', '/shows?Show[network_id]=135&page=1', 'https://i.imgur.com/5ubnvOh.png'),
			('Cinemax', '/shows?Show[network_id]=19&page=1', 'https://i.imgur.com/zWypFNI.png'),
			('Comedy Central', '/shows?Show[network_id]=23&page=1', 'https://i.imgur.com/ko6XN77.png'),
			('Crackle', '/shows?Show%5BwebChannel_id%5D=4&page=1', 'https://i.imgur.com/53kqZSY.png'),
			('CTV', '/shows?Show[network_id]=48&page=1', 'https://i.imgur.com/qUlyVHz.png'),
			('CuriosityStream', '/shows?Show[webChannel_id]=188&page=1', 'https://i.imgur.com/5wJsQdi.png'),
			('CW', '/shows?Show[network_id]=5&page=1', 'https://i.imgur.com/Q8tooeM.png'),
			('CW Seed', '/shows?Show[webChannel_id]=13&page=1', 'https://i.imgur.com/nOdKoEy.png'),
			('DC Universe', '/shows?Show%5BwebChannel_id%5D=187&page=1', 'https://i.imgur.com/bhWIubn.png'),
			('Discovery Channel', '/shows?Show[network_id]=66&page=1', 'https://i.imgur.com/8UrXnAB.png'),
			('Discovery ID', '/shows?Show[network_id]=89&page=1', 'https://i.imgur.com/07w7BER.png'),
			('Disney+', '/shows?Show[webChannel_id]=287&page=1', 'https://i.postimg.cc/SQ8fG2qF/435560.jpg'),
			('Disney Channel', '/shows?Show[network_id]=78&page=1', 'https://i.imgur.com/ZCgEkp6.png'),
			('Disney Junior', '/shows?Show[network_id]=1039&page=1', 'https://i.imgur.com/EqPPq5S.png'),
			('Disney XD', '/shows?Show[network_id]=25&page=1', 'https://i.imgur.com/PAJJoqQ.png'),
			('E! Entertainment', '/shows?Show[network_id]=43&page=1', 'https://i.imgur.com/3Delf9f.png'),
			('E4', '/shows?Show[network_id]=41&page=1', 'https://i.imgur.com/frpunK8.png'),
			('Fearnet', '/shows?Show[network_id]=466&page=1', 'https://i.imgur.com/CdJ6fZt.png'),
			('FOX', '/shows?Show[network_id]=4&page=1', 'https://i.imgur.com/6vc0Iov.png'),
			('Freeform', '/shows?Show[network_id]=26&page=1', 'https://i.imgur.com/f9AqoHE.png'),
			('Fusion', '/shows?Show[network_id]=187&page=1', 'https://i.imgur.com/NPxic1M.png'),
			('FX', '/shows?Show[network_id]=13&page=1', 'https://i.imgur.com/aQc1AIZ.png'),
			('Hallmark', '/shows?Show[network_id]=50&page=1', 'https://i.imgur.com/zXS64I8.png'),
			('Hallmark Movies & Mysteries', '/shows?Show[network_id]=252&page=1', 'https://static.tvmaze.com/uploads/images/original_untouched/13/34664.jpg'),
			('HBO', '/shows?Show[network_id]=8&page=1', 'https://i.imgur.com/Hyu8ZGq.png'),
			('HGTV', '/shows?Show[network_id]=192&page=1', 'https://i.imgur.com/INnmgLT.png'),
			('History Channel', '/shows?Show[network_id]=53&page=1', 'https://i.imgur.com/LEMgy6n.png'),
			('H2', '/shows?Show[network_id]=74&page=1', 'https://i.imgur.com/OvkmoDA.png'),
			('Hulu', '/shows?Show[webChannel_id]=2&page=1', 'https://i.imgur.com/gvHOZgC.png'),
			('ITV', '/shows?Show[network_id]=35&page=1', 'https://i.imgur.com/5Hxp5eA.png'),
			('Lifetime', '/shows?Show[network_id]=18&page=1', 'https://i.imgur.com/tvYbhen.png'),
			('MTV', '/shows?Show[network_id]=22&page=1', 'https://i.imgur.com/QM6DpNW.png'),
			('National Geographic', '/shows?Show[network_id]=42&page=1', 'https://i.imgur.com/XCGNKVQ.png'),
			('NBC', '/shows?Show[network_id]=1&page=1', 'https://i.imgur.com/yPRirQZ.png'),
			('Netflix', '/shows?Show[webChannel_id]=1&page=1', 'https://i.imgur.com/jI5c3bw.png'),
			('Nickelodeon', '/shows?Show[network_id]=27&page=1', 'https://i.imgur.com/OUVoqYc.png'),
			('Nicktoons', '/shows?Show[network_id]=73&page=1', 'https://i.imgur.com/890wBrw.png'),
			('Oxygen', '/shows?Show[network_id]=79&page=1', 'https://i.imgur.com/uFCQvbR.png'),
			# ('Playboy TV', '/shows?Show[network_id]=1035&page=1', 'https://static.tvmaze.com/uploads/images/original_untouched/46/115366.jpg'),
			('PBS', '/shows?Show[network_id]=85&page=1', 'https://i.imgur.com/r9qeDJY.png'),
			('Showcase', '/shows?Show[network_id]=270&page=1', 'https://i.postimg.cc/CKN3Ph8S/66074.jpg'),
			('Showtime', '/shows?Show[network_id]=9&page=1', 'https://i.imgur.com/SawAYkO.png'),
			('Sky1', '/shows?Show[network_id]=63&page=1', 'https://i.imgur.com/xbgzhPU.png'),
			('Starz', '/shows?Show[network_id]=17&page=1', 'https://i.imgur.com/Z0ep2Ru.png'),
			('Sundance', '/shows?Show[network_id]=33&page=1', 'https://i.imgur.com/qldG5p2.png'),
			('Syfy', '/shows?Show[network_id]=16&page=1', 'https://i.imgur.com/9yCq37i.png'),
			('TBS', '/shows?Show[network_id]=32&page=1', 'https://i.imgur.com/RVCtt4Z.png'),
			('TLC', '/shows?Show[network_id]=80&page=1', 'https://i.imgur.com/c24MxaB.png'),
			('TNT', '/shows?Show[network_id]=14&page=1', 'https://i.imgur.com/WnzpAGj.png'),
			('Travel Channel', '/shows?Show[network_id]=82&page=1', 'https://i.imgur.com/mWXv7SF.png'),
			('TruTV', '/shows?Show[network_id]=84&page=1', 'https://i.imgur.com/HnB3zfc.png'),
			('TV Land', '/shows?Show[network_id]=57&page=1', 'https://i.imgur.com/1nIeDA5.png'),
			('TV One', '/shows?Show[network_id]=224&page=1', 'https://i.imgur.com/gGCTa8s.png'),
			('USA', '/shows?Show[network_id]=30&page=1', 'https://i.imgur.com/Doccw9E.png'),
			('VH1', '/shows?Show[network_id]=55&page=1', 'https://i.imgur.com/IUtHYzA.png'),
			('Viceland', '/shows?Show[network_id]=1006&page=1', 'https://i.imgur.com/sLNNqEY.png'),
			('WGN', '/shows?Show[network_id]=28&page=1', 'https://i.imgur.com/TL6MzgO.png'),
			('WWE Network', '/shows?Show[webChannel_id]=15&page=1', 'https://i.imgur.com/JjbTbb2.png')
			# ('YouTube', '/webchannels/21/youtube', 'https://i.imgur.com/ZfewP1Y.png'),
			# ('YouTube Premium', '/webchannels/43/youtube-premium', 'https://static.tvmaze.com/uploads/images/medium_landscape/160/401362.jpg')
		]

originals_this_season = [
			('Amazon', '/webchannels/3/amazon', 'https://i.imgur.com/ru9DDlL.png'),
			('Hulu', '/webchannels/2/hulu', 'https://i.imgur.com/gvHOZgC.png'),
			('Netflix', '/webchannels/1/netflix', 'https://i.imgur.com/jI5c3bw.png')
		]

originals_view_all = [
			('Amazon', '/shows?Show[webChannel_id]=3&page=1', 'https://i.imgur.com/ru9DDlL.png'),
			('Hulu', '/shows?Show[webChannel_id]=2&page=1', 'https://i.imgur.com/gvHOZgC.png'),
			('Netflix', '/shows?Show[webChannel_id]=1&page=1', 'https://i.imgur.com/jI5c3bw.png')
		]


class tvshows:
	def __init__(self, type = 'show', notifications = True):
		last = []
		self.count = 40
		self.list = []
		self.meta = []
		self.threads = []
		self.type = type
		self.lang = control.apiLanguage()['tvdb']
		self.notifications = notifications
		self.datetime = (datetime.datetime.utcnow() - datetime.timedelta(hours = 5))
		self.disable_fanarttv = control.setting('disable.fanarttv')

		self.tvmaze_link = 'https://www.tvmaze.com'
		self.tvmaze_info_link = 'https://api.tvmaze.com/shows/%s?embed=cast'

		self.tvdb_key = 'N1I4U1paWDkwVUE5WU1CVQ=='
		self.imdb_user = control.setting('imdb.user').replace('ur', '')
		self.user = str(self.imdb_user) + str(self.tvdb_key)

		self.tvdb_info_link = 'https://thetvdb.com/api/%s/series/%s/%s.xml' % (self.tvdb_key.decode('base64'), '%s', '%s')
		self.tvdb_by_imdb = 'https://thetvdb.com/api/GetSeriesByRemoteID.php?imdbid=%s'
		self.tvdb_by_query = 'https://thetvdb.com/api/GetSeries.php?seriesname=%s'
		self.tvdb_image = 'https://thetvdb.com/banners/'


	def tvmaze_list(self, url):
		try:
			result = client.request(url)
			next = ''
			if control.setting('tvshows.networks.view') == '0':
				result = client.parseDOM(result, 'section', attrs = {'id': 'this-seasons-shows'})
				items = client.parseDOM(result, 'span', attrs = {'class': 'title .*'})
				list_count = 60

			if control.setting('tvshows.networks.view') == '1':
				result = client.parseDOM(result, 'div', attrs = {'id': 'w1'})
				items = client.parseDOM(result, 'span', attrs = {'class': 'title'})

				list_count = 25
				page = int(str(url.split('&page=', 1)[1]))
				next = '%s&page=%s' % (url.split('&page=', 1)[0], page+1)

				last = []
				last = client.parseDOM(result, 'li', attrs = {'class': 'last disabled'})
				if last != []:
					next = ''

			items = [client.parseDOM(i, 'a', ret='href') for i in items]
			items = [i[0] for i in items if len(i) > 0]
			items = [re.findall('/(\d+)/', i) for i in items]
			items = [i[0] for i in items if len(i) > 0]
			items = items[:list_count]
			sortList = items
		except:
			log_utils.error()
			return

		def items_list(i):
			try:
				tvmaze = i
				url = self.tvmaze_info_link % i
				item = requests.get(url, timeout=10).json()

				content = item.get('type', '0').lower()

				try:
					title = (item.get('name')).encode('utf-8')
				except:
					title = item.get('name')

				premiered = item.get('premiered', '0')

				year = str(item.get('premiered', '0'))
				if year is not None and year != 'None' and year != '0':
					year = re.search(r"(\d{4})", year).group(1)
				else:
					year = '0'

				imdb = item.get('externals').get('imdb', '0')
				if imdb == '' or imdb is None or imdb == 'None':
					imdb = '0'

				tvdb = str(item.get('externals').get('thetvdb', '0'))
				if tvdb == '' or tvdb is None or tvdb == 'None':
					tvdb = '0'

				# TVMaze does not have tmdb_id in api
				tmdb = '0'

				studio = item.get('network', {}) or item.get('webChannel', {})
				studio = studio.get('name', '0')

				genre = []
				for i in item['genres']:
					genre.append(i.title())
				if genre == []: genre = 'NA'

				duration = str(item.get('runtime', '0'))

				rating = str(item.get('rating').get('average', '0'))

				plot = item.get('summary', '0')
				if plot:
					plot = re.sub('<.+?>|</.+?>|\n', '', plot)

				status = item.get('status', '0')

				castandart = []
				for person in item['_embedded']['cast']:
					try:
						try:
							castandart.append({'name': person['person']['name'].encode('utf-8'), 'role': person['character']['name'].encode('utf-8'), 'thumbnail': (person['person']['image']['original'] if person['person']['image']['original'] is not None else '0')})
						except:
							castandart.append({'name': person['person']['name'], 'role': person['character']['name'], 'thumbnail': (person['person']['image']['medium'] if person['person']['image']['medium'] is not None else '0')})
					except:
						castandart = []
						pass
					if len(castandart) == 150: break

				image = item.get('image')
				poster = image.get('original', '0') if image is not None else '0'
				fanart = '0' ; banner = '0'
				mpaa = '0' ; votes = '0'
				airday = '0' ; airtime = '0'

				# self.list = metacache.fetch(self.list, self.lang, self.user)
				# if self.list['metacache'] is True:
					# raise Exception()

				if (tvdb == '0' or tmdb == '0') and imdb != '0':
					from resources.lib.modules import trakt
					trakt_ids = trakt.IdLookup('show', 'imdb', imdb)
					if tvdb == '0':
						tvdb = str(trakt_ids.get('tvdb', '0'))
						if tvdb == '' or tvdb is None or tvdb == 'None':
							tvdb = '0'
					if tmdb == '0':
						tmdb = str(trakt_ids.get('tmdb', '0'))
						if tvdb == '' or tvdb is None or tvdb == 'None':
							tvdb = '0'

###--Check TVDb by IMDB_ID for missing ID's
				if tvdb == '0' and imdb != '0':
					try:
						url = self.tvdb_by_imdb % imdb
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
							raise Exception()
						tvdb = item[0][2]
						tvdb = tvdb[0] or '0'
					except:
						log_utils.error()
						pass

###--Check TVDb by seriesname
				if tvdb == '0' or imdb == '0':
					try:
						url = self.tvdb_by_query % (urllib.quote_plus(title))
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
							raise Exception()
						if tvdb == '0':
							tvdb = item[0][2]
							tvdb = tvdb[0] or '0'
						if imdb == '0':
							imdb = item[0][3]
							imdb = imdb[0] or '0'
					except:
						log_utils.error()
						pass
#################################

				if tvdb == '0':
					raise Exception()

				try:
					url = self.tvdb_info_link % (tvdb, self.lang)
					item3 = requests.get(url).content
				except:
					item3 = None

				if item3 is not None:
					if poster == '0':
						poster = client.parseDOM(item3, 'poster')[0]
						poster = '%s%s' % (self.tvdb_image, poster) if poster else '0'

					fanart = client.parseDOM(item3, 'fanart')[0]
					fanart = '%s%s' % (self.tvdb_image, fanart) if fanart else '0'

					banner = client.parseDOM(item3, 'banner')[0]
					banner = '%s%s' % (self.tvdb_image, banner) if banner else '0'

					mpaa = client.parseDOM(item3, 'ContentRating')[0] or '0'

					if duration == '0':
						duration = client.parseDOM(item3, 'Runtime')[0] or '0'

					if rating == '0':
						rating = client.parseDOM(item3, 'Rating')[0] or '0'

					votes = client.parseDOM(item3, 'RatingCount')[0] or '0'

					if status == '0':
						status = client.parseDOM(item3, 'Status')[0] or '0'

					if year == '0':
						year = client.parseDOM(item3, 'FirstAired')[0] or '0'
						if year != '0':
							year = re.compile('(\d{4})').findall(year)[0] or '0'

					if not plot:
						plot = client.parseDOM(item3, 'Overview')[0] or '0'
						plot = client.replaceHTMLCodes(plot)
						try: plot = plot.encode('utf-8')
						except: pass

					airday = client.parseDOM(item3, 'Airs_DayOfWeek')[0] or '0'
					# log_utils.log('airday = %s' % str(airday), __name__, log_utils.LOGDEBUG)
					airtime = client.parseDOM(item3, 'Airs_Time')[0] or '0'

				item = {}
				item = {'content': content, 'title': title, 'originaltitle': title, 'year': year, 'premiered': premiered, 'studio': studio, 'genre': genre, 'duration': duration, 'rating': rating, 'votes': votes, 
							'mpaa': mpaa, 'castandart': castandart, 'plot': plot, 'tagline': '0', 'status': status, 'imdb': imdb, 'tvdb': tvdb, 'tmdb': tmdb, 'tvmaze': tvmaze, 'airday': airday, 'airtime': airtime, 'poster': poster,
							'poster2': '0', 'banner': banner, 'banner2': '0', 'fanart': fanart, 'fanart2': '0', 'clearlogo': '0', 'clearart': '0', 'landscape': fanart, 'metacache': False, 'next': next}

				meta = {}
				meta = {'tmdb': tmdb, 'imdb': imdb, 'tvdb': tvdb, 'lang': self.lang, 'user': self.user, 'item': item}

				if self.disable_fanarttv != 'true':
					from resources.lib.indexers import fanarttv
					# extended_art = cache.get(fanarttv.get_tvshow_art, 168, tvdb)
					extended_art = fanarttv.get_tvshow_art(tvdb)
					if extended_art is not None:
						item.update(extended_art)
						meta.update(item)

				item = dict((k,v) for k,v in item.iteritems() if v != '0')
				self.list.append(item)

				if 'next' in meta.get('item'):
					del meta['item']['next']

				self.meta.append(meta)
				metacache.insert(self.meta)
			except:
				log_utils.error()
				pass

		try:
			threads = []
			for i in items:
				threads.append(workers.Thread(items_list, i))
			[i.start() for i in threads]
			[i.join() for i in threads]

			sorted_list = []
			for i in sortList:
				sorted_list += [item for item in self.list if str(item['tvmaze']) == str(i)]
			return sorted_list
		except:
			log_utils.error()
			return
