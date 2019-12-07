import urllib
import urllib2
import re
import os
import json
import cookielib
import xbmcplugin
import xbmcgui
import xbmcvfs
import xbmcaddon
import StorageServer
from traceback import format_exc
from urlparse import urlparse, parse_qs
from BeautifulSoup import BeautifulSoup

addon = xbmcaddon.Addon(id='plugin.audio.iheart')
addon_path = xbmc.translatePath(addon.getAddonInfo('path'))
addon_profile = xbmc.translatePath(addon.getAddonInfo('profile'))
cookie_file = os.path.join(addon_profile, 'cookie_file')
cookie_jar = cookielib.LWPCookieJar(cookie_file)
icon = os.path.join(addon_path, 'icon.png')
fanart = os.path.join(addon_path, 'fanart.jpg')
base_url = 'http://www.iheart.com'
debug = addon.getSetting('debug')
addon_version = addon.getAddonInfo('version')
cache = StorageServer.StorageServer("iheart", 24)
profile = xbmc.translatePath(addon.getAddonInfo('profile'))
favorites_file = os.path.join(profile, 'favorites')


def addon_log(string):
    if debug == 'true':
        xbmc.log("[addon.iheart-%s]: %s" %(addon_version, string))


def make_request(url, data=None, headers=None):
    addon_log('Request URL: %s' %url)
    if headers is None:
        headers = {'User-agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0',
                   'Referer' : base_url}
    if not xbmcvfs.exists(cookie_file):
        addon_log('Creating cookie_file!')
        cookie_jar.save()
    cookie_jar.load(cookie_file, ignore_discard=True, ignore_expires=True)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie_jar))
    urllib2.install_opener(opener)
    try:
        req = urllib2.Request(url, data, headers)
        response = urllib2.urlopen(req)
        cookie_jar.save(cookie_file, ignore_discard=True, ignore_expires=False)
        data = response.read()
        addon_log(str(response.info()))
        redirect_url = response.geturl()
        response.close()
        if redirect_url != url:
                addon_log('Redirect URL: %s' %redirect_url)
        return data
    except urllib2.URLError, e:
        addon_log('We failed to open "%s".' %url)
        if hasattr(e, 'reason'):
            addon_log('We failed to reach a server.')
            addon_log('Reason: ', e.reason)
        if hasattr(e, 'code'):
            addon_log('We failed with error code - %s.' %e.code)


def login():
    url = 'http://www.iheart.com/a/account/login/?_country=US&_rel=507'
    post_data = {'email': addon.getSetting('email'), 'password': addon.getSetting('password')}
    data = make_request(url, urllib.urlencode(post_data))
    if eval(data)['ok'] == 1:
        addon_log('Successfully Logged In')
    else:
        xbmc.executebuiltin("XBMC.Notification(iHeartRadio,%s,5000,%s)" %('Login Failed', icon))


def scrape_categories():
    soup = BeautifulSoup(make_request(base_url+'/find'), convertEntities=BeautifulSoup.HTML_ENTITIES)
    script = None
    local_url = ''
    local_name = ''
    country = ''
    rel = ''
    for i in soup.findAll('script'):
        try:
            if 'BOOT' in i.string:
                script = i.string.replace('\n', '')
                break
        except: continue

    if script:
        try:
            country = re.findall("country: '(.+?)',", script)[0].encode('utf-8')
            rel = re.findall("rel: (.+?),", script)[0]
            c_ip = re.findall("clientIp: '(.+?)',", script)[0]
            near_by_url = ('http://www.iheart.com/a/misc/detect_market/%s/?_country=%s&_rel=%s'
                           %(c_ip, country, rel))
            data = json.loads(make_request(near_by_url))
            local_url = data['url']
            local_name = data['name'].encode('utf-8')
        except:
            addon_log('exception local data: %s' %format_exc())

    items = [soup.find('ul', attrs={'class': 'js-talk'})('a'),
             soup.find('ul', attrs={'class': 'js-genres'})('a'),
             soup('select', attrs={'name': 'state'})[0]('option'),
             soup('select', attrs={'name': 'market'})[0]('option')]
    categories = {'local': (local_name, local_url, country, rel),
                  'talk': [(i.string, i['href']) for i in items[0]],
                  'genre': [(i.string, i['href']) for i in items[1]],
                  'state': [(i.string, i['value']) for i in items[2] if len(i['value']) > 0],
                  'city': [(i.string, i['value']) for i in items[3] if len(i['value']) > 0]}

    return categories


def add_stations(url):
    soup = BeautifulSoup(make_request(base_url+url), convertEntities=BeautifulSoup.HTML_ENTITIES)
    try: items = soup.find('ul', attrs={'class': 'strips js-sortable'})('li')
    except:
        addon_log('exception add_stations items: %s' %format_exc())
        return
    addon_log('Found %s stations.' %len(items))
    for i in items:
        try:
            name = i['data-name']
            item_url = i.a['href']
            iconimage = 'http://' + re.findall("background-image: url\(.+?\)/(.+?)'\)", str(i))[0]
            add_station(name.encode('utf-8'), item_url, iconimage)
        except:
            addon_log('exception add_stations: %s' %format_exc())


def resolve_url(url):
    headers = {'User-agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0',
               'Referer' : base_url+url}
    local = cache.cacheFunction(scrape_categories)['local']
    json_url = ('http://www.iheart.com/a/live/station/%s/stream/?_country=%s&_rel=%s'
                %(url.split('-')[-1], local[2], local[3]))
    addon_log('json_url: %s' %json_url)
    data = json.loads(make_request(json_url, '', headers))
    playback_url = None
    try:
        playback_url = data['shoutcast_url']
        addon_log('playback_url: %s' %playback_url)
    except:
        addon_log('playback_url exception')
        addon_log('Stream_urls: %s' %data['stream_urls'])

    if playback_url:
        if playback_url.endswith('.pls'):
            playback_url = parse_playlist(playback_url)

    if playback_url:
        success = True
    else:
        success = False
        playback_url = ''
    item = xbmcgui.ListItem(path=playback_url)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), success, item)


class HeadRequest(urllib2.Request):
    def get_method(self):
        return "HEAD"


def parse_playlist(url):
    data = make_request(url)
    for i in data.split():
        if i.startswith('File'):
            try:
                stream_url = i.split('=', 1)[1]
                response = urllib2.urlopen(HeadRequest(stream_url))
                if 'audio' in response.info()['Content-Type']:
                    return stream_url
                else: continue
            except:
                addon_log('exception parse_playlist: %s' %format_exc())


def add_categories():
    cats = cache.cacheFunction(scrape_categories)
    if len(cats['local'][0]) > 0:
        add_dir('Local Stations: '+cats['local'][0], cats['local'][1], 2, icon)
    add_dir('Talk Radio', 'talk', 1, icon)
    add_dir('By Genre', 'genre', 1, icon)
    add_dir('By State', 'state', 1, icon)
    add_dir('By City', 'city', 1, icon)
    add_dir('Search', 'search', 7, icon)
    add_dir('Favorites', 'favorites', 5, icon)


def add_subcats(sub_cat_key):
    subcats = cache.cacheFunction(scrape_categories)[sub_cat_key]
    for name, url in subcats:
        add_dir(name, url, 2, icon)


def search():
    keyboard = xbmc.Keyboard('','Search')
    keyboard.doModal()
    if (keyboard.isConfirmed() == False):
        return
    search_q = keyboard.getText()
    if len(search_q) == 0:
        return
    add_stations('/search/?q=%s' %search_q)


def add_station(name, item_url, iconimage, context=None):
    params = {'name': name, 'url': item_url, 'mode': 3}
    url = '%s?%s' %(sys.argv[0], urllib.urlencode(params))
    listitem = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
    fav_mode = 4
    menu_string = 'Add to Add-on Favorites'
    if context == 'fav':
        fav_mode = 6
        menu_string = 'Remove from Favorites'
    fav_params = {'name': name, 'url': item_url, 'mode': fav_mode, 'iconimage': iconimage}
    listitem.addContextMenuItems(
        [(menu_string, 'XBMC.RunPlugin(%s?%s)' %(sys.argv[0], urllib.urlencode(fav_params)))])
    listitem.setProperty('IsPlayable', 'true')
    listitem.setProperty("Fanart_Image", fanart)
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), url, listitem, False)


def add_dir(name, url, mode, iconimage):
    params = {'name': name, 'url': url, 'mode': mode}
    url = '%s?%s' %(sys.argv[0], urllib.urlencode(params))
    listitem = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
    listitem.setProperty("Fanart_Image", fanart)
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), url, listitem, True)


def add_favorite(name, url, iconimage):
    favorites = xbmcvfs.exists(favorites_file)
    if not favorites:
        fav_list = []
    else:
        fav_list = eval(open(favorites_file).read())
    fav_list.append((name, url, iconimage))
    a = open(favorites_file, "w")
    a.write(repr(fav_list))
    a.close()


def get_favorites():
    if xbmcvfs.exists(favorites_file):
        fav_list = eval(open(favorites_file).read())
        for name, item_url, iconimage in fav_list:
            add_station(name.title(), item_url, iconimage, 'fav')


def rm_favorite(fav_name):
    fav_list = eval(open(favorites_file).read())
    new_list = list(fav_list)
    for i in range(len(new_list)):
        if new_list[i][0] == fav_name:
            del fav_list[i]
            break
    a = open(favorites_file, "w")
    a.write(repr(fav_list))
    a.close()


def get_params():
    p = parse_qs(sys.argv[2][1:])
    for i in p.keys():
        p[i] = p[i][0]
    return p


if debug == 'true':
    cache.dbg = True
params = get_params()
addon_log("params: %s" %params)

try:
    mode = int(params['mode'])
except:
    mode = None

if mode == None:
    add_categories()
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode == 1:
    add_subcats(params['url'])
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode == 2:
    add_stations(params['url'])
    xbmc.executebuiltin('Container.SetViewMode(500)')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode == 3:
    resolve_url(params['url'])

elif mode == 4:
    add_favorite(params['name'], params['url'], params['iconimage'])
    xbmc.executebuiltin("XBMC.Notification(%s - added to favorites,%s,%s)"
                        %(params['name'], '5000', icon))

elif mode == 5:
    get_favorites()
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode == 6:
    rm_favorite(params['name'])
    xbmc.executebuiltin('Container.Refresh')

elif mode == 7:
    search()
    xbmcplugin.endOfDirectory(int(sys.argv[1]))