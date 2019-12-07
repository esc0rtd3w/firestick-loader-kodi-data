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
from pftvso import *
import xbmcvfs
try:
    from addon.common.addon import Addon
    from addon.common.net import Net
except:
    print 'Failed to import script.module.addon.common'
    xbmcgui.Dialog().ok("PFTVso Import Failure", "Failed to import addon.common", "A component needed by PFTVso is missing on your system", "Please visit www.tvaddons.ag for support")

try:
    from metahandler import metahandlers
except:
    print 'Failed to import script.module.metahandler'
    xbmcgui.Dialog().ok("PFTV Import Failure", "Failed to import Metahandlers", "A component needed by PFTV is missing on your system", "Please visit www.tvaddons.ag for support")


###########################################################################################################################################################
###########################################################################################################################################################
###########################################################################################################################################################


addonID=xbmcaddon.Addon().getAddonInfo("id")
db_dir = xbmc.translatePath("special://profile/addon_data/"+addonID)
db_path = os.path.join(db_dir, 'favourites.db')
if not os.path.exists(db_dir):
    os.makedirs(db_dir)

db=sqlite3.connect(db_path)

addon = Addon('plugin.video.pftvso', sys.argv)
AddonPath = addon.get_path()
if xbmc.getCondVisibility('System.HasAddon(script.pftvso.themepak)'):
    themepak_path = xbmcaddon.Addon('script.pftvso.themepak').getAddonInfo('path')
else:
    themepak_path = AddonPath
my_addon = xbmcaddon.Addon()

themes=['Blue','Maccharm','PFTV','Simple']
try:theme= themes[int(addon.get_setting('theme'))]
except:theme='Blue'
    
IconPath = themepak_path + "/art/themes/%s/"%(theme)


downloadPath = addon.get_setting('download_folder')

def icon_path(filename):
    try:
        return IconPath + filename
    except:
        print('Problem with using themes occured. Contact the addon developer.')
        return ''


###########################################################################################################################################################
###########################################################################################################################################################
###########################################################################################################################################################







def download(name, url, type):
       
    agent = None
    referer = None
    cookie = None

    my_addon = xbmcaddon.Addon()

    downloadPath= my_addon.getSetting('download_folder')
    
    
    if downloadPath and downloadPath !='':
        if xbmcvfs.exists(downloadPath):
          tvpath=os.path.join(downloadPath, 'TV Shows', '')
          moviepath=os.path.join(downloadPath, 'Movies', '')
        if not xbmcvfs.exists(tvpath):
            xbmcvfs.mkdir(tvpath)
        if not xbmcvfs.exists(moviepath):
            xbmcvfs.mkdir(moviepath)

        if type=='movie':
            destination=moviepath
        else:
            destination=tvpath

        title=name
        name=re.sub('[^-a-zA-Z0-9_.() ]+', '', name)
        name=name.rstrip('.')
        filename=name + '.mp4'
        
        #dest = os.path.join(destination, name + '.mp4')

        #import commondownloader
        #commondownloader.download(url, dest, 'ProjectFreeTV.so', referer=referer, agent=agent, cookie=cookie)

        import SimpleDownloader as downloader
        downloader = downloader.SimpleDownloader()
        params = { "url": url, "download_path": destination, "Title": title }
        downloader.download(filename, params)



    else:
        xbmcgui.Dialog().ok("ProjectFreeTV.so", "You must set your download path!")
        xbmc.executebuiltin("Addon.OpenSettings(%s)"%addonID)



    
    

def get_linkss(url):
    my_addon = xbmcaddon.Addon()
    black = unicode(my_addon.getSetting('source_blacklist'))
    blacklist=black.split(',')

    white = unicode(my_addon.getSetting('source_whitelist'))
    whitelist=white.split(',')
    if len(whitelist)==1 and whitelist[0]=='':
        whitelist = None
    


    linksout=[]
    html=read_url(url)
    soup=bs(html)
    rows=soup.findAll('tr')
    a=2
    if 'movie' in url:
        a=3
    for i in range(a,len(rows)):
        row=rows[i]
        link=row.find('td').find('a')['href']
        h = HTMLParser.HTMLParser()
        dm=row.find('td').getText()
        domain=h.unescape(dm).strip()
        age=row.findAll('td')[2].getText().replace('days',' days').replace('1day','1 day')
        if whitelist is None:
            if 'movie' in url and domain not in blacklist:   
                linksout+=[[domain,link]]
            elif domain not in blacklist:
                linksout+=[[domain,link,age]]
        else:
            if domain in whitelist and 'movie' in url:
                linksout+=[[domain,link]]
            elif domain in whitelist:
                linksout+=[[domain,link,age]]
    return linksout

def sort_links(links):
    my_addon = xbmcaddon.Addon()
    sort=my_addon.getSetting('enable_sorting')
    black = unicode(my_addon.getSetting('source_blacklist'))
    blacklist=black.split(',')
    listout=[]
    if sort!='false':
        sorting=unicode(my_addon.getSetting('sort'))
        sort_list=sorting.split(',')

        for i in range(len(sort_list)):
            for j in range(len(links)):
                if sort_list[i]==links[j][0]:
                    listout.append(links[j])
        for k in range(len(links)):
            
            if links[k] not in listout and links[k][0] not in blacklist:
                listout.append(links[k])
        return listout

    else:
        return links


#Notify function from Eldorado's PFTV
def Notify(typeq, box_title, message, times='', line2='', line3=''):
     if box_title == '':
          box_title='PFTV.so Notification'
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
        cur.execute("SELECT Link,Title,Thumb from Favourite_shows WHERE  Link=? AND Title = ? AND Thumb=?", (link,name,thumb))
        data=cur.fetchall()
        if len(data)!=0:
            Notify('small', 'Favourite Already Exists', name + ' already exists in your PFTV.so favourites','')
            return
        cur.execute("INSERT INTO Favourite_shows(Link,Title, Thumb) VALUES (?,?, ?);",(link,name,thumb))
        db.commit()
        cur.close()
    Notify('small', 'Added to favourites', name + ' added to your PFTV.so favourites','')

    return
def add_favourite_movie(title,year,link,thumb):
    with db:
        cur = db.cursor()    
        cur.execute("begin") 
        cur.execute("create table if not exists Favourite_movies (Title TEXT, Year TEXT, Thumb TEXT, Link TEXT)")    
        db.commit()
        cur.execute("SELECT Title,Year,Thumb,Link from Favourite_movies WHERE Title = ? AND Year=? AND Thumb=? AND Link=?", (title,year,thumb,link))
        data=cur.fetchall()
        if len(data)!=0:
            Notify('small', 'Favourite Already Exists', title + ' already exists in your PFTV.so favourites','')
            return
        cur.execute("INSERT INTO Favourite_movies(Title,Year, Thumb,Link) VALUES (?,?,?,?);",(title, year, thumb,link))
        db.commit()
        cur.close()
    Notify('small', 'Added to favourites', title + ' added to your PFTV.so favourites','')
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
def get_favourite_movies():
    with db:
        cur = db.cursor()
        cur.execute("begin")    
        cur.execute("create table if not exists Favourite_movies (Title TEXT, Year TEXT, Thumb TEXT, Link TEXT)")    
        db.commit() 
        cur.execute("SELECT Title,Year,Thumb,Link FROM Favourite_movies")
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
def delete_all_movie_favs():
    with db:
        cur = db.cursor()
        cur.execute("drop table if exists Favourite_movies")
        cur.close()
    return

def delete_all_tv_favs():
    with db:
        cur = db.cursor()
        cur.execute("drop table if exists Favourite_shows")
        cur.close()
    return

def remove_movie_fav(title,year,thumb,link):
    cur = db.cursor()  
    cur.execute("begin")  
    cur.execute("DELETE FROM Favourite_movies WHERE Title = ? AND Year= ? AND Thumb = ? AND Link = ?",(title,year,thumb,link))
    db.commit()
    cur.close()

def remove_tv_fav(title,link):
    cur = db.cursor()  
    cur.execute("begin")  
    cur.execute("DELETE FROM Favourite_shows WHERE Title = ? AND Link = ?",(title,link))
    db.commit()
    cur.close()

def add_movie_item(link,thumb, title,meta=None, year='', fav='0',totalitems=0):
    try:
        if fav=='1':
            try:
                    del_uri = build_url({'mode': 'del_movie_fav', 'title':title, 'thumb':thumb , 'link':link, 'year':year})
                    down_uri = build_url({'mode': 'download', 'title':title,'link':link, 'type':'movie'})

            except:
                    del_uri = build_url({'mode': 'del_movie_fav', 'title':title.encode('ascii','ignore'), 'thumb':thumb , 'link':link, 'year':year})
                    down_uri = build_url({'mode': 'download', 'title':title.encode('ascii','ignore'),'link':link, 'type':'movie'})
            del_all=build_url({'mode': 'del_movie_all'})
            contextMenuItems = [('Movie Information', 'XBMC.Action(Info)'),
                    ('Remove from PFTV favourites','RunPlugin(%s)'%del_uri),
                    ('Remove all PFTV movie favourites','RunPlugin(%s)'%del_all),
                    ('Download','RunPlugin(%s)'%down_uri)]

        else:
            try:
                    fav_uri = build_url({'mode': 'add_movie_fav', 'title':title, 'thumb':thumb , 'link':link, 'year':year})
                    down_uri = build_url({'mode': 'download', 'title':title,'link':link, 'type':'movie'})

            except:
                    fav_uri = build_url({'mode': 'add_movie_fav', 'title':title.encode('ascii','ignore'), 'thumb':thumb , 'link':link, 'year':year})
                    down_uri = build_url({'mode': 'download', 'title':title.encode('ascii','ignore'),'link':link, 'type':'movie'})
            contextMenuItems = [('Movie Information', 'XBMC.Action(Info)'),
                    ('Add to PFTV favourites','RunPlugin(%s)'%fav_uri),
                    ('Download','RunPlugin(%s)'%down_uri)]

        if meta['backdrop_url']==None:
            meta['title']='%s (%s)'%(meta['title'],year)
        
        addon.add_video_item({'type':'movie','url': link,'title': title, 'year':year}, meta, contextmenu_items=contextMenuItems, context_replace=False, img=meta['cover_url'], fanart=meta['backdrop_url'], total_items=totalitems)
    except:
        pass

def add_tv_item(link,show_title,season,episode,meta=None,totalitems=0):
    seas=str(season.zfill(2))
    ep=str(episode.zfill(2))
    title='%s S%sE%s'%(show_title,seas,ep)
    try:
        down_uri = build_url({'mode': 'download', 'title':title,'link':link, 'type':'tv'})
        add_favourite_show_uri = build_url({'mode':'add_fav_from_ep', 'show': show_title, 'link':link })

    except:
        down_uri = build_url({'mode': 'download', 'title':title.encode('ascii','ignore'),'link':link, 'type':'tv'})
        add_favourite_show_uri = build_url({'mode':'add_fav_from_ep', 'show': show_title.encode('ascii','ignore'), 'link':link })

    title='%s: %sx%s'%(show_title,season,episode)
    if meta['title']!=title:
        
        meta['title']='%sx%s. %s'%(season,episode,meta['title'])
    contextMenuItems=[('Episode Information', 'XBMC.Action(Info)'),
                        ('Add show to favourites','RunPlugin(%s)'%add_favourite_show_uri),
                        ('Download','RunPlugin(%s)'%down_uri)]

    addon.add_video_item({'type':'ep','url': link,'title': title, 'season':season, 'episode':episode}, meta,contextmenu_items=contextMenuItems, context_replace=False,img=meta['cover_url'], fanart=meta['backdrop_url'], total_items=totalitems)






###########################################################################################################################################################
###########################################################################################################################################################
###########################################################################################################################################################
addon = Addon('plugin.video.pftvso', sys.argv)

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

xbmcplugin.setContent(addon_handle, 'movies')

def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

mode = args.get('mode', None)

play = addon.queries.get('play', '')





if play:
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    link=dicti['url'][0]
    type=dicti['type'][0]
    title=dicti['title'][0]
    links=get_linkss(link)
    links=sort_links(links)

    my_addon = xbmcaddon.Addon()
    autoplay = my_addon.getSetting('autoplay')
    if autoplay=='false':
        hosts=[]
        linky=[]
        if type=='movie':
            for i in range(len(links)):
                host=links[i][0]
                link=links[i][1]
                linky.append(link)

                hosts.append('%s.'%(i+1) +' '+host)

        elif type=='ep':
            for i in range(len(links)):
                host=links[i][0]
                link=links[i][1]
                age=links[i][2]
                linky.append(link)
                hosts.append('%s.'%(i+1) +' '+host + ' ('+age+')')

        dialog = xbmcgui.Dialog()
        index = dialog.select('Choose a source:', hosts)
        
        if index>-1:
            link=get_link(linky[index])
            print(link)
            import urlresolver
            resolved=urlresolver.resolve(link)

            if resolved:
                if my_addon.getSetting('axel') != 'false':
                    download_name = title
                    import axelproxy as proxy
                    axelhelper = proxy.ProxyHelper()
                    resolved, download_id = axelhelper.create_proxy_url(resolved, name=download_name)
                
                addon.resolve_url(resolved)
    else:
        import urlresolver
        from random import shuffle
        shuffle(links)
        for i in range(len(links)):
            link=get_link(links[i][1])
            resolved=urlresolver.resolve(link)

            if resolved:
                if my_addon.getSetting('axel') != 'false':
                    download_name = title
                    import axelproxy as proxy
                    axelhelper = proxy.ProxyHelper()
                    resolved, download_id = axelhelper.create_proxy_url(resolved, name=download_name)
                
                addon.resolve_url(resolved)
                break
           


    


if mode is None:
    url = build_url({'mode': 'movies', 'foldername': 'movies'})
    li = xbmcgui.ListItem('Movies', iconImage=icon_path('Movies.png'))
    li.setArt({ 'fanart':icon_path('fanart.jpg')})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'tv', 'foldername': 'shows'})
    li = xbmcgui.ListItem('TV Shows', iconImage=icon_path('TV_Shows.png'))
    li.setArt({ 'fanart':icon_path('fanart.jpg')})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'favs', 'foldername': 'favs'})
    li = xbmcgui.ListItem('Favourites', iconImage=icon_path('Favourites.png'))
    li.setArt({ 'fanart':icon_path('fanart.jpg')})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'search', 'foldername': 'search'})
    li = xbmcgui.ListItem('Search All', iconImage=icon_path('Search.png'))
    li.setArt({ 'fanart':icon_path('fanart.jpg')})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'settings'})
    li = xbmcgui.ListItem('Settings', iconImage=icon_path('Settings.png'))
    li.setArt({ 'fanart':icon_path('fanart.jpg')})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)



###########################################################################################################################################################
###########################################################################################################################################################
###########################################################################################################################################################


elif mode[0]=='movies':
    url = build_url({'mode': 'fav_movies', 'foldername': 'favs'})
    li = xbmcgui.ListItem('Favourites', iconImage=icon_path('Favourites.png'))
    li.setArt({ 'fanart':icon_path('fanart.jpg')})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'latest_movies', 'foldername': 'movies', 'page':'1'})
    li = xbmcgui.ListItem('Latest Added', iconImage=icon_path('Latest_Added.png'))
    li.setArt({ 'fanart':icon_path('fanart.jpg')})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'movies_genre', 'foldername': 'movies'})
    li = xbmcgui.ListItem('Genre', iconImage=icon_path('Genre.png'))
    li.setArt({ 'fanart':icon_path('fanart.jpg')})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'movies_year', 'foldername': 'movies'})
    li = xbmcgui.ListItem('Year', iconImage=icon_path('Year.png'))
    li.setArt({ 'fanart':icon_path('fanart.jpg')})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    url = build_url({'mode': 'search_movie_history', 'foldername': 'search'})
    li = xbmcgui.ListItem('Search', iconImage=icon_path('Search.png'))
    li.setArt({ 'fanart':icon_path('fanart.jpg')})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)


    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='latest_movies':

    dicti=urlparse.parse_qs(sys.argv[2][1:])
    page=dicti['page'][0]
    movies=get_latest_movies(page)
    total=len(movies)
    for i in range(len(movies)):
        title=movies[i][0]
        year=movies[i][1]
        thumb=movies[i][2]
        link=movies[i][3]
        

        my_addon = xbmcaddon.Addon()
        meta_setting = my_addon.getSetting('movie_metadata')
        meta=None
        if meta_setting!='false':
            metaget=metahandlers.MetaData()
            try:             
                meta = metaget.get_meta('movie', unicode(title), year=unicode(year))
            except:
                meta=None
        if meta==None:
            meta={}
            meta['title']=title
            meta['year']=year
            meta['cover_url']=thumb
            meta['backdrop_url']=None

        add_movie_item(link,thumb, title, meta=meta,year=year,totalitems=total)

    url = build_url({'mode': 'latest_movies', 'page': str((int(page)+1))})
    li = xbmcgui.ListItem('Next Page >>', iconImage=icon_path('Next.png'))
    li.setArt({ 'fanart':icon_path('fanart.jpg')})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)


elif mode[0]=='movies_genre':
    genres=['Action','Adventure','Animation','Biography','Comedy','Crime','Documentary','Drama','Family','Fantasy','History','Horror','Musical','Mystery','Romance','Sci-Fi','Sport','Thriller','War','Western']

    for i in range(len(genres)):
        url = build_url({'mode': 'open_genre', 'slug': '%s'%(genres[i].lower()), 'page':'1'})
        li = xbmcgui.ListItem('%s'%genres[i], iconImage=icon_path('Genre.png'))
        li.setArt({ 'fanart':icon_path('fanart.jpg')})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)




elif mode[0]=='open_genre':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    genre=dicti['slug'][0]
    page=dicti['page'][0]
    movies=get_movies_genre(genre,page)
    total=len(movies)
    for i in range(len(movies)):
        title=movies[i][0]
        year=movies[i][1]
        thumb=movies[i][2]
        link=movies[i][3]
        

        my_addon = xbmcaddon.Addon()
        meta_setting = my_addon.getSetting('movie_metadata')
        meta=None
        if meta_setting!='false':
            metaget=metahandlers.MetaData()             
            try:             
                meta = metaget.get_meta('movie', unicode(title), year=unicode(year))
            except:
                meta=None
        if meta==None:
            meta={}
            meta['title']=title
            meta['year']=year
            meta['cover_url']=thumb
            meta['backdrop_url']=None

        add_movie_item(link,thumb, title, meta=meta,year=year,totalitems=total)


    url = build_url({'mode': 'open_genre','slug': genre, 'page': str((int(page)+1))})
    li = xbmcgui.ListItem('Next Page >>', iconImage=icon_path('Next.png'))
    li.setArt({ 'fanart':icon_path('fanart.jpg')})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)



elif mode[0]=='movies_year':
    years=['2016','2015','2014','2013','2012','2011','2010','2009','2008','2007','2006','2005','2004','2003','2002','2001','2000']

    for i in range(len(years)):
        url = build_url({'mode': 'open_year', 'year': '%s'%(years[i]), 'page':'1'})
        li = xbmcgui.ListItem('%s'%years[i], iconImage=icon_path('Year.png'))
        li.setArt({ 'fanart':icon_path('fanart.jpg')})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'search_year' })
    li = xbmcgui.ListItem('Enter a Year', iconImage=icon_path('Search.png'))
    li.setArt({ 'fanart':icon_path('fanart.jpg')})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)


    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='open_year':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    year=dicti['year'][0]
    page=dicti['page'][0]
    movies=get_movies_year(year,page)
    total=len(movies)
    for i in range(len(movies)):
        title=movies[i][0]
        year=movies[i][1]
        thumb=movies[i][2]
        link=movies[i][3]
        

        my_addon = xbmcaddon.Addon()
        meta_setting = my_addon.getSetting('movie_metadata')
        meta=None
        if meta_setting!='false':
            metaget=metahandlers.MetaData()             
            try:             
                meta = metaget.get_meta('movie', unicode(title), year=unicode(year))
            except:
                meta=None
        if meta==None:
            meta={}
            meta['title']=title
            meta['year']=year
            meta['cover_url']=thumb
            meta['backdrop_url']=None

        add_movie_item(link,thumb, title, meta=meta,year=year,totalitems=total)


    url = build_url({'mode': 'open_year','year': year, 'page': str((int(page)+1))})
    li = xbmcgui.ListItem('Next Page >>', iconImage=icon_path('Next.png'))
    li.setArt({ 'fanart':icon_path('fanart.jpg')})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='search_year':
    keyboard = xbmc.Keyboard('', 'Enter a year', False)
    keyboard.doModal()
    
    if keyboard.isConfirmed():
        year = keyboard.getText()
        page='1'

        movies=get_movies_year(year,page)
        total=len(movies)
    for i in range(len(movies)):
        title=movies[i][0]
        year=movies[i][1]
        thumb=movies[i][2]
        link=movies[i][3]
        

        my_addon = xbmcaddon.Addon()
        meta_setting = my_addon.getSetting('movie_metadata')
        meta=None
        if meta_setting!='false':
            metaget=metahandlers.MetaData()             
            try:             
                meta = metaget.get_meta('movie', unicode(title), year=unicode(year))
            except:
                meta=None
        if meta==None:
            meta={}
            meta['title']=title
            meta['year']=year
            meta['cover_url']=thumb
            meta['backdrop_url']=None

        add_movie_item(link,thumb, title, meta=meta,year=year,totalitems=total)

    url = build_url({'mode': 'open_year','year': year, 'page': str((int(page)+1))})
    li = xbmcgui.ListItem('Next Page >>', iconImage=icon_path('Next.png'))
    li.setArt({ 'fanart':icon_path('fanart.jpg')})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)


elif mode[0]=='add_movie_fav':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    title=dicti['title'][0]
    year=dicti['year'][0]
    thumb=dicti['thumb'][0]
    link=dicti['link'][0] 
    add_favourite_movie(title,year,link,thumb)  



elif mode[0]=='search_movies':
    keyboard = xbmc.Keyboard('', 'Search movies', False)
    keyboard.doModal()

    if keyboard.isConfirmed():
        query = keyboard.getText()
        add_search_query(query,'movie')
        xbmc.executebuiltin("Container.Refresh")
        time.sleep(1.5)
        url='http://projectfreetv.so/movies/search/' + urllib.quote(query)
        url = build_url({'mode': 'open_movies_search','url':url})
        builtin = 'Container.Update(%s)' % (url)
        xbmc.executebuiltin(builtin)

elif mode[0]=='search_movie_history':
    url = build_url({'mode': 'search_movies', 'foldername': 'search'})
    li = xbmcgui.ListItem('[COLOR green]New Search[/COLOR]', iconImage=icon_path('Search.png'))
    
    li.setArt({ 'fanart':icon_path('fanart.jpg')})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    his=get_search_history('movie')
    for i in range(len(his)):
        url='http://projectfreetv.so/movies/search/' + urllib.quote(his[i])
        
        url = build_url({'mode': 'open_movies_search', 'url': url})
        li = xbmcgui.ListItem(his[i], iconImage=icon_path('Search.png'))
        del_url = build_url({'mode': 'del_his_movie'})
        li.addContextMenuItems([('Erase movie search history','RunPlugin(%s)'%del_url)])
        li.setArt({ 'fanart':icon_path('fanart.jpg')})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                            listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)
elif mode[0]=='open_movies_search':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    url=dicti['url'][0]
    
    movies,next_page=search(url)
    total=len(movies)
    for i in range(len(movies)):
        title=movies[i][0]
        year=movies[i][1]
        thumb=movies[i][2]
        link=movies[i][3]
        

        my_addon = xbmcaddon.Addon()
        meta_setting = my_addon.getSetting('movie_metadata')
        meta=None
        if meta_setting!='false':
            metaget=metahandlers.MetaData()             
            try:             
                meta = metaget.get_meta('movie', unicode(title), year=unicode(year))
            except:
                meta=None
        if meta==None:
            meta={}
            meta['title']=title
            meta['year']=year
            meta['cover_url']=thumb
            meta['backdrop_url']=None

        add_movie_item(link,thumb, title, meta=meta,year=year,totalitems=total)

    if next_page and next_page!='last':
        url = build_url({'mode': 'open_movies_search', 'url':next_page})
        li = xbmcgui.ListItem('Next Page >>', iconImage=icon_path('Next.png'))
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)


###########################################################################################################################################################
###########################################################################################################################################################
#TV
###########################################################################################################################################################


elif mode[0]=='tv':
    url = build_url({'mode': 'fav_tv', 'foldername': 'favs'})
    li = xbmcgui.ListItem('Favourites', iconImage=icon_path('Favourites.png'))
    li.setArt({ 'fanart':icon_path('fanart.jpg')})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'latest_tv', 'foldername': 'shows'})
    li = xbmcgui.ListItem('Lastest Added', iconImage=icon_path('Last_24_Hours.png'))
    li.setArt({ 'fanart':icon_path('fanart.jpg')})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    url = build_url({'mode': 'last7_tv', 'foldername': 'shows'})
    li = xbmcgui.ListItem('TV Calendar', iconImage=icon_path('Calendar.png'))
    li.setArt({ 'fanart':icon_path('fanart.jpg')})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    url = build_url({'mode': 'az_shows', 'foldername': 'shows'})
    li = xbmcgui.ListItem('A-Z', iconImage=icon_path('AZ.png'))
    li.setArt({ 'fanart':icon_path('fanart.jpg')})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'all_tv', 'foldername': 'shows'})
    li = xbmcgui.ListItem('All Shows', iconImage=icon_path('All_Shows.png'))
    li.setArt({ 'fanart':icon_path('fanart.jpg')})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'search_tv_history', 'foldername': 'search'})
    li = xbmcgui.ListItem('Search', iconImage=icon_path('Search.png'))
    li.setArt({ 'fanart':icon_path('fanart.jpg')})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)


    xbmcplugin.endOfDirectory(addon_handle)





elif mode[0]=='latest_tv':
    eps=get_last_eps()
    
    my_addon = xbmcaddon.Addon()
    action = my_addon.getSetting('episodes_action')
    total=len(eps)
    if action=='0':

        for i in range(len(eps)):
                try:
                    show=eps[i][0]
                    season=eps[i][1]
                    episode=eps[i][2]
                    link=eps[i][3]
                    my_addon = xbmcaddon.Addon()
                    meta_setting = my_addon.getSetting('tv_metadata')
                    meta=None
                    if meta_setting!='false':
                        metaget=metahandlers.MetaData()
                        try:             
                            meta=metaget.get_episode_meta(eps[i][0], '', eps[i][1], eps[i][2])
                            title='%s: %sx%s'%(show,season,episode)
                            meta['title']=title
                            meta['name']=title
                        except:
                            meta=None
                    if meta==None:
                        meta={}
                        title='%s: %sx%s'%(show,season,episode)
                        meta['title']=title
                        meta['name']=title
                        meta['tvshowtitle']=show
                        meta['season']=season
                        meta['episode']=episode
                        meta['cover_url']=icon_path('TV_Shows.png')
                        meta['backdrop_url']=None
            
                    add_tv_item(link,show,season,episode,meta=meta,totalitems=total)
                except:
                    show=eps[i][0].encode('ascii','ignore')
                    season=eps[i][1]
                    episode=eps[i][2]
                    link=eps[i][3]
                    my_addon = xbmcaddon.Addon()
                    meta_setting = my_addon.getSetting('tv_metadata')
                    meta=None
                    if meta_setting!='false':
                        metaget=metahandlers.MetaData()   
                        try:          
                            meta=metaget.get_episode_meta(show, '', eps[i][1], eps[i][2])
                            title='%s: %sx%s'%(show,season,episode)
                            meta['title']=title
                            meta['name']=title
                        except:
                            meta=None
                    if meta==None:
                        meta={}
                        title='%s: %sx%s'%(show,season,episode)
                        meta['title']=title
                        meta['name']=title

                        meta['tvshowtitle']=show
                        meta['season']=season
                        meta['episode']=episode
                        meta['cover_url']=icon_path('TV_Shows.png')
                        meta['backdrop_url']=None

                    add_tv_item(link,show,season,episode,meta=meta,totalitems=total)

        xbmcplugin.endOfDirectory(addon_handle)


    else:
        for i in range(len(eps)):


                try:
                    show=eps[i][0]
                    season=eps[i][1]
                    episode=eps[i][2]
                    link=eps[i][3]
                    my_addon = xbmcaddon.Addon()
                    meta_setting = my_addon.getSetting('tv_metadata')
                    meta=None
                    if meta_setting!='false':
                        metaget=metahandlers.MetaData()   
                        try:          
                            meta=metaget.get_episode_meta(eps[i][0], '', eps[i][1], eps[i][2])
                            title='%s: %sx%s'%(show,season,episode)
                            meta['title']=title
                            meta['name']=title
                        except:
                            meta=None
                    if meta==None:
                        meta={}
                        title='%s: %sx%s'%(show,season,episode)
                        meta['title']=title
                        meta['name']=title
                        meta['tvshowtitle']=show
                        meta['season']=season
                        meta['episode']=episode
                        meta['cover_url']=icon_path('TV_Shows.png')
                        meta['backdrop_url']=None

                except:
                    show=eps[i][0].encode('ascii','ignore')
                    season=eps[i][1]
                    episode=eps[i][2]
                    link=eps[i][3]
                    my_addon = xbmcaddon.Addon()
                    meta_setting = my_addon.getSetting('tv_metadata')
                    meta=None
                    if meta_setting!='false':
                        metaget=metahandlers.MetaData()   
                        try:          
                            meta=metaget.get_episode_meta(show, '', eps[i][1], eps[i][2])
                            title='%s: %sx%s'%(show,season,episode)
                            meta['title']=title
                            meta['name']=title
                        except:
                            meta=None
                    if meta==None:
                        meta={}
                        title='%s: %sx%s'%(show,season,episode)
                        meta['title']=title
                        meta['name']=title

                        meta['tvshowtitle']=show
                        meta['season']=season
                        meta['episode']=episode
                        meta['cover_url']=icon_path('TV_Shows.png')
                        meta['backdrop_url']=None

                url = build_url({'mode': 'more_tv','link':link})

                li = xbmcgui.ListItem(title, iconImage=meta['cover_url'])

                li.setInfo('video', meta)
                li.addContextMenuItems([(('Episode Information', 'XBMC.Action(Info)'))])
                li.setProperty("Fanart_Image", meta['backdrop_url'])

                xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True, totalItems=total)


        xbmcplugin.endOfDirectory(addon_handle)  

elif mode[0]=='more_tv':
    
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    page=dicti['link'][0]

    
    show=get_show_from_ep(page)
    


    eps,next_page=get_episodes(show)

    total=len(eps)
    for i in range(len(eps)-1,-1,-1):
                try:
                    show=eps[i][0]
                    season=eps[i][1]
                    episode=eps[i][2]
                    link=eps[i][3]
                    my_addon = xbmcaddon.Addon()
                    meta_setting = my_addon.getSetting('tv_metadata')
                    meta=None
                    if meta_setting!='false':
                        metaget=metahandlers.MetaData()    
                        try:         
                            meta=metaget.get_episode_meta(eps[i][0], '', eps[i][1], eps[i][2])
                            meta['title']=meta['title'].encode('ascii','ignore')
                        except:
                            meta=None    
                    if meta==None:
                        meta={}
                        title='%s: %sx%s'%(show,season,episode)
                        meta['title']=title
                        meta['name']=title
                        meta['tvshowtitle']=show
                        meta['season']=season
                        meta['episode']=episode
                        meta['cover_url']=icon_path('TV_Shows.png')
                        meta['backdrop_url']=None
            
                    add_tv_item(link,show,season,episode,meta=meta,totalitems=total)
                except:
                    show=eps[i][0].encode('ascii','ignore')
                    season=eps[i][1]
                    episode=eps[i][2]
                    link=eps[i][3]
                    my_addon = xbmcaddon.Addon()
                    meta_setting = my_addon.getSetting('tv_metadata')
                    meta=None
                    if meta_setting!='false':
                        metaget=metahandlers.MetaData()        
                        try:     
                            meta=metaget.get_episode_meta(eps[i][0], '', eps[i][1], eps[i][2])
                            meta['title']=meta['title'].encode('ascii','ignore')
                        except:
                            meta=None
                    if meta==None:
                        meta={}
                        title='%s: %sx%s'%(show,season,episode)
                        meta['title']=title
                        meta['name']=title

                        meta['tvshowtitle']=show
                        meta['season']=season
                        meta['episode']=episode
                        meta['cover_url']=icon_path('TV_Shows.png')
                        meta['backdrop_url']=None

                    add_tv_item(link,show,season,episode,meta=meta,totalitems=total)

    if next_page and next_page!='last':
        url = build_url({'mode': 'open_season', 'link':next_page})
        li = xbmcgui.ListItem('Next Page >>', iconImage=icon_path('Next.png'))
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)  



elif mode[0]=='last7_tv':
    days=get_last_days()
    my_addon = xbmcaddon.Addon()
    action = my_addon.getSetting('calendar_type')
    action2 = my_addon.getSetting('episodes_action')
    if action=='0':

        for i in range(len(days)):
            url = build_url({'mode': 'open_days', 'ind': '%s'%(days[i][1])})
            li = xbmcgui.ListItem('%s'%days[i][0], iconImage=icon_path('Calendar.png'))
            li.setArt({ 'fanart':icon_path('fanart.jpg')})
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)
    else:
        for l in range(len(days)):
            li = xbmcgui.ListItem('[COLOR blue]%s[/COLOR]'%days[l][0], iconImage=icon_path('Upcoming.png'))
            li.setProperty('IsPlayable', 'false')
            li.setArt({ 'fanart':icon_path('fanart.jpg')})
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=None,
                                    listitem=li)

            eps=get_day_eps(int(days[l][1]))
            total=len(eps)
            if action2=='0':

                for i in range(len(eps)):
                        try:
                            show=eps[i][0]
                            season=eps[i][1]
                            episode=eps[i][2]
                            link=eps[i][3]
                            my_addon = xbmcaddon.Addon()
                            meta_setting = my_addon.getSetting('tv_metadata')
                            meta=None
                            if meta_setting!='false':
                                metaget=metahandlers.MetaData()     
                                try:        
                                    meta=metaget.get_episode_meta(eps[i][0], '', eps[i][1], eps[i][2])
                                    title='%s: %sx%s'%(show,season,episode)
                                    meta['title']=title
                                    meta['name']=title
                                except:
                                    meta=None
                            if meta==None:
                                meta={}
                                title='%s: %sx%s'%(show,season,episode)
                                meta['title']=title
                                meta['name']=title
                                meta['tvshowtitle']=show
                                meta['season']=season
                                meta['episode']=episode
                                meta['cover_url']=icon_path('TV_Shows.png')
                                meta['backdrop_url']=None
                    
                            add_tv_item(link,show,season,episode,meta=meta,totalitems=total)
                        except:
                            show=eps[i][0].encode('ascii','ignore')
                            season=eps[i][1]
                            episode=eps[i][2]
                            link=eps[i][3]
                            my_addon = xbmcaddon.Addon()
                            meta_setting = my_addon.getSetting('tv_metadata')
                            meta=None
                            if meta_setting!='false':
                                metaget=metahandlers.MetaData()        
                                try:     
                                    meta=metaget.get_episode_meta(show, '', eps[i][1], eps[i][2])
                                    title='%s: %sx%s'%(show,season,episode)
                                    meta['title']=title
                                    meta['name']=title
                                except:
                                    meta=None
                            if meta==None:
                                meta={}
                                title='%s: %sx%s'%(show,season,episode)
                                meta['title']=title
                                meta['name']=title

                                meta['tvshowtitle']=show
                                meta['season']=season
                                meta['episode']=episode
                                meta['cover_url']=icon_path('TV_Shows.png')
                                meta['backdrop_url']=None

                            add_tv_item(link,show,season,episode,meta=meta,totalitems=total)

                

            else:
                for i in range(len(eps)):


                        try:
                            show=eps[i][0]
                            season=eps[i][1]
                            episode=eps[i][2]
                            link=eps[i][3]
                            my_addon = xbmcaddon.Addon()
                            meta_setting = my_addon.getSetting('tv_metadata')
                            meta=None
                            if meta_setting!='false':
                                metaget=metahandlers.MetaData()     
                                try:        
                                    meta=metaget.get_episode_meta(eps[i][0], '', eps[i][1], eps[i][2])
                                    title='%s: %sx%s'%(show,season,episode)
                                    meta['title']=title
                                    meta['name']=title
                                except:
                                    meta=None
                            if meta==None:
                                meta={}
                                title='%s: %sx%s'%(show,season,episode)
                                meta['title']=title
                                meta['name']=title
                                meta['tvshowtitle']=show
                                meta['season']=season
                                meta['episode']=episode
                                meta['cover_url']=icon_path('TV_Shows.png')
                                meta['backdrop_url']=None

                        except:
                            show=eps[i][0].encode('ascii','ignore')
                            season=eps[i][1]
                            episode=eps[i][2]
                            link=eps[i][3]
                            my_addon = xbmcaddon.Addon()
                            meta_setting = my_addon.getSetting('tv_metadata')
                            meta=None
                            if meta_setting!='false':
                                metaget=metahandlers.MetaData()     
                                try:        
                                    meta=metaget.get_episode_meta(show, '', eps[i][1], eps[i][2])
                                    title='%s: %sx%s'%(show,season,episode)
                                    meta['title']=title
                                    meta['name']=title
                                except:
                                    meta=None
                            if meta==None:
                                meta={}
                                title='%s: %sx%s'%(show,season,episode)
                                meta['title']=title
                                meta['name']=title

                                meta['tvshowtitle']=show
                                meta['season']=season
                                meta['episode']=episode
                                meta['cover_url']=icon_path('TV_Shows.png')
                                meta['backdrop_url']=None

                        url = build_url({'mode': 'more_tv','link':link})

                        li = xbmcgui.ListItem(title, iconImage=meta['cover_url'])

                        li.setInfo('video', meta)
                        li.addContextMenuItems([(('Episode Information', 'XBMC.Action(Info)'))])
                        li.setProperty("Fanart_Image", meta['backdrop_url'])

                        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                        listitem=li, isFolder=True)


                







    xbmcplugin.endOfDirectory(addon_handle)


elif mode[0]=='open_days':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    page=dicti['ind'][0]

    eps=get_day_eps(int(page))
        
    my_addon = xbmcaddon.Addon()
    action = my_addon.getSetting('episodes_action')
    total=len(eps)
    if action=='0':

        for i in range(len(eps)):
                try:
                    show=eps[i][0]
                    season=eps[i][1]
                    episode=eps[i][2]
                    link=eps[i][3]
                    my_addon = xbmcaddon.Addon()
                    meta_setting = my_addon.getSetting('tv_metadata')
                    meta=None
                    if meta_setting!='false':
                        metaget=metahandlers.MetaData()   
                        try:          
                            meta=metaget.get_episode_meta(eps[i][0], '', eps[i][1], eps[i][2])
                            title='%s: %sx%s'%(show,season,episode)
                            meta['title']=title
                            meta['name']=title
                        except:
                            meta=None
                    if meta==None:
                        meta={}
                        title='%s: %sx%s'%(show,season,episode)
                        meta['title']=title
                        meta['name']=title
                        meta['tvshowtitle']=show
                        meta['season']=season
                        meta['episode']=episode
                        meta['cover_url']=icon_path('TV_Shows.png')
                        meta['backdrop_url']=None
            
                    add_tv_item(link,show,season,episode,meta=meta,totalitems=total)
                except:
                    show=eps[i][0].encode('ascii','ignore')
                    season=eps[i][1]
                    episode=eps[i][2]
                    link=eps[i][3]
                    my_addon = xbmcaddon.Addon()
                    meta_setting = my_addon.getSetting('tv_metadata')
                    meta=None
                    if meta_setting!='false':
                        metaget=metahandlers.MetaData()     
                        try:        
                            meta=metaget.get_episode_meta(show, '', eps[i][1], eps[i][2])
                            title='%s: %sx%s'%(show,season,episode)
                            meta['title']=title
                            meta['name']=title
                        except:
                            meta=None
                    if meta==None:
                        meta={}
                        title='%s: %sx%s'%(show,season,episode)
                        meta['title']=title
                        meta['name']=title

                        meta['tvshowtitle']=show
                        meta['season']=season
                        meta['episode']=episode
                        meta['cover_url']=icon_path('TV_Shows.png')
                        meta['backdrop_url']=None

                    add_tv_item(link,show,season,episode,meta=meta,totalitems=total)

        xbmcplugin.endOfDirectory(addon_handle)  


    else:
        for i in range(len(eps)):


                try:
                    show=eps[i][0]
                    season=eps[i][1]
                    episode=eps[i][2]
                    link=eps[i][3]
                    my_addon = xbmcaddon.Addon()
                    meta_setting = my_addon.getSetting('tv_metadata')
                    meta=None
                    if meta_setting!='false':
                        metaget=metahandlers.MetaData()
                        try:             
                            meta=metaget.get_episode_meta(eps[i][0], '', eps[i][1], eps[i][2])
                            title='%s: %sx%s'%(show,season,episode)
                            meta['title']=title
                            meta['name']=title
                        except:
                            meta=None
                    if meta==None:
                        meta={}
                        title='%s: %sx%s'%(show,season,episode)
                        meta['title']=title
                        meta['name']=title
                        meta['tvshowtitle']=show
                        meta['season']=season
                        meta['episode']=episode
                        meta['cover_url']=icon_path('TV_Shows.png')
                        meta['backdrop_url']=None

                except:
                    show=eps[i][0].encode('ascii','ignore')
                    season=eps[i][1]
                    episode=eps[i][2]
                    link=eps[i][3]
                    my_addon = xbmcaddon.Addon()
                    meta_setting = my_addon.getSetting('tv_metadata')
                    meta=None
                    if meta_setting!='false':
                        metaget=metahandlers.MetaData()  
                        try:           
                            meta=metaget.get_episode_meta(show, '', eps[i][1], eps[i][2])
                            title='%s: %sx%s'%(show,season,episode)
                            meta['title']=title
                            meta['name']=title
                        except:
                            meta=None
                    if meta==None:
                        meta={}
                        title='%s: %sx%s'%(show,season,episode)
                        meta['title']=title
                        meta['name']=title

                        meta['tvshowtitle']=show
                        meta['season']=season
                        meta['episode']=episode
                        meta['cover_url']=icon_path('TV_Shows.png')
                        meta['backdrop_url']=None

                url = build_url({'mode': 'more_tv','link':link})

                li = xbmcgui.ListItem(title, iconImage=meta['cover_url'])

                li.setInfo('video', meta)
                add_favourite_show_uri = build_url({'mode':'add_fav_from_ep', 'show': show.encode('ascii','ignore'), 'link':link })

                li.addContextMenuItems([('Episode Information', 'XBMC.Action(Info)'),
                        ('Add show to favourites','RunPlugin(%s)'%add_favourite_show_uri)])
                li.setProperty("Fanart_Image", meta['backdrop_url'])

                xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)


        xbmcplugin.endOfDirectory(addon_handle)  
elif mode[0]=='az_shows':
    abc = get_alphabet()
    for i in range(len(abc)):
        icon = abc[i]
        if icon == '#':
            icon = '0'
        url = build_url({'mode': 'open_letter', 'letter':'%s'%abc[i]})
        li = xbmcgui.ListItem('%s'%abc[i], iconImage=icon_path('%s.png'%icon))
        li.setArt({ 'fanart':icon_path('fanart.jpg')})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='open_letter':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    letter=dicti['letter'][0]

    shows=get_shows_by_letter(letter)

    for i in range(len(shows)):
        url = build_url({'mode': 'open_show', 'link': '%s'%(shows[i][1])})
        li = xbmcgui.ListItem('%s'%shows[i][0], iconImage=icon_path('TV_Shows.png'))
        try:
            fav_uri = build_url({'mode': 'add_tv_fav', 'show': shows[i][0],'link': shows[i][1]})
        except:
            fav_uri = build_url({'mode': 'add_tv_fav', 'show': ((shows[i][0]).encode('ascii','ignore')),'link':shows[i][1] })

        li.addContextMenuItems([ ('Add to PFTV favourites', 'RunPlugin(%s)'%fav_uri)])
        li.setArt({ 'fanart':icon_path('fanart.jpg')})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='all_tv':
    shows=get_all_shows()
    

    for i in range(len(shows)):
        url = build_url({'mode': 'open_show', 'link': '%s'%(shows[i][1])})
        li = xbmcgui.ListItem('%s'%shows[i][0], iconImage=icon_path('TV_Shows.png'))

        fav_uri = build_url({'mode': 'add_tv_fav', 'show': shows[i][0],'link': shows[i][1]})

        li.addContextMenuItems([ ('Add to PFTV favourites', 'RunPlugin(%s)'%fav_uri)])
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)
elif mode[0]=='add_tv_fav':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    name=dicti['show'][0]
    link=dicti['link'][0]
    thumb=get_show_img(link)

    add_favourite_show(name,link,thumb)

elif mode[0] == 'add_fav_from_ep':
    name = args['show'][0]
    ep_link = args['link'][0]
    link = get_show_from_ep(ep_link)
    thumb=get_show_img(link)

    add_favourite_show(name,link,thumb)

elif mode[0]=='open_show':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    link=dicti['link'][0]

    seasons=get_seasons(link)

    for season in seasons:
        url = build_url({'mode': 'open_season', 'link': '%s'%(season[1])})
        li = xbmcgui.ListItem('%s'%season[0].replace('(',' ('), iconImage=icon_path('TV_Shows.png'))
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='open_season':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    link=dicti['link'][0]

    eps,next_page=get_episodes(link)
    total=len(eps)
    if next_page :
        eps=list(reversed(eps))

    for i in range(len(eps)):
            try:
                show=eps[i][0]
                season=eps[i][1]
                episode=eps[i][2]
                link=eps[i][3]
                my_addon = xbmcaddon.Addon()
                meta_setting = my_addon.getSetting('tv_metadata')
                meta=None
                if meta_setting!='false':
                    metaget=metahandlers.MetaData()
                    try:             
                        meta=metaget.get_episode_meta(eps[i][0], '', eps[i][1], eps[i][2])
                    except:
                        meta=None
                if meta==None:
                    meta={}
                    title='%s: %sx%s'%(show,season,episode)

                    meta['title']=title.encode('ascii','ignore')
                    meta['name']=title.encode('ascii','ignore')
                    meta['tvshowtitle']=show
                    meta['season']=season
                    meta['episode']=episode
                    meta['cover_url']=icon_path('TV_Shows.png')
                    meta['backdrop_url']=None
        
                add_tv_item(link,show,season,episode,meta=meta,totalitems=total)
            except:
                show=eps[i][0]
                season=eps[i][1]
                episode=eps[i][2]
                link=eps[i][3]
                my_addon = xbmcaddon.Addon()
                meta_setting = my_addon.getSetting('tv_metadata')
                meta=None
                if meta_setting!='false':
                    metaget=metahandlers.MetaData()             
                    try:             
                        meta=metaget.get_episode_meta(eps[i][0], '', eps[i][1], eps[i][2])
                    except:
                        meta=None
                    
                if meta==None:
                    meta={}
                    title='%s: %sx%s'%(show,season,episode)
                    meta['title']=title
                    meta['name']=title

                    meta['tvshowtitle']=show
                    meta['season']=season
                    meta['episode']=episode
                    meta['cover_url']=icon_path('TV_Shows.png')
                    meta['backdrop_url']=None

                add_tv_item(link,show,season,episode,meta=meta,totalitems=total)
    if next_page and next_page!='last':
        url = build_url({'mode': 'open_season', 'link':next_page})
        li = xbmcgui.ListItem('Next Page >>', iconImage=icon_path('Next.png'))
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)  


    


elif mode[0]=='open_link':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    link=dicti['link'][0]
    sh=dicti['show'][0]
    s=dicti['season'][0]
    e=dicti['ep'][0]
    meta=json.loads(dicti['meta'][0])


    link=get_link(link)
    import urlresolver
    resolved=urlresolver.resolve(link)

    if meta['title']==sh:
        meta['tvshowtitle']=sh
        meta['title']='%s: %sx%s'%(sh,s,e)
        meta['season']=s
        meta['episode']=e
                               


    li = xbmcgui.ListItem(meta['title'])
    li.setInfo('video',meta)
    
    
    li.setProperty('IsPlayable', 'true')
    li.setThumbnailImage(meta['poster'])


    xbmc.Player().play(item=resolved, listitem=li)





elif mode[0]=='search':
    url = build_url({'mode': 'search_movie_history', 'foldername': 'search'})
    li = xbmcgui.ListItem('Search Movies', iconImage=icon_path('Search.png'))
    li.setArt({ 'fanart':icon_path('fanart.jpg')})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'search_tv_history', 'foldername': 'search'})
    li = xbmcgui.ListItem('Search TV Shows', iconImage=icon_path('Search.png'))
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
        url = build_url({'mode': 'open_tv_search', 'query': his[i]})
        li = xbmcgui.ListItem(his[i], iconImage=icon_path('Search.png'))
        del_url = build_url({'mode': 'del_his_tv'})
        li.addContextMenuItems([('Erase tv search history','RunPlugin(%s)'%del_url)])
    
        li.setArt({ 'fanart':icon_path('fanart.jpg')})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                            listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)


elif mode[0]=='search_tv':
    keyboard = xbmc.Keyboard('', 'Search TV Episodes', False)
    keyboard.doModal()
    
    if keyboard.isConfirmed():
        query = keyboard.getText()
        add_search_query(query,'tv')
        xbmc.executebuiltin("Container.Refresh")
        time.sleep(1.5)

        url = build_url({'mode': 'open_tv_search', 'query':query})
        builtin = 'Container.Update(%s)' % (url)
        xbmc.executebuiltin(builtin)




elif mode[0]=='open_tv_search':
        dicti=urlparse.parse_qs(sys.argv[2][1:])
        query=dicti['query'][0]
        my_addon = xbmcaddon.Addon()
        setting = my_addon.getSetting('search_type')

        if setting=='1':
                            
            site='http://projectfreetv.so/search/'+urllib.quote(query)
            eps,next_page=get_episodes(site)
            total=len(eps)
            for i in range(len(eps)-1,-1,-1):
                        try:
                            show=eps[i][0]
                            season=eps[i][1]
                            episode=eps[i][2]
                            link=eps[i][3]
                            my_addon = xbmcaddon.Addon()
                            meta_setting = my_addon.getSetting('tv_metadata')
                            meta=None
                            if meta_setting!='false':
                                metaget=metahandlers.MetaData()   
                                try:          
                                    meta=metaget.get_episode_meta(eps[i][0], '', eps[i][1], eps[i][2])
                                    meta['title']=meta['title'].encode('ascii','ignore')
                                except:
                                    meta=None
                                
                            if meta==None:
                                meta={}
                                title='%s: %sx%s'%(show,season,episode)
                                meta['title']=title
                                meta['name']=title
                                meta['tvshowtitle']=show
                                meta['season']=season
                                meta['episode']=episode
                                meta['cover_url']=icon_path('TV_Shows.png')
                                meta['backdrop_url']=None
                    
                            add_tv_item(link,show,season,episode,meta=meta,totalitems=total)
                        except:
                            show=eps[i][0].encode('ascii','ignore')
                            season=eps[i][1]
                            episode=eps[i][2]
                            link=eps[i][3]
                            my_addon = xbmcaddon.Addon()
                            meta_setting = my_addon.getSetting('tv_metadata')
                            meta=None
                            if meta_setting!='false':
                                metaget=metahandlers.MetaData() 
                                try:            
                                    meta=metaget.get_episode_meta(eps[i][0], '', eps[i][1], eps[i][2])
                                    meta['title']=meta['title'].encode('ascii','ignore')
                                except:
                                    meta=None
                            if meta==None:
                                meta={}
                                title='%s: %sx%s'%(show,season,episode)
                                meta['title']=title
                                meta['name']=title

                                meta['tvshowtitle']=show
                                meta['season']=season
                                meta['episode']=episode
                                meta['cover_url']=icon_path('TV_Shows.png')
                                meta['backdrop_url']=None

                            add_tv_item(link,show,season,episode,meta=meta,totalitems=total)

            if next_page and next_page!='last':
                url = build_url({'mode': 'open_season', 'link':next_page})
                li = xbmcgui.ListItem('Next Page >>', iconImage=icon_path('Next.png'))
                xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                        listitem=li, isFolder=True)
            xbmcplugin.endOfDirectory(addon_handle)  

            
        else:
            shows=search_shows(query)
            for i in range(len(shows)):
                url = build_url({'mode': 'open_show', 'link': '%s'%(shows[i][1])})
                li = xbmcgui.ListItem('%s'%shows[i][0], iconImage=icon_path('TV_Shows.png'))
                try:
                    fav_uri = build_url({'mode': 'add_tv_fav', 'show': shows[i][0],'link': shows[i][1]})
                except:
                    fav_uri = build_url({'mode': 'add_tv_fav', 'show': ((shows[i][0]).encode('ascii','ignore')),'link':shows[i][1] })

                li.addContextMenuItems([ ('Add to PFTV favourites', 'RunPlugin(%s)'%fav_uri)])
                xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                        listitem=li, isFolder=True)
            xbmcplugin.endOfDirectory(addon_handle)




###########################################################################################################################################################
###########################################################################################################################################################
###########################################################################################################################################################

elif mode[0]=='erase_all':
    ret = xbmcgui.Dialog().yesno('Remove all favourites', 'Are you sure you want to reset your favourites?' ) 
    
    if ret:       

        delete_all_movie_favs()
        delete_all_tv_favs()
        xbmcgui.Dialog().ok("ProjectFreeTV.so", "Successfully erased favourites database!")

elif mode[0]=='settings':
    xbmc.executebuiltin("Addon.OpenSettings(%s)"%addonID)


elif mode[0]=='favs':
    url = build_url({'mode': 'fav_movies', 'foldername': 'favs'})
    li = xbmcgui.ListItem('Movie Favourites', iconImage=icon_path('Movies.png'))
    li.setArt({ 'fanart':icon_path('fanart.jpg')})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'fav_tv', 'foldername': 'favs'})
    li = xbmcgui.ListItem('TV Favourites', iconImage=icon_path('Tv_Shows.png'))
    li.setArt({ 'fanart':icon_path('fanart.jpg')})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

   


    xbmcplugin.endOfDirectory(addon_handle)
elif mode[0]=='fav_tv':
    shows=get_favourite_shows()

    for i in range(len(shows)):
        url = build_url({'mode': 'open_show', 'link': '%s'%(shows[i][1])})
        title=shows[i][0]
        link=shows[i][1]
        thumb=shows[i][2]
        li = xbmcgui.ListItem('%s'%shows[i][0], iconImage=thumb)

        try:
            del_uri = build_url({'mode': 'del_show_fav', 'title':title,  'link':link})

        except:
            del_uri = build_url({'mode': 'del_show_fav', 'title':title.encode('ascii','ignore'),'link':link})

        del_all = build_url({'mode': 'del_tv_all'})

        li.addContextMenuItems([('Remove from PFTV favourites','RunPlugin(%s)'%del_uri),
                                ('Remove all PFTV TV favourites','RunPlugin(%s)'%del_all)])
        
        
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
elif mode[0]=='fav_movies':
    movies=get_favourite_movies()
    total=len(movies)
    for i in range(len(movies)):
        title=movies[i][0]
        year=movies[i][1]
        thumb=movies[i][2]
        link=movies[i][3]
        

        my_addon = xbmcaddon.Addon()
        meta_setting = my_addon.getSetting('movie_metadata')
        meta=None
        if meta_setting!='false':
            metaget=metahandlers.MetaData()             
            try:             
                meta = metaget.get_meta('movie', unicode(title), year=unicode(year))
            except:
                meta=None
        if meta==None:
            meta={}
            meta['title']=title
            meta['year']=year
            meta['cover_url']=thumb
            meta['backdrop_url']=None

        add_movie_item(link,thumb, title, meta=meta,year=year,fav='1',totalitems=total)


    
    xbmcplugin.endOfDirectory(addon_handle)
elif mode[0]=='del_movie_fav':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    title=dicti['title'][0]
    year=dicti['year'][0]
    thumb=dicti['thumb'][0]
    link=dicti['link'][0] 
    remove_movie_fav(title,year,thumb,link) 
    xbmc.executebuiltin("Container.Refresh")

elif mode[0]=='del_movie_all':
    delete_all_movie_favs()
    xbmc.executebuiltin("Container.Refresh")


elif mode[0]=='download':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    title=dicti['title'][0]
    type=dicti['type'][0]
    link=dicti['link'][0] 

    my_addon = xbmcaddon.Addon()
    links=get_linkss(link)
    sort = my_addon.getSetting('down_sort')
    if sort !='false':
        links=sort_links(links)

    
    autodown = my_addon.getSetting('autodownload')
    if autodown=='false':
        hosts=[]
        linky=[]
        if type=='movie':
            for i in range(len(links)):
                host=links[i][0]
                link=links[i][1]
                linky.append(link)

                hosts.append(host)

        elif type=='tv':
            for i in range(len(links)):
                host=links[i][0]
                link=links[i][1]
                age=links[i][2]
                linky.append(link)
                hosts.append(host + '('+age+')')

        dialog = xbmcgui.Dialog()
        index = dialog.select('Choose a download source:', hosts)
        
        if index>-1:
            link=get_link(linky[index])
            import urlresolver
            resolved=urlresolver.resolve(link)

            if resolved:
                

                download(title,resolved,type)
    else:
        import urlresolver
        for i in range(len(links)):
            link=get_link(links[i][1])
            resolved=urlresolver.resolve(link)

            if resolved:
                download(title,stream_url,type)
                break    
elif mode[0]=='erase_history':
    
    ret = xbmcgui.Dialog().yesno('Erase history', 'Are you sure you want to delete your search history?' ) 
    
    if ret:       

        delete_history('movies')
        delete_history('tv')
        xbmcgui.Dialog().ok("ProjectFreeTV.so", "Successfully erased search history!")

elif mode[0]=='del_his_tv':
    delete_history('tv')
    xbmc.executebuiltin("Container.Refresh")
elif mode[0]=='del_his_movie':
    delete_history('movie')
    xbmc.executebuiltin("Container.Refresh")
