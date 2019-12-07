'''
Created on Jul 10, 2013

@author: ajju
'''
from common.DataObjects import VideoHostingInfo, VideoInfo, VIDEO_QUAL_SD
from common import HttpUtils
import re
import urllib

def getVideoHostingInfo():
    video_hosting_info = VideoHostingInfo()
    video_hosting_info.set_video_hosting_image('http://my-entertainment.biz/forum/images/misc/vbulletin4_logo.png')
    video_hosting_info.set_video_hosting_name('My-Entertainment Biz')
    return video_hosting_info

def retrieveVideoInfo(video_id):
    video_info = VideoInfo()
    video_info.set_video_hosting_info(getVideoHostingInfo())
    video_info.set_video_id(video_id)
    try:
        video_link = 'http://my-entertainment.biz/' + str(video_id)
        print video_link
        HttpUtils.HttpClient().enableCookies()
        HttpUtils.HttpClient().getHtmlContent(url='http://my-entertainment.biz/forum/content.php')
        html = HttpUtils.HttpClient().getHtmlContent(url=video_link)
        print html
        match = re.compile("file=(.+?)&&").findall(html)
        video_link = urllib.unquote(match[0])
        video_info.set_video_stopped(False)
        video_info.add_video_link(VIDEO_QUAL_SD, video_link)
    except:
        video_info.set_video_stopped(True)
    return video_info