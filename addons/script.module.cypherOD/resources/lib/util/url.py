# -*- coding: utf-8 -*-

"""
    urls.py ---
    Copyright (C) 2017, Jen

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
import os
import urllib
import sys
import urllib2
import urlparse
import random

import xbmc
import xbmcaddon
import xbmcvfs
import koding
import requests
from resources.lib.plugin import run_hook
from language import get_string as _

def __replace_gif(url):
    """ put gifs in local cache
    try to put gif in cache to enable motion
    Keyword Arguments:
    url -- url pointing to gif
    """
    if not url.endswith(".gif"):
        return url
    else:
        base_folder = xbmcaddon.Addon().getSetting("cache_folder")
        dest_folder = os.path.join(xbmc.translatePath(base_folder), "artcache")
        xbmcvfs.mkdirs(dest_folder)
        parts = url.split("/")
        dest = xbmc.makeLegalFilename(
            # TODO make sure this is unique
            os.path.join(dest_folder, parts[-2] + parts[-1]))
        if not xbmcvfs.exists(dest):
            try:
                response = requests.get(url, timeout=10, verify=False)
            except:
                return None
            if response.status_code == 200:
                with open(dest, 'wb') as out_file:
                    data = response.content
                    response.close()
                    out_file.write(data)
                    # shutil.copyfileobj(response.raw, out_file)
                    del data
                    del response
                if os.path.getsize(dest) == 0:
                    koding.dolog("0 size gif: " + repr(dest))
                    os.remove(dest)
                    return None
                else:
                    koding.dolog("size: " + repr(os.path.getsize(dest)))
            else:
                koding.Text_Box(xbmcaddon.Addon().getAddonInfo('name'),
                                _("gif not found: ") + url)
                return None
        xbmc.log("gif done: " + repr(dest))
        return dest


def replace_url(url, replace_gif=True):
    """ replace url with correct one
    replace url to point to correct jen server
    Keyword Arguments:
    url         -- url to replace
    replace_gif -- whether to place gifs into cache to enable motion
                   (default True)
    """
    result = run_hook("replace_url", url)
    if result:
        url = result
    enable_gifs = xbmcaddon.Addon().getSetting('enable_gifs') == "true"
    if enable_gifs and replace_gif:
        return __replace_gif(url)
    return url


def get_addon_url(mode, url=""):
    if type(url) == dict:
        url = repr(url)
    result = sys.argv[0] + "?mode=%s" % mode
    if url:
        result += "&url=%s" % urllib.quote_plus(url)
    return result


def proxy_get(url, check, headers=None, data=None):
    if headers is None:
        headers = {
            'User-Agent': randomagent(),
        }
        try:
            request = urllib2.Request(url, headers=headers, data=data)
            html = urllib2.urlopen(request, timeout=10).read()
            if check in str(html):
                return html
        except:
            pass

    try:
        new_url = get_proxy_url() % urllib.quote_plus(url)
        headers['Referer'] = 'http://%s/' % urlparse.urlparse(new_url).netloc
        request = urllib2.Request(new_url, headers=headers)
        response = urllib2.urlopen(request, timeout=10)
        html = response.read()
        response.close()
        if check in html:
            return html
    except:
        pass

    try:
        new_url = get_proxy_url() % urllib.quote_plus(url)
        headers['Referer'] = 'http://%s/' % urlparse.urlparse(new_url).netloc
        request = urllib2.Request(new_url, headers=headers)
        html = urllib2.urlopen(request, timeout=10).read()
        if check in html:
            return html
    except:
        pass

    return


def proxy_get_raw(url, headers=None, data=None):
    if headers is None:
        headers = {
            'User-Agent': randomagent(),
        }

    try:
        new_url = get_proxy_url() % urllib.quote_plus(url)
        headers['Referer'] = 'http://%s/' % urlparse.urlparse(new_url).netloc
        request = urllib2.Request(new_url, headers=headers)
        response = urllib2.urlopen(request, timeout=10)
        return response
    except:
        pass


def get_proxy_url():
    return random.choice([
        'http://alter-ip.com/index.php?hl=3c0&q=%s',
        'http://buka.link/browse.php?b=20&u=%s&b=0&f=norefer',
        'http://dontfilter.us/browse.php?b=20&u=%s',
        'http://free-proxyserver.com/browse.php?b=20&u=%s',
        'http://www.freeopenproxy.com/browse.php?b=20&u=%s',
        'http://www.justproxy.co.uk/index.php?hl=2e5&q=%s',
        'http://protectproxy.com/browse.php?b=20&u=%s',
        'http://proxite.net/browse.php?b=20&u=%s',
        'http://www.proxythis.info/index.php?hl=2e5&q=%s',
        'http://quickprox.com/browse.php?b=20&u=%s',
        'http://unblock-proxy.com/browse.php?b=20&u=%s&b=0&f=norefer',
        'http://www.unblockmyweb.com/browse.php?b=20&u=%s',
        'http://unblocksite.org/view.php?b=20&u=%s',
        'http://unblockthatsite.net/ahora.php?b=20&u=',
    ])


def randomagent():
    BR_VERS = [
        ['%s.0' % i for i in xrange(18, 43)],
        ['37.0.2062.103', '37.0.2062.120', '37.0.2062.124', '38.0.2125.101',
         '38.0.2125.104', '38.0.2125.111', '39.0.2171.71', '39.0.2171.95',
         '39.0.2171.99', '40.0.2214.93', '40.0.2214.111', '40.0.2214.115',
         '42.0.2311.90', '42.0.2311.135', '42.0.2311.152', '43.0.2357.81',
         '43.0.2357.124', '44.0.2403.155', '44.0.2403.157', '45.0.2454.101',
         '45.0.2454.85', '46.0.2490.71',
         '46.0.2490.80', '46.0.2490.86', '47.0.2526.73', '47.0.2526.80'],
        ['11.0']]
    WIN_VERS = ['Windows NT 10.0', 'Windows NT 7.0', 'Windows NT 6.3',
                'Windows NT 6.2', 'Windows NT 6.1', 'Windows NT 6.0',
                'Windows NT 5.1', 'Windows NT 5.0']
    FEATURES = ['; WOW64', '; Win64; IA64', '; Win64; x64', '']
    RAND_UAS = ['Mozilla/5.0 ({win_ver}{feature}; rv:{br_ver}) Gecko/20100101 Firefox/{br_ver}',
                'Mozilla/5.0 ({win_ver}{feature}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{br_ver} Safari/537.36',
                'Mozilla/5.0 ({win_ver}{feature}; Trident/7.0; rv:{br_ver}) like Gecko']
    index = random.randrange(len(RAND_UAS))
    return RAND_UAS[index].format(win_ver=random.choice(WIN_VERS),
                                  feature=random.choice(FEATURES),
                                  br_ver=random.choice(BR_VERS[index]))
