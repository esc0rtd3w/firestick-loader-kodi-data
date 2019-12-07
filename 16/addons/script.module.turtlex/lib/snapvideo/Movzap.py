'''
Created on Feb 1, 2014

@author: ajju
'''
from common import HttpUtils, AddonUtils, Logger
from common.DataObjects import VideoHostingInfo, VideoInfo, VIDEO_QUAL_SD
import re

def getVideoHostingInfo():
    video_hosting_info = VideoHostingInfo()
    video_hosting_info.set_video_hosting_image('')
    video_hosting_info.set_video_hosting_name('Movzap')
    return video_hosting_info
    
def retrieveVideoInfo(video_id):
    
    video_info = VideoInfo()
    video_info.set_video_hosting_info(getVideoHostingInfo())
    video_info.set_video_id(video_id)
    try:
        video_info_link = 'http://movzap.com/' + str(video_id)
        html = HttpUtils.HttpClient().getHtmlContent(url=video_info_link)
        
        paramSet = re.compile("return p\}\(\'(.+?)\',(\d+),(\d+),\'(.+?)\'").findall(html)
        if len(paramSet) > 0:
            video_info_link = AddonUtils.parsePackedValue(paramSet[0][0], int(paramSet[0][1]), int(paramSet[0][2]), paramSet[0][3].split('|')).replace('\\', '').replace('"', '\'')
            
            img_data = re.compile(r"image:\'(.+?)\'").findall(video_info_link)
            if len(img_data) == 1:
                video_info.set_video_image(img_data[0])
            video_link = re.compile(r"file:\'(.+?)\'").findall(video_info_link)[0]
        else:
            video_link = re.compile("'file': '(.+?)'").findall(html)[0]
        video_info.set_video_stopped(False)
        video_info.add_video_link(VIDEO_QUAL_SD, video_link)
        
    except Exception, e:
        Logger.logError(e)
        video_info.set_video_stopped(True)
    return video_info
