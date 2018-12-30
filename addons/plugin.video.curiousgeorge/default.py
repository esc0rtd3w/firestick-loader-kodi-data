# -*- coding: utf-8 -*-
#------------------------------------------------------------
# http://www.youtube.com/user/CuriousGeorgeEnglish
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Based on code from youtube addon
#------------------------------------------------------------

import os
import sys
import plugintools
import xbmcplugin
import xbmcaddon


PLUGIN='plugin.video.curiousgeorge'
YOUTUBE_CHANNEL_ID = "CuriousGeorgeEnglish"
ADDON = xbmcaddon.Addon(id=PLUGIN)

nextpage = xbmc.translatePath(os.path.join('special://home/addons/'+PLUGIN, 'nextpage.png'))

# Entry point
def run():
    
    cmd='plugin://plugin.video.youtube/12?feed=search&path=%2froot%2fsearch&search=curious%20george%20full%20episodes'
    xbmc.executebuiltin('XBMC.Container.Update(%s)' % cmd)
    

    

# Main menu
def main_list(params):
    plugintools.log(YOUTUBE_CHANNEL_ID+" "+repr(params))

    # On first page, pagination parameters are fixed
    if params.get("url") is None:
        params["url"] = "http://gdata.youtube.com/feeds/api/users/"+YOUTUBE_CHANNEL_ID+"/uploads?start-index=1&max-results=10"

    # Fetch video list from YouTube feed
    data = plugintools.read( params.get("url") )
    
    # Extract items from feed
    pattern = ""
    matches = plugintools.find_multiple_matches(data,"<entry>(.*?)</entry>")
    
    for entry in matches:
        
        # Not the better way to parse XML, but clean and easy
        title = plugintools.find_single_match(entry,"<titl[^>]+>([^<]+)</title>")
        plot = plugintools.find_single_match(entry,"<media\:descriptio[^>]+>([^<]+)</media\:description>")
        thumbnail = plugintools.find_single_match(entry,"<media\:thumbnail url='([^']+)'")
        video_id = plugintools.find_single_match(entry,"http\://www.youtube.com/watch\?v\=([^\&]+)\&").replace("&amp;","&")
        url = "plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid="+video_id

        # Appends a new item to the xbmc item list
        plugintools.add_item( action="play" , title=title , plot=plot , url=url ,thumbnail=thumbnail , folder=True )
    
    # Calculates next page URL from actual URL
    start_index = int( plugintools.find_single_match( params.get("url") ,"start-index=(\d+)") )
    max_results = int( plugintools.find_single_match( params.get("url") ,"max-results=(\d+)") )
    next_page_url = "http://gdata.youtube.com/feeds/api/users/"+YOUTUBE_CHANNEL_ID+"/uploads?start-index=%d&max-results=%d" % ( start_index+max_results , max_results)

    plugintools.add_item( action="main_list" , title=">> Next page" , url=next_page_url,thumbnail=nextpage , folder=True )
    setView('movies', 'default') 
    
def setView(content, viewType):
        # set content type so library shows more views and info
        if content:
                xbmcplugin.setContent(int(sys.argv[1]), content)
        if ADDON.getSetting('auto-view') == 'true':#<<<----see here if auto-view is enabled(true) 
                xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting(viewType) )#<<<-----then get the view type
    

def play(params):
    plugintools.play_resolved_url( params.get("url") )

run()
