# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para playedto adaptadtado a livestream
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urllib2
import re

def get_video_url( page_url ):

    # Normaliza la URL
    if not page_url.startswith("http://streamin.to/embed-"):
        videoid = re.findall( 'streamin.to/([a-z0-9A-Z]+)' ,page_url ,flags=re.DOTALL )[0]
        page_url = "http://streamin.to/embed-"+videoid+".html"

    # Descarga la página
    headers = {'User-agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0'}
    req = urllib2.Request(page_url,None,headers)
    res = urllib2.urlopen(req)
    data = res.read()
    res.close()

    # Extrae la URL
    host = re.findall( 'image: "(http://[^/]+/)' ,data ,flags=re.DOTALL )[0]
    path = re.findall( 'file: ".*?h=([^"]+)"' ,data ,flags=re.DOTALL )[0]
    flv = "/v.flv"
    video_url = host+path+flv

    return video_url

