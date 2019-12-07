# -*- coding: utf-8 -*-




import re,urlparse
from liveresolver.modules import client,constants
from liveresolver.modules.log_utils import log

def resolve(url):
    try:
        try: referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
        except: referer = url

        channel = urlparse.urlparse(url).path
        channel = re.compile('/([\w]+)').findall(channel)[-1]
        domain = urlparse.urlparse(url).netloc


        pageUrl = urlparse.urljoin('http://%s' % domain, channel)
        if 'instagib' in domain: playpath = 'instagib_%s' % channel
        elif 'breakers' in domain: playpath = 'btv_%s' % channel
        elif 'vapers' in domain: playpath = 'vtv_%s' % channel
        else: playpath = 'live_%s' % channel

        import requests
        s = requests.session()
        result = s.get(pageUrl).text
        swfUrl = re.compile('"(/\d+/swf/[0-9A-Za-z]+\.swf)').findall(result)[0]
        swfUrl = urlparse.urljoin(pageUrl, swfUrl)

        s.headers = {'User-agent':client.agent(),'X-Requested-With':constants.get_shockwave(),'Accept-Encoding':'gzip, deflate, lzma, sdch','Connection':'keep-alive','Host':'mvn.vaughnsoft.net','Referer':'http://vaughnlive.tv/' + channel}
        infoUrl = 'http://mvn.vaughnsoft.net/video/edge/mnv-%s' % (playpath)
        result = s.get(infoUrl).text
        streamer = re.compile('(.+?);').findall(result)[0]
        streamer = 'rtmp://%s/live' % streamer
        app = re.compile('mvnkey-(.+)').findall(result)[0].replace("0m0", "")
        app = 'live?%s' % app

        url = '%s app=%s playpath=%s pageUrl=http://vaughnlive.tv/ swfUrl=%s live=true flashver=%s timeout=15' % (streamer, app, playpath,swfUrl,constants.flash_ver())

        return url
    except:
        return

