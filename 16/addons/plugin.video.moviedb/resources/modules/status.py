# Status/Help Module By: Blazetamer 2013
import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,os,sys,time,shutil,main
import urlresolver
import downloader
import extract


try:
        from addon.common.addon import Addon

except:
        from t0mm0.common.addon import Addon
addon_id = 'plugin.video.moviedb'
ADDON = xbmcaddon.Addon(id='plugin.video.moviedb')
#addon = Addon(addon_id, sys.argv)
addon = main.addon

try:
        from addon.common.net import Net

except:  
        from t0mm0.common.net import Net
net = Net()


settings=xbmcaddon.Addon(id='plugin.video.moviedb')
#==============ADD Addon Instaler========================
base_url = 'http://addons.xbmchub.com/'
if settings.getSetting('theme') == '0':
    artwork = xbmc.translatePath(os.path.join('http://cliqaddon.com/support/commoncore/tvaddons/moviedb/showgunart/images/', ''))
else:
    artwork = xbmc.translatePath(os.path.join('http://cliqaddon.com/support/commoncore/tvaddons/moviedb/images/', ''))

def ADDONLIST(url):
    fanart = ''
    link=OPEN_URL(url)
    match=re.compile('<li><a href="(.+?)"><span class="thumbnail"><img src="(.+?)" width="100%" alt="(.+?)"').findall(link)
    for url,image,name in match:
        iconimage = base_url + image
        ADDONINDEX(name,url,'')
        

def ADDONINDEX(name,url,filetype):
    fanart = 'http://cliqaddon.com/support/commoncore/tvaddons/Blazetamer/Repo/fanart.jpg'
    link=OPEN_URL(url)
    #match=re.compile('<img src="(.+?)" alt=".+?" class="pic" /></span>\r\n\t\t\t\t<h2>(.+?)</h2>\r\n\t\t\t\t<strong>Author:</strong> <a href=".+?">.+?</a><br /><strong>Version:</strong> .+?<br /><strong>Released:</strong> .+?<br /><strong>Repository:</strong> <a href="(.+?)" rel="nofollow">.+?</a><div class="description"><h4>Description:</h4><p> (.+?)</p></div><ul class="addonLinks"><li><strong>Forum Discussion:</strong><br /><a href=".+?" target="_blank"><img src="images/forum.png" alt="Forum discussion" /></a></li><li><strong>Source Code:</strong><br /><img src="images/codebw.png" alt="Source code" /></li><li><strong>Website:</strong><br /><a href=".+?" target="_blank"><img src="images/website.png" alt="Website" /></a></li><li><strong>Direct Download:</strong><br /><a href="(.+?)" rel="nofollow">').findall(link)
    description = 'Description not available at this time'
    match2=re.compile('<img src="(.+?)" alt=".+?" class="pic" /></span>').findall(link)
    for image in match2:
        match3=re.compile('class="pic" /></span>\r\n\t\t\t\t<h2>(.+?)</h2>').findall(link)
        for name in match3:
            match4=re.compile('Repository:</strong> <a href="(.+?)"').findall(link)
            for repourl in match4:
                match5=re.compile('Description:</h4><p>(.+?)</p>').findall(link)
                for description in match5:
                    match6=re.compile('Direct Download:</strong><br /><a href="(.+?)"').findall(link)
                    for addonurl in match6:
                        iconimage = base_url + image
                        print 'Image  is ' + iconimage
                        print 'Name is ' + name
                        print 'REPOurl is ' + repourl
                        print 'Description is ' + description
                        print 'ADDONurl is ' + addonurl
                        addADDONDir('Install '+name,addonurl,'addoninstall',iconimage,fanart,description,'addon',repourl)
                        #addADDONDir('Install '+name,addonurl,'addoninstall',iconimage,fanart,description,'addon',repourl)
                        #ADDONINSTALL(name,addonurl,description,'addon',repourl)
                        main.AUTO_VIEW('movies')


def addADDONDir(name,url,mode,iconimage,fanart,description,filetype,repourl):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)+"&filetype="+urllib.quote_plus(filetype)+"&repourl="+urllib.quote_plus(repourl)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok

#===============END Addon Installer======================================    

def STATUSCATEGORIES(url):
          link=OPEN_URL(url).replace('\n','').replace('\r','')
          match=re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)".+?ype="(.+?)"').findall(link)
          for name,url,iconimage,fanart,description,filetype in match:
                  #main.add2HELPDir(name,'http://addons.xbmchub.com/search/?keyword=Blazetamer','addonlist',iconimage,fanart,description,filetype)
              if 'status' in filetype:
                 main.addHELPDir(name,url,'addonstatus',iconimage,fanart,description,filetype)
              elif 'getshorts' in filetype:
                 main.add2HELPDir(name,url,'getshorts',iconimage,fanart,description,filetype) 
              elif 'main' in filetype:
                    main.addHELPDir(name,url,'addoninstall',iconimage,fanart,description,filetype)
              elif 'addrepo' in filetype:
                    main.add2HELPDir(name,url,'getrepolink',iconimage,fanart,description,filetype)
              elif 'source' in filetype:
                    main.addHELPDir(name,url,'addsource',iconimage,fanart,description,filetype)
              elif 'getvideo' in filetype:
                    main.add2HELPDir(name,url,'getvideolink',iconimage,fanart,description,filetype)
                    #Add your addon url line here========================
              elif 'blazeaddons' in filetype:
                    main.add2HELPDir(name,url,'addonlist',iconimage,fanart,description,filetype)
                    #end Add your addon url line here========================
                    main.AUTO_VIEW('movies')

def OPEN_URL(url):
  req=urllib2.Request(url)
  req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
  response=urllib2.urlopen(req)
  link=response.read()
  response.close()
  return link

def ADDONINSTALL(name,url,description,filetype,repourl):
  path=xbmc.translatePath(os.path.join('special://home/addons','packages'))
  confirm=xbmcgui.Dialog().yesno("Please Confirm","                Do you wish to install the chosen add-on and","                        its respective repository if needed?              ","                    ","Cancel","Install")
  
  if confirm: 
        dp=xbmcgui.DialogProgress()
        dp.create("Download Progress:","Downloading your selection ",'','Please Wait')
        lib=os.path.join(path,name+'.zip')
        try: os.remove(lib)
        except: pass
        downloader.download(url, lib, dp)
        if filetype == 'addon':
            addonfolder = xbmc.translatePath(os.path.join('special://','home/addons'))
        elif filetype == 'media':
             addonfolder = xbmc.translatePath(os.path.join('special://','home'))    
        elif filetype == 'main':
             addonfolder = xbmc.translatePath(os.path.join('special://','home'))
        time.sleep(2)
        #dp.update(0,"","Installing selections.....")
        print '======================================='
        print addonfolder
        print '======================================='
        extract.all(lib,addonfolder,dp)
        #dialog=xbmcgui.Dialog()
        #dialog.ok("Success!","Please Reboot To Take Effect","    Brought To You By XBMCHUB.COM ")
#start repo dl
        if  'none' not in repourl:
            path=xbmc.translatePath(os.path.join('special://home/addons','packages'))
  
   
            dp=xbmcgui.DialogProgress()
            dp.create("Updating Repo if needed:","Configuring Installation ",'',' ')
            lib=os.path.join(path,name+'.zip')
            try: os.remove(lib)
            except: pass
            downloader.download(repourl, lib, '')
            if filetype == 'addon':
                addonfolder = xbmc.translatePath(os.path.join('special://','home/addons'))
            elif filetype == 'media':
                 addonfolder = xbmc.translatePath(os.path.join('special://','home'))    
            elif filetype == 'main':
                 addonfolder = xbmc.translatePath(os.path.join('special://','home'))
            time.sleep(2)
            #dp.update(0,"","Checking Installation......")
            print '======================================='
            print addonfolder
            print '======================================='
            extract.all(lib,addonfolder,dp)
            #dialog=xbmcgui.Dialog()
            #dialog.ok("Success!","                              Please Reboot To Take Effect","                            Brought To You By Blazetamer!! ")
        else:
             pass
        INSTALLPOP()
        #REBOOTCHECK()
        '''reboot=xbmcgui.Dialog().yesno("Instalation complete!","                   Please restart XBMC for changes to take effect.","                   Brought To You By Blazetamer ","","Later","Reboot Now")
        if reboot:
                main.addDir("[COLOR gold]Browse Blazetamer's Addons[/COLOR]",'http://addons.xbmchub.com/author/Blazetamer/','addonlist','http://cliqaddon.com/support/commoncore/tvaddons/Blazetamer/Repo/icon.png','','')
                main.AUTO_VIEW('')'''
                
                
        
                
                
  #backtoroutine      
  else:
      return

def REBOOTCHECK():
        dialog = xbmcgui.Dialog()
        reboot = dialog.select('Reboot Options', ['Reboot Now', 'Reboot Later', 'Dont Care'])
        reboot1 = str(reboot)
        print 'REBOOT RETURN IS ' +reboot1
        if '0' in reboot1:
                print 'REBOOT RETURN 2 IS' +reboot1        
                main.addDir('[COLOR gold]Announcements/Info[/COLOR]','http://cliqaddon.com/support/commoncore/tvaddons/moviedb/messages/addonannouncements.txt','addonstatus',artwork +'announcements.jpg','','')
                main.addDir("[COLOR gold]Browse Blazetamer's Addons[/COLOR]",'http://addons.xbmchub.com/author/Blazetamer/','addonlist','http://cliqaddon.com/support/commoncore/tvaddons/Blazetamer/Repo/icon.png','','')
                main.AUTO_VIEW('')
        


def ADDSHORTCUTS(name,url,description,filetype):
   confirm=xbmcgui.Dialog()
   if confirm.yesno("Shortcut Creation!!","                By Clicking 'YES' you agree to allow this Addon","                 Access to add Shortcuts to your pages.              ","                    "):

    link=OPEN_URL(url)
    proname=xbmc.getInfoLabel("System.ProfileName")
    shorts=re.compile('shortcut="(.+?)"').findall(link)
    for shortname in shorts: xbmc.executebuiltin("Skin.SetString(%s)" % shortname)
    time.sleep(2)
    xbmc.executebuiltin('UnloadSkin()')
    xbmc.executebuiltin('ReloadSkin()')
    xbmc.executebuiltin("LoadProfile(%s)" % proname)
    dialog=xbmcgui.Dialog()
    dialog.ok("Success!","Please Reboot To Take","Effect    Brought To You By BLAZETAMER ")

def ADDSOURCE(name,url,description,filetype):
   confirm=xbmcgui.Dialog()
   if confirm.yesno("Source Creation!!","                By Clicking 'YES' you agree to allow this Addon","                 Access to add Sources to your settings.              ","                    "):
       link=OPEN_URL(url)
       source=re.compile("source='(.+?)'").findall(link)
       for sourcename in source:
        newfile=re.compile("addfile='(.+?)'").findall(link)    
        for addfile in newfile:     
         newsource = os . path . join ( xbmc . translatePath ( 'special://home' ) , 'userdata' , 'sources.xml' )
         if not os . path . exists ( newsource ) :
          src = open ( newsource , mode = 'w' )
          src . write ( addfile )
          src . close ( )
          dialog=xbmcgui.Dialog()
          dialog.ok("Success!","Please Reboot To Take","Effect    Brought To You By BLAZETAMER ")
          return
       src = open ( newsource , mode = 'r' )
       str = src . read ( )
       src . close ( )
       #if not 'http://fusion.xbmchub.com' in str:
        #if '</files>' in str :
       str = str . replace ( '</files>' , sourcename )
       src = open ( newsource , mode = 'w' )
       src . write ( str )
       src . close ( )
    
       dialog=xbmcgui.Dialog()
       dialog.ok("Success!","Please Reboot To Take","Effect    Brought To You By BLAZETAMER ")

def ADDONSTATUS(url):
  link=OPEN_URL(url).replace('\n','').replace('\r','')
  match=re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)".+?ype="(.+?)"').findall(link)
  for name,url,iconimage,fanart,description,filetype in match:
    header="[B][COLOR gold]"+name+"[/B][/COLOR]"
    msg=(description)
    TextBoxes(header,msg)

def TextBoxes(heading,anounce):
  class TextBox():
    WINDOW=10147
    CONTROL_LABEL=1
    CONTROL_TEXTBOX=5
    def __init__(self,*args,**kwargs):
      xbmc.executebuiltin("ActivateWindow(%d)" % (self.WINDOW, )) # activate the text viewer window
      self.win=xbmcgui.Window(self.WINDOW) # get window
      xbmc.sleep(500) # give window time to initialize
      self.setControls()
    def setControls(self):
      self.win.getControl(self.CONTROL_LABEL).setLabel(heading) # set heading
      try: f=open(anounce); text=f.read()
      except: text=anounce
      self.win.getControl(self.CONTROL_TEXTBOX).setText(str(text))
      return
  TextBox()


def VIDEORESOLVE(name,url,iconimage):
         url= url
         ok=True
         liz=xbmcgui.ListItem(name, iconImage=iconimage,thumbnailImage=iconimage); liz.setInfo( type="Video", infoLabels={ "Title": name } )
         ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=str(url),listitem=liz)
         xbmc.executebuiltin("XBMC.Notification(Please Wait!,Preparing Your Video,3000)")
         xbmc.sleep(1000)
         xbmc.Player ().play(str(url), liz, False)

         

def YTVIDEORESOLVE(name,url,iconimage):
         url = urlresolver.HostedMediaFile(url=url).resolve()
         ok=True
         liz=xbmcgui.ListItem(name, iconImage=iconimage,thumbnailImage=iconimage); liz.setInfo( type="Video", infoLabels={ "Title": name } )
         ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=str(url),listitem=liz)
         xbmc.executebuiltin("XBMC.Notification(Please Wait!,Preparing Your Video,3000)")
         xbmc.sleep(1000)
         xbmc.Player ().play(str(url), liz, False)


        
def GETVIDEOLINK(url):
    link=OPEN_URL(url).replace('\n','').replace('\r','')
    match=re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)".+?ype="(.+?)"').findall(link)
    for name,url,iconimage,fanart,description,filetype in match:
        if 'video' in filetype:
            main.addHELPDir(name,url,'getvideo',iconimage,fanart,description,filetype)
        elif 'youtube' in filetype:
           main.addHELPDir(name,url,'getvideo',iconimage,fanart,description,filetype)
        elif 'stream' in filetype:
           main.addHELPDir(name,url,'getvideo',iconimage,fanart,description,filetype)   
    

    main.AUTO_VIEW('movies')


def GETVIDEO(name,url,iconimage,description,filetype):
    if 'video' in filetype:
            VIDEORESOLVE(name,url,iconimage)
    elif 'youtube' in filetype:
            YTVIDEORESOLVE(name,url,iconimage)
    elif 'stream' in filetype:
            PLAYSTREAM(name,url,iconimage,description)        
            
         

def GETREPOLINK(url):
    link=OPEN_URL(url).replace('\n','').replace('\r','')
    match=re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)".+?ype="(.+?)"').findall(link)
    for name,url,iconimage,fanart,description,filetype in match:
        main.addHELPDir(name,url,'addoninstall',iconimage,fanart,description,filetype)
                  
        main.AUTO_VIEW('movies')

def GETSHORTS(url):
    link=OPEN_URL(url).replace('\n','').replace('\r','')
    match=re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)".+?ype="(.+?)"').findall(link)
    for name,url,iconimage,fanart,description,filetype in match:
        main.addHELPDir(name,url,'addshortcuts',iconimage,fanart,description,filetype)
                  
        main.AUTO_VIEW('movies')        



def PLAYSTREAM(name,url,iconimage,description):
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name} )
    liz.setProperty("IsPlayable","true")
    pl = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    pl.clear()
    pl.add(url, liz)
    xbmc.Player(xbmc.PLAYER_CORE_MPLAYER).play(pl)


#==============POP UP FUNCTION==================
def INSTALLPOP():# Added Close_time for window auto-close length.....
    
    if xbmc.getCondVisibility('system.platform.ios'):
        if not xbmc.getCondVisibility('system.platform.atv'):
            popup = INSTCONFIRM('instconfirm1.xml',ADDON.getAddonInfo('path'),'DefaultSkin',close_time=60,logo_path='%s/resources/skins/DefaultSkin/media/Logo/'%ADDON.getAddonInfo('path'))
    elif xbmc.getCondVisibility('system.platform.android'):
        popup = INSTCONFIRM('instconfirm1.xml',ADDON.getAddonInfo('path'),'DefaultSkin',close_time=60,logo_path='%s/resources/skins/DefaultSkin/media/Logo/'%ADDON.getAddonInfo('path'))
    else:
        popup = INSTCONFIRM('instconfirm.xml',ADDON.getAddonInfo('path'),'DefaultSkin',close_time=60,logo_path='%s/resources/skins/DefaultSkin/media/Logo/'%ADDON.getAddonInfo('path'))

    
    popup.doModal()
    del popup
    
class INSTCONFIRM( xbmcgui.WindowXMLDialog ): # The call MUST be below the xbmcplugin.endOfDirectory(int(sys.argv[1])) or the dialog box will be visible over the pop-up.
    def __init__( self, *args, **kwargs ):
        self.shut = kwargs['close_time'] 
        xbmc.executebuiltin( "Skin.Reset(AnimeWindowXMLDialogClose)" )
        xbmc.executebuiltin( "Skin.SetBool(AnimeWindowXMLDialogClose)" )
                                       
    def onInit( self ):
        #xbmc.Player().play('%s/resources/skins/DefaultSkin/media/xbmchub.mp3'%ADDON.getAddonInfo('path'))# Music.
        '''xbmc.Player().play(''%ADDON.getAddonInfo('path'))# Music.
        while self.shut > 0:
            xbmc.sleep(1000)
            self.shut -= 1
        xbmc.Player().stop()
        self._close_dialog()'''
                
    def onFocus( self, controlID ): pass
    
    def onClick( self, controlID ): 
        if controlID == 12:
            xbmc.Player().stop()
            self._close_dialog()

    def onAction( self, action ):
        if action in [ 5, 6, 7, 9, 10, 92, 117 ] or action.getButtonCode() in [ 275, 257, 261 ]:
            xbmc.Player().stop()
            self._close_dialog()

    def _close_dialog( self ):
        xbmc.executebuiltin( "Skin.Reset(AnimeWindowXMLDialogClose)" )
        time.sleep( .4 )
        self.close()    
#==============END POP UP FUNCTION===============
