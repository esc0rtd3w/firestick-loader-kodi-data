'''
Created on Nov 21, 2012

@author: ajju
'''
from BeautifulSoup import BeautifulStoneSoup
from common.DataObjects import VideoHostingInfo, VideoInfo, VIDEO_QUAL_HD_720
from common import HttpUtils
import re

VIDEO_HOSTING_NAME = 'PLAYWIRE'
def getVideoHostingInfo():
    video_hosting_info = VideoHostingInfo()
    video_hosting_info.set_video_hosting_image('http://www.playwire.com/images/logo.png')
    video_hosting_info.set_video_hosting_name(VIDEO_HOSTING_NAME)
    return video_hosting_info

def retrieveVideoInfo(video_id):
    video_info = VideoInfo()
    video_info.set_video_hosting_info(getVideoHostingInfo())
    video_info.set_video_id(video_id)
    try:
        video_link = 'http://cdn.playwire.com/' + str(video_id) + '.xml'
        soup = BeautifulStoneSoup(HttpUtils.HttpClient().getHtmlContent(url=video_link), convertEntities=BeautifulStoneSoup.XML_ENTITIES)
        cfg = soup.find("config")
        img_link = cfg.findNext("poster").string
        video_link = cfg.findNext("src").string
        
        video_info.set_video_stopped(False)
        video_info.set_video_image(img_link)
        video_info.set_video_name("PLAYWIRE Video")
        if re.search(r'\Artmp',video_link):
            video_info.add_video_link(VIDEO_QUAL_HD_720, video_link, addUserAgent=False)
        else:
            video_info.add_video_link(VIDEO_QUAL_HD_720, video_link, addUserAgent=True)
    except:
        video_info.set_video_stopped(True)
    return video_info

