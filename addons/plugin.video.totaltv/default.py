import sys
import urllib
import urlparse
import xbmcgui
import xbmcplugin
import xbmcaddon
import urllib2
import sqlite3
import re
import os
import json,time
from BeautifulSoup import BeautifulSoup as bs
from resources.modules.totaltv import *
import xbmcvfs,base64
try:
    from addon.common.addon import Addon
    from addon.common.net import Net
except:
    print 'Failed to import script.module.addon.common'
    xbmcgui.Dialog().ok("Total TV Import Failure", "Failed to import addon.common", "A component needed by Total TV is missing on your system", "Please visit www.tvaddons.ag for support")
try:
    from metahandler import metahandlers
except:
    print 'Failed to import script.module.metahandler'
    xbmcgui.Dialog().ok("Total TV Import Failure", "Failed to import addon.common", "A component needed by Total TV is missing on your system", "Please visit www.tvaddons.ag for support")
###########################################################################################################################################################
###########################################################################################################################################################
###########################################################################################################################################################
my_addon = xbmcaddon.Addon()
params=urlparse.parse_qs(sys.argv[2][1:])
addonID=xbmcaddon.Addon().getAddonInfo("id")
db_dir = xbmc.translatePath("special://profile/addon_data/"+addonID)
db_path = os.path.join(db_dir, 'favourites.db')
if not os.path.exists(db_dir):
    os.makedirs(db_dir)
db=sqlite3.connect(db_path)
addon = Addon('plugin.video.totaltv', sys.argv)
AddonPath = addon.get_path()
IconPath = AddonPath + "/resources/icons/new/"
downloadPath = addon.get_setting('download_folder')
def icon_path(filename):
    return IconPath + filename
###########################################################################################################################################################
###########################################################################################################################################################
###########################################################################################################################################################
def setView(content, viewType):
	if content:
		xbmcplugin.setContent(int(sys.argv[1]), content)
def get_links(url):
    domain='http://www.watchfree.to'
    my_addon = xbmcaddon.Addon()

    html=read_url(url)
    soup=bs(html)
    links=re.compile('<a href="(.+?)" rel="nofollow" title=".+?" target="_blank">').findall(html)
    out=[]
    ind=0
    for link in links:
        link = link.split('gtfo=')
        link = link[-1]
        link = base64.b64decode(link)
        out+=[link]
        ind=0
    return out
  
def get_month():
    import datetime
    now = datetime.datetime.now()
    out=[]
    for i in range(30):
        date=now - datetime.timedelta(hours=i*24)
        year=date.year
        day=date.day
        month=date.month
        name=date.strftime("%A")
        mnth=date.strftime("%B")
        out+=[[name,day,month,year,mnth]]
    return out

#borrowed from 1Channel by tknorris and modified
def get_dbid(title, season='', episode='', year=''):
    video_type='episode'
    dbid = 0
    filter = ''
    max_title_len_diff = 1000
    titleComp2 = re.sub('[^a-zA-Z0-9]+', '', title).lower()

    if video_type == 'episode':
        filter = '"filter": {"and":['
        if year: filter += '{"field": "year", "operator": "is", "value": "%s"},' % year
        filter += '{"field": "season", "operator": "is", "value": "%s"},' % season
        filter += '{"field": "episode", "operator": "is", "value": "%s"}]},' % episode
        json_string = '{"jsonrpc": "2.0", "id": 1, "method": "VideoLibrary.GetEpisodes", "params": {%s "properties": ["showtitle"], "limits": {"end": 10000}}}' % (filter)
        result_key = "episodes"
        id_key = "episodeid"
        title_key = "showtitle"
    result = xbmc.executeJSONRPC(json_string)
    resultObj = json.loads(result)
    if not ('result' in resultObj and result_key in resultObj['result']): return None
    for item in resultObj['result'][result_key]:
        titleComp1 = re.sub('[^a-zA-Z0-9]+', '', item[title_key]).lower()
        found_match = 0
        if len(titleComp1) > len(titleComp2):
            if titleComp2 in titleComp1: found_match = 1
        else:
            if titleComp1 in titleComp2: found_match = 1
        if found_match:
            title_len_diff = abs(len(titleComp1) - len(titleComp2))
            if title_len_diff <= max_title_len_diff:
                max_title_len_diff = title_len_diff
                if video_type == 'movie':
                    dbid = item[id_key]
                if video_type == 'episode':
                    dbid = item[id_key]
    if dbid:
        return dbid
    else:
        utils.log('Failed to recover dbid, type: %s, title: %s, season: %s, episode: %s' % (video_type, title, season, episode), xbmc.LOGDEBUG)
        return None

7
#Notify function from Eldorado's PFTV
def Notify(typeq, box_title, message, times='', line2='', line3=''):
     if box_title == '':
          box_title='Total TV Notification'
     if typeq == 'small':
          if times == '':
               times='5000'
          smallicon= icon_path('icon.png')
          addon.show_small_popup(title=box_title, msg=message, delay=int(times), image=smallicon)
     elif typeq == 'big':
          addon.show_ok_dialog(message, title=box_title)
     else:
          addon.show_ok_dialog(message, title=box_title)
def add_favourite_show(name, link, thumb):
    with db:
        cur = db.cursor()    
        cur.execute("begin") 
        cur.execute("create table if not exists Favourite_shows (Link TEXT,Title TEXT, Thumb TEXT )")    
        db.commit()
        cur.execute("SELECT Title,Link,Thumb from Favourite_shows WHERE Title = ? AND Link=? and Thumb=?", (name,link,thumb))
        data=cur.fetchall()
        if len(data)!=0:
            Notify('small', 'Favourite Already Exists', name + ' already exists in your Total TV favourites','')
            return
        
        cur.execute("INSERT INTO Favourite_shows(Link,Title, Thumb) VALUES (?,?, ?);",(link,name,thumb))
        db.commit()
        cur.close()
    Notify('small', 'Added to favourites', name + ' added to your Total TV favourites','')
    return
def get_favourite_shows():
    with db:
        cur = db.cursor()
        cur.execute("begin")   
        cur.execute("create table if not exists Favourite_shows (Title TEXT, Link TEXT, Thumb TEXT)")    
        db.commit()  
        cur.execute("SELECT Title,Link,Thumb FROM Favourite_shows")
        rows = cur.fetchall()
        cur.close()
        favs=[]
        for i in range (len(rows)):
            folder=rows[i]
            favs+=[folder]
    return favs
def add_search_query(query,type):
    with db:
        cur = db.cursor()    
        cur.execute("begin") 
        cur.execute("create table if not exists Search_history (type TEXT, query TEXT)")    
        db.commit()
        cur.execute("INSERT INTO Search_history(type,query) VALUES (?,?);",(type,query))
        db.commit()
        cur.close()
    return
def get_search_history(type):
    with db:
        cur = db.cursor()
        cur.execute("begin")    
        cur.execute("create table if not exists Search_history (type TEXT, query TEXT)")    
        db.commit() 
        cur.execute("SELECT query FROM Search_history WHERE type = ?",(type,))
        rows = cur.fetchall()
        cur.close()
        his=[]
        for i in range (len(rows)):
            folder=rows[i][0]
            his+=[folder]
    return his
def delete_history(type):
    cur = db.cursor()  
    cur.execute("begin")  
    cur.execute("DELETE FROM Search_history WHERE type = ?",(type,))
    db.commit()
    cur.close()

def delete_all_tv_favs():
    with db:
        cur = db.cursor()
        cur.execute("drop table if exists Favourite_shows")
        cur.close()
    return

def remove_tv_fav(title,link):
    cur = db.cursor()  
    cur.execute("begin")  
    cur.execute("DELETE FROM Favourite_shows WHERE Title = ? AND Link = ?",(title,link))
    db.commit()
    cur.close()

def add_tv_item(type,link,show_title,season,episode,meta=None,totalitems=0):
    seas=str(season.zfill(2))
    ep=str(episode.zfill(2))
    title='%s S%sE%s'%(show_title,seas,ep)

    title='%s %sx%s'%(show_title,season,episode)
    if type=='season':
        
        meta['title']='%sx%s .  %s'%(season,episode,meta['title'])
    elif 'new' in type:
        meta['title']='%s %sx%s'%(show_title,season,episode)
    contextMenuItems=[('Show Informations', 'XBMC.Action(Info)')]
                        
    if type!='new_iw':type='ep'

    addon.add_video_item({'type': type,'url': link,'title': title, 'season':season, 'episode':episode}, meta,contextmenu_items=contextMenuItems, context_replace=False,img=meta['cover_url'], fanart=meta['backdrop_url'], total_items=totalitems)

def make_art(meta):
    # default fanart to theme fanart
    art_dict = {'thumb': '', 'poster': '', 'fanart': '', 'banner': ''}

    # set the thumb & cover to the poster if it exists
    if 'cover_url' in meta:
        art_dict['thumb'] = meta['cover_url']
        art_dict['poster'] = meta['cover_url']
    # override the fanart with metadata if fanart is on and it exists and isn't blank
    if 'backdrop_url' in meta and meta['backdrop_url']: art_dict['fanart'] = meta['backdrop_url']
    if 'banner_url' in meta: art_dict['banner'] = meta['banner_url']
    return art_dict
###########################################################################################################################################################
###########################################################################################################################################################
###########################################################################################################################################################
addon = Addon('plugin.video.totaltv', sys.argv)
base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])
xbmcplugin.setContent(addon_handle, 'movies')
def build_url(query):
    return base_url + '?' + urllib.urlencode(query)
mode = args.get('mode', None)
play = addon.queries.get('play', '')
if play:
    import random
    resolved=None
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    link=dicti['url'][0]
    type=dicti['type'][0]
    title=dicti['title'][0]
    # season=dicti['season'][0]
    # episode=dicti['episode'][0]
    links=get_links(link)
 
    randomitem = []
    sources = []
    autoplay = my_addon.getSetting('autoplay')
    listmode = my_addon.getSetting('listplay')
	
 
    import urlresolver
    dp = xbmcgui.DialogProgress()
    dp.create("Opening", 'Please wait')
    dp.update(0)
    begin = time.time()
    nItem = 30
    count=0
    for i in range(len(links)):
		url=links[i]
		try:
			sources.append(url)
		except:pass    
    for link in links: randomitem.append([link])
    index = random.randrange(1, len(links))
    playrandom = randomitem[index][0]
    if listmode=='true':
       dialog = xbmcgui.Dialog()
       index = dialog.select('Choose a source:', sources)
       if index>-1:
            url=sources[index]
            import urlresolver
            resolved=urlresolver.HostedMediaFile(url).resolve()
            addon.resolve_url(resolved)
    elif autoplay=='true':
        for i in range(len(links)):
         count+=1
         progress = float(count) / float(len(links)) * 100  
         try:
            index = random.randrange(1, len(links))
            playrandom = randomitem[index][0]
            dp.update(int(progress), 'TRYING (random on): ', playrandom)
            resolved=urlresolver.HostedMediaFile(playrandom).resolve()
            if resolved:
				addon.resolve_url(resolved)
				break
            else:
                Notify('small', 'Link down: ', playrandom,'')
         except: pass  	
    elif autoplay=='false':
		    for url in links:
				count+=1
				progress = float(count) / float(len(links)) * 100  
				
				try:
					dp.update(int(progress), 'TRYING (random off): ', url)
					resolved=urlresolver.HostedMediaFile(url).resolve()
					if resolved:
						addon.resolve_url(resolved)
						xbmc.sleep(500)
						break
				except: pass

				# try:
					# index = random.randrange(1, len(links))
					# playrandom = randomitem[index][0]
					# resolved=urlresolver.HostedMediaFile(playrandom).resolve()
					# if resolved:
						# addon.resolve_url(resolved)
						# xbmc.sleep(500)
						# break
				# except: pass

###########################################################################################################################################################
###########################################################################################################################################################
#TV
###########################################################################################################################################################


elif mode is None :

    url = build_url({'mode': 'movies_index', 'foldername': 'favs'})
    li = xbmcgui.ListItem('Movies', iconImage=icon_path('TV_Shows.png'))
    li.setArt({ 'fanart':icon_path('fanart.jpg')})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'tv_index', 'foldername': 'favs'})
    li = xbmcgui.ListItem('TV Shows', iconImage=icon_path('TV_Shows.png'))
    li.setArt({ 'fanart':icon_path('fanart.jpg')})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
								
    url = build_url({'mode': 'fav_tv', 'foldername': 'favs'})
    li = xbmcgui.ListItem('Favourites', iconImage=icon_path('Favourites.png'))
    li.setArt({ 'fanart':icon_path('fanart.jpg')})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    # url = build_url({'mode': 'popular_today', 'foldername': 'shows','page': 1})
    # li = xbmcgui.ListItem('Most Popular', iconImage=icon_path('Popular.png'))
    # li.setArt({ 'fanart':icon_path('fanart.jpg')})
    # xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                # listitem=li, isFolder=True)

    # url = build_url({'mode': 'most_popular', 'foldername': 'shows', 'page': 1})
    # li = xbmcgui.ListItem('Latest Shows', iconImage=icon_path('Popular.png'))
    # li.setArt({ 'fanart':icon_path('fanart.jpg')})
    # xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                # listitem=li, isFolder=True)

    # url = build_url({'mode': 'genres_tv', 'foldername': 'shows'})
    # li = xbmcgui.ListItem('Genres', iconImage=icon_path('Genre.png'))
    # li.setArt({ 'fanart':icon_path('fanart.jpg')})
    # xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,listitem=li, isFolder=True)


    xbmcplugin.endOfDirectory(addon_handle)
elif mode[0]=='movies_index':
    url = build_url({'mode': 'popular_today_movies', 'foldername': 'shows','page': 1})
    li = xbmcgui.ListItem('Most Popular', iconImage=icon_path('Popular.png'))
    li.setArt({ 'fanart':icon_path('fanart.jpg')})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'most_popular_movies', 'foldername': 'shows', 'page': 1})
    li = xbmcgui.ListItem('Latest Movies', iconImage=icon_path('Popular.png'))
    li.setArt({ 'fanart':icon_path('fanart.jpg')})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'genres_movies', 'foldername': 'shows'})
    li = xbmcgui.ListItem('Genres', iconImage=icon_path('Genre.png'))
    li.setArt({ 'fanart':icon_path('fanart.jpg')})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,listitem=li, isFolder=True)
    
	
    url = build_url({'mode': 'search_movies_history', 'foldername': 'search'})
    li = xbmcgui.ListItem('Search', iconImage=icon_path('Search.png'))
    li.setArt({ 'fanart':icon_path('fanart.jpg')})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)
elif mode[0]=='tv_index':
    url = build_url({'mode': 'popular_today', 'foldername': 'shows','page': 1})
    li = xbmcgui.ListItem('Most Popular', iconImage=icon_path('Popular.png'))
    li.setArt({ 'fanart':icon_path('fanart.jpg')})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'most_popular', 'foldername': 'shows', 'page': 1})
    li = xbmcgui.ListItem('Latest Shows', iconImage=icon_path('Popular.png'))
    li.setArt({ 'fanart':icon_path('fanart.jpg')})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'genres_tv', 'foldername': 'shows'})
    li = xbmcgui.ListItem('Genres', iconImage=icon_path('Genre.png'))
    li.setArt({ 'fanart':icon_path('fanart.jpg')})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,listitem=li, isFolder=True)

    url = build_url({'mode': 'search_tv_history', 'foldername': 'search'})
    li = xbmcgui.ListItem('Search', iconImage=icon_path('Search.png'))
    li.setArt({ 'fanart':icon_path('fanart.jpg')})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)
elif mode[0]=='popular_today':
    shows=popular_today()
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    page=int(dicti['page'][0])
    
    my_addon = xbmcaddon.Addon()
    meta_setting = my_addon.getSetting('tv_metadata')

    if meta_setting!='false':
        setting=my_addon.getSetting('limit_shows')
        if setting=='false':
            first=0
            total=len(shows)
        else:

            limit = int(my_addon.getSetting('results_number'))
            first = (page-1)*limit
            total = (page)*limit
            if len(shows)<total:
                total=len(shows)
            if len(shows)<limit:
                first=0
                total=len(shows)
    else:
        first=0
        total=len(shows)
    for i in range(first,total):
        show=shows[i]
        url=show[0]
        show_title=show[1]
        show_year=show[2]
        show_title = re.sub('Watch','',show_title)
        try:
            fav_uri = build_url({'mode': 'add_tv_fav', 'show': show_title,'link': url, 'year':show_year})
        except:
            fav_uri = build_url({'mode': 'add_tv_fav', 'show': ((show_title).encode('ascii','ignore')),'link':url, 'year':show_year })
        context=[('Show Informations', 'XBMC.Action(Info)'), ('Add to Total TV favourites','RunPlugin(%s)'%fav_uri)]
        meta=None
        if meta_setting!='false':
            imdb_id=get_imdb(url)
            metaget=metahandlers.MetaData()             
            meta=metaget.get_meta('tvshow', show_title,imdb_id=imdb_id, year=show_year)
            meta['title']=meta['title'].encode('ascii','ignore')
            title='%s (%s)'%(show_title,show_year)
            meta['title']=title
        if meta==None:
            meta={}
            title='%s (%s)'%(show_title,show_year)
            meta['title']=title
            meta['name']=title
            meta['tvshowtitle']=show_title
            meta['cover_url']=icon_path('TV_Shows.png')
            meta['backdrop_url']=None
        if meta['cover_url']=='':
            meta['cover_url']=icon_path('TV_Shows.png')
        addon.add_directory({'mode': 'open_show', 'url': url,'title': show_title,  }, meta, contextmenu_items=context, context_replace=False, img=meta['cover_url'], fanart=meta['backdrop_url'], total_items=total-first)
    if meta_setting!='false' and (total+1)<len(shows):
        url = build_url({'mode': 'popular_today', 'foldername': 'shows', 'page': page+1})
        li = xbmcgui.ListItem('Next Page >>', iconImage=icon_path('Next.png'))
        li.setArt({ 'fanart':icon_path('fanart.jpg')})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)
elif mode[0]=='popular_today_movies':
    shows=popular_today_mov()
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    page=int(dicti['page'][0])
    
    my_addon = xbmcaddon.Addon()
    meta_setting = my_addon.getSetting('tv_metadata')

    if meta_setting!='false':
        setting=my_addon.getSetting('limit_shows')
        if setting=='false':
            first=0
            total=len(shows)
        else:

            limit = int(my_addon.getSetting('results_number'))
            first = (page-1)*limit
            total = (page)*limit
            if len(shows)<total:
                total=len(shows)
            if len(shows)<limit:
                first=0
                total=len(shows)
    else:
        first=0
        total=len(shows)
    for i in range(first,total):
        show=shows[i]
        url=show[0]
        show_title=show[1]
        show_year=show[2]
        show_title = re.sub('Watch','',show_title)
        try:
            fav_uri = build_url({'mode': 'add_tv_fav', 'show': show_title,'link': url, 'year':show_year})
        except:
            fav_uri = build_url({'mode': 'add_tv_fav', 'show': ((show_title).encode('ascii','ignore')),'link':url, 'year':show_year })
        context=[('Show Informations', 'XBMC.Action(Info)'), ('Add to Total TV favourites','RunPlugin(%s)'%fav_uri)]
        meta=None
        if meta_setting!='false':
            imdb_id=get_imdb(url)
            metaget=metahandlers.MetaData()             
            meta=metaget.get_meta('movie', show_title,imdb_id=imdb_id, year=show_year)
            meta['title']=meta['title'].encode('ascii','ignore')
            title='%s (%s)'%(show_title,show_year)
            meta['title']=title
        if meta==None:
            meta={}
            title='%s (%s)'%(show_title,show_year)
            meta['title']=title
            meta['name']=title
            meta['tvshowtitle']=show_title
            meta['cover_url']=icon_path('TV_Shows.png')
            meta['backdrop_url']=None
        if meta['cover_url']=='':
            meta['cover_url']=icon_path('TV_Shows.png')
        addon.add_directory({'mode': 'open_show', 'url': url,'title': show_title,  }, meta, contextmenu_items=context, context_replace=False, img=meta['cover_url'], fanart=meta['backdrop_url'], total_items=total-first)
    if meta_setting!='false' and (total+1)<len(shows):
        url = build_url({'mode': 'popular_today_movies', 'foldername': 'shows', 'page': page+1})
        li = xbmcgui.ListItem('Next Page >>', iconImage=icon_path('Next.png'))
        li.setArt({ 'fanart':icon_path('fanart.jpg')})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)
elif mode[0]=='most_popular':
    shows=most_popular()
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    page=int(dicti['page'][0])
    my_addon = xbmcaddon.Addon()
    meta_setting = my_addon.getSetting('tv_metadata')
    if meta_setting!='false':
        setting=my_addon.getSetting('limit_shows')
        if setting=='false':
            first=0
            total=len(shows)
        else:
            limit = int(my_addon.getSetting('results_number'))
            first = (page-1)*limit
            total = (page)*limit
            if len(shows)<total:
                total=len(shows)
            if len(shows)<limit:
                first=0
                total=len(shows)
    else:
        first=0
        total=len(shows)
    for i in range(first,total):
        show=shows[i]
        url=show[0]
        show_title=show[1]
        show_year=show[2]
        show_title = re.sub('Watch','',show_title)
        try:
            fav_uri = build_url({'mode': 'add_tv_fav', 'show': show_title,'link': url, 'year':show_year})
        except:
            fav_uri = build_url({'mode': 'add_tv_fav', 'show': ((show_title).encode('ascii','ignore')),'link':url , 'year':show_year})
        context=[('Show Informations', 'XBMC.Action(Info)'), ('Add to Total TV favourites','RunPlugin(%s)'%fav_uri)]
        meta=None
        if meta_setting!='false':
            imdb_id=get_imdb(url)
            metaget=metahandlers.MetaData()             
            meta=metaget.get_meta('tvshow', show_title,imdb_id=imdb_id, year=show_year)
            meta['title']=meta['title'].encode('ascii','ignore')
            title='%s (%s)'%(show_title,show_year)
            meta['title']=title
        if meta==None:
            meta={}
            title='%s (%s)'%(show_title,show_year)
            meta['title']=title
            meta['name']=title
            meta['tvshowtitle']=show_title
            meta['cover_url']=icon_path('TV_Shows.png')
            meta['backdrop_url']=None
        if meta['cover_url']=='':
            meta['cover_url']=icon_path('TV_Shows.png')
        addon.add_directory({'mode': 'open_show', 'url': url, 'title': show_title }, meta, contextmenu_items=context, context_replace=False, img=meta['cover_url'], fanart=meta['backdrop_url'], total_items=total-first)
    if meta_setting!='false' and (total+1)<len(shows):
        url = build_url({'mode': 'most_popular', 'foldername': 'shows', 'page': page+1})
        li = xbmcgui.ListItem('Next Page >>', iconImage=icon_path('Next.png'))
        li.setArt({ 'fanart':icon_path('fanart.jpg')})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)
elif mode[0]=='most_popular_movies':
    shows=most_popular_mov()
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    page=int(dicti['page'][0])
    my_addon = xbmcaddon.Addon()
    meta_setting = my_addon.getSetting('tv_metadata')
    if meta_setting!='false':
        setting=my_addon.getSetting('limit_shows')
        if setting=='false':
            first=0
            total=len(shows)
        else:
            limit = int(my_addon.getSetting('results_number'))
            first = (page-1)*limit
            total = (page)*limit
            if len(shows)<total:
                total=len(shows)
            if len(shows)<limit:
                first=0
                total=len(shows)
    else:
        first=0
        total=len(shows)
    for i in range(first,total):
        show=shows[i]
        url=show[0]
        show_title=show[1]
        show_year=show[2]
        show_title = re.sub('Watch','',show_title)
        try:
            fav_uri = build_url({'mode': 'add_tv_fav', 'show': show_title,'link': url, 'year':show_year})
        except:
            fav_uri = build_url({'mode': 'add_tv_fav', 'show': ((show_title).encode('ascii','ignore')),'link':url , 'year':show_year})
        context=[('Show Informations', 'XBMC.Action(Info)'), ('Add to Total TV favourites','RunPlugin(%s)'%fav_uri)]
        meta=None
        if meta_setting!='false':
            imdb_id=get_imdb(url)
            metaget=metahandlers.MetaData()             
            meta=metaget.get_meta('movie', show_title,imdb_id=imdb_id, year=show_year)
            meta['title']=meta['title'].encode('ascii','ignore')
            title='%s (%s)'%(show_title,show_year)
            meta['title']=title
        if meta==None:
            meta={}
            title='%s (%s)'%(show_title,show_year)
            meta['title']=title
            meta['name']=title
            meta['tvshowtitle']=show_title
            meta['cover_url']=icon_path('TV_Shows.png')
            meta['backdrop_url']=None
        if meta['cover_url']=='':
            meta['cover_url']=icon_path('TV_Shows.png')
        addon.add_directory({'mode': 'open_show', 'url': url, 'title': show_title }, meta, contextmenu_items=context, context_replace=False, img=meta['cover_url'], fanart=meta['backdrop_url'], total_items=total-first)
    if meta_setting!='false' and (total+1)<len(shows):
        url = build_url({'mode': 'most_popular_movies', 'foldername': 'shows', 'page': page+1})
        li = xbmcgui.ListItem('Next Page >>', iconImage=icon_path('Next.png'))
        li.setArt({ 'fanart':icon_path('fanart.jpg')})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)
elif mode[0]=='open_show':
	try:
		dicti=urlparse.parse_qs(sys.argv[2][1:])
		url=dicti['url'][0]
		show=dicti['title'][0]
		my_addon = xbmcaddon.Addon()
		meta_setting = my_addon.getSetting('tv_metadata')
		imdb_id,seasons=get_seasons(url)
		total=len(seasons)
		if meta_setting!='false':
			ses=[]
			for item in seasons:
				season_list = []
				season_list.append(item)
				ses+=[int(item[1])]
				metaget=metahandlers.MetaData()
				try:
					meta=metaget.get_seasons(show, imdb_id,ses)
				except: meta=metaget.get_seasons(show, '',ses)
		else:
			meta=[]
			for i in range(total):
				meta.append({})
				meta[i]['season']=seasons[i][1]
				meta[i]['backdrop_url']=''
				meta[i]['cover_url']=''

		for i in range(len(meta)):
			metas=meta[i]
			metas['title'] = 'Season ' + str(metas['season'])
			addon.add_directory({'mode': 'open_season', 'url': 'http://www.watchfree.to' + seasons[i][0],'num':seasons[i][1], 'show': show }, metas, img=metas['backdrop_url'], fanart=metas['backdrop_url'], total_items=total)
		xbmcplugin.endOfDirectory(addon_handle)
	except:
		dicti=urlparse.parse_qs(sys.argv[2][1:])
		url=dicti['url'][0]
		show=dicti['title'][0]
		imdb_id=get_imdb(url)
		metaget=metahandlers.MetaData() 
		meta=metaget.get_meta('tvshow', show, imdb_id=imdb_id)
		meta['title']=meta['title'].encode('ascii','ignore')
		title='%s'%(show)
		meta['title']=title
		if meta['cover_url']=='': meta['cover_url']=icon_path('TV_Shows.png')
		if meta['backdrop_url']=='': meta['backdrop_url']=icon_path('fanart.jpg')	
		season = 1
		episode = 1
		total = 1
		addon.add_video_item({'type': 'episode','url': 'http://www.watchfree.to' + url,'title': show, 'season':season, 'episode':episode}, meta, context_replace=False,img=meta['cover_url'], fanart=meta['backdrop_url'], total_items=total)
		# add_tv_item('season','http://www.watchfree.to'+url,show,season,episode,meta=meta,totalitems=total)
		xbmcplugin.endOfDirectory(addon_handle)

 
elif mode[0]=='open_season':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    url=dicti['url'][0]
    show=dicti['show'][0]
    num=dicti['num'][0]
    my_addon = xbmcaddon.Addon()
    meta_setting = my_addon.getSetting('tv_metadata')
    imdb_id,episodes=get_episodes(url,num)
    total=len(episodes)
    show_title=show
    for item in episodes:
        url=item[0]
        ep_title=item[1]
        season=item[2]
        episode=item[3]
        meta=None
        if meta_setting!='false':
			metaget=metahandlers.MetaData()             
			try:
				meta=metaget.get_meta('tvshow', show_title)
			except: meta=metaget.get_episode_meta(ep_title, '', season, episode)
			if meta['title']=='': meta['title']=ep_title
			title='%s'%(ep_title)
			meta['title']=title    
        if meta==None:
            meta={}
            meta['imdb_id']=''
            meta['title']=ep_title
            meta['name']=''
            meta['tvshowtitle']=show_title
            meta['season']=season
            meta['episode']=episode
            meta['cover_url']=icon_path('TV_Shows.png')
            meta['backdrop_url']=None

        if meta['cover_url']=='':
            meta['cover_url']=icon_path('TV_Shows.png')
        add_tv_item('season','http://www.watchfree.to'+url,show_title,season,episode,meta=meta,totalitems=total)
    xbmcplugin.endOfDirectory(addon_handle)
    setView('episodes', 'episodes-view')

elif mode[0]=='add_tv_fav':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    name=dicti['show'][0]
    link=dicti['link'][0]
    thumb=dicti['year'][0]
    add_favourite_show(name,link,thumb)
elif mode[0]=='search_movies_history':
    url = build_url({'mode': 'search_movies', 'foldername': 'search'})
    li = xbmcgui.ListItem('[COLOR green]New Search[/COLOR]', iconImage=icon_path('Search.png'))
    
    li.setArt({ 'fanart':icon_path('fanart.jpg')})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    his=get_search_history('movies')
    for i in range(len(his)):
        url = build_url({'mode': 'open_movies_search', 'query': his[i], 'foldername': 'shows', 'page': 1})
        li = xbmcgui.ListItem(his[i], iconImage=icon_path('Search.png'))
        del_url = build_url({'mode': 'del_his_movies'})
        li.addContextMenuItems([('Erase search history','RunPlugin(%s)'%del_url)])
        li.setArt({ 'fanart':icon_path('fanart.jpg')})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                            listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)
	
elif mode[0]=='search_tv_history':
    url = build_url({'mode': 'search_tv', 'foldername': 'search'})
    li = xbmcgui.ListItem('[COLOR green]New Search[/COLOR]', iconImage=icon_path('Search.png'))
    
    li.setArt({ 'fanart':icon_path('fanart.jpg')})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    his=get_search_history('tv')
    for i in range(len(his)):
        url = build_url({'mode': 'open_tv_search', 'query': his[i], 'foldername': 'shows', 'page': 1})
        li = xbmcgui.ListItem(his[i], iconImage=icon_path('Search.png'))
        del_url = build_url({'mode': 'del_his_tv'})
        li.addContextMenuItems([('Erase search history','RunPlugin(%s)'%del_url)])
        li.setArt({ 'fanart':icon_path('fanart.jpg')})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                            listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)
elif mode[0]=='search_tv':
    keyboard = xbmc.Keyboard('', 'Search TV Shows', False)
    keyboard.doModal()
    if keyboard.isConfirmed():
        query = keyboard.getText()
        add_search_query(query,'tv')
        xbmc.executebuiltin("Container.Refresh")
        time.sleep(1.3)

        url = build_url({'mode': 'open_tv_search', 'query':query, 'foldername': 'shows', 'page': 1})
elif mode[0]=='search_movies':
    keyboard = xbmc.Keyboard('', 'Search Movies', False)
    keyboard.doModal()
    if keyboard.isConfirmed():
        query = keyboard.getText()
        add_search_query(query,'movies')
        xbmc.executebuiltin("Container.Refresh")
        time.sleep(1.3)

        url = build_url({'mode': 'open_movies_search', 'query':query, 'foldername': 'shows', 'page': 1})
elif mode[0]=='open_tv_search':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    query=dicti['query'][0]
    page=int(params['page'][0])
    shows=search(query)
    my_addon = xbmcaddon.Addon()
    meta_setting = my_addon.getSetting('tv_metadata')
    if meta_setting!='false':
        setting=my_addon.getSetting('limit_shows')
        if setting=='false':
            first=0
            total=len(shows)
        else:
            limit = int(my_addon.getSetting('results_number'))
            first = (page-1)*limit
            total = (page)*limit
            if len(shows)<total:
                total=len(shows)
            if len(shows)<limit:
                first=0
                total=len(shows)
    else:
        first=0
        total=len(shows)
    for i in range(first,total):
        show=shows[i]
        url=show[0]
        show_title=show[1]
        show_year=show[2]
        show_title = re.sub('Watch','',show_title)
        try:
            fav_uri = build_url({'mode': 'add_tv_fav', 'show': show_title,'link': url, 'year':show_year})
        except:
            fav_uri = build_url({'mode': 'add_tv_fav', 'show': ((show_title).encode('ascii','ignore')),'link':url , 'year':show_year})
        context=[('Show Informations', 'XBMC.Action(Info)'), ('Add to Total TV favourites','RunPlugin(%s)'%fav_uri)]
        meta=None
        if meta_setting!='false':
				imdb_id=get_imdb(url)
				metaget=metahandlers.MetaData()             
				try:meta=metaget.get_meta('tvshow', show_title,imdb_id=imdb_id, year=show_year)
				except: metaget.get_meta(show, imdb_id=imdb_id)
				try:
					
					title='%s (%s)'%(show_title,show_year)
					meta['title']=title
				except: pass
        if meta==None:
            meta={}
            title='%s (%s)'%(show_title,show_year)
            meta['title']=title
            meta['name']=title
            meta['tvshowtitle']=show_title
            meta['cover_url']=icon_path('TV_Shows.png')
            meta['backdrop_url']=None
        if meta['cover_url']=='':
            meta['cover_url']=icon_path('TV_Shows.png')
        addon.add_directory({'mode': 'open_show', 'url': url, 'title': show_title }, meta, contextmenu_items=context, context_replace=False, img=meta['cover_url'], fanart=meta['backdrop_url'], total_items=total-first)
    if meta_setting!='false' and (total+1)<len(shows):
        url = build_url({'mode': 'open_tv_search', 'query':query, 'foldername': 'shows', 'page': page+1})
        li = xbmcgui.ListItem('Next Page >>', iconImage=icon_path('Next.png'))
        li.setArt({ 'fanart':icon_path('fanart.jpg')})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)
    xbmcplugin.endOfDirectory(addon_handle)
elif mode[0]=='open_movies_search':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    query=dicti['query'][0]
    page=int(params['page'][0])
    shows=search_m(query)
    my_addon = xbmcaddon.Addon()
    meta_setting = my_addon.getSetting('tv_metadata')
    if meta_setting!='false':
        setting=my_addon.getSetting('limit_shows')
        if setting=='false':
            first=0
            total=len(shows)
        else:
            limit = int(my_addon.getSetting('results_number'))
            first = (page-1)*limit
            total = (page)*limit
            if len(shows)<total:
                total=len(shows)
            if len(shows)<limit:
                first=0
                total=len(shows)
    else:
        first=0
        total=len(shows)
    for i in range(first,total):
        show=shows[i]
        url=show[0]
        show_title=show[1]
        show_year=show[2]
        show_title = re.sub('Watch','',show_title)
        try:
            fav_uri = build_url({'mode': 'add_tv_fav', 'show': show_title,'link': url, 'year':show_year})
        except:
            fav_uri = build_url({'mode': 'add_tv_fav', 'show': ((show_title).encode('ascii','ignore')),'link':url , 'year':show_year})
        context=[('Show Informations', 'XBMC.Action(Info)'), ('Add to Total TV favourites','RunPlugin(%s)'%fav_uri)]
        meta=None
        if meta_setting!='false':
				imdb_id=get_imdb(url)
				metaget=metahandlers.MetaData()             
				try:meta=metaget.get_meta('movie', show_title,imdb_id=imdb_id, year=show_year)
				except: metaget.get_meta(show, imdb_id=imdb_id)
				try:
					
					title='%s (%s)'%(show_title,show_year)
					meta['title']=title
				except: pass
        if meta==None:
            meta={}
            title='%s (%s)'%(show_title,show_year)
            meta['title']=title
            meta['name']=title
            meta['tvshowtitle']=show_title
            meta['cover_url']=icon_path('TV_Shows.png')
            meta['backdrop_url']=None
        if meta['cover_url']=='':
            meta['cover_url']=icon_path('TV_Shows.png')
        addon.add_directory({'mode': 'open_show', 'url': url, 'title': show_title }, meta, contextmenu_items=context, context_replace=False, img=meta['cover_url'], fanart=meta['backdrop_url'], total_items=total-first)
    if meta_setting!='false' and (total+1)<len(shows):
        url = build_url({'mode': 'open_movies_search', 'query':query, 'foldername': 'shows', 'page': page+1})
        li = xbmcgui.ListItem('Next Page >>', iconImage=icon_path('Next.png'))
        li.setArt({ 'fanart':icon_path('fanart.jpg')})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)
    xbmcplugin.endOfDirectory(addon_handle)
###########################################################################################################################################################
###########################################################################################################################################################
###########################################################################################################################################################
elif mode[0]=='fav_tv':
    shows=get_favourite_shows()
    my_addon = xbmcaddon.Addon()
    meta_setting = my_addon.getSetting('tv_metadata')
    total=len(shows)
    for i in range(total):
        show=shows[i]
        url=show[1]
        show_title=show[0]
        show_year=show[2]
        try:
            del_uri = build_url({'mode': 'del_show_fav', 'title':show_title,  'link':url})
        except:
            del_uri = build_url({'mode': 'del_show_fav', 'title':show_title.encode('ascii','ignore'),'link':url})
        del_all = build_url({'mode': 'del_tv_all'})
        context=[('Show Informations', 'XBMC.Action(Info)'),
                    ('Remove from Total TV favourites','RunPlugin(%s)'%del_uri),
                    ('Remove all Total TV favourites','RunPlugin(%s)'%del_all)]
        meta=None
        if meta_setting!='false':
            if url[0]!='/' and 'http' not in url:
                url='/'+url
            imdb_id=get_imdb(url)
            metaget=metahandlers.MetaData()             
            meta=metaget.get_meta('tvshow', show_title,imdb_id=imdb_id, year=show_year)
            meta['title']=meta['title'].encode('ascii','ignore')
            title='%s (%s)'%(show_title,show_year)
            meta['title']=title
        if meta==None:
            meta={}
            title='%s (%s)'%(show_title,show_year)
            meta['title']=title
            meta['name']=title
            meta['tvshowtitle']=show_title
            meta['cover_url']=icon_path('TV_Shows.png')
            meta['backdrop_url']=None
        if meta['cover_url']=='':
            meta['cover_url']=icon_path('TV_Shows.png')
        addon.add_directory({'mode': 'open_show', 'url': url,'title': show_title, }, meta, contextmenu_items=context, context_replace=False, img=meta['cover_url'], fanart=meta['backdrop_url'], total_items=total)
    xbmcplugin.endOfDirectory(addon_handle)
elif mode[0]=='genres_tv':
    genre=get_genres()
    for i in range(len(genre)):
        url = build_url({'mode': 'open_letter', 'letter':genre[i][0],'page':'1'})
        li = xbmcgui.ListItem(genre[i][1], iconImage=icon_path('Genre.png'))
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)
elif mode[0]=='genres_movies':
    genre=get_genres_mov()
    for i in range(len(genre)):
        url = build_url({'mode': 'open_letter_movies', 'letter':genre[i][0],'page':'1'})
        li = xbmcgui.ListItem(genre[i][1], iconImage=icon_path('Genre.png'))
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)
elif mode[0]=='open_letter':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    letter=dicti['letter'][0]

    shows=get_shows_letter(letter)

    page=int(params['page'][0])
    
    my_addon = xbmcaddon.Addon()
    meta_setting = my_addon.getSetting('tv_metadata')

    if meta_setting!='false':
        setting=my_addon.getSetting('limit_shows')
        if setting=='false':
            first=0
            total=len(shows)
        else:

            limit = int(my_addon.getSetting('results_number'))
            first = (page-1)*limit
            total = (page)*limit
            if len(shows)<total:
                total=len(shows)
            if len(shows)<limit:
                first=0
                total=len(shows)
    else:
        first=0
        total=len(shows)

    for i in range(first,total):
        show=shows[i]
        url=show[0]
        show_title=show[1]
        show_title = re.sub('Watch ','',show_title)
        show_title = re.sub('Watch','',show_title)
        show_year=show[2]
        try:
            fav_uri = build_url({'mode': 'add_tv_fav', 'show': show_title,'link': url, 'year':show_year})
        except:
            fav_uri = build_url({'mode': 'add_tv_fav', 'show': ((show_title).encode('ascii','ignore')),'link':url, 'year':show_year })

        
        context=[('Show Informations', 'XBMC.Action(Info)'), ('Add to Total TV favourites','RunPlugin(%s)'%fav_uri)]
        meta=None
        if meta_setting!='false':
            imdb_id=get_imdb(url)
            metaget=metahandlers.MetaData()             
            meta=metaget.get_meta('tvshow', show_title,imdb_id=imdb_id, year=show_year)
            
            meta['title']=meta['title'].encode('ascii','ignore')
            title='%s (%s)'%(show_title,show_year)
            meta['title']=title
            
        if meta==None:
            meta={}
            title='%s (%s)'%(show_title,show_year)
            meta['title']=title
            meta['name']=title
            meta['tvshowtitle']=show_title
            meta['cover_url']=icon_path('TV_Shows.png')
            meta['backdrop_url']=None

        if meta['cover_url']=='':
            meta['cover_url']=icon_path('TV_Shows.png')

        addon.add_directory({'mode': 'open_show', 'url': url, 'title': show_title }, meta, contextmenu_items=context, context_replace=False, img=meta['cover_url'], fanart=meta['backdrop_url'], total_items=total)
    
    if meta_setting!='false' and (total+1)<len(shows):
        url = build_url({'mode': 'open_letter','letter':letter, 'foldername': 'shows', 'page': page+1})
        li = xbmcgui.ListItem('Next Page >>', iconImage=icon_path('Next.png'))
        li.setArt({ 'fanart':icon_path('fanart.jpg')})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='open_letter_movies':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    letter=dicti['letter'][0]

    shows=get_shows_letter(letter)

    page=int(params['page'][0])
    
    my_addon = xbmcaddon.Addon()
    meta_setting = my_addon.getSetting('tv_metadata')

    if meta_setting!='false':
        setting=my_addon.getSetting('limit_shows')
        if setting=='false':
            first=0
            total=len(shows)
        else:

            limit = int(my_addon.getSetting('results_number'))
            first = (page-1)*limit
            total = (page)*limit
            if len(shows)<total:
                total=len(shows)
            if len(shows)<limit:
                first=0
                total=len(shows)
    else:
        first=0
        total=len(shows)

    for i in range(first,total):
        show=shows[i]
        url=show[0]
        show_title=show[1]
        show_title = re.sub('Watch ','',show_title)
        show_title = re.sub('Watch','',show_title)
        show_year=show[2]
        try:
            fav_uri = build_url({'mode': 'add_tv_fav', 'show': show_title,'link': url, 'year':show_year})
        except:
            fav_uri = build_url({'mode': 'add_tv_fav', 'show': ((show_title).encode('ascii','ignore')),'link':url, 'year':show_year })

        
        context=[('Show Informations', 'XBMC.Action(Info)'), ('Add to Total TV favourites','RunPlugin(%s)'%fav_uri)]
        meta=None
        if meta_setting!='false':
            imdb_id=get_imdb(url)
            metaget=metahandlers.MetaData()             
            meta=metaget.get_meta('movie', show_title,imdb_id=imdb_id, year=show_year)
            
            meta['title']=meta['title'].encode('ascii','ignore')
            title='%s (%s)'%(show_title,show_year)
            meta['title']=title
            
        if meta==None:
            meta={}
            title='%s (%s)'%(show_title,show_year)
            meta['title']=title
            meta['name']=title
            meta['tvshowtitle']=show_title
            meta['cover_url']=icon_path('TV_Shows.png')
            meta['backdrop_url']=None

        if meta['cover_url']=='':
            meta['cover_url']=icon_path('TV_Shows.png')

        addon.add_directory({'mode': 'open_show', 'url': url, 'title': show_title }, meta, contextmenu_items=context, context_replace=False, img=meta['cover_url'], fanart=meta['backdrop_url'], total_items=total)
    
    if meta_setting!='false' and (total+1)<len(shows):
        url = build_url({'mode': 'open_letter_movies','letter':letter, 'foldername': 'shows', 'page': page+1})
        li = xbmcgui.ListItem('Next Page >>', iconImage=icon_path('Next.png'))
        li.setArt({ 'fanart':icon_path('fanart.jpg')})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)

        

elif mode[0]=='del_show_fav':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    title=dicti['title'][0]
    link=dicti['link'][0] 
    remove_tv_fav(title,link) 
    xbmc.executebuiltin("Container.Refresh")

elif mode[0]=='del_tv_all':
    delete_all_tv_favs()
    xbmc.executebuiltin("Container.Refresh")

elif mode[0]=='del_his_tv':
    delete_history('tv')
    xbmc.executebuiltin("Container.Refresh")