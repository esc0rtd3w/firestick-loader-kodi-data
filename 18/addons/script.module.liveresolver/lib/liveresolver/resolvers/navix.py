# -*- coding: utf-8 -*-


import re,urllib,urlparse,base64,json
from liveresolver.modules import client,constants,liveresolver_utils
from liveresolver.modules.log_utils import log
import requests
def resolve(url):
    #try:
        s = requests.Session()

        ref = liveresolver_utils.remove_referer(url)
        result = s.get(url, headers={'User-agent':client.agent()}).text
        log(s.cookies)
        
    #except:
    #    return

