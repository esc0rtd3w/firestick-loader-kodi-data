from __future__ import unicode_literals
from resources.lib.modules.addon import Addon
import sys,os,re
import urlparse,urllib
import xbmc, xbmcgui, xbmcplugin, xbmcaddon
from resources.lib.modules import control,client,teevee2,metadata,cache
from resources.lib.modules.log_utils import log

meta_enabled = control.setting('tv_metadata') == 'true'
paginated = control.setting('limit_shows') == 'true'
offset = int(control.setting('results_number'))

base = 'http://opentuner.is/'

addon = Addon('plugin.video.teevee', sys.argv)
addon_handle = int(sys.argv[1])

if not os.path.exists(control.dataPath):
    os.mkdir(control.dataPath)

AddonPath = addon.get_path()
themes=['new','simple']

theme = themes[int(control.setting('theme'))]
IconPath = os.path.join(AddonPath , "resources/media/%s"%theme)


def icon_path(filename):
    if 'http://' in filename:
        return filename
    return os.path.join(IconPath, filename)
fanart = icon_path('fanart.jpg')
args = urlparse.parse_qs(sys.argv[2][1:])
mode = args.get('mode', None)


if mode is None:
    addon.add_item({'mode': 'favourites'}, {'title':control.lang(30100).encode('utf-8')}, img=icon_path('Favourites.png'), fanart=fanart,is_folder=True)
    addon.add_item({'mode': 'new_episodes', 'page':'1'}, {'title':control.lang(30101).encode('utf-8'), 'page':'1'}, img=icon_path('Latest_added.png'), fanart=fanart,is_folder=True)
    if control.setting('enable_calendar')=='true':
        addon.add_item({'mode': 'calendar'}, {'title':control.lang(30102).encode('utf-8')}, img=icon_path('Calendar.png'), fanart=fanart,is_folder=True)

    addon.add_item({'mode': 'open_shows', 'url':'/latest-added/', 'page':'1'}, {'title':control.lang(30103).encode('utf-8')}, img=icon_path('Latest_added.png'), fanart=fanart,is_folder=True)
    addon.add_item({'mode': 'open_shows', 'url':'/popular-today/', 'page':'1'}, {'title':control.lang(30104).encode('utf-8')}, img=icon_path('Popular.png'), fanart=fanart,is_folder=True)
    addon.add_item({'mode': 'open_shows', 'url':'/most-popular/', 'page':'1'}, {'title':control.lang(30105).encode('utf-8')}, img=icon_path('Popular.png'), fanart=fanart,is_folder=True)
    addon.add_item({'mode': 'alphabet'}, {'title':control.lang(30106).encode('utf-8')}, img=icon_path('AZ.png'), fanart=fanart,is_folder=True)
    addon.add_item({'mode': 'genres'}, {'title':control.lang(30107).encode('utf-8')}, img=icon_path('Genre.png'), fanart=fanart,is_folder=True)
    addon.add_item({'mode': 'downloader'}, {'title':control.lang(30108).encode('utf-8')}, img=icon_path('Downloads.png'), fanart=fanart,is_folder=True)
    addon.add_item({'mode': 'search'}, {'title':control.lang(30109).encode('utf-8')}, img=icon_path('Search.png'), fanart=fanart,is_folder=True)
    
    
    
    addon.end_of_directory()
    from resources.lib.modules import cache, changelog
    cache.get(changelog.get, 600000000, control.addonInfo('version'), table='changelog')

elif mode[0]=='favourites':
    from resources.lib.modules import favourites
    favs = favourites.get_favourites()
    total=len(favs)
    for fav in favs:
        title,url,year = fav
        url = base + url
        meta = metadata.get_show_meta(title,url,year=year)
        context = cache.get(teevee2.get_tv_context,10000,title,url,year,True)
        addon.add_item({'mode': 'open_show', 'url': url,'title': title}, meta,img=meta['cover_url'], fanart=meta['backdrop_url'], total_items=total,contextmenu_items=context,is_folder=True)
    addon.end_of_directory()

elif mode[0]=='open_shows':
    url = url_sh = args['url'][0]
    page = int(args['page'][0])
    try:    sort = args['sort'][0] == 'true'
    except: sort = False

    shows = cache.get(teevee2.get_shows,24,url)
    if sort:
        shows.sort(key=lambda x: x[1])
    last = False
    if paginated and meta_enabled:
        if len(shows)<=offset:
            last=True
            pass
        else:
            start = (page-1)*offset
            end = start + offset
            if (end+1) >= len(shows):
                last = True
                end = len(shows) - 1
            shows = shows[start:end]
    
    total = len(shows)

    for show in shows:
        url,title,year = show
        meta = metadata.get_show_meta(title,url,year=year)
        context = teevee2.get_tv_context(title,url,year,False)
        addon.add_item({'mode': 'open_show', 'url': url,'title': title}, meta,img=meta['cover_url'], fanart=meta['backdrop_url'],contextmenu_items=context, total_items=total,is_folder=True)

    if paginated and meta_enabled and not last:
        addon.add_item({'mode': 'open_shows', 'url':url_sh, 'page':'%s'%(page+1)}, {'title':control.lang(30171).encode('utf-8')}, img=icon_path('Next.png'), fanart=fanart,is_folder=True)


    addon.end_of_directory()

elif mode[0]=='new_episodes':
    page = int(args['page'][0])
    episodes = cache.get(teevee2.get_new_episodes,24)
    last = False
    if paginated and meta_enabled:
        if len(episodes)<=offset:
            last=True
        else:
            start = (page-1)*offset
            end = start + offset
            if (end+1) >= len(episodes):
                last = True
                end = len(episodes) - 1
            episodes = episodes[start:end]
    
    total = len(episodes)

    for ep in episodes:
        url,showtitle,season,episode = ep
        meta = metadata.get_episode_meta(showtitle,season,episode,url,more=True)
        context = teevee2.get_episode_context(showtitle,season,episode,url,meta['cover_url'])
        addon.add_video_item({'mode':'play_episode','url':'url'},meta,img=meta['cover_url'], fanart=meta['backdrop_url'],contextmenu_items=context, total_items=total)

    if paginated and meta_enabled and not last:
        addon.add_item({'mode': 'new_episodes','page':'%s'%(page+1)}, {'title':control.lang(30171).encode('utf-8')}, img=icon_path('Next.png'), fanart=fanart,is_folder=True)


    addon.end_of_directory()


elif mode[0]=='alphabet':
    alphabet = teevee2.get_alphabet()
    for al in alphabet:
        addon.add_item({'mode': 'open_shows', 'url':al[0], 'page':'1','sort':'true'}, {'title':al[1]}, img=icon_path('AZ.png'), fanart=fanart,is_folder=True)
    addon.end_of_directory()   

elif mode[0]=='genres':
    alphabet = teevee2.get_genres()
    for al in alphabet:
        addon.add_item({'mode': 'open_shows', 'url':al[0], 'page':'1'}, {'title':al[1]}, img=icon_path('Genre.png'), fanart=fanart,is_folder=True)
    addon.end_of_directory()    
    

elif mode[0]=='open_show':
    url = args['url'][0]
    show = args['title'][0]

    imdb,seasons = teevee2.get_seasons(url)
    meta = metadata.get_season_meta(show,len(seasons),imdb)
    i = 0
    for s in seasons:
        addon.add_item({'mode': 'open_season', 'url':s[0], 'num':'%s'%(i+1)}, {'title':'%s %s'%(control.lang(30170).encode('utf-8'),s[1])}, img=meta[i]['cover_url'], fanart=meta[i]['backdrop_url'],is_folder=True)
        i += 1
    addon.end_of_directory()

elif mode[0]=='open_season':
    url = args['url'][0]
    num = args['num'][0]

    imdb,showtitle,episodes = teevee2.get_episodes(url,num)
    total = len(episodes)
    for ep in episodes:
        url,episode,episode_title = ep
        meta = metadata.get_episode_meta(showtitle,num,episode,url,ep_title=episode_title)
        if episode_title not in meta['title']:
            meta['title'] = '%sx%s %s'%(num,episode,episode_title)
        context = teevee2.get_episode_context(showtitle,num,episode,url,meta['cover_url'])
        addon.add_video_item({'mode':'play_episode','url':url},meta,img=meta['cover_url'], fanart=meta['backdrop_url'],contextmenu_items=context, total_items=total)

    addon.end_of_directory()


elif mode[0]=='calendar':
    days = teevee2.get_month()
    for day in days:
        d=day[1]
        m=day[2]
        y=day[3]
        mnth=day[4]
        name=day[0]+', %s %s '%(d,mnth)
        addon.add_item({'mode': 'open_day', 'day':d, 'month':m, 'year':y,'page':'1'},{'title': name}, img=icon_path('Calendar.png'), fanart=fanart,is_folder=True)
    addon.end_of_directory()

elif mode[0]=='open_day':
    day = args['day'][0]
    month = args['month'][0]
    year = args['year'][0]
    page = int(args['page'][0])
    episodes = cache.get(teevee2.get_episodes_calendar,100,day,month,year)
    last = False
    if paginated and meta_enabled:
        if len(episodes)<=offset:
            last = True
        else:
            start = (page-1)*offset
            end = start + offset
            if (end+1) >= len(episodes):
                last = True
                end = len(episodes) - 1
            episodes = episodes[start:end]
    
    total = len(episodes)

    for ep in episodes:
        
        url,season,episode,showtitle,year = ep
        meta = metadata.get_episode_meta(showtitle,season,episode,url,more=True)
        context = teevee2.get_episode_context(showtitle,season,episode,url,meta['cover_url'])
        addon.add_video_item({'mode':'play_episode','url':url},meta,img=meta['cover_url'], fanart=meta['backdrop_url'],contextmenu_items=context, total_items=total)

    if paginated and meta_enabled and not last:
        addon.add_item({'mode': 'new_episodes','page':'%s'%(page+1)}, {'title':control.lang(30171).encode('utf-8')}, img=icon_path('Next.png'), fanart=fanart,is_folder=True)


    addon.end_of_directory()




elif mode[0]=='play_episode':
    url = args['url'][0]
    links,sl = teevee2.get_sources(url)
    if control.setting('autoplay')!='true':
        i = control.selectDialog(sl)
        if i>-1:
            try:
                url = links[i]
                if 'iwatch' in url:
                    url = teevee2.resolve_iwatch(url)
                import urlresolver
                resolved = urlresolver.resolve(url)
                if control.setting('use_TM')=='true':
                    try:
                        from dudehere.routines.transmogrifier import TransmogrifierAPI
                        TM = TransmogrifierAPI()
                        resolved = TM.get_streaming_url(resolved)
                    except:
                        pass
                addon.resolve_url(resolved)
            except:
                control.infoDialog(control.lang(30168).encode('utf-8'))
    else:
        index = 0
        import urlresolver
        done = False
        checked = 0
        while not done:
            url = links[index%len(links)]
            if 'iwatch' in url:
                url = teevee2.resolve_iwatch(url)
            
            try:
                checked +=1
                import urlresolver
                resolved=urlresolver.resolve(url)
            except:
                index +=1
                continue
            if not resolved:
                index +=1
                continue
            else:
                break

            if checked>=len(links):
                resolved = False
                break

        if resolved:
            if control.setting('use_TM')=='true':
                try:
                    from dudehere.routines.transmogrifier import TransmogrifierAPI
                    TM = TransmogrifierAPI()
                    resolved = TM.get_streaming_url(resolved)
                except:
                    pass
            addon.resolve_url(resolved)

elif mode[0] == 'downloader':
    import resources.lib.modules.downloader as downloader
    downloader.downloader()

elif mode[0] == 'addDownload':
    name,url,image=args['name'][0],args['url'][0],args['thumb'][0]
    import resources.lib.modules.downloader as downloader
    downloader.addDownload(name,url,image)

elif mode[0] == 'removeDownload':
    url=args['url'][0]
    import resources.lib.modules.downloader as downloader
    downloader.removeDownload(url)

elif mode[0] == 'startDownload':
    import resources.lib.modules.downloader as downloader
    downloader.startDownload()

elif mode[0] == 'startDownloadThread':
    import resources.lib.modules.downloader as downloader
    downloader.startDownloadThread()

elif mode[0] == 'stopDownload':
    import resources.lib.modules.downloader as downloader
    downloader.stopDownload()

elif mode[0] == 'statusDownload':
    import resources.lib.modules.downloader as downloader
    downloader.statusDownload()

elif mode[0]=='download':


    url = args['url'][0]
    title = args['title'][0]
    image = args['thumb'][0]


    tm = control.setting('dl_TM') == 'true'
    try:
        from dudehere.routines.transmogrifier import TransmogrifierAPI
        TM = TransmogrifierAPI()
    except:
        tm = False



    links,sl = teevee2.get_sources(url)
    if control.setting('auto_download')!='true':
        i = control.selectDialog(sl)
        if i>-1:
            try:
                url = links[i]
                if 'iwatch' in url:
                    url = teevee2.resolve_iwatch(url)
                import urlresolver
                resolved = urlresolver.resolve(url)
                if tm:
                    resolved = resolved.split('|')[0]
                    ext = os.path.splitext(urlparse.urlparse(resolved).path)[1][1:].lower()
                    if ext == 'm3u8': raise Exception()
                    filename = title.replace(' ','_')
                    filename = re.sub('[^-a-zA-Z0-9_.() ]+', '', filename)
                    filename = filename.rstrip('.')
                    try:
                        season = re.findall('S(\d+)',title)[0]
                        episode = re.findall('E(\d+)',title)[0]
                    except:
                        season,episode = '',''
                    video = {
                        "type": 'tvshow',
                        "filename": filename + '.' + ext,
                        "url": resolved,
                        "season": season,
                        "episode": episode,
                        "addon": "plugin.video.teevee",
                        "save_dir": control.setting('download_folder')
                    }
                    response = TM.enqueue([video])
                else:
                    import resources.lib.modules.downloader as downloader
                    downloader.addDownload(title,resolved,image,resolved=True)
            except:
                control.infoDialog(control.lang(30168).encode('utf-8'))
    else:
        resolved = False
        index = 0
        import urlresolver
        done = False
        checked = 0
        while not done:
            url = links[index%len(links)]
            if 'iwatch' in url:
                url = teevee2.resolve_iwatch(url)
            
            try:
                checked +=1
                import urlresolver
                resolved=urlresolver.resolve(url)
            except:
                index +=1
                continue
            if not resolved:
                index +=1
                continue
            else:
                break

            if checked>=len(links):
                resolved = False
                break

        if resolved:
            if tm:
                resolved = resolved.split('|')[0]
                ext = os.path.splitext(urlparse.urlparse(resolved).path)[1][1:].lower()
                if ext == 'm3u8': raise Exception()
                filename = title.replace(' ','_')
                filename = re.sub('[^-a-zA-Z0-9_.() ]+', '', filename)
                filename = filename.rstrip('.')
                try:
                    season = re.findall('S(\d+)',title)[0]
                    episode = re.findall('E(\d+)',title)[0]
                except:
                    season,episode = '',''
                video = {
                    "type": 'tvshow',
                    "filename": filename + '.' + ext,
                    "url": resolved,
                    "season": season,
                    "episode": episode,
                    "addon": "plugin.video.teevee",
                    "save_dir": control.setting('download_folder')
                }
                response = TM.enqueue([video])
            else:
                import resources.lib.modules.downloader as downloader
                downloader.addDownload(title,resolved,image,resolved=True)
            

elif mode[0]=='add_tv_fav':
    name = args['show'][0]
    link = args['link'][0]
    year = args['year'][0]
    from resources.lib.modules import favourites
    favourites.add_favourite_show(name,link,year)

elif mode[0]=='rem_tv_fav':
    title = args['show'][0]
    link = args['link'][0] 
    from resources.lib.modules import favourites
    favourites.remove_tv_fav(title,link) 
    xbmc.executebuiltin("Container.Refresh")

elif mode[0]=='del_tv_all':
    confirm = control.yesnoDialog(control.lang(30169).encode('utf-8'),control.lang(30401).encode('utf-8'),'')
    if confirm==1:
        from resources.lib.modules import favourites
        favourites.delete_all_tv_favs()
        xbmc.executebuiltin("Container.Refresh")
        control.infoDialog(control.lang(30402).encode('utf-8'))

elif mode[0]=='search':
    addon.add_item({'mode': 'open_key_search'}, {'title':'[COLOR green]%s[/COLOR]'%control.lang(30404).encode('utf-8')}, img=icon_path('Search.png'), fanart=fanart,is_folder=True)
    from resources.lib.modules import favourites
    queries = favourites.get_search_history('tv')

    del_url = addon.build_plugin_url({'mode': 'del_his_tv'})
    context = [(control.lang(30143).encode('utf-8'),'RunPlugin(%s)'%del_url)]
    for q in queries:
        addon.add_item({'mode': 'open_search', 'q': q, 'page':'1'}, {'title':q}, img=icon_path('Search.png'), fanart=fanart,contextmenu_items=context, is_folder=True)

    addon.end_of_directory()

elif mode[0]=='open_key_search':
    q = control.get_keyboard(control.lang(30403).encode('utf-8'))
    if q:
        from resources.lib.modules import favourites
        url = addon.build_plugin_url({'mode':'open_search','q':q,'page':'1'})
        favourites.add_search_query(q,'tv')
        xbmc.executebuiltin("Container.Refresh")
        import time
        time.sleep(2)
        control.execute('Container.Update(%s)'%url)


elif mode[0]=='open_search':
    url = url_sh = args['q'][0]
    page = int(args['page'][0])
    shows = teevee2.search(url)
    last = False
    if paginated and meta_enabled:
        if len(shows)<=offset:
            last=True
            pass
        else:
            start = (page-1)*offset
            end = start + offset
            if (end+1) >= len(shows):
                last = True
                end = len(shows) - 1
            shows = shows[start:end]
    
    total = len(shows)

    for show in shows:
        url,title,year = show
        meta = metadata.get_show_meta(title,url,year=year)
        context = teevee2.get_tv_context(title,url,year,False)
        addon.add_item({'mode': 'open_show', 'url': url,'title': title}, meta,img=meta['cover_url'], fanart=meta['backdrop_url'],contextmenu_items=context, total_items=total,is_folder=True)

    if paginated and meta_enabled and not last:
        addon.add_item({'mode': 'open_search', 'q':url, 'page':'%s'%(page+1)}, {'title':control.lang(30171).encode('utf-8')}, img=icon_path('Next.png'), fanart=fanart,is_folder=True)


    addon.end_of_directory()

elif mode[0]=='del_his_tv':
    from resources.lib.modules import favourites
    favourites.delete_history('tv')
    xbmc.executebuiltin("Container.Refresh")
    control.infoDialog(control.lang(30402).encode('utf-8'))

elif mode[0]=='clear_cache':
    cache.clear()