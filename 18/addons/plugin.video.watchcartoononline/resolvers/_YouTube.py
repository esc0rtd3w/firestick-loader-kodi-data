
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

def Resolve(html):   
    try:
        import yt
        return DoResolve(html)
    except:
        pass

    return UseAddon(html)


def DoResolve(html):
    ret  = []
    text = ''

    if not 'youtube' in html:
        return [[None, 'Error Resolving URL']]

    try:
        import yt
        match = re.compile('src="http://.+?.com/v/(.+?)">').findall(html)
        if len(match) < 1:
            return DoResolve2(html)

        for id in match:            
            id  = id.split('?', 1)[0]

            video, links = yt.GetVideoInformation(id)

            if 'best' in video:
                ret.append([video['best'], ''])
            
    except:
        pass

    if len(ret) < 1:
        ret.append([[None, 'Error Resolving URL']])

    return ret


def DoResolve2(html):
    ret  = []
    text = ''

    if not 'youtube' in html:
        return [[None, 'Error Resolving URL']]

    try:
        from simpleYT import yt
        match = re.compile('src="http://.+?.com/embed/(.+?)"').findall(html)

        for id in match:
            video, links = yt.GetVideoInformation(id)

            if 'best' in video:
                ret.append([video['best'], ''])
    except:
        pass

    if len(ret) < 1:
        ret.append([None, 'Error Resolving YouTube URL'])

    return ret


def UseAddon(html):
    ret  = []
    text = ''

    if not 'youtube' in html:
        return [[None, 'Error Resolving URL']]

    try:
        match = re.compile('src="http://.+?.com/v/(.+?)">').findall(html)
        for id in match:
            id  = id.split('?', 1)[0]
            url = 'plugin://plugin.video.youtube/?path=root/video&action=play_video&videoid=%s' % id
            ret.append([url, ''])            
    except:
        ret.append([None, 'Error Resolving YouTube URL'])

    if not CheckYouTube():
        return [None, 'Please install YouTube addon']   

    return ret


def CheckYouTube():
    import xbmcaddon
    import os
    try:
        yt    = 'plugin.video.youtube'
        path  = xbmcaddon.Addon(yt).getAddonInfo('path')
        if os.path.exists(path):
            return True
    except Exception, e:
        print str(e)
        pass

    return False