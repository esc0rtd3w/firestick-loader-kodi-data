# coding: utf-8
# Service Module
__author__ = 'mancuniancol'
from tools2 import *
import feedparser
from time import time
from time import asctime
from time import localtime
from time import strftime
from time import gmtime
import random

def update_service():
    if settings.value['service'] == 'true':
        from socket import setdefaulttimeout
        # Begin Service
        storage = Storage(settings.storageName, type="dict", eval=True)
        listUrl = storage.database.values()
        # Begin reading
        magnetsMovie = []
        titlesMovie = []
        magnetsShow = []
        titlesShow = []
        magnetsAnime = []
        titlesAnime = []
        for (url, isIntegrated) in listUrl:
            if url is not '' and isIntegrated:
                goodSpider()  # to be a smart spider
                settings.notification('Checking Online\n%s...' % url)
                settings.log(url)
                setdefaulttimeout(5)
                feeds = feedparser.parse(url)
                for entry in feeds.entries:
                    settings.debug(entry)
                    isMagnet = False
                    for key in entry.keys():
                        if "magnet" in key:
                            isMagnet = True
                            tag = key
                            break
                    if isMagnet:
                        value = entry[tag]
                    else:
                        for link in entry.links:
                            value = link.href  # Taking the last link
                    info = formatTitle(entry.title)
                    if 'MOVIE' in info['type']:
                        titlesMovie.append(entry.title)
                        magnetsMovie.append(value)
                    if 'SHOW' in info['type']:
                        titlesShow.append(entry.title)
                        magnetsShow.append(value)
                    if 'ANIME' in info['type']:
                        titlesAnime.append(entry.title)
                        magnetsAnime.append(value)
        if len(titlesMovie) > 0:
            integration(titles=titlesMovie, magnets=magnetsMovie, typeList='MOVIE',
                        folder=settings.movieFolder, silence=True)
        if len(titlesShow) > 0:
            integration(titles=titlesShow, magnets=magnetsShow, typeList='SHOW',
                        folder=settings.showFolder, silence=True)
        if len(titlesAnime) > 0:
            integration(titles=titlesAnime, magnets=magnetsAnime, typeList='ANIME',
                        folder=settings.animeFolder, silence=True)

if settings.value['service'] == 'true':
    every = 28800  # seconds
    previous_time = time()
    settings.log("Persistent Update Service starting...")
    update_service()
    while (not xbmc.abortRequested) and settings.value["persistent"] == 'true':
        if time() >= previous_time + every:  # verification
            previous_time = time()
            update_service()
            settings.log('Update List at %s' % asctime(localtime(previous_time)))
            settings.log('Next Update in %s' % strftime("%H:%M:%S", gmtime(every)))
            update_service()
        sleep(1)

del settings
del browser
