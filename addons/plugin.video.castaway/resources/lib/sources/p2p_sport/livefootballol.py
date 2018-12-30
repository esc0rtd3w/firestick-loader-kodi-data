from resources.lib.modules import client,webutils,control
import re,sys,xbmcgui,os


AddonPath = control.addonPath
IconPath = AddonPath + "/resources/media/"
def icon_path(filename):
    return os.path.join(IconPath, filename)

class info():
    def __init__(self):
        self.mode = 'livefootballol'
        self.name = 'livefootballol.com'
        self.icon = icon_path('livefootballol.png')
        self.categorized = False
        self.paginated = False
        self.multilink = True

class main():
    def __init__(self):
        self.base = 'http://www.livefootballol.me'        

    def links(self,url):
        if url=='x':
            return ['x']
        result = client.request(url)
        links = re.findall('<td>(.+?)</td>\s*<td><a href="(.+?)"><strong>(.+? (?:AceStream|Sopcast))</strong>', result)
        links = self.__prepare_links(links)
        return links

    def channels(self):
        result = client.request(self.base + '/live-football-streaming-2016.html')
        dates=re.findall('<h3>(.+?)\s*CEST</h3></div>\s*<list class="uk-list uk-list-striped">',result)
        d = webutils.bs(result).findAll('list', {'class': 'uk-list uk-list-striped'})
        events = self.__prepare_events(dates, d)
        return events

    


    @staticmethod
    def convert_time(time):             
        li = time.split(':')
        hour,minute=li[0],li[1]
        import datetime
        from resources.lib.modules import pytzimp
        d = pytzimp.timezone(str(pytzimp.timezone('Europe/Ljubljana'))).localize(datetime.datetime(2000 , 1, 1, hour=int(hour), minute=int(minute)))
        timezona= control.setting('timezone_new')
        my_location=pytzimp.timezone(pytzimp.all_timezones[int(timezona)])
        convertido=d.astimezone(my_location)
        fmt = "%H:%M"
        time=convertido.strftime(fmt)
        return time

    def __prepare_events(self,dates, d):
        new = []

        for i in range(len(dates)):
            new.append(('x','[COLOR yellow]%s[/COLOR]'%dates[i], info().icon))
            events = re.findall('<img.+?alt="(.+?)"\s*/>\s*(\d+:\d+)\s*\[(.+?)\]\s*<a href="(/streaming.+?)"(?: target="_blank")?>(.+?)<',str(d[i]))
            for e in events:
                league = e[0]
                time = self.convert_time(e[1])
                sport = e[2]
                url = self.base + e[3]
                title = e[4]
                title = '[COLOR orange](%s)[/COLOR] (%s) [B]%s[/B]'%(time,sport, title)
                new.append((url,title, info().icon))

        return new

    def __prepare_links(self,links):
        new=[]
        for link in links:
            lang = link[0]
            if '[' not in lang:
                lang = ''
            lang = lang.replace('[','').replace(']','')
            url = link[1]
            name = link[2]
            title = "%s %s" %(lang,name)
            new.append((url,title, info().icon))
        return new

    def resolve(self,url):
        html = client.request(url)
        url = re.findall('[\"\']((?:sop|acestream)://[^\"\']+)[\"\']',html)[0]
        import liveresolver
        return liveresolver.resolve(url)