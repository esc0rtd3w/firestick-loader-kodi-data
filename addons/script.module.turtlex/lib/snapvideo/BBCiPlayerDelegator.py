'''
Created on Jun 29, 2012

@author: ajju
'''
from common import Logger
from common.DataObjects import VideoHostingInfo, VideoInfo, VIDEO_QUAL_SD
import xbmcaddon  # @UnresolvedImport
import xbmcgui  # @UnresolvedImport


def getVideoHostingInfo():
    video_hosting_info = VideoHostingInfo()
    video_hosting_info.set_video_hosting_image('')
    video_hosting_info.set_video_hosting_name('BBC add-on by Hitcher')
    return video_hosting_info

def retrieveVideoInfo(videoUrl):
    try: 
        xbmcaddon.Addon('plugin.video.iplayer')
    except: 
        dialog = xbmcgui.Dialog()
        dialog.ok('[B][COLOR red]MISSING: [/COLOR][/B] BBC IPlayer v2 add-on', '', 'Please install BBC IPlayer v2 add-on created by Hitcher!', 'Available at http://code.google.com/p/xbmc-iplayerv2/')
        raise
    video_info = VideoInfo()
    video_info.set_video_hosting_info(getVideoHostingInfo())
    video_info.set_video_id(videoUrl)
    addon_url = 'plugin://plugin.video.iplayer/?'
    video_params = videoUrl.split('/')
    
    addon_url += 'pid=%s' % video_params[0]
    video_info.add_video_link(VIDEO_QUAL_SD, addon_url, addUserAgent=False, addReferer=False)
    video_info.set_video_image('http://www.bbc.co.uk/iplayer/images/episode/%s_512_288.jpg' % video_params[0])
    video_info.set_video_name(video_params[1].replace('_', ' '))
    
    Logger.logDebug(addon_url)
    video_info.set_video_stopped(False)
    return video_info
