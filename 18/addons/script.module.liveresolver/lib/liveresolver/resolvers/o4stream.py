# -*- coding: utf-8 -*-


import re,urlparse,urllib2
from liveresolver.modules import client
from liveresolver.modules import rowbalance,decryptionUtils,constants
from liveresolver.modules.log_utils import log
import urllib
import xbmcgui,xbmc,os,xbmcaddon
import requests

path=xbmcaddon.Addon().getAddonInfo("path")
captcha_img = os.path.join(path, 'captcha.jpg')


def resolve(url):

    try:
        session=requests.Session()
        try: referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
        except: referer = url
        id = urlparse.parse_qs(urlparse.urlparse(url).query)['stream'][0]
        url = 'http://www.04stream.com/weed.js?stream=%s&width=600&height=460&str=is&link=1&cat=1'%id
        
        session.headers.update({'referer': referer,
                                'User-agent' : client.agent()})

        result = session.get(url).text
        result = decryptionUtils.doDemystify(result)
        src = re.compile('.*?src=([^\'"><]+).*').findall(result)[0] + 'thefeed2all.eu'
        page = src
        ref2 = src
        result = session.get(src).text
        
        try:
            captcha = re.compile("<input type=\"hidden\" name=\"x\" value=\"(.+?)\">").findall(result)[0]
            url = re.compile("<input type=\"hidden\" name=\"url\" value=\"(.+?)\">").findall(result)[0]
            if 'http' not in url:
                url = 'http://www.04stream.com'+ url
            cap_url = 'http://www.blocked.com/captcha.php?x=' + captcha
            urllib.urlretrieve(cap_url,captcha_img)
            input = get_response(captcha_img)
            post_data = {'blockscript' : 'captcha',
                         'x' : captcha,
                         'url' : url,
                         'val' : input}
            session.headers.update({'Host':'www.04stream.com',
                                'Origin': 'http://www.04stream.com',
                                'Referer' : ref2})

            result = session.put(url, data=urllib.urlencode(post_data))
            result=result.text
        except:
            pass
        result = decryptionUtils.doDemystify(result)
        var = re.compile('var\s(.+?)\s*=\s*[\'\"](.+?)[\'\"]').findall(result)
        server_id = re.findall('.*?boxig=.*?&srp=(\d+)',result)[0]
        rtmp = rowbalance.get(server_id)
        var.append(('thist',rtmp))
        for i in range(100):
            for v in var: result = result.replace("+%s+" % v[0], '%s'%v[1])
            for v in var: result = result.replace("+%s" % v[0], '%s'%v[1])
            for v in var: result = result.replace("%s+" % v[0], '%s'%v[1])
            
        
        
        file = re.findall("&file=(rtmp://[^&]+)&",result)[0]#.replace('/stream//','').replace('/stream/','').replace('?.stream','.stream')
        file = file.replace('\'','').replace('"','')
        url = file + ' swfUrl=http://thecdn.04stream.com/p/ooolo1.swf flashver=' + constants.flash_ver() + ' timeout=15 live=1 pageUrl='+page
        return url
    except:
        return

def get_response(img):
    try:
        img = xbmcgui.ControlImage(450, 0, 400, 130, img)
        wdlg = xbmcgui.WindowDialog()
        wdlg.addControl(img)
        wdlg.show()
        xbmc.sleep(3000)
        kb = xbmc.Keyboard('', 'Type the letters in the image', False)
        kb.doModal()
        if (kb.isConfirmed()):
            solution = kb.getText()
            if solution == '':
                raise Exception('You must enter text in the image to access video')
            else:
                return solution
        else:
            raise Exception('Captcha Error')
    finally:
        wdlg.close()