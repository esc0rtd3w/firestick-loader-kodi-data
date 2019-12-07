'''
Created on Jan 3, 2012

@author: ajju
'''
from common import HttpUtils
from common.DataObjects import VideoHostingInfo, VideoInfo, VIDEO_QUAL_SD

def getVideoHostingInfo():
    video_hosting_info = VideoHostingInfo()
    video_hosting_info.set_video_hosting_image('http://profile.ak.fbcdn.net/hprofile-ak-snc4/50313_127613750585226_4787_n.jpg')
    video_hosting_info.set_video_hosting_name('veevr')
    return video_hosting_info
    
def retrieveVideoInfo(video_id):
    
    video_info = VideoInfo()
    video_info.set_video_hosting_info(getVideoHostingInfo())
    video_info.set_video_id(video_id)
    try:
        video_info_link = 'http://veevr.com/embed/' + str(video_id)
        soup = HttpUtils.HttpClient().getBeautifulSoup(url=video_info_link)
        thumbTag = soup.findChild('img', attrs={'id':'vid-thumb'})
        imageUrl = thumbTag['src']
        videoTitle = thumbTag['alt']
        
        vidTag = soup.findChild('img', attrs={'id':'smil-load'})
        videoUrl = vidTag['src']
        video_info.add_video_link(VIDEO_QUAL_SD, videoUrl)
        video_info.set_video_name(videoTitle)
        video_info.set_video_image(imageUrl)
        video_info.set_video_stopped(False)
        
    except: 
        video_info.set_video_stopped(True)
    return video_info

