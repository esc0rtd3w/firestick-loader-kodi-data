# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para allmyvideos
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os
import re

from core import scrapertools
from core import logger
from core import config

def test_video_exists( page_url ):
    logger.info("[allmyvideos.py] test_video_exists(page_url='%s')" % page_url)

    # No existe / borrado: http://allmyvideos.net/8jcgbrzhujri
    data = scrapertools.cache_page(page_url)
    #logger.info("data="+data)
    if "<b>File Not Found</b>" in data or "<b>Archivo no encontrado</b>" in data or '<b class="err">Deleted' in data or '<b class="err">Removed' in data or '<font class="err">No such' in data:
        return False,"No existe o ha sido borrado de allmyvideos"
    else:
        # Existe: http://allmyvideos.net/6ltw8v1zaa7o
        patron  = '<META NAME="description" CONTENT="(Archivo para descargar[^"]+)">'
        matches = re.compile(patron,re.DOTALL).findall(data)
        
        if len(matches)>0:
            return True,""
    
    return True,""

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[allmyvideos.py] url="+page_url)

    # Normaliza la URL
    videoid = scrapertools.get_match(page_url,"http://allmyvideos.net/([a-z0-9A-Z]+)")
    page_url = "http://allmyvideos.net/embed-"+videoid+"-728x400.html"
    data = scrapertools.cache_page(page_url)

    if "File was banned" in data:
        data = scrapertools.cache_page(page_url,post="op=download1&usr_login=&id="+videoid+"&fname=&referer=&method_free=1&x=147&y=25")

    # Extrae la URL
    match = re.compile('"file" : "(.+?)",').findall(data)
    media_url = ""
    if len(match) > 0:
        for tempurl in match:
            if not tempurl.endswith(".png") and not tempurl.endswith(".srt"):
                media_url = tempurl

        if media_url == "":
            media_url = match[0]

    video_urls = []

    if media_url!="":
        media_url+= "&direct=false"
        video_urls.append( [ scrapertools.get_filename_from_url(media_url)[-4:]+" [allmyvideos]",media_url])

    for video_url in video_urls:
        logger.info("[allmyvideos.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):

    # Añade manualmente algunos erróneos para evitarlos
    encontrados = set()
    encontrados.add("http://allmyvideos.net/embed-theme.html")
    encontrados.add("http://allmyvideos.net/embed-jquery.html")
    encontrados.add("http://allmyvideos.net/embed-s.html")
    encontrados.add("http://allmyvideos.net/embed-images.html")
    encontrados.add("http://allmyvideos.net/embed-faq.html")
    encontrados.add("http://allmyvideos.net/embed-embed.html")
    encontrados.add("http://allmyvideos.net/embed-ri.html")
    encontrados.add("http://allmyvideos.net/embed-d.html")
    encontrados.add("http://allmyvideos.net/embed-css.html")
    encontrados.add("http://allmyvideos.net/embed-js.html")
    encontrados.add("http://allmyvideos.net/embed-player.html")
    encontrados.add("http://allmyvideos.net/embed-cgi.html")
    encontrados.add("http://allmyvideos.net/embed-i.html")
    encontrados.add("http://allmyvideos.net/images")
    encontrados.add("http://allmyvideos.net/theme")
    encontrados.add("http://allmyvideos.net/xupload")
    encontrados.add("http://allmyvideos.net/s")
    encontrados.add("http://allmyvideos.net/js")
    encontrados.add("http://allmyvideos.net/jquery")
    encontrados.add("http://allmyvideos.net/login")
    encontrados.add("http://allmyvideos.net/make")
    encontrados.add("http://allmyvideos.net/i")
    encontrados.add("http://allmyvideos.net/faq")
    encontrados.add("http://allmyvideos.net/tos")
    encontrados.add("http://allmyvideos.net/premium")
    encontrados.add("http://allmyvideos.net/checkfiles")
    encontrados.add("http://allmyvideos.net/privacy")
    encontrados.add("http://allmyvideos.net/refund")
    encontrados.add("http://allmyvideos.net/links")
    encontrados.add("http://allmyvideos.net/contact")

    devuelve = []

    # http://allmyvideos.net/3sw6tewl21sn
    patronvideos  = 'allmyvideos.net/([a-z0-9]+)'
    logger.info("[allmyvideos.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if len(matches)>0:
        for match in matches:
            titulo = "[allmyvideos]"
            url = "http://allmyvideos.net/"+match
            if url not in encontrados and "embed" not in match:
                logger.info("  url="+url)
                devuelve.append( [ titulo , url , 'allmyvideos' ] )
                encontrados.add(url)
            else:
                logger.info("  url duplicada="+url)

    # http://allmyvideos.net/embed-3sw6tewl21sn.html
    patronvideos  = 'allmyvideos.net/embed-([a-z0-9]+).html'
    logger.info("[allmyvideos.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if len(matches)>0:
        for match in matches:
            titulo = "[allmyvideos]"
            url = "http://allmyvideos.net/"+match
            if url not in encontrados and "-728x400" not in match:
                logger.info("  url="+url)
                devuelve.append( [ titulo , url , 'allmyvideos' ] )
                encontrados.add(url)
            else:
                logger.info("  url duplicada="+url)

    # http://allmyvideos.net/embed-3sw6tewl21sn-728x400.html
    patronvideos  = 'allmyvideos.net/embed-([a-z0-9]+)-728x400.html'
    logger.info("[allmyvideos.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if len(matches)>0:
        for match in matches:
            titulo = "[allmyvideos]"
            url = "http://allmyvideos.net/"+match
            if url not in encontrados:
                logger.info("  url="+url)
                devuelve.append( [ titulo , url , 'allmyvideos' ] )
                encontrados.add(url)
            else:
                logger.info("  url duplicada="+url)

    # http://www.cinetux.org/video/allmyvideos.php?id=3sw6tewl21sn
    patronvideos  = 'allmyvideos.php\?id\=([a-z0-9]+)'
    logger.info("[allmyvideos.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if len(matches)>0:
        for match in matches:
            titulo = "[allmyvideos]"
            url = "http://allmyvideos.net/"+match
            if url not in encontrados:
                logger.info("  url="+url)
                devuelve.append( [ titulo , url , 'allmyvideos' ] )
                encontrados.add(url)
            else:
                logger.info("  url duplicada="+url)

    return devuelve

def test():

    video_urls = get_video_url("http://allmyvideos.net/uhah7dmq2ydp")

    return len(video_urls)>0