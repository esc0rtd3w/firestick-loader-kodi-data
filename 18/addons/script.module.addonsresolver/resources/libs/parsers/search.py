# -*- coding: UTF-8 -*-
# by Mafarricos
# email: MafaStudios@gmail.com
# This program is free software: GNU General Public License

import urllib2,xbmcaddon,xbmcgui,re,urllib,json,threading
from resources.libs import basic
import links
from BeautifulSoup import BeautifulSoup

def basic_search(searchurl,name,imdb,year,expression,type):
	if type == 'IMDB': searchresult = basic.open_url(searchurl % (imdb))
	elif type == 'NameYear': searchresult = basic.open_url(searchurl % (name+' ('+year+')'))
	elif type == 'Name': searchresult = basic.open_url(searchurl % (name))
	try:  return re.compile(expression).findall(searchresult)[0].replace('\\','')
	except: 
		if type == 'NameYear': 
			searchresult = basic.open_url(searchurl % (name))
			try:  return re.compile(expression).findall(searchresult)[0]
			except: return False
		else: return False

def _sdpsearch(name,link,result):
	sdp = basic.open_url(link % (urllib.quote_plus(name)))
	if sdp:
		if 'Nenhuma mensagem corresponde' in sdp or 'nothing matched' in sdp: result.append('NOTFOUND')
		else: result.append('MATCH')
	
def sdpsearch(name,imdb):
	threads = []
	result = []
	for i in range(7): threads.append(threading.Thread(name=name+str(i),target=_sdpsearch,args=(name,links.link().sdp_search_add[i],result, )))
	[i.start() for i in threads]
	[i.join() for i in threads]
	if result:
		for res in result: 
			if 'MATCH' in res: return res

def ytssearch(imdb_id):
	try:
		quality = []
		magnet = []
		try:
			yts = basic.open_url(links.link().yts_search % (imdb_id))
			jtys = json.loads(yts)
		except: return '',''
		if 'No movies found' in str(jtys): return '',''
		for j in jtys["data"]["movies"]:
			for i in j["torrents"]:
				#quality.append(j["Quality"]+'_'+j["Size"])
				quality.append(i["quality"])
				magnet.append(links.link().yts_magnet % (i["hash"],j["title_long"]))
		return quality,magnet
	except BaseException as e: print '##ERROR-addonsresolver:ytssearch: '+str(imdb_id)+' '+str(e)

def icesearch(title):
	if title.lower().startswith('the '): title2 = title.lower().replace('the ','')
	else: title2 = title
	if title2[0].isalpha(): url = links.link().ice_base + "/movies/a-z/" + title2[0].upper()
	else: url = links.link().ice_base + "/movies/a-z/1"
	html = basic.open_url(url)
	soup = BeautifulSoup(html)
	link = soup.find("a", href=re.compile("ip.php"), text=title)
	if link: return links.link().ice_base+link.parent["href"]
	else: return None