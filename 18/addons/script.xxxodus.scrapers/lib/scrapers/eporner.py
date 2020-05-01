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
base_domain  = 'https://eporner.com'
base_name    = base_domain.replace('www.',''); base_name = re.findall('(?:\/\/|\.)([^.]+)\.',base_name)[0].title()
type         = 'video'
menu_mode    = 200
content_mode = 201
player_mode  = 801

search_tag   = 1
search_base  = urlparse.urljoin(base_domain,'search/%s')

@utils.url_dispatcher.register('%s' % menu_mode)
def menu():
    
    scraper_updater.check(filename)
    
    url           = urlparse.urljoin(base_domain,'0')
    content_type  = 'dir'
    title_pattern = '''<strong>([^<]+)'''
    url_pattern   = '''href="([^"]+)'''
    icon_pattern  = None
    d_p1          = 'li'
    d_p2          = 'class'
    d_p3          = ''
    parse         = '%s|SPLIT|url' % base_domain
    cache_time    = 4
    
    helper.scraper().get_list(content_mode,content_type,url,title_pattern,url_pattern,icon_pattern,filename,d_p1,d_p2,d_p3,parse,cache_time)

@utils.url_dispatcher.register('%s' % content_mode,['url'],['searched'])
def content(url,searched=False):

    try:
        c = client.request(url)
        r = dom_parser2.parse_dom(c, 'div', {'class': 'mb'})
        r = [(dom_parser2.parse_dom(i, 'a', req=['href', 'title']),dom_parser2.parse_dom(i, 'img', req=['src'])) for i in r if r]
        r = [(urlparse.urljoin(base_domain,i[0][0].attrs['href']),i[0][0].attrs['title'],i[1][0].attrs['src']) for i in r]
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
            name = kodi.sortX(i[1].encode('utf-8'))
            if searched: description = 'Result provided by %s' % base_name.title()
            else: description = name
            content_url = i[0] + '|SPLIT|%s' % base_name
            fanarts = xbmc.translatePath(os.path.join('special://home/addons/script.xxxodus.artwork', 'resources/art/%s/fanart.jpg' % filename))
            dirlst.append({'name': name, 'url': content_url, 'mode': player_mode, 'icon': i[2], 'fanart': fanarts, 'description': description, 'folder': False})
        except Exception as e:
            log_utils.log('Error adding menu item %s in %s:: Error: %s' % (i[0].title(),base_name.title(),str(e)), log_utils.LOGERROR)
    
    if dirlst: buildDirectory(dirlst, stopend=True, isVideo = True, isDownloadable = True)
    else:
        if (not searched):
            kodi.notify(msg='No Content Found')
            quit()
        
    if searched: return str(len(r))
    
    if not searched:
        search_pattern = '''href=['"]+([^'"]+)['"]\s+title=['"]Next'''
        parse = base_domain
        
        helper.scraper().get_next_page(content_mode,url,search_pattern,filename,parse)