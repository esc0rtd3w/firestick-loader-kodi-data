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
base_domain  = 'http://www.girlfriendvideos.com'
base_name    = base_domain.replace('www.',''); base_name = re.findall('(?:\/\/|\.)([^.]+)\.',base_name)[0].title()
type         = 'video'
menu_mode    = 293
content_mode = 294
player_mode  = 801

search_tag   = 1
search_base  = urlparse.urljoin(base_domain,'search.fcgi?query=%s')

@utils.url_dispatcher.register('%s' % menu_mode)
def menu():
    
    scraper_updater.check(filename)
    
    try:
        url = urlparse.urljoin(base_domain,'categories.php')
        c = client.request(url)
        r = dom_parser2.parse_dom(c, 'a', req='href')
        r = [i for i in r if len(i.content) > 2 and 'pages' in i.attrs['href'] \
             and '0-9' not in i.attrs['href'] and '&nbsp;' not in i.content]
        r = [(urlparse.urljoin(base_domain,i.attrs['href']), i.content) for i in r]
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
            dirlst.append({'name': name, 'url': i[0], 'mode': content_mode, 'icon': icon, 'fanart': fanarts, 'folder': True})
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
        r = dom_parser2.parse_dom(c, 'td', {'width': '25%'})
        r = [(dom_parser2.parse_dom(i, 'a', req='href'), \
              dom_parser2.parse_dom(i, 'img')) for i in r]
        r = [(i[0][0].attrs['href'].replace('/content.fcgi?',''), i[0][0].content, urlparse.urljoin(base_domain,i[1][0].attrs['src'])) for i in r \
              if 'http://www.girlfriendvideos.com' in i[0][0].attrs['href']]
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
            name = kodi.sortX(i[1].encode('utf-8')).title()
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
        
        try:
            search_pattern = '''<a\s*href=['"]([^'"]+)['"]>Next\s*Page<\/a>'''
            parse = re.sub('\d+.php$', '', url)
            helper.scraper().get_next_page(content_mode,url,search_pattern,filename,parse)
        except Exception as e: 
            log_utils.log('Error getting next page for %s :: Error: %s' % (base_name.title(),str(e)), log_utils.LOGERROR)