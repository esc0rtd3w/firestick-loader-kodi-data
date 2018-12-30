# -*- coding: utf-8 -*-


import re,urlparse
from liveresolver.modules import client,constants
import urllib,urllib2
import xbmcgui,xbmc,os,xbmcaddon
path=xbmcaddon.Addon().getAddonInfo("path")
captcha_img = os.path.join(path, 'captcha.jpg')
import requests



def resolve(url):
    try:    
        session=requests.Session()
        id = urlparse.parse_qs(urlparse.urlparse(url).query)['u'][0]
        referer = url
        session.headers.update({'referer': referer,
                                'User-agent' : client.agent()})

        result = session.get(url).text
        try:
            captcha = re.compile("<input type=\"hidden\" name=\"x\" value=\"(.+?)\">").findall(result)[0]
            url = re.compile("<input type=\"hidden\" name=\"url\" value=\"(.+?)\">").findall(result)[0]
            if 'http' not in url:
                url = 'http://www.lshstreams.com'+ url
            cap_url = 'http://www.blocked.com/captcha.php?x=' + captcha
            urllib.urlretrieve(cap_url,captcha_img)
            input = get_response(captcha_img)
            post_data = {'blockscript' : 'captcha',
                         'x' : captcha,
                         'url' : url,
                         'val' : input}
            session.headers.update({'Host':'www.lshstreams.com',
                                'Origin': 'http://www.lshstreams.com'})
            result = session.post(url, data=urllib.urlencode(post_data)).text
        except:
          pass
        streamer = result.replace('//file', '')
        streamer = re.compile("file *: *'(.+?)'").findall(streamer)[-1]

        url=streamer + ' swfUrl=http://www.lshstreams.com/jw/jwplayer.flash.swf flashver=' + constants.flash_ver() + ' live=1 token=SECURET0KEN#yw%.?()@W! timeout=14 swfVfy=1 pageUrl=http://cdn.lshstreams.com/embed.php?u=' + id

        return url.strip()
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
