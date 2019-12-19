# -*- coding: utf-8 -*-


import re,urlparse
from liveresolver.modules import client
from liveresolver.modules.log_utils import log

def resolve(url):
    try:
        import hdcastinfo
        return hdcastinfo.resolve(url)
    except:
        return

