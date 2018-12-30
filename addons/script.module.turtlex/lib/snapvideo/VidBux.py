'''
Created on Dec 23, 2011

@author: ajju
'''
from common.DataObjects import VideoHostingInfo
from snapvideo import UrlResolverDelegator


def getVideoHostingInfo():
    video_hosting_info = VideoHostingInfo()
    video_hosting_info.set_video_hosting_image('http://www.vidbux.com/images/vid_bux_logo_small.png')
    video_hosting_info.set_video_hosting_name('VidBux')
    return video_hosting_info
    
def retrieveVideoInfo(video_id):
    videoUrl = 'http://www.vidbux.com/' + str(video_id)
    return UrlResolverDelegator.retrieveVideoInfo(videoUrl)

