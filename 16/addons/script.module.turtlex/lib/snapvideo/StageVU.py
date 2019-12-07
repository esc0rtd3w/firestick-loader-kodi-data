'''
Created on Jan 3, 2012

@author: ajju
'''
from common import HttpUtils
from common.DataObjects import VideoHostingInfo, VideoInfo, VIDEO_QUAL_SD
import re

def getVideoHostingInfo():
    video_hosting_info = VideoHostingInfo()
    video_hosting_info.set_video_hosting_image('http://userlogos.org/files/logos/jumpordie/stagevu-iphone.png')
    video_hosting_info.set_video_hosting_name('StageVU')
    return video_hosting_info
    
def retrieveVideoInfo(video_id):
    
    video_info = VideoInfo()
    video_info.set_video_hosting_info(getVideoHostingInfo())
    video_info.set_video_id(video_id)
    try:
        video_info_link = 'http://stagevu.com/video/' + str(video_id)
        html = HttpUtils.HttpClient().getHtmlContent(url=video_info_link)
        html = ''.join(html.splitlines()).replace('\t', '').replace('\'', '"')
        match = re.compile('<param name="src" value="(.+?)"(.+?)<param name="movieTitle" value="(.+?)"(.+?)<param name="previewImage" value="(.+?)"').findall(html)
        video_info.add_video_link(VIDEO_QUAL_SD, match[0][0])
        video_info.set_video_name(match[0][2])
        video_info.set_video_image(match[0][4])
        video_info.set_video_stopped(False)
        
    except: 
        video_info.set_video_stopped(True)
    return video_info
