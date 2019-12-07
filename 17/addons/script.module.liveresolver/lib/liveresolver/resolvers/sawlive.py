# -*- coding: utf-8 -*-
import re,urllib,urlparse,base64
from liveresolver.modules import client,decryptionUtils
from liveresolver.modules import jsunpack
from liveresolver.modules.log_utils import log




def resolve(url):
    try:

        page = re.compile('//(.+?)/(?:embed|v)/([0-9a-zA-Z-_]+)').findall(url)[0]
        
        try: referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
        except: referer = page
        try: host = urlparse.parse_qs(urlparse.urlparse(url).query)['host'][0]
        except: host = 'www.sawlive.tv'
        page = 'http://sawlive.tv/embed/%s' % (page[1])
        headers={'User-Agent': client.agent(),'Host': host, 'Referer': referer, 'Connection': 'keep-alive'}
        result = client.request(page, referer=referer, headers = headers)
        
        unpacked = ''
        
        packed = result.split('\n')
        for i in packed:
            try:
                unpacked += jsunpack.unpack(i)
            except:
                pass
        result += unpacked
        result = urllib.unquote_plus(result)
        r2 = result
        resul = None
        try:
            url = client.parseDOM(result, 'iframe', ret='src')[-1]
        except:
            result = unpacked
            try:
                url = client.parseDOM(result, 'iframe', ret='src')[-1]
                var = re.compile('var\s(.+?)\s*=\s*[\'\"](.+?)[\'\"]').findall(result)
                var_dict = dict(var)       
                
                for v in var_dict.keys():
                    url = url.replace(v,var_dict[v])
                url = url.replace('\'','').replace('\"','').replace('+','').replace(' ','')
                resul = client.request(url, headers = headers)
            except:
                pass
        
        if resul is None:
            #aaa = r2.replace('var ','').replace('\' ','\' +').replace(' \'','+ \'')

            aaa = r2.replace('document.write(',' var result =').replace('\');','\'')
            aaa = aaa.replace('"\' +swidth+ \'"','')
            aaa = aaa.replace('"\' +sheight+ \'"','')
            aaa = re.sub('([^+\s])\s([^+\s])',r'\1+\2',aaa)
            aaa = aaa.replace('function+','function ')
            aaa = aaa.replace('var+','var ')
            aaa = aaa.replace('result+','result ')
            import js2py
            context = js2py.EvalJs()
            context.swidth = '400'
            context.sheight = '400'
            context.execute(aaa)
            result = context.result
            result = urllib.unquote_plus(result)
            url = client.parseDOM(result, 'iframe', ret='src')[-1]
            result = client.request(url, headers = headers)
        else:
            result = resul
        unpacked = ''
        packed = result.split('\n')
        for i in packed:
            try:
                unpacked += jsunpack.unpack(i)
            except:
                pass
        result += unpacked
        result = urllib.unquote_plus(result)
        var = re.compile('var\s(.+?)\s*=\s*[\'\"](.+?)[\'\"]').findall(result)
        rplcs = re.findall(';.+?=(.+?).replace\([\"\'](.+?)[\"\']\s*,\s*[\"\']([^\"\']*)[\"\']',result)
        var_dict = dict(var)       
        file = re.compile("'file'\s*(.+?)\)").findall(result)[0]
        file = file.replace('\'','')
            
        for v in var_dict.keys():
            file = file.replace(v,var_dict[v])
        file = file.replace('+','').replace(',','').strip().replace(' ', '')
        log("Sawlive: Found file url: " + file)
        if 'f4m' in file:
            return file
        try:
            log("Sawlive: Finding m3u8 link.")
            if not file.startswith('http'): raise Exception()
            url = client.request(file, output='geturl')
            if not '.m3u8' in url: raise Exception()
            url += '|%s' % urllib.urlencode({'User-Agent': client.agent(), 'Referer': file})
            log("Sawlive: Found m3u8 link: " + url)
            return url
        except:
            log("Sawlive: m3u8 link not found, finding rtmp.")
            pass
        strm = re.compile("'streamer'\s*(.+?)\)").findall(result)[0]
        strm = strm.replace('\'','')
        for v in var_dict.keys():
            strm = strm.replace(v,var_dict[v])
        strm = strm.replace('+','').replace(',','').strip().replace(' ', '')
        swf = re.compile("SWFObject\('(.+?)'").findall(result)[0].replace(' ', '')

        url = '%s playpath=%s swfUrl=%s pageUrl=%s live=1 timeout=60' % (strm, file, swf, url)
        url = urllib.unquote(url).replace('unescape(','')

        for r in rplcs:
            url = url.replace(r[1],r[2])
        log("Sawlive: rtmp link found: " + url)
        return url
    except Exception as e:
        log("Sawlive exception:\n" + str(e))
        log("Sawlive: Resolver failed. Returning...")
        return


