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
base_domain  = 'https://www.porndig.com'
base_name    = base_domain.replace('www.',''); base_name = re.findall('(?:\/\/|\.)([^.]+)\.',base_name)[0].title()
type         = 'video'
menu_mode    = 246
content_mode = 247
player_mode  = 801

search_tag   = 0
search_base  = urlparse.urljoin(base_domain,'/amateur/search/%s')

@utils.url_dispatcher.register('%s' % menu_mode)
def menu():
    
    scraper_updater.check(filename)
    
    try:
        url = urlparse.urljoin(base_domain,'video')
        c = client.request(url)
        r = dom_parser2.parse_dom(c, 'a', {'class': 'sidebar_section_item'})
        r = [i for i in r if 'channels' in i.attrs['href']]        
        r = [(urlparse.urljoin(base_domain,i.attrs['href']), i.content + ' - [ Professional ]') for i in r]
        url = urlparse.urljoin(base_domain,'amateur/videos/')
        c = client.request(url)
        e = dom_parser2.parse_dom(c, 'a', {'class': 'sidebar_section_item'})
        e = [i for i in e if 'channels' in i.attrs['href']]
        r += [(urlparse.urljoin(base_domain,i.attrs['href']), i.content + ' - [ Amateur ]') for i in e]        
        r = sorted(r, key=lambda x: x[1])
        if ( not r ):
            log_utils.log('Scraping Error in %s:: Content of request: %s' % (base_name.title(),str(c)), log_utils.LOGERROR)
            kodi.notify(msg='Scraping Error: Info Added To Log File', duration=6000, sound=True)
            quit()
    except Exception as e:
        log_utils.log('Fatal Error in %s:: Error: %s' % (base_name.title(),str(e)), log_utils.LOGERROR)
        kodi.notify(msg='Fatal Error', duration=4000, sound=True)
        quit()

    dirlst = []
    urls = []
    for i in r:
        try:
            if ( not i[0] in str(urls) ):
                urls.append(i[0])
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
        r = dom_parser2.parse_dom(c, 'div', {'id': re.compile('category_videos_\d+')})
        r = [(dom_parser2.parse_dom(i, 'a', req=['href','title']), \
            dom_parser2.parse_dom(i, 'span', {'class': 'pull-left'}), \
            dom_parser2.parse_dom(i, 'img', req='src')) \
            for i in r if i]
        r = [(urlparse.urljoin(base_domain,i[0][0].attrs['href']), i[0][0].attrs['title'], i[1][0].content, i[2][0].attrs['src']) for i in r]
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
            content_url = i[0] + '|SPLIT|%s' % base_name
            fanarts = xbmc.translatePath(os.path.join('special://home/addons/script.xxxodus.artwork', 'resources/art/%s/fanart.jpg' % filename))
            dirlst.append({'name': name, 'url': content_url, 'mode': player_mode, 'icon': i[3], 'fanart': fanarts, 'description': description, 'folder': False})
        except Exception as e:
            log_utils.log('Error adding menu item %s in %s:: Error: %s' % (i[1].title(),base_name.title(),str(e)), log_utils.LOGERROR)
    
    if dirlst: buildDirectory(dirlst, stopend=False, isVideo = True, isDownloadable = True)
    else:
        if (not searched):
            kodi.notify(msg='No Content Found')
            quit()
        
    if searched: return str(len(r))