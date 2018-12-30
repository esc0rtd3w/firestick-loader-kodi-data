# -*- coding: UTF-8 -*-

import urllib

def escape(string):
     return urllib.quote(string)

def unescape(string):
     return urllib.unquote(string)
