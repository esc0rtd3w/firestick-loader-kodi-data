from os import walk

from defs import addon
from defs import addon_setxml
from defs import addon_pdir
from defs import CT_AUDIO
from defs import CT_IMAGE
from defs import CT_VIDEO
from defs import CT_UMP
import dom

cats=[CT_AUDIO, CT_IMAGE, CT_VIDEO,CT_UMP]
types=["index","link","url"]

def update_settings():
	lst=[]
	for root, dirs, files in walk(addon_pdir):
		for file in files:
			if file.endswith('.py') and len(file.split("_"))==3 and file.split("_")[0] in cats and file.split("_")[1] in types:
				lst.append(file[:-3].split("_"))
	#first remove unused providers from settings.xml
	res=dom.read(addon_setxml)
	inxml=[]
	for xcat in res.getElementsByTagName("category"):
		if xcat.getAttribute("id").lower() in types:
			for item in xcat.getElementsByTagName("setting"):
				if not item.getAttribute("id").lower().split("_") in lst:
					xcat.removeChild(item)
				else:
					inxml.append(item.getAttribute("id").lower().split("_"))

	#then remove disabled providers from list and determine new providers to be added to xml
	addnew=[]
	lst2=[]
	for prv in lst:
		if not prv in inxml:
			addnew.append(prv)
		set=addon.getSetting("%s_%s_%s"%(prv[0],prv[1],prv[2]))
		if not set.lower()=="false":
			lst2.append(prv)
	
	#finally add new providers to xml
	for prv in addnew:
		for xcat in res.getElementsByTagName("category"):
			if xcat.getAttribute("id").lower()==prv[1]:
				newnode = res.createElement("setting")
				newnode.setAttribute("id", ("%s_%s_%s"%(prv[0],prv[1],prv[2])))
				newnode.setAttribute("type", "bool")
				newnode.setAttribute("label", "%s:%s"%(prv[0].upper(),prv[2].title()))
				newnode.setAttribute("default", "true")
				xcat.appendChild(newnode)
	dom.write(addon_setxml,res)
	return lst2

def find(cat,type):
	lst=[]
	for root, dirs, files in walk(addon_pdir):
		for file in files:
			if file.endswith('.py') and len(file.split("_"))==3 and file.split("_")[0] in cats and file.split("_")[1] in types:
				lst.append(file[:-3].split("_"))
	lst2=[]
	lst3=[]
	for item in lst:
		if item[0] == "ump" and item[1]==type and not addon.getSetting("%s_%s_%s"%(item[0],item[1],item[2]))=="false":
			lst3.append(item)
		elif (item[0]==cat or cat == "ump") and item[1]==type and not addon.getSetting("%s_%s_%s"%(item[0],item[1],item[2]))=="false":
			lst2.append(item)
	lst2.extend(lst3)
	return lst2

def is_loadable(cat,type,name,providers=None):
	providers=[providers,find(cat,type)][providers is None]
	if [cat,type,name] in providers:
		return 1
	elif ["ump",type,name] in providers:
		return 2
	else:
		return 0

def load(cat,type,name):
	fname=cat+"_"+type+"_"+str(name)
	module=__import__("providers",fromlist=[fname])
	return getattr(module,fname)