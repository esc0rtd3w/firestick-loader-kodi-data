# -*- coding: utf-8 -*-


import re,urlparse,urllib,random
from resources.lib.libraries import client
from resources.lib.libraries import jsunpack


def resolve(url):
    try:
        try:
            referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
        except:
            referer=url

        id = urlparse.parse_qs(urlparse.urlparse(url).query)['u'][0]
        url = 'http://www.finecast.tv/embed4.php?u=%s&vw=640&vh=450'%id
        result = client.request(url, referer=referer, mobile = True)
        unpacked = ''
        packed = result.split('\n')
        for i in packed: 
            try: unpacked += jsunpack.unpack(i)
            except: pass
        result += unpacked
   
        var = re.compile('var\s(.+?)\s*=\s*(?:\'|\"|\s*)(.+?)(?:\'|\"|\s*);').findall(result)
        
        try:
            url = re.compile('file\s*:\s*(.+?)\n').findall(result)

            url = [i.split("'") for i in url]
            url = [[x.replace('+','').replace(',','') for x in i if not x == ''] for i in url]
            url = [[x.replace(x,[v[1] for v in var if v[0] == x][0]) if len([v[1] for v in var if v[0] == x]) > 0 else x for x in i] for i in url]
            url = [''.join(i) for i in url]
            
            url = [i for i in url if i.startswith('rtmp') or '.m3u8' in i]
            url = random.choice(url)
          
            dummy = ' swfUrl=http://www.finecast.tv/player6/jwplayer.flash.swf flashver=WIN\2020,0,0,228 live=1 timeout=14 swfVfy=1 pageUrl=http://www.finecast.tv/'
            if url.startswith('rtmp://'):
                url = 'rtmp://play.finecast.tv:1935/live/?'+url.split('?')[1]+ str(dummy)
            else:
                url = 'http://play.finecast.tv/live/'+url.split('live/')[1]+ str(dummy)
                pass
            return url
        
        except:
            pass
        ids = re.findall('id=(.+?)>(.+?)<',result)
        result = re.sub(r"'(.+?)'", r'\1', result)
        x = re.findall('\[(.+?)\].join\(""\)',result)
        auth, auth2 = re.findall('\[.+?\].join\(""\).+?\+\s*(.+?).join\(""\).+?document.getElementById\("(.+?)"\).innerHTML\);',result)[0]
        for v in var:
            if v[0] == auth:
                auth = re.findall('\[(.+?)\]',v[1])[0]
        for v in ids:
            if v[0] == auth2:
                auth2 = v[1]
        rtmp, file = x[0], x[1]
        rtmp = rtmp.replace('"','').replace(',','') + auth.replace('"','').replace(',','') + auth2.replace('"','').replace(',','')
        file = file.replace('"','').replace(',','')
        rtmp = rtmp 
        rtmp = rtmp.replace(r'\/','/')
        url = rtmp + '/' + file + ' swfUrl=http://www.finecast.tv/player6/jwplayer.flash.swf flashver=WIN\2020,0,0,228 live=1 timeout=14 swfVfy=1 pageUrl=http://www.finecast.tv/'

        
        return url
    except:
        return

