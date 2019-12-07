# -*- coding: utf-8 -*-
################################################################################
# |                                                                            #
# |     ______________________________________________________________         #
# |     :~8a.`~888a:::::::::::::::88......88:::::::::::::::;a8~".a88::|        #
# |     ::::~8a.`~888a::::::::::::88......88::::::::::::;a8~".a888~:::|        #
# |     :::::::~8a.`~888a:::::::::88......88:::::::::;a8~".a888~::::::|        #
# |     ::::::::::~8a.`~888a::::::88......88::::::;a8~".a888~:::::::::|        #
# |     :::::::::::::~8a.`~888a:::88......88:::;a8~".a888~::::::::::::|        #
# |     ::::::::::::  :~8a.`~888a:88 .....88;a8~".a888~:::::::::::::::|        #
# |     :::::::::::::::::::~8a.`~888......88~".a888~::::::::::::::::::|        #
# |     8888888888888888888888888888......8888888888888888888888888888|        #
# |     ..............................................................|        #
# |     ..............................................................|        #
# |     8888888888888888888888888888......8888888888888888888888888888|        #
# |     ::::::::::::::::::a888~".a88......888a."~8;:::::::::::::::::::|        #
# |     :::::::::::::::a888~".a8~:88......88~888a."~8;::::::::::::::::|        #
# |     ::::::::::::a888~".a8~::::88......88:::~888a."~8;:::::::::::::|        # 
# |     :::::::::a888~".a8~:::::::88......88::::::~888a."~8;::::::::::|        #
# |     ::::::a888~".a8~::::::::::88......88:::::::::~888a."~8;:::::::|        #
# |     :::a888~".a8~:::::::::::::88......88::::::::::::~888a."~8;::::|        #
# |     a888~".a8~::::::::::::::::88......88:::::::::::::::~888a."~8;:|        #
# |                                                                            #
# |    Rebirth Addon                                                           #
# |    Copyright (C) 2017 Cypher                                               #
# |                                                                            #
# |    This program is free software: you can redistribute it and/or modify    #
# |    it under the terms of the GNU General Public License as published by    #
# |    the Free Software Foundation, either version 3 of the License, or       #
# |    (at your option) any later version.                                     #
# |                                                                            #
# |    This program is distributed in the hope that it will be useful,         #
# |    but WITHOUT ANY WARRANTY; without even the implied warranty of          #
# |    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the           #
# |    GNU General Public License for more details.                            #
# |                                                                            #
################################################################################

import re
import unicodedata


def get(title):
    if title is None: return
    try:
        title = title.encode('utf-8')
    except:
        pass
    title = re.sub('&#(\d+);', '', title)
    title = re.sub('(&#[0-9]+)([^;^0-9]+)', '\\1;\\2', title)
    title = title.replace('&quot;', '\"').replace('&amp;', '&')
    title = re.sub('\n|([[].+?[]])|([(].+?[)])|\s(vs|v[.])\s|(:|;|-|–|"|,|\'|\_|\.|\?)|\s', '', title).lower()
    return title


def geturl(title):
    if title is None: return
    title = title.lower()
    title = title.translate(None, ':*?"\'\.<>|&!,')
    title = title.replace('/', '-')
    title = title.replace(' ', '-')
    title = title.replace('--', '-')
    return title


def get_simple(title):
    if title is None: return
    title = title.lower()
    title = re.sub('(\d{4})', '', title)
    title = re.sub('&#(\d+);', '', title)
    title = re.sub('(&#[0-9]+)([^;^0-9]+)', '\\1;\\2', title)
    title = title.replace('&quot;', '\"').replace('&amp;', '&')
    title = re.sub('\n|\(|\)|\[|\]|\{|\}|\s(vs|v[.])\s|(:|;|-|–|"|,|\'|\_|\.|\?)|\s', '', title).lower()
    return title


def getsearch(title):
    if title is None: return
    title = title.lower()
    title = re.sub('&#(\d+);', '', title)
    title = re.sub('(&#[0-9]+)([^;^0-9]+)', '\\1;\\2', title)
    title = title.replace('&quot;', '\"').replace('&amp;', '&')
    title = re.sub('\\\|/|-|–|:|;|\*|\?|"|\'|<|>|\|', '', title).lower()
    return title


def query(title):
    if title is None: return
    title = title.replace('\'', '').rsplit(':', 1)[0].rsplit(' -', 1)[0].replace('-', ' ')
    return title


def normalize(title):
    try:
        try: return title.decode('ascii').encode("utf-8")
        except: pass

        return str(''.join(c for c in unicodedata.normalize('NFKD', unicode(title.decode('utf-8'))) if unicodedata.category(c) != 'Mn'))
    except:
        return title