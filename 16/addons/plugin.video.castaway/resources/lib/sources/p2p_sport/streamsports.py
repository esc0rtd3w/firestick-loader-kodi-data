from resources.lib.modules import client,webutils,control
import re,sys,xbmcgui,os


AddonPath = control.addonPath
IconPath = AddonPath + "/resources/media/"
def icon_path(filename):
    return os.path.join(IconPath, filename)
class info():
    def __init__(self):
        self.mode = 'streamsports'
        self.name = 'Streamsports.me'
        self.icon = icon_path('streamsports.png')
        self.categorized = False
        self.paginated = False
        self.multilink = True

class main():
    def __init__(self):
        self.base = 'http://www.streamsports.me'


    def links(self,url):
        html = client.request(url)
        soup = webutils.bs(html)
        links = soup.findAll('tr')
        links.pop(0)
        links.pop(0)
        links = self.__prepare_links(links)
        return links




    def channels(self):
        html = client.request(self.base)
        soup = webutils.bs(html)
        events = soup.findAll('tr')
        events = self.__prepare_events(events)
        return events

    @staticmethod
    def convert_time(time):
        time = time.replace('<hr>','').replace('<br>','')
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

    def __prepare_events(self,events):
        new = []
        for ev in events:
            try:
                event = ev.findAll('td')
                time = event[0].findAll('span')[1].getText().strip()
                sport = event[1].getText().strip() + '-' +event[2].findAll('span')[1].getText().strip()
                title = event[3].findAll('span')[0].getText() + ' - ' + event[3].findAll('span')[1].getText()
                time = self.convert_time(time)
                url = self.base + event[4].find('a')['href']
                title = '[COLOR orange](%s)[/COLOR] (%s) [B]%s[/B]'%(time,sport,title)
                title = title.encode('utf-8')
                new.append((url,title,info().icon))
            except:
                pass

        return new

    def __prepare_links(self,links):
        new = []
        
        for l in links:
            try:
                infoa = l.findAll('td')
                kbps = infoa[1].getText().strip()
                service = infoa[2].getText().strip()
                lang = infoa[3].getText().strip()
                type = infoa[4].getText().strip()
                url = infoa[5].find('a')['href']
                title = "%s (%s, %s)"%(service, lang, kbps)
                if type.lower()=='p2p':
                    new.append((url,title, info().icon))
                
            except:
                pass
        
        return new

    def resolve(self,url):
        import liveresolver
        return liveresolver.resolve(url,cache_timeout=0)