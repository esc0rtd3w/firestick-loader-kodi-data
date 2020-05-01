
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
import urllib
import net

import wco_utils as utils


def Resolve(html):
    try:    
        results = []

        urls = re.compile('<iframe id.+?src="(.+?)".+?</iframe>').findall(html)

        for url in urls:
            if 'cizgifilmlerizle' in url:
                DoResolve(url, results)

            if 'animeuploads' in url:                
                DoResolve(url, results)

            if 'vid44.php' in url:
                url = re.compile('iframe src=\"(.+)\" frameborder').search(html).group(1)
                html = utils.GetHTML(url)
                url = re.compile('file: \"(.+)\",\\r  height').search(html).group(1)
                results.append([url, text])

    except:
        pass

    if len(results) == 0:
        results = [[None, 'Error Resolving URL']]

    return results


def DoResolve(url, results):
    try:        
        import wco_utils as utils
        theNet = net.Net()

        data = {'fuck_you' : '', 'confirm' : 'Click+Here+to+Watch+Free%21%21'}
        url  = url.replace(' ', '%20')

        #theNet.set_user_agent('Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        theNet.set_user_agent(utils.getUserAgent())

        html  = theNet.http_POST(url, data).content.replace('\n', '').replace('\t', '')        

        links = re.compile('file:.+?"(.+?)",.+?label:.+?"(.+?)"').findall(html)
        for link in links:
            try:    results.append([link[0], link[1]])
            except: pass        

        if len(links) == 0:
            links = re.compile(';file=(.+?)&provider=http\'').findall(html)
            for link in links:
                results.append([urllib.unquote_plus(link), ''])

        if len(links) == 0:
            links = re.compile('file:"(.+?)"').findall(html.replace(' ', ''))
            for link in links:
                results.append([link, ''])


    except Exception, e:
        pass

    return results