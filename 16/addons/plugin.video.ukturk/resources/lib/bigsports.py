import urllib,urllib2,re,os

def scrape():
    string=''
    link=open_url("http://www.bigsports.me/cat/4/football-live-stream.html")
    livegame=re.compile('<td>.+?<td>(.+?)\-(.+?)\-(.+?)</td>.+?<td>(.+?)\:(.+?)</td>.+?<td>Football</td>.+?<td><strong>(.+?)</strong></td>.+?<a target=.+? href=(.+?) class=.+?',re.DOTALL).findall(link)
    for day,month,year,hour,mins,name,url in livegame:
        url=url.replace('"','')
        date=day+' '+month+' '+year
        time=hour+':'+mins
        date='[COLOR gold]'+date+'[/COLOR]'
        time='[COLOR blue]('+time+')[/COLOR]'
        string=string+'\n<item>\n<title>%s</title>\n<sportsdevil>%s</sportsdevil>\n'%(date+' '+time+' '+name,url)
        string=string+'<thumbnail>ImageHere</thumbnail>\n<fanart>fanart</fanart>\n</item>\n'
    return string

def open_url(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36')
    response = urllib2.urlopen(req)
    link=response.read()
    return link

