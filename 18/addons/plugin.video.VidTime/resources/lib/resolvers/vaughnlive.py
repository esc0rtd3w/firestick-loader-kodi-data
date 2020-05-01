import re,xbmc
import urlparse
from resources.lib.modules import client
from resources.lib.modules import jsunpack

pUrl='https://dl.dropboxusercontent.com/s/gsi57fqqkosg073/247%20shows.xml'
result = client.request(pUrl, referer=pUrl)

variable=re.findall('<vaughnlive>([^>]+)</vaughnlive>',result)[0]


def resolve(url):
        channel = urlparse.urlparse(url).path
        channel = re.compile('/([\w]+)').findall(channel)[-1]
        domain = urlparse.urlparse(url).netloc


        pageUrl = urlparse.urljoin('http://%s' % domain, channel)       

        result = client.request(pageUrl, referer=pageUrl)
        swfUrl = re.compile('"(/\d+/swf/[0-9A-Za-z]+\.swf)').findall(result)[0]
        file1=re.findall('\.k1 = "([^"]+)";',result)[0]
        file2=re.findall('\.k2 = "([^"]+)";',result)[0]
        swfUrl = urlparse.urljoin(pageUrl, swfUrl)

        infoUrl = 'http://mvn.vaughnsoft.net/video/edge/'+variable+'-%s_%s' % (file1,file2)
        result = client.request(infoUrl)
        streamer = re.compile('(.+?);').findall(result)[0]
        streamer = 'rtmp://%s/live' % streamer

        app = re.compile('mvnkey-(.+?);NA').findall(result)[0]
        app = 'live?%s' % app

        url = '%s app=%s  playpath=%s_%s swfUrl=%s pageUrl=%s swfVfy=true live=true timeout=20' % (streamer,app, file1, file2, swfUrl, pageUrl)

        return url
