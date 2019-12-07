from __future__ import unicode_literals
from resources.lib.modules import client,control
import re,sys,xbmcgui,os


class info():
    def __init__(self):
    	self.mode = 'lmshows'
        self.name = 'LMShows.com'
        self.icon = 'lmshows.jpg'
        self.paginated = False
        self.categorized = False
        self.multilink = False
class main():
    def __init__(self):
        self.base = 'http://lmshows.se/'
        
    def channels(self):
        html = client.request(self.base)
        channels = re.findall('href=[\"\']([^\"\']+)[\"\']><img src=[\"\']([^\"\']+)[\"\'] alt=[\"\']([^\"\']+)[\"\'].+?class=[\"\']ch-cover',html)
        events = []
        for c in channels:
           
            url = self.base + c[0]
            img = self.base + c[1]
            title = c[2]
            if c[0] == 'tr.php':
                continue
            events.append((url,title,img))
        events.append(('http://lmshows.se/sb.php','SpongeBob SquarePants','http://vignette2.wikia.nocookie.net/spongebobtv/images/0/0b/SpongeBob-Logo.jpg/revision/latest?cb=20100716014643'))
        events=list(set(events))
        events.append(('http://www.ustream.tv/embed/19964595','Toonami Aftermath','http://66.media.tumblr.com/tumblr_lnfu9bYqaH1qa0xnuo1_500.png'))
        events.sort(key=lambda x: x[1])
        return events
        
    def resolve(self,url):
        import liveresolver
        return liveresolver.resolve(url,cache_timeout=0)