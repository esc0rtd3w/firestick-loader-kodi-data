# -*- coding: utf-8 -*-

import xbmc,xbmcaddon,xbmcgui,xbmcplugin,urllib,os,re,sys

def list_addons():
      #info directory
      addDir('[COLOR lime][B]%s[/B][/COLOR]' % (translate(30001)),'None',None,os.path.join(xbmc.translatePath(xbmcaddon.Addon().getAddonInfo('path')).decode('utf-8'),'icon.png'))

      #get the path of addons
      pathofaddons = xbmc.translatePath('special://home/addons').decode('utf-8')

      #list with addons
      listofaddons = os.listdir(pathofaddons)
      for individual_addon in listofaddons:
            #path to individual addon, cycle for all the addons
            path_to_addon = os.path.join(pathofaddons, individual_addon)

            #define addon.xml path
            addon_xml_path=os.path.join(path_to_addon,'addon.xml')

            #check the existence of addon.xml, if true, we continue
            if os.path.exists(addon_xml_path):

                  #get addon.xml content
                  xml_content=openfile(addon_xml_path)

                  if re.search('point="xbmc.service"',xml_content):
                        #addon with service on
                        addDir('%s (on)' % (individual_addon),path_to_addon,1,os.path.join(path_to_addon,'icon.png'))
                  elif re.search('point="xbmc.pass"',xml_content):
                        #addon with service off
                        addDir('[B][COLOR lime]%s[/B] (off)[/COLOR]' % (individual_addon),path_to_addon,1,os.path.join(path_to_addon,'icon.png'))
                  else:
                        #addon with no service
                        pass

def change_state(name,path):
      #define addon.xml path to change
      addon_xml_path=os.path.join(path,'addon.xml')

      #get addon.xml content
      content=openfile(addon_xml_path)
      
      if re.search('COLOR lime',name):
            #service off to on, so we change from fake variable to service variable
            content=content.replace('point="xbmc.pass"','point="xbmc.service"')
      else:
            #service on to off, so we change from service variable to fake variable
            content=content.replace('point="xbmc.service"','point="xbmc.pass"')

      #change state on addon.xml
      savefile(addon_xml_path,content)

      #refresh the list
      xbmc.executebuiltin("Container.Refresh")
      

def openfile(path_to_the_file):
    try:
        fh = open(path_to_the_file, 'rb')
        contents=fh.read()
        fh.close()
        return contents
    except:
        print "Wont open: %s" % filename
        return None

def savefile(path_to_the_file,content):
    try:
        fh = open(path_to_the_file, 'wb')
        fh.write(content)  
        fh.close()
    except: print "Wont save: %s" % filename

def addDir(name,path,mode,iconimage):
      return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url="%s?path=%s&mode=%s&name=%s" % (sys.argv[0],urllib.quote_plus(path),mode,urllib.quote_plus(name)),listitem=xbmcgui.ListItem(name,iconImage="DefaultFolder.png", thumbnailImage=iconimage),isFolder=False)

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

def translate(text):
      return xbmcaddon.Addon().getLocalizedString(text).encode('utf-8')

params=get_params()
path=None
name=None
mode=None

try: path=urllib.unquote_plus(params["path"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass

if mode==None: list_addons()
elif mode==1: change_state(name,path)
                       
xbmcplugin.endOfDirectory(int(sys.argv[1]))
