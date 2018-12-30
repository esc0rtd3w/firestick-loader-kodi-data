# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from BeautifulSoup import BeautifulSoup as bs
import urllib2
import urllib
import HTMLParser
import sys
import json
import re
import client,convert
from log_utils import log



domain="http://projectfreetv.so"




def read_url(url):
    return client.request(url)



def get_last_days():
	html=read_url(domain + '/calendar/')
	soup=bs(html)
	days=soup.findAll('div',{'class':'column5'})
	out=[]
	a=len(days)
	for i in range(a-1,-1,-1):
		day=days[i].find('h4').getText()

		out+=[[day, i]]
	return out



def get_day_eps(ind):
	html=read_url(domain + '/calendar/')
	soup=bs(html)
	out=[]
	day=soup.findAll('div',{'class':'column5'})[ind]
	
	links=day.findAll('li')
	for i in range(len(links)):
		link=links[i].find('a')['href']

		name=links[i].find('a').getText()
		try:
			show, season, episode = re.findall('(.+?)\s*[Ss]eason\s*(\d+)\s*[Ee]p.+?\s*(\d+)',name)[0]
			out+=[[show,season,episode,link]]
		except:
			pass
	return out

def get_last_eps():
	html=read_url(domain )
	soup=bs(html)
	out=[]
	day=soup.findAll('div',{'class':'column5'})
	for i in range(1,-1,-1):
		links=day[i].findAll('li')
		for i in range(len(links)):


			link=links[i].find('a')['href']
			name=links[i].find('a').getText()
			try:
				show, season, episode = re.findall('(.+?)\s*[Ss]eason\s*(\d+)\s*[Ee]p.+?\s*(\d+)',name)[0]
				out+=[[show,season,episode,link]]
			except:
				pass

	return out

def get_alphabet():
	html = read_url('http://projectfreetv.so/watch-tv-series/')
	letters = re.findall('href=[\"\']\#mctm\-([^\"\']+)[\"\']',html)
	return letters

def get_shows_by_letter(letter):
	abc = get_alphabet()
	html=read_url(domain + '/watch-tv-series/')
	
	soup=bs(html)
	tags=soup.findAll('div',{'class':'tagindex'})
	for i in range(len(abc)):
		if abc[i]==letter:
			index=i
	out=[]
	tag=tags[index]
	lis=tag.findAll('li')
	for i in range(len(lis)):
		link=lis[i].find('a')['href']
		name=lis[i].find('a')['title']
		out+=[[name,link]]
	return out

def get_seasons(url):
	html=read_url(url)
	soup=bs(html)
	tag=soup.find('ul')
	seasons=tag.findAll('li')
	out=[]
	for i in range(len(seasons)):
		link=seasons[i].find('a')['href']
		name=seasons[i].getText().lower()

		ind=name.index('season')
		name=name[ind:].title()

		out+=[[name,link]]
	return out


def get_episodes(url):
	html=read_url(url)
	html = convert.unescape(html.decode('utf-8'))
	soup=bs(html)
	
	trs=soup.findAll('tr')
	out=[]
	aa=len(trs)-1
	
	for i in range(aa,-1,-1):
		link=trs[i].find('a')['href']
		name=trs[i].find('a').getText().encode('utf-8', 'xmlcharrefreplace')
		if 'reclame' not in link:
			try:
				show, season, episode = re.findall('(.+?)\s*[Ss]eason\s*(\d+)\s*[Ee]p.+?\s*(\d+)',name)[0]
				out+=[[show,season,episode,link]]
			except:
				pass
	
		
		
	try:
		tag=soup.find('div',{'class':'pagination'})

	except:
		tag=None
	if tag==None:
		pages=False
	else:
		pages=True
	if pages==True:
		try:
			lis=tag.find('li',{'class':'current'})
			next_page=lis.findNext('li').find('a')['href']
		except:
			next_page='last'
	else:
		next_page=False
	return out,next_page

def get_latest_movies(page):
	if page!='1':
		url=domain + '/movies/page/%s/'%page
	else:
		url=domain + '/movies/'
	html=read_url(url)
	soup=bs(html)
	out=[]
	tags=soup.findAll('a',{'id':'featured-thumbnail'})
	for i in range(len(tags)):
		link=tags[i]['href']
		thumb=tags[i].find('img')['src']
		title=tags[i]['title']
		try:
			b_ind=title.index('(')
			year=title[b_ind+1:len(title)-1]
		except:
			year=''
		title=title[:b_ind-1]

		out+=[[title,year,thumb,link]]
	return out

def get_movies_year(year,page):

	if page!='1':
		url=domain + '/movies/search/%s/page/%s'%(year,page)
	else:
		url=domain + '/movies/search/%s'%year

	html=read_url(url)
	soup=bs(html)
	out=[]
	tags=soup.findAll('a',{'id':'featured-thumbnail'})
	for i in range(len(tags)):
		link=tags[i]['href']
		thumb=tags[i].find('img')['src']
		title=tags[i]['title']
		try:
			b_ind=title.index('(')
			year=title[b_ind+1:len(title)-1]
		except:
			year=''
		title=title[:b_ind-1]

		out+=[[title,year,thumb,link]]
	return out

def get_movies_genre(genre,page):
	#/movies/free/action/
	if page!='1':
		url=domain + '/movies/free/%s/page/%s'%(genre,page)
	else:
		url=domain + '/movies/free/%s'%genre

	html=read_url(url)
	soup=bs(html)
	out=[]
	tags=soup.findAll('a',{'id':'featured-thumbnail'})
	for i in range(len(tags)):
		link=tags[i]['href']
		thumb=tags[i].find('img')['src']
		title=tags[i]['title']
		try:
			b_ind=title.index('(')
			year=title[b_ind+1:len(title)-1]
		except:
			year=''
		title=title[:b_ind-1]

		out+=[[title,year,thumb,link]]
	return out



def search(url):
	
	
		

		html=read_url(url)
		soup=bs(html)
		out=[]
		tags=soup.findAll('a',{'id':'featured-thumbnail'})
		for i in range(len(tags)):
			link=tags[i]['href']
			thumb=tags[i].find('img')['src']
			title=tags[i]['title']
			try:
				b_ind=title.index('(')
				year=title[b_ind+1:len(title)-1]
			except:
				year=''
			title=title[:b_ind-1]

			out+=[[title,year,thumb,link]]

		try:
			tag=soup.find('div',{'class':'pagination'})

		except:
			tag=None
		if tag==None:
			pages=False
		else:
			pages=True
		if pages==True:
			try:
				lis=tag.find('li',{'class':'current'})
				next_page=lis.findNext('li').find('a')['href']
			except:
				next_page='last'
		else:
			next_page=False
		return out,next_page
		


def get_link(url):
	html=read_url(url)
	link=re.findall('<a.+?href=[\"\'](.+?)[\"\']><input.+?value=[\"\']Continue to video[\"\']',html)[0]

	
	return link

def get_show_from_ep(url):
	html=read_url(url)
	soup=bs(html)
	return soup.find('span',{'class':'thecategory'}).findAll('a')[1]['href']
def get_all_shows():
	out=[]
	html=read_url('http://projectfreetv.so/watch-tv-series/')
	soup=bs(html)
	tags=soup.findAll('ul',{'class':'links'})
	reg='<a title="(.+?)" href="(.+?)">'
	for tag in tags:


		listy=re.findall(re.compile(reg),str(tag))
		items=[]
		for i in range(len(listy)):
			lista=list(listy[i])
			out+=[lista]
	return out

def get_show_img(url):
	html=read_url(url)
	soup=bs(html)
	return soup.find('div',{'style':'float:left; margin-right:20px;'}).find('img')['src']

def search_shows(query):
	words=query.encode('ascii','ignore').lower().split(' ')
	shows= get_all_shows()
	br=0
	pom=0
	out=[]
	for show in shows:
		for word in words:

			if word.encode('ascii','ignore') in show[0].lower():
				br+=1

		if br>0:
			tup=(br,pom)
			out.append(tup)
		br=0
		pom+=1
	from operator import itemgetter
	out=sorted(out,key=lambda x: x[0], reverse=True)
	outt=[]
	for i in range(len(out)):
		outt+=[shows[out[i][1]]]

	return outt

	