import cache
import control
import client, webutils
import re,sys,urlparse,urllib
from log_utils import log


from addon import Addon
addon = Addon('plugin.video.teevee', sys.argv)
addon_handle = int(sys.argv[1])

base = 'http://opentuner.is'


def get_new_episodes():
	url = base + '/new-episodes/'
	html = client.request(url)
	eps = re.findall('<a href=[\"\'](.+?)[\"\'].+?>(.+?) S(\d+)E(\d+)</a>',html)
	return eps

def get_shows(sub):
	url = base + sub
	html = client.request(url)
	shows = re.findall('<a href=[\"\'](.+?)[\"\'].+?>(.+?) \((\d+)\)</a>',html)
	return shows

def get_genres():
	out = []
	html = client.request(base)
	genres = re.findall('href=[\"\']http://opentuner.is(/genre/[^\"\']+)[\"\'] title=[\"\'](.+?)\s*TV Shows',html)
	for g in genres:
		url = g[0]
		title = _translate(g[1]).decode('utf-8')
		out.append((url,title))
	return out

def get_alphabet():
	html = client.request(base)
	alpha = re.findall('href=[\"\']http://opentuner.is(/alphabet/[^\"\']+)[\"\'] title=[\"\'](.+?)\s*TV Shows',html)
	return alpha

def get_info(url):
	try:
		html = client.request(url)
		info = client.parseDOM(html,'div',attrs={'class':'tv_info'})[0]
		try:	imdb = re.findall('title/(tt\d+)',info)[0]
		except:	imdb = ''
		try:	year = re.findall('(?:Release|Air Date).+?(\d\d\d\d)',info)[0]
		except:	year = ''
		return imdb,year
	except:
		return '',''

def get_thumbnail(url):
	try:
		html = client.request(url)
		img  = base + re.findall('(/images/thumbs/[^\"\']+)',html)[0]
	except:
		img = control.icon_path('TV_Shows.png')

	return img


def get_episode_context(showtitle,season,episode,url,thumbnail):
	title='%s S%02dE%02d'%(showtitle,int(season),int(episode))
	try:
		down_uri = addon.build_plugin_url({'mode': 'download', 'title':title,'url':url, 'thumb':thumbnail})
	except:
		down_uri = addon.build_plugin_url({'mode': 'download', 'title':title.encode('ascii','ignore'),'url':link, 'thumb':thumbnail})
	context = [(control.lang(30156).encode('utf-8'), 'XBMC.Action(Info)'),(control.lang(30157).encode('utf-8'),'RunPlugin(%s)'%down_uri)]
	return context

def get_tv_context(show_title,url,show_year,fav=True):
	context=[(control.lang(30158).encode('utf-8'), 'XBMC.Action(Info)')]
	if fav:
		try:
			fav_uri = addon.build_plugin_url({'mode': 'rem_tv_fav', 'show': show_title,'link': url, 'year':show_year})
		except:
			fav_uri = addon.build_plugin_url({'mode': 'rem_tv_fav', 'show': ((show_title).encode('ascii','ignore')),'link':url , 'year':show_year})


		context.append((control.lang(30160).encode('utf-8'),'RunPlugin(%s)'%fav_uri))
	else:
		try:
			fav_uri = addon.build_plugin_url({'mode': 'add_tv_fav', 'show': show_title,'link': url, 'year':show_year})
		except:
			fav_uri = addon.build_plugin_url({'mode': 'add_tv_fav', 'show': ((show_title).encode('ascii','ignore')),'link':url , 'year':show_year})


		context.append((control.lang(30159).encode('utf-8'),'RunPlugin(%s)'%fav_uri))

	return context

def get_seasons(url):
	if url[0] != '/' and 'http' not in url:
		url = '/' + url

		url = base + url
	if base not in url:
		url = base + url
	html = client.request(url)

	seasons = re.findall('<h3><a href=[\"\'](.+?)[\"\'].+?>Season (\d+)</a></h3>',html)
	
	try:
		imdb = re.findall('title/(tt[\"\']+)',html)[0]
	except:
		imdb = ''
	return imdb,seasons

def get_episodes(url,season_num):
	out = []
	if base not in url:
		url = base + url
	html = client.request(url)
	showtitle = re.findall('h1>.+?>([^\(]+)',html)[0]
	episodes = re.findall('href=[\"\'](.+?season-%s[^\"\']+)[\"\'].+?<strong>Episode</strong>\s*(\d+)\s*-\s*([^<]+)<'%(season_num),html)
	try:
		imdb = re.findall('title/(tt[\"\']+)',html)[0]
	except:
		imdb = ''

	if control.setting('specials')=='false':
		last_num = 0
		for e in episodes:
			if 'special:' in e[2].lower() or 'special-' in e[2].lower():
				continue
			if (int(e[1]) - last_num) > 10:
				continue
			out.append(e)
			last_num = int(e[1])

	else:
		out = episodes

	return imdb,showtitle,out



def sort_links(links):
	listout = []
	sort = control.setting('enable_sorting')
	if sort!='false':
		sorting = control.setting('sort')
		sort_list = sorting.split(',')

		for s in sort_list:
			for l in links:
				if s in l:
					listout.append(l)

		for l in links:
			if l not in listout:
				listout.append(l)
		return listout

	else:
		return links

def get_selection(sources):
	out = []
	for s in sources:
		out.append(urlparse.urlparse(s).netloc.replace('www.','').replace('http://','').replace('https://','').replace('embed','').lstrip('.'))
	return out

def get_sources(url):
	if 'iwatch' in url:
		return get_iwatch(url)
	html = client.request(url)
	black = control.setting('source_blacklist')
	if black!= '':
		blacklist=black.split(',')
	else:
		blacklist=[] 
	links = re.findall('/(?:go|stream)?.php\?(?:url=)?([^\"\']+)[\"\']',html)
	out=[]
	ind=0
	import base64
	for link in links:

		link = base64.b64decode(link)
		link = re.findall('(https?:/[^$]+)',link)[0]
		for b in blacklist:
			if b not in link:
				out.append(link)
		if len(blacklist)==0:
			out.append(link)

		

	out = sort_links(out)
	sl = get_selection(out)
	return out,sl

def resolve_iwatch(url):
	html = client.request(url)
	match = re.search('<iframe name="frame" class="frame" src="([^"]+)', html)
	if match:
		return match.group(1)


def get_month():
    import datetime
    now = datetime.datetime.now()
    out=[]
    for i in range(30):
        date = now - datetime.timedelta(hours=i*24)
        year = date.year
        day = date.day
        month = date.month
        name = _translate(date.strftime("%A")).decode('utf-8')
        mnth = _translate(date.strftime("%B")).decode('utf-8')
        out.append([name,day,month,year,mnth])
    return out

def _translate(str):
	dictionary = {'January': control.lang(30528).encode('utf-8'),
	'February': control.lang(30529).encode('utf-8'),
	'March': control.lang(30530).encode('utf-8'),
	'April': control.lang(30531).encode('utf-8'),
	'May': control.lang(30532).encode('utf-8'),
	'June': control.lang(30533).encode('utf-8'),
	'July': control.lang(30534).encode('utf-8'),
	'August': control.lang(30535).encode('utf-8'),
	'September': control.lang(30536).encode('utf-8'),
	'October': control.lang(30537).encode('utf-8'),
	'November': control.lang(30538).encode('utf-8'),
	'December': control.lang(30539).encode('utf-8'),
	'Monday': control.lang(30521).encode('utf-8'),
	'Tuesday': control.lang(30522).encode('utf-8'),
	'Wednesday': control.lang(30523).encode('utf-8'),
	'Thursday': control.lang(30524).encode('utf-8'),
	'Friday': control.lang(30525).encode('utf-8'),
	'Saturday': control.lang(30526).encode('utf-8'),
	'Sunday': control.lang(30527).encode('utf-8'),
	'Action': control.lang(30110).encode('utf-8'),
	'Adventure': control.lang(30111).encode('utf-8'),
	'Animation': control.lang(30112).encode('utf-8'),
	'Biography': control.lang(30113).encode('utf-8'),
	'Comedy': control.lang(30114).encode('utf-8'),
	'Crime': control.lang(30115).encode('utf-8'),
	'Documentary': control.lang(30116).encode('utf-8'),
	'Drama': control.lang(30117).encode('utf-8'),
	'Family': control.lang(30118).encode('utf-8'),
	'Fantasy': control.lang(30119).encode('utf-8'),
	'Game-Show': control.lang(30120).encode('utf-8'),
	'History': control.lang(30121).encode('utf-8'),
	'Horror': control.lang(30122).encode('utf-8'),
	'Japanese': control.lang(30123).encode('utf-8'),
	'Korean': control.lang(30124).encode('utf-8'),
	'Music': control.lang(30125).encode('utf-8'),
	'Musical': control.lang(30126).encode('utf-8'),
	'Mystery': control.lang(30127).encode('utf-8'),
	'Reality - TV': control.lang(30128).encode('utf-8'),
	'Romance': control.lang(30129).encode('utf-8'),
	'Sci-Fi': control.lang(30130).encode('utf-8'),
	'Short': control.lang(30131).encode('utf-8'),
	'Sport': control.lang(30132).encode('utf-8'),
	'Talk - Show': control.lang(30133).encode('utf-8'),
	'Thriller': control.lang(30134).encode('utf-8'),
	'War': control.lang(30135).encode('utf-8'),
	'Western': control.lang(30136).encode('utf-8')
	}
	try:
		a = dictionary[str]
	except:
		a = str
	return a


def get_episodes_calendar(day,month,year):
	url = 'https://www.iwatchonline.ph/tv-schedule?day=%s&month=%s&year=%s'%(day.lstrip("0"),month.lstrip("0"),year)
	html = client.request(url)
	eps = re.findall('href="(.+?s(\d+)e(\d+))">(.+?) \((\d+)\)</a>',html)
	return eps

def get_iwatch(url):
	tuples = []
	html = client.request(url)
	table = client.parseDOM(html, 'table', attrs={'id':'streamlinks'})[0]
	pts = client.parseDOM(table, 'tr', {'id': 'pt\d+'})
	for p in pts:
		try:
			url = re.findall('href="([^"]+)',p)[0]
			host = re.findall('img.*>\s*([^<\s]+)\s*<',p)[0].lower()
			tuples.append((url,host))
		except:
			pass
		
	links,hosts = sort_iw(tuples)

	

	return links,hosts
	

def sort_iw(tuples):
	sort = control.setting('enable_sorting')
	black = control.setting('source_blacklist')
	if black!= '':
		blacklist=black.split(',')
	else:
		blacklist=[] 

	listout = []
	hostout = []
	if sort != 'false':
		sorting = control.setting('sort')
		sort_list = sorting.split(',')
		for s in sort_list:
			for b in blacklist:
				for t in tuples:
					if s in t[1] and b not in t[1]:
						listout.append(t[0])
						hostout.append(t[1])
			if len(blacklist)==0:
				for t in tuples:
					if s in t[1] and b not in t[1]:
						listout.append(t[0])
						hostout.append(t[1])


		for b in blacklist:
			for t in tuples:
				if t[0] not in listout and b not in t[1]:
					listout.append(t[0])
					hostout.append(t[1])
		if len(blacklist)==0:
			for t in tuples:
				if t[0] not in listout:
					listout.append(t[0])
					hostout.append(t[1])
		return listout,hostout
	else:
		links,sources=[],[]
		for t in tuples:
			for b in blacklist:
				if b not in t[1]:
					links.append(t[0])
					sources.append(t[1])
			if len(blacklist)==0:
				links.append(t[0])
				sources.append(t[1])

		return links,sources

def search(query):

	url = base + '/search.php?q=%s'%(urllib.quote_plus(query))
	html = client.request(url)
	tag = client.parseDOM(html, 'div',attrs={'class':'found'})[0]
	shows = re.findall('<a href="(.+?)" target="_blank">(.+?) \((\d+)\)</a>',tag)

	return shows