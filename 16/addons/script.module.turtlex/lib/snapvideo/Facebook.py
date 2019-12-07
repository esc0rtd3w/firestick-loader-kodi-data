'''
Created on Dec 23, 2011

@author: ajju
'''
from common.DataObjects import VideoHostingInfo, VideoInfo, VIDEO_QUAL_SD, \
    VIDEO_QUAL_HD_720
from common import HttpUtils
import re
import urllib

def getVideoHostingInfo():
    video_hosting_info = VideoHostingInfo()
    video_hosting_info.set_video_hosting_image('http://www.koreaittimes.com/images/imagecache/medium/facebook-video-player-logo.png')
    video_hosting_info.set_video_hosting_name('Facebook')
    return video_hosting_info
    
def retrieveVideoInfo(video_id):
    
    video_info = VideoInfo()
    video_info.set_video_hosting_info(getVideoHostingInfo())
    video_info.set_video_id(video_id)
    try:
        
        video_info_link = 'http://www.facebook.com/video/video.php?v=' + str(video_id)
        html = urllib.unquote_plus(HttpUtils.HttpClient().getHtmlContent(url=video_info_link).replace('\u0025', '%'))

        video_title = re.compile('addVariable\("video_title"\, "(.+?)"').findall(html)[0]
        img_link = re.compile('addVariable\("thumb_url"\, "(.+?)"').findall(html)[0]
        high_video_link = re.compile('addVariable\("highqual_src"\, "(.+?)"').findall(html)
        low_video_link = re.compile('addVariable\("lowqual_src"\, "(.+?)"').findall(html)
        video_link = re.compile('addVariable\("video_src"\, "(.+?)"').findall(html)
        if len(high_video_link) > 0:
            video_info.add_video_link(VIDEO_QUAL_HD_720, high_video_link[0])
        if len(low_video_link) > 0:
            video_info.add_video_link(VIDEO_QUAL_SD, low_video_link[0])
        if len(video_link) > 0:
            video_info.add_video_link(VIDEO_QUAL_SD, video_link[0])

        video_info.set_video_stopped(False)
        video_info.set_video_name(video_title)
        video_info.set_video_image(img_link)
    except:
        raise
        video_info.set_video_stopped(True)
    return video_info

