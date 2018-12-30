from resources.lib.modules import client,webutils
import re,sys

class info():
    def __init__(self):
        self.mode = 'wizhdsports'
        self.name = 'wizhdsports.com'
        self.icon = 'wizhdsports.jpg'
        self.categorized = True
        self.paginated = False
        self.multilink = True

class main():
    def __init__(self):
        self.base = 'http://wizhdsports.com/'

    def categories(self):
        cats = [('#live','[B]Live[/B]','live.png'),
                ('http://wizhdsports.com/sports/Football.html','Football','icons/soccer.png'),('http://wizhdsports.com/sports/NFL.html','American Football','icons/football.png'),
                ('http://wizhdsports.com/sports/NBA.html','Basketball','icons/basketball.png'),('http://wizhdsports.com/sports/Boxing.html', 'Boxing','icons/fighting.png'),
                ('http://wizhdsports.com/sports/Rugby.html', 'Rugby', 'icons/rugby.png'), ('http://wizhdsports.com/sports/NHL.html', 'Ice Hockey', 'icons/hockey.png'),
                ('http://wizhdsports.com/sports/Tennis.html', 'Tennis', 'icons/tennis.png'), ('http://wizhdsports.com/sports/Motorsport.html', 'Motorsport', 'icons/f1.png'),
                ('http://wizhdsports.com/sports/Golf.html', 'Golf', 'icons/golf.png'), ('http://wizhdsports.com/sports/Cricket.html', 'Cricket', 'icons/cricket.png'), 
                ('http://wizhdsports.com/sports/Baseball.html', 'Baseball', 'icons/baseball.png'), ('http://wizhdsports.com/sports/Darts.html', 'Darts', 'icons/darts.png'),
                ('http://wizhdsports.com/sports/WWE.html','WWE','icons/fighting.png'),('http://wizhdsports.com/sports/Horse-Racing.html','Horse Racing','icons/horse_racing.png'),
                ('http://wizhdsports.com/sports/UFC.html','UFC','icons/fighting.png'),('http://wizhdsports.com/sports/Other.html','Other','icons/snooker.png')]
        return cats

    def events(self,url):
        if url == '#live':
            html = client.request(self.base)
        else:
            html = client.request(url)
        if url == '#live':
            events = re.findall('<input type="hidden" id="startTime(\d+)" value="(\d+)"\s*/>\s*<input type="hidden".+?/>\s*<span id=.+?">\s*.+?</span>\s*.+?\s*<span id=.+?>\s*.+?\s*</span>\s*</div>\s*<div class="name">(.+?)</div>\s*<\!.+?\s*<div.+?\s*<img\s*src=..+?live.gif',html)
        else:
            events = re.findall('<input type="hidden" id="startTime(\d+)" value="(\d+)"\s*/>\s*<input type="hidden".+?/>\s*<span id=.+?">\s*.+?</span>\s*.+?\s*<span id=.+?>\s*.+?\s*</span>\s*</div>\s*<div class="name">(.+?)</div>',html)
        if url=='#live':
            url = self.base
        events = self.__prepare_events(events,url)
        return events

    def links(self,url):
        ur = url.split('@')
        url, tag = ur[0], ur[1]
        html = client.request(url)
        soup = webutils.bs(html)
        ls = soup.find('div',{'id':'channel%s'%tag}).findAll('a')
        links=self.__prepare_links(ls)
        return links



    @staticmethod
    def convert_time(time):             
        import datetime
        time = datetime.datetime.fromtimestamp(float(time)).strftime('%H:%M')
        li = time.split(':')
        hour,minute=li[0],li[1]
        
        time = "%s:%s"%(hour,minute)
        return time

    def __prepare_links(self,links):
        new=[]
        for link in links:
            title = link.getText().replace('()','').strip().encode('utf-8')
            url = link['href']
            new.append((url,title))
        return new


    

    def __prepare_events(self,events,url):
        out=[]
        for ev in events:
            uri = url + '@%s'%ev[0]
            time = self.convert_time(ev[1])
            title = ev[2]
            title = '[COLOR orange](%s)[/COLOR] %s'%(time,title)
            out.append((uri,title))
        return out

    def resolve(self,url):
        import liveresolver
        return liveresolver.resolve(url)