from liveresolver.modules import client,constants
import re,sys,urllib,urlparse,base64,urllib2,cookielib
from liveresolver.modules.log_utils import log



def resolve(url):
    try:
        
        result = client.request(url)
        uri = re.findall("decodeURIComponent\(atob\('(.+?)'",result)[0]
        while not ('http') in uri:
            uri = base64.b64decode(uri)
            if not ('http') in uri:
                uri = re.findall("'(.+?)'",uri)[0]
            else:
                pass
        murl = re.findall('"src":"(.+?)"',uri)[0]  
    
        result = client.request(murl,referer = url)
        base = urlparse.urlparse(murl).netloc
        items = client.parseDOM(result, 'video', attrs={'id': 'player'})
        url = client.parseDOM(items, 'source', ret='src')[0]
        if ('http') in url: return url+test
        if url[0]!='/':
            url='http://%s/'%base+url
        else:
            url='http://%s'%base+url   
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36 OPR/38.0.2220.25 (Edition beta)' ,'Referer':murl,'X-Requested-With':constants.get_shockwave(),'Host':base, 'Connection':'keep-alive','Accept-encoding':'gzip, deflate, lzma, sdch'}
        r2 = client.request(url,headers=headers)
        u2 = re.findall('(http://[^\s]+)',r2)[0]
        return u2 + '|%s' % urllib.urlencode({'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36 OPR/38.0.2220.25 (Edition beta)' ,'Referer':url,'X-Requested-With':constants.get_shockwave()})
    except:
        return
