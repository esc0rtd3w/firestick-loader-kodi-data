
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
import json

import wco_utils as utils

def Resolve(html):
    if not 'movieweb' in html:
        return []

    ret  = None
    text = ''
    try:
        id   = re.compile('http://www.movieweb.com/v/(.+?)"').search(html).group(1)
        url  = 'http://www.movieweb.com/v/%s/play?s=1&idx=0&e=1' % id
        html = utils.getHTML(url, useCache=False)
        
        jsn = json.loads(html)

        url = str(jsn['url_img']).split('.img', 1)[0]
        url += '/'
        url += jsn['videoId']
        url += '_'
        url += str(jsn['ii']) #might be i
        url += jsn['iii']
        url += '?'
        url += jsn['iiii']
        ret  = url
    except Exception, e:        
        text = 'Error Resolving Movieweb URL'

    return [[ret, text]]