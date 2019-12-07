#############################################################################
#############################################################################
import os,xbmc,xbmcgui,xbmcaddon,sys,logging,re,urllib,urllib2

#############################################################################
#############################################################################
addon=xbmcaddon.Addon(); 
addon_id   =addon.getAddonInfo('id'); 
addon_name =addon.getAddonInfo('name'); 
addon_path =addon.getAddonInfo('path'); addon_path8=addon.getAddonInfo('path').decode("utf-8"); 
#MediaPath  =xbmc.translatePath( os.path.join(addon_path8,'resources','skins','default','media').encode("utf-8") ).decode("utf-8"); 
MediaPath  =xbmc.translatePath( os.path.join(addon_path,'resources','skins','default','media') ); 
addonPath=addon_path; addonId=addon_id; addonName=addon_name; 

#############################################################################
#############################################################################
def tP(p): return xbmc.translatePath(p)
def MediaFile(n,e='',p=MediaPath): return os.path.join(p,n+e)
def MediaFileP(n,e='',p=MediaPath): return MediaFile(n,e='.png')
def MediaFileG(n,e='',p=MediaPath): return MediaFile(n,e='.gif')
def MediaFileJ(n,e='',p=MediaPath): return MediaFile(n,e='.jpg')
def getSet(id,d=''): 
    try: return addon.getSetting(id)
    except: return d
def setSet(id,v): 
    try: return addon.setSetting(id,v)
    except: pass
def tfalse(r,d=False): ## Get True / False
	if   (r.lower()=='true' ) or (r.lower()=='t') or (r.lower()=='y') or (r.lower()=='1') or (r.lower()=='yes'): return True
	elif (r.lower()=='false') or (r.lower()=='f') or (r.lower()=='n') or (r.lower()=='0') or (r.lower()=='no'): return False
	else: return d
def isPath(path): return os.path.exists(path)
def isFile(filename): return os.path.isfile(filename)
def deb(a,b):
	try: print "%s:  %s"%(str(a),str(b))
	except: pass
def debob(o):
	try: print o
	except: pass
def nolines(t):
	it=t.splitlines(); t=''
	for L in it: t=t+L
	t=((t.replace("\r","")).replace("\n",""))
	return t
def cFL( t,c='tan'): ### For Coloring Text ###
	try: return '[COLOR '+c+']'+t+'[/COLOR]'
	except: pass
def cFL_(t,c='tan'): ### For Coloring Text (First Letter-Only) ###
	try: return '[COLOR '+c+']'+t[0:1]+'[/COLOR]'+t[1:]
	except: pass
def DoE(e): xbmc.executebuiltin(e)
def DoAW(e): xbmc.executebuiltin("ActivateWindow(%s)"%str(e))
def DoRW(e): xbmc.executebuiltin("ReplaceWindow(%s)"%str(e))
def DoRA(e): xbmc.executebuiltin("RunAddon(%s)"%str(e))
def DoRA2(e,e2="1",e3=""): xbmc.executebuiltin('RunAddon(%s,"%s","%s")'%(str(e),str(e2),e3)); 
def DoA(a): xbmc.executebuiltin("Action(%s)"%str(a))
def DoCM(a): xbmc.executebuiltin("Control.Message(windowid=%s)"%(str(a)))
def DoSC(a): xbmc.executebuiltin("SendClick(%s)"%(str(a)))
def DoSC2(a,Id): xbmc.executebuiltin("SendClick(%s,%s)"%(str(a),str(Id)))
def DoStopScript(e): xbmc.executebuiltin("StopScript(%s)"%str(e))
def showAddonSettings(): addon.openSettings()
def note(title='',msg='',delay=5000,image='http://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/US_99_%281961%29.svg/40px-US_99_%281961%29.svg.png'): xbmc.executebuiltin('XBMC.Notification("%s","%s",%d,"%s")'%(title,msg,delay,image))
def popYN(title='',line1='',line2='',line3='',n='',y=''):
	diag=xbmcgui.Dialog()
	r=diag.yesno(title,line1,line2,line3,n,y)
	if r: return r
	else: return False
	#del diag
def popOK(msg="",title="",line2="",line3=""):
	dialog=xbmcgui.Dialog()
	#ok=dialog.ok(title,msg,line2,line3)
	dialog.ok(title,msg,line2,line3)
def FileSAVE(path,data): file=open(path,'w'); file.write(data); file.close()
def FileOPEN(path,d=''):
	try:
		#deb('File',path)
		if os.path.isfile(path): ## File found.
			#deb('Found',path)
			file = open(path, 'r')
			contents=file.read()
			file.close()
			return contents
		else: return d ## File not found.
	except: return d
def FolderNEW(dir_path):
	dir_path=dir_path.strip()
	if not os.path.exists(dir_path): os.makedirs(dir_path)
def FolderLIST(mypath,dirname): #...creates sub-directories if they are not found.
	subpath=os.path.join(mypath,dirname)
	if not os.path.exists(subpath): os.makedirs(subpath)
	return subpath
def getURL(url):
	try:
		req=urllib2.Request(url)
		#req.add_header(MyBrowser[0],MyBrowser[1]) 
		response=urllib2.urlopen(req)
		link=response.read()
		response.close()
		return(link)
	except: deb('Failed to fetch url',url); return ''
def postURL(url,form_data={},headers={},compression=True):
	try:
		req=urllib2.Request(url)
		if form_data: form_data=urllib.urlencode(form_data); req=urllib2.Request(url,form_data)
		#req.add_header(MyBrowser[0],MyBrowser[1])
		for k, v in headers.items(): req.add_header(k, v)
		if compression: req.add_header('Accept-Encoding', 'gzip')
		response=urllib2.urlopen(req)
		link=response.read()
		response.close()
		return link
	except: deb('Failed to fetch url',url); return ''
def postURL2(url,form_data={}):
	try:
		postData=urllib.urlencode(form_data)
		req=urllib2.Request(url,postData)
		#req.add_header(MyBrowser[0], MyBrowser[1]) 
		response=urllib2.urlopen(req)
		link=response.read()
		response.close()
		return(link)
	except: deb('Failed to fetch url',url); return ''
def showkeyboard(txtMessage="",txtHeader="",passwordField=False):
	try:
		if txtMessage=='None': txtMessage=''
		keyboard = xbmc.Keyboard(txtMessage, txtHeader, passwordField)#("text to show","header text", True="password field"/False="show text")
		keyboard.doModal()
		if keyboard.isConfirmed(): return keyboard.getText()
		else: return '' #return False
	except: return ''
def art(f,fe=''): 
	fe1='.png'; fe2='.jpg'; fe3='.gif'; 
	if   fe1 in f: f=f.replace(fe1,''); fe=fe1; 
	elif fe2 in f: f=f.replace(fe2,''); fe=fe2; 
	elif fe3 in f: f=f.replace(fe3,''); fe=fe3; 
	return xbmc.translatePath(os.path.join(addonPath,'art',f+fe))
def artp(f,fe='.png'): 
	return art(f,fe)
def artj(f,fe='.jpg'): 
	return art(f,fe)
def addonPath2(f,fe=''):
	return xbmc.translatePath(os.path.join(addonPath,f+fe))
def get_xbmc_os():
	try: xbmc_os=str(os.environ.get('OS'))
	except:
		try: xbmc_os=str(sys.platform)
		except: xbmc_os="unknown"
	return xbmc_os
def doCtoS(c,s="",d=""): ## Put's an array (Example: [68,68,68,68]) into a string, converting each number in the array into it's character form to make up a string.
	try:
		if len(c)==0: return d
		for k in range(0,len(c)):
			s+=str(chr(c[k]))
	except: return d
#############################################################################
#############################################################################
def SKgetStringValue(Tag,ErResult=''): 
    try: return xbmc.getInfoLabel('Skin.String('+Tag+')')
    except: return ErResult
def SKchange(Tag,NewValue=''):  xbmc.executebuiltin('Skin.SetString('+Tag+', %s)' % NewValue)
def SKnchange(Tag,NewValue=0):  xbmc.executebuiltin('Skin.SetNumeric('+Tag+', %s)' % NewValue)
def SKgchange(Tag,NewValue=''):  xbmc.executebuiltin('Skin.SetImage('+Tag+', %s)' % NewValue)
def SKgLchange(Tag,NewValue=''):  xbmc.executebuiltin('Skin.SetLargeImage('+Tag+', %s)' % NewValue)
def SKbchange(Tag,NewValue=False):  xbmc.executebuiltin('Skin.SetBool('+Tag+', %s)' % NewValue)
def SKtchange(Tag,NewValue=False):  xbmc.executebuiltin('Skin.ToggleSetting('+Tag+', %s)' % NewValue)
def SKsetStringValue(Tag,NewValue=''):  xbmc.executebuiltin('Skin.SetString('+Tag+', %s)' % NewValue)
#############################################################################
#############################################################################


