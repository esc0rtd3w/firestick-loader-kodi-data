# coding: utf-8
# Service Module
__author__ = 'mancuniancol'
from time import asctime
from time import gmtime
from time import localtime
from time import strftime
from time import time

from main import importAll
from tools2 import *


def update_service():
    if settings.value['service'] == 'true':
        # Begin Service
        storage = Storage(settings.storageName, type="dict", eval=True)
        for key, (url, isIntegrated) in storage.database.items():
            if isIntegrated:
                goodSpider()  # to be a smart spider
                importAll(url)


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
