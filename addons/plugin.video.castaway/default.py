from __future__ import unicode_literals
from resources.lib.modules.addon import Addon
import sys,os
import urlparse,urllib
import xbmc, xbmcgui, xbmcplugin, xbmcaddon
from resources.lib.modules import control,myLists,client
from resources.lib.modules.log_utils import log

addon = Addon('plugin.video.castaway', sys.argv)
addon_handle = int(sys.argv[1])

if not os.path.exists(control.dataPath):
    os.mkdir(control.dataPath)

AddonPath = addon.get_path()
IconPath = os.path.join(AddonPath , "resources/media/")
fanart = os.path.join(AddonPath + "/fanart.jpg")
def icon_path(filename):
    if 'http://' in filename:
        return filename
    return os.path.join(IconPath, filename)

args = urlparse.parse_qs(sys.argv[2][1:])
mode = args.get('mode', None)


if mode is None:
    addon.add_item({'mode': 'live_sport'}, {'title':'Live Sport'}, img=icon_path('live_sport.jpg'), fanart=fanart,is_folder=True)
    addon.add_item({'mode': 'live_tv'}, {'title':'Live TV'}, img=icon_path('live_tv.jpg'), fanart=fanart,is_folder=True)
    addon.add_item({'mode': 'p2p_corner'}, {'title':'P2P Corner'}, img=icon_path('p2p_corner.jpg'), fanart=fanart,is_folder=True)
    addon.add_item({'mode': 'on_demand_sport_categories'}, {'title':'Sport On Demand'}, img=icon_path('sport_on_demand.jpg'), fanart=fanart,is_folder=True)
    addon.add_item({'mode': 'reddit'}, {'title':'Subreddits'}, img=icon_path('reddit.jpg'), fanart=fanart,is_folder=True)
    addon.add_item({'mode': 'my_castaway'}, {'title':'My Castaway'}, img=icon_path('my_castaway.jpg'), fanart=fanart,is_folder=True)
    addon.add_item({'mode': 'tools'}, {'title':'Tools'}, img=icon_path('tools.jpg'), fanart=fanart,is_folder=True)
    
    addon.end_of_directory()
    from resources.lib.modules import cache, control, changelog
    cache.get(changelog.get, 600000000, control.addonInfo('version'), table='changelog')
    

elif mode[0]=='my_castaway':
    #addon.add_item({'mode': 'favourites'}, {'title':'Favourites'}, img=icon_path('favourites.jpg'), fanart=fanart,is_folder=True)
    addon.add_item({'mode': 'my_lists'}, {'title':'My Lists'}, img=icon_path('my_lists.jpg'), fanart=fanart,is_folder=True)
    addon.add_item({'mode': 'keyboard_open'}, {'title':'Open URL'}, img=icon_path('my_castaway.jpg'), fanart=fanart,is_folder=True)
    addon.add_item({'mode': 'x'}, {'title':'[COLOR yellow]Follow me @natko1412[/COLOR]'}, img=icon_path('twitter.png'), fanart=fanart)
    addon.end_of_directory()


elif mode[0]=='keyboard_open':
    keyboard = xbmc.Keyboard('', 'Enter URL:', False)
    keyboard.doModal()
    if keyboard.isConfirmed():
        query = keyboard.getText()
        if query.startswith('livestreamer'):
            from resources.lib.resolvers import livestreamer
            resolved = livestreamer.resolve(query)
        else:
            import liveresolver
            url=query
            resolved = liveresolver.resolve(url,cache_timeout=0)
        xbmc.Player().play(resolved)

elif mode[0] == 'live_sport':
    sources = os.listdir(AddonPath + '/resources/lib/sources/live_sport')
    sources.remove('__init__.py')
    for source in sources:
        if '.pyo' not in source and '__init__' not in source:
            try:
                source = source.replace('.py','')
                exec "from resources.lib.sources.live_sport import %s"%source
                info = eval(source+".info()")
                addon.add_item({'mode': 'open_live_sport', 'site': info.mode}, {'title': info.name}, img=icon_path(info.icon), fanart=fanart,is_folder=True)
            except:
                pass
    addon.end_of_directory()



elif mode[0] == 'live_tv':
    sources = os.listdir(AddonPath + '/resources/lib/sources/live_tv')
    sources.remove('__init__.py')
    for source in sources:
        if '.pyo' not in source and '__init__' not in source:
            #try:
                source = source.replace('.py','')
                exec "from resources.lib.sources.live_tv import %s"%source
                info = eval(source+".info()")
                addon.add_item({'mode': 'open_live_tv', 'site': info.mode}, {'title': info.name}, img=icon_path(info.icon), fanart=fanart,is_folder=True)
            #except:
            #    pass
    addon.end_of_directory()


elif mode[0] == 'on_demand_sport_categories':
    addon.add_item({'mode': 'on_demand_sport', 'category':'football'}, {'title':'Football'}, img=icon_path('icons/soccer.png'), fanart=fanart,is_folder=True)
    addon.add_item({'mode': 'on_demand_sport', 'category':'basketball'}, {'title':'Basketball'}, img=icon_path('icons/basketball.png'), fanart=fanart,is_folder=True)
    addon.add_item({'mode': 'on_demand_sport', 'category':'american_football'}, {'title':'American Football'}, img=icon_path('icons/football.png'), fanart=fanart,is_folder=True)
    addon.add_item({'mode': 'on_demand_sport', 'category':'hockey'}, {'title':'Hockey'}, img=icon_path('icons/hockey.png'), fanart=fanart,is_folder=True)
    addon.add_item({'mode': 'on_demand_sport', 'category':'Other'}, {'title':'Other'}, img=icon_path('icons/tennis.png'), fanart=fanart,is_folder=True)

    addon.end_of_directory()

elif mode[0] == 'on_demand_sport':
    cat = args['category'][0]
    sources = os.listdir(AddonPath + '/resources/lib/sources/on_demand_sport/%s'%cat)
    sources.remove('__init__.py')
    for source in sources:
        if '.pyo' not in source and '__init__' not in source:
            #try:
                source = source.replace('.py','')
                exec "from resources.lib.sources.on_demand_sport.%s import %s"%(cat,source)
                info = eval(source+".info()")
                addon.add_item({'mode': 'open_demand_sport', 'site': info.mode, 'category':cat}, {'title': info.name}, img=icon_path(info.icon), fanart=fanart,is_folder=True)
            #except:
            #    pass
    addon.end_of_directory()

elif mode[0] == 'p2p_corner':
    sources = os.listdir(AddonPath + '/resources/lib/sources/p2p_sport')
    sources.remove('__init__.py')
    for source in sources:
        if '.pyo' not in source and '__init__' not in source:
            try:
                source = source.replace('.py','')
                exec "from resources.lib.sources.p2p_sport import %s"%source
                info = eval(source+".info()")
                addon.add_item({'mode': 'open_p2p_sport', 'site': info.mode}, {'title': info.name}, img=icon_path(info.icon), fanart=fanart,is_folder=True)
            except:
                pass
    addon.end_of_directory()













elif mode[0] == 'open_live_sport':
    
    site = args['site'][0]
    try:
        next_page = args['next'][0]
    except:
        next_page = None
    exec "from resources.lib.sources.live_sport import %s"%site
    info = eval(site+".info()")
    if not info.categorized:
        if next_page:
            source = eval(site+".main(url=next_page)")
        else:
            source = eval(site+".main()")
        events = source.events()
        for event in events:
            if not info.multilink:
                browser = 'plugin://plugin.program.chrome.launcher/?url=%s&mode=showSite&stopPlayback=no'%(event[0])
                context = [('Open in browser','RunPlugin(%s)'%browser)]
                addon.add_video_item({'mode': 'play_special_sport', 'url': event[0], 'title':event[1], 'img': icon_path(info.icon),'site':site}, {'title': event[1]}, img=icon_path(info.icon), fanart=fanart, contextmenu_items=context)
            else:
                addon.add_item({'mode': 'get_sport_event','site':site, 'url': event[0], 'title':event[1], 'img': icon_path(info.icon)}, {'title': event[1]}, img=icon_path(info.icon), fanart=fanart,is_folder=True)
        if (info.paginated and source.next_page()):
            addon.add_item({'mode': 'open_live_sport', 'site': info.mode, 'next' : source.next_page()}, {'title': 'Next Page >>'}, img=icon_path(info.icon), fanart=fanart,is_folder=True)

    else:
        source = eval(site+".main()")
        categories  = source.categories()
        for cat in categories:
            addon.add_item({'mode': 'open_sport_cat', 'url': cat[0], 'site': info.mode}, {'title': cat[1]}, img=icon_path(cat[2]), fanart=fanart,is_folder=True)

    addon.end_of_directory()




elif mode[0] == 'open_live_tv':
    
    site = args['site'][0]
    try:
        next_page = args['next'][0]
    except:
        next_page = None
    exec "from resources.lib.sources.live_tv import %s"%site
    info = eval(site+".info()")
    
    if not info.categorized:
        if next_page:
            source = eval(site+".main(url=next_page)")
        else:
            source = eval(site+".main()")
        channels = source.channels()
        try: special = info.special
        except: special = False
        for channel in channels:
            if not info.multilink:
                browser = 'plugin://plugin.program.chrome.launcher/?url=%s&mode=showSite&stopPlayback=no'%(channel[0])
                context = [('Open in browser','RunPlugin(%s)'%browser)]
                if not special:
                    addon.add_video_item({'mode': 'play_special', 'url': channel[0], 'title': channel[1], 'img':channel[2], 'site': site}, {'title': channel[1]}, img=channel[2], fanart=fanart, contextmenu_items=context)
                else:
                    addon.add_item({'mode': 'play_folder', 'url': channel[0], 'title': channel[1], 'img':channel[2], 'site': site}, {'title': channel[1]}, img=channel[2], fanart=fanart, contextmenu_items=context,is_folder=True)

            else:

                addon.add_item({'mode': 'get_tv_event', 'url': channel[0],'site':site , 'title':channel[1], 'img': channel[2]}, {'title': channel[1]}, img=channel[2], fanart=fanart,is_folder=True)

        if (info.paginated and source.next_page()):
            addon.add_item({'mode': 'open_live_tv', 'site': info.mode, 'next' : source.next_page()}, {'title': 'Next Page >>'}, img=icon_path(info.icon), fanart=fanart,is_folder=True)
    else:
        source = eval(site+".main()")
        categories  = source.categories()
        for cat in categories:
            thumb = cat[2]
            if not 'http' in thumb:
                thumb = icon_path(thumb)
            addon.add_item({'mode': 'open_tv_cat', 'url': cat[0], 'site': info.mode}, {'title': cat[1]}, img=thumb, fanart=fanart, is_folder=True)


    addon.end_of_directory()

elif mode[0] == 'open_p2p_sport':
    
    site = args['site'][0]
    try:
        next_page = args['next'][0]
    except:
        next_page = None
    exec "from resources.lib.sources.p2p_sport import %s"%site
    info = eval(site+".info()")
    if not info.categorized:
        if next_page:
            source = eval(site+".main(url=next_page)")
        else:
            source = eval(site+".main()")
        channels = source.channels()
        for event in channels:
            if not info.multilink:
                browser = 'plugin://plugin.program.chrome.launcher/?url=%s&mode=showSite&stopPlayback=no'%(event[0])
                context = [('Open in browser','RunPlugin(%s)'%browser)]
                addon.add_video_item({'mode': 'play_p2p', 'url': event[0],'title':event[1], 'img': event[2], 'site':site}, {'title': event[1]}, img=event[2], fanart=fanart, contextmenu_items=context)
            else:
                addon.add_item({'mode': 'get_p2p_event', 'url': event[0],'site':site , 'title':event[1], 'img': event[2]}, {'title': event[1]}, img=event[2], fanart=fanart,is_folder=True)
    
        if (info.paginated and source.next_page()):
            addon.add_item({'mode': 'open_p2p_sport', 'site': info.mode, 'next' : source.next_page()}, {'title': 'Next Page >>'}, img=icon_path(info.icon), fanart=fanart,is_folder=True)
    else:
        source = eval(site+".main()")
        categories  = source.categories()
        for cat in categories:
            from resources.lib.modules import constants
            adult = False
            for a in constants.adult:
                if a in cat[1].lower():
                    adult = True
            from resources.lib.modules import parental
            parent = parental.Parental()
            if not adult or parent.isVisible():
                addon.add_item({'mode': 'open_p2p_cat', 'url': cat[0], 'site': info.mode, 'adult':adult}, {'title': cat[1]}, img=icon_path(cat[2]), fanart=fanart,is_folder=True)

    addon.end_of_directory()








elif mode[0]=='open_p2p_cat':
    
    url = args['url'][0]
    site = args['site'][0]
    adult = args['adult'][0]=='True'
    exec "from resources.lib.sources.p2p_sport import %s"%site
    info = eval(site+".info()")
    source = eval(site+".main()")
    channels = source.channels(url)
    from resources.lib.modules import parental
    par = parental.Parental()
    par_enabled = par.isEnabled()
    correct = True
    if adult and par_enabled:
        correct = par.promptPassword()

    if correct or not adult:
        for event in channels:
            if not info.multilink:
                browser = 'plugin://plugin.program.chrome.launcher/?url=%s&mode=showSite&stopPlayback=no'%(event[0])
                context= [('Open in browser','RunPlugin(%s)'%browser)]
                addon.add_video_item({'mode': 'play_p2p', 'url': event[0],'title':event[1], 'img': event[2], 'site':site}, {'title': event[1]}, img=event[2], fanart=fanart,contextmenu_items=context)
            else:
                addon.add_item({'mode': 'get_p2p_event', 'url': event[0],'site':site , 'title':event[1], 'img': event[2]}, {'title': event[1]}, img=event[2], fanart=fanart,is_folder=True)
        
        if (info.paginated and source.next_page()):
            addon.add_item({'mode': 'open_p2p_cat', 'site': info.mode, 'url': source.next_page()}, {'title': 'Next Page >>'}, img=icon_path(info.icon), fanart=fanart,is_folder=True)
        
        addon.end_of_directory()

elif mode[0] == 'open_demand_sport':
    
    cat = args['category'][0]
    site = args['site'][0]
    try:
        next_page = args['next'][0]
    except:
        next_page = None
    exec "from resources.lib.sources.on_demand_sport.%s import %s"%(cat,site)
    info = eval(site+".info()")
    if not info.categorized:
        if next_page:
            source = eval(site+".main(url=next_page)")
        else:
            source = eval(site+".main()")
        items = source.items()
        for item in items:
            if info.multilink:
                addon.add_item({'mode': 'open_od_item', 'url': item[1], 'title': item[0], 'img':item[2],'site': info.mode, 'category':cat}, {'title': item[0]}, img=item[2], fanart=fanart,is_folder=True)
            else:
                addon.add_item({'mode': 'play_od_item', 'url': item[1], 'title': item[0], 'img':item[2],'site': info.mode, 'category':cat}, {'title': item[0]}, img=item[2], fanart=fanart)

        if (info.paginated and source.next_page()):
            addon.add_item({'mode': 'open_demand_sport','site': info.mode, 'next' : source.next_page(), 'category':cat}, {'title': 'Next Page >>'}, img=icon_path(info.icon), fanart=fanart,is_folder=True)
    else:
        source = eval(site+".main()")
        categories  = source.categories()
        for c in categories:
            addon.add_item({'mode': 'open_demand_cat', 'url': c[0], 'site': info.mode, 'category':cat}, {'title': c[1]}, img=icon_path(c[2]), fanart=fanart,is_folder=True)


    addon.end_of_directory()

elif mode[0] == 'open_demand_cat':
    
    site = args['site'][0]
    url = args['url'][0]
    cat = args['category'][0]
    try:
        next_page = args['next'][0]
    except:
        next_page = None
    exec "from resources.lib.sources.on_demand_sport.%s import %s"%(cat,site)
    info = eval(site+".info()")
    if next_page:
        source = eval(site+".main(url=next_page)")
    else:
        source = eval(site+".main(url=url)")
    items = source.items()
    for item in items:
        if info.multilink:
            addon.add_item({'mode': 'open_od_item', 'url': item[1], 'title': item[0], 'img':item[2],'site': info.mode, 'category':cat}, {'title': item[0]}, img=item[2], fanart=fanart,is_folder=True)
        else:
            addon.add_item({'mode': 'play_od_item', 'url': item[1], 'title': item[0], 'img':item[2],'site': info.mode, 'category':cat}, {'title': item[0]}, img=item[2], fanart=fanart)

    if (info.paginated and source.next_page()):
        addon.add_item({'mode': 'open_demand_cat', 'url': source.next_page(), 'site': info.mode, 'next' : source.next_page(), 'category':cat}, {'title': 'Next Page >>'}, img=icon_path(info.icon), fanart=fanart,is_folder=True)


    addon.end_of_directory()


elif mode[0]=='open_tv_cat':
    url = args['url'][0]
    site = args['site'][0]
    exec "from resources.lib.sources.live_tv import %s"%site
    info = eval(site+".info()")
    source = eval(site+".main()")
    channels = source.channels(url)

    for event in channels:
        if not info.multilink:
            browser = 'plugin://plugin.program.chrome.launcher/?url=%s&mode=showSite&stopPlayback=no'%(event[0])
            context = [('Open in browser','RunPlugin(%s)'%browser)]
            addon.add_video_item({'mode': 'play_special', 'url': event[0],'title':event[1],'site':site, 'img': event[2]}, {'title': event[1]}, img=event[2], fanart=fanart, contextmenu_items=context)
        else:
            addon.add_item({'mode': 'get_tv_event', 'url': event[0],'site':site , 'title':event[1], 'img': event[2]}, {'title': event[1]}, img=event[2], fanart=fanart,is_folder=True)
    
    if (info.paginated and source.next_page()):
        addon.add_item({'mode': 'open_tv_cat', 'site': info.mode, 'url': source.next_page()}, {'title': 'Next Page >>'}, img=icon_path(info.icon), fanart=fanart,is_folder=True)
    
    addon.end_of_directory()


elif mode[0]=='open_sport_cat':
    url = args['url'][0]
    site = args['site'][0]
    exec "from resources.lib.sources.live_sport import %s"%site
    info = eval(site+".info()")
    source = eval(site+".main()")
    events = source.events(url)
    for event in events:
        if not info.multilink:
            browser = 'plugin://plugin.program.chrome.launcher/?url=%s&mode=showSite&stopPlayback=no'%(event[0])
            context = [('Open in browser','RunPlugin(%s)'%browser)]
            addon.add_video_item({'mode': 'play_special_sport', 'url': event[0],'title':event[1], 'img': icon_path(info.icon),'site':site}, {'title': event[1]}, img=icon_path(info.icon), fanart=fanart, contextmenu_items=context)
        else:
            addon.add_item({'mode': 'get_sport_event', 'url': event[0],'site':site , 'title':event[1], 'img': icon_path(info.icon)}, {'title': event[1]}, img=icon_path(info.icon), fanart=fanart,is_folder=True)
    if (info.paginated and source.next_page()):
        addon.add_item({'mode': 'open_cat', 'site': info.mode, 'url': source.next_page()}, {'title': 'Next Page >>'}, img=icon_path(info.icon), fanart=fanart,is_folder=True)
    
    addon.end_of_directory()


elif mode[0]=='open_od_item':
    
    url = args['url'][0]
    title = args['title'][0]
    site = args['site'][0]
    img = args['img'][0]
    cat = args['category'][0]
    exec "from resources.lib.sources.on_demand_sport.%s import %s"%(cat,site)
    info = eval(site+".info()")
    source = eval(site+".main()")
    links = source.links(url)
    for link in links:
        addon.add_item({'mode': 'play_od_item', 'url': link[1], 'title': title, 'img':img,'site': info.mode, 'category':cat}, {'title': link[0]}, img=img, fanart=fanart)
    addon.end_of_directory()




elif mode[0]=='get_sport_event':
    
    url = args['url'][0]
    title = args['title'][0]
    site = args['site'][0]
    img = args['img'][0]
    exec "from resources.lib.sources.live_sport import %s"%site
    info = eval(site+".info()")
    source = eval(site+".main()")
    events = source.links(url)

    autoplay = addon.get_setting('autoplay')
    if autoplay == 'false':
        for event in events:
            browser = 'plugin://plugin.program.chrome.launcher/?url=%s&mode=showSite&stopPlayback=no'%(event[0])
            context = [('Open in browser','RunPlugin(%s)'%browser)]
            addon.add_video_item({'mode': 'play_special_sport', 'url': event[0],'title':title, 'img': img,'site':site}, {'title': event[1]}, img=img, fanart=fanart, contextmenu_items=context)
        addon.end_of_directory()
    else:
        for event in events:
            import liveresolver
            try:
                resolved = liveresolver.resolve(event[0])
            except:
                resolved = None
            if resolved:
                player=xbmc.Player()
                li = xbmcgui.ListItem(title)
                li.setThumbnailImage(img)
                player.play(resolved,listitem=li)
                break
        control.infoDialog("No stream found")

elif mode[0]=='get_tv_event':
    
    url = args['url'][0]
    title = args['title'][0]
    site = args['site'][0]
    img = args['img'][0]
    exec "from resources.lib.sources.live_tv import %s"%site
    info = eval(site+".info()")
    source = eval(site+".main()")
    events = source.links(url)

    autoplay = addon.get_setting('autoplay')
    if autoplay == 'false':
        for event in events:
            browser = 'plugin://plugin.program.chrome.launcher/?url=%s&mode=showSite&stopPlayback=no'%(event[0])
            context = [('Open in browser','RunPlugin(%s)'%browser)]
            addon.add_video_item({'mode': 'play_special', 'url': event[0],'title':title, 'img': img, 'site':site}, {'title': event[1]}, img=img, fanart=fanart, contextmenu_items=context)
        addon.end_of_directory()
    else:
        for event in events:
            import liveresolver
            try:
                resolved = liveresolver.resolve(event[0])
            except:
                resolved = None
            if resolved:
                player=xbmc.Player()
                li = xbmcgui.ListItem(title)
                li.setThumbnailImage(img)
                player.play(resolved,listitem=li)
                break
        control.infoDialog("No stream found")

elif mode[0]=='get_p2p_event':
    url = args['url'][0]
    title = args['title'][0]
    site = args['site'][0]
    img = args['img'][0]
    exec "from resources.lib.sources.p2p_sport import %s"%site
    info = eval(site+".info()")
    source = eval(site+".main()")
    events = source.links(url)

    for event in events:
        browser = 'plugin://plugin.program.chrome.launcher/?url=%s&mode=showSite&stopPlayback=no'%(event[0])
        context = [('Open in browser','RunPlugin(%s)'%browser)]
        addon.add_video_item({'mode': 'play_p2p', 'url': event[0],'title':title, 'img': img, 'site':site}, {'title': event[1]}, img=img, fanart=fanart, contextmenu_items=context)
    addon.end_of_directory()
    


elif mode[0] == 'play_p2p':
    #try:
        url = args['url'][0]
        title = args['title'][0]
        img = args['img'][0]
        site = args['site'][0]
        exec "from resources.lib.sources.p2p_sport import %s"%(site)
        source = eval(site+'.main()')
        resolved = source.resolve(url)
        li = xbmcgui.ListItem(title, path=resolved)
        li.setThumbnailImage(img)
        li.setLabel(title)
        handle = int(sys.argv[1])
        if handle > -1:
            xbmcplugin.endOfDirectory(handle, True, False, False)
        
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, li)
    #except:
    #    pass

elif mode[0] == 'play':
    try:
        url = args['url'][0]
        title = args['title'][0]
        img = args['img'][0]
        if url.endswith('.ts') or 'bit.ly' in url:
            resolved = url
        else:
            import liveresolver
            resolved = liveresolver.resolve(url,cache_timeout=0,title=title)
        li = xbmcgui.ListItem(title, path=resolved)
        li.setThumbnailImage(img)
        li.setLabel(title)
        li.setProperty('IsPlayable', 'true')
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, li)
    except:
        pass

elif mode[0] == 'play_special':
    #try:
        url = args['url'][0]
        title = args['title'][0]
        img = args['img'][0]
        site = args['site'][0]
        exec "from resources.lib.sources.live_tv import %s"%(site)
        source = eval(site+'.main()')
        resolved = source.resolve(url)
        li = xbmcgui.ListItem(title, path=resolved)
        li.setThumbnailImage(img)
        li.setLabel(title)
        handle = int(sys.argv[1])
        if handle > -1:
            xbmcplugin.endOfDirectory(handle, True, False, False)
        
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, li)
    #except:
    #    pass

elif mode[0] == 'play_folder':
    #try:
        url = args['url'][0]
        title = args['title'][0]
        img = args['img'][0]
        site = args['site'][0]
        exec "from resources.lib.sources.live_tv import %s"%(site)
        source = eval(site+'.main()')
        resolved = source.resolve(url)
        li = xbmcgui.ListItem(title, path=resolved)
        li.setThumbnailImage(img)
        li.setLabel(title)
        xbmc.Player().play(resolved, listitem=li)
    #except:
    #    pass

elif mode[0] == 'play_special_sport':
    #try:
        url = args['url'][0]
        title = args['title'][0]
        img = args['img'][0]
        site = args['site'][0]
        exec "from resources.lib.sources.live_sport import %s"%(site)
        source = eval(site+'.main()')
        resolved = source.resolve(url)
        li = xbmcgui.ListItem(title, path=resolved)
        li.setThumbnailImage(img)
        li.setLabel(title)
        li.setProperty('IsPlayable', 'true')
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, li)
    #except:
    #    pass


elif mode[0]=='play_od_item':
    #try:
        url = args['url'][0]
        title = args['title'][0]
        site = args['site'][0]
        img = args['img'][0]
        cat = args['category'][0]
        exec "from resources.lib.sources.on_demand_sport.%s import %s"%(cat,site)
        info = eval(site+".info()")
        source = eval(site+".main()")
        resolved = source.resolve(url)
        li = xbmcgui.ListItem(title, path=resolved)
        li.setThumbnailImage(img)
        li.setLabel(title)
        li.setProperty('IsPlayable', 'true')
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, li)
    #except:
    #    pass
       

########################################################################################################################################################################################################
########################################################################################################################################################################################################
########################################################################################################################################################################################################
####
####______________________________________________________________________________________________TOOLS_________________________________________________________________________________________________
####
########################################################################################################################################################################################################
########################################################################################################################################################################################################
########################################################################################################################################################################################################




elif mode[0]=='tools':
    addon.add_item({'mode': 'settings'}, {'title':'Settings'}, img=icon_path('tools.jpg'), fanart=fanart,is_folder=True)
    addon.add_item({'mode': 'addon_installer'}, {'title':'Install external addons'}, img=icon_path('tools.jpg'), fanart=fanart,is_folder=True)
    addon.add_item({'mode': 'parental'}, {'title':'Parental control'}, img=icon_path('tools.jpg'), fanart=fanart, is_folder=True)
    addon.add_item({'mode': 'clear_liveresolver_cache'}, {'title':'Clear Liveresolver cache'}, img=icon_path('tools.jpg'), fanart=fanart,is_folder=True)
    addon.add_item({'mode': 'x'}, {'title':'[COLOR yellow]Follow me @natko1412[/COLOR]'}, img=icon_path('twitter.png'), fanart=fanart)

    addon.end_of_directory()

elif mode[0]=='clear_liveresolver_cache':
    import liveresolver
    liveresolver.delete_cache()

elif mode[0]=='parental':
    from resources.lib.modules import parental
    parent = parental.Parental()
    parental_enabled = parent.isEnabled()
    adult_visible = parent.isVisible()

    title = 'Enable'
    tit = 'Parental protection disabled'
    color = 'red'
    if parental_enabled:
        tit = 'Parental protection enabled'
        title = 'Disable'
        color='green'

    tit2 = 'Adult content not visible'
    m2 = 'Show adult content'
    color2='green'
    if adult_visible:
        tit2 = 'Adult content visible'
        m2 = 'Hide adult content'
        color2 = 'red'

    addon.add_item({'mode': 'x'}, {'title':'[COLOR %s]%s[/COLOR] / [COLOR %s]%s[/COLOR]'%(color,tit,color2,tit2)}, img=icon_path('tools.jpg'), fanart=fanart)
    password_set = parent.isPasswordSet()
    addon.add_item({'mode': 'toggle_parental'}, {'title':title}, img=icon_path('tools.jpg'), fanart=fanart, is_folder=True)
    if password_set:
        addon.add_item({'mode': 'change_password'}, {'title':'Change password'}, img=icon_path('tools.jpg'), fanart=fanart, is_folder=True)
    else:
        addon.add_item({'mode': 'set_password'}, {'title':'Set password'}, img=icon_path('tools.jpg'), fanart=fanart, is_folder=True)

    addon.add_item({'mode': 'toggle_visible'}, {'title':m2}, img=icon_path('tools.jpg'), fanart=fanart, is_folder=True)    


    addon.end_of_directory()

elif mode[0]=='toggle_visible':
    from resources.lib.modules import parental
    parent = parental.Parental()
    parental_enabled = parent.isVisible()
    if parental_enabled:
        parent.setVisible(0)
    else:
        parent.setVisible(1)

elif mode[0]=='toggle_parental':
    from resources.lib.modules import parental
    parent = parental.Parental()
    parental_enabled = parent.isEnabled()
    if parental_enabled:
        parent.disable()
    else:
        parent.enable()

elif mode[0]=='set_password':
    from resources.lib.modules import parental
    parent = parental.Parental()
    parent.setPassword()

elif mode[0]=='change_password':
    from resources.lib.modules import parental
    parent = parental.Parental()
    parent.changePassword()


elif mode[0]=='settings':
    from resources.lib.modules import control
    control.openSettings()

elif mode[0]=='addon_installer':
    from resources.lib.modules import addonInstaller
    addons = addonInstaller.get_addons()
    for a in addons:
        addon.add_item({'mode': 'install', 'id':a[2], 'key':a[1], 'name':a[0]}, {'title': a[0], 'plot': 'Install addon'}, img=a[3], fanart=fanart, is_folder=True)

    addon.end_of_directory()

elif mode[0]=='install':
    id = args['id'][0]
    key = args['key'][0]
    name = args['name'][0]

    from resources.lib.modules import addonInstaller
    if not addonInstaller.isInstalled(id):
        addonInstaller.install(key)
    else:
        from resources.lib.modules import control
        control.infoDialog('%s already installed'%name)

elif mode[0]=='blogs':
    sources = os.listdir(AddonPath + '/resources/lib/sources/blogs')
    sources.remove('__init__.py')
    for source in sources:
        if '.pyo' not in source and '__init__' not in source:
            #try:
                source = source.replace('.py','')
                exec "from resources.lib.sources.blogs import %s"%source
                info = eval(source+".info()")
                addon.add_item({'mode': 'open_blog', 'site': info.mode}, {'title': info.name}, img=icon_path(info.icon), fanart=fanart,is_folder=True)
            #except:
            #    pass
    addon.end_of_directory()

############################################################################################################################################################################################################################################
############################################################################################################################################################################################################################################
############################################################################################################################################################################################################################################

elif mode[0]=='open_blog':
    site = args['site'][0]
    try:
        next_page = args['next'][0]
    except:
        next_page = None
    exec "from resources.lib.sources.blogs import %s"%site
    info = eval(site+".info()")
    
    if not info.categorized:
        if next_page:
            source = eval(site+".main(url=next_page)")
        else:
            source = eval(site+".main()")
        articles = source.articles()
        for channel in articles:
            browser = 'plugin://plugin.program.chrome.launcher/?url=%s&mode=showSite&stopPlayback=no'%(channel[0])
            context = [('Open in browser','RunPlugin(%s)'%browser)]
            addon.add_item({'mode': 'open_article', 'url': channel[0], 'title': channel[1], 'img':channel[2], 'site':site}, {'title': channel[1]}, img=channel[2], fanart=fanart, contextmenu_items=context,is_folder=True)


        if (info.paginated and source.next_page()):
            addon.add_item({'mode': 'open_blog', 'site': info.mode, 'next' : source.next_page()}, {'title': 'Next Page >>'}, img=icon_path(info.icon), fanart=fanart,is_folder=True)
    else:
        source = eval(site+".main()")
        categories  = source.categories()
        for cat in categories:
            thumb = cat[2]
            if not 'http' in thumb:
                thumb = icon_path(thumb)
            addon.add_item({'mode': 'open_blog_cat', 'url': cat[0], 'site': info.mode}, {'title': cat[1]}, img=thumb, fanart=fanart, is_folder=True)


    addon.end_of_directory()

elif mode[0]=='open_article':
    site = args['site'][0]
    url = args['url'][0]
    title = args['title'][0]
    img = args['img'][0]

    exec "from resources.lib.sources.blogs import %s"%site
    source = eval(site+".main()")

    text,video = source.content(url)
    from resources.lib.modules import blog_viewer as bv
    wind = bv.Viewer(title, image=img, text=text)
    wind.doModal()
    del wind

elif mode[0]=='bblogs':
    from resources.lib.modules import blog_viewer as bv
    wind = bv.Viewer('My first window')
    wind.doModal()
    del wind

###########################################################################################
elif mode[0]=='my_lists':
    lists = myLists.getLists()
    for ls in lists:
        delete = addon.build_plugin_url({'mode':'remove_list','name':ls[0]})
        context = [('Remove list','RunPlugin(%s)'%delete)]
        addon.add_item({'mode': 'open_list', 'path':ls[1], 'name':ls[0]}, {'title': ls[0]}, img=icon_path('my_lists.jpg'), fanart=fanart, is_folder=True, contextmenu_items=context)
    addon.add_item({'mode':'add_list'},{'title':'[B][COLOR green]Add list...[/COLOR][/B]'},img=icon_path('my_lists.jpg'), fanart=fanart, is_folder=True)
    addon.end_of_directory()

elif mode[0]=='add_list':
    answ = control.yesnoDialog('Do you want to add local list or remote list?','', '' ,yeslabel='Remote',nolabel='Local')
    
    #remote
    if str(answ)=='1':
        path = control.get_keyboard('Enter list URL:')

        name = control.get_keyboard('Enter list title:')
        if path and name:
            good = client.request(path)
            if good:
                myLists.addList(name,path)
            else:
                control.infoDialog('Cannot connect to list.',heading='Castaway Lists')
        else:
            control.infoDialog('A problem occured. Try again!',heading='Castaway Lists')

    #local
    elif str(answ)=='0':
        path = control.dialog.browse(1,'Select your list:','files', '', False, False, 'canceled',False)
        canceled = path == 'canceled'
        if not canceled:
            name = control.get_keyboard('Enter list title:')
            if path and name:
                myLists.addList(name,path)

elif mode[0]=='remove_list':
    name = args['name'][0]
    myLists.removeList(name)
    control.refresh()        

elif mode[0]=='open_list':
    path = args['path'][0]
    items = myLists.getItems(path)
    for item in items:
            url = item[0]
            if url.endswith('.ts'):
                import liveresolver
                url = liveresolver.resolve(url,title= item[1])
                item = control.item(item[1],item[2])
                control.addItem(handle=addon_handle,url=url,listitem=item)
            else:
                addon.add_video_item({'mode': 'play_playlist', 'url': item[0],'title':item[1], 'img': item[2]}, {'title': item[1]}, img=item[2], fanart=fanart)
    addon.end_of_directory()

elif mode[0] == 'play_playlist':
    url = args['url'][0]
    title = args['title'][0]
    img = args['img'][0]
    if url.endswith('.ts'):
        import liveresolver
        resolved = liveresolver.resolve(url,cache_timeout=0,title=title)
    else:
        resolved = url

    li = xbmcgui.ListItem(title, path=resolved)
    li.setThumbnailImage(img)
    li.setLabel(title)
    li.setProperty('IsPlayable', 'true')
    if resolved.startswith('plugin'):
        control.execute("RunPlugin(%s)"%resolved)
    else:
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, li)
    


##################################################################################################################################
##################################################################################################################################

elif mode[0]=='reddit':
    from resources.lib.modules import subreddits
    items = subreddits.get_subreddits()
    for item in items:

        delete = addon.build_plugin_url({'mode':'delete_subreddit','reddit':item})
        context = [('Remove subreddit','RunPlugin(%s)'%delete)]
        addon.add_item({'mode': 'open_subreddit', 'reddit': item}, {'title': item}, img=icon_path('reddit.jpg'), fanart=fanart,contextmenu_items=context,is_folder=True)

    addon.add_item({'mode': 'add_subreddit'}, {'title': '[B][COLOR green]Add a subreddit[/COLOR][/B]'}, img=icon_path('reddit.jpg'), fanart=fanart)    
    addon.end_of_directory()
elif mode[0]=='add_subreddit':
    from resources.lib.modules import subreddits
    subreddits.add_subreddit()
    control.refresh()

elif mode[0]=='delete_subreddit':
    reddit = args['reddit'][0]
    from resources.lib.modules import subreddits
    subreddits.remove_subreddit(reddit)
    control.refresh()

elif mode[0]=='open_subreddit':
    reddit = args['reddit'][0]
    from resources.lib.modules import subreddits
    items = subreddits.events(reddit)
    for item in items:
        addon.add_item({'mode': 'open_subreddit_event', 'url': item[0]}, {'title': item[1]}, img=icon_path('reddit.jpg'), fanart=fanart,is_folder=True)
    addon.end_of_directory()

elif mode[0]=='open_subreddit_event':
    url = args['url'][0]
    from resources.lib.modules import subreddits
    items = subreddits.event_links(url)
    for event in items:
        browser = 'plugin://plugin.program.chrome.launcher/?url=%s&mode=showSite&stopPlayback=no'%(event[0])
        context = [('Open in browser','RunPlugin(%s)'%browser)]

        addon.add_video_item({'mode': 'play', 'url': event[0],'title':event[1], 'img': icon_path('reddit.jpg')}, {'title': event[1]}, img=icon_path('reddit.jpg'), fanart=fanart, contextmenu_items=context)
    addon.end_of_directory()

