'''
Created on Dec 24, 2011

@author: ajju
'''
from common import HttpUtils, Logger
from common.DataObjects import VideoHostingInfo, VideoInfo, VIDEO_QUAL_SD, \
    VIDEO_QUAL_HD_720
import re

def getVideoHostingInfo():
    video_hosting_info = VideoHostingInfo()
    video_hosting_info.set_video_hosting_image('http://cdn1.iconfinder.com/data/icons/Social_Networking_Icons_PNG/PNG/Vimeo.png')
    video_hosting_info.set_video_hosting_name('Vimeo')
    return video_hosting_info
    
def retrieveVideoInfo(video_id):
    
    video_info = VideoInfo()
    video_info.set_video_hosting_info(getVideoHostingInfo())
    video_info.set_video_id(video_id)
    try:

        html = HttpUtils.HttpClient().getHtmlContent(url='http://vimeo.com/' + str(video_id))
        referrerObj = re.compile('"timestamp":(.+?),"signature":"(.+?)"').findall(html)[0]
        req_sig_exp = referrerObj[0]
        req_sig = referrerObj[1]
        
        img_link = re.compile('itemprop="thumbnailUrl" content="(.+?)"').findall(html)[0]
        video_title = re.compile('"title":"(.+?)"').findall(html)[0]
        
        qual = 'sd'
        video_link = "http://player.vimeo.com/play_redirect?clip_id=%s&sig=%s&time=%s&quality=%s&codecs=H264,VP8,VP6&type=moogaloop_local&embed_location=" % (video_id, req_sig, req_sig_exp, qual)
        video_info.add_video_link(VIDEO_QUAL_SD, video_link)
        
        if(re.search('"hd":1', html)):
            qual = 'hd'
            video_link = "http://player.vimeo.com/play_redirect?clip_id=%s&sig=%s&time=%s&quality=%s&codecs=H264,VP8,VP6&type=moogaloop_local&embed_location=" % (video_id, req_sig, req_sig_exp, qual)
            video_info.add_video_link(VIDEO_QUAL_HD_720, video_link)
            
        video_info.set_video_stopped(False)
        video_info.set_video_image(img_link)
        video_info.set_video_name(video_title)
        
    except Exception, e:
        Logger.logError(e)
        video_info.set_video_stopped(True)
    return video_info
