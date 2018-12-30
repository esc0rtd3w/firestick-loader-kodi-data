from resources.lib.modules import client,webutils,convert,control
from resources.lib.modules.log_utils import log
import re,sys

class info():
    def __init__(self):
        self.mode = 'batmanstream'
        self.name = 'batmanstream.com'
        self.icon = 'batmanstream.png'
        self.categorized = True
        self.paginated = False
        self.multilink = True

class main():
    def __init__(self):
        self.base = 'http://batmanstream.com/'

    def categories(self):
        cats = [('http://www.batmanstream.com/free-live-streaming-videos.html','Live','live.png') ,('http://www.batmanstream.com/football-live-streaming-video-2016.html','Football','icons/soccer.png'),
                ('http://www.batmanstream.com/nfl-live-streaming-video-2016-1.html','American Football','icons/football.png'),
                ('http://www.batmanstream.com/basketball-live-streaming-video-2016-1.html','Basketball','icons/basketball.png'),
                ('http://www.batmanstream.com/rugby-live-streaming-video-2016-1.html', 'Rugby', 'icons/rugby.png'), 
                ('http://www.batmanstream.com/hockey-live-streaming-video-2015.html', 'Ice Hockey', 'icons/hockey.png'),
                ('http://www.batmanstream.com/tennis-live-streaming-video-2016.html', 'Tennis', 'icons/tennis.png'), 
                ('http://www.batmanstream.com/motor-sports-live-streaming-video.html', 'Motosport', 'icons/f1.png'),
                ('http://www.batmanstream.com/baseball-live-streaming-video.html', 'Baseball', 'icons/baseball.png'),
                ('http://www.batmanstream.com/handball-live-streaming-video.html', 'Handball', 'icons/handall.png'),
                ('http://www.batmanstream.com/volleyball-live-streaming-video-2016.html', 'Volleyball', 'icons/volleyall.png'),
                ('http://www.batmanstream.com/other-live-streaming-video-1.html', 'Other', 'icons/athletics.png') ]
        return cats

    def events(self,url):
        html = client.request(url)
        html = convert.unescape(html.decode('utf-8'))
        #events = webutils.bs(html).findAll('div',{'class':'lshpanel'})
        events = client.parseDOM(html, 'div',attrs={'class':'lshpanel'})
        events = self.__prepare_events(events)
        return events

    def links(self,url):
        html = client.request(url)
        trs = client.parseDOM(html,'table', attrs={'style':'border-width: 0px; width: 100%;'})
        links = self.__prepare_links(trs)
        return links



    @staticmethod
    def convert_time(time):
        
        li = time.split(':')
        hour,minute=li[0],li[1]
    
        import datetime
        from resources.lib.modules import pytzimp
        d = pytzimp.timezone(str(pytzimp.timezone('Europe/London'))).localize(datetime.datetime(2000 , 1, 1, hour=int(hour), minute=int(minute)))
        timezona= control.setting('timezone_new')
        my_location=pytzimp.timezone(pytzimp.all_timezones[int(timezona)])
        convertido=d.astimezone(my_location)
        fmt = "%H:%M"
        time=convertido.strftime(fmt)
        return time

    def __prepare_links(self,links):
        new=[]
        for tx in links:
            t = client.parseDOM(tx, 'td')[0]
            title = client.parseDOM(tx,'img',ret='title')[0]
            urls = client.parseDOM(t,'a',attrs={'target':'_blank'} ,ret='href')
            i=1
            for u in urls:
                if 'bet' not in u and 'mamahd' not in u and title!='MamaHD' and title!='HDcast' and title.lower()!='website':
                    new.append((u,title+' Link #%s'%i))
                    i+=1
        return new


    def __prepare_events(self,events):
        new = []
        for ev in events:
            time = client.parseDOM(ev,'span',attrs={'class':'lshstart_time'})[0]
            sport = client.parseDOM(ev,'span',attrs={'class':'section'})[0]
            event = client.parseDOM(ev,'span',attrs={'class':'lshevent'})[0]
            title = u'[COLOR orange](%s)[/COLOR] (%s) %s'%(time,sport,event)
            uri = self.base + client.parseDOM(ev,'a', attrs={'class':'open_event_tab'}, ret='href')[0]
            new.append((uri,title.encode('utf-8')))
        return new

    def resolve(self,url):
        html = client.request(url)
        import liveresolver
        return liveresolver.resolve(url,html=html,cache_timeout=0)