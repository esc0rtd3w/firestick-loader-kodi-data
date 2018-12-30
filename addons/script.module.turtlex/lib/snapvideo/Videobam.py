'''
Created on Dec 25, 2011

@author: ajju
'''
from common import HttpUtils
from common.DataObjects import VideoHostingInfo, VideoInfo, VIDEO_QUAL_SD, \
    VIDEO_QUAL_HD_720
import re

def getVideoHostingInfo():
    video_hosting_info = VideoHostingInfo()
    video_hosting_info.set_video_hosting_image('')
    video_hosting_info.set_video_hosting_name('Videobam')
    return video_hosting_info
    
def retrieveVideoInfo(video_id):
    video_info = VideoInfo()
    video_info.set_video_hosting_info(getVideoHostingInfo())
    video_info.set_video_id(video_id)
    try:
        video_info_link = 'http://videobam.com/' + str(video_id)
        html = HttpUtils.HttpClient().getHtmlContent(url=video_info_link)
        streams = re.compile('(low|high): \'(.+?)\'').findall(html)
        for streamType, streamUrl in streams:
            if streamType == 'low':
                video_info.add_video_link(VIDEO_QUAL_SD, streamUrl)
            elif streamType == 'high':
                video_info.add_video_link(VIDEO_QUAL_HD_720, streamUrl)
        video_info.set_video_stopped(False)
        
    except: 
        video_info.set_video_stopped(True)
    return video_info
