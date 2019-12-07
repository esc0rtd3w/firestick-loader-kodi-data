import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc, xbmcaddon, os, sys
import urlresolver
from metahandler import metahandlers
addon_id = 'plugin.video.docuhub'




#ReddiTube - Blazetamer.
addon = xbmcaddon.Addon ('plugin.video.docuhub')
#URL= 'http://www.xbmchub.com'

#PATHS
addonPath = addon.getAddonInfo('path')
artPath = addonPath + '/art/'
fanartPath = addonPath + '/art/'

#HOOKS
settings = xbmcaddon.Addon(id='plugin.video.docuhub')

#Setup Meta
grab=metahandlers.MetaData()

def GRABMETA(name,year):
        meta = grab.get_meta('movie',name,year,None,None,overlay=6)
        infoLabels = {'rating': meta['rating'],'duration': meta['duration'],'genre': meta['genre'],'mpaa':"rated %s"%meta['mpaa'],
        'plot': meta['plot'],'title': meta['title'],'writer': meta['writer'],'cover_url': meta['cover_url'],
        'director': meta['director'],'cast': meta['cast'],'backdrop_url': meta['backdrop_url'],'tmdb_id': meta['tmdb_id'],'year': meta['year']}
                
        return infoLabels


#AutoView
def AUTO_VIEW(content):
        if content:
                xbmcplugin.setContent(int(sys.argv[1]), content)
                if settings.getSetting('auto-view') == 'true':
                        if content == 'movies':
                                xbmc.executebuiltin("Container.SetViewMode(%s)" % settings.getSetting('movies-view') )
                        if content == 'list':
                                xbmc.executebuiltin("Container.SetViewMode(%s)" % settings.getSetting('list-view') )
                else:
                        xbmc.executebuiltin("Container.SetViewMode(%s)" % settings.getSetting('default-view') )    


#Main Links 
def CATEGORIES():
        if settings.getSetting('topdocfilms') == 'true':
                addDir('Top Documentary Films ','none','topdoc',artPath+'topdocfilm.png')
        if settings.getSetting('docnet') == 'true':        
                addDir('Documentary.net','none','docnet',artPath+'docnet.png')
        if settings.getSetting('doclog') == 'true':        
                addDir('Documentary-Log ','none','doclog',artPath+'doculog.png')
        if settings.getSetting('docstorm') == 'true':        
                addDir('Documentary Storm ','none','docstorm',artPath+'docstorm.png')
        if settings.getSetting('resolver') == 'true':
                addDir('[COLOR gold]Resolver Settings[/COLOR]','none','resolverSettings','')        
        AUTO_VIEW('list')

def TOPDOC():
        addDir('9/11','http://topdocumentaryfilms.com/category/911/','tdindex','')
        addDir('Art/Artists','http://topdocumentaryfilms.com/category/art-artists/','tdindex','')
        addDir('Biography','http://topdocumentaryfilms.com/category/biography/','tdindex','')
        addDir('Comedy','http://topdocumentaryfilms.com/category/comedy/','tdindex','')
        addDir('Crime/Conspiracy','http://topdocumentaryfilms.com/category/crime-conspiracy/','tdindex','')
        addDir('Crime','http://topdocumentaryfilms.com/category/crime/','tdindex','')
        addDir('Drugs','http://topdocumentaryfilms.com/category/drugs/','tdindex','')
        addDir('Economics','http://topdocumentaryfilms.com/category/economics/','tdindex','')
        addDir('Enviroment','http://topdocumentaryfilms.com/category/enviroment/','tdindex','')
        addDir('Health','http://topdocumentaryfilms.com/category/health/','tdindex','')
        addDir('History','http://topdocumentaryfilms.com/category/history/','tdindex','')
        addDir('Media','http://topdocumentaryfilms.com/category/media/','tdindex','')
        addDir('Military/War','http://topdocumentaryfilms.com/category/military-war/','tdindex','')
        addDir('Mystery','http://topdocumentaryfilms.com/category/mystery/','tdindex','')
        addDir('Nature/Wildlife','http://topdocumentaryfilms.com/category/nature-wildlife/','tdindex','')
        addDir('Performing Arts','http://topdocumentaryfilms.com/category/music-performing-arts/','tdindex','')
        addDir('Philosophy','http://topdocumentaryfilms.com/category/philosophy/','tdindex','')
        addDir('Politics','http://topdocumentaryfilms.com/category/politics/','tdindex','')
        addDir('Psychology','http://topdocumentaryfilms.com/category/psychology/','tdindex','')
        addDir('Religion','http://topdocumentaryfilms.com/category/religion/','tdindex','')
        addDir('Science/Tech','http://topdocumentaryfilms.com/category/science-technology/','tdindex','')
        addDir('Sexuality','http://topdocumentaryfilms.com/category/sex/','tdindex','')
        addDir('Society','http://topdocumentaryfilms.com/category/society/','tdindex','')
        addDir('Sports','http://topdocumentaryfilms.com/category/sports/','tdindex','')
        addDir('Technology','http://topdocumentaryfilms.com/category/technology/','tdindex','')
        AUTO_VIEW('list')       

def DOCNET():
        addDir('Latest Documentaries','http://documentary.net/','docnetlatest','')
        addDir('Catagories','http://documentary.net/','docnetcat','')
        AUTO_VIEW('list')
        

def DOCLOG():
        addDir('Latest Documentaries','http://www.documentary-log.com/','docloglatest','')
        addDir('Catagories','http://www.documentary-log.com/','doclogcat','')
        AUTO_VIEW('list')

        
def DOCSTORM():
        addDir('Latest Documentaries','http://documentarystorm.com/','stormlatest','')
        addDir('Catagories','http://documentarystorm.com/','stormcat','')
        AUTO_VIEW('list')

#First Links from RSS 
def TDINDEX(url):
        #link = net.http_GET(url).content
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('"postTitle"><a\nhref="(.+?)" title="(.+?)">').findall(link)
        #matchimg=re.compile('src="(.+?)" class="alignleft').findall(link)
        for url,name in match:
            name =name.replace("&#039;s","'s")
         #for thumb in matchimg:        
            addDir(name,url,'tdvidpage','')
            match=re.compile('rel="next" href="(.+?)"').findall(link)
        if len(match) > 0:
                addDir('Next Page',(match[0]),'tdindex',artPath+'next.png')
                AUTO_VIEW('list')

# For Documentary.net
def DOCNETINDEX(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<a href="(.+?)"   class=\'fix\'><img src="(.+?)" alt="(.+?)"').findall(link)
        #matchimg=re.compile('src="(.+?)" class="alignleft').findall(link)
        for url,iconimage,name in match:
                name =name.replace("&#039;s","'s")
         #for thumb in matchimg:        
                addDir(name,url,'docnetvidpage',iconimage)
        match=re.compile("<a class='page-numbers' href='(.+?)'>(.+?)</a>").findall(link)
        for url, number in match:
          if len(match) > 0:
                  addDir('Page'+number,'http://documentary.net'+url,'docnetindex',artPath+'next.png')
                  AUTO_VIEW('movies')


def DOCNETCAT(url):
#link = net.http_GET(url).content
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<li><a href="(.+?)">(.+?)</a>').findall(link)
        for url,name in match:
         #for thumb in matchimg:        
            addDir(name,url,'docnetindex','')
            AUTO_VIEW('list')            

def DOCNETLATEST(url):
#link = net.http_GET(url).content
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<a href="(.+?)"   class=.+?><img src="(.+?)" alt="(.+?)" />').findall(link)
        #matchimg=re.compile('src="(.+?)" class="alignleft').findall(link)
        for url,iconimage,name in match:
             name =name.replace("&#039;s","'s")
             name =name.replace("&#8211;","-")   
         #for thumb in matchimg:        
             addDir(name,url,'docnetvidpage',iconimage)
             AUTO_VIEW('movies')

def STORMLATEST(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('class="cover">\r\n\t\t<a href="(.+?)" title="(.+?)" >\r\n   \t\t\t<img width="198" height="297" src="(.+?)"').findall(link)
        for url,name,iconimage in match:        
            addDir(name,url,'stormvidpage',iconimage)
            AUTO_VIEW('movies')

def STORMCAT(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<a href="(.+?)" title=".+?">(.+?)</a></li>').findall(link)
        for url,name in match:        
            addDir(name,url,'stormindex','')
            AUTO_VIEW('list')

def STORMINDEX(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('class="cover">\r\n\t\t<a href="(.+?)" title="(.+?)" >\r\n   \t\t\t<img width="198" height="297" src="(.+?)"').findall(link)
        for url,name,iconimage in match:
                name =name.replace("&#039;s","'s")
                name =name.replace("&#8211;","-")        
                addDir(name,url,'stormvidpage',iconimage)
        match=re.compile('<link rel="next" href="(.+?)" />').findall(link)
        if len(match) > 0:
           addDir('Next Page',(match[0]),'stormindex',artPath+'next.png')
           AUTO_VIEW('movies')

def STORMVIDPAGE(url,name):
        #link = net.http_GET(url).content
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        #match=re.compile('<p><iframe src="(.+?)" .+?" .+?"').findall(link)==========old links
        match=re.compile('<p><iframe width=".+?" height=".+?" src="(.+?)" frameborder=".+?" ').findall(link)
        if len(match) > 0:
           for url in match:
                if 'youtube' in url:
                        if 'http:' in url:
                                url = url.replace('http:','')
                                
                                url = url.replace('//www.youtube.com/embed/','http://www.youtube.com/embed?v=')
                                   
                                RESOLVE(name,url,'')

                                AUTO_VIEW('movies')
                        else:
                                url = url.replace('//www.youtube.com/embed/','http://www.youtube.com/embed?v=')
                                   
                                RESOLVE(name,url,'')

                                AUTO_VIEW('movies')
#for Vimeo first page
        #if len(match)<1:           
        if 'vimeo' in url:
                #else:   
        
                #match=re.compile('<p><iframe src="(.+?)" .+?" .+?"').findall(link)
                for url in match:
                         #url = url.replace('//player.vimeo.com/video/','http://player.vimeo.com/video/')
                        
                         TDVIMEO(name,url,'')

                         AUTO_VIEW('movies')

        else:
                match=re.compile('<iframe class=".+?" width=".+?" src="(.+?)" frameborder=').findall(link)
                for url in match:
                        TDVIMEO(name,url,'')

                        AUTO_VIEW('movies')
                
            
def DOCLOGCAT(url):
#link = net.http_GET(url).content
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<li class=".+?"><a href="(.+?)" title=".+?">(.+?)</a>').findall(link)
        for url,name in match:       
            addDir(name,url,'docloglatest','')
            AUTO_VIEW('list')

def DOCLOGVIDPAGE(url):
        #link = net.http_GET(url).content
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<iframe.*?src="(http://.+?)".*?>').findall(link)
        for url in match:
                if 'youtube' in url:
                   url = url.replace('embed/','embed?v=')
                    
                   RESOLVE(name,url,'')

                   AUTO_VIEW('movies')

#for Vimeo first page
        #if len(match)<1:           
        if 'vimeo' in url:
                #else:   
        
                #match=re.compile('"url":"(.+?)"').findall(link)
                for url in match:
                         #url = url.replace('vimeo.com/moogaloop.swf?','player.vimeo.com/video/')
                        
                         TDVIMEO(name,url,'')

                         AUTO_VIEW('movies')                     

def DOCLOGLATEST(url):
#link = net.http_GET(url).content
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<a href="(.+?)" title="(.+?)">\r\n          <img src="(.+?)" alt=".+?" class="thumb"').findall(link)
        #matchimg=re.compile('src="(.+?)" class="alignleft').findall(link)
        for url,name,iconimage in match:
         #for thumb in matchimg:        
            addDir(name,url,'doclogvidpage',iconimage)
        match=re.compile("<a href='(.+?)' class='page larger'>(.+?)</a>").findall(link)
        for url, number in match:
         if len(match) > 0:
           addDir('Page'+number,url,'docloglatest',artPath+'next.png')
           AUTO_VIEW('movies')                        
    
# For Primary YouTube Listing                
def TDVIDPAGE(url,name):
        #link = net.http_GET(url).content
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('width=".+?" height=".+?" src="(.+?)rel=0.+?"').findall(link)
        for url in match:
                if 'http:'in url:
                   url = url.replace('embed/','embed?v=')
                    
                   RESOLVE(name,url,'')

                   AUTO_VIEW('movies')
                else:
                 
                   url = 'http:'+url
                   url = url.replace('embed/','embed?v=')
                    
                   RESOLVE(name,url,'')

                   AUTO_VIEW('movies')

#for odd YT and Vimeo first page 
        if len(match)<1:
                match=re.compile('width="530" height="325" src="(.+?)"').findall(link)
                for url in match:
                      if 'youtube' in url:
                         url = 'http:'+url
                         url = url.replace('/embed/videoseries?list=','embed?=')
                         RESOLVE(name,url,'')

                         AUTO_VIEW('movies') 
        
                
                
                      if 'vimeo' in url:  
                         TDVIMEO(name,url,'')

                         AUTO_VIEW('movies')

              
        
                                

#Scrape and Play TD Vimeo url
def TDVIMEO(name,url,iconimage):
          req = urllib2.Request(url)
          req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
          response = urllib2.urlopen(req)
          link=response.read()
          response.close()
          match=re.compile('"url":"(.+?)","height":.+?,"width":.+?,').findall(link)
          for url in match:
           ok=True
          liz=xbmcgui.ListItem(name, iconImage=iconimage,thumbnailImage=iconimage); liz.setInfo( type="Video", infoLabels={ "Title": name } )
          ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=str(url),listitem=liz)
          xbmc.executebuiltin("XBMC.Notification(Please Wait!,Preparing Your Video,3000)")
          xbmc.sleep(1000)
          xbmc.Player ().play(str(url), liz, False)

          AUTO_VIEW('')

# DocNet  Start                          
def DOCNETVIDPAGE(url,name):
        #link = net.http_GET(url).content
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('"embedURL" content="(.+?)?version').findall(link)
        for url in match:
                #url = url.replace('v/','embed?v=')
                if 'youtube' in url:
                   url = url.replace('v/','embed?v=')
                    
                   RESOLVE(name,url,'')

                   AUTO_VIEW('movies')

#for Vimeo first page
        if len(match)<1:           
        #if 'vimeo' in url:
                #else:   
        
                match=re.compile('"embedURL" content="(.+?)" />').findall(link)
                for url in match:
                         url = url.replace('vimeo.com/moogaloop.swf?','player.vimeo.com/video/')
                        
                         TDVIMEO(name,url,'')

                         AUTO_VIEW('movies')                   
                         

# Second From Source to YT
def VIDEOLINKSYT(url,name):
        link = net.http_GET(url).content
        match=re.compile('<a class="title " href="(.+?)" tabindex="1"').findall(link)
        for url in match:
         movie_name = name[:-6]
         year = name[-6:]
         movie_name = movie_name.decode('UTF-8','ignore')
                                
         data = GRABMETA(movie_name,year)
         thumb = data['cover_url']
         RESOLVEYT(name,url,iconimage)
            
         AUTO_VIEW('movies') 



def RESOLVE(name,url,iconimage):
         url = urlresolver.HostedMediaFile(url=url).resolve()
         ok=True
         liz=xbmcgui.ListItem(name, iconImage=iconimage,thumbnailImage=iconimage); liz.setInfo( type="Video", infoLabels={ "Title": name } )
         ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=str(url),listitem=liz)
         xbmc.executebuiltin("XBMC.Notification(Please Wait!,Preparing Your Video,3000)")
         xbmc.sleep(1000)
         xbmc.Player ().play(str(url), liz, False)

         AUTO_VIEW('')

#Resolve 2 forYouTube

def RESOLVEYT(name,url,iconimage):
         url = urlresolver.HostedMediaFile(url=url).resolve()
         ok=True
         liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage); liz.setInfo( type="Video", infoLabels={ "Title": name } )
         ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
         xbmc.executebuiltin("XBMC.Notification(Please Wait!,Preparing Your Video,3000)")
         xbmc.sleep(1000)
         xbmc.Player ().play(url, liz, False)         

         AUTO_VIEW('')
            
                

	
#Start Ketboard Function                
def _get_keyboard( default="", heading="", hidden=False ):
	""" shows a keyboard and returns a value """
	keyboard = xbmc.Keyboard( default, heading, hidden )
	keyboard.doModal()
	if ( keyboard.isConfirmed() ):
		return unicode( keyboard.getText(), "utf-8" )
	return default


#Start Search Function
def SEARCH(url):
	searchUrl = url 
	vq = _get_keyboard( heading="Searching  DocuHub" )
	# if blank or the user cancelled the keyboard, return
	if ( not vq ): return False, 0
	# we need to set the title to our query
	title = urllib.quote_plus(vq)
	searchUrl += title 
	print "Searching URL: " + searchUrl 
	INDEX(searchUrl)

	AUTO_VIEW('movies') 
        

                
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param



# addLink for direct play
def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage);liz.setInfo('video',{'Title':name,'Genre':'Live','Studio':name})
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        xbmc.executebuiltin("XBMC.Notification(Please Wait!,Resolving Link,3000)")
        xbmc.sleep(1000)
        xbmc.Player (xbmc.PLAYER_CORE_PAPLAYER).play(url, liz, False)
        return ok

# Standard addDir
def addDir(name,url,mode,iconimage):
        
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        xbmc.executebuiltin("Container.SetViewMode(500)")
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

#Alt addDir
def addDird(name,url,mode,iconimage,labels,favtype):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels=labels )
        if favtype == 'movie':
                contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)'))
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok  
              
params=get_params()
url=None
name=None
mode=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
#May need toremove
#try:
 #       mode=int(params["mode"])
#except:
 #       pass

try:
        mode=urllib.unquote_plus(params["mode"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)


if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()

elif mode=='topdoc':
        print ""+url
        TOPDOC()
        
elif mode=='docnetcat':
        print ""+url
        DOCNETCAT(url)

elif mode=='doclogcat':
        print ""+url
        DOCLOGCAT(url)        
        
elif mode=='docnet':
        print ""+url
        DOCNET()        
       
elif mode=='doclog':
        print ""+url
        DOCLOG()       
               
       
        
       
elif mode=='tdindex':
        print ""+url
        TDINDEX(url)

elif mode=='docstorm':
        print ""+url
        DOCSTORM()        

elif mode=='stormindex':
        print ""+url
        STORMINDEX(url)

elif mode=='stormvidpage':
        print ""+url
        STORMVIDPAGE(url,name)

elif mode=='stormlatest':
        print ""+url
        STORMLATEST(url)

elif mode=='stormcat':
        print ""+url
        STORMCAT(url)        
        

elif mode=='tdvidpage':
        print ""+url
        TDVIDPAGE(url,name)

elif mode=='docnetindex':
        print ""+url
        DOCNETINDEX(url)

elif mode=='doclogvidpage':
        print ""+url
        DOCLOGVIDPAGE(url)        

elif mode=='docnetlatest':
        print ""+url
        DOCNETLATEST(url)

elif mode=='docloglatest':
        print ""+url
        DOCLOGLATEST(url)        

elif mode=='docnetvidpage':
        print ""+url
        DOCNETVIDPAGE(url,name)        

elif mode=='videolinksyt':
        print ""+url
        VIDEOLINKSYT(url,name)

        
elif mode=='resolverSettings':
        print ""+url
        urlresolver.display_settings()        

       
#For Search Function
elif mode==10:
        print ""+url
        SEARCH(url)



xbmcplugin.endOfDirectory(int(sys.argv[1]))


