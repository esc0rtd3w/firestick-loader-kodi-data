'''
Created on Feb 1, 2014

@author: ajdeveloped@gmail.com

This file is part of XOZE. 

XOZE is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

XOZE is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with XOZE.  If not, see <http://www.gnu.org/licenses/>.
'''
from common.DataObjects import VideoHostingInfo, VideoInfo, VIDEO_QUAL_SD
from common import HttpUtils
import re

def getVideoHostingInfo():
    video_hosting_info = VideoHostingInfo()
    video_hosting_info.set_video_hosting_image('http://www.nowvideo.ch/images/logo.png')
    video_hosting_info.set_video_hosting_name('Nowvideo')
    return video_hosting_info
    
def retrieveVideoInfo(video_id):
    
    video_info = VideoInfo()
    video_info.set_video_hosting_info(getVideoHostingInfo())
    video_info.set_video_id(video_id)
    try:
        HttpUtils.HttpClient().enableCookies()
        video_info_link = 'http://www.nowvideo.ch/video/' + str(video_id)
        html = HttpUtils.HttpClient().getHtmlContent(url=video_info_link)
        if re.search(r'Video hosting is expensive. We need you to prove you\'re human.', html):
            html = HttpUtils.HttpClient().getHtmlContent(url=video_info_link)

        domainStr = re.compile('flashvars.domain="(.+?)"').findall(html)[0]
        fileStr = re.compile('flashvars.file="(.+?)"').findall(html)[0]
        filekey = re.compile('flashvars.filekey="(.+?)"').findall(html)
        filekeyStr = None
        if len(filekey) == 0:
            filekeyStr = re.compile('flashvars.filekey=(.+?);').findall(html)[0]
            filekeyStr = re.compile('var ' + filekeyStr + '="(.+?)"').findall(html)[0]
        else:
            filekeyStr = filekey[0]
        video_info_link = domainStr + '/api/player.api.php?user=undefined&pass=undefined&codes=1&file=' + fileStr + '&key=' + filekeyStr
        html = HttpUtils.HttpClient().getHtmlContent(url=video_info_link)
        video_link = re.compile(r'url=(.+?)&').findall(html)[0]
        HttpUtils.HttpClient().disableCookies()
        
        video_info.set_video_stopped(False)
        video_info.add_video_link(VIDEO_QUAL_SD, video_link)
    except: 
        video_info.set_video_stopped(True)
    return video_info
