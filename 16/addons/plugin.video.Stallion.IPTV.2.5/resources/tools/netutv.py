# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para netutv
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config
from core import unpackerjs,unpackerjs3

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[netutv.py] url="+page_url)

    # Lo pide una vez
    headers = [['User-Agent','Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10']]
    data = scrapertools.cache_page( page_url , headers=headers )
    logger.info("data="+data)
    
    '''
    http://netu.tv/watch_video.php?v=96WDAA71A8K
    http://s1.netu.tv/flv/api/files/thumbs/2013/09/17/1373323542a37c1-640x480-1.jpg
    http://s1.netu.tv/hls-vod/flv/api/files/videos/2013/09/17/1373323542a37c1.mp4.m3u8
    '''

    # Extrae la URL
    image_url = scrapertools.get_match( data , '<meta property="og:image" content="([^"]+)"' )
    media_url = image_url.replace("flv/api/files/thumbs","hls-vod/flv/api/files/videos")
    media_url = media_url.replace("-640x480-1.jpg",".mp4.m3u8")

    video_urls = []
    video_urls.append( [ scrapertools.get_filename_from_url(media_url)[-4:]+" [netu.tv]",media_url])

    for video_url in video_urls:
        logger.info("[netutv.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # http://netu.tv/player/embed_player.php?vid=82U4BRSOB4UU&autoplay=no
    patronvideos  = 'netu.tv/player/embed_player.php\?vid\=([A-Z0-9]+)'
    logger.info("[netutv.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[netu.tv]"
        url = "http://netu.tv/watch_video.php?v="+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'netutv' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    # http://netu.tv/watch_video.php?v=96WDAAA71A8K
    patronvideos  = 'netu.tv/watch_video.php\?v\=([A-Z0-9]+)'
    logger.info("[netutv.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[netu.tv]"
        url = "http://netu.tv/watch_video.php?v="+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'netutv' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve

def test():

    #http://www.peliculasid.net/player/netu.php?id=NA44292KD53O
    video_urls = get_video_url("http://netu.tv/watch_video.php?v=NA44292KD53O")

    return len(video_urls)>0