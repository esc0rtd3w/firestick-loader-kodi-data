from resources.lib.modules import client,control
import re,sys

class info():
    def __init__(self):
        self.mode = 'wiz1'
        self.name = 'Wiz1.net'
        self.icon = 'wiz1.png'
        self.categorized = False
        self.paginated = False
        self.multilink = False

class main():
    def __init__(self):
        self.base = 'http://www.wiz1.net'
        self.html = client.request(self.base)
        self.base = self.base + re.findall('<iframe src="(.+?)"',self.html)[0]
        self.html = client.request(self.base)


    def events(self):
        reg = re.compile('>\s*(.+?)<font color=".+?"><b>(.+?)</b></font>(.+?)<a href="(.+?)" target="_blank">')
        events = re.findall(reg,self.html)
        events = self.__prepare_events(events)
        return events

    @staticmethod
    def convert_time(time):
        time = time.replace('<hr>','').replace('<br>','')
        time = time.split(' -')[0]
        li = time.split(':')
        hour,minute=li[0],li[1]
        
        import datetime
        from resources.lib.modules import pytzimp
        d = pytzimp.timezone(str(pytzimp.timezone('Africa/Luanda'))).localize(datetime.datetime(2000 , 1, 1, hour=int(hour), minute=int(minute)))
        timezona= control.setting('timezone_new')
        my_location=pytzimp.timezone(pytzimp.all_timezones[int(timezona)])
        convertido=d.astimezone(my_location)
        fmt = "%H:%M"
        time=convertido.strftime(fmt)
        return time

    def __prepare_events(self,events):
        new = []
        for event in events:
            url = event[3]
            sport = event[1]
            title = event[2]
            time = self.convert_time(event[0])
            title = '[COLOR orange](%s)[/COLOR] (%s) [B]%s[/B]'%(time,sport,title)
            new.append((url,title))

        return new

    def resolve(self,url):
        import liveresolver
        return liveresolver.resolve(url,cache_timeout=0)