
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

import wco_utils as utils


def Resolve(html):
    if not 'veoh' in html:
        return [[None, 'Error Resolving URL']]

    ret  = None
    text = ''

    try:
        id   = re.compile('veoh.php\?v=(.+?)&').search(html).group(1)
        url  = 'http://www.veoh.com/rest/video/%s/details' % id
        html = utils.getHTML(url, useCache=False)
        if ' items="0"' in html:
            text = 'Video has been removed from Veoh'
        else:
            ret  = re.compile('fullPreviewHashPath="(.+?)"').search(html).group(1)
    except Exception, e:
        text = 'Error Resolving Veoh URL'

    return [[ret, text]]