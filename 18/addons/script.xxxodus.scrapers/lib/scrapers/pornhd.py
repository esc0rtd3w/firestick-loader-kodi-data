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
base_domain  = 'https://www.pornhd.com'
base_name    = base_domain.replace('www.',''); base_name = re.findall('(?:\/\/|\.)([^.]+)\.',base_name)[0].title()
type         = 'video'
menu_mode    = 224
content_mode = 225
player_mode  = 801

search_tag   = 1
search_base  = urlparse.urljoin(base_domain,'search?search=%s')

@utils.url_dispatcher.register('%s' % menu_mode)
def menu():
    
    scraper_updater.check(filename)
    
    try:
        url = urlparse.urljoin(base_domain,'category')
        c = client.request(url)
        r = dom_parser2.parse_dom(c, 'li', {'class': 'category'})
        r = [(dom_parser2.parse_dom(i, 'a', req='href'), \
            dom_parser2.parse_dom(i, 'img', req=['alt','data-original'])) \
            for i in r if i]
        r = [(urlparse.urljoin(base_domain,i[0][0].attrs['href']),i[1][0].attrs['alt'],i[1][0].attrs['data-original']) for i in r]
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
            name = kodi.sortX(i[1].encode('utf-8'))
            icon = xbmc.translatePath(os.path.join('special://home/addons/script.xxxodus.artwork', 'resources/art/%s/icon.png' % filename))
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
        for_np = c
        r = dom_parser2.parse_dom(c, 'li', req='data-thumbIndexes')
        r = [(dom_parser2.parse_dom(i, 'a', {'class': 'title'}), \
            dom_parser2.parse_dom(i, 'time'), \
            i.content) \
            for i in r]
        r = [(urlparse.urljoin(base_domain,i[0][0].attrs['href']), i[0][0].content, i[1][0].content,i[2]) for i in r]
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
            name = '%s - [ %s ]' % (kodi.sortX(i[1].encode('utf-8')).title(),kodi.sortX(i[2].encode('utf-8')))
            if searched: description = 'Result provided by %s' % base_name.title()
            else: description = name
            try:
                pattern = r'''((?:http)([^'"]+)(?:jpg|png|webp))([^'"]*)'''
                icon = re.search(pattern,i[3])
                icon =icon.group(1)
            except: icon = xbmc.translatePath(os.path.join('special://home/addons/script.xxxodus.artwork', 'resources/art/%s/icon.png' % filename))
            content_url = i[0] + '|SPLIT|%s' % base_name
            fanarts = xbmc.translatePath(os.path.join('special://home/addons/script.xxxodus.artwork', 'resources/art/%s/fanart.jpg' % filename))
            dirlst.append({'name': name, 'url': content_url, 'mode': player_mode, 'icon': icon, 'fanart': fanarts, 'description': description, 'folder': False})
        except Exception as e:
            log_utils.log('Error adding menu item %s in %s:: Error: %s' % (i[1].title(),base_name.title(),str(e)), log_utils.LOGERROR)
    
    if dirlst: buildDirectory(dirlst, stopend=True, isVideo = True, isDownloadable = True)
    else:
        if (not searched):
            kodi.notify(msg='No Content Found')
            quit()
        
    if searched: return str(len(r))
    
    if not searched:
        
        try:
            search_pattern = '''\<a\s*href\=['"]([^']+)['"]\>Next'''
            
            pattern = r'''((?:http|https)(\:\/\/)(?:www\.)(pornhd\.com\/category\/)([^\/?]+))'''
            u = re.search(pattern,url)
            u = u.group(0)
            pattern = '''li\s*class\=\"next\s*\"\>\s*\<span class\=\"icon\s*jsFilter\s*js\-link\"\s*data-query\-key\=\"page"\s*data\-query\-value\=\"(\d+)\"\>'''
            np = re.findall(pattern,for_np)[0]
            url = u + '?page=%s|%s' % (np, 'GOT_URL')
            helper.scraper().get_next_page(content_mode,url,search_pattern,filename)
        except Exception as e: 
            log_utils.log('Error getting next page for %s :: Error: %s' % (base_name.title(),str(e)), log_utils.LOGERROR)