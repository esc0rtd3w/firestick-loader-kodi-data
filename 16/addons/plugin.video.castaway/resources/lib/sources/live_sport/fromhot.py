from resources.lib.modules import client,webutils,convert
import re,sys,urllib
from resources.lib.modules.log_utils import log

class info():
    def __init__(self):
        self.mode = 'fromhot'
        self.name = 'fromhot.com'
        self.icon = 'fromhot.png'
        self.categorized = True
        self.paginated = False
        self.multilink = True

class main():
    def __init__(self):
        self.base = 'http://www.fromhot.com/'

    def categories(self):
        cats = [('#live','[B]Live[/B]','live.png'),('http://www.sportcategory.com/c-1.html','Football','icons/soccer.png'),
                ('http://www.sportcategory.com/c-6.html','Basketball','icons/basketball.png'),('http://www.sportcategory.com/c-3.html', 'Ice Hockey', 'icons/hockey.png'),
                ('http://www.sportcategory.com/c-4.html', 'Tennis', 'icons/tennis.png'), ('http://www.sportcategory.com/c-10.html', 'Motorsports', 'icons/f1.png'),
                ('http://www.sportcategory.com/c-8.html', 'Golf', 'icons/golf.png'), ('http://www.sportcategory.com/c-7.html', 'Baseball', 'icons/baseball.png'), 
                ('http://www.sportcategory.com/c-9.html','Cycling','icons/cycling.png'),('http://www.sportcategory.com/c-11.html','Other','icons/snooker.png')]
        return cats

    def events(self,url):
        if url == '#live':
            html = client.request(self.base)
        else:
            html = client.request(url)
        events = re.findall('>(\d+:\d+)</span> - <.+?class=[\"\']flg.+?[\"\']>.+?<td>([^<]+)</td><td.+?target=[\"\']_blank[\"\'].+?title=[\"\']Open Video[\"\']>([^<]+)<.+?id=.+?a href=[\"\']([^\"\']+)',html)
        events = self.__prepare_events(events)
        return events

    def links(self,url):
        html = client.request(url)
        title = re.findall('<h2>([^<]+)<',html)[0]
        links = re.findall('href=[\"\'](http://www.sportingvideo.org[^\"\']+.html)[\"\']',html)
        links=self.__prepare_links(links,title)
        return links



    @staticmethod
    def convert_time(time):             
        
        li = time.split(':')
        hour,minute=li[0],li[1]
        
        time = "%s:%s"%(hour,minute)
        return time

    def __prepare_links(self,links,titl):
        new=[]
        i = 1
        for link in links:
            title = '%s Link %s'%(titl,i)
            i += 1
            url = link
            new.append((url,title))
            
        return new


    

    def __prepare_events(self,events):
        out=[]
        urls = []
        for ev in events:
            uri = ev[3]
            time = self.convert_time(ev[0])
            title = ev[2]
            league = ev[1]
            title = '[COLOR orange](%s)[/COLOR] (%s) %s'%(time,league,title)
            if uri not in urls:
                urls.append(uri)
                out.append((uri,title))
        return out

    def resolve(self,url):
        html = client.request(url)
        try:
            html= convert.unescape(html)
        except:
            pass
        res = url
        try:
            res = urllib.unquote(re.findall('unescape\s*\(\s*[\"\']([^\"\']+)',html)[0])
            res = re.findall('(?:href|src)=[\"\']([^\"\']+)',res)[0]
        except:
            pass
        
        import liveresolver
        return liveresolver.resolve(res)