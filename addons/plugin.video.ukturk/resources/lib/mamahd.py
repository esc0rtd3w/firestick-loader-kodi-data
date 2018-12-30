import urllib,urllib2,re,os

def scrape():
    string=''
    link=open_url("http://mamahd.com/index1.html").replace('\n','').replace('\t','')
    allgames=re.compile('<div class="schedule">(.+?)<div id="pagination">').findall(link)[0]
    livegame=re.compile('<a href="(.+?)">.+?<img src="(.+?)".+?<div class="home cell">.+?<span>(.+?)</span>.+?<span>(.+?)</span>.+?</a>').findall(allgames)
    for url,iconimage,home,away in livegame:
        string=string+'<item>\n<title>%s vs %s</title>\n<sportsdevil>%s</sportsdevil>\n<thumbnail>%s</thumbnail>\n<fanart>fanart</fanart>\n</item>\n\n'%(home,away,url,iconimage)
    return string

def open_url(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36')
    response = urllib2.urlopen(req)
    link=response.read()
    return link

