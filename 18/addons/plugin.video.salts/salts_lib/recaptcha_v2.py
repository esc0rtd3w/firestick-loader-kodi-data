# -*- coding: utf-8 -*-
"""
    SALTS XBMC Addon
    Copyright (C) 2016 tknorris
    Derived from Shani's LPro Code (https://github.com/Shani-08/ShaniXBMCWork2/blob/master/plugin.video.live.streamspro/unCaptcha.py)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    reusable captcha methods
"""
import re
import urllib
import urllib2
import os
import xbmcgui
import log_utils
import kodi
import dom_parser2
import scraper_utils

logger = log_utils.Logger.get_logger(__name__)
logger.disable()

class cInputWindow(xbmcgui.WindowDialog):
    def __init__(self, *args, **kwargs):  # @UnusedVariable
        media_path = os.path.join(kodi.get_path(), 'resources', 'skins', 'Default', 'media')
        bg_image = os.path.join(media_path, 'DialogBack2.png')
        check_image = os.path.join(media_path, 'checked.png')
        button_fo = os.path.join(media_path, 'button-fo.png')
        button_nofo = os.path.join(media_path, 'button-nofo.png')
        self.cancelled = False
        self.chk = [0] * 9
        self.chkbutton = [0] * 9
        self.chkstate = [False] * 9

        imgX, imgY, imgw, imgh = 436, 210, 408, 300
        ph, pw = imgh / 3, imgw / 3
        x_gap = 70
        y_gap = 70
        button_gap = 40
        button_h = 40
        button_y = imgY + imgh + button_gap
        middle = imgX + (imgw / 2)
        win_x = imgX - x_gap
        win_y = imgY - y_gap
        win_h = imgh + 2 * y_gap + button_h + button_gap
        win_w = imgw + 2 * x_gap

        ctrlBackgound = xbmcgui.ControlImage(win_x, win_y, win_w, win_h, bg_image)
        self.addControl(ctrlBackgound)
        self.msg = '[COLOR red]%s[/COLOR]' % (kwargs.get('msg'))
        self.strActionInfo = xbmcgui.ControlLabel(imgX, imgY - 30, imgw, 20, self.msg, 'font13')
        self.addControl(self.strActionInfo)
        img = xbmcgui.ControlImage(imgX, imgY, imgw, imgh, kwargs.get('captcha'))
        self.addControl(img)
        self.iteration = kwargs.get('iteration')
        name = kwargs.get('name')
        name = 'for: [I]%s[/I]' % (name) if name is not None else ''
        self.strActionInfo = xbmcgui.ControlLabel(imgX, imgY + imgh, imgw, 20, 'Captcha Round: %s %s' % (self.iteration, name), 'font40')
        self.addControl(self.strActionInfo)
        self.cancelbutton = xbmcgui.ControlButton(middle - 110, button_y, 100, button_h, 'Cancel', focusTexture=button_fo, noFocusTexture=button_nofo, alignment=2)
        self.okbutton = xbmcgui.ControlButton(middle + 10, button_y, 100, button_h, 'OK', focusTexture=button_fo, noFocusTexture=button_nofo, alignment=2)
        self.addControl(self.okbutton)
        self.addControl(self.cancelbutton)

        for i in xrange(9):
            row = i / 3
            col = i % 3
            x_pos = imgX + (pw * col)
            y_pos = imgY + (ph * row)
            self.chk[i] = xbmcgui.ControlImage(x_pos, y_pos, pw, ph, check_image)
            self.addControl(self.chk[i])
            self.chk[i].setVisible(False)
            self.chkbutton[i] = xbmcgui.ControlButton(x_pos, y_pos, pw, ph, str(i + 1), font='font1', focusTexture=button_fo, noFocusTexture=button_nofo)
            self.addControl(self.chkbutton[i])

        for i in xrange(9):
            row_start = (i / 3) * 3
            right = row_start + (i + 1) % 3
            left = row_start + (i - 1) % 3
            up = (i - 3) % 9
            down = (i + 3) % 9
            self.chkbutton[i].controlRight(self.chkbutton[right])
            self.chkbutton[i].controlLeft(self.chkbutton[left])
            if i <= 2:
                self.chkbutton[i].controlUp(self.okbutton)
            else:
                self.chkbutton[i].controlUp(self.chkbutton[up])

            if i >= 6:
                self.chkbutton[i].controlDown(self.okbutton)
            else:
                self.chkbutton[i].controlDown(self.chkbutton[down])

        self.okbutton.controlLeft(self.cancelbutton)
        self.okbutton.controlRight(self.cancelbutton)
        self.cancelbutton.controlLeft(self.okbutton)
        self.cancelbutton.controlRight(self.okbutton)
        self.okbutton.controlDown(self.chkbutton[2])
        self.okbutton.controlUp(self.chkbutton[8])
        self.cancelbutton.controlDown(self.chkbutton[0])
        self.cancelbutton.controlUp(self.chkbutton[6])
        self.setFocus(self.okbutton)

    def get(self):
        self.doModal()
        self.close()
        if not self.cancelled:
            return [i for i in xrange(9) if self.chkstate[i]]

    def onControl(self, control):
        # logger.log('control: %s' % (control), log_utils.LOGDEBUG)
        if control == self.okbutton and any(self.chkstate):
            self.close()

        elif control == self.cancelbutton:
            self.cancelled = True
            self.close()
        else:
            label = control.getLabel()
            if label.isdigit():
                index = int(label) - 1
                self.chkstate[index] = not self.chkstate[index]
                self.chk[index].setVisible(self.chkstate[index])

    def onAction(self, action):
        # logger.log('action: %s' % (action), log_utils.LOGDEBUG)
        if action == 10:
            self.cancelled = True
            self.close()

class UnCaptchaReCaptcha:
    def processCaptcha(self, key, lang, name=None, referer=None):
        if referer is None: referer = 'https://www.google.com/recaptcha/api2/demo'
        headers = {'Referer': referer, 'Accept-Language': lang}
        html = get_url('http://www.google.com/recaptcha/api/fallback?k=%s' % (key), headers=headers)
        token = ''
        iteration = 0
        while True:
            payload = dom_parser2.parse_dom(html, 'img', {'class': 'fbc-imageselect-payload'}, req='src')
            iteration += 1
            message = dom_parser2.parse_dom(html, 'label', {'class': 'fbc-imageselect-message-text'})
            if not message:
                message = dom_parser2.parse_dom(html, 'div', {'class': 'fbc-imageselect-message-error'})
                
            if message and payload:
                message = message[0].content
                payload = payload[0].attrs['src']
            else:
                token = dom_parser2.parse_dom(html, 'div', {'class': 'fbc-verification-token'})
                if token:
                    token = dom_parser2.parse_dom(token[0].content, 'textarea')[0].content
                    logger.log('Captcha Success: %s' % (token), log_utils.LOGDEBUG)
                else:
                    logger.log('Captcha Failed', log_utils.LOGDEBUG)
                break

            cval = dom_parser2.parse_dom(html, 'input', {'name': 'c'}, req='value')
            if not cval: break
            
            cval = cval[0].attrs['value']
            captcha_imgurl = scraper_utils.urljoin('https://www.google.com', scraper_utils.cleanse_title(payload))
            message = message.replace('<strong>', '[B]').replace('</strong>', '[/B]')
            message = re.sub(re.compile('</?(div|strong)[^>]*>', re.I), '', message)
            if any(c for c in ['<', '>'] if c in message):
                logger.log('Suspicious Captcha Prompt: %s' % (message), log_utils.LOGWARNING)
                
            oSolver = cInputWindow(captcha=captcha_imgurl, msg=message, iteration=iteration, name=name)
            captcha_response = oSolver.get()
            if not captcha_response:
                break

            data = {'c': cval, 'response': captcha_response}
            html = get_url("http://www.google.com/recaptcha/api/fallback?k=%s" % (key), data=data, headers=headers)
        return token

def get_url(url, data=None, timeout=20, headers=None):
    if headers is None: headers = {}
    if data is None: data = {}
    post_data = urllib.urlencode(data, doseq=True)
    if 'User-Agent' not in headers:
        headers['User-Agent'] = scraper_utils.get_ua()
    logger.log('URL: |%s| Data: |%s| Headers: |%s|' % (url, post_data, headers), log_utils.LOGDEBUG)

    try:
        req = urllib2.Request(url)
        for key in headers:
            req.add_header(key, headers[key])
    
        response = urllib2.urlopen(req, data=post_data, timeout=timeout)
        result = response.read()
        response.close()
    except urllib2.HTTPError as e:
        logger.log('ReCaptcha.V2 HTTP Error: %s on url: %s' % (e.code, url), log_utils.LOGWARNING)
        result = ''
    except urllib2.URLError as e:
        logger.log('ReCaptcha.V2 URLError Error: %s on url: %s' % (e, url), log_utils.LOGWARNING)
        result = ''

    return result
