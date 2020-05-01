import json
from os import path as opath
from re import findall
from sys import argv
from urllib import urlencode
import urlparse
from xml.dom import minidom
import zlib
import dom

import xbmc
import xbmcgui

from defs import kodi_favxml


try:
	from ump.defs import WID
except:
	from defs import WID

def resolve():
	if argv[2].startswith("?hash="):
		argv[2]=zlib.decompress(argv[2][6:].decode("hex"))

def create(url=None):
	if not url is None:
		return argv[0]+"?hash="+zlib.compress(url).encode("hex")
	elif not argv[2].startswith("?hash="):
		return argv[0]+"?hash="+zlib.compress(argv[2]).encode("hex")
	else:
		return argv[0]+argv[2]


def decode(uri):
	uri=urlparse.urlparse(uri)
	#python 2.x version behave diffent about this parsing issue, dont know why
	if not uri.query=="":
		q=uri.query
	else:
		q=uri.path[2:]
	result=urlparse.parse_qs(q)
	[content_cat]=result.get('content_type', ["ump"])
	[module]= result.get('module', ["ump"])
	[page]= result.get('page', ["root"])
	[args]= result.get('args', ["e30="])
	try:
		args=json.loads(args.decode("base64"))
	except:
		args=json.loads(args.encode("utf-8")) #old url encoding format
	[info]=result.get("info", ["e30="])
	try:
		info=json.loads(info.decode("base64"))
	except:
		info=json.loads(info.encode("utf-8"))
	[art]=result.get("art", ["e30="])
	try:
		art=json.loads(art.decode("base64"))
	except:
		art=json.loads(art.encode("utf-8"))
	return uri.path,content_cat.encode("utf-8"),module.encode("utf-8"),page.encode("utf-8"),args,info,art

def load():
	favs=[]
	
	if opath.exists(kodi_favxml):
		res=dom.read(kodi_favxml)
	else:
		return None,favs
	for fav in res.getElementsByTagName("favourite"):
		cmd=None
		data=fav.lastChild.data.replace("&quot;",'"')
		cmd1=findall('RunPlugin\((.*?)"\)',data)
		cmd2=findall('PlayMedia\((.*?)"\)',data)
		cmd3=findall('ActivateWindow\(([0-9]*?)\,(.*?)"\,',data)
		if len(cmd1):
			cmd=cmd1[0]
			wid=None
		if len(cmd2):
			cmd=cmd2[0]
			wid=None
		elif len(cmd3):
			wid,cmd=cmd3[0]
		if not cmd is None:
			path,cat,module,page,args,info,art=decode(cmd)
			if not "plugin.program.ump" in path:
				continue
			name=fav.getAttribute("name").encode("utf-8")
			thumb=fav.getAttribute("thumb").encode("utf-8")
			favs.append((wid,name,thumb,data,cat,module,page,args,info,art))
	return res,favs

def ren(name,thumb,data):
	res,favs=load()
	mfavs=res.getElementsByTagName("favourites")[0]
	dialog = xbmcgui.Dialog()
	for fav in res.getElementsByTagName("favourite"):
		fname=fav.getAttribute("name").encode("utf-8")
		fthumb=fav.getAttribute("thumb").encode("utf-8")
		fdata=fav.lastChild.data.replace("&quot;",'"')
		if name==fname and fthumb==thumb and fdata==data:
			kb = xbmc.Keyboard('default', 'Rename Bookmark', True)
			kb.setDefault(name)
			kb.setHiddenInput(False)
			kb.doModal()
			newname=kb.getText()
			if not newname==name or newname=="":
				fav.setAttribute("name", newname)
				dom.write(kodi_favxml,res)
				xbmc.executebuiltin("Container.Refresh")
				dialog.ok('UMP', '%s has been to %s'%(name,newname))
			break

def rem(name,thumb,data):
	res,favs=load()
	found=False
	mfavs=res.getElementsByTagName("favourites")[0]
	dialog = xbmcgui.Dialog()
	for fav in res.getElementsByTagName("favourite"):
		fname=fav.getAttribute("name").encode("utf-8")
		fthumb=fav.getAttribute("thumb").encode("utf-8")
		fdata=fav.lastChild.data.replace("&quot;",'"')
		if name==fname and fthumb==thumb and fdata==data:
			found=True
			if 	dialog.yesno("UMP", "Are you sure you want to remove?",name):
				mfavs.removeChild(fav)
				dialog.ok('UMP', '%s has been removed from bookmarks'%name)
			break
	if found:
		dom.write(kodi_favxml,res)
		xbmc.executebuiltin("Container.Refresh")
	else:
		dialog.ok('UMP', '%s can not be found in bookmarks!'%name)
	res.unlink()


def add(isFolder,content_type,name,thumb,uri):
	p,cat,module,page,args,info,art=decode(uri)
	if opath.exists(kodi_favxml):
		res=dom.read(kodi_favxml)
	else:
		res=minidom.parseString("<favourites></favourites>")
	favs=res.getElementsByTagName("favourites")[0]
	newnode = res.createElement("favourite")
	newnode.setAttribute("name", name)
	newnode.setAttribute("thumb", thumb)
	link="plugin://plugin.program.ump/?%s"%urlencode({"module":module,"page":page,"args":json.dumps(args).encode("base64"),"info":json.dumps(info).encode("base64"),"art":json.dumps(art).encode("base64"),"content_type":content_type})
	if isFolder:
		str='ActivateWindow(%d,"%s",return)'%(WID[content_type],link)
	else:
		str='RunPlugin("%s")'%link
	favs.appendChild(newnode)
	newnode.appendChild(res.createTextNode(str))
	dom.write(kodi_favxml,res)
	dialog = xbmcgui.Dialog()
	dialog.ok('UMP', '%s added to bookmarks'%name)
