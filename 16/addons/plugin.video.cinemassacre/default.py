# Copyright 2014 cdwertmann


# ------------------------------------------------------------------------------
# 2016
# Updated By esc0rtd3w [http://github.com/esc0rtd3w]
# ------------------------------------------------------------------------------

# fanart.jpg source: http://the-great-pipmax.deviantart.com/art/cinemassacre-chainsaw-camera-386865336


import base64
import binascii
import hashlib
import hmac
import os
import re
import sys
import time
import urllib
import urllib2
import urlparse
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
import xmltodict

from datetime import datetime, date
from types import *

# Importing BeautifulSoup
from bs4 import *

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])
PLUGIN_NAME = "plugin.video.cinemassacre"

site_base = "http://cinemassacre.com/"

site_xml = 'site.xml'

try:
    import StorageServer
except:
    import storageserverdummy as StorageServer

# cache for one hour
cache = StorageServer.StorageServer(PLUGIN_NAME, 1)

#cache.table_name = PLUGIN_NAME
#cache.set("some_string", "string")
#save_data = { "some_string": "string", "some_int": 1234, "some_dict": repr({ "our": { "dictionary": [] } }) }
#cache.setMulti("pre-", save_data)

def doNothing():
    nothing=""

# Youtube Video ID (MOSTLY OBSOLETE AS OF 2016)
def videoIdYoutube(value):
    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?.*?(?=v=)v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')

    youtube_regex_match = re.match(youtube_regex, value)
	
    if youtube_regex_match:
        return youtube_regex_match.group(6)

    return youtube_regex_match
	

def getSignature(key, msg):
    return base64.b64encode(hmac.new(key, msg, hashlib.sha1).digest())

def buildUrl(query):
    return base_url + '?' + urllib.urlencode(query)

# Default Log
def log(msg):
    xbmc.log(PLUGIN_NAME + ": "+ str(msg), level=xbmc.LOGNOTICE)

# Log With Additional Text Display
def logPlus(msg, label):
    xbmc.log(PLUGIN_NAME + ": "+ str(label) + str(msg), level=xbmc.LOGNOTICE)


# Read Content From XML
def getContentFromXML():
	
    addon = xbmcaddon.Addon()
    addon_path = addon.getAddonInfo('path')
    _path = os.path.join(addon_path, site_xml)
    f = open(_path, 'r')
    xml = f.read()
    return xmltodict.parse(xml)['document']


def getCategoriesFromXML(content, id):
	
    items = []
	
    #if id=="":
    #    listitem=xbmcgui.ListItem("- All Videos Sorted By Date -", iconImage="DefaultFolder.png")
    #    url = buildUrl({'id': "all"})
    #    items.append((url, listitem, True))

    if id=="all":
        xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_DATE)
    else:
        xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_LABEL)

    for cat in content['MainCategory']:
        if cat['@parent_id'] == id:
            #if cat['@activeInd'] == "N": continue
			
            listitem=xbmcgui.ListItem(cat['@name'], iconImage="DefaultFolder.png")
            url = buildUrl({'id': cat['@id']})
            items.append((url, listitem, True))
    
    if id!="" or id=="all":
        count=0
        for clip in content['item']:
            if clip['movieURL']=="" or clip['@activeInd'] == "N": continue
            cat_tag=clip['categories']['category']
            cat=None
            if type(cat_tag)==DictType:
                if cat_tag['@id']==id: cat=[cat_tag['@id']]
            elif type(cat_tag)==ListType:
                for c in cat_tag:
                    if c['@id']==id: cat=c['@id']

            if not cat and id!="all": continue
            url = clip['movieURL']
			
            if not "http" in url:
                #url = "http://video1.screenwavemedia.com/Cinemassacre/smil:"+url+".smil/playlist.m3u8"
                url = "http://content.jwplatform.com/manifests/"+url+".m3u8"
				
            elif "youtu" in url:
                #url = "plugin://plugin.video.youtube/?action=play_video&videoid="+videoIdYoutube(url)
                url = "plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid="+videoIdYoutube(url)
				
            date=None
            airdate=None
            if clip['pubDate']:
                # python bug http://stackoverflow.com/questions/2609259/converting-string-to-datetime-object-in-python
                d=clip['pubDate'][:-6]
				
                # python bug http://forum.xbmc.org/showthread.php?tid=112916
                try:
                    d=datetime.strptime(d, '%a, %d %b %Y %H:%M:%S')
                except TypeError:
                    d=datetime(*(time.strptime(d, '%a, %d %b %Y %H:%M:%S')[0:6]))

                date=d.strftime('%d.%m.%Y')
                airdate=d.strftime('%Y-%m-%d')
            count+=1
            listitem=xbmcgui.ListItem (clip['title'], thumbnailImage=clip['smallThumbnail'], iconImage='DefaultVideo.png')
            listitem.setInfo( type="Video", infoLabels={ "title": clip['title'], "plot": clip['description'], "aired": airdate, "date": date, "count": count})
            listitem.setProperty('IsPlayable', 'true')
            listitem.addStreamInfo('video', {'duration': clip['duration']})
            items.append((url, listitem, False))

    xbmcplugin.addDirectoryItems(addon_handle,items)
	
	
def getTitle(data):

    try:
        #request = urllib2.Request(web_url + "/page/" + page_num, headers={ 'User-Agent': 'CasperTheFriendlyGhost/v1.0' })
        #html = urllib2.urlopen(request).read()
        #soup = BeautifulSoup(data, "html.parser")
        #link = soup.find('a', 'title')
        #value = link['href']
        #logPlus(value, "value: ")

        return {data}
		

    except:
        error_msg = xbmcgui.Dialog()
        error_msg.ok("Error!", "Could Not Get Title From HTML Source")

	
def findValidLinks(blob):
    
    # Get "Dated" URLs
    get_dated = ("http:\/\/cinemassacre.com\/)([0-9]*?\/[0-9]\/*?[0-9]\/[0-9]+)(\/[A-Za-z])(.+?)")
	
    temp = re.compile(get_dated, re.DOTALL + re.MULTILINE + re.UNICODE)
    temp_link = temp.findall(blob)
    logPlus(temp, "temp: ")
    logPlus(temp_link, "temp_link: ")

    return temp_link
	

def getPageSource(web_url, page_num):
    request = urllib2.Request(web_url + "/page/" + str(page_num), headers={ 'User-Agent': 'CasperTheFriendlyGhost/v1.0' })
    response = urllib2.urlopen(request)
    output = response.read()
    response.close()
    soup = BeautifulSoup(output, "html.parser")
    episodes = soup.findAll("div", class_="archiveitem")
    #logPlus(episodes, "episodes: ")
    return episodes

		
def getPageLinks(web_url, page_num):
	
    request = urllib2.Request(web_url + "/page/" + str(page_num), headers={ 'User-Agent': 'CasperTheFriendlyGhost/v1.0' })
    #blob = urllib2.urlopen(request).read()
    #soup = BeautifulSoup(blob, "html.parser")
	
    response = urllib2.urlopen(request)
    output = response.read()
    #logPlus(output, "output: ")
    response.close()

    soup = BeautifulSoup(output, "html.parser")
    #episodes = soup.findAll("div", {"class": "archiveitem"})
    episodes = soup.findAll("div", class_="archiveitem")
	
    #links = {}
    links=[]
    counter = 0
    for element in episodes:
        #links[element.a.get_text()] = {}
        #links[element.a.get_text()]["href"] = element.a["href"]
        #links[element.a.get_text()]["title"] = element.a["title"]
        
        if counter < 50:
            link = episodes[counter].a["href"]
            counter += 1
            links.append(link)
		
    return links
	
	
def processLinks(page_base, page_max):

    page_counter = 1
    links = []
    while page_counter <= page_max:
        link = getPageLinks(site_base + page_base, str(page_counter))
        page_counter += 1
        links.append(link)
	
    return links
	
	
def processLinksAlt(page_base, page_start, page_max):

    page_counter = page_start
    links = []
    while page_counter <= page_max:
        link = getPageLinks(site_base + page_base, str(page_counter))
        page_counter += 1
        links.append(link)
	
    return links
	

def dumpPageByDate():
    
    more_data = "0"
    #cur_page = "0"
    #max_page = "20"
	
    # # By Date
    # cur_day = "0"
    # max_day = "31"
    # cur_month = "0"
    # max_month = "12"
    # cur_year = "2005"
    # max_year = "2016"
    # cur_date = "0"
    # max_date = max_year + "/" + max_month + "/" + max_day
	
    # while cur_year <= max_year:
	
        # cur_day = cur_day + 1
	
        # cur_date = cur_year + "/" + cur_month + "/" + cur_day
        # cur_link = site_base + "/" + cur_date + "/"
		
        # if cur_day == max_day:
            # cur_month += 1
            # #break
		
        # if cur_month == max_month:
            # cur_year += 1
            # #break
		
        # if cur_year == max_year:
            # more_data = "1"
        # break
			
        # # Advance Page Forward
        # cur_page += 1
		
        # pageDump(site_base + "/" + cur_year + "/", cur_page)
        # pageDump(site_base + "/" + cur_year + "/" + cur_month + "/", cur_page)
        # pageDump(site_base + "/" + cur_year + "/" + cur_month + "/" + cur_day + "/", cur_page)
	
        # logPlus(cur_date, "cur_date: ")
        # logPlus(cur_link, "cur_link: ")
        # logPlus(cur_page, "cur_page: ")
        # logPlus(cur_day, "cur_day: ")
        # logPlus(cur_month, "cur_month: ")
        # logPlus(cur_year, "cur_year: ")
	
	
def dumpPageShows(show):
	
    # Angry Video Game Nerd
    if show == "avgn":
        links = processLinks("category/avgn/avgnepisodes", 6)
        #logPlus(links, "Links (SHOWS -> Angry Video Game Nerd): ")
	
    # James and Mike Mondays
    if show == "jamm":
        links = processLinks("category/jamesandmike", 7)
        #logPlus(links, "Links (SHOWS -> James and Mike Mondays): ")
	
    # Mike and Ryan
    if show == "mar":
        links = processLinks("category/mikeryantalkaboutgames", 1)
        #logPlus(links, "Links (SHOWS -> Mike and Ryan): ")
	
    # Mike and Bootsy
    if show == "mab":
        links = processLinks("category/mike-bootsy", 1)
        #logPlus(links, "Links (SHOWS -> Mike and Bootsy): ")
	
    # Board James
    if show == "bj":
        links = processLinks("category/boardjames", 1)
        #logPlus(links, "Links (SHOWS -> Board James): ")
	
    # You Know Whats Bullshit
    if show == "ykwb":
        links = processLinks("category/ykwb", 2)
        #logPlus(links, "Links (SHOWS -> You Know Whats Bullshit): ")
	
    return links
	
	
def dumpPageGames(show):
	
    # Mikes Gaming Videos
    if show == "mgv":
        links = processLinks("category/mikevideos", 3)
        #logPlus(links, "Links (GAMES -> Mikes Gaming Videos): ")
	
    # Bootsy Beats
    if show == "bb":
        links = processLinks("category/bootsy-beats", 1)
        #logPlus(links, "Links (GAMES -> Bootsy Beats): ")
	
    # James Gaming Videos
    if show == "jgv":
        links = processLinks("category/jamesgamingvideos", 1)
        #logPlus(links, "Links (GAMES -> James Gaming Videos): ")
	
    # Other Gaming Videos
    if show == "ogv":
        links = processLinks("category/othergaming-videos", 1)
        #logPlus(links, "Links (GAMES -> Other Gaming Videos): ")
	
    return links
	
	
def dumpPageMovies(show):
	
    # Movie Reviews A-Z
    if show == "mraz":
        links = processLinks("category/moviereviewsatoz", 13)
        #logPlus(links, "Links (MOVIES -> Movie Reviews A-Z): ")
	
    # Top Tens
    if show == "mrtt":
        links = processLinks("category/moviereviews/top-tens", 1)
        #logPlus(links, "Links (MOVIES -> Top Tens): ")
	
    # Animation Related
    if show == "mrar":
        links = processLinks("category/moviereviews/animation-moviereviews", 1)
        #logPlus(links, "Links (MOVIES -> Animation Related): ")
	
    # Commentaries
    if show == "mrc":
        links = processLinks("category/moviereviews/commentaries", 1)
        #logPlus(links, "Links (MOVIES -> Commentaries): ")
	
    # Interviews
    if show == "mri":
        links = processLinks("category/moviereviews/interviews", 1)
        #logPlus(links, "Links (MOVIES -> Interviews): ")
	
    # Location Tours
    if show == "mrlt":
        links = processLinks("category/moviereviews/location-tours", 1)
        #logPlus(links, "Links (MOVIES -> Location Tours): ")
	
    # Monster Madness
    if show == "mrmm":
        links_mrmm = processLinks("category/moviereviews/monstermadness", 12)
        #logPlus(links_mrmm, "Links (MOVIES -> Monster Madness): ")
	
    # Trivia Videos
    if show == "mrtv":
        links = processLinks("category/moviereviews/trivia-videos", 1)
        #logPlus(links, "Links (MOVIES -> Trivia Videos): ")
	
    # Other Movie Related Videos
    if show == "mromrv":
        links = processLinks("category/moviereviews/othermovierelatedvideos", 1)
        #logPlus(links, "Links (MOVIES -> Other Movie Related Videos): ")
	
    return links
	
	
def dumpPageFilm(show):
	
    # Original Films Main
    if show == "film":
        links = processLinks("category/films", 4)
        #logPlus(links, "Links (ORIGINAL FILMS -> Main): ")
	
    # Favorites
    if show == "filmfav":
        links = processLinks("category/films/favorites", 1)
        #logPlus(links, "Links (ORIGINAL FILMS -> Favorites): ")
	
    # Animation
    if show == "filmani":
        links = processLinks("category/films/animation", 1)
        #logPlus(links, "Links (ORIGINAL FILMS -> Animation): ")
	
    # Horror Films
    if show == "filmhorror":
        links = processLinks("category/films/horror-films", 2)
        #logPlus(links, "Links (ORIGINAL FILMS -> Horror Films): ")
	
    # Comedy
    if show == "filmcomedy":
        links = processLinks("category/films/comedy", 1)
        #logPlus(links, "Links (ORIGINAL FILMS -> Comedy): ")
	
    # 48-Hour Films
    if show == "film48":
        links = processLinks("category/films/48-hour-films", 1)
        #logPlus(links, "Links (ORIGINAL FILMS -> 48 Hour Films): ")
	
    # Other
    if show == "filmother":
        links = processLinks("category/films/other", 1)
        #logPlus(links, "Links (ORIGINAL FILMS -> Other): ")
	
    return links
	

def dumpPageMusic(show):
	
    # Music Main
    if show == "mus":
        links = processLinks("category/music-2", 1)
        #logPlus(links, "Links (MUSIC -> Main): ")
	
    # Audio Slaughter
    if show == "musas":
        links = processLinks("category/music-2/audio-slaughter", 1)
        #logPlus(links, "Links (MUSIC -> Audio Slaughter): ")
	
    # Kyle Justin
    if show == "musjk":
        links = processLinks("category/music-2/kylejustin", 1)
        #logPlus(links, "Links (MUSIC -> Kyle Justin): ")
	
    # Name That Tune
    if show == "musntt":
        links = processLinks("category/music-2/namethattune", 1)
        #logPlus(links, "Links (MUSIC -> Name That Tune): ")
	
    return links
	

def dumpPageSite(show):
    
    # Site Main
    if show == "site":
        links = processLinks("category/site-2", 1)
        #logPlus(links, "Links (SITE -> Main): ")
	
    # Articles
    if show == "sitearticles":
        links = processLinks("category/site-2/featuredarticles", 1)
        #logPlus(links, "Links (SITE -> Articles): ")
	
    # Appearances
    if show == "siteappear":
        links = processLinks("category/site-2/appearances", 1)
        #logPlus(links, "Links (SITE -> Appearances): ")
	
    # Misc Videos
    if show == "sitemisc":
        links = processLinks("category/site-2/misc-videos", 1)
        #logPlus(links, "Links (SITE -> Misc Videos): ")
	
    return links
	
	
def dumpPageAll():

    dumpPageShows()
    dumpPageGames()
    dumpPageMovies()
    dumpPageFilm()
    dumpPageMusic()
    dumpPageSite()


try:

    #dumpPageAll()
    source = getPageSource(site_base + "category/avgn/avgnepisodes", 1)
    #links_valid = findValidLinks(source)
    logPlus(findValidLinks(source), "links_valid: ")
	
    #start = 0
    #stop = 1
    #for link in dumpPageShows("avgn"):
        #length = len(link)
        #if stop <= length:
            #logPlus(link[start:stop], "link: ")
            #start += 1
            #stop += 1
	
except:
    doNothing()

xbmcplugin.setContent(addon_handle, "episodes")
id = ''.join(args.get('id', ""))
content = cache.cacheFunction(getContentFromXML)
getCategoriesFromXML(content, id)

xbmcplugin.endOfDirectory(addon_handle)

# Media Info View
xbmc.executebuiltin('Container.SetViewMode(504)')
