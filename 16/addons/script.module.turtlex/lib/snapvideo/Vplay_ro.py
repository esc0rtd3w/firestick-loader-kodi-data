'''
Created on Feb 10, 2012

@author: ajju
'''
from common.DataObjects import VideoHostingInfo, VideoInfo, VIDEO_QUAL_SD
from common import HttpUtils

def getVideoHostingInfo():
    video_hosting_info = VideoHostingInfo()
    video_hosting_info.set_video_hosting_image('http://s18.postimage.org/lgklzy6s5/vplay.png')
    video_hosting_info.set_video_hosting_name('VPlay')
    return video_hosting_info

def retrieveVideoInfo(video_id):
    video_info = VideoInfo()
    video_info.set_video_hosting_info(getVideoHostingInfo())
    video_info.set_video_id(video_id)
    try:
        HttpUtils.HttpClient().enableCookies()
        html = HttpUtils.HttpClient().getHtmlContent(url='http://www.vplay.ro/watch/' + str(video_id))
        html = HttpUtils.HttpClient().getHtmlContent(url='http://www.vplay.ro/play/dinosaur.do', params={'key':str(video_id)})
        params = HttpUtils.getUrlParams(html)
        video_link = HttpUtils.getRedirectedUrl(url=params['nqURL'])
        HttpUtils.HttpClient().disableCookies()
        video_info.set_video_stopped(False)
        video_info.add_video_link(VIDEO_QUAL_SD, video_link)
        video_info.set_video_image(params['th'])
    except:
        video_info.set_video_stopped(True)
    return video_info