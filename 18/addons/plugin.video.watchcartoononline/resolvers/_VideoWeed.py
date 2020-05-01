#
#      Copyright (C) 2014 funnies.
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
import net

import wco_utils as utils

def Resolve(html):
    
    try:  
        if not 'vweed.php' in html:
            return []
 
        html = html.split('.flv',   1)[0]
        html = html.rsplit('src="', 1)[-1]
        url  = html + '.flv'

        url = url.split('"')[0]
        return DoResolve(url)

    except:
        pass

    return []


def DoResolve(url):

    ret  = None
    text = ''
    try:        
        theNet = net.Net()

        data = {'fuck_you' : '', 'confirm' : 'Close%20Ad%20and%20Watch%20as%20Free%20User'}
        url  = url.replace(' ', '%20')

        theNet.set_user_agent('Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')

        html  = theNet.http_POST(url, data).content

        try:
            url  = re.compile('iframe src=\"(.+)\" frameborder').search(html).group(1)
            html = utils.getHTML(url)
            url  = re.compile('file: \"(.+)\",\\r  height').search(html).group(1)
            
        except:
            url  = re.compile('410px\\\' src=\\\'(.+)\\\' scrolling').search(html).group(1)
            html = utils.getHTML(url)

            url  = re.compile('advURL=\"(.+)\";flashvars.cid3').search(html).group(1)
            html = utils.getHTML(url)

            flashfile = re.compile('flashvars.file=\"(.+)\";').search(html).group(1).split('"')[0]           
            flashkey  = re.compile('flashvars.filekey=\"(.+)\";').search(html).group(1).split('"')[0]
            
            url  = 'http://www.videoweed.es/api/player.api.php?file='+flashfile+'&key='+flashkey.replace(".","%2E").replace("-","%2D")
            html = theNet.http_GET(url,headers = { 'Referer' : 'http://www.videoweed.es/player/cloudplayer.swf' , 'Host' : 'www.videoweed.es'}).content
            url  = re.compile('url=(.+\.flv)&title=').search(html).group(1)
            
            domain  = re.compile('http://(.+)/.+').search(url).group(1).split('/')[0]
            url    += '?client=FLASH|Host='+domain+'&User-Agent=Mozilla/5.0 (Windows NT 6.3; WOW64; rv:29.0) Gecko/20100101 Firefox/29.0&Accept=application/octet-stream,text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8&Referer=http://www.videoweed.es/player/cloudplayer.swf&Connection=keep-alive'
               
        url = url.replace(' ', '%20')
        ret = url       
    except:
        text = 'Error Resolving URL'

    return [[ret, text]]
