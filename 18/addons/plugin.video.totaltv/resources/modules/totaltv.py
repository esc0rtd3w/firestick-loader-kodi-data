
from BeautifulSoup import BeautifulSoup as bs
import urllib2
import urllib
import HTMLParser
import sys
import json
import re
import threading
import Queue

try:
    from addon.common.net import Net
    from addon.common.addon import Addon

except:
    print 'Failed to import script.module.addon.common'
    xbmcgui.Dialog().ok("Total TV Import Failure", "Failed to import addon.common", "A component needed by Total TV is missing on your system", "")
addon = Addon('plugin.video.totaltv', sys.argv)


domain='http://www.watchfree.to'

def read_url(url):
    net = Net()
    html=net.http_GET(url).content
    h = HTMLParser.HTMLParser()
    html = h.unescape(html)
    return html.encode('utf-8')
def popular_today():
	url=domain + '/?sort=views&keyword=&tv='
	html=read_url(url)
	soup=bs(html)
	tag=soup.find('div',{'class':'body'})
	reg=re.compile('<a href="(.+?)" title="(.+?) \((\d+)\)">')

	shows=re.findall(reg,str(tag))
	return shows
	
def popular_today_mov():
	url=domain + '/?sort=views&keyword='
	html=read_url(url)
	soup=bs(html)
	tag=soup.find('div',{'class':'body'})
	reg=re.compile('<a href="(.+?)" title="(.+?) \((\d+)\)">')

	shows=re.findall(reg,str(tag))
	return shows
def search(query):

	url=domain + '/?keyword=%s'%(urllib.quote_plus(query))+'&search_section=2'
	html=read_url(url)
	soup=bs(html)
	tag=soup.find('div',{'class':'body'})
	reg=re.compile('<a href="(.+?)" title="(.+?) \((\d+)\)">')

	shows=re.findall(reg,str(tag))
	return shows
def search_m(query):

	url=domain + '/?keyword=%s'%(urllib.quote_plus(query))+'&search_section=1'
	html=read_url(url)
	soup=bs(html)
	tag=soup.find('div',{'class':'body'})
	reg=re.compile('<a href="(.+?)" title="(.+?) \((\d+)\)">')

	shows=re.findall(reg,str(tag))
	return shows
def movies_popular():
	url=domain + '/?sort=release&keyword='
	html=read_url(url)
	soup=bs(html)
	tag=soup.find('div',{'class':'body'})
	reg=re.compile('<a href="(.+?)" title="(.+?) \((\d+)\)">')

	shows=re.findall(reg,str(tag))
	return shows
def most_popular():
	url=domain + '/?sort=release&keyword=&tv='
	html=read_url(url)
	soup=bs(html)
	tag=soup.find('div',{'class':'body'})
	reg=re.compile('<a href="(.+?)" title="(.+?) \((\d+)\)">')

	shows=re.findall(reg,str(tag))
	return shows
def most_popular_mov():
	url=domain + '/?sort=release&keyword='
	html=read_url(url)
	soup=bs(html)
	tag=soup.find('div',{'class':'body'})
	reg=re.compile('<a href="(.+?)" title="(.+?) \((\d+)\)">')

	shows=re.findall(reg,str(tag))
	return shows
def get_shows_letter(letter):
	url=domain+ letter
	html=read_url(url)
	soup=bs(html)
	tag=soup.find('div',{'class':'body'})
	reg=re.compile('<a href="(.+?)" title="(.+?) \((\d+)\)">')
	shows=re.findall(reg,str(tag))

	return shows
def get_genres_mov():
	url=domain+'/?genres'
	html=read_url(url)
	soup=bs(html)
	tag=soup.find('div',{'class':'body'})
	reg=re.compile('<a href="(.+?)">(.+?)</a>')
	genres=re.findall(reg,str(tag))
	
	return genres
def get_genres():
	url=domain+'/?genres&tv'
	html=read_url(url)
	soup=bs(html)
	tag=soup.find('div',{'class':'body'})
	reg=re.compile('<a href="(.+?)">(.+?)</a>')
	genres=re.findall(reg,str(tag))
	
	return genres
def get_shows(genre):
	url=domain+genre
	html=read_url(url)
	soup=bs(html)
	tag=soup.find('div',{'class':'home'})
	reg=re.compile('<a href="(.+?)".+?>(.+?) \((\d+)\)</a>')
	shows=re.findall(reg,str(tag))

	return shows


def get_seasons(show):
	url=show
	url=domain + show
	if domain not in url:
		url=domain+url
	html=read_url(url)
	soup=bs(html)
	reg=re.compile('<a data-id=".+?" class="season-toggle" href=[\"\'](.+?)[\"\']>Season (\d+)<span style=".+?">')
	seasons=re.findall(reg,str(soup))
	try:
		imdb=re.compile('(?:\"|\')http://www.imdb.com/title/(.+?)(?:\"|\')')
		imdb=re.findall(imdb,html)[0]
	except:pass
	if imdb:
		return imdb,seasons
	else:
		imdb = ''
		return imdb,seasons
def get_episodes(season,season_num):
		url=season
		if domain not in url:
			url=domain + season
		html=read_url(url)
		soup=bs(html)
		tag=soup.find('div',{'class':'show_season'})
		reg=re.compile('<a href="(.+?)">')
		links=list(re.findall(reg,str(tag)))
		reg2=re.compile('<a href=".+?">E(\d+)\s*<span class=".+?"> (.+?)</span>')
		names=re.findall(reg2,str(tag))
		out=[]
 		for i in range(len(links)):
			out+=[[links[i],names[i][1],season_num,names[i][0]]]
		try:
			imdb=re.compile('[\"\']http://www.imdb.com/title/(.+?)[\"\']')
			imdb=re.findall(imdb,str(soup))[0]
		except:pass
		if imdb:
			return imdb,out
		else:
			imdb = ''
			return imdb,out	

def get_imdb(url):
	# if url[0]!='/' and 'http' not in url:
			# url='/'+url+'/'
			# url=domain + url

	# else:
			# url=url+'/'
	if domain not in url:
		url=domain+url
	html=read_url(url)
	soup=bs(html)
	imdb=re.compile('[\"\']http://www.imdb.com/title/(.+?)[\"\']')
	try:
		imdb=re.findall(imdb,str(soup))[0]
	except:
		imdb=''
	
	return imdb
def get_sources(links):
	sources=[]
	ind=0
	for i in range(len(links)):

			sources.insert(ind, '%s. iWatch HD link'%(i+1))
			ind+=1
	
	return sources

def get_ep_url(ep):
	item=[]
	season=ep[1]
	episode=ep[2]
	show_title=ep[3]
	show_year=ep[4]
	sr=search(show_title)
	for i in range(len(sr)):

		if sr[i][2]==show_year:
			ind=i
			
			
			break
	try:
		lst=list(sr[ind])
		
		url=lst[0]
		url=url+'season-%s-episode-%s'%(season.lstrip("0"),episode.lstrip("0"))
		if url[0]!='/' and 'http' not in url:
			url='/'+url+'/'
		else:
			url=url+'/'
		link=url
		
		item=[link,show_title,season,episode,ep[0]]
		return item
	except:
		return ['0',0,0,0,0]
def get_ep_urll(ep,queue):
	item=[]
	season=ep[1]
	episode=ep[2]
	show_title=ep[3]
	show_year=ep[4]
	sr=search(show_title)
	for i in range(len(sr)):

		if sr[i][2]==show_year:
			ind=i
			
			
			break
	try:
		lst=list(sr[ind])
		
		url=lst[0]
		url=url+'season-%s-episode-%s'%(season.lstrip("0"),episode.lstrip("0"))
		if url[0]!='/' and 'http' not in url:
			url='/'+url+'/'
		else:
			url=url+'/'
		link=url
		
		item=[link,show_title,season,episode,ep[0]]
		queue.put(item)
	except:
		pass

def fetch_parallel(eps):
    result = Queue.Queue()
    threads = [threading.Thread(target=get_ep_urll, args = (ep,result)) for ep in eps]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return result

def get_all_queue_result(queue):

    result_list = []
    while not queue.empty():
        result_list.append(queue.get())

    return result_list

def get_parallel(eps):
	from multiprocessing.dummy import Pool as ThreadPool 

	pool = ThreadPool(10) 


	results=pool.map(get_ep_url, eps)


	pool.close() 
	pool.join() 
	return results

