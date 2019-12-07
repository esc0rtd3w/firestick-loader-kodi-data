from resources.lib.modules import client,control
from resources.lib.modules.log_utils import log
import re,sys

class info():
    def __init__(self):
        self.mode = 'ifirstrow'
        self.name = 'ifirstrow.eu'
        self.icon = 'ifirstrow.png'
        self.categorized = True
        self.paginated = False
        self.multilink = True

class main():
    def __init__(self):
        self.base = 'http://ifirstrow.eu'

    def categories(self):
        cats = [('http://ifirstrow.eu/sport/football.html','Football','icons/soccer.png'),('http://ifirstrow.eu/sport/american-football.html','American Football','icons/football.png'),
                ('http://ifirstrow.eu/sport/basketball.html','Basketball','icons/basketball.png'),('http://ifirstrow.eu/sport/boxing-wwe-ufc.html', 'Fighting','icons/fighting.png'),
                ('http://ifirstrow.eu/sport/rugby.html', 'Rugby', 'icons/rugby.png'), ('http://ifirstrow.eu/sport/ice-hockey.html', 'Ice Hockey', 'icons/hockey.png'),
                ('http://ifirstrow.eu/sport/tennis.html', 'Tennis', 'icons/tennis.png'), ('http://ifirstrow.eu/sport/motosport.html', 'Motorsport', 'icons/f1.png'),
                ('http://ifirstrow.eu/sport/golf.html', 'Golf', 'icons/golf.png'), ('http://ifirstrow.eu/sport/cricket.html', 'Cricket', 'icons/cricket.png') ]
        return cats

    def events(self,url):
        html = client.request(url)
        events = re.findall('<img class="chimg" alt="(.+?)" src=".+?"/> <span> &nbsp;.+?\s*(?:<span class="matchtime"|</span)>(.+?)<',html)
        events = self.__prepare_events(events,url)
        return events

    def links(self,url):
        ur = url.split('@')
        url, tag = ur[0], ur[1]
        html = client.request(url)
        links = re.findall("href=[\"'](.+?)[\"'] title=[\"']%s (.+?)[\"'] target=_blank>"%tag, html)
        links = self.__prepare_links(links)
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
        for link in links:
            title = link[1]
            url = self.base + link[0]
            new.append((url,title))
        return new


    def __prepare_events(self,events,url):
        new = []
        for ev in events:
            uri = url + '@%s'%ev[0]
            time = ev[1]
            try:    time = self.convert_time(time)
            except: time = '00:00'
            title = ev[0]
            title = '[COLOR orange](%s)[/COLOR] %s'%(time,title)
            new.append((uri,title))
        return new

    def resolve(self,url):
        import liveresolver
        return liveresolver.resolve(url,cache_timeout=0)