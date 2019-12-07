'''
Created on Jan 13, 2014

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



'''
Created on Dec 25, 2011

@author: ajju
'''
from common.DataObjects import VideoHostingInfo, VideoInfo, VIDEO_QUAL_SD

VIDEO_HOSTING_NAME = 'VideoPress'

def getVideoHostingInfo():
    video_hosting_info = VideoHostingInfo()
    video_hosting_info.set_video_hosting_image('http://s2.wp.com/wp-content/themes/a8c/videopress4/img/logo-footer.png?m=1340912836g')
    video_hosting_info.set_video_hosting_name('VideoPress')
    return video_hosting_info
    
def retrieveVideoInfo(video_id):
    
    video_info = VideoInfo()
    video_info.set_video_hosting_info(getVideoHostingInfo())
    video_info.set_video_id(video_id)
    try:
        video_link = 'http://videos.videopress.com/' + str(video_id) + '.mp4'
        print video_link
        video_info.add_video_link(VIDEO_QUAL_SD, video_link)
        video_info.set_video_stopped(False)
        
    except: 
        video_info.set_video_stopped(True)
    return video_info
