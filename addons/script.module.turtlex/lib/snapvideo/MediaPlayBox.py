'''
Created on Nov 21, 2012

@author: ajju
'''
from common import HttpUtils
from common.DataObjects import VideoHostingInfo, VideoInfo, VIDEO_QUAL_HD_720, \
    VIDEO_QUAL_SD
import re

VIDEO_HOSTING_NAME = 'MediaPlayBox'
def getVideoHostingInfo():
    video_hosting_info = VideoHostingInfo()
    video_hosting_info.set_video_hosting_image('http://www.mediaplaybox.com/administration/fckeditor/uploaded_files/mslogo.png')
    video_hosting_info.set_video_hosting_name(VIDEO_HOSTING_NAME)
    return video_hosting_info

def returnVideoInfo(video_id):
    video_info = VideoInfo()
    video_info.set_video_hosting_info(getVideoHostingInfo())
    video_info.set_video_id(video_id)
    try:
        video_link_info = 'http://www.mediaplaybox'+video_id
        video_link_info = video_link_info.replace('/:81/','/').replace('mediaplaybox:81','mediaplaybox.com') + '.mp4'
        video_link = video_link_info.replace('_ipod.mp4', '.flv')
        hd_video_link = video_link.replace('_ipod.mp4', '_hd.mp4')
        video_info.set_video_stopped(False)
        video_info.set_video_name("Media PlayBox Video")
        try:
            response = HttpUtils.HttpClient().getResponse(url=hd_video_link)
            if response.status < 400:
                video_info.add_video_link(VIDEO_QUAL_HD_720, hd_video_link, addUserAgent=False)
        except Exception,e:
            print 'No HD link'
        video_info.add_video_link(VIDEO_QUAL_SD, video_link, addUserAgent=False)
    except Exception,e:
        video_info.set_video_stopped(True)
        raise e
    return video_info

def retrieveVideoInfo(video_id):
    video_info = VideoInfo()
    video_info.set_video_hosting_info(getVideoHostingInfo())
    video_info.set_video_id(video_id)
    try:
        video_link = 'http://www.mediaplaybox.com/mobile?vinf=' + str(video_id)
        html = HttpUtils.HttpClient().getHtmlContent(url=video_link, headers=HttpUtils.IPAD_HEADERS)
        video_file_info = re.compile('href="http://www.mediaplaybox.com/media/files_flv/(.+?)"').findall(html)
        if(len(video_file_info) == 0):
            video_file_info = re.compile('href="http://www.mediaplaybox.com:81/media/files_flv/(.+?)"').findall(html)
        video_file = video_file_info[0]
        img_file_info = re.compile('src="http://www.mediaplaybox.com/media/files_thumbnail/(.+?)"').findall(html)
        if(len(img_file_info) == 0):
            img_file_info = re.compile('src="http://www.mediaplaybox.com/media/files_thumbnail/(.+?)"').findall(html)[0]
        img_file = img_file_info[0]
        video_link = 'http://www.mediaplaybox.com/media/files_flv/' + video_file.replace('_ipod.mp4', '.flv')
        hd_video_link = 'http://www.mediaplaybox.com/media/files_flv/' + video_file.replace('_ipod.mp4', '_hd.mp4')
        img_link = 'http://www.mediaplaybox.com/media/files_thumbnail/' + img_file
        video_info.set_video_stopped(False)
        video_info.set_video_image(img_link)
        video_info.set_video_name("Media PlayBox Video")
        try:
            response = HttpUtils.HttpClient().getResponse(url=hd_video_link)
            if response.status < 400:
                video_info.add_video_link(VIDEO_QUAL_HD_720, hd_video_link, addUserAgent=False)
        except Exception,e:
            print 'No HD link'
        video_info.add_video_link(VIDEO_QUAL_SD, video_link, addUserAgent=False)
    except Exception,e:
        video_info.set_video_stopped(True)
        raise e
    return video_info

