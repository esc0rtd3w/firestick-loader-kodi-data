'''
Created on Dec 25, 2011

@author: ajju
'''
from common import HttpUtils
from common.DataObjects import VideoHostingInfo, VideoInfo, VIDEO_QUAL_SD
import re

def getVideoHostingInfo():
    video_hosting_info = VideoHostingInfo()
    video_hosting_info.set_video_hosting_image('')
    video_hosting_info.set_video_hosting_name('Zalaa')
    return video_hosting_info
    
def retrieveVideoInfo(video_id):
    
    video_info = VideoInfo()
    video_info.set_video_hosting_info(getVideoHostingInfo())
    video_info.set_video_id(video_id)
    try:
        video_info_link = 'http://www.zalaa.com/' + str(video_id)
        html = HttpUtils.HttpClient().getHtmlContent(url=video_info_link)
        link = ''.join(html.splitlines()).replace('\'', '"')
        video_link = re.compile('s1.addVariable\("file","(.+?)"\);').findall(link)[0]
        video_info.add_video_link(VIDEO_QUAL_SD, video_link)
        video_info.set_video_stopped(False)
        
    except: 
        video_info.set_video_stopped(True)
    return video_info
