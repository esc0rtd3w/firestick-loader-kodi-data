'''
Created on Dec 24, 2011

@author: ajju
'''
from common import HttpUtils, Logger
from common.DataObjects import VideoHostingInfo, VideoInfo, VIDEO_QUAL_SD, \
    VIDEO_QUAL_HD_720, VIDEO_QUAL_HD_1080, VIDEO_QUAL_LOW
import re

def getVideoHostingInfo():
    video_hosting_info = VideoHostingInfo()
    video_hosting_info.set_video_hosting_image('http://tune.pk/styles/tunev3/images/logo.png')
    video_hosting_info.set_video_hosting_name('Tune.pk')
    return video_hosting_info
    
def retrieveVideoInfo(video_id):
    
    video_info = VideoInfo()
    video_info.set_video_hosting_info(getVideoHostingInfo())
    video_info.set_video_id(video_id)
    try:
        video_info_link = 'http://embed.tune.pk/play/' + str(video_id) + '?autoplay=no'
        html = HttpUtils.HttpClient().getHtmlContent(url=video_info_link)
        image = re.compile("preview_img = '(.+?)';").findall(html)
        if image is not None and len(image) == 1:
            video_info.set_video_image(str(image[0]))
        html = html.replace('\n\r', '').replace('\r', '').replace('\n', '')
        sources = re.compile("{(.+?)}").findall(re.compile("sources:(.+?)]").findall(html)[0])
        for source in sources:
            video_link = str(re.compile('file[: ]*"(.+?)"').findall(source)[0])
            Logger.logDebug(video_link)
            label_text = re.compile('label[: ]*"(.+?)"').findall(source)
            if label_text is not None and len(label_text) == 1:
                label = str(label_text[0])
                Logger.logDebug(label)
                if label == '240p':
                    video_info.add_video_link(VIDEO_QUAL_LOW, video_link)
                elif label == '360p' and video_info.get_video_link(VIDEO_QUAL_SD) is None:
                    video_info.add_video_link(VIDEO_QUAL_SD, video_link)
                elif label == '480p' or label == 'SD':
                    video_info.add_video_link(VIDEO_QUAL_SD, video_link)
                elif label == '720p' or label == 'HD':
                    video_info.add_video_link(VIDEO_QUAL_HD_720, video_link)
                elif label == '1080p':
                    video_info.add_video_link(VIDEO_QUAL_HD_1080, video_link)
                else:
                    video_info.add_video_link(VIDEO_QUAL_SD, video_link)
                    
            else:
                video_info.add_video_link(VIDEO_QUAL_SD, video_link)
        video_info.set_video_stopped(False)
        
    except Exception, e:
        Logger.logError(e)
        video_info.set_video_stopped(True)
    return video_info
