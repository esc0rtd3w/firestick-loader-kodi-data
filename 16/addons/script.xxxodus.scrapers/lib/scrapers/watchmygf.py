import xbmc,xbmcplugin,os,urlparse,re
import client
import kodi
import dom_parser2
import log_utils
import scraper_updater
from resources.lib.modules import utils
from resources.lib.modules import helper
buildDirectory = utils.buildDir

filename     = os.path.basename(__file__).split('.')[0]
base_domain  = 'https://www.watchmygf.me'
base_name    = base_domain.replace('www.',''); base_name = re.findall('(?:\/\/|\.)([^.]+)\.',base_name)[0].title()
type         = 'video'
menu_mode    = 262
content_mode = 263
player_mode  = 801

search_tag   = 1
search_base  = urlparse.urljoin(base_domain,'search/%s/')

pictures_tag = 1
pic_men_mode = 264
pic_con_mode = 265
pic_v_mode   = 805

"""""""""
        The section below is dedicated to the video aspect of the scraper 
"""""""""

@utils.url_dispatcher.register('%s' % menu_mode)
def menu():
    
    scraper_updater.check(filename)

    try:
        url = urlparse.urljoin(base_domain,'categories/')
        c = client.request(url)
        r = dom_parser2.parse_dom(c, 'div', {'class': ['item','pic-category']})
        r = [(dom_parser2.parse_dom(i, 'a', req='href'), \
              dom_parser2.parse_dom(i, 'img', req=['src','alt']), \
              dom_parser2.parse_dom(i, 'span', {'class': 'item-stats'})) \
              for i in r if i]
        r = [(i[0][0].attrs['href'], i[1][0].attrs['alt'], i[1][0].attrs['src'], re.findall('.+?(\d+)', re.sub('<.+?>','',i[2][0].content))[0]) for i in r if i]
        if ( not r ):
            log_utils.log('Scraping Error in %s:: Content of request: %s' % (base_name.title(),str(c)), log_utils.LOGERROR)
            kodi.notify(msg='Scraping Error: Info Added To Log File', duration=6000, sound=True)
            quit()
    except Exception as e:
        log_utils.log('Fatal Error in %s:: Error: %s' % (base_name.title(),str(e)), log_utils.LOGERROR)
        kodi.notify(msg='Fatal Error', duration=4000, sound=True)
        quit()
        
    dirlst = []
    
    for i in r:
        try:
            name = kodi.sortX(i[1].encode('utf-8')).title()
            name = name.title() + ' - [ %s ]' % i[3]
            fanarts = xbmc.translatePath(os.path.join('special://home/addons/script.xxxodus.artwork', 'resources/art/%s/fanart.jpg' % filename))
            dirlst.append({'name': name, 'url': i[0], 'mode': content_mode, 'icon': i[2], 'fanart': fanarts, 'folder': True})
        except Exception as e:
            log_utils.log('Error adding menu item %s in %s:: Error: %s' % (i[1].title(),base_name.title(),str(e)), log_utils.LOGERROR)
    
    if dirlst: buildDirectory(dirlst)    
    else:
        kodi.notify(msg='No Menu Items Found')
        quit()
        
@utils.url_dispatcher.register('%s' % content_mode,['url'],['searched'])
def content(url,searched=False):

    try:
        c = client.request(url)
        r = dom_parser2.parse_dom(c, 'div', {'class': ['item','video']})
        r = [(dom_parser2.parse_dom(i, 'a', req='href'), \
              dom_parser2.parse_dom(i, 'img', req=['src','alt']), \
              dom_parser2.parse_dom(i, 'span', {'class': 'duration'})) \
              for i in r if i]
        r = [(i[0][0].attrs['href'], i[1][0].attrs['alt'], i[1][0].attrs['src'], re.sub('<.+?>','',i[2][0].content.replace('\n','').replace(' ',''))) for i in r if i]
        if ( not r ) and ( not searched ):
            log_utils.log('Scraping Error in %s:: Content of request: %s' % (base_name.title(),str(c)), log_utils.LOGERROR)
            kodi.notify(msg='Scraping Error: Info Added To Log File', duration=6000, sound=True)
    except Exception as e:
        if ( not searched ):
            log_utils.log('Fatal Error in %s:: Error: %s' % (base_name.title(),str(e)), log_utils.LOGERROR)
            kodi.notify(msg='Fatal Error', duration=4000, sound=True)
            quit()    
        else: pass

    dirlst = []
    
    for i in r:
        try:
            name = '%s - [ %s ]' % (kodi.sortX(i[1].encode('utf-8')).title(),kodi.sortX(i[3].encode('utf-8')))
            if searched: description = 'Result provided by %s' % base_name.title()
            else: description = name
            content_url = i[0] + '|SPLIT|%s' % base_name
            fanarts = xbmc.translatePath(os.path.join('special://home/addons/script.xxxodus.artwork', 'resources/art/%s/fanart.jpg' % filename))
            dirlst.append({'name': name, 'url': content_url, 'mode': player_mode, 'icon': i[2], 'fanart': fanarts, 'description': description, 'folder': False})
        except Exception as e:
            log_utils.log('Error adding menu item %s in %s:: Error: %s' % (i[1].title(),base_name.title(),str(e)), log_utils.LOGERROR)
    
    if dirlst: buildDirectory(dirlst, stopend=True, isVideo = True, isDownloadable = True)
    else:
        if (not searched):
            kodi.notify(msg='No Content Found')
            quit()
        
    if searched: return str(len(r))
    
    if not searched:
        search_pattern = '''<link\s*href=['"]([^'"]+)['"]\s*rel=['"]next['"]'''
        parse = base_domain
        
        helper.scraper().get_next_page(content_mode,url,search_pattern,filename)
        
"""""""""
        The section below is dedicated to the picture aspect of the scraper 
"""""""""

@utils.url_dispatcher.register('%s' % pic_men_mode, ['url'])
def pic_menu(url=None):
    
    try:
        if ( not url ): url = urlparse.urljoin(base_domain,'photos/popular/')
        c = client.request(url)
        r = dom_parser2.parse_dom(c, 'div', {'class': ['item','photo']})
        r = [(dom_parser2.parse_dom(i, 'a', req=['href','title']), \
              dom_parser2.parse_dom(i, 'img', req='src')) \
              for i in r if i]
        r = [(i[0][0].attrs['href'], i[0][0].attrs['title'], i[1][0].attrs['src']) for i in r if i]
        if ( not r ):
            log_utils.log('Scraping Error in %s:: Content of request: %s' % (base_name.title(),str(c)), log_utils.LOGERROR)
            kodi.notify(msg='Scraping Error: Info Added To Log File', duration=6000, sound=True)
            quit()
    except Exception as e:
        log_utils.log('Fatal Error in %s:: Error: %s' % (base_name.title(),str(e)), log_utils.LOGERROR)
        kodi.notify(msg='Fatal Error', duration=4000, sound=True)
        quit()
        
    dirlst = []
    
    for i in r:
        try:
            name = kodi.sortX(i[1].encode('utf-8')).title()
            fanarts = xbmc.translatePath(os.path.join('special://home/addons/script.xxxodus.artwork', 'resources/art/%s/fanart.jpg' % filename))
            dirlst.append({'name': name, 'url': i[0], 'mode': pic_con_mode, 'icon': i[2], 'fanart': fanarts, 'folder': True})
        except Exception as e:
            log_utils.log('Error adding menu item %s in %s:: Error: %s' % (i[1].title(),base_name.title(),str(e)), log_utils.LOGERROR)
    
    if dirlst:
        buildDirectory(dirlst, stopend=True, pictures=True)    
        search_pattern = '''<link\s*href=['"]([^'"]+)['"]\s*rel=['"]next['"]'''
        parse = base_domain
        helper.scraper().get_next_page(pic_men_mode,url,search_pattern,filename,pictures=True)    
    else:
        kodi.notify(msg='No Menu Items Found')
        quit()
        
@utils.url_dispatcher.register('%s' % pic_con_mode, ['url'])
def pic_content(url):
    
    try:
        c = client.request(url)
        r = dom_parser2.parse_dom(c, 'a', req=['data-w','data-h'])
        r = [(dom_parser2.parse_dom(i, 'img', req=['src','title'])) \
              for i in r if i]
        r = [(i[0].attrs['src'], i[0].attrs['title']) for i in r if i]
        if ( not r ):
            log_utils.log('Scraping Error in %s:: Content of request: %s' % (base_name.title(),str(c)), log_utils.LOGERROR)
            kodi.notify(msg='Scraping Error: Info Added To Log File', duration=6000, sound=True)
            quit()
    except Exception as e:
        log_utils.log('Fatal Error in %s:: Error: %s' % (base_name.title(),str(e)), log_utils.LOGERROR)
        kodi.notify(msg='Fatal Error', duration=4000, sound=True)
        quit()
        
    dirlst = []
    
    for i in r:
        try:
            name = kodi.sortX(i[1].encode('utf-8')).title()
            fanarts = xbmc.translatePath(os.path.join('special://home/addons/script.xxxodus.artwork', 'resources/art/%s/fanart.jpg' % filename))
            dirlst.append({'name': name, 'url': i[0], 'mode': pic_v_mode, 'icon': i[0], 'fanart': fanarts, 'folder': True})
        except Exception as e:
            log_utils.log('Error adding menu item %s in %s:: Error: %s' % (i[1].title(),base_name.title(),str(e)), log_utils.LOGERROR)
    
    if dirlst: 
        buildDirectory(dirlst, stopend=True, pictures=True)    
        search_pattern = '''<a\s*href=['"]([^'"]+)['"]\s*class=['"]pop['"]\s*rel=['"]\d+['"]>NEXT'''
        parse = base_domain
        helper.scraper().get_next_page(pic_con_mode,url,search_pattern,filename,parse,pictures=True)
    else:
        kodi.notify(msg='No Menu Items Found')
        quit()        