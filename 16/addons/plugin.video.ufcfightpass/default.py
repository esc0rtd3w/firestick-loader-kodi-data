import sys, xbmcgui, xbmcplugin, xbmcaddon
import os, requests, urllib, urllib2, cookielib, re, json, datetime, time
from urlparse import parse_qsl
from bs4 import BeautifulSoup 


addon           = xbmcaddon.Addon(id='plugin.video.ufcfightpass')
addon_url       = sys.argv[0]
addon_handle    = int(sys.argv[1])
addon_icon      = addon.getAddonInfo('icon')
addon_BASE_PATH = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo('profile'))
COOKIE_FILE     = os.path.join(addon_BASE_PATH, 'cookies.lwp')
CACHE_FILE      = os.path.join(addon_BASE_PATH, 'data.json')
c_base_url      = 'https://www.ufc.tv/category/'
ua              = 'Mozilla/5.0 (Linux; Android 6.0.1; D6603 Build/23.5.A.0.570; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/56.0.2924.87 Mobile Safari/537.36 android mobile ufc 7.0310'


def get_creds():
    if len(addon.getSetting('email')) == 0 or len(addon.getSetting('password')) == 0:
        return None
    return {
        'username': addon.getSetting('email'),
        'password': addon.getSetting('password')
    }


def post_auth(creds):
    url = 'https://www.ufc.tv/page/fightpass' 
    cj = cookielib.LWPCookieJar(COOKIE_FILE)
    try:
        cj.load()
    except:
        pass

    # build an opener that we can reuse here
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    opener.addheaders = [('User-Agent', urllib.quote(ua))]

    # pre-auth, load in the required cookies to be used in the next step
    try:
        resp = opener.open(url)
    except urllib2.URLError, e:
        print e.args
        return None

    s_url = 'https://www.ufc.tv/secure/signin?parent=' + url
    try:
        s_resp = opener.open(s_url)
    except urllib2.URLError, e:
        print e.args
        return None
    
    # login with creds and capture the auth response
    a_url = 'https://www.ufc.tv/secure/authenticate'
    try:
        auth_resp = opener.open(a_url, urllib.urlencode(creds))
    except urllib2.URLError, e:
        print e.args
        return None

    rdata = auth_resp.read()
    auth_resp.close()

    cj.save(COOKIE_FILE, ignore_discard=True)

    if auth_resp.code == 200:
        #TODO: need to handle login locked scenario as well
        soup = BeautifulSoup(rdata,"html.parser")
        code = soup.find('code').get_text()
        if code == 'loginsuccess':
            return True
        else:
            print('Authentication error. Status: ' + code)

    return False


def publish_point(video):
    url = 'https://www.ufc.tv/service/publishpoint'
    headers = {
        'User-Agent': ua
    }

    payload = {
        'id': video['id'],
        'type': 'video',
        'nt': '1',
        'format': 'json'
    }

    cj = cookielib.LWPCookieJar(COOKIE_FILE)
    try:
        cj.load(COOKIE_FILE, ignore_discard=True)
    except:
        pass

    s = requests.Session()
    s.cookies = cj
    resp = s.post(url, data=payload, headers=headers)
    # normally status 400 if have an expired session
    status = resp.status_code
    result = resp.json()
    if not result:
        return status, None

    o_path = result['path']
    h_path = o_path.replace('android', 'ced')
    # does the hd video resource exist?
    resp = s.get(h_path, data=payload, headers=headers)
    if resp.status_code == 404:
        return status, o_path

    return resp.status_code, h_path


def get_categories():
    # Fetch the main UFC Fight Pass category menu data
    data = get_data(c_base_url + 'fightpass')
    results = []

    for c in data['subCategories']:
        results.append({
            'title': c['name'],
            'url': c_base_url +  c['seoName'].replace('FIGHTPASS-LIVE-EVENTS', 'LIVE-EVENTS'),
            'level': 'top'
        })

    # append the Just Added category as well
    results.append({
        'title': 'Just Added', 
        'url': c_base_url + 'JUST-ADDED', 
        'level': 'top'
    })

    return {
        'paging': None,
        'items': results
    }


def main():
    creds = get_creds()
    if creds is None:
        # TODO: ensure we have credentials stored first, and if not, prompt for them.
        dialog = xbmcgui.Dialog()
        result = dialog.yesno('UFC Fight Pass', 'You have not yet signed in to UFC Fight Pass.\nWould you like to sign in now?')
        if result:
            addon.openSettings()
            creds = get_creds()
        else:
            # build free option menu
            dialog = xbmcgui.Dialog()
            dialog.ok('UFC Fight Pass', 'You have not yet signed in to UFC Fight Pass. \nPlease enjoy some free videos until you do.')
            create_free_menu()

    if creds:
        if not post_auth(creds):
            dialog = xbmcgui.Dialog()
            dialog.ok('Authorization Error', 'Authorization to UFC Fight Pass failed. \nPlease enjoy some free videos.')
            # build free option (provided by ufc.tv) menu for those that do not have Fight Pass.
            create_free_menu()
        else:
            # fetch the main categories to start, and display the main menu
            categories = get_categories()
            build_menu(categories)


def create_free_menu():
    data = get_data('http://www.ufc.tv/category/free-video')
    vids = get_parsed_vids(data)
    build_menu(vids)


def build_menu(itemData):
    listing = []
    first = itemData['items'][0]
    is_folder = 'id' not in first
    is_top_level = 'level' in first

    for i in itemData['items']:
        thumb = i['thumb'] if not is_folder else None
        # stupid encoding hack for now..
        try:
            i_title = i['title'].encode('utf-8')
        except:
            i_title = i['title']

        live_state = ''
        if 'isLive' in i and i['isLive'] == 1:
            live_state = ' - [COLOR green]LIVE NOW[/COLOR]'

        if is_folder and 'Live Events' in i_title:
            live_count = get_live_count()
            title = '{0} [B][COLOR green]({1})[/COLOR][/B]'.format(i_title, live_count) if live_count > 0 else i_title
        else:
            title = '[B][{0}{1}][/B]  {2}'.format(i['airdate'], live_state, i_title) if not is_folder else i_title
        
        item = xbmcgui.ListItem(label=title, thumbnailImage=thumb)

        if is_folder:
            url = '{0}?action=traverse&u={1}&t={2}'.format(addon_url, i['url'], i_title)
        else:
            url = '{0}?action=play&i={1}&t={2}'.format(addon_url, i['id'], i_title)
            # generate appropriate context menu
            ctx = get_ctx_items(i)
            if len(ctx) > 0:
                item.addContextMenuItems(get_ctx_items(i), replaceItems=True)

        listing.append((url, item, is_folder))

    if is_top_level:
        # append My Queue menu item - refactor to allow pulling other single action based options like search
        item = xbmcgui.ListItem(label='My Queue') 
        listing.append(('{0}?action=queue'.format(addon_url), item, True))

    # generate paging navigation
    if 'paging' in itemData and itemData['paging']:
        pg_items = get_paging(itemData['paging'])
        if len(pg_items) > 0:
            listing.extend(pg_items)

    if len(listing) > 0:
        xbmcplugin.addDirectoryItems(addon_handle, listing, len(listing))
        xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=False)


def get_paging(pagingData):
    items = []
    pn = int(pagingData['pageNumber'])
    tp = int(pagingData['totalPages'])
    url = dict(parse_qsl(sys.argv[2][1:]))['u']
    if pn < tp:
        # next
        item = xbmcgui.ListItem(label='[B]- [I]Page %s of %s[/I] - Next Page[/B] >' %(pn, tp))
        items.append(('{0}?action=traverse&u={1}&pn={2}'.format(addon_url, url, pn+1), item, True))
        # goto page
        #item = xbmcgui.ListItem(label='[B][I]Goto Page..[/I][/B]')
        #items.append(('{0}?action=goto_pn&u={1}&c={2}&m={3}'.format(addon_url, url, pn, tp), item, True))
        return items
    return []


def get_ctx_items(item):
    ctx = []
    params = dict(parse_qsl(sys.argv[2][1:]))
    if params and params['action'] == 'queue':
        ctx_path = '{0}?action=queueDel&i={1}'.format(addon_url, item['id'])
        ctx.append(('Remove from My Queue', 'XBMC.RunPlugin({0})'.format(ctx_path)))
        ctx.append(('Refresh My Queue', 'Container.Refresh'))
    else:
        ctx_path = '{0}?action=queueSet&i={1}'.format(addon_url, item['id'])
        ctx.append(('Add to My Queue', 'XBMC.RunPlugin({0})'.format(ctx_path)))
    return ctx


def get_data(url, params=None):
    if params is None:
        params = {
            'format': 'json'
        }

    headers = {
        'User-Agent': ua
    }

    cj = cookielib.LWPCookieJar(COOKIE_FILE)
    try:
        cj.load(COOKIE_FILE, ignore_discard=True)
    except:
        pass

    s = requests.Session()
    s.cookies = cj
    resp = s.get(url, headers=headers, params=params)
    if not resp.status_code == 200:
        return None

    return resp.json()

# refactor to consolidate common api client code..
def post_data(url, payload):
    headers = {
        'User-Agent': ua
    }

    cj = cookielib.LWPCookieJar(COOKIE_FILE)
    try:
        cj.load(COOKIE_FILE, ignore_discard=True)
    except:
        pass

    s = requests.Session()
    s.cookies = cj
    resp = s.post(url, data=payload, headers=headers)
    if not resp.status_code == 200:
        return None

    return resp.json()


def get_parsed_subs(data):
    # if we're at video depth, signal as such
    if 'programs' in data or 'subCategories' not in data:
        return []

    subCategories = []
    for sc in data['subCategories']:
        subCategories.append({
            'title': sc['name'], 
            'url': c_base_url + sc['seoName']
        })

    return {
        'paging': None, 
        'items': subCategories
    }

    
def get_parsed_vids(data):
    if 'programs' not in data:
        return []

    img_base_url = 'https://neulionmdnyc-a.akamaihd.net/u/ufc/thumbs/'
    v_list = []
    
    for v in data['programs']:

        if 'beginDateTime' in v:
            v_date = v['beginDateTime']
        else:
            v_date  = v['releaseDate']

        v_list.append({
            'id': v['id'], 
            'title': get_title(v), 
            'thumb': img_base_url + v['image'], 
            'airdate': datetime.datetime.strftime(parse_date(v_date, '%Y-%m-%dT%H:%M:%S.%f'), '%Y-%m-%d'), 
            'plot': v['description'], 
            'isLive': v['liveState'] if 'liveState' in v else 0
        })
      
    return {
        'paging': data['paging'] if 'paging' in data else None,
        'items': v_list
    }


def get_title(program):
    name  = program['name'].encode('utf-8')
    if 'programCode' in program and program['programCode'].strip():
        pcode = program['programCode'].encode('utf-8')
        return '{0} - {1}'.format(pcode, name)
    else:
        return name


def get_live_count():
    try:
        data = get_data(c_base_url + 'LIVE-EVENTS')
        return sum(1 for i in data['programs'] if 'liveState' in i and i['liveState'] == 1)
    except:
        return 0


def load_queue():
    queued = queue_get()
    if len(queued) > 0:
        build_menu(queued)
    else:
        xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=False)


def get_accessToken():
    payload = {
        'format': 'json'
    }
    data = post_data('https://www.ufc.tv/secure/accesstoken', payload)
    if data and 'accessToken' in data['data']:
        return data['data']['accessToken']
    return None


def queue_get():
    q_data = get_pers('https://apis.neulion.com/personalization_ufc/v1/playlist/get')
    if 'contents' in q_data:
        q_ids = [q['id'] for q in q_data['contents']]

        if len(q_ids) > 0:
            ids = ','.join(q_ids)
            results = get_data('https://ufc.tv/service/programs', params={
                'ids': ids,
                'format': 'json'
            })
            return get_parsed_vids(results)

    return []


def get_pers(url, pid=None, ptype=None, count=0):
    token = get_accessToken()
    params = {
        'token': token
    }

    if pid and ptype:
        params['id'] = pid
        params['type'] = ptype
        
    data = get_data(url, params=params)

    if 'result' in data and data['result'] == 'unauthorized': # status still 200??
        if count < 3:  # allow 3 retries on failure before bailing
            # we need to re-auth and update token
            print('UFCFP: get_pers re-auth for token (retry %s/3)' %(count+1))
            if post_auth(get_creds()):
                return get_pers(url, pid, ptype, (count+1))
        else:
            return None

    return data


def queue_set(id):
    resp = get_pers('https://apis.neulion.com/personalization_ufc/v1/playlist/set', id, 'program')
    if 'result' in resp and resp['result'] == 'success': 
        notify('Success', 'Video added to queue')
    else:
        notify('Error', 'Unable to add video to queue')


def queue_del(id):
    resp = get_pers('https://apis.neulion.com/personalization_ufc/v1/playlist/delete', id, 'program')
    if 'result' in resp and resp['result'] == 'success':
        xbmc.executebuiltin('Container.Refresh') 
    else:
        notify('Error', 'Unable to remove video from queue')


def goto_page(url, curr_pn, max_pn):
    pn = 0
    input_pn = xbmcgui.Dialog().numeric(0, 'Go to page number:')
    if input_pn:
        pn = int(input_pn)
    if pn > 0 and pn <= max_pn:
        traverse(url, pn)
    else:
        xbmcgui.Dialog().ok('Error', 'Invalid page selected. Returning to page %s.' %(curr_pn))
        traverse(url, curr_pn)


def parse_date(dateString, format='%Y-%m-%d %H:%M:%S.%f'):
    try:
        p_date = datetime.datetime.strptime(dateString, format)
    except TypeError:
        p_date = datetime.datetime.fromtimestamp(time.mktime(time.strptime(dateString, format)))
    return p_date


def needs_refresh(cache_date):
    p_date = parse_date(cache_date)
    delta = (datetime.datetime.now() - p_date).seconds / 60
    interval = addon.getSetting('cacheInterval')
    print 'UFCFP: Minutes elapsed since last cached: {0}. Set at: {1}.'.format(delta, interval)
    return delta >= int(interval)


def traverse(url, pn=None):
    p_url = url + '/%s' %(pn) if pn else url
    print("UFCFP: Traversing categories for URL: " + p_url)
    # check / load from cache if available and prior to next refresh interval
    items  = None
    cached = None

    if should_cache(p_url):
        cached = get_cacheItem(p_url)

    if cached and not needs_refresh(cached['lastCached']):
        items = cached['data']
        print('UFCFP: Using cached data..')

    else:
        print('UFCFP: No cached data. Fetching new data..')
        params = None
        if pn:
            params = {
                'format': 'json', 
                'pn': pn
            }

        data = get_data(url, params)

        if not data:
            # ideally, we need to throw an error here, because we received no data from the server
            print('UFCFP get_data() returned no data')
            dialog = xbmcgui.Dialog()
            dialog.ok('Error', 'Unable to load content. Check log for more details.')
            return

        items = get_parsed_subs(data)

        if len(items) == 0:
            # no sub categories, so we're likely at video list depth
            items = get_parsed_vids(data)
            if len(items) == 0:
                dialog = xbmcgui.Dialog()
                dialog.ok('No content', 'No content found.')
                return

        # save the sub-category or video list data to cache
        if should_cache(p_url):
            save_cacheItem(p_url, {
                'data': items,
                'lastCached': str(datetime.datetime.now())
            })

    build_menu(items)


def should_cache(url):
    if 'LIVE-EVENTS' in url or 'JUST-ADDED' in url:
        return False
    return True


def play_video(v_id, v_title):
    # Fetch the stream url and play the video
    status, stream = publish_point({ 'id': v_id })
    if status == 400:
        #TODO: maybe pop up a messge to the user that it looks like they logged onto another device
        # ask if they would like to end that session and play on current device instead?
        # at this point, we likely need to re-auth
        if post_auth(get_creds()):
            status, stream = publish_point({ 'id': v_id })
        else:
            dialog = xbmcgui.Dialog()
            dialog.ok('Authorization Error', 'Authorization to UFC Fight Pass failed.')

    if stream:
        stream = stream + '|User-Agent=' + ua
        item = xbmcgui.ListItem(label=v_title)
        xbmc.Player().play(stream, item)
    else:
        dialog = xbmcgui.Dialog()
        dialog.ok('Playback Error', 'Unable to play video: ' + v_title)

    

def router(paramstring):
    params = dict(parse_qsl(paramstring))
    if params:
        action = params['action']
        if action == 'listing':
            main()
        elif action == 'play':
            play_video(params['i'], params['t'])
        elif action == 'traverse':
            pn = None
            if 'pn' in params:
                pn = params['pn']
            traverse(params['u'], pn)
        elif action == 'queue':
            load_queue()
        elif action == 'queueSet':
            queue_set(params['i'])
        elif action == 'queueDel':
            queue_del(params['i'])
        elif action == 'goto_pn':
            goto_page(params['u'], params['c'], params['m'])

    else:
        main()

def notify(header, msg, wait=3000, icon=addon_icon):
    xbmc.executebuiltin('Notification(%s,%s,%s,%s)' %(header, msg, wait, icon))


# data caching layer -- should move this into another class..
# should be consumed inside some sort of data repo class, and bits above abstracted out into that as well..
def get_allCache():
    try:
        fs = open(CACHE_FILE, 'r')
        data = json.load(fs)
        fs.close()
        return data
    except:
        return {}


def get_cacheItem(key):
    try:
        fs = open(CACHE_FILE, 'r')
        data = json.load(fs)
        fs.close()
        return data[key]
    except:
        return None


def save_cacheItem(key, data):
    try:
        # get cache / set value on key, save back to cache file
        cache = get_allCache()
        cache[key] = data
        fs = open(CACHE_FILE, 'w')
        json.dump(cache, fs)
        fs.close()
    except: 
        return False
    return True


if __name__ == '__main__':
    router(sys.argv[2][1:])