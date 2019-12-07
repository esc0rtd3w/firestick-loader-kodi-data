'''
Created on Jun 29, 2012

@author: ajju
'''
from common import Logger, HttpUtils
from common.DataObjects import VideoHostingInfo, VideoInfo, VIDEO_QUAL_SD

try:
    import json
except ImportError:
    import simplejson as json
    
def getVideoHostingInfo():
    video_hosting_info = VideoHostingInfo()
    video_hosting_info.set_video_hosting_image('')
    video_hosting_info.set_video_hosting_name('SoundCloud')
    return video_hosting_info

def retrieveAudioInfo(audioUrl):
    url = 'https://api.soundcloud.com/' + audioUrl
    jObj = json.loads(HttpUtils.HttpClient().getHtmlContent(url=url))
    
    video_info = VideoInfo()
    video_info.set_video_hosting_info(getVideoHostingInfo())
    video_info.set_video_id(url)
    video_info.add_video_link(VIDEO_QUAL_SD, jObj['http_mp3_128_url'], addUserAgent=False, addReferer=False)
    video_info.set_video_image('')
    video_info.set_video_name('')
    
    Logger.logDebug(jObj['http_mp3_128_url'])
    video_info.set_video_stopped(False)
    return video_info
