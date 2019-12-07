
# -*- coding: utf-8 -*-
try:
	from BeautifulSoup import BeautifulSoup as bss
except:
	from bs4 import BeautifulSoup as bss
try:
	import urllib2
except:
	import urllib.request as urllib2
	
import urllib, client,xbmcgui,xbmc
import re

def read_url(url):
	return client.request(url)
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

def show_text(heading,anounce):
    class TextBox():

            """Thanks to BSTRDMKR for this code:)"""
            WINDOW=10147; CONTROL_LABEL=1; CONTROL_TEXTBOX=5 # constants
            def __init__(self,*args,**kwargs):
                xbmc.executebuiltin("ActivateWindow(%d)" % (self.WINDOW,)) # activate the text viewer window
                self.win=xbmcgui.Window(self.WINDOW) # get window
                xbmc.sleep(500) # give window time to initialize
                self.setControls()
            def setControls(self):
                self.win.getControl(self.CONTROL_LABEL).setLabel(heading) # set heading
                try: f=open(anounce); text=f.read()
                except: text=anounce
                self.win.getControl(self.CONTROL_TEXTBOX).setText(text); return
    TextBox()

def adfly(url):
    import re
    import urllib2
    import httplib
    from socket import timeout
    import base64
    
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req, timeout=5)
    html = response.read()
    response.close()
    ysmm = re.findall("var ysmm =\s*[\"\']([^\"\']+)[\"\']", html)[0]
    left = ''
    right = ''
    for c in [ysmm[i:i+2] for i in range(0, len(ysmm), 2)]:
        left += c[0]
        right = c[1] + right
    decoded_uri = base64.b64decode(left.encode() + right.encode())[2:].decode()
    if re.search(r'go\.php\?u\=', decoded_uri):
        decoded_uri = base64.b64decode(re.sub(r'(.*?)u=', '', decoded_uri)).decode()

    return decoded_uri

def remove_referer(url):
    return re.sub("referer=.+?(?:&|$)","",url).rstrip('?').rstrip('&')
