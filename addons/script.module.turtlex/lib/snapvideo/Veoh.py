'''
Created on Dec 24, 2011

@author: ajju
'''
from BeautifulSoup import BeautifulStoneSoup
from common import HttpUtils
from common.DataObjects import VideoHostingInfo, VideoInfo, VIDEO_QUAL_SD

API_KEY = 'E97FCECD-875D-D5EB-035C-8EF241F184E2'

def getVideoHostingInfo():
    video_hosting_info = VideoHostingInfo()
    video_hosting_info.set_video_hosting_image('http://blog.toggle.com/wp-content/uploads/2011/05/veoh_logo.png')
    video_hosting_info.set_video_hosting_name('Veoh')
    return video_hosting_info
    
def retrieveVideoInfo(video_id):
    
    video_info = VideoInfo()
    video_info.set_video_hosting_info(getVideoHostingInfo())
    video_info.set_video_id(video_id)
    try:
        video_info_link = 'http://www.veoh.com/rest/v2/execute.xml?method=veoh.video.findByPermalink&permalink=' + str(video_id) + '&apiKey=' + API_KEY
        soup = BeautifulStoneSoup(HttpUtils.HttpClient().getHtmlContent(url=video_info_link), convertEntities=BeautifulStoneSoup.XML_ENTITIES)
        
        videoObj = soup.findChild(name='video')
        video_link = HttpUtils.getRedirectedUrl(str(videoObj['ipodurl']))
        img_link = str(videoObj['highresimage'])
        video_title = str(videoObj['title'])
        
        video_info.set_video_stopped(False)
        video_info.set_video_image(img_link)
        video_info.set_video_name(video_title)
        video_info.add_video_link(VIDEO_QUAL_SD, video_link)
        
    except: 
        video_info.set_video_stopped(True)
    return video_info
