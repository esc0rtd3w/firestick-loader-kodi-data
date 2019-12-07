# -*- coding: utf-8 -*-
#------------------------------------------------------------
# RadioReference.com
#------------------------------------------------------------
# Based on code from pelisalacarta
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
#------------------------------------------------------------

# Code Upated by: Blazetamer 2014
# Code Updated by: idleloop @ 2014 Oct, 2015 March, 2017 Aug, 2017 Sept, 2019 Jan

import urlparse,urllib2,urllib,re
import os, sys
from random import randint
import time
import xbmc
import xbmcgui

# //kodi.wiki/index.php?title=Add-on:Parsedom_for_xbmc_plugins
from CommonFunctions import parseDOM, stripTags

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
PLACES_URL = URL + 'network/'
SEARCH_URL = 'search/ft_search.php?_sbox=1&s1=1&term='
RESULTS_URL= 'search/ft_search.php?_sbox=1&s1=1&'

IMAGES = os.path.join(config.get_runtime_path(),"resources")


def isGeneric():
    return True


def mainlist(item):
    if (DEBUG): ("[channel.py] mainlist")
    itemlist=[]
    itemlist.append( Item(action="cams",  title="Featured Cams" , url=PLACES_URL ) )
    itemlist.append( Item(action="places", title="Places" , url=PLACES_URL ) )
    itemlist.append( Item(action="searching",    title="Search" ,    url='' ) )
    return itemlist


def searching( action ):
    dialog = xbmcgui.Dialog()
    search_term = dialog.input(heading='Type term of serch for EarthCam :', type=xbmcgui.INPUT_ALPHANUM)
    del dialog
    search_term = search_term.replace( ' ', '+' )
    if len(search_term)==0:
        return []
    url = URL + SEARCH_URL + search_term
    return _get_category( Item( action = "searching", title="Search results", url=url ), 'search' )


def _get_html(url, retries=5):
    url = url.replace( ' ', '%20' )
    return scrapertools.cache_page( url )


def _get_category(item, category):
    itemlist = []

    if (DEBUG): logger.info("url=" + item.url)

    html = _get_html( item.url )

    divs = parseDOM( html, 'div', attrs={'class': '[^\'"]*?col\-xs\-[^\'"]+?result_column_[AB][^\'"]*'})

    (title, thumbnail, url, location, plot) = ('', '', '', '', '')

    if divs:
        for _id, div in enumerate( divs ):
            try:
                # column_A (even) contains thumbnail whilst column_B (odd) contains the rest of infos...
                if ( _id % 2 == 0 ):
                    # column_A: thumbnail
                    thumbnail = parseDOM( div, 'img', attrs={'class': '[^\'"]*thumbnailImage[^\'"]*'}, ret='src' )[0].replace('256x144', '512x288').replace('128x72', '256x144')
                else:
                    # column_B
                    url       = parseDOM( div, 'a', attrs={'class': 'camTitle'}, ret='href' )[0]
                    # discard (almost all) the external links:
                    if not re.search( r'(//www.earthcam.com/|//(www.)?youtube.com/)', url ):
                        #bStopNavigation = True
                        #break
                        continue
                    title     = parseDOM( parseDOM( div, 'a', attrs={'class': 'camTitle'} ), 'span' )[0].replace('EarthCam: ', '')
                    location  = parseDOM( div, 'div', attrs={'class': 'cam_location'} )[0]
                    plot      = parseDOM( div, 'div', attrs={'class': 'cam_description'} )[0]
                    if plot == None: plot=''
                    if (DEBUG): logger.info("%s, %s, %s, %s, %s" % (title, thumbnail, url, location, plot))
                    item=Item(action="play", title=title, url=url, thumbnail=thumbnail,
                        fanart=thumbnail, plot=plot )
                    itemlist.append( item )
            except:
                continue
    else:
        divs = parseDOM( html, 'div', attrs={'class': r'[^\'"]*?col\-xs\-12' } )
        zone = parseDOM( html, 'p', attrs={ 'class': 'pageTitle' } )[0].replace(':', '')
        for _id, div in enumerate( divs ):
            thumbnail = parseDOM( div, 'img', ret='src' )[0].replace('256x144', '512x288').replace('128x72', '256x144')
            url       = parseDOM( div, 'a', ret='href' )[0]
            title     = parseDOM( div, 'span', attrs={'class': 'featuredTitle'} )[0]
            location  = parseDOM( div, 'div', attrs={ 'class': 'featuredCity' } )[0] + ', ' + zone
            plot      = title + "\n(" + location + ')'
            if plot == None: plot=''
            if (DEBUG): logger.info("%s, %s, %s, %s, %s" % (title, thumbnail, url, location, plot))
            item=Item(action="play", title=title, url=url, thumbnail=thumbnail,
                fanart=thumbnail, plot=plot )
            itemlist.append( item )

    try:
        links = parseDOM( parseDOM( html, 'div', attrs={'id': 'pagination_bottom'} ), 'a', ret='href' )
        links_text = parseDOM( parseDOM( html, 'div', attrs={'id': 'pagination_bottom'} ), 'a' )
        link = links[-1]
        if re.search(r'^Next', links_text[-1]):
            url = link
            if category.startswith('search'):
                url = URL + RESULTS_URL + url[1:]
                category = 'search_results'
            else:
                url = URL + PREFIX_PATCH + url[1:]
            if (DEBUG): (url)
            item=Item(action=category, title='Next >>' , url=url, thumbnail='',
                    fanart='', plot='' )
            itemlist.append( item )
    except:
        pass

    return itemlist


def search_results(item):
    if (DEBUG): ("[channel.py] search_results")
    return _get_category( item, 'search_results' )


def place(item):
    if (DEBUG): ("[channel.py] place")
    return _get_category( item, 'place' )


def places(item):
    if (DEBUG): ("[channel.py] places")
    itemlist = []
    html = _get_html( item.url )
    places = parseDOM( html, 'a', attrs={'class': 'locationLink'} )
    places_url = parseDOM( html, 'a', attrs={'class': 'locationLink'}, ret='href' )
    for _id, place in enumerate( places ):
        title = place
        url   = PLACES_URL + places_url[_id]
        item=Item(action='place', title=title , url=url, thumbnail='',
                    fanart='', plot='' )
        itemlist.append( item )
    return itemlist


# featured cams
def cams(item):
    if (DEBUG): ("[channel.py] cams")
    itemlist = []

    if (DEBUG): logger.info("url=" + item.url)

    html = _get_html( item.url )
    divs = parseDOM( html, 'div', attrs={'class': r'[^\'"]*?col\-xs\-12' } )
    for _id, div in enumerate( divs ):
        thumbnail = parseDOM( div, 'img', ret='src' )[0].replace('256x144', '512x288').replace('128x72', '256x144')
        url       = parseDOM( div, 'a', ret='href' )[0]
        if 'www.earthcam.com' not in url or 'alexa' in url or 'myearthcam' in url:
            continue
        title     = parseDOM( div, 'span', attrs={'class': 'featuredTitle'} )[0]
        location  = parseDOM( div, 'div', attrs={ 'class': 'featuredCity' } )[0]
        plot      = title + "\n(" + location + ')'
        if plot == None: plot=''
        if (DEBUG): logger.info("%s, %s, %s, %s, %s" % (title, thumbnail, url, location, plot))
        item=Item(action="play", title=title, url=url, thumbnail=thumbnail,
            fanart=thumbnail, plot=plot )
        itemlist.append( item )

    # more cameras from front page
    if (DEBUG): logger.info("url=" + URL)

    html = _get_html( URL )
    divs = parseDOM( html, 'div', attrs={ 'class': '[^\'"]*?camera_block[^\'"]*?' } )

    for _id, div in enumerate(divs):
        if not re.search( r'//www.earthcam.com/[^"}\']+?\?cam=', div ):
            continue
        try:
            title     = parseDOM( div, 'img', ret='title')[0].replace('EarthCam: ','')
            thumbnail = parseDOM( div, 'img', ret='src')[0].replace('256x144', '512x288').replace('128x72', '256x144')
            url       = URL + re.search( r'//www.earthcam.com/([^"}\']+)', div ).group(1)
            location  = parseDOM( div, 'div', attrs={ 'class': '[^\'"]*?thumbnailTitle[^\'"]*?' } )[0]
            plot      = title
            if (DEBUG): logger.info("cams : %s, %s, %s, %s, %s" % (title, thumbnail, url, location, plot))
        except:
            continue
        item=Item(action="play", title=title , url=url, thumbnail=thumbnail,
                fanart=thumbnail, plot=plot )
        itemlist.append( item )
        #if _id >= 12:
        #    break

    return itemlist


def previous_play(item, just_check=False):
    itemlist = []

    data = _get_html( item.url )
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
                new_item=Item(action="previous_play", title=cam_id["title"] , url=item.url + cam_id["url"],
                    thumbnail=cam_id["thumbnail"].replace('256x144', '512x288').replace('128x72', '256x144'),
                    fanart=cam_id["thumbnail"].replace('256x144', '512x288').replace('128x72', '256x144'), plot=cam_id["title"] )
                itemlist.append( new_item )
            return itemlist
        except Exception, e:
            if (DEBUG): ("[earthcam] channel.py " + str(e))
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
                        video_url = cam_data[cam_id]["html5_streamingdomain"]
                        if not re.search( r'^http', video_url ): video_url = 'http://' + video_url
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
                    fanart=cam_data[cam_id]["thumbimage2"].replace('256x144', '512x288').replace('128x72', '256x144').replace(r'\\', '')
                except Exception, e:
                    fanart=''
                    if (DEBUG): logger.info("[channel.py] [play] ERROR: no fanart")
                try:
                    thumbnail=cam_data[cam_id]["thumbimage"].replace('256x144', '512x288').replace('128x72', '256x144').replace(r'\\', '')
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
        if re.search('(/channel/.+)', item.url):
            channel = re.search('(/channel/.+)', item.url).group(1) + '/playlists/'
            xbmc.executebuiltin('PlayMedia(plugin://plugin.video.youtube' + channel + ')')
        elif re.search('/c/(.+)/live', item.url):
            channel = re.search('/c/(.+)/live', item.url).group(1) + '/'
            xbmc.executebuiltin('PlayMedia(plugin://plugin.video.youtube/user/' + channel + ')')
        else:
            video_id = re.sub('.+?=', '', item.url)
            xbmc.executebuiltin('PlayMedia(plugin://plugin.video.youtube/play/?video_id=' + video_id + ')')
    elif re.search( r'(\.flv|\.mp4|\.jpg|\.png|\.m3u8)$', item.url ) or item.url.startswith("rtmp"):
        itemlist.append( item )
    else:   # for backward compatitbility with v1.0.7 favorites
        itemlist=previous_play( item )
    return itemlist


def calculate_url(video_url):
    if video_url.lower().endswith(".jpg") or video_url.lower().endswith(".png"):
        url = video_url
    elif video_url.lower().endswith(".m3u8"):
        try:
            m3u8_content = _get_html( video_url )
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
        swfurl = "https://www.earthcam.com/swf/cam_player_v2/ecnPlayer.swf"
        url=rtmp_url + " app=" + app + " swfUrl=" + swfurl + " playpath=" + playpath + " live=true timeout=10"
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
