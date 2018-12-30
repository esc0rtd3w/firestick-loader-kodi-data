#
#       Copyright (C) 2014-2015
#       Sean Poyser (seanpoyser@gmail.com)
#
#  This Program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2, or (at your option)
#  any later version.
#
#  This Program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with XBMC; see the file COPYING.  If not, write to
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
#  http://www.gnu.org/copyleft/gpl.html
#

import xbmcaddon
import os


ADDONID = 'plugin.video.watchcartoononline'
ADDON   = xbmcaddon.Addon(ADDONID)
HOME    = ADDON.getAddonInfo('path')
PROFILE = ADDON.getAddonInfo('profile')
TITLE   = ADDON.getAddonInfo('name')
VERSION = ADDON.getAddonInfo('version')
ARTWORK = os.path.join(HOME, 'resources', 'artwork')
ICON    = os.path.join(HOME, 'icon.png')
URL     = 'http://www.watchcartoononline.io/'



def clean(text):
    text = text.replace('&#8211;', '-')
    text = text.replace('&#8230;', '...')
    text = text.replace('&#215;',  'x')

    text = text.replace('&#8216;', '\'')
    text = text.replace('&#8217;', '\'')
    text = text.replace('&#8220;', '"')
    text = text.replace('&#8221;', '"')
    text = text.replace('&#39;',   '\'')
    text = text.replace('&#038;',  '&')
    text = text.replace('<b>',     '')
    text = text.replace('</b>',    '')
    text = text.replace('&amp;',   '&')
    text = text.replace('\ufeff', '')
    return text


def fixup(text):
    newText    = ''
    ignoreNext = False

    for c in text:
        if ord(c) < 127:
            newText   += c
            ignoreNext = False
        elif ignoreNext:
            ignoreNext = False
        else:
            newText   += ' '
            ignoreNext = True

    newText = newText.strip('/\\')
    return newText

    
def sloppyCompare(str1, str2):
    import re

    sloppyStr1 = re.sub(r'[\W\s_]', '', str1).lower()
    sloppyStr2 = re.sub(r'[\W\s_]', '', str2).lower()
    
    return sloppyStr1 == sloppyStr2

    

def fileSystemSafe(text):
    import re
    return re.sub('[:\\/*?\<>|"]+', '', text).strip()


def getUserAgent():
    #based on method Copyright (C) 2016 lambda
    import random
    BR_VERS = [
        ['%s.0' % i for i in xrange(18, 43)],
        ['37.0.2062.103', '37.0.2062.120', '37.0.2062.124', '38.0.2125.101', '38.0.2125.104', '38.0.2125.111', '39.0.2171.71', '39.0.2171.95', '39.0.2171.99', '40.0.2214.93', '40.0.2214.111',
         '40.0.2214.115', '42.0.2311.90', '42.0.2311.135', '42.0.2311.152', '43.0.2357.81', '43.0.2357.124', '44.0.2403.155', '44.0.2403.157', '45.0.2454.101', '45.0.2454.85', '46.0.2490.71',
         '46.0.2490.80', '46.0.2490.86', '47.0.2526.73', '47.0.2526.80'],
        ['11.0']]
    WIN_VERS = ['Windows NT 10.0', 'Windows NT 7.0', 'Windows NT 6.3', 'Windows NT 6.2', 'Windows NT 6.1', 'Windows NT 6.0', 'Windows NT 5.1', 'Windows NT 5.0']
    FEATURES = ['; WOW64', '; Win64; IA64', '; Win64; x64', '']
    RAND_UAS = ['Mozilla/5.0 ({win_ver}{feature}; rv:{br_ver}) Gecko/20100101 Firefox/{br_ver}',
                'Mozilla/5.0 ({win_ver}{feature}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{br_ver} Safari/537.36',
                'Mozilla/5.0 ({win_ver}{feature}; Trident/7.0; rv:{br_ver}) like Gecko']
    index = random.randrange(len(RAND_UAS))
    agent = RAND_UAS[index].format(win_ver=random.choice(WIN_VERS), feature=random.choice(FEATURES), br_ver=random.choice(BR_VERS[index]))

    #modify Mozilla version to add more randomness
    agent = agent.replace('Mozilla/5.0', 'Mozilla/%d.%d' % (random.randrange(9), random.randrange(9)))
    return agent


def getHTML(url, useCache=True):
    import quicknet
    agent = getUserAgent()

    if useCache:
        html = quicknet.getURL(url, 86400, agent=agent)
    else:
        html = quicknet.getURLNoCache(url, agent=agent)

    return html