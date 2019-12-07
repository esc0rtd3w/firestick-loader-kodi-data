# -*- coding: utf-8 -*-
#:-----------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para enlaces a torrent y magnet versión mínima
# adaptadtado a livestream
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urllib

def get_video_url( page_url ):

    data = urllib.quote_plus(page_url)
    video_url = 'plugin://plugin.video.pulsar/play?uri='+data

    return video_url

