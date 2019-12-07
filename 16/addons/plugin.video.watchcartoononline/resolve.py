
#
#      Copyright (C) 2013 Sean Poyser
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

import re
import os
import sys

import wco_utils as utils


HOME = utils.ADDON.getAddonInfo('path')

def ResolveURL(url):
    #print url
    #url = 'http://www.watchcartoononline.com/axis-powers-hetalia-episode-46-english-subbed' #vweed
    #url = 'http://www.watchcartoononline.com/halo-legends-episode-8-english-dubbed' #veoh
    #url = 'http://www.watchcartoononline.com/american-dad-season-1-episode-20-roger-n-me'#cizgifilmlerizle
    #url = 'http://www.watchcartoononline.com/adventures-of-sonic-the-hedgehog-episode-66-sonic-christmas-blast' #Youtube
    #url = 'http://www.watchcartoononline.com/tmnt-season-7-episode-13-wedding-bells-and-bytes' #Youtube 2 PARTS
    #url = 'http://www.watchcartoononline.com/thundercats-2011-premiere' #movieweb
    #url = 'http://www.watchcartoononline.com/hacklegend-of-the-twilight-episode-12-english-dubbed'
    #url = 'http://www.watchcartoononline.com/mr-bean-the-animated-series-episode-49-in-the-pink' #YouTube GEOLOCKED embeded

    ImportModules()


    html = utils.getHTML(url)
    html = html.replace('"Click Here!!"</a></div>', '')

    url = None
    msg = None

    resolved = []

    match = re.compile('<div class=\'postTabs_divs(.+?)</div>').findall(html)  

    try:
        for item in match:   
            for module in MODULES:                        
                links = MODULES[module].Resolve(item)
                for link in links:                                   
                    if link[0] != None:                       
                        resolved.append([module.replace('_', ''), link[0], link[1]])
    except Exception, e:
        pass

    return resolved


def ImportModules():
    global MODULES
    MODULES = dict()

    libPath = os.path.join(HOME, 'resolvers')
    sys.path.insert(0, libPath)

    module = []

    import glob
    lib   = os.path.join(HOME, 'resolvers', '_*.py')
    files = glob.glob(lib)
    for name in files:
        name = name.rsplit(os.sep, 1)[1]
        if name.rsplit('.', 1)[1] == 'py':
            module.append(name.rsplit('.', 1)[0])

    modules = map(__import__, module)

    for module in modules:
        MODULES[module.__name__] = module
