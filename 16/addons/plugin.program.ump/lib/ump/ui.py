import json
from operator import itemgetter
import time
import urllib
import urlparse

import xbmc
import xbmcaddon
import xbmcgui

from ump import providers
import prefs


addon = xbmcaddon.Addon('plugin.program.ump')
addon_dir = xbmc.translatePath( addon.getAddonInfo('path') )

class xplayer(xbmc.Player):
	def __init__(self,ump=None,*args,**kwargs):
		self.ump=ump
		if not self.ump.content_type==self.ump.defs.CT_IMAGE:
			try:
				xbmc.Player.__init__(self,xbmc.PLAYER_CORE_MPLAYER )
				#sorry team kodi, u are just so moronic to software decode mp3 files so we need to manually select player for beckwards compatiblity
			except:
				# i have no ide what kind of exception you guys will throw. congrats
				xbmc.Player.__init__(self)
			self.playlist=xbmc.PlayList(self.ump.content_type==self.ump.defs.CT_VIDEO)
		else:
			self.playlist=[]
	
	def selectmirror(self,part,auto=False):
		#in case its multiparted and it has timed out
		part=self.ump._validatepart(part)
		if len(part["urls"].keys())>1:
			if (auto or addon.getSetting("automir")=="true") and "defmir" in part and not part["defmir"]=="":
				k=part["defmir"]
			else:
				slc=self.ump.dialog.select("Select Quality", part["urls"].keys())
				k=part["urls"].keys()[slc]
		elif len(part["urls"].keys())==1:
			k=part["urls"].keys()[0]
		else:
			return "#"
		url=part["urls"][k]["url"]
		urlp=urlparse.urlparse(url)
		urlenc={"Cookie":"","User-Agent":self.ump.ua,"Referer":part["urls"][k]["referer"]}
		cook=""
		for cookie in self.ump.cj:
			if urlp.netloc in cookie.domain or cookie.domain in urlp.netloc:
				cook+=cookie.name+"="+cookie.value+";"
		urlenc["Cookie"]=cook
		return url+"|"+urllib.urlencode(urlenc),k
		self.ump.stat.query("download",part["url_provider_name"],part["link_provider_name"])
	
	def create_list(self,it,auto=False):
		dialog = xbmcgui.DialogProgress()
		dialog.create('UMP', 'Opening Media')
		if not self.ump.content_type==self.ump.defs.CT_IMAGE:
			self.playlist.clear()
		else:
			self.playlist=[]
		parts=json.loads(it.getProperty("parts"))
		for i in range(len(parts)):
			listitem = xbmcgui.ListItem()
			for key in ["uptime","urls","url_provider_hash","url_provider_name","link_provider_name"]:
				if key in parts[i].keys():
					listitem.setProperty(key,json.dumps(parts[i][key]))
			info=parts[i].get("info",None)
			art=parts[i].get("art",None)
			if info is None:
				info=self.ump.info
			if art is None:
				art=self.ump.art
			listitem.setInfo(self.ump.defs.LI_CTS[self.ump.content_type],info)
			self.ump.backwards.setArt(listitem,art)
			if "partname" in parts[i].keys():
				listitem.setLabel(parts[i]["partname"])
			else:
				listitem.setLabel(self.ump.info["title"])
			url,k=self.selectmirror(parts[i],auto)
			if url:
				if not self.ump.content_type==self.ump.defs.CT_IMAGE:
					self.playlist.add(url,listitem)
				else:
					self.playlist.append((url,parts[i]["urls"][k]["meta"]["width"],parts[i]["urls"][k]["meta"]["height"]))
			else:
				#not sure even this is possible :) gotta clean this sometime
				self.ump.add_log("Part Vanished!!!")
		dialog.close()
		return True
		
	def xplay(self):
		if not self.ump.content_type==self.ump.defs.CT_IMAGE:
			self.play(self.playlist)
			xbmcgui.Window(10000).setProperty('script.trakt.ids', json.dumps({u'imdb': self.ump.info["code"]}))
			prefs.set("play","flag",True)
		else:
			self.ump.iwindow.playlist=self.playlist
			self.ump.iwindow.doModal()

	def decode_hash(self,part):
		if not part["url"]=="#":
			return part["url"]
		else:
			name=part["url_provider_name"]
			hash=part["url_provider_hash"]
			provider=providers.load(self.ump.content_type,"url",name)
			link=provider.run(hash,self.ump)
			return link

class imagewindow(xbmcgui.WindowXMLDialog):
	def __init__(self,strXMLname, strFallbackPath, strDefaultName, forceFallback="720p"):
		self.zt=0 #zoome type 0 fited 1 zoomed
		self.cur=0
		self.playlist=None

	def onInit(self):
		self.img=self.getControl(666)
		res=[(1920,1080),(1280,720),(720,480),(720,480),(720,480),(720,480),(720,576),(720,576),(720,480),(720,480)]
		self.ww,self.wh=(1280,720)
		self.setimage(0)

	def setimage(self,cur):
		self.cur=cur%len(self.playlist)
		u,w,h=self.playlist[self.cur][0],self.playlist[self.cur][1],self.playlist[self.cur][2]
		self.w=w
		self.h=h
		self.img.setImage(u)
		self.fitmode()

	def fitmode(self,type=0):
		self.zt=type
		if self.h>self.w:
			mode=(type+1)%2
		else:
			mode=type%2
		if mode==0:
			self.img.setWidth(self.ww)
			self.img.setHeight(self.h*self.ww/self.w)
		if mode==1:
			self.img.setWidth(self.w*self.wh/self.h)
			self.img.setHeight(self.wh)

		x,y=self.img.getPosition()
		
		x1=self.ww-self.img.getWidth()
		if x1>0:
			x1=x1/2
		else:
			x1=0

		y1=self.wh-self.img.getHeight()
		if y1>0:
			y1=y1/2
		else:
			y1=0

		self.img.setPosition(x1,y1)
	
	def onAction(self, action):
		x,y=self.img.getPosition()
		#2 right 
		if action.getId() == 2:
			self.setimage(self.cur+1)
		#1 left
		if action.getId() == 1 :
			self.setimage(self.cur-1)
		#4 down 
		if action.getId() == 4:
			refy=-self.img.getHeight()+self.wh
			refx=-self.img.getWidth()+self.ww
			self.img.setPosition(x-(x-refx)/10,y-(y-refy)/10)
		#3 up
		if action.getId() == 3 :
			ref=0
			self.img.setPosition(x-(x-ref)/10,y-(y-ref)/10)

		#5 item select
		if action.getId() == 7 :
			self.fitmode(self.zt+1)

		if action.getId() in [10,92] :
			self.close()
	
	def onClick(self, controlID):
		pass

	def onFocus(self, controlID):
		pass
	
class listwindow(xbmcgui.WindowXMLDialog):
	def __init__(self,strXMLname, strFallbackPath, strDefaultName, forceFallback,ump=None):
		self.ump=ump
		self.items=[]

	def onInit(self):
		self.ump.dialogpg.close()
		q,a,p=self.ump.tm.stats()
		self.percent=0
		self.progress=self.getControl(2)
		self.ump.tm.add_queue(target=self._update, args=(p,),pri=0)
		self.lst=self.getControl(6)
		self.status=self.getControl(8)
		self.setFocus(self.lst)
		self.lst.setNavigation(self.lst,self.lst,self.lst,self.lst)
		if not self.ump.art.get("fanart","")=="":
			self.getControl(3).setImage(self.ump.art["fanart"])
			self.getControl(3).setColorDiffuse('0xFF333333')

	def _update(self,current):
		while True:
			if self.ump.terminate or self.ump.backwards.abortRequested():
				break
			q,a,p=self.ump.tm.stats()
			if not q+a+p-current == 0:
				self.percent=float(p-current+1)*100/float(q+a+p-current)
				self.progress.setPercent(self.percent)
			time.sleep(0.15)

	def onAction(self, action):
		if action.getId() in [1,2,3,4,107] :
			#user input
			pass

		if action.getId() in [10,92] :
			self.ump.shut()

	def onClick(self, controlID):
		if controlID==5 and self.percent>95:
			self.ump.shut()
		else:
			try:
				it=self.lst.getSelectedItem()
				state=self.ump.player.create_list(it)
				if state:
					self.ump.shut(True)
			except Exception,e:
				self.ump.notify_error(e)

	def onFocus(self, controlID):
		pass
	
	def addListItem(self,listItem):
		listItem.setProperty("sortid",str(len(self.items)+1))
		selected=self.lst.getSelectedItem()
		if not selected is None:
			selectedid=int(selected.getProperty("sortid"))
		else:
			selectedid=0
		k,w,h,s=self.ump.max_meta(json.loads(listItem.getProperty("parts")))
		self.items.append((listItem,w*h,s))
		self.items=sorted(self.items, key=itemgetter(2),reverse=True)
		
		index=0
		for item,res,s in self.items:
			itemid=int(item.getProperty("sortid"))
			if itemid == selectedid:
				break
			index+=1
		self.lst.reset()
		self.lst.addItems(zip(*self.items)[0])
		self.lst.selectItem(index)
		self.setFocus(self.lst)