'''
Created on Nov 21, 2012

@author: ajju
'''
from common.DataObjects import VideoHostingInfo
from snapvideo import UrlResolverDelegator

VIDEO_HOSTING_NAME = 'PutLocker'
def getVideoHostingInfo():
    video_hosting_info = VideoHostingInfo()
    video_hosting_info.set_video_hosting_image('http://static.putlocker.com/images/v1_r2_c5.png')
    video_hosting_info.set_video_hosting_name(VIDEO_HOSTING_NAME)
    return video_hosting_info

def retrieveVideoInfo(video_id):
    videoUrl = "http://www.putlocker.com/file/" + video_id
    return UrlResolverDelegator.retrieveVideoInfo(videoUrl)