'''
Created on Oct 29, 2011

@author: ajju
'''
from common import HttpUtils, Logger
from common.DataObjects import VideoHostingInfo, VideoInfo, VIDEO_QUAL_LOW, \
    VIDEO_QUAL_SD, VIDEO_QUAL_HD_720, VIDEO_QUAL_HD_1080
import YDStreamExtractor

VIDEO_HOSTING_NAME = 'YouTube'

def getVideoHostingInfo():
    video_hosting_info = VideoHostingInfo()
    video_hosting_info.set_video_hosting_image('http://www.automotivefinancingsystems.com/images/icons/socialmedia_youtube_256x256.png')
    video_hosting_info.set_video_hosting_name(VIDEO_HOSTING_NAME)
    return video_hosting_info

def retrieveVideoInfo(video_id):
    
    video_info = VideoInfo()
    video_info.set_video_hosting_info(getVideoHostingInfo())
    video_info.set_video_id(video_id)
    try:
        
        video_url = 'https://www.youtube.com/watch?v=' + video_id
        yd_video_info = YDStreamExtractor.getVideoInfo(video_url, quality=1)
        if yd_video_info is not None:
            video_info.set_video_name(yd_video_info.title)
            video_info.set_video_image(yd_video_info.thumbnail)
            video_info.add_video_link(VIDEO_QUAL_HD_720, yd_video_info.streamURL())
            video_info.set_video_stopped(False)
        else:
            video_info.set_video_stopped(True)
        
    except Exception, e:
        Logger.logError(e)
        video_info.set_video_stopped(True)
    return video_info


def retrievePlaylistVideoItems(playlistId):
    Logger.logFatal('YouTube Playlist ID = ' + playlistId)
    soupXml = HttpUtils.HttpClient().getBeautifulSoup('http://gdata.youtube.com/feeds/api/playlists/' + playlistId + '?max-results=50')
    videoItemsList = []
    for media in soupXml.findChildren('media:player'):
        videoUrl = str(media['url'])
        videoItemsList.append(videoUrl)
    return videoItemsList
    
def retrieveReloadedPlaylistVideoItems(playlistId):
    Logger.logFatal('YouTube Reloaded Playlist ID = ' + playlistId)
    soupXml = HttpUtils.HttpClient().getBeautifulSoup('http://gdata.youtube.com/feeds/api/playlists/' + playlistId)
    videoItemsList = []
    for media in soupXml.findChildren('track'):
        videoUrl = media.findChild('location').getText()
        videoItemsList.append(videoUrl)
    return videoItemsList
    
