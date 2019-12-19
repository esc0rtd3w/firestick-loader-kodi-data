# -*- coding: utf-8 -*-


import re,urllib,urlparse,base64
from liveresolver.modules import client,constants,decryptionUtils
from liveresolver.modules.log_utils import log

def resolve(url):
    try:
        try:
            cid  = urlparse.parse_qs(urlparse.urlparse(url).query)['cid'][0] 
        except:
            cid = re.compile('channel/(.+?)(?:/|$)').findall(url)[0]

        
        try:
            referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
        except:
            referer='http://castalba.tv'
        
        url = 'http://castalba.tv/embed.php?cid=%s&wh=600&ht=380&r=%s'%(cid,urlparse.urlparse(referer).netloc)
        pageUrl=url

        result = client.request(url, referer=referer,mobile=True)
        result = decryptionUtils.doDemystify(result)
        result=urllib.unquote(result)
        var = re.compile('var\s(.+?)\s*=\s*[\'\"](.+?)[\'\"]').findall(result)
        var_dict = dict(var)

        if 'm3u8' in result:
            url = re.compile('(?:var\s*)?file.+?\s*=\s*(?:unescape\()[\'\"](.+?)[\'\"]').findall(result)[-1]
            url = 'http://' + url + '.m3u8'
            url += '|%s' % urllib.urlencode({'User-Agent': client.agent(), 'Referer': url,'X-Requested-With':constants.get_shockwave()})
            log("Castalba: Found m3u8 url: " + url)
            
        else:
            try:
                filePath = re.compile("'file'\s*:\s*(?:unescape\()?'(.+?)'").findall(result)[0]
                
            except:
                file = re.findall('(?:var\s*)?file\s*=\s*(?:unescape\()?(?:\'|\")(.+?)(?:\'|\")',result)[-1]
                try:
                    file2 = re.findall("'file':\s*unescape\(file\)\s*\+\s*unescape\('(.+?)'\)",result)[0]
                    filePath = file+file2
                except:
                    filePath = file
            swf = re.compile("'flashplayer'\s*:\s*\"(.+?)\"").findall(result)[0]
            
            sm = re.findall("'streamer':(.+?),",result)[0]
            strm_funcs = re.findall('function\s*(.+?)\s*\{([^\}]+)',result,flags=re.DOTALL)
            for f in strm_funcs:
                if f[0] in ['(p,a,c,k,e,r)','()']:
                    continue
                if '%s'%f[0] in sm:
                    strm_func = f[1]
                    break
            strm_func = re.sub('\s//[^;]+','',strm_func)
            streamer = 'rtmp://' +  re.findall('.*["\'/](\d{1,3}\.\d{1,3}\.\d{1,3}\.[^"\'/]+)["\'/]',strm_func)[0] + '/live'
            streamer = streamer.replace('///','//')
            url = streamer  + ' playpath=' + filePath +' swfUrl=' + swf + ' flashver=' + constants.flash_ver() +' live=true timeout=15 swfVfy=true pageUrl=' + pageUrl
            log("Castalba: Found rtmp link: " + url)

        return url
    
    except:
        log("Castalba: Resolver failed. Returning...")
        return

