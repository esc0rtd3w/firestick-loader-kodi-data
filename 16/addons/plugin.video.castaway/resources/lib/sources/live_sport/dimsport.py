from resources.lib.modules import client,control
import re,sys
from resources.lib.modules.log_utils import log

class info():
    def __init__(self):
        self.mode = 'dimsport'
        self.name = 'Dimsports.eu'
        self.icon = 'dimsport.png'
        self.categorized = True
        self.paginated = False
        self.multilink = True

class main():
    def __init__(self):
        self.base = 'http://idimsports.eu'

    def categories(self):
        cats = [('http://idimsports.eu/football.html','Football','icons/soccer.png'),('http://idimsports.eu/american-football.html','American Football','icons/football.png'),
                ('http://idimsports.eu/basketball.html','Basketball','icons/basketball.png'),('http://idimsports.eu/boxing-wwe-ufc.html', 'Fighting','icons/fighting.png'),
                ('http://idimsports.eu/rugby.html', 'Rugby', 'icons/rugby.png'), ('http://idimsports.eu/ice-hockey.html', 'Ice Hockey', 'icons/hockey.png'),
                ('http://idimsports.eu/tennis.html', 'Tennis', 'icons/tennis.png'), ('http://idimsports.eu/motosport.html', 'Motorsport', 'icons/f1.png'),
                ('http://idimsports.eu/golf.html', 'Golf', 'icons/golf.png'), ('http://idimsports.eu/cricket.html', 'Cricket', 'icons/cricket.png'), ('http://idimsports.eu/baseball.html', 'Baseball', 'icons/baseball.png') ]
        return cats

    def events(self,url):
        html = client.request(url)
        events = re.findall('<span>[^<]*?</span>\s*([^<]+) </a> </h3> <div>',html)
        events = self.__prepare_dim(events,url)
        eventy =  re.findall('<span class="matchtime">([^<]+)</span> </span>\s*([^<]+)</a> </h3>',html)
        events = self.__prepare_events(events,eventy,url)
        return events

    def links(self,url):
        ur = url.split('@')
        url, tag = ur[0], ur[1]
        html = client.request(url)
        links = re.findall("title=[\"'](%s[^'\"]+)[\"']\s*href=[\"'](/watch/\d+/\d+/[^'\"]+)[\"']"%tag, html)
        links = self.__prepare_links(links)
        return links



    @staticmethod
    def convert_time(time):
        li = time.split(':')
        hour,minute=li[0],li[1]
        if int(hour)>23:
            hour = int(hour)%24
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
        for link in links:
            title = link[0]
            url = self.base + link[1]
            new.append((url,title))
        return new


    def __prepare_dim(self,events,url):
        new = []
        for event in events:

            uri = url+'@%s'%event
            title = event
            new.append((uri,title))

        return new

    def __prepare_events(self,events,eventy,url):

        for ev in eventy:
            uri = url + '@%s'%ev[1]
            time = ev[0]
            time = self.convert_time(time)
            title = ev[1]
            title = '[COLOR orange](%s)[/COLOR] %s'%(time,title)
            events.append((uri,title))
        return events

    def resolve(self,url):
        import liveresolver
        return liveresolver.resolve(url,cache_timeout=0)