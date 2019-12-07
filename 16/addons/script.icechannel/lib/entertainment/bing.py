
#
#      Copyright (C) 2015 Mikey1234
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
#  This code is a derivative of the YouTube plugin for XBMC and associated works
#  released under the terms of the GNU General Public License as published by
#  the Free Software Foundation; version 3


import re
import random,urllib

BROWSERS = (
    # Top most popular browsers in my access.log on 2009.02.12
    # tail -50000 access.log |
    #  awk -F\" '{B[$6]++} END { for (b in B) { print B[b] ": " b } }' |
    #  sort -rn |
    #  head -20
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.6) Gecko/2009011913 Firefox/3.0.6',
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.0.6) Gecko/2009011912 Firefox/3.0.6',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.6) Gecko/2009011913 Firefox/3.0.6 (.NET CLR 3.5.30729)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.6) Gecko/2009020911 Ubuntu/8.10 (intrepid) Firefox/3.0.6',
    'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.0.6) Gecko/2009011913 Firefox/3.0.6',
    'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.0.6) Gecko/2009011913 Firefox/3.0.6 (.NET CLR 3.5.30729)',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/1.0.154.48 Safari/525.19',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648)',
    'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.0.6) Gecko/2009020911 Ubuntu/8.10 (intrepid) Firefox/3.0.6',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.5) Gecko/2008121621 Ubuntu/8.04 (hardy) Firefox/3.0.5',
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_6; en-us) AppleWebKit/525.27.1 (KHTML, like Gecko) Version/3.2.1 Safari/525.27.1',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
)

def Search(url,search_term,extractor=''):
        
        from entertainment.net import Net
        net = Net(cached=False)
        
        UA=random.choice(BROWSERS)
        headers={'User-Agent' : UA}
        
        URL='https://www.bing.com/search?q=%s+site:%s' % (search_term.replace(' ','+'),url)
        
        link = net.http_GET(URL,headers=headers).content.replace('<strong>','').replace('</strong>','')
        
        match=re.compile('<h2><a href="(.+?)" h=".+?">(.+?)</a>').findall(link)
        
        uniques=[]
        returnme=[]
        
        for URL ,TITLE in match:
                
            movie_url = urllib.unquote(URL)
            
            if movie_url not in uniques:
                uniques.append(movie_url)
                
                if extractor=='':
                    RETURN={'url': u'%s'%movie_url, 'title': u'%s' % TITLE}    
                    returnme.append(RETURN)
                    
                else:
                        
                    if extractor.lower() in TITLE.lower():    
                       RETURN={'url': u'%s'%movie_url, 'title': u'%s' % TITLE}    
                       returnme.append(RETURN)
                

        
        return returnme

        
