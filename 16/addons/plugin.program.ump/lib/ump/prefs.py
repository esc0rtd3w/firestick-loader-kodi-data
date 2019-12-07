import xbmc
from defs import addon
from defs import addon_preffile
from defs import kodi_sdir
from defs import addon_setxml
from os import path
import json
import dom

preffile=addon_preffile

def prefs(mode,data=None):
	if data is None and not path.exists(preffile):
		return ""
	try:
		fo=open(preffile, mode)
	except:
		pass
	with fo as pref:
		if data is None:
			ret=pref.read()
		else:
			try:
				ret=pref.write(data)
			except:
				pass
	return ret

def get_skin_view(ctype):
	xmls={"video":"MyVideoNav.xml","audio":"MyMusicNav.xml","image":"MyPics.xml"}
	res=dom.read(path.join(kodi_sdir,"addon.xml"))
	dir=res.getElementsByTagName("res")[0].getAttribute("folder")
	res.unlink()
	navxml=path.join(kodi_sdir,dir,xmls[ctype])
	res=dom.read(navxml)
	views=res.getElementsByTagName("views")[0].lastChild.data.split(",")
	res.unlink()
	for view in views:
		label=xbmc.getInfoLabel("Control.GetLabel(%s)"%view)
		if not (label == '' or label == None): break
	return xbmc.getSkinDir(),view

def settingsActive(sets):
	res=dom.read(addon_setxml)
	actives=[]
	for set in sets:
		for setting in res.getElementsByTagName("setting"):
			if setting.getAttribute("id") == set and not setting.getAttribute("visible").lower()=="false":
				actives.append(set)
				break
	res.unlink()
	return actives

def set_setting_attrs(attrs):
	ret=False
	res=dom.read(addon_setxml)
	for name,set,val in attrs:
		for setting in res.getElementsByTagName("setting"):
			if setting.getAttribute("id") == name:
				setting.setAttribute(set,val)
				ret=True
				break
	if ret:
		dom.write(addon_setxml,res)
	return ret

def setkeys(d,k,v):
	s="d"
	for key in k:
		s=s+"['%s']"%key
	exec("%s=%s"%(s,v))
	return d

def getkeys(d,k):
	s="d"
	for key in k:
		if key == k[-1]:
			s=s+".get('%s',{})"%key
		else:
			s=s+"['%s']"%key
	return eval(s)

#this function loads a json encoded string and and convert the dict of dics in it to python onjects, ie:data["master"]["sub"]["subofsub"]....
#the purpose is to use dict as a nested xml-like object, if the pointed path does not exists in the dict of dicts
#function creates an empty dict with the correct dict structure. This is used to stored data in settings.xml
#in a hidden string with json encoding. path dicts are only accepted as string!!! dont use numerics and weird types
#that is a restriction in json and the returned value can be anything that json can encode, basically all generic built in types
#ie: int,float,str, None, list, tuple, dicts etc..

def dictate(boot,path):
	#boot: json string to decode
	#path to n, path strings.
	try:
		boot=json.loads(boot)
	except:
		boot={}
	prekeys=[]
	for key in path:
		currentkey=getkeys(boot,prekeys)
		if not key in currentkey:
			prekeys.append(key)
			setkeys(boot,prekeys,{})
		else:
			prekeys.append(key)
	
	return boot	

def get(*args):
	#args: path to prefernce dict key
	result=dictate(prefs("r"),args)
	prefs("wb",json.dumps(result))
	return getkeys(result,args)

def set(*args):
	#args: path to prefernce dict key
	#args(n): set object
	result=dictate(prefs("r"),args[:-1])
	setkeys(result,args[:-1],args[-1])
	prefs("wb",json.dumps(result))

def set_view(ctype,ccat):
	sid,vid=get_skin_view(ctype)
	set("pref_views",ccat,sid,vid)
	if not addon.getSetting("view_%s"%ccat).lower()=="default":
		addon.setSetting("view_%s"%ccat,"Default")