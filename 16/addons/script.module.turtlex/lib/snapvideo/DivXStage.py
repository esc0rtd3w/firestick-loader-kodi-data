'''
Created on Dec 23, 2011

@author: ajju
'''
from common.DataObjects import VideoHostingInfo, VideoInfo, VIDEO_QUAL_SD
from common import HttpUtils
import re
import logging

def getVideoHostingInfo():
    video_hosting_info = VideoHostingInfo()
    video_hosting_info.set_video_hosting_image('http://www.divxstage.eu/images/logo.jpg')
    video_hosting_info.set_video_hosting_name('DivXStage')
    return video_hosting_info
    
def retrieveVideoInfo(video_id):
    
    video_info = VideoInfo()
    video_info.set_video_hosting_info(getVideoHostingInfo())
    video_info.set_video_id(video_id)
    try:
        HttpUtils.HttpClient().enableCookies()
        video_info_link = 'http://www.divxstage.eu/video/' + str(video_id)
        html = HttpUtils.HttpClient().getHtmlContent(url=video_info_link)
        if re.search(r'Video hosting is expensive. We need you to prove you\'re human.', html):
            html = HttpUtils.HttpClient().getHtmlContent(url=video_info_link)
        
        HttpUtils.HttpClient().disableCookies()
        fileKey = re.compile('flashvars.filekey="(.+?)";').findall(html)[0]
        video_info_link = 'http://www.divxstage.eu/api/player.api.php?file=' + video_id + '&key=' + fileKey
        html = HttpUtils.HttpClient().getHtmlContent(url=video_info_link)
        video_link = re.compile('url=(.+?)&').findall(html)[0]
        video_info.set_video_stopped(False)
        video_info.add_video_link(VIDEO_QUAL_SD, video_link)
    except Exception, e:
        logging.exception(e)
        video_info.set_video_stopped(True)
    return video_info
