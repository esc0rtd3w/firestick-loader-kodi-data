# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para streamcloud adaptadtado a livestream
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urllib2
import urllib
import re

def get_video_url( page_url ):

    # Normaliza la URL
    if len(page_url.split('/')) < 5:
        page_url = match( page_url, "(http://streamcloud.eu/[a-z0-9]+)" )

    headers = {'User-agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0'}
    req = urllib2.Request(page_url,None,headers)
    res = urllib2.urlopen(req)
    data = res.read()
    res.close()

    op = match( data, 'name="op" value="([^"]+)">' )
    usr_login = match( data, 'name="usr_login" value="([^"]+)">' )
    id = match( data, 'name="id" value="([^"]+)">' )
    fname = match( data, 'name="fname" value="([^"]+)">' )
    referer = match( data, 'name="referer" value="([^"]+)">' )
    hash = match( data, 'name="hash" value="([^"]+)">' )
    imhuman = match( data, 'name="imhuman".*?value="([^"]+)">' )
    
    import time
    time.sleep(10)

    headers = {'User-agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0', 'Referer': page_url}

    values = {'op' : op, 'usr_login' : usr_login, 'id' : id, 'fname' : fname, 'referer' : referer, 'hash' : hash, 'imhuman' : imhuman}

    post = urllib.urlencode(values)

    req = urllib2.Request(page_url,post,headers)
    res = urllib2.urlopen(req)
    data = res.read()
    res.close()

    # Extrae la URL
    video_url = match( data, 'file: "([^"]+)"' )

    return video_url

def match(string,pattern):
    match = ""
    matches = re.findall( pattern ,string,flags=re.DOTALL )
    if len(matches) > 0: match = matches[0]
    return match
