import xbmc,xbmcplugin,os,urlparse,re
import client
import kodi
import dom_parser2
import log_utils
import scraper_updater
from resources.lib.modules import utils
from resources.lib.modules import helper
from resources.lib.modules import linkfinder
buildDirectory = utils.buildDir

filename     = 'xtheatre'
base_domain  = 'https://xtheatre.net'
base_name    = base_domain.replace('www.',''); base_name = re.findall('(?:\/\/|\.)([^.]+)\.',base_name)[0].title()
type         = 'movies'
menu_mode    = 291
player_mode  = 810
        
@utils.url_dispatcher.register('%s' % menu_mode, ['url'])
def content(url):

    try:
        if not url: url = 'https://xtheatre.net/?filtre=date&cat=0'
        c = client.request(url)
        r = dom_parser2.parse_dom(c, 'li', {'class': ['border-radius-5','box-shadow']})
        r = [(dom_parser2.parse_dom(i, 'a', req=['href','title']), \
              dom_parser2.parse_dom(i, 'p'), \
              dom_parser2.parse_dom(i, 'img', req='data-lazy-src')) \
              for i in r if i]
        r = [(i[0][0].attrs['href'], i[0][0].attrs['title'], i[1][0].content, \
              i[2][0].attrs['data-lazy-src']) for i in r]
        if ( not r ):
            log_utils.log('Scraping Error in %s:: Content of request: %s' % (base_name.title(),str(c)), log_utils.LOGERROR)
            kodi.notify(msg='Scraping Error: Info Added To Log File', duration=6000, sound=True)
    except Exception as e:
        log_utils.log('Fatal Error in %s:: Error: %s' % (base_name.title(),str(e)), log_utils.LOGERROR)
        kodi.notify(msg='Fatal Error', duration=4000, sound=True)
        quit()    

    dirlst = []
    
    for i in r:
        try:
            name = kodi.sortX(i[1].title())
            description = kodi.sortX(i[2])
            content_url = i[0] + '|SPLIT|%s' % base_name
            fanarts = xbmc.translatePath(os.path.join('special://home/addons/script.xxxodus.artwork', 'resources/art/%s/fanart.jpg' % filename))
            dirlst.append({'name': name, 'url': content_url, 'mode': player_mode, 'icon': i[3], 'fanart': fanarts, 'description': description, 'folder': False})
        except Exception as e:
            log_utils.log('Error adding menu item %s in %s:: Error: %s' % (i[1].title(),base_name.title(),str(e)), log_utils.LOGERROR)
    
    if dirlst: buildDirectory(dirlst, stopend=True, isVideo = True, isDownloadable = True)
    else:
        kodi.notify(msg='No Content Found')
        quit()

    search_pattern = '''<a\s*href=['"]([^'"]+)['"]>Next'''
    helper.scraper().get_next_page(menu_mode,url,search_pattern,filename)