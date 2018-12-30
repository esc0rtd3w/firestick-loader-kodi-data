# -*- coding: utf-8 -*-
#------------------------------------------------------------
# RadioReference.com
#------------------------------------------------------------
# Based on code from pelisalacarta
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
#------------------------------------------------------------

# Code Upated by: Blazetamer 2014
# Code Updated by: idleloop @ 2014 Oct, 2015 March, 2017 Aug, 2017 Sept

import urlparse,urllib2,urllib,re
import os, sys
import xbmc

from BeautifulSoup import BeautifulSoup

from core import logger
from core import config
from core import scrapertools
from core.item import Item

DEBUG = False
if (config.get_setting("debug") == 'true'):
        DEBUG=True
HLS = True
if (config.get_setting("hls") == 'false'):
        HLS=False
URL = 'https://www.earthcam.com/'
USA_PREFIX_PATCH = 'search/adv_search.php?restrict=1&country[]=United%20States'
WORLDWIDE_PREFIX_PATCH = 'search/adv_search.php?restrict=1&country[]='
EARTHCAM_NAVIGATION_LINK_END = '&vars=0:2359:0:0'

IMAGES = os.path.join(config.get_runtime_path(),"resources")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[channel.py] mainlist")
    itemlist=[]
    itemlist.append( Item(action="cams",  title="Featured Cams" , url=URL ) )
    itemlist.append( Item(action="worldwide", title="Worldwide" , url=URL + WORLDWIDE_PREFIX_PATCH + EARTHCAM_NAVIGATION_LINK_END ) )
    itemlist.append( Item(action="usa",       title="USA" ,       url=URL + USA_PREFIX_PATCH + EARTHCAM_NAVIGATION_LINK_END ) )
    return itemlist

def _get_tree(url, just_get_content = False):

    html = scrapertools.cache_page(url)

    if just_get_content == True: return html

    try:
        tree = BeautifulSoup(html, convertEntities='html')
    except TypeError:
        html = html.decode('utf-8', 'ignore')
        tree = BeautifulSoup(html, convertEntities='html')

    return tree

def worldwide(item):
    logger.info("[channel.py] worldwide")
    itemlist = []
    #bStopNavigation = False

    if (DEBUG): logger.info("url=" + item.url)

    tree = _get_tree( item.url )

    divs = tree.findAll('div', {'class': re.compile(r'.*col\-xs\-.+result_column_[AB].*')})

    (title, thumbnail, url, location, plot) = ('', '', '', '', '')

    for _id, div in enumerate(divs):
        try:
            # column_A (even) contains thumbnail whilst column_B (odd) contains the rest of infos...
            if (_id % 2 == 0):
                # column_A: thumbnail
                thumbnail = div.find('img', {'class': re.compile(r'.*thumbnailImage.*')})['src']
            else:
                # column_B
                url       = div.find('a', {'class': 'camTitle'})['href']
                # discard (almost all) the external links:
                if not re.search( r'(//www.earthcam.com/|//(www.)?youtube.com/)', url ):
                    #bStopNavigation = True
                    #break
                    pass
                title     = div.find('a', {'class': 'camTitle'}).span.string.replace('EarthCam: ', '')
                location  = div.find('div', {'class': 'cam_location'}).string
                plot      = div.find('div', {'class': 'cam_description'}).string
                if plot == None: plot=''
                if (DEBUG): logger.info("%s, %s, %s, %s, %s" % (title, thumbnail, url, location, plot))
                item=Item(action="play", title=title, url=url, thumbnail=thumbnail, 
                    fanart=thumbnail, plot=plot )
                itemlist.append( item )
        except:
            continue

    try:
        links = tree.find('div', {'id': 'pagination_bottom'}).findAll('a')
        logger.info(str(links))
        # next page
        #if bStopNavigation == False or (bStopNavigation == True and len(itemlist)>0):
        link = links[-1]
        if re.search(r'^Next', link.text):
            url = link['href']
            # Unfortunately, until BeautifulSoup 4.2.1 there're problems with double ampersands, so:
            url = URL + USA_PREFIX_PATCH + url[1:]
            logger.info(url)
            item=Item(action="worldwide", title='Next >>' , url=url, thumbnail='', 
                    fanart='', plot='' )
            itemlist.append( item )
    except:
        pass

    return itemlist

def usa(item):
    logger.info("[channel.py] usa")
    itemlist = []
    #bStopNavigation = False

    if (DEBUG): logger.info("url=" + item.url)

    tree = _get_tree( item.url )

    divs = tree.findAll('div', {'class': re.compile(r'.*col-xs-.+result_column_[AB].*')})

    (title, thumbnail, url, location, plot) = ('', '', '', '', '')

    for _id, div in enumerate(divs):
        try:
            # column_A (even) contains thumbnail whilst column_B (odd) contains the rest of infos...
            if (_id % 2 == 0):
                # column_A: thumbnail
                thumbnail = div.find('img', {'class': re.compile(r'.*thumbnailImage.*')})['src']
            else:
                # column_B
                url       = div.find('a', {'class': 'camTitle'})['href']
                # discard (almost all) the external links:
                if not re.search( r'(//www.earthcam.com/|//(www.)?youtube.com/)', url ):
                    #bStopNavigation = True
                    #break
                    pass
                title     = div.find('a', {'class': 'camTitle'}).span.string.replace('EarthCam: ', '')
                location  = div.find('div', {'class': 'cam_location'}).string
                plot      = div.find('div', {'class': 'cam_description'}).string
                if plot == None: plot=''
                if (DEBUG): logger.info("%s, %s, %s, %s, %s" % (title, thumbnail, url, location, plot))
                item=Item(action="play", title=title , url=url, thumbnail=thumbnail, 
                    fanart=thumbnail, plot=plot )
                itemlist.append( item )
        except:
            continue

    try:
        links = tree.find('div', {'id': 'pagination_bottom'}).findAll('a')
        logger.info(str(links))
        # next page
        #if bStopNavigation == False or (bStopNavigation == True and len(itemlist)>0):
        link = links[-1]
        if re.search(r'^Next', link.text):
            url = link['href']
            # Unfortunately, until BeautifulSoup 4.2.1 there're problems with double ampersands, so:
            url = URL + USA_PREFIX_PATCH + url[1:]
            logger.info(url)
            item=Item(action="usa", title='Next >>' , url=url, thumbnail='', 
                    fanart='', plot='' )
            itemlist.append( item )
    except:
        pass

    return itemlist

def cams(item):
    logger.info("[channel.py] cams")
    itemlist = []

    if (DEBUG): logger.info("url=" + item.url)

    #tree = _get_tree( item.url )
    # Ops... some earthcam's wrong html code here mangles BeautifulSoup tree :-(
    html = _get_tree( item.url, just_get_content=True )
    html = html.replace(' ; id=', ' id=')
    try:
        tree = BeautifulSoup(html, convertEntities='html')
    except TypeError:
        html = html.decode('utf-8', 'ignore')
        tree = BeautifulSoup(html, convertEntities='html')

    divs = tree.findAll('div', {'class': re.compile(r'.*homepageplayer-camera.*')})

    for _id, div in enumerate(divs):
        try:
            title     = div.find('img', {'class': re.compile(r'homepage_player_thumb.*')})['alt']
            thumbnail = div.find('img')['src']
            url       = URL + re.search( r'cam_url.*?:.*?//www.earthcam.com/([^"}\']+)', 
                                str(div) ).group(1)
            location  = div.find('div', {'class': 'thumbnailTitle'}).string
            plot      = ''
            if (DEBUG): logger.info("cams : %s, %s, %s, %s, %s" % (title, thumbnail, url, location, plot))
        except:
            continue
        item=Item(action="play", title=title , url=url, thumbnail=thumbnail, 
                fanart=thumbnail, plot=plot )
        itemlist.append( item )

    return itemlist

def previous_play(item, just_check=False):
    itemlist = []

    data = scrapertools.cache_page(item.url)
    if (DEBUG): logger.info("item.url="+item.url)
    # Extracts json info
    json_text=''
    try:
        json_text = scrapertools.get_match(data,'flashvars.path\s+\=\s*"([^"]+)"')
    except Exception, e:
        pass
    if len(json_text) < 100:
        try:
            json_text = (re.search( r'flashvars.json\s+\=\s*"([^"]+)"', data )).group(1)
        except Exception, e:
            pass
    if len(json_text) < 100:
        try:        
            json_text = (re.search( r'json_base\s+\=\s*(.+);', data )).group(1)
        except Exception, e:
            pass
    if len(json_text) < 100:
        try:
            # array of pages for deeper inspection throu new previous_play(): so new folder
            cams = [m.groupdict() for m in 
                (re.finditer( r' href="(?P<url>index.php\?cam=[^"]+)">.+?<img src="(?P<thumbnail>[^"]+)".+?title="(?P<title>[^"]+)"', 
                    data, flags=re.DOTALL))]
            if not cams:
                return []
            if (DEBUG): logger.info("portal of cams=" + str(cams))
            for cam_id in cams:
                new_item=Item(action="previous_play", title=cam_id["title"] , url=item.url + cam_id["url"], thumbnail=cam_id["thumbnail"], 
                    fanart=cam_id["thumbnail"], plot=cam_id["title"] )
                itemlist.append( new_item )
            return itemlist
        except Exception, e:
            logger.info("[earthcam] channel.py " + str(e))
            return []
    if (DEBUG): logger.info("json_text="+json_text)
    if json_text.startswith('%'):
        json_text = urllib.unquote(json_text)
        if (DEBUG): logger.info("json_decoded="+json_text)
    json_object = load_json(json_text)
    if (DEBUG): logger.info("json_object="+str(json_object))
    try:
        cam_data=json_object["cam"]
    except Exception, e:
        return []

    #http://www.earthcam.com/usa/newyork/timessquare/?cam=tsstreet
    #if "?cam=" in item.url:
    #video_url=""
    #try:
    #    # Extract cam_id
    #    cam_id = item.url.split("?")[1].split("=")[1]
    #    logger.info("cam_id="+cam_id)
    #    cam_data=json_object["cam"][cam_id]
    #    if (DEBUG): logger.info("cam_data="+str(cam_data))

    #    offline = cam_data["showOfflineMessage"]
    #    logger.info("offline="+offline)
    #    liveon = cam_data["liveon"]
    #    logger.info("liveon="+liveon)
    
    #    video_url = cam_data["worldtour_path"]
    #    logger.info("video_url="+video_url)
    #    url = calculate_url(video_url)
    #    itemlist.append( Item(action="play", title=item.title , server="directo", url=url, 
    #        fanart=item.thumbnail, thumbnail=item.thumbnail, folder=False) )
    #except:
    #   logger.info("NO cam_id")

    if (DEBUG): logger.info("len(cam_data)=%d" % len(cam_data))
    for cam_id in cam_data:
        if (just_check and len(itemlist)>1): # just checking how menu submenus are here... if >1, info is already enough
            return itemlist
        if (DEBUG): logger.info("cam_id="+str(cam_id))
        liveon = cam_data[cam_id]["liveon"]
        if (DEBUG): logger.info("liveon="+liveon)
        if liveon!="disabled":
            ###video_url = cam_data[cam_id]["worldtour_path"]
            video_url = ''
            try:
                if (HLS):
                    if "html5_streamingdomain" in cam_data[cam_id]:
                        video_url = 'http:' + cam_data[cam_id]["html5_streamingdomain"]
                        if "html5_streampath" in cam_data[cam_id] and  re.search( r'(\.m3u8)$', cam_data[cam_id]["html5_streampath"] ):
                            video_url = video_url + cam_data[cam_id]["html5_streampath"]
                            if (DEBUG): logger.info("html5_stream="+video_url)
                        else:
                            continue
                else:
                    if "worldtour_path" in cam_data[cam_id] and re.search( r'(\.flv|\.mp4|\.jpg|\.png)$', cam_data[cam_id]["worldtour_path"] ):
                        video_url = cam_data[cam_id]["worldtour_path"]
                    elif "livestreamingpath" in cam_data[cam_id] and re.search( r'(\.flv|\.mp4)$', cam_data[cam_id]["livestreamingpath"] ):
                        video_url = cam_data[cam_id]["streamingdomain"] + cam_data[cam_id]["livestreamingpath"]
                    elif "timelapsepath" in cam_data[cam_id] and re.search( r'(\.flv|\.mp4)$', cam_data[cam_id]["timelapsepath"] ):
                        video_url = cam_data[cam_id]["timelapsedomain"] + cam_data[cam_id]["timelapsepath"]
                    elif "archivepath" in cam_data[cam_id] and re.search( r'(\.flv|\.mp4)$', cam_data[cam_id]["archivepath"] ):
                        video_url = cam_data[cam_id]["archivedomain"] + cam_data[cam_id]["archivepath"]
                    else:
                        continue
                #video_url=re.sub(r'(?<!:)//','/',video_url)
                url = calculate_url(video_url)
                try:
                    title=cam_data[cam_id]["title"]
                except Exception, e:
                    title=str(cam_id)
                try:
                    fanart=cam_data[cam_id]["offlineimage"]
                except Exception, e:
                    fanart=''
                    if (DEBUG): logger.info("[channel.py] [play] ERROR: no fanart")
                try:
                    thumbnail=cam_data[cam_id]["thumbimage"]
                except Exception, e:
                    thumbnail=''
                    if (DEBUG): logger.info("[channel.py] [play] ERROR: no thumbnail")
                try:
                    plot = re.sub(r'</?span[^>]*>', '', 
                        cam_data[cam_id]["description"].replace('+', ' '), 
                        flags=re.IGNORECASE )
                    plot = re.sub(r'<[^>]+>', "\n", plot)
                except Exception, e:
                    plot=''
                    if (DEBUG): logger.info("[channel.py] [play] ERROR: no plot")
                itemlist.append( Item(action="play", url=url, thumbnail=thumbnail, title=title, fanart=fanart, plot=plot) )
            except Exception, e:
                if (DEBUG): logger.info("[channel.py] [play] ERROR:"+url)
    
    return itemlist

def play(item):
    itemlist = []
    if re.search( r'//(www.)?youtube.com/', item.url ):
        video_id = re.sub('.+?=', '', item.url)
        xbmc.executebuiltin('PlayMedia(plugin://plugin.video.youtube/play/?video_id=' + video_id + ')')
    elif re.search( r'(\.flv|\.mp4|\.jpg|\.png|\.m3u8)$', item.url ) or item.url.startswith("rtmp"):
        itemlist.append( item )
    else:   # for backward compatitbility with v1.0.7 favorites
        itemlist=previous_play( item )
    return itemlist

def calculate_url(video_url):
    #video_url2 = scrapertools.get_match(json_decoded,'"worldtour_path"\:"([^"]+)"')
    #logger.info("video_url2="+video_url2)
    #video_url = "rtmp://video2.earthcam.com/fecnetwork/hdtimes11.flv"
    #./rtmpdump-2.4 -r "rtmp://video2.earthcam.com/fecnetwork/4828.flv" --swfVfy "http://www.earthcam.com/swf/cam_player_v2/ecnPlayer.swf?20121010" --pageUrl "http://www.earthcam.com/world/turkey/istanbul/" --tcUrl "rtmp://video2.earthcam.com/fecnetwork" --app fecnetwork --live --playpath "4828.flv" -o out.flv
    # Taken from http://forum.xbmc.org/archive/index.php/thread-120418-20.html
    # rtmp://video2.earthcam.com/ app=fecnetwork swfUrl=http://www.earthcam.com/swf/cam_player_v2/ecnPlayer.swf playpath=fridaysHD1.flv live=true timeout=180
    if video_url.lower().endswith(".jpg") or video_url.lower().endswith(".png"):
        url = video_url
    elif video_url.lower().endswith(".m3u8"):
        try:
            m3u8_content = _get_tree(video_url, just_get_content = True)
            url = video_url.replace( 'playlist', re.search(r'^([^#].+)\.m3u8$', m3u8_content, re.MULTILINE).group(1) )
        except:
            url=''
    elif video_url.lower().startswith("http://") or video_url.lower().startswith("https://") or video_url.lower().endswith(".mp4"):
        url = video_url
    else:
        rtmp_url = scrapertools.get_match(video_url,"(rtmp\://[^\/]+/)")
        app = scrapertools.get_match(video_url,"rtmp\://[^\/]+/([a-z]+)/")
        ###playpath = scrapertools.get_match(video_url,"rtmp\://[^\/]+/[a-z]+/([a-zA-Z0-9]+\.flv)")
        playpath = scrapertools.get_match(video_url,"rtmp\://[^\/]+/[a-z]+/(.+\.flv)")
        swfurl = "http://www.earthcam.com/swf/cam_player_v2/ecnPlayer.swf"
        url=rtmp_url + " app=" + app + " swfUrl=" + swfurl + " playpath=" + playpath + " live=true timeout=180"
    if (DEBUG): logger.info("calculated_url="+url)
    return url


def load_json(data):
    # callback to transform json string values to utf8
    def to_utf8(dct):
        rdct = {}
        for k, v in dct.items() :
            if isinstance(v, (str, unicode)) :
                rdct[k] = v.encode('utf8', 'ignore')
            else :
                rdct[k] = v
        return rdct
    try :        
        import json
        json_data = json.loads(data, object_hook=to_utf8)
        return json_data
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line ) 
