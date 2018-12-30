# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para powvideo
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config
from core import jsunpack

def test_video_exists( page_url ):
    logger.info("pelisalacarta.powvideo test_video_exists(page_url='%s')" % page_url)
    
    return True,""

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("pelisalacarta.powvideo get_video_url(page_url='%s')" % page_url)

    # Lo pide una vez
    headers = [['User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14']]
    data = scrapertools.cache_page( page_url , headers=headers )
    #logger.info("data="+data)
    
    try:
        '''
        <input type="hidden" name="op" value="download1">
        <input type="hidden" name="usr_login" value="">
        <input type="hidden" name="id" value="auoxxtvyquoy">
        <input type="hidden" name="fname" value="Star.Trek.Into.Darkness.2013.HD.m720p.LAT.avi">
        <input type="hidden" name="referer" value="">
        <input type="hidden" name="hash" value="1624-83-46-1377796069-b5e6b8f9759d080a3667adad637f00ac">
        <input type="submit" name="imhuman" value="Continue to Video" id="btn_download">
        '''
        op = scrapertools.get_match(data,'<input type="hidden" name="op" value="(down[^"]+)"')
        usr_login = ""
        id = scrapertools.get_match(data,'<input type="hidden" name="id" value="([^"]+)"')
        fname = scrapertools.get_match(data,'<input type="hidden" name="fname" value="([^"]+)"')
        referer = scrapertools.get_match(data,'<input type="hidden" name="referer" value="([^"]*)"')
        hashvalue = scrapertools.get_match(data,'<input type="hidden" name="hash" value="([^"]*)"')
        submitbutton = scrapertools.get_match(data,'<input type="submit" name="imhuman" value="([^"]+)"').replace(" ","+")

        import time
        time.sleep(5)

        # Lo pide una segunda vez, como si hubieras hecho click en el banner
        #op=download1&usr_login=&id=auoxxtvyquoy&fname=Star.Trek.Into.Darkness.2013.HD.m720p.LAT.avi&referer=&hash=1624-83-46-1377796019-c2b422f91da55d12737567a14ea3dffe&imhuman=Continue+to+Video
        #op=search&usr_login=&id=auoxxtvyquoy&fname=Star.Trek.Into.Darkness.2013.HD.m720p.LAT.avi&referer=&hash=1624-83-46-1377796398-8020e5629f50ff2d7b7de99b55bdb177&imhuman=Continue+to+Video
        post = "op="+op+"&usr_login="+usr_login+"&id="+id+"&fname="+fname+"&referer="+referer+"&hash="+hashvalue+"&imhuman="+submitbutton
        headers.append(["Referer",page_url])
        data = scrapertools.cache_page( page_url , post=post, headers=headers )
        #logger.info("data="+data)
    except:
        import traceback
        traceback.print_exc()
    
    # Extrae la URL
    logger.info("data="+data)
    data = scrapertools.find_single_match(data,"<script type='text/javascript'>(.*?)</script>")
    logger.info("data="+data)
    data = jsunpack.unpack(data)
    logger.info("data="+data)
    data = data.replace("\\","")

    media_url = scrapertools.find_single_match(data,"file:'([^']+)'")
    video_urls = []
    video_urls.append( [ scrapertools.get_filename_from_url(media_url)[-4:]+" [powvideo]",media_url])

    for video_url in video_urls:
        logger.info("[powvideo.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # http://powvideo.net/embed-sbb9ptsfqca2
    patronvideos  = 'powvideo.net/embed-([a-z0-9]+)'
    logger.info("pelisalacarta.powvideo find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[powvideo]"
        url = "http://powvideo.net/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'powvideo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    # http://powvideo.net/auoxxtvyoy
    patronvideos  = 'powvideo.net/([a-z0-9]+)'
    logger.info("pelisalacarta.powvideo find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[powvideo]"
        url = "http://powvideo.net/"+match
        if url not in encontrados and match!="embed":
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'powvideo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)
            
    return devuelve

def test():
    video_urls = get_video_url("http://powvideo.net/auoxxtvyquoy")

    return len(video_urls)>0