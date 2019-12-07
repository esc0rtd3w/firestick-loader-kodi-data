import urllib,urllib2,re,os

def scrape(): 
    string=''
    link=open_url("http://cricfree.sc/football-live-stream")
    events=re.compile('<td><span class="sport-icon(.+?)</tr>',re.DOTALL).findall(link)
    for event in events:
        cal=re.compile('<td>(.+?)<br(.+?)</td>').findall(event)
        for day,date in cal:
            day='[COLOR gold]'+day+'[/COLOR]'
            date=date.replace('>','')   
        time=re.compile('<td class="matchtime" style="color:#545454;font-weight:bold;font-size: 9px">(.+?)</td>').findall(event)[0]
        time='[COLOR blue]('+time+')[/COLOR]'
        naurl=re.compile('<a style="text-decoration:none !important;color:#545454;" href="(.+?)" target="_blank">(.+?)</a></td>').findall(event)
        for url,progname in naurl:
            url=url
            progname=progname
        string=string+'\n<item>\n<title>%s</title>\n<sportsdevil>%s</sportsdevil>\n'%(day+' '+time+' - '+progname,url)
        string=string+'<thumbnail>ImageHere</thumbnail>\n<fanart>fanart</fanart>\n</item>\n'
    return string

def open_url(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36')
    response = urllib2.urlopen(req)
    link=response.read()
    return link
