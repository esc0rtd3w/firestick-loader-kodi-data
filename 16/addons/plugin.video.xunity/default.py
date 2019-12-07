import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os
import extract
import downloader


ADDON = xbmcaddon.Addon(id='plugin.video.xunity')
base_url='http://xunitytalk.me/xfinity/Skins/'
icon = 'http://xtyrepo.me/xunitytalk/addons/plugin.video.xunity/icon.png'
ifan = 'http://xtyrepo.me/xunitytalk/addons/plugin.video.xunity/fanart.jpg'

xbmcfolder = xbmc.translatePath(os.path.join('special://home',''))
splashimage = xbmc.translatePath(os.path.join('special://home/media','Splash.png'))

addonfolder = xbmc.translatePath(os.path.join('special://home','addons'))
xunitytalk=os.path.join(addonfolder,'repository.xunitytalk')

ISTREAM_PATH=os.path.join(addonfolder,'repository.istream')
packages = xbmc.translatePath(os.path.join('special://home/addons','packages'))
icechannel = xbmc.translatePath(os.path.join('special://home/addons','script.icechannel'))

icechannelzip='http://xunitytalk.me/xfinity/Modules/script.icechannel.zip'

ISTREAMREPO='http://xtyrepo.me/xunitytalk/addons/repository.istream/repository.istream-10.2.zip'

XUNITYTALK='http://xunitytalk.me/xfinity/XunityTalk_Repository.zip'



def CATEGORIES():
        addDir('[COLOR blue]R[/COLOR]emove [COLOR blue]S[/COLOR]plash [COLOR blue]I[/COLOR]mage','url',3,icon,ifan,'','')
        addDir('F[COLOR blue]i[/COLOR]x My [COLOR blue]i[/COLOR]Stream','url',2,icon,ifan,'','')
        addDir('[B][COLOR blue]i[/COLOR]Stream Without Skin Helix/Krypton Compatible Too[/B]','url',4,icon,ifan,'','')
        link=OPEN_URL(base_url+'skins.txt')
        match=re.compile('name="(.+?)".+?skins="(.+?)".+?desc="(.+?)"',re.DOTALL).findall (link)
        for name ,zip_url ,description in match:
        
            url_dest    =   'http://xunitytalk.me/xfinity/Skins/'+'%s/%s' %(name,zip_url)
            iconimage   =   'http://xunitytalk.me/xfinity/Skins/'+'%s/icon.png' %name
            fanart      =   'http://xunitytalk.me/xfinity/Skins/'+'%s/fanart.png' %name
            
            addDir(name,url_dest,1,iconimage,fanart,description,'')
            
        setView('movies', 'everything') 
       
def changekeys(skin):
    
    left='<onleft>%s</onleft>'
    right='<onright>%s</onright>'
    up='<onup>%s</onup>'
    down='<ondown>%s</ondown>'
    button='<control type="button" id="%s">'    
    LETTER=[('65','140'),('66','164'),('67','162'),('68','142'),('69','122'),('70','143'),('71','144'),('72','145'),('73','127'),('74','146'),('75','147'),('76','148'),('77','166'),('78','165'),('79','128'),('80','129'),('81','120'),('82','123'),('83','141'),('84','124'),('85','126'),('86','163'),('87','121'),('88','161'),('89','125'),('90','160')]
        
    for old , new in LETTER:

        a=open(skin).read()  
        CHANGE=a.replace(button%old,button%new).replace(left%old,left%new).replace(right%old,right%new).replace(up%old,up%new).replace(down%old,down%new)
        f = open(skin, mode='w')
        f.write(CHANGE)
        f.close()   
    
def changekeyboard(skin):
    dialog=xbmcgui.Dialog()
    

    path = xbmc.translatePath(os.path.join('special://home/addons', skin))
    
    for root, dirs, files in os.walk(path):
       for f in files:
            if 'DialogKeyboard.xml' in f:
                skin= os.path.join(root, f)
                a=open(skin).read()
                CHANGE=a.replace('<control type="label" id="310"','<control type="edit" id="312"')
                f = open(skin, mode='w')
                f.write(CHANGE)
                f.close()     
                changekeys(skin)
                for i in range(48, 58):
                    changenumber(i,skin)
                   
def setSetting(setting, value):
    setting = '"%s"' % setting

    if isinstance(value, list):
        text = ''
        for item in value:
            text += '"%s",' % str(item)

        text  = text[:-1]
        text  = '[%s]' % text
        value = text

    elif not isinstance(value, int):
        value = '"%s"' % value

    query = '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue","params":{"setting":%s,"value":%s}, "id":1}' % (setting, value)
    xbmc.executeJSONRPC(query)

def getSetting(setting):
  
        import json
        setting = '"%s"' % setting
 
        query = '{"jsonrpc":"2.0", "method":"Settings.GetSettingValue","params":{"setting":%s}, "id":1}' % (setting)
        response = xbmc.executeJSONRPC(query)

        response = json.loads(response)                

        if response.has_key('result'):
            if response['result'].has_key('value'):
                return response ['result']['value']



def EXIT():
        xbmc.executebuiltin("XBMC.Container.Update(path,replace)")
        xbmc.executebuiltin("XBMC.ActivateWindow(Home)")

        
def MakeiStreamKrypton():
        xbmc_version =  re.search('^(\d+)', xbmc.getInfoLabel( "System.BuildVersion" ))
        if xbmc_version:
            xbmc_version = int(xbmc_version.group(1))
        else:
            xbmc_version = 1

        if xbmc_version >= 16.9:
                dependencies = ['repository.istream','repository.xunitytalk','script.module.requests','script.module.elementtree','script.icechannel.theme.xunity','script.icechannel.theme.xunityhd','script.icechannel.extn.xunitytalk','script.common.plugin.cache', 'script.icechannel.extn.common', 'script.icechannel.extn.xunity.tv.common', 'script.istream.dialogs', 'script.module.addon.common', 'script.module.beautifulsoup', 'script.module.dnspython', 'script.module.f4mproxy', 'script.module.feedparser', 'script.module.metahandler', 'script.module.myconnpy', 'script.module.parsedom', 'script.module.pyamf', 'script.module.simple.downloader', 'script.module.socksipy', 'script.module.t0mm0.common', 'script.module.unidecode', 'script.module.universal', 'script.module.urlresolver']            
                import glob


                folder = xbmc.translatePath('special://home/addons/')

                for DEPEND in glob.glob(folder+'script.icechannel*'):
                    try:dependencies.append(DEPEND.rsplit('\\', 1)[1])
                    except:dependencies.append(DEPEND.rsplit('/', 1)[1])


                for THEPLUGIN in dependencies:
                    xbmc.log(str(THEPLUGIN))
                    query = '{"jsonrpc":"2.0", "method":"Addons.SetAddonEnabled","params":{"addonid":"%s","enabled":true}, "id":1}' % (THEPLUGIN)
                 
                    xbmc.executeJSONRPC(query)
            
                xbmc.executebuiltin('UpdateLocalAddons') 
                xbmc.executebuiltin("UpdateAddonRepos")
                dialog = xbmcgui.Dialog()
                dialog.ok("[COLOR blue]i[/COLOR]Stream", "", "Please Wait Until All Updates Have Finsihed", "Then Restart Kodi To Take Effect")
                EXIT()
             
                                                                      
def Install(name,url,common):
        profile = xbmc.getInfoLabel("System.ProfileName" )
        dp = xbmcgui.DialogProgress()
        dp.create("[COLOR blue]i[/COLOR]Stream","Downloading ",name, 'Please Wait')
        lib=os.path.join(packages,name+'.zip')
        commonzip=os.path.join(packages,common)
        splash=os.path.join(packages,'splash.zip')
        try:
           os.remove(lib)
        except:
           pass
        downloader.download(url, lib, dp)#download skin
        dp.update(0,name, "Extracting Zip Please Wait")
        extract.all(lib,addonfolder,dp)#extract skin
        import zipfile
        z = zipfile.ZipFile(lib, "r")
        for filename in z.namelist():
            if 'addon.xml' in filename:
                a = z.read(filename)
                SKIN =re.compile('id="(.+?)"').findall(a)[0]
                continue        
        Dependencies()
        
        if os.path.exists(icechannel)==True:
            GetFile(packages,'script.icechanne*')
            GetFile(addonfolder,'script.icechannel')
            
        downloader.download(icechannelzip, os.path.join(packages,'script.icechannel.zip'), dp)
        dp.update(0,name, "Extracting Zip Please Wait")
        extract.all(os.path.join(packages,'script.icechannel.zip'),addonfolder,dp)
        
        if os.path.exists(xunitytalk)==False:
            downloader.download(XUNITYTALK, os.path.join(packages,'XunityTalk_Repository.zip'), dp)
            dp.update(0,name, "Extracting Zip Please Wait")
            extract.all(os.path.join(packages,'XunityTalk_Repository.zip'),addonfolder,dp)
            
        if os.path.exists(ISTREAM_PATH)==False:
            downloader.download(ISTREAMREPO, os.path.join(packages,'iStream_Repository.zip'), dp)
            dp.update(0,name, "Extracting Zip Please Wait")
            extract.all(os.path.join(packages,'iStream_Repository.zip'),addonfolder,dp)            
            
        if os.path.exists(splashimage)==False:
            dp.update(0,"", "Downloading") #download splash 
            downloader.download(base_url+'splash.zip', splash, dp)        
            dp.update(0,"", "Extracting Zip Please Wait")
            extract.all(splash,xbmcfolder,dp)#extract splash
            
        xbmc_version =  re.search('^(\d+)', xbmc.getInfoLabel( "System.BuildVersion" ))
        if xbmc_version:
            xbmc_version = int(xbmc_version.group(1))
        else:
            xbmc_version = 1
        if xbmc_version >= 13.9:          
            changekeyboard(name)
            
        xbmc.executebuiltin('UpdateLocalAddons') 
        xbmc.executebuiltin("UpdateAddonRepos")
        dialog = xbmcgui.Dialog()
        #if dialog.yesno("[COLOR blue]i[/COLOR]Stream", "Would You Like To Change Skin Now", ""):
            #skin    = getSetting(setting)
        setSetting('lookandfeel.skin', SKIN)
            #import time
            #profile = xbmc.getInfoLabel("System.ProfileName" )
            #time.sleep(5)
            #xbmc.executebuiltin("LoadProfile(%s)"%profile)
        import time
        time.sleep(2)
        MakeiStreamKrypton()

                                                                      
def InstallWithout(name,url,common):
        profile = xbmc.getInfoLabel("System.ProfileName" )
        dp = xbmcgui.DialogProgress()
        dp.create("[COLOR blue]i[/COLOR]Stream","Downloading ",name, 'Please Wait')

        
        Dependencies()
        
        if os.path.exists(icechannel)==True:
            GetFile(packages,'script.icechanne*')
            GetFile(addonfolder,'script.icechannel')
            
        downloader.download(icechannelzip, os.path.join(packages,'script.icechannel.zip'), dp)
        dp.update(0,name, "Extracting Zip Please Wait")
        extract.all(os.path.join(packages,'script.icechannel.zip'),addonfolder,dp)
        
        if os.path.exists(xunitytalk)==False:
            downloader.download(XUNITYTALK, os.path.join(packages,'XunityTalk_Repository.zip'), dp)
            dp.update(0,name, "Extracting Zip Please Wait")
            extract.all(os.path.join(packages,'XunityTalk_Repository.zip'),addonfolder,dp)
            
        if os.path.exists(ISTREAM_PATH)==False:
            downloader.download(ISTREAMREPO, os.path.join(packages,'iStream_Repository.zip'), dp)
            dp.update(0,name, "Extracting Zip Please Wait")
            extract.all(os.path.join(packages,'iStream_Repository.zip'),addonfolder,dp)            
            
            
        xbmc.executebuiltin('UpdateLocalAddons') 
        xbmc.executebuiltin("UpdateAddonRepos")
        import time
        time.sleep(2)
        MakeiStreamKrypton()
            
def Dependencies():
    xbmc_version =  re.search('^(\d+)', xbmc.getInfoLabel( "System.BuildVersion" ))
    if xbmc_version:
        xbmc_version = int(xbmc_version.group(1))
    else:
        xbmc_version = 1
    if xbmc_version >= 14:    
        dependencies = ['script.module.requests','script.module.elementtree','script.icechannel.theme.xunity','script.icechannel.theme.xunityhd','script.icechannel.extn.xunitytalk','script.common.plugin.cache', 'script.icechannel.extn.common', 'script.icechannel.extn.xunity.tv.common', 'script.istream.dialogs', 'script.module.addon.common', 'script.module.beautifulsoup', 'script.module.dnspython', 'script.module.f4mproxy', 'script.module.feedparser', 'script.module.metahandler', 'script.module.myconnpy', 'script.module.parsedom', 'script.module.pyamf', 'script.module.simple.downloader', 'script.module.socksipy', 'script.module.t0mm0.common', 'script.module.unidecode', 'script.module.universal_helix', 'script.module.urlresolver']
    else:
        dependencies = ['script.module.requests','script.module.elementtree','script.icechannel.theme.xunity','script.icechannel.theme.xunityhd','script.icechannel.extn.xunitytalk','script.common.plugin.cache', 'script.icechannel.extn.common', 'script.icechannel.extn.xunity.tv.common', 'script.istream.dialogs', 'script.module.addon.common', 'script.module.beautifulsoup', 'script.module.dnspython', 'script.module.f4mproxy', 'script.module.feedparser', 'script.module.metahandler', 'script.module.myconnpy', 'script.module.parsedom', 'script.module.pyamf', 'script.module.simple.downloader', 'script.module.socksipy', 'script.module.t0mm0.common', 'script.module.unidecode', 'script.module.universal', 'script.module.urlresolver']            

    for scripts in dependencies:
        
        addon=xbmc.translatePath(os.path.join('special://home/addons',scripts))
        if os.path.exists(addon)==False:
            dp = xbmcgui.DialogProgress()
            dp.create("[COLOR blue]i[/COLOR]Stream","Downloading ",scripts, 'Please Wait')
            lib=os.path.join(packages,scripts+'.zip')
            downloader.download('http://xunitytalk.me/xfinity/Modules/%s.zip'%scripts, lib, dp)
            dp.update(0,name, "Extracting Zip Please Wait")
            extract.all(os.path.join(lib),addonfolder,dp)
            
                    
def iStreamFix():
        dialog = xbmcgui.Dialog()
        
        GetFile(packages,'script.icechanne*')
        GetFile(addonfolder,'script.icechannel')
        
        dialog = xbmcgui.Dialog()
        dialog.ok("[COLOR blue]i[/COLOR]Stream", "", "Please Reboot For [B][COLOR blue]i[/COLOR]Stream[/B] [B]F[COLOR blue]i[/COLOR]x[/B] To Take Effect", "")
        
def GetFile(directory,name):
     import glob
     both=xbmc.translatePath(os.path.join(directory, name))
     for infile in glob.glob(both):
         removefolder(infile)
         try:
             os.remove(infile)
         except:
             pass
        
def removefolder(name):   
    
    if os.path.exists(str(name))==True: 
        for root, dirs, files in os.walk(name):
            for f in files:
                try:
                    os.unlink(os.path.join(root, f))
                except:
                    pass
    if os.path.exists(str(name))==True: 
        for root, dirs, files in os.walk(name):
            for d in dirs:
                try:
                    os.rmdir(os.path.join(root, d))
                except:
                    pass
    try:
        os.rmdir(name)
    except:
        pass



    


            
def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
    
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
        
        

def addDir(name,url,mode,iconimage,fanart,description,common):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)+"&common="+urllib.quote_plus(common)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description} )
        liz.setProperty("Fanart_Image", fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok
        
        
        
 
        
#below tells plugin about the views                
def setView(content, viewType):
        # set content type so library shows more views and info
        if content:
                xbmcplugin.setContent(int(sys.argv[1]), content)
        if ADDON.getSetting('auto-view') == 'true':#<<<----see here if auto-view is enabled(true) 
                xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting(viewType) )#<<<-----then get the view type
                      
               
params=get_params()
url=None
name=None
mode=None
iconimage=None
fanart=None
description=None
common=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:        
        mode=int(params["mode"])
except:
        pass
try:        
        fanart=urllib.unquote_plus(params["fanart"])
except:
        pass
try:        
        description=urllib.unquote_plus(params["description"])
except:
        pass
try:        
        common=urllib.unquote_plus(params["common"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "IconImage: "+str(iconimage)
   
        
#these are the modes which tells the plugin where to go
if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
       
elif mode==1:
        Install(name,url,common)
        
elif mode==2:
        iStreamFix()
        

        
elif mode==3:
        os.remove(splashimage)      
        dialog = xbmcgui.Dialog()
        dialog.ok("[COLOR blue]i[/COLOR]Stream", "", "Please Reboot To Take Effect", "")

elif mode==4:
        InstallWithout(name,url,common)        
        
xbmcplugin.endOfDirectory(int(sys.argv[1]))
