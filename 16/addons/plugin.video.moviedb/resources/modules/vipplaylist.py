#Custom vipplaylist by Blazetamer Ported from Mash
import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,urlresolver,xbmc,os,xbmcaddon,main,math,cookielib
from resources.modules import main,resolvers
import urlresolver
from addon.common.addon import Addon
from addon.common.net import Net as net
#from addon.common.net import Net
addon_id = 'plugin.video.moviedb'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon('plugin.video.moviedb', sys.argv)
ADDON = xbmcaddon.Addon(id='plugin.video.moviedb')
#net = Net(http_debug=True)
#========================Alternate Param Stuff=======================
mode = addon.queries['mode']
url = addon.queries.get('url', '')
name = addon.queries.get('name', '')
thumb = addon.queries.get('thumb', '')
favtype = addon.queries.get('favtype', '')
mainimg = addon.queries.get('mainimg', '')
gomode = addon.queries.get('gomode', '')
iconimage = addon.queries.get('iconimage', '')
artwork = addon.queries.get('artwork', '')
art = addon.queries.get('art', '')
fanart = addon.queries.get('fanart', '')
#======================== END Alternate Param Stuff=======================
artwork = xbmc.translatePath(os.path.join('http://cliqaddon.com/support/commoncore/tvaddons/moviedb/showgunart/images/', ''))
fanart = xbmc.translatePath(os.path.join('http://cliqaddon.com/support/commoncore/tvaddons/moviedb/showgunart/images/fanart/fanart.jpg', ''))

settings = xbmcaddon.Addon(id='plugin.video.moviedb')

def LogNotify(title,message,times,icon):
        xbmc.executebuiltin("XBMC.Notification("+title+","+message+","+times+","+icon+")")

def OPEN_URL(url):
  req=urllib2.Request(url)
  req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
  response=urllib2.urlopen(req)
  link=response.read()
  response.close()
  return link



def DMODE(murl):
        link=OPEN_URL(murl)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        r=re.findall('<poster>(.+?)</poster>',link)
        if r:
                vip=r[0]
        else:
                vip=''
        f=re.findall('<fanart>(.+?)</fanart>',link)
        if f:
                fanart=f[0]
        else:
                fanart=''
        print 'FANART IS ' +fanart        
        match=re.compile('<notify><new>(.+?)</new><message1>(.+?)</message1><message2>(.+?)</message2><message3>(.+?)</message3><old>(.+?)</old></notify>').findall(link)
        if len(match)>0:
            for new,mes1,mes2,mes3,old in match: continue
            if new != ' ':
                new=vip+new
                onetime=os.path.join(main.datapath,'OneTime')
                notified=os.path.join(onetime,str(new))
                if not os.path.exists(notified):
                    open(notified,'w').write('version="%s",'%new)
                    dialog = xbmcgui.Dialog()
                    ok=dialog.ok('[B] Announcement From '+vip+'![/B]', str(mes1) ,str(mes2),str(mes3))
                if old != ' ':
                    old=vip+old
                    notified=os.path.join(onetime,str(old))
                    if  os.path.exists(notified):
                        os.remove(notified)
            else: print 'No Messages'
        else: print 'Link Down'
        match3=re.compile('<name>([^<]+)</name><link>([^<]+)</link><thumbnail>([^<]+)</thumbnail><mode>([^<]+)</mode>').findall(link)
        for name,url,thumb,mode in match3:
                if re.findall('http',thumb):
                        thumbs=thumb
                else:
                        thumbs=art+'/'+thumb+'.png'
                main.addDir(name,url,mode,thumbs,fanart,'')
        match=re.compile('<name>([^<]+)</name><link>([^<]+)</link><thumbnail>([^<]+)</thumbnail><date>([^<]+)</date>').findall(link)
        for name,url,thumb,date in match:
            main.addDir(name+' [COLOR red] Updated '+date+'[/COLOR]',url,'ndmode',thumb,fanart,'')
        info=re.findall('<info><message>(.+?)</message><thumbnail>(.+?)</thumbnail></info>',link)
        if info:
            for msg,pic in info:
                main.addLink(msg,'',pic)
        popup=re.compile('<popup><name>([^<]+)</name.+?popImage>([^<]+)</popImage.+?thumbnail>([^<]+)</thumbnail.+?sound>([^<]+)</sound></popup>').findall(link)
        for name,image,thumb,sound in popup:
                
                main.addDirpop(name,image,'vpop',thumb,fanart,sound)
      
def NDMODE(mname,murl):
        link=OPEN_URL(murl)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        r=re.findall('<poster>(.+?)</poster>',link)
        if r:
                vip=r[0]
        else:
                vip=''
        f=re.findall('<fanart>(.+?)</fanart>',link)
        if f:
                fanart=f[0]
        else:
                fanart=''
        print 'FANART IS ' +fanart         
        info=re.findall('<info><message>(.+?)</message><thumbnail>(.+?)</thumbnail></info>',link)
        if info:
            for msg,pic in info:
                main.addLink(msg,'',pic)
        popup=re.compile('<popup><name>([^<]+)</name.+?popImage>([^<]+)</popImage.+?thumbnail>([^<]+)</thumbnail></popup>').findall(link)
        for name,image,thumb in popup:
                main.addDirpop(name,image,'vpop',thumb,fanart,'')
        directory=re.compile('<dir><name>([^<]+)</name.+?link>([^<]+)</link.+?thumbnail>([^<]+)</thumbnail></dir>').findall(link)
        for name,url,thumb in directory:
                main.addDir(name,url,'ndmode',thumb,fanart,'')
        match=re.compile('<title>([^<]+)</title.+?link>(.+?)</link.+?thumbnail>([^<]+)</thumbnail>').findall(link)
        #for name,url,thumb in sorted(match):
        for name,url,thumb in match:
            main.addDir(name+' [COLOR blue]'+vip+'[/COLOR]',url,'linkmode',thumb,fanart,'')


def LINKMODE(mname,murl,thumb):
        
        namelist=[]
        urllist=[]
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        if '.f4m'in murl:
                from resources.mobules import F4mProxy
                player=F4mProxy.f4mProxyHelper()
                proxy=None
                use_proxy_for_chunks=False
                player.playF4mLink(murl, mname, proxy, use_proxy_for_chunks,'',thumb)
                
        else:
                if '</regex>'in murl: 
                        murl=main.doRegex(murl)
                match=re.compile('<sublink>(.+?)</sublink>').findall(murl)
                if match:
                        i=1
                        for url in match:
                                name= 'Link '+str(i)
                                namelist.append(name)        
                                urllist.append(url)
                                i=i+1
                        dialog = xbmcgui.Dialog()
                        answer =dialog.select("Choose A Link", namelist)
                        if answer != -1:
                                murl=urllist[int(answer)]
                        else:
                              return
                
                stream_url = murl
                urls = murl
                if 'project-free-upload'in murl:
                        stream_url=resolve_projectfreeupload(murl)
                        xbmc.sleep(1000)
                        LIVERESOLVE(mname,stream_url,'')
                elif 'veehd'in murl:
                        stream_url=resolve_veehd(murl)
                        xbmc.sleep(1000)
                        LIVERESOLVE(mname,stream_url,'')
                else:        
                  hmf = urlresolver.HostedMediaFile(urls)
                  if hmf:
                     host = hmf.get_host()
                     dlurl = urlresolver.resolve(urls)
                     LIVERESOLVE(mname,dlurl,'')
  
                  else:
                     xbmc.sleep(1000)
                     LIVERESOLVE(mname,murl,'')
                  
                  
     



def LIVERESOLVE(name,url,thumb):
         params = {'url':url, 'name':name, 'thumb':thumb}
         addon.add_video_item(params, {'title':name}, img=thumb)
         liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumb)
         xbmc.Player ().play(str(url), liz, False)
         return
         

def addDir(name,url,mode,thumb,desc,favtype, isFolder=True, isPlayable=False):
        gomode=mode
        contextMenuItems = []
        params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb, 'desc':desc}
        fanart = fanart
        
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&thumb="+urllib.quote_plus(thumb)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumb)
        liz.setInfo( type="Video", infoLabels={ "title": name, "Plot": desc } )
        liz.setProperty( "Fanart_Image", fanart )
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        if isPlayable:
            liz.setProperty("IsPlayable","true")
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isFolder)
        return ok
      

   
#===============Resolver Area=================
def resolve_projectfreeupload(url):
    try:
        import jsunpack
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving Phoenix Project Free Link...')       
        dialog.update(0)
        print 'PhoenixStreams Project Free - Requesting GET URL: %s' % url
        html = net().http_GET(url).content
        r = re.findall(r'\"hidden\"\sname=\"?(.+?)\"\svalue=\"?(.+?)\"\>', html, re.I)
        post_data = {}
        for name, value in r:
            post_data[name] = value
        post_data['referer'] = url
        post_data['method_premium']=''
        post_data['method_free']=''
        html = net().http_POST(url, post_data).content
        embed=re.findall('<IFRAME SRC="(.+?)"',html)
        html = net().http_GET(embed[0]).content
        r = re.findall(r'(eval\(function\(p,a,c,k,e,d\)\{while.+?)</script>',html,re.M|re.DOTALL)
        try:unpack=jsunpack.unpack(r[1])
        except:unpack=jsunpack.unpack(r[0])
        stream_url=re.findall('<param name="src"value="(.+?)"/>',unpack)[0]
        return stream_url
        if dialog.iscanceled(): return None
    except Exception:
        xbmc.executebuiltin("XBMC.Notification(Resolver Failed,Project Free,2000)")

        
def resolve_veehd(url):     
    try:
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving Phoenix VeeHD Link...')       
        dialog.update(0)
        if dialog.iscanceled(): return False
        dialog.update(33)
        headers = {}
        headers = {'User-Agent': 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7','Referer':url}
        print 'Phoenix VeeHD - Requesting GET URL: %s' % url
        setCookie('http://veehd.com')
        html = net().http_GET(url, headers).content
        if dialog.iscanceled(): return False
        dialog.update(66)
        fragment = re.findall('playeriframe".+?attr.+?src : "(.+?)"', html)
        for frags in fragment:
            pass
        frag = 'http://%s%s'%('veehd.com',frags)
        setCookie('http://veehd.com')
        html = net().http_GET(frag, headers).content
        va=re.search('iframe" src="([^"]+?)"',html)
        if va:
            poop='http://veehd.com'+va.group(1)
            headers = {'User-Agent': 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7','Referer':frag,'Cache-Control':'max-age=0'}
            setCookie(poop)
            html = net().http_GET(frag, headers).content
        r = re.search('"video/divx" src="(.+?)"', html)
        if r:
            stream_url = r.group(1)
        if not r:
            a = re.search('"url":"(.+?)"', html)
            if a:
                r=urllib.unquote(a.group(1))
                if r:
                    stream_url = r
                else:
                    xbmc.executebuiltin("XBMC.Notification(File Not Found,VeeHD,2000)")
                    return False
            if not a:
                a = re.findall('href="(.+?)">', html)
                stream_url = a[1]
        if dialog.iscanceled(): return False
        dialog.update(100)
        return stream_url
    except Exception:
        xbmc.executebuiltin("XBMC.Notification(Resolver Failed,VeeHD,2000)")
               
