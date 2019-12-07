# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para vidspot adaptadtado a livestream
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urllib2
import re

def get_video_url( page_url ):

    # Normaliza la URL
    videoid = re.findall( "http://vidspot.net/([a-z0-9A-Z]+)" ,page_url ,flags=re.DOTALL )[0]
    page_url = "http://vidspot.net/embed-"+videoid+"-728x400.html"

    headers = {'User-agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0'}
    req = urllib2.Request(page_url,None,headers)
    res = urllib2.urlopen(req)
    data = res.read()
    res.close()

    # Extrae la URL
    video_url = re.findall( '"sources" : \[.*?"file" : "(.+?\?v2)",' ,data ,flags=re.DOTALL )[0]+"&direct=false"

    return video_url

