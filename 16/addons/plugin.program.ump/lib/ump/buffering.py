from os import path
from xml.dom import minidom
import dom
from xbmcgui import Dialog
from defs import kodi_setxml


logs={
"0":"Buffer all internet filesystems (like 2 but additionally also ftp, webdav, etc.) (default)",
"1":"Buffer all filesystems, both internet and local",
"2":"Only buffer true internet filesystems (streams) (http, etc.)",
"3":"No buffer"
}

setxml=kodi_setxml

def addchild(res,parent,child):
	newnode = res.createElement(child)
	parent.appendChild(newnode)
	return newnode

def getchild(res,parent,child):
	found=False
	for ch in parent.childNodes:
		try:
			if ch.tagName==child:
				return ch
		except:
			continue
	if not found:
		return addchild(res,parent,child)

def force(mode):
	mode=str(mode)
	if path.exists(setxml):
		res=dom.read(setxml)
		adv=getchild(res,res,"advancedsettings")
		nw=getchild(res,adv,"network")
		bm=getchild(res,nw,"buffermode")
		for text in bm.childNodes:
			bm.removeChild(text)
		bm.appendChild(res.createTextNode(mode))
	else:
		res=minidom.parseString("<advancedsettings><network><buffermode>%s</buffermode></network></advancedsettings>"%mode)
	dom.write(setxml,res)
	dialog = Dialog()
	dialog.ok('UMP', 'LibCurl Buffering Mode set to %s'%mode,logs[mode],"YOU NEED TO RESTART KODI TO CHANGES TAKE AFFECT")

def get():
	if path.exists(setxml):
		res=dom.read(setxml)
		if not res:
			#minidom weirdness
			try:
				res.unlink()
			except:
				pass
			return "0" 
		adv=getchild(res,res,"advancedsettings")
		nw=getchild(res,adv,"network")
		bm=getchild(res,nw,"buffermode")
		bm=bm.lastChild
		if bm is None:
			ret="0"
		else:
			ret=bm.data
		res.unlink()
	else:
		ret="0"
	return ret