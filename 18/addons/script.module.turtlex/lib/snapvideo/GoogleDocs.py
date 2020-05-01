'''
@author: ajju
'''
from common.DataObjects import VideoHostingInfo, VideoInfo, VIDEO_QUAL_LOW, VIDEO_QUAL_SD, \
    VIDEO_QUAL_HD_720, VIDEO_QUAL_HD_1080
from common import HttpUtils
import re
import logging

VIDEO_HOSTING_NAME = 'Google Docs'
def getVideoHostingInfo():
    video_hosting_info = VideoHostingInfo()
    video_hosting_info.set_video_hosting_image('http://oakhill.newton.k12.ma.us/sites/oakhill.newton.k12.ma.us/files/users/3/google_docs_image.png')
    video_hosting_info.set_video_hosting_name(VIDEO_HOSTING_NAME)
    return video_hosting_info
    
def retrieveVideoInfo(video_id):
    
    video_info = VideoInfo()
    video_info.set_video_hosting_info(getVideoHostingInfo())
    video_info.set_video_id(video_id)
    try:
        html = HttpUtils.HttpClient().getHtmlContent(url='https://docs.google.com/file/' + str(video_id) + '?pli=1')
        html = html.decode('utf8')
        title = re.compile("'title': '(.+?)'").findall(html)[0]
        video_info.set_video_name(title)
        stream_map = re.compile('fmt_stream_map":"(.+?)"').findall(html)[0].replace("\/", "/")
        formatArray = stream_map.split(',')
        for formatContent in formatArray:
            formatContentInfo = formatContent.split('|')
            qual = formatContentInfo[0]
            url = (formatContentInfo[1]).decode('unicode-escape')
            if(qual == '13'):  # 176x144
                video_info.add_video_link(VIDEO_QUAL_LOW, url)
            elif(qual == '17'):  # 176x144
                video_info.add_video_link(VIDEO_QUAL_LOW, url)
            elif(qual == '36'):  # 320x240
                video_info.add_video_link(VIDEO_QUAL_LOW, url)
            elif(qual == '5'):  # 400\\327226
                video_info.add_video_link(VIDEO_QUAL_LOW, url)
            elif(qual == '34'):  # 480x360 FLV
                video_info.add_video_link(VIDEO_QUAL_SD, url)
            elif(qual == '6'):  # 640\\327360 FLV
                video_info.add_video_link(VIDEO_QUAL_SD, url)
            elif(qual == '35'):  # 854\\327480 HD
                video_info.add_video_link(VIDEO_QUAL_SD, url)
            elif(qual == '18'):  # 480x360 MP4
                video_info.add_video_link(VIDEO_QUAL_SD, url)
            elif(qual == '22'):  # 1280x720 MP4
                video_info.add_video_link(VIDEO_QUAL_HD_720, url)
            elif(qual == '37'):  # 1920x1080 MP4
                video_info.add_video_link(VIDEO_QUAL_HD_1080, url)
            elif(qual == '38' and video_info.get_video_link(VIDEO_QUAL_HD_1080) is None):  # 4096\\3272304 EPIC MP4
                video_info.add_video_link(VIDEO_QUAL_HD_1080, url)
            elif(qual == '43' and video_info.get_video_link(VIDEO_QUAL_SD) is None):  # 360 WEBM
                video_info.add_video_link(VIDEO_QUAL_SD, url)
            elif(qual == '44'):  # 480 WEBM
                video_info.add_video_link(VIDEO_QUAL_SD, url)
            elif(qual == '45' and video_info.get_video_link(VIDEO_QUAL_HD_720) is None):  # 720 WEBM
                video_info.add_video_link(VIDEO_QUAL_HD_720, url)
            elif(qual == '46' and video_info.get_video_link(VIDEO_QUAL_HD_1080) is None):  # 1080 WEBM
                video_info.add_video_link(VIDEO_QUAL_HD_1080, url)
            elif(qual == '120' and video_info.get_video_link(VIDEO_QUAL_HD_720) is None):  # New video qual
                video_info.add_video_link(VIDEO_QUAL_HD_720, url)
                # 3D streams - MP4
                # 240p -> 83
                # 360p -> 82
                # 520p -> 85
                # 720p -> 84
                # 3D streams - WebM
                # 360p -> 100
                # 360p -> 101
                # 720p -> 102
            else:  # unknown quality
                video_info.add_video_link(VIDEO_QUAL_SD, url)

            video_info.set_video_stopped(False)
    except Exception, e:
        logging.exception(e)
        video_info.set_video_stopped(True)
    return video_info

