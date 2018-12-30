# -*- coding: utf-8 -*-

'''
    Genesis Add-on
    Copyright (C) 2015 lambda

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
'''


import re,urllib,urlparse,json,time

from resources.lib.libraries import cache
from resources.lib.libraries import control
from resources.lib.libraries import client


def request(url, debrid=''):
    try:
        u = url

        if '</regex>' in url:
            import regex ; url = regex.resolve(url)
            if not url == None: u = url

        if url.startswith('rtmp'):
            if len(re.compile('\s*timeout=(\d*)').findall(url)) == 0: url += ' timeout=10'
            return url

        if url.startswith('$base64'):
            import base64 ; url = base64.b64decode(re.compile('\$base64\[(.+?)\]$').findall(url)[0])
            if not url == None: u = url

        if not debrid == '': return debridResolver(url, debrid)

        n = (urlparse.urlparse(url).netloc).lower() ; n = re.sub('www\d+\.|www\.|embed\.', '', n)

        try: url = re.compile('://(http.+)').findall(url)[0]
        except: pass

        r = [i['class'] for i in info() if n in i['netloc']]
        r += [i['class'] for i in info2() if n in i['netloc']]
        r = __import__(r[0], globals(), locals(), [], -1)
        r = r.resolve(url)

        return r
    except:
        return u



def rdDict():
    try:
        if '' in debridCredentials()['realdebrid'].values(): raise Exception()
        url = 'http://api.real-debrid.com/rest/1.0/hosts/domains'
        result = cache.get(client.request, 24, url)
        hosts = json.loads(result)
        hosts = [i.lower() for i in hosts]
        return hosts
    except:
        return []


def pzDict():
    try:
        if '' in debridCredentials()['premiumize'].values(): raise Exception()
        user, password = debridCredentials()['premiumize']['user'], debridCredentials()['premiumize']['pass']
        url = 'http://api.premiumize.me/pm-api/v1.php?method=hosterlist&params[login]=%s&params[pass]=%s' % (user, password)
        result = cache.get(client.request, 24, url)
        hosts = json.loads(result)['result']['hosterlist']
        hosts = [i.lower() for i in hosts]
        return hosts
    except:
        return []


def adDict():
    try:
        if '' in debridCredentials()['alldebrid'].values(): raise Exception()
        url = 'http://alldebrid.com/api.php?action=get_host'
        result = cache.get(client.request, 24, url)
        hosts = json.loads('[%s]' % result)
        hosts = [i.lower() for i in hosts]
        return hosts
    except:
        return []


def rpDict():
    try:
        if '' in debridCredentials()['rpnet'].values(): raise Exception()
        url = 'http://premium.rpnet.biz/hoster2.json'
        result = cache.get(client.request, 24, url)
        result = json.loads(result)
        hosts = result['supported']
        hosts = [i.lower() for i in hosts]
        return hosts
    except:
        return []


def rdAuthorize():
    try:
        CLIENT_ID = 'MUQMIQX6YWDSU'
        USER_AGENT = 'URLResolver for Kodi'

        headers = {'User-Agent': USER_AGENT}
        url = 'http://api.real-debrid.com/oauth/v2/device/code?client_id=%s&new_credentials=yes' % (CLIENT_ID)
        result = client.request(url, headers=headers)
        result = json.loads(result)
        verification_url = 'Go to URL: %s' % (result['verification_url'])
        user_code = 'When prompted enter: %s' % (result['user_code'])
        device_code = result['device_code']
        interval = result['interval']

        progressDialog = control.progressDialog
        progressDialog.create('RealDebrid', verification_url, user_code)

        for i in range(0, 3600):
            try:
                if progressDialog.iscanceled(): break
                time.sleep(1)
                if not float(i) % interval == 0: raise Exception()
                url = 'https://api.real-debrid.com/oauth/v2/device/credentials?client_id=%s&code=%s' % (CLIENT_ID, device_code)
                result = client.request(url, headers=headers, error=True)
                result = json.loads(result)
                if 'client_secret' in result: break
            except:
                pass

        try: progressDialog.close()
        except: pass

        id, secret = result['client_id'], result['client_secret'] 

        url = 'https://api.real-debrid.com/oauth/v2/token'
        post = urllib.urlencode({'client_id': id, 'client_secret': secret, 'code': device_code, 'grant_type': 'http://oauth.net/grant_type/device/1.0'})

        result = client.request(url, post=post, headers=headers)
        result = json.loads(result)

        token, refresh = result['access_token'], result['refresh_token']

        control.setSetting(id='realdebrid_id', value=id)
        control.setSetting(id='realdebrid_secret', value=secret)
        control.setSetting(id='realdebrid_token', value=token)
        control.setSetting(id='realdebrid_refresh', value=refresh)
    except:
        return


def debridCredentials():
    return {
        'realdebrid': {
        'id': control.setting('realdebrid_id'),
        'secret': control.setting('realdebrid_secret'),
        'token': control.setting('realdebrid_token'),
        'refresh': control.setting('realdebrid_refresh')
    },
        'premiumize': {
        'user': control.setting('premiumize_user'),
        'pass': control.setting('premiumize_password')
    },
        'alldebrid': {
        'user': control.setting('alldebrid_user'),
        'pass': control.setting('alldebrid_password')
    },
        'rpnet': {
        'user': control.setting('rpnet_user'),
        'pass': control.setting('rpnet_password')
    }}


def debridResolver(url, debrid):
    u = url.replace('filefactory.com/stream/', 'filefactory.com/file/')

    try:
        if not debrid == 'realdebrid' and not debrid == True: raise Exception()

        credentials = debridCredentials()['realdebrid']
        if '' in credentials.values(): raise Exception()
        id, secret, token, refresh = credentials['id'], credentials['secret'], credentials['token'], credentials['refresh']

        USER_AGENT = 'URLResolver for Kodi'

        post = urllib.urlencode({'link': url})
        headers = {'Authorization': 'Bearer %s' % token, 'User-Agent': USER_AGENT}
        url = 'http://api.real-debrid.com/rest/1.0/unrestrict/link'

        result = client.request(url, post=post, headers=headers, error=True)
        result = json.loads(result)

        if 'error' in result and result['error'] == 'bad_token':
            result = client.request('https://api.real-debrid.com/oauth/v2/token', post=urllib.urlencode({'client_id': id, 'client_secret': secret, 'code': refresh, 'grant_type': 'http://oauth.net/grant_type/device/1.0'}), headers={'User-Agent': USER_AGENT}, error=True)
            result = json.loads(result)
            if 'error' in result: return

            headers['Authorization'] = 'Bearer %s' % result['access_token']
            result = client.request(url, post=post, headers=headers)
            result = json.loads(result)

        url = result['download']
        return url
    except:
        pass

    try:
        if not debrid == 'premiumize' and not debrid == True: raise Exception()

        credentials = debridCredentials()['premiumize']
        if '' in credentials.values(): raise Exception()
        user, password = credentials['user'], credentials['pass']

        url = 'http://api.premiumize.me/pm-api/v1.php?method=directdownloadlink&params[login]=%s&params[pass]=%s&params[link]=%s' % (user, password, urllib.quote_plus(u))
        result = client.request(url, close=False)
        url = json.loads(result)['result']['location']
        return url
    except:
        pass

    try:
        if not debrid == 'alldebrid' and not debrid == True: raise Exception()

        credentials = debridCredentials()['alldebrid']
        if '' in credentials.values(): raise Exception()
        user, password = credentials['user'], credentials['pass']

        login_data = urllib.urlencode({'action': 'login', 'login_login': user, 'login_password': password})
        login_link = 'http://alldebrid.com/register/?%s' % login_data
        cookie = client.request(login_link, output='cookie', close=False)

        url = 'http://www.alldebrid.com/service.php?link=%s' % urllib.quote_plus(u)
        result = client.request(url, cookie=cookie, close=False)
        url = client.parseDOM(result, 'a', ret='href', attrs = {'class': 'link_dl'})[0]
        url = client.replaceHTMLCodes(url)
        url = '%s|Cookie=%s' % (url, urllib.quote_plus(cookie))
        return url
    except:
        pass

    try:
        if not debrid == 'rpnet' and not debrid == True: raise Exception()

        credentials = debridCredentials()['rpnet']
        if '' in credentials.values(): raise Exception()
        user, password = credentials['user'], credentials['pass']

        login_data = urllib.urlencode({'username': user, 'password': password, 'action': 'generate', 'links': u})
        login_link = 'http://premium.rpnet.biz/client_api.php?%s' % login_data
        result = client.request(login_link, close=False)
        result = json.loads(result)
        url = result['links'][0]['generated']
        return url
    except:
        return



def hostDict():
    d = [i['netloc'] for i in info()]
    try: d = [i.lower() for i in reduce(lambda x, y: x+y, d)]
    except: pass
    return [x for y,x in enumerate(d) if x not in d[:y]]


def hosthqDict():
    d = [i['netloc'] for i in info() if 'quality' in i and i['quality'] == 'High']
    try: d = [i.lower() for i in reduce(lambda x, y: x+y, d)]
    except: pass
    return [x for y,x in enumerate(d) if x not in d[:y]]


def hostmqDict():
    d = [i['netloc'] for i in info() if 'quality' in i and i['quality'] == 'Medium']
    try: d = [i.lower() for i in reduce(lambda x, y: x+y, d)]
    except: pass
    return [x for y,x in enumerate(d) if x not in d[:y]]


def hostlqDict():
    d = [i['netloc'] for i in info() if 'quality' in i and i['quality'] == 'Low']
    try: d = [i.lower() for i in reduce(lambda x, y: x+y, d)]
    except: pass
    return [x for y,x in enumerate(d) if x not in d[:y]]


def hostcapDict():
    d = [i['netloc'] for i in info() if 'captcha' in i and i['captcha'] == True]
    try: d = [i.lower() for i in reduce(lambda x, y: x+y, d)]
    except: pass
    return [x for y,x in enumerate(d) if x not in d[:y]]


def hostprDict():
    d = [i['netloc'] for i in info() if 'class' in i and i['class'] == '']
    try: d = [i.lower() for i in reduce(lambda x, y: x+y, d)]
    except: pass
    return [x for y,x in enumerate(d) if x not in d[:y]]



def info():
    return [{
        'class': '',
        'netloc': ['oboom.com', 'rapidgator.net', 'rg.to', 'uploaded.net', 'uploaded.to', 'ul.to', 'filefactory.com', 'nitroflare.com', 'turbobit.net'],
        'quality': 'High'
    }, {
        'class': '_180upload',
        'netloc': ['180upload.com'],
        'quality': 'High'
    }, {
        'class': 'allmyvideos',
        'netloc': ['allmyvideos.net'],
        'quality': 'Medium'
    }, {
        'class': 'allvid',
        'netloc': ['allvid.ch'],
        'quality': 'High'
    }, {
        'class': 'bestreams',
        'netloc': ['bestreams.net'],
        'quality': 'Low'
    }, {
        'class': 'castalba',
        'netloc': ['castalba.tv']
    }, {
        'class': 'clicknupload',
        'netloc': ['clicknupload.me', 'clicknupload.com'],
        'quality': 'High'
    }, {
        'class': 'cloudtime',
        'netloc': ['cloudtime.to'],
        'quality': 'Medium'
    }, {
        'class': 'cloudyvideos',
        'netloc': ['cloudyvideos.com'],
        'quality': 'High'
    }, {
        'class': 'cloudzilla',
        'netloc': ['cloudzilla.to'],
        'quality': 'Medium'
    }, {
        'class': 'daclips',
        'netloc': ['daclips.in'],
        'quality': 'Low'
    }, {
        'class': 'dailymotion',
        'netloc': ['dailymotion.com']
    }, {
        'class': 'datemule',
        'netloc': ['datemule.com']
    }, {
        'class': 'exashare',
        'netloc': ['exashare.com'],
        'quality': 'Low'
    }, {
        'class': 'filehoot',
        'netloc': ['filehoot.com'],
        'quality': 'Low'
    }, {
        'class': 'filenuke',
        'netloc': ['filenuke.com', 'sharesix.com'],
        'quality': 'Low'
    }, {
        'class': 'filmon',
        'netloc': ['filmon.com']
    }, {
        'class': 'finecast',
        'netloc': ['finecast.tv']
    }, {
        'class': 'filepup',
        'netloc': ['filepup.net']
    }, {
        'class': 'googledocs',
        'netloc': ['docs.google.com', 'drive.google.com']
    }, {
        'class': 'googlephotos',
        'netloc': ['photos.google.com']
    }, {
        'class': 'googlepicasa',
        'netloc': ['picasaweb.google.com']
    }, {
        'class': 'googleplus',
        'netloc': ['plus.google.com']
    }, {
        'class': 'gorillavid',
        'netloc': ['gorillavid.com', 'gorillavid.in'],
        'quality': 'Low'
    }, {
        'class': 'grifthost',
        'netloc': ['grifthost.com'],
        'quality': 'High'
    }, {
        'class': 'hdcast',
        'netloc': ['hdcast.me']
    }, {
        'class': 'hdcastorg',
        'netloc': ['hdcast.org']
    }, {
        'class': 'hugefiles',
        'netloc': ['hugefiles.net'],
        'quality': 'High',
        'captcha': True
    }, {
        'class': 'ipithos',
        'netloc': ['ipithos.to'],
        'quality': 'High'
    }, {
        'class': 'ishared',
        'netloc': ['ishared.eu'],
        'quality': 'High'
    }, {
        'class': 'letwatch',
        'netloc': ['letwatch.us'],
        'quality': 'Medium'
    }, {
        'class': 'mailru',
        'netloc': ['mail.ru', 'my.mail.ru', 'videoapi.my.mail.ru', 'api.video.mail.ru']
    }, {
        'class': 'mightyupload',
        'netloc': ['mightyupload.com'],
        'quality': 'High'
    }, {
        'class': 'miplayer',
        'netloc': ['miplayer.net'],
        'quality': 'High'
    }, {    
        'class': 'movdivx',
        'netloc': ['movdivx.com'],
        'quality': 'Low'
    }, {
        'class': 'movpod',
        'netloc': ['movpod.net', 'movpod.in'],
        'quality': 'Low'
    }, {
        'class': 'movshare',
        'netloc': ['movshare.net'],
        'quality': 'Low'
    }, {
        'class': 'mybeststream',
        'netloc': ['mybeststream.xyz']
    }, {
        'class': 'neodrive',
        'netloc': ['neodrive.co'],
        'quality': 'Medium'
    }, {
        'class': 'nosvideo',
        'netloc': ['nosvideo.com', 'noslocker.com'],
        'quality': 'High'
    }, {
        'class': 'novamov',
        'netloc': ['novamov.com'],
        'quality': 'Low'
    }, {
        'class': 'nowvideo',
        'netloc': ['nowvideo.eu', 'nowvideo.sx'],
        'quality': 'Low'
    }, {
        'class': 'odnoklassniki',
        'netloc': ['ok.ru', 'odnoklassniki.ru'],
        'quality': 'High'
    }, {
        'class': 'openload',
        'netloc': ['openload.io', 'openload.co'],
        'quality': 'High',
        'captcha': True
    }, {
        'class': 'p2pcast',
        'netloc': ['p2pcast.tv']
    }, {
        'class': 'primeshare',
        'netloc': ['primeshare.tv'],
        'quality': 'High'
    }, {
        'class': 'promptfile',
        'netloc': ['promptfile.com'],
        'quality': 'High'
    }, {
        'class': 'sawlive',
        'netloc': ['sawlive.tv']
    }, {
        'class': 'shadownet',
        'netloc': ['sdw-net.co']
    }, {        
        'class': 'shared2',
        'netloc': ['shared2.me'],
        'quality': 'High'
    }, {
        'class': 'sharerepo',
        'netloc': ['sharerepo.com'],
        'quality': 'Low'
    }, {
        'class': 'speedvideo',
        'netloc': ['speedvideo.net']
    }, {
        'class': 'stagevu',
        'netloc': ['stagevu.com'],
        'quality': 'Low'
    }, {
        'class': 'streamcloud',
        'netloc': ['streamcloud.eu'],
        'quality': 'Medium'
    }, {
        'class': 'streamin',
        'netloc': ['streamin.to'],
        'quality': 'Medium'
    }, {
        'class': 'streamlive',
        'netloc': ['streamlive.to'],
        'quality': 'Medium'
    }, {
        'class': 'streamup',
        'netloc': ['streamup.com']
    }, {
        'class': 'thevideo',
        'netloc': ['thevideo.me'],
        'quality': 'Low'
    }, {
        'class': 'tusfiles',
        'netloc': ['tusfiles.net'],
        'quality': 'High'
    }, {
        'class': 'up2stream',
        'netloc': ['up2stream.com'],
        'quality': 'Medium'
    }, {
        'class': 'uploadaf',
        'netloc': ['upload.af'],
        'quality': 'High'
    }, {
        'class': 'uploadc',
        'netloc': ['uploadc.com', 'uploadc.ch', 'zalaa.com'],
        'quality': 'High'
    }, {
        'class': 'uploadrocket',
        'netloc': ['uploadrocket.net'],
        'quality': 'High',
        'captcha': True
    }, {
        'class': 'uptobox',
        'netloc': ['uptobox.com'],
        'quality': 'High'
    }, {
        'class': 'v_vids',
        'netloc': ['v-vids.com'],
        'quality': 'High'
    }, {
        'class': 'vaughnlive',
        'netloc': ['vaughnlive.tv', 'breakers.tv', 'instagib.tv', 'vapers.tv']
    }, {
        'class': 'veehd',
        'netloc': ['veehd.com']
    }, {
        'class': 'veetle',
        'netloc': ['veetle.com']
    }, {
        'class': 'vidag',
        'netloc': ['vid.ag'],
        'quality': 'Medium'
    }, {
        'class': 'vidbull',
        'netloc': ['vidbull.com'],
        'quality': 'Low'
    }, {
        'class': 'vidce',
        'netloc': ['vidce.tv'],
        'quality': 'High'
    }, {
        'class': 'videomega',
        'netloc': ['videomega.tv'],
        'quality': 'High'
    }, {
        'class': 'videopremium',
        'netloc': ['videopremium.tv', 'videopremium.me']
    }, {
        'class': 'videoweed',
        'netloc': ['videoweed.es'],
        'quality': 'Low'
    }, {
        'class': 'videowood',
        'netloc': ['videowood.tv'],
        'quality': 'High'
    }, {
        'class': 'vidlockers',
        'netloc': ['vidlockers.ag'],
        'quality': 'High'
    }, {
        'class': 'vidspot',
        'netloc': ['vidspot.net'],
        'quality': 'Medium'
    }, {
        'class': 'vidto',
        'netloc': ['vidto.me'],
        'quality': 'Medium'
    }, {
        'class': 'vidzi',
        'netloc': ['vidzi.tv'],
        'quality': 'High'
    }, {
        'class': 'vimeo',
        'netloc': ['vimeo.com']
    }, {
        'class': 'vk',
        'netloc': ['vk.com']
    }, {
        'class': 'vodlocker',
        'netloc': ['vodlocker.com'],
        'quality': 'Low'
    }, {
        'class': 'xvidstage',
        'netloc': ['xvidstage.com'],
        'quality': 'Medium'
    }, {
        'class': 'yocast',
        'netloc': ['yocast.tv']
    }, {
        'class': 'youtube',
        'netloc': ['youtube.com'],
        'quality': 'Medium'
    }, {
        'class': 'zerocast',
        'netloc': ['zerocast.tv']
    }, {
        'class': 'zettahost',
        'netloc': ['zettahost.tv'],
        'quality': 'High'
    }, {
        'class': 'zstream',
        'netloc': ['zstream.to'],
        'quality': 'High'
    }]


def info2():
    return [{
        'class': 'watch1080',
        'netloc': ['watch1080p.com', 'sefilmdk.com']
    }]


