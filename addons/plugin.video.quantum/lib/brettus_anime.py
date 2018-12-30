import xbmc,xbmcaddon,xbmcgui,xbmcplugin,urllib,urllib2,os,re,sys,shutil,urlresolver, process
baseurl         = 'http://brettusbuilds.com/Anime%20/anime%20index.xml'

def GetList():
        link=process.OPEN_URL(baseurl)
        match= re.compile('<link>(.+?)</link><thumbnail>(.+?)</thumbnail><title>(.+?)</title>').findall(link)
        for url,iconimage,name in match:
                if not 'http' in iconimage:iconimage=''
                process.Menu(name,url,1601,iconimage,'','','')

def GetContent(url,iconimage):
        link=process.OPEN_URL(url)
        match= re.compile('<link>(.+?)</link><thumbnail>(.+?)</thumbnail><title>(.+?)</title>').findall(link)
        for url,iconimage,name in match:
                if not 'http' in iconimage:iconimage=''
                if '/brettusbuilds.com/' in url:
                    process.Menu(name,url,1601,iconimage,'','','')
                else:process.Play(name,url,906,iconimage,'','','')
