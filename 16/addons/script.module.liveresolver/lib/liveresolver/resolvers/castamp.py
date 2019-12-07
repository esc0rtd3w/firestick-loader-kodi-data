# -*- coding: utf-8 -*-


import re,urllib,urlparse,base64
from liveresolver.modules import client,constants
from liveresolver.modules.log_utils import log
def resolve(url):
    try:
        id  = urlparse.parse_qs(urlparse.urlparse(url).query)['c'][0] 
        try:
            referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
        except:
            referer= url 
        url = 'http://castamp.com/embed.php?c=%s&vwidth=640&vheight=380'%id
        pageUrl=url

        
        result = client.request(url, referer=referer,headers = {'Host':'www.castamp.com'})
        result = urllib.unquote(result).replace('unescape(','').replace("'+'",'')
        rplcs = re.findall('=(.+?).replace\([\"\'](.+?)[\"\']\s*,\s*[\"\']([^\"\']*)[\"\']',result)
        result = re.sub('\/\*[^*]+\*\/','',result)
        var = re.compile('var\s(.+?)\s*=\s*[\'\"](.+?)[\'\"]').findall(result)
        var_dict = dict(var)
        file = re.compile('\'file\'\s*:\s*(.+?),').findall(result)[-1]
        file = var_dict[file]
        rtmp = re.compile('(rtmp://[^\"\']+)').findall(result)[0]
        for r in rplcs:
            file = file.replace(r[1],r[2])
        url = rtmp + ' playpath=' + file + ' swfUrl=http://p.castamp.com/cplayer.swf' + ' flashver=' + constants.flash_ver() + ' live=true timeout=15 swfVfy=1 pageUrl=' + pageUrl
        
        return url
    
    except:
        return

