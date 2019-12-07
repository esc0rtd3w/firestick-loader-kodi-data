'''
Created on Nov 21, 2012

@author: ajju
'''
from common.DataObjects import VideoHostingInfo
from snapvideo import UrlResolverDelegator

def getVideoHostingInfo():
    video_hosting_info = VideoHostingInfo()
    video_hosting_info.set_video_hosting_image('http://external.ak.fbcdn.net/safe_image.php?d=AQDX8O6c1SWeFsIT&url=http%3A%2F%2Fprofile.ak.fbcdn.net%2Fhprofile-ak-ash4%2F373037_143140885811844_207401638_n.jpg')
    video_hosting_info.set_video_hosting_name('sockshare')
    return video_hosting_info

def retrieveVideoInfo(video_id):
    videoUrl = "http://www.sockshare.com/file/" + video_id
    return UrlResolverDelegator.retrieveVideoInfo(videoUrl)

