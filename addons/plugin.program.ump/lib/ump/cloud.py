from third import dropbox
import xbmcgui
import xbmcaddon
import sys
from xml.dom import minidom
import urllib2
from distutils.version import LooseVersion
from ump import defs

addon = xbmcaddon.Addon('plugin.program.ump')

def upload(content,name,overwrite=True):
    dropbox.client.DropboxClient("oDWx2zTSXZAAAAAAAAAACCD5aQr2FgS-fe33WMr7moiZr9aHAp0gpuvUyXtiDHX5").put_file("/%s"%name, content,overwrite=overwrite)
    
def upload_log(head,msg,name,locals,errlog,kodilog,umplog,extra):
    dialog = xbmcgui.Dialog()
    if(dialog.yesno(head,msg)):
        content="UMP VER:%s\r\nSYS ARGV:%s\r\nLOCAL INFO:\r\n%s\r\nERROR LOG:\r\n%s\r\nKODI LOG:\r\n%s\r\nUMP LOG:\r\n%s\r\n%s"%(addon.getAddonInfo('version'),str(sys.argv)+"\r\n",locals,errlog,kodilog,umplog,extra)
        upload(content,name)
    else:
        print errlog

def get_latest():
	try:
		dom=minidom.parseString(urllib2.urlopen(defs.addonsxmluri).read())
		for tag in dom.getElementsByTagName("addon"):
			xmlver=LooseVersion(tag.getAttribute("version"))
			addver=LooseVersion(addon.getAddonInfo('version'))
			if tag.getAttribute("id")=="plugin.program.ump" and xmlver>addver :
				return xmlver
	except:
		return None
    
def collect_log(logtype,head,msg,umplog,e=None,more=True):
    errlog=""
    fname=logtype
    umplog=umplog.split("\n")
    umplog="\r\n".join(umplog[::-1])
    if not e is None:
        import inspect
        import traceback
        frm = inspect.trace()[-1]
        mod = inspect.getmodule(frm[0])
        modname = mod.__name__ if mod else frm[1]
        errtype= e.__class__.__name__
        fname+="_"+errtype
        errlog=errtype+"\r\n"+traceback.format_exc().replace("\n","\r\n")
    import os
    from third import logviewer
    logmodule=logviewer.Logmodule()
    kodilog=logmodule.getcontent()
    from datetime import datetime
    fname+="_"+datetime.utcnow().strftime("%Y%m%d+%H%M%S")
    import platform
    localdata="PLATFORM        : "+os.name
    fname+="_"+os.name
    localdata+="\r\nRELEASE         : "+platform.release()
    fname+="_"+platform.release()
    localdata+="\r\nENVIRONMENT     : "+str(os.environ)
    import xbmc
    localdata+="\r\nXBMC VERSION    : "+xbmc.getInfoLabel( "System.BuildVersion" )
    fname+="_"+xbmc.getInfoLabel( "System.BuildVersion" )
    localdata+="\r\nPYTHON VERSION  : "+platform.python_version()
    fname+="_"+platform.python_version()
    localdata+="\r\n"
    fname=fname.replace(" ","_").replace("/","-").replace(":","-").replace("?","-").replace(".","-")
    fname+=".log"
    from ump import defs
    extra=""
    if more:
        others={"working_xml":os.path.join(defs.addon_ddir,"settings.xml"),"addon_xml":defs.addon_setxml,"addon_prefs":defs.addon_preffile,"addon_cookies":defs.addon_cookfile,"kodi_advanced":defs.kodi_setxml,"guisettings":defs.kodi_guixml}
        for k,v in others.iteritems():
            if os.path.exists(v):
                f=open(v)
                extra+="\r\n%s : \r\n %s"%(k.upper(),f.read().replace("\n","\r\n"))
                f.close()
            else:
                extra+="\r\n%s : %s does not exist"%(k.upper(),v)
    upload_log(head,msg,fname,localdata,errlog,kodilog,umplog,extra)