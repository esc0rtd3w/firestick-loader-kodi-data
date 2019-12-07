# -*- coding: utf-8 -*-
try:
	from BeautifulSoup import BeautifulSoup as bss
except:
	from bs4 import BeautifulSoup as bs
try:
	import urllib2
except:
	import urllib.request as urllib2
	
import urllib
import re

def read_url(url):
	html=urllib2.urlopen(url).read()
	try:
		import HTMLParser
		h = HTMLParser.HTMLParser()
		html = h.unescape(html)
	except:
		pass
	try:
		return html.encode('utf-8')
	except:
		return html
def get_soup(url):
	return bs(read_url(url))

def bs(html):
	return bss(html)


def remove_tags(text):
	TAG_RE = re.compile(r'<[^>]+>')
	return TAG_RE.sub('', text)

def normal(string):
    string=string.replace('Š','S').replace('Ž','Z').replace('Č','C').replace('Ć','C').replace('Đ','D')
    return string.replace('š','s').replace('ž','z').replace('č','c').replace('ć','c').replace('đ','d')