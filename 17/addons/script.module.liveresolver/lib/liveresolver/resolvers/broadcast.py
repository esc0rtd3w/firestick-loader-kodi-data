# -*- coding: utf-8 -*-


import re,urllib,urlparse,base64,json
from liveresolver.modules import client,constants,liveresolver_utils
from liveresolver.modules.log_utils import log
import requests
def resolve(url):
    try:
        s = requests.Session()
        try:
            referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
        except:
            referer= url 


        ref = liveresolver_utils.remove_referer(url)
        result = s.get(url, headers={'Referer':referer,'User-agent':client.agent()}).text
        curl = re.findall('.*url\s*=\s*["\']([^"\']+).*',result)[0]
        url = base64.b64decode(curl)
        token = json.loads(s.get('http://bro.adca.st/getToken.php').text)['token']
        url+= '2iJlpi2DMMr7q_DP8E9d9g'
        url+='|%s' % urllib.urlencode({'User-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36','Referer':ref,'X-Requested-With':constants.get_shockwave()})
        return url

    
    except:
        return

