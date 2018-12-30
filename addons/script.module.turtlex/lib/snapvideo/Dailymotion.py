'''
Created on Oct 29, 2011

@author: ajju
'''
from common import HttpUtils, Logger
from common.DataObjects import VideoHostingInfo, VideoInfo, VIDEO_QUAL_SD, \
    VIDEO_QUAL_HD_720, VIDEO_QUAL_HD_1080, VIDEO_QUAL_LOW
import re
import urllib
try:
    import json
except ImportError:
    import simplejson as json

VIDEO_HOSTING_NAME = 'Dailymotion'
def getVideoHostingInfo():
    video_hosting_info = VideoHostingInfo()
    video_hosting_info.set_video_hosting_image('http://press.dailymotion.com/fr/wp-content/uploads/logo-Dailymotion.png')
    video_hosting_info.set_video_hosting_name(VIDEO_HOSTING_NAME)
    return video_hosting_info
    
def retrieveVideoInfo(video_id):
    video_info = VideoInfo()
    video_info.set_video_hosting_info(getVideoHostingInfo())
    video_info.set_video_id(video_id)
    try:
        video_link = 'http://www.dailymotion.com/embed/video/' + str(video_id)
        html = HttpUtils.HttpClient().getHtmlContent(url=video_link)
        HttpUtils.HttpClient().disableCookies()
        
        player = re.compile('document\.getElementById\(\'player\'\), (.+?)\);').findall(html)
        player_obj = json.loads(player[0])
        video_qual = player_obj['metadata']['qualities']
        print video_qual
        dm_LD = None
        if video_qual.has_key('380'):
            dm_LD = video_qual['380'][0]['url']
        dm_SD = None
        if video_qual.has_key('480'):
            dm_SD = video_qual['480'][0]['url']
        dm_720 = None
        if video_qual.has_key('720'):
            dm_720 = video_qual['720'][0]['url']
        dm_1080 = None
        if video_qual.has_key('1080'):
            dm_1080 = video_qual['1080'][0]['url']
        
        if dm_LD is not None:
            video_info.add_video_link(VIDEO_QUAL_LOW, dm_LD, addReferer=True, refererUrl=video_link)
        if dm_SD is not None:
            video_info.add_video_link(VIDEO_QUAL_SD, dm_SD, addReferer=True, refererUrl=video_link)
        if dm_720 is not None:
            video_info.add_video_link(VIDEO_QUAL_HD_720, dm_720, addReferer=True, refererUrl=video_link)
        if dm_1080 is not None:
            video_info.add_video_link(VIDEO_QUAL_HD_1080, dm_1080, addReferer=True, refererUrl=video_link)
        video_info.set_video_stopped(False)
    except Exception, e:
        Logger.logError(e)
        video_info.set_video_stopped(True)
    return video_info


def retrievePlaylistVideoItems(playlistId):
    html = HttpUtils.HttpClient().getHtmlContent(url='https://api.dailymotion.com/playlist/' + playlistId + '/videos')
    playlistJsonObj = json.loads(html)
    videoItemsList = []
    for video in playlistJsonObj['list']:
        videoItemsList.append('http://www.dailymotion.com/video/' + str(video['id']))
    return videoItemsList

