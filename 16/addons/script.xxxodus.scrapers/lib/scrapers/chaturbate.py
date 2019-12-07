import xbmc,xbmcgui,xbmcplugin,os,urlparse,re
import client
import kodi
import dom_parser2
import log_utils
import scraper_updater
from resources.lib.modules import utils
from resources.lib.modules import helper
from resources.lib.modules import player
buildDirectory = utils.buildDir

filename     = os.path.basename(__file__).split('.')[0]
base_domain  = 'http://chaturbate.com'
base_name    = base_domain.replace('www.',''); base_name = re.findall('(?:\/\/|\.)([^.]+)\.',base_name)[0].title()
type         = 'cam'
menu_mode    = 300
content_mode = 301
player_mode  = 801

search_tag   = 0

chaturbate_icon = xbmc.translatePath(os.path.join('special://home/addons/script.xxxodus.artwork/resources/art/', 'main/chaturbate.png'))

import sqlite3
databases = xbmc.translatePath(os.path.join('special://profile/addon_data/plugin.video.XXX-O-DUS', 'databases'))
chaturbatedb = xbmc.translatePath(os.path.join(databases, 'chaturbate.db'))

if ( not os.path.exists(databases)): os.makedirs(databases)
conn = sqlite3.connect(chaturbatedb)
c = conn.cursor()
try:
    c.executescript("CREATE TABLE IF NOT EXISTS chaturbate (name, url, image);")
except:
    pass
conn.close()

@utils.url_dispatcher.register('%s' % menu_mode)
def menu():
    
    scraper_updater.check(filename)
    
    url = base_domain
    r = client.request(url)
    r = dom_parser2.parse_dom(r, 'dd')
    r = dom_parser2.parse_dom(r, 'a', req='href')
    r = [i for i in r if 'private-cams' not in i.attrs['href']]
    r = [(urlparse.urljoin(base_domain,i.attrs['href']),i.content) for i in r if i]
    dirlst = []
    icon = xbmc.translatePath(os.path.join('special://home/addons/script.xxxodus.artwork', 'resources/art/main/%s.png' % filename))
    fanarts = xbmc.translatePath(os.path.join('special://home/addons/script.xxxodus.artwork', 'resources/art/%s/fanart.jpg' % filename))
    dirlst.append({'name': 'Monitored Performers', 'url': 'none', 'mode': 30, 'icon': icon, 'fanart': fanarts, 'folder': True})
    dirlst.append({'name': 'Search By Username', 'url': 'none', 'mode': 32, 'icon': icon, 'fanart': fanarts, 'folder': False})
    dirlst.append({'name': 'Rooms By Tag', 'url': 'tags', 'mode': 302, 'icon': icon, 'fanart': fanarts, 'folder': True})
    for i in r:
        try:
            name = kodi.sortX(i[1].encode('utf-8')).title()
            dirlst.append({'name': name, 'url': i[0], 'mode': content_mode, 'icon': icon, 'fanart': fanarts, 'folder': True})
        except Exception as e:
            log_utils.log('Error adding menu item %s in %s:: Error: %s' % (i[1].title(),base_name.title(),str(e)), log_utils.LOGERROR)
    
    if dirlst: buildDirectory(dirlst)    
    else:
        kodi.notify(msg='No Menu Items Found')
        quit()
        
@utils.url_dispatcher.register('%s' % content_mode,['url'],['searched'])
def content(url,searched=False):

    r = client.request(url)
    r = dom_parser2.parse_dom(r, 'li')
    r = [(dom_parser2.parse_dom(i, 'div', {'class': 'title'}), \
        dom_parser2.parse_dom(i, 'img', req='src'), \
        dom_parser2.parse_dom(i, 'div', {'class': re.compile('thumbnail_label.+?')}), \
        dom_parser2.parse_dom(i, 'li', {'title': re.compile('.+?')}), \
        dom_parser2.parse_dom(i, 'li', {'class': 'location'}), \
        dom_parser2.parse_dom(i, 'li', {'class': 'cams'}) \
        ) for i in r if '<div class="title">' in i.content]

    r = [(dom_parser2.parse_dom(i[0], 'a'), \
        dom_parser2.parse_dom(i[0], 'span'), \
        i[2][0].content, \
        i[1][0].attrs['src'], \
        i[3][0].content if i[3] else 'Unknown', \
        i[4][0].content, \
        i[5][0].content, \
        ) for i in r]
    r = [(urlparse.urljoin(base_domain,i[0][0].attrs['href']), i[0][0].content, i[1][0].content,i[2],i[3],i[6],i[5],i[4]) for i in r]
    dirlst = []
    
    for i in r:
        try:
            name = '%s - [ %s ]' % (kodi.sortX(i[1].encode('utf-8')).title(),kodi.sortX(i[3].encode('utf-8')))
            description = 'Name: %s \nAge: %s \nLocation: %s \nStats: %s \n\nDescription: %s' % \
            (kodi.sortX(i[1].encode('utf-8')),i[2],kodi.sortX(i[6].encode('utf-8')),kodi.sortX(i[5].encode('utf-8')),kodi.sortX(i[7].encode('utf-8')))
            content_url = i[0] + '|SPLIT|%s' % base_name
            fanarts = xbmc.translatePath(os.path.join('special://home/addons/script.xxxodus.artwork', 'resources/art/%s/fanart.jpg' % filename))
            dirlst.append({'name': name, 'url': content_url, 'mode': player_mode, 'icon': i[4], 'fanart': fanarts, 'description': description, 'folder': False})
        except Exception as e:
            log_utils.log('Error adding menu item %s in %s:: Error: %s' % (i[1].title(),base_name.title(),str(e)), log_utils.LOGERROR)
    
    if dirlst: buildDirectory(dirlst, stopend=True, isVideo = False, isDownloadable = False, chaturbate = True)
    else:
        kodi.notify(msg='No Content Found')
        quit()
        
    search_pattern = '''<li><a\s*href=['"]([^'"]+)['"]\s*class=['"]next endless_page_link['"]>next<\/a><\/li>'''
    parse = base_domain
    helper.scraper().get_next_page(content_mode,url,search_pattern,filename,parse)
    
@utils.url_dispatcher.register('302', ['url'])
def byTags(url):

    c = client.request(urlparse.urljoin(base_domain, url))
    r = dom_parser2.parse_dom(c, 'div', {'class': 'tag_row'})
    r = [(dom_parser2.parse_dom(i, 'a', req='href'), \
          dom_parser2.parse_dom(i, 'span', {'class': 'viewers'}), \
          dom_parser2.parse_dom(i, 'span', {'class': 'rooms'})) \
        for i in r]
    r = [(urlparse.urljoin(base_domain, i[0][0].attrs['href']), i[0][0].content, i[1][0].content, i[2][0].content) for i in r]
    dirlst = []
    
    for i in r:
        try:
            name = '%s - [ Viewers: %s | Rooms: %s ]' % (kodi.sortX(i[1].encode('utf-8')).title(),kodi.sortX(i[2].encode('utf-8')),kodi.sortX(i[3].encode('utf-8')))
            icon = xbmc.translatePath(os.path.join('special://home/addons/script.xxxodus.artwork', 'resources/art/%s/icon.png' % filename))
            fanarts = xbmc.translatePath(os.path.join('special://home/addons/script.xxxodus.artwork', 'resources/art/%s/fanart.jpg' % filename))
            dirlst.append({'name': name, 'url': i[0], 'mode': content_mode, 'icon': icon, 'fanart': fanarts, 'description': name, 'folder': True})
        except Exception as e:
            log_utils.log('Error adding menu item %s in %s:: Error: %s' % (i[1].title(),base_name.title(),str(e)), log_utils.LOGERROR)
    
    if dirlst: 
        try:
            np = re.findall('''<li><a\s*href=['"]([^'"]+)['"]\s*class=['"]next endless_page_link['"]>next<\/a><\/li>''',c)[0]
            dirlst.append({'name': 'Next Page -->', 'url': np, 'mode': 302, 'icon': icon, 'fanart': fanarts, 'description': 'View more tags.', 'folder': True})
        except: 
            log_utils.log('No next page link found for Chaturbate :: %s ' % (url), log_utils.LOGNOTICE)
        buildDirectory(dirlst)
    else:
        kodi.notify(msg='No Content Found')
        quit()
        
@utils.url_dispatcher.register('30')
def getMonitoring():

    dirlist = []
    fanarts = xbmc.translatePath(os.path.join('special://home/addons/script.xxxodus.artwork', 'resources/art/%s/fanart.jpg' % filename))

    conn = sqlite3.connect(chaturbatedb)
    conn.text_factory = str
    c = conn.cursor()
    c.execute("SELECT * FROM chaturbate")
    e = [i for i in c.fetchall()]
    conn.close()

    xbmc.executebuiltin("Dialog.Close(busydialog)")
    kodi.dp.create(kodi.get_name(),"[COLOR white]Currently Checking......[/COLOR]" )
    kodi.dp.update(0)
    i = 0
    namelist = []; urllist = []; iconlist = []; countlist = []; combinedlists=[]
    for (name, url, iconimage) in e:
        try:
            iconimage = 'https://roomimg.stream.highwebmedia.com/ri/' + name.lower() + '.jpg'
            progress = 100 * int(i)/len(e)
            kodi.dp.update(progress,"[COLOR white]Currently Checking " + name + "[/COLOR]","[COLOR white]Checked " + str(i) + " of " + str(len(e)) + "[/COLOR]")
            r = client.request(url)
            if '.m3u8' in r:
                namelist.append(name)
                urllist.append(url)
                iconlist.append(iconimage)
                countlist.append('0')
                combinedlists = list(zip(countlist,namelist,urllist,iconlist))
            else: 
                try: 
                    last_seen=re.compile("<dt>Last Broadcast:<\/dt><dd>(.+?)<\/dd>").findall(r)[0]
                except: last_seen = "Unknown"
                namelist.append(name + '|SPLIT|' + last_seen)
                urllist.append(url)
                iconlist.append(iconimage)
                countlist.append('1')
                combinedlists = list(zip(countlist,namelist,urllist,iconlist))
        except: 
            namelist.append(name)
            urllist.append(url)
            iconlist.append(iconimage)
            countlist.append('2')
            combinedlists = list(zip(countlist,namelist,urllist,iconlist))
        i += 1        
        if kodi.dp.iscanceled(): break

    kodi.dp.close()
    
    dirlist.append({'name': kodi.giveColor('Add A Performer To Monitor','white',True), 'url': 'None', 'mode': 31, 'icon': chaturbate_icon, 'fanart': fanarts, 'folder': False})
    dirlist.append({'name': kodi.giveColor('Delete All Performers from List','white',True), 'url': 'None', 'mode': 33, 'icon': chaturbate_icon, 'fanart': fanarts, 'folder': False})

    if combinedlists: 
        tup = sorted(combinedlists, key=lambda x: (int(x[0]),x[1]),reverse=False)
        for count,title,url,iconimage in tup:
            url += '|CHAT|%s|CHAT|%s' % (base_name,title)
            if count == '0':
                title = '[COLOR pink][B]%s is online now![/B][/COLOR]' % title 
            elif count == '1':
                title,last_seen = title.split('|SPLIT|')
                title = '[COLOR white][B]%s[/B][/COLOR] - Offline! - Last Broadcast: %s' % (title,last_seen)
            else: title = '[COLOR white][B]%s[/B][/COLOR] - Error Checking!' % title
    
            dirlist.append({'name': title, 'url': url, 'mode': player_mode, 'icon': iconimage, 'fanart': fanarts, 'folder': False})
     
    buildDirectory(dirlist, isDownloadable=False, isVideo=True, chaturbate=True)

@utils.url_dispatcher.register('32')  
def searchUser():

    user = kodi.get_keyboard('Enter Username')
    if user:
        user = user.replace(' ','_')
        url = 'https://chaturbate.com/' + user
        iconimg = 'https://roomimg.stream.highwebmedia.com/ri/' + user + '.jpg'
        url += '|SPLIT|Chaturbate'
        player.resolve_url(url,user,iconimg)
    else:
        kodi.dialog.ok(kodi.get_name(), 'No username entered. Please try again.')
        quit()

@utils.url_dispatcher.register('31')  
def followUser():

    user = kodi.get_keyboard('Enter Username')
    if user:
        user = user.replace(' ','_')
        xbmc.executebuiltin("ActivateWindow(busydialog)")
        
        conn = sqlite3.connect(chaturbatedb)
        conn.text_factory = str
        c = conn.cursor()
        c.execute("SELECT name FROM chaturbate")
        e = [i for i in c.fetchall()]
        conn.close()
        if user in str(e):
            kodi.dialog.ok(kodi.get_name(), user + ' is already being monitored.')
            xbmc.executebuiltin("Dialog.Close(busydialog)")
            quit()
        url = 'https://chaturbate.com/' + user
        try:
            r = client.request(url)
        except:
            xbmc.executebuiltin("Dialog.Close(busydialog)")
            kodi.dialog.ok(kodi.get_name(), 'We could not find any model matching the username ' + user + '. Please check the username and try again.')
            quit()
        if not 'Bio and Free Webcam' in r:
                xbmc.executebuiltin("Dialog.Close(busydialog)")
                dialog.ok(kodi.get_name(), 'We could not find any model matching the username ' + user + '. Please check the username and try again.')
                quit()
        else:
            iconimg = 'https://roomimg.stream.highwebmedia.com/ri/' + user + '.jpg'
            addPerformer(user,url,iconimg)
            kodi.dialog.ok(kodi.get_name(), user + ' has been added to the monitor list.')
            xbmc.executebuiltin("Dialog.Close(busydialog)")
            xbmc.executebuiltin('Container.Refresh')
            quit()
    else:
        kodi.dialog.ok(kodi.get_name(), 'No username entered. Please try again.')
        xbmc.executebuiltin("Dialog.Close(busydialog)")
        quit()
            
@utils.url_dispatcher.register('101', ['chat','chatmode','name','url','iconimage','folder'])  
def monitorRunner(chat,chatmode,name,url,img,_folder):
    try: name = name.split(' - ')[0]
    except: pass
    if chat == "add":
        delPerformer(url)
        addPerformer(name, url, img)
        kodi.notify('Chaturbate','%s is being monitored.' % name, sound=True, icon_path=chaturbate_icon)
    elif chat == "del":
        delPerformer(url)
        log_utils.log('Deleting %s from chaturbate monitoring' % (url), log_utils.LOGNOTICE)
        kodi.notify('Chaturbate','Performer removed from monitoring.', sound=True, icon_path=chaturbate_icon)
    xbmc.executebuiltin('Container.Refresh')
        
def addPerformer(name,url,img):
    conn = sqlite3.connect(chaturbatedb)
    conn.text_factory = str
    c = conn.cursor()
    c.execute("INSERT INTO chaturbate VALUES (?,?,?)", (name, url, img))
    conn.commit()
    conn.close()


def delPerformer(url):
    conn = sqlite3.connect(chaturbatedb)
    c = conn.cursor()
    c.execute("DELETE FROM chaturbate WHERE url = '%s'" % url)
    conn.commit()
    conn.close()
 
@utils.url_dispatcher.register('33')
def clearMonitor():

    if os.path.isfile(chaturbatedb):
        choice = xbmcgui.Dialog().yesno(kodi.get_name(), kodi.giveColor('Would you like to clear all history?','white'))
        if choice:
            try: os.remove(chaturbatedb)
            except: kodi.notify(msg='Error removing history.')
            xbmc.executebuiltin("Container.Refresh")
            kodi.notify(msg='Monitoring list reset.')