from resources.lib.modules import client,webutils,control
import re,sys,xbmcgui,os


AddonPath = control.addonPath
IconPath = AddonPath + "/resources/media/"
def icon_path(filename):
    return os.path.join(IconPath, filename)

class info():
    def __init__(self):
        self.mode = 'livefootballvideo'
        self.name = 'Livefootballvideo.com'
        self.icon = icon_path('livefootballvideo.png')
        self.categorized = False
        self.paginated = False
        self.multilink = True

class main():
    def __init__(self):
        self.base = 'http://livefootballvideo.com/'        

    def links(self,url):
        result = client.request(url)
        soup=webutils.bs(result)
        ls = soup.findAll('tr')
        links = self.__prepare_links2(ls)
        return links

    def channels(self):
        result = client.request('http://livefootballvideo.com/streaming')
        events=re.findall('<li\s*(?:class="odd")?>\s*<div\s*class="leaguelogo\s*column">\s*<img.+?src=".+?"\s*alt=".+?"/>\s*</div>\s*<div\s*class="league\s*column">\s*<a\s*href=".+?"\s*title=".+?">(.+?)</a>\s*</div>\s*<div\s*class="date_time\s*column"><span\s*class="starttime\s*time"\s*rel="(.+?)">.+?</span></div>\s*<div\s*class="team\s*column"><img.+?alt="(.+?)"\s*src=".+?"><span>.+?</span></div>\s*<div\s*class="versus\s*column">vs.</div>\s*<div\s*class="team\s*away\s*column"><span>(.+?)</span><img.+?alt=".+?"\s*src=".+?"></div>\s*<div\s*class="live_btn\s*column">\s*<a\s*(class="online")?\s*href="(.+?)">',result)
        events = self.__prepare_events(events)
        return events

    


    @staticmethod
    def convert_time(time):             
        import datetime
        time = datetime.datetime.fromtimestamp(float(time)).strftime('%H:%M')
        li = time.split(':')
        hour,minute=li[0],li[1]
        
        time = "%s:%s"%(hour,minute)
        return time

    def __prepare_events(self,events):
        new = []

        for event in events:
            url = event[5]
            color = 'orange'
            if 'online' in event[4]:
                color = 'red'
            sport = event[0]
            home = event[2]
            away = event[3]
            title = '%s - %s'%(home,away)
            time = self.convert_time(event[1])
            title = '[COLOR %s](%s)[/COLOR] (%s) [B]%s[/B]'%(color,time,sport,title)
            new.append((url,title, info().icon))
        return new

    def __prepare_links(self,links):
        new=[]
        for link in links:
            url = link[4]
            service = link[0].title()
            name = link[1]
            lang = link[2]
            kbps = link[3]
            title = "%s (%s, %skbps) - %s"%(name, lang, kbps, service)
            if 'sopcast' in service or 'acestream' in service:
                new.append((url,title, info().icon))
        return new

    def __prepare_links2(self,links):
        new=[]
        for link in links:
            try:
                tds=link.findAll('td')
                name=tds[1].getText()
                if 'Kick off' in name:
                    continue
                try:lang=tds[2].getText().replace('-','N/A')
                except: lang='-'
                try:kbps=tds[3].getText().replace('-','N/A')
                except:kbps='-'
                url = link.findAll('a')[1]['href']
                service = link.find('a')['title']
                
                title = "%s (%s, %s) - %s"%(name, lang, kbps, service)
                if 'sopcast' in service or 'acestream' in service:
                    new.append((url,title, info().icon))
            except:
                pass
        return new

    def resolve(self,url):
        import liveresolver
        return liveresolver.resolve(url,cache_timeout=0)