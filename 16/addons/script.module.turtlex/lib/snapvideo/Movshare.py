'''
Created on Dec 22, 2011

@author: ajju
'''
from common.DataObjects import VideoHostingInfo, VideoInfo, VIDEO_QUAL_SD
from common import HttpUtils
import re

def getVideoHostingInfo():
    video_hosting_info = VideoHostingInfo()
    video_hosting_info.set_video_hosting_image('http://www.movshare.net/images/logo.png')
    video_hosting_info.set_video_hosting_name('Movshare')
    return video_hosting_info
    
def retrieveVideoInfo(video_id):
    
    video_info = VideoInfo()
    video_info.set_video_hosting_info(getVideoHostingInfo())
    video_info.set_video_id(video_id)
    try:
        HttpUtils.HttpClient().enableCookies()
        video_info_link = 'http://www.movshare.net/video/' + str(video_id)
        html = HttpUtils.HttpClient().getHtmlContent(url=video_info_link)
        if re.search(r'Video hosting is expensive. We need you to prove you\'re human.', html):
            html = HttpUtils.HttpClient().getHtmlContent(url=video_info_link)

        video_info_link = re.compile('<embed type="video/divx" src="(.+?)"').findall(html)
        video_link = ''
        if len(video_info_link) == 0:
            domainStr = re.compile('flashvars.domain="(.+?)"').findall(html)[0]
            fileStr = re.compile('flashvars.file="(.+?)"').findall(html)[0]
            filekeyStr = re.compile('flashvars.filekey="(.+?)"').findall(html)[0]
            
            video_info_link = domainStr + '/api/player.api.php?user=undefined&pass=undefined&codes=1&file=' + fileStr + '&key=' + filekeyStr
            html = HttpUtils.HttpClient().getHtmlContent(url=video_info_link)
            video_link = re.compile(r'url=(.+?)&').findall(html)[0]
        else:
            video_link = video_info_link[0]
            
        HttpUtils.HttpClient().disableCookies()
        
        video_info.set_video_stopped(False)
        video_info.add_video_link(VIDEO_QUAL_SD, video_link)
    except: 
        video_info.set_video_stopped(True)
    return video_info
