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

filename     = os.path.basename(__file__).split('.')[0]
base_domain  = 'http://www.streamingporn.xyz'
base_name    = base_domain.replace('www.',''); base_name = re.findall('(?:\/\/|\.)([^.]+)\.',base_name)[0].title()
type         = 'scenes'
menu_mode    = 282
content_mode = 283
player_mode  = 810

search_tag   = 1
search_base  = urlparse.urljoin(base_domain,'?s=%s')

@utils.url_dispatcher.register('%s' % menu_mode,['url'],['searched'])
def menu(url, searched=False):

    try:
        if not url: url = 'http://streamingporn.xyz/stream/'
        c = client.request(url)
        r = dom_parser2.parse_dom(c, 'article', {'id': re.compile('post-\d+')})
        log_utils.log('Scraping Error in %s:: Content of request: %s' % (base_name.title(),str(r)), log_utils.LOGERROR)

        r = [(dom_parser2.parse_dom(i, 'a', req='href'), \
              dom_parser2.parse_dom(i, 'img', req='src')) \
              for i in r if i]
        log_utils.log('Scraping Error in %s:: Content of request: %s' % (base_name.title(),str(r)), log_utils.LOGERROR)
        r = [(i[0][0].attrs['href'], i[0][1].content, i[1][0].attrs['src']) for i in r]
        if ( not r ) and ( not searched ):
            log_utils.log('Scraping Error in %s:: Content of request: %s' % (base_name.title(),str(c)), log_utils.LOGERROR)
            kodi.notify(msg='!!Scraping Error: Info Added To Log File', duration=6000, sound=True)
    except Exception as e:
        if ( not searched ):
            log_utils.log('Fatal Error in %s:: Error: %s' % (base_name.title(),str(e)), log_utils.LOGERROR)
            kodi.notify(msg='Fatal Error', duration=4000, sound=True)
            quit()    
        else: pass

    dirlst = []
    
    for i in r:
        try:
            name = i[1].title()
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
        search_pattern = '''rel\=['"]next['"]\s*href=['"]([^'"]+)\s*'''
        
        helper.scraper().get_next_page(menu_mode,url,search_pattern,filename)