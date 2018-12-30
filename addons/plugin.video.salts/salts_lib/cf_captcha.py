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
"""
import re
import urllib2
import urllib
import urlparse
import log_utils
from salts_lib import recaptcha_v2
from salts_lib.constants import USER_AGENT

logger = log_utils.Logger.get_logger(__name__)
logger.disable()

class NoRedirection(urllib2.HTTPErrorProcessor):
    def http_response(self, request, response):  # @UnusedVariable
        logger.log('Stopping Redirect', log_utils.LOGDEBUG)
        return response

    https_response = http_response

def solve(url, cj, user_agent=None, name=None):
    if user_agent is None: user_agent = USER_AGENT
    headers = {'User-Agent': user_agent, 'Referer': url}
    request = urllib2.Request(url)
    for key in headers: request.add_header(key, headers[key])
    try:
        response = urllib2.urlopen(request)
        html = response.read()
    except urllib2.HTTPError as e:
        html = e.read()

    match = re.search('data-sitekey="([^"]+)', html)
    match1 = re.search('data-ray="([^"]+)', html)
    if match and match1:
        token = recaptcha_v2.UnCaptchaReCaptcha().processCaptcha(match.group(1), lang='en', name=name, referer=url)
        if token:
            data = {'g-recaptcha-response': token, 'id': match1.group(1)}
            scheme = urlparse.urlparse(url).scheme
            domain = urlparse.urlparse(url).hostname
            url = '%s://%s/cdn-cgi/l/chk_captcha?%s' % (scheme, domain, urllib.urlencode(data))
            if cj is not None:
                try: cj.load(ignore_discard=True)
                except: pass
                opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
                urllib2.install_opener(opener)

            try:
                request = urllib2.Request(url)
                for key in headers: request.add_header(key, headers[key])
                opener = urllib2.build_opener(NoRedirection)
                urllib2.install_opener(opener)
                response = urllib2.urlopen(request)
                while response.getcode() in [301, 302, 303, 307]:
                    if cj is not None:
                        cj.extract_cookies(response, request)
                    redir_url = response.info().getheader('location')
                    if not redir_url.startswith('http'):
                        redir_url = urlparse.urljoin(url, redir_url)
                    request = urllib2.Request(redir_url)
                    for key in headers: request.add_header(key, headers[key])
                    if cj is not None:
                        cj.add_cookie_header(request)
                        
                    response = urllib2.urlopen(request)

                final = response.read()
                if cj is not None:
                    cj.extract_cookies(response, request)
                    cj.save(ignore_discard=True)
                    
                return final
            except urllib2.HTTPError as e:
                logger.log('CF Captcha Error: %s on url: %s' % (e.code, url), log_utils.LOGWARNING)
                return False
    else:
        logger.log('CF Captcha without sitekey/data-ray: %s' % (url), log_utils.LOGWARNING)
