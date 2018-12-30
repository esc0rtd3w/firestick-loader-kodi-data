import cookielib
import inspect
import json
import os
from random import choice
import re
import socket
from string import punctuation
import sys
import time
import datetime
import traceback
import urllib
import urllib2
from urlparse import parse_qs
import gc
import calendar

import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin

from quality import meta
from third.unescape import unescape
from third.unidecode import unidecode
from ump import buffering
from ump import cloudfare
from ump import defs
from ump import providers
from ump import proxy
from ump import task
from ump import ui
from ump import webtunnel
from ump import prefs 
from ump import http
from ump import teamkodi
from ump import clicky
from ump import identifier
from ump import stats
from ump import throttle
from third.dateutil import parser

addon = xbmcaddon.Addon('plugin.program.ump')

def findcaller(index=1):
	return inspect.getframeinfo(inspect.stack()[index][0]).filename.split(os.path.sep)[-1].split(".py")[0]

def humanint(size,precision=2):
	suffixes=['B','KB','MB','GB','TB']
	suffixIndex = 0
	while size > 1024:
		suffixIndex += 1 #increment the index of the suffix
		size = size/1024.0 #apply the division
	return "%.*f %s"%(precision,size,suffixes[suffixIndex])

def humanres(w,h):
	res=""
	heights=[240,360,480,576,720,1080,2160,4320]
	if h == 0 or w == 0 :
		return "???p"
	for height in heights:
		if h>=height*height/w:
			res=str(height)+"p"
	return res

def uniurlenc(d):
	return urllib.urlencode(dict ([k, v.encode('utf-8') if isinstance (v, unicode) else v] for k, v in d.items()))

class ump():
	def __init__(self,pt=False):
		if not os.path.exists(defs.addon_ddir):
			os.makedirs(defs.addon_ddir)
		self.pub=[]
		self.index_items=[]
		self.backwards=teamkodi.backwards()
		self.settings={}
		self.buffermode=buffering.get()
		self.log=""
		self.handle = int(sys.argv[1])
		self.ws_limit=False #web search limit
		self.defs=defs
		if self.backwards.abortRequested():sys.exit()
		self.window = ui.listwindow('select.xml', defs.addon_dir,'Default', '720p',ump=self)
		self.iwindow = ui.imagewindow('picture.xml', defs.addon_dir,"Default","720p")
		self.urlval_en=True
		self.urlval_tout=30
		self.urlval_d_size={self.defs.CT_VIDEO:1000000,self.defs.CT_AUDIO:10000,self.defs.CT_IMAGE:200}
		self.urlval_d_tout=1.5
		self.tm_conc=int(float(addon.getSetting("conc")))
		self.player=None
		self.cfagents=prefs.get("cfagents")
		self.cflocks={}
		self.mirrors=[]
		self.terminate=False
		self.loaded_uprv={}
		self.checked_uids={"video":{},"audio":{},"image":{}}
		self.pt=pt
		socket.socket = proxy.getsocket()
		policy=cookielib.DefaultCookiePolicy(rfc2965=True, rfc2109_as_netscape=True, strict_rfc2965_unverifiable=False)
		self.cj=cookielib.LWPCookieJar(os.path.join(defs.addon_ddir, "cookie"))
		self.cj.set_policy(policy)
		self.dialog=xbmcgui.Dialog()
		if os.path.exists(defs.addon_cookfile):
			try:
				self.cj.load()
			except cookielib.LoadError:
				pass
			except IOError:
				pass
		if addon.getSetting("verifyssl").lower()=="false":
			self.opener = urllib2.build_opener(http.HTTPErrorProcessor,urllib2.HTTPCookieProcessor(self.cj),http.HTTPSHandler)
		else:
			self.opener = urllib2.build_opener(http.HTTPErrorProcessor,urllib2.HTTPCookieProcessor(self.cj))	
		if addon.getSetting("overrideua")=="true":
			self.ua=addon.getSetting("useragent")
		else:
			from ump import useragents
			self.ua=choice(useragents.all)
		self.opener.addheaders = [('User-agent', self.ua)]
		self.tunnel=webtunnel.tunnel(self.opener)
		query=sys.argv[2][1:]
		result=parse_qs(query)
		[self.module]= result.get('module', ["ump"])
		[self.page]= result.get('page', ["root"])
		[args]= result.get('args', ["e30="])
		try:
			self.args=json.loads(args.decode("base64"))
		except:
			self.args=json.loads(args) # old url formatting
		for keep in ["info","art","pub"]:
			if keep in ["pub"]:default="W10="
			else: default= "e30="
			[lst]=result.get(keep, [default])
			try:
				setattr(self,keep,json.loads(lst.decode("base64")))
			except:
				try:
					setattr(self,keep,json.loads(lst))
				except:
					self.dialog.ok("Address Error","UMP can not translate the navigation URL you have provided\n\n This is mainly because you are trying to access with old favorites. To fix it delete your bookmark and add again.\n\n Another cause is because you are calling UMP from another third party addonn with wrong syntax. If so please fix your it in the addonn you are calling from.")
					self.shut()
					sys.exit()
		[self.content_type]= result.get('content_type', ["ump"])
		self.loadable_uprv=providers.find(self.content_type,"url")
		self.stats=stats.stats()
		self.throttle=throttle.throttle(self.defs.addon_tdir)

		if prefs.get("play","flag"):
			self.refreshing=True
			prefs.set("play","flag",False)
		else:
			self.refreshing=False
		self.dialogpg=teamkodi.backwards.DialogProgressBG()
		self.dialogpg.create("UMP")
		self.tm=task.manager(self.dialogpg,self.tm_conc)
		self.stat=clicky.clicky(self)
		if not self.page=="urlselect":
			self.stat.query()
		self.identifier=identifier.identifier()
		self.container_mediatype=defs.MT_NONE
		self.dialogpg.update(100,"UMP %s:%s:%s"%(self.content_type,self.module,self.page))
	
	def publish(self,*args):
		for arg in args:
			if not arg in self.pub:
				self.pub.append(arg)
		
	def subscribe(self,*args):
		for arg in args:
			if not arg in self.pub:
				return False
		return True
	
	def get_keyboard(self,*args):
		if self.refreshing:
			return True,prefs.get("play","keyboard") 
		kb = xbmc.Keyboard(*args)
		kb.setDefault("")
		kb.setHiddenInput(False)
		if not self.backwards.abortRequested():
			kb.doModal()
		if self.backwards.abortRequested():
			self.dialogpg.close()
			sys.exit()
		text=kb.getText()
		prefs.set("play","keyboard",json.dumps(text))
		if kb.isConfirmed():
			self.stat.query(search=text)
		return kb.isConfirmed(),text
		
	def absuri(self,pre,post):
		if pre.startswith("//"):
			pre="http:"+pre
		if pre.endswith("/"):
			pre=pre[:-1]
		if post.startswith("http://") or post.startswith("https://"):
			return post
		elif post.startswith("/"):
			d=pre.split("/")
			return d[0]+"//"+d[2]+post
		else:
			return pre+post

		
	def index_item(self,name,page=None,args={},module=None,thumb="DefaultFolder.png",icon="DefaultFolder.png",info={},art={},cmds=[],adddefault=True,removeold=True,isFolder=True,noicon=False,mediatype=None,content_type=None):
		if page=="urlselect":isFolder=False
		if info == {}:info=self.info
		if info is None:info={}
		if mediatype is None:
			info["mediatype"]=self.info.get("mediatype",self.defs.MT_NONE)
		else: 
			info["mediatype"]=mediatype
		if art == {}:art=self.art
		if art is None: art={}
		if thumb == "DefaultFolder.png":
			if "thumb" in art:thumb=art["thumb"]
			elif "poster" in art:thumb=art["poster"]
		if icon == "DefaultFolder.png":
			if "poster" in art:icon=art["poster"]
			elif "thumb" in art:icon=art["thumb"]
		if noicon:
			icon=thumb="DefaultFolder.png"
		else:
			self.art=art
		#if thumb == "DefaultFolder.png" and "thumb" in art and not art["thumb"] == "":thumb=art["thumb"]
		#if icon == "DefaultFolder.png" and "thumb" in art and not art["thumb"] == "":icon=art["thumb"]
		info["index"]=findcaller(2)
		self.info=info
		u=self.link_to(page,args,module,content_type)
		lname=name
		if not info["mediatype"]==self.defs.MT_NONE:
			isseen=self.stats.isseen(info)
			info["playcount"]=info["watched"]=isseen
			if isseen:
				lname="[COLOR dimgray]%s[/COLOR]"%name
			else:
				lname="[COLOR white]%s[/COLOR]"%name
		li=xbmcgui.ListItem(lname, iconImage=icon, thumbnailImage=thumb)
		li.setIconImage(icon)
		li.setThumbnailImage(thumb)
		if not noicon:self.backwards.setArt(li,art)
		li.setInfo(self.defs.LI_CTS[self.content_type],info)
		coms=[]
		if isFolder==False:
			li.addStreamInfo(self.defs.LI_SIS[self.content_type],{}) #workaround for unsupport protocol warning
		if adddefault:
			if not info["mediatype"]==self.defs.MT_NONE:
				ptr=self.identifier.getpointer(info)
				for k in range(len(ptr)):
					key=ptr[k]
					nestedptr=ptr[:k+1]
					amiseen=self.stats.isseen(info,nestedptr)
					if amiseen:cmd="unseen"
					elif not isseen:cmd="seen"
					else:continue
					if key=="code":
						try:txt=self.getnames(1,False)[0]
						except:txt=name
					else:
						txt="%s:%s"%(key,info.get(key,key))
					if not len(ptr)==k+1:
						txt="All %s"%txt
					txt="Mark %s %s"%(cmd,txt)
					txt=txt.title()
					coms.append((txt,
								"RunScript(%s,mark%s,%s,%s)"%(
															os.path.join(defs.addon_dir,"lib","ump","script.py"),
															cmd,
															urllib.quote_plus(json.dumps(info)),
															urllib.quote_plus(json.dumps(nestedptr))
															)
								))
			coms.append(('Detailed Info',"Action(Info)"))
			coms.append(('Bookmark',"RunScript(%s,addfav,%s,%s,%s,%s,%s)"%(os.path.join(defs.addon_dir,"lib","ump","script.py"),str(isFolder),self.content_type,json.dumps(name),thumb,u)))
		coms.extend(cmds)
		if adddefault:
			coms.append(("Addon Settings","Addon.OpenSettings(plugin.program.ump)"))
		li.addContextMenuItems(coms,removeold)
		self.index_items.append((u,li,isFolder,adddefault,coms,removeold,info["mediatype"]))
		return li

	def view_text(self,label,text):
		try:
			id = 10147
			xbmc.executebuiltin('ActivateWindow(%d)' % id)
			xbmc.sleep(100)
			win = xbmcgui.Window(id)
			retry = 50
			while (retry > 0):
				try:
					xbmc.sleep(10)
					win.getControl(1).setLabel(label)
					win.getControl(5).setText(text)
					retry = 0
				except:
					retry -= 1
		except:
			pass


	def match_cast(self,casting):
		match_cast=False
		if len(casting)>0:
			infocasting=self.info["cast"]
			cast_found=0
			for cast in casting:
				for icast in infocasting:
					if self.is_same(cast,icast):
						cast_found+=1
						continue

			if len(casting)==cast_found or (len(infocasting)==cast_found and len(casting)>len(infocasting)) or (len(casting)==cast_found and len(casting)<len(infocasting)):
				match_cast=True
		return match_cast

	def getnames(self,max=5,orgfirst=True):
		is_serie=self.info["mediatype"] in [self.defs.MT_EPISODE]
		names=[]
		if is_serie:
			ww=self.info["tvshowtitle"]
		else:
			ww=self.info["title"]
		if orgfirst and "originaltitle" in self.info:
			names.append(self.info["originaltitle"])
			names.append(ww)
		elif not orgfirst and "originaltitle" in self.info:
			names.append(ww)
			names.append(self.info["originaltitle"])
		if "localtitle" in self.info:
			names.append(self.info["localtitle"])
		if "alternates" in self.info:
			names.extend(self.info["alternates"])
		names2=[]
		for name in names:
			if not name in names2:
				names2.append(name)

		if max==0:
			return names2
		else:
			return names2[:max]

	def _do_container(self):
		items=[]
		mediatypes={}
		if len(self.index_items):
			for u,li,isfolder,adddef,coms,remold,mediatype in self.index_items:
				if not mediatype in mediatypes: mediatypes[mediatype]=1
				else: mediatypes[mediatype]+=1
				items.append((u,li,isfolder))
				if adddef:
					mcc=self.defs.media_to_cc[mediatype]
					coms.append(('Set current view \"default\" for %s'%mcc,"RunScript(%s,setview,%s,%s)"%(os.path.join(defs.addon_dir,"lib","ump","script.py"),self.content_type,mcc)))
					li.addContextMenuItems(coms,remold)
			xbmcplugin.addDirectoryItems(self.handle,items,len(items))
		else:
			return
		v=list(mediatypes.values())
	 	k=list(mediatypes.keys())
	 	self.container_mediatype=k[v.index(max(v))]
	 	content_cat= self.defs.media_to_cc[self.container_mediatype]
	 	xbmcplugin.setContent(self.handle, content_cat)
	 	xbmcplugin.endOfDirectory(self.handle,cacheToDisc=False,updateListing=False,succeeded=True)
		wmode=addon.getSetting("view_"+content_cat).lower()
		if wmode=="":wmode="default"
		if not wmode == "default":
			mode=self.defs.VIEW_MODES[wmode].get(xbmc.getSkinDir(),None)
		else:
			mode=prefs.get("pref_views",content_cat,xbmc.getSkinDir())
			if mode=={}: mode=None
		if not mode is None:
			for i in range(0, 10*20):
				if self.terminate or self.backwards.abortRequested():
					break
				if self.content_type==self.defs.CT_AUDIO and content_cat in ["songs","movies","artists","albums"]:
					#issue #38
					xbmc.sleep(300)
					xbmc.executebuiltin('Container.SetViewMode(%d)' % mode)
					break
				elif xbmc.getCondVisibility('Container.Content(%s)' % content_cat):
					xbmc.executebuiltin('Container.SetViewMode(%d)' % mode)
					break
				xbmc.sleep(100)
				
	def is_same(self,name1,name2,strict=False):
		predicate = lambda x:x not in punctuation+" "
		if strict:
			return filter(predicate,name1.lower())==filter(predicate,name2.lower())
		else:
			name1=name1.lower()
			name2=name2.lower()
			for word in ["the"]:
				name1=name1.replace("%s "%word,"")
				name2=name2.replace("%s "%word,"")
			return filter(predicate,unidecode(name1))==filter(predicate,unidecode(name2))
	
	def link_to(self,page=None,args={},module=None,content_type=None):
		query={}
		query["module"]=[module,self.module][module is None]
		query["page"]=[page,self.page][page is None]
		query["args"]=json.dumps(args).encode("base64")[:-1]
		query["content_type"]=[content_type,self.content_type][content_type is None]
		for keep in ["info","art","pub"]:
			query[keep]=json.dumps(getattr(self,keep)).encode("base64")[:-1]
		return sys.argv[0] + '?' + urllib.urlencode(query)

	def get_page(self,url,encoding,query=None,data=None,range=None,tout=None,head=False,referer=None,header=None,tunnel="disabled",forcetunnel=False,cache=None,throttle=2):
		if self.terminate:
			raise task.killbill
		tid=self.throttle.id(url,query,referer,header,data)
		if throttle==True:throttle=0
		if isinstance(throttle,(int,float)) and not head and not range and self.throttle.check(tid,throttle):
			stream=self.throttle.get(tid)
		else:	
			#python cant handle unicode urlencoding so needs to get dirty below.
			if not query is None:
				query=uniurlenc(query) 
				url=url+"?"+query
			if not data is None and isinstance(data,dict):
				data=uniurlenc(data)
			#change timeout
			if tout is None:
				tout=int(float(addon.getSetting("tout")))
			
			headers={'Accept-encoding':'gzip'}
			if not referer is None : headers["Referer"]=referer
			if not header is None :
				for k,v in header.iteritems():
					headers[k]=v
			tmode="disabled"
			if head==True:
				req=http.HeadRequest(url,headers=headers)
			else:
				if not range is None : headers["Range"]="bytes=%d-%d"%(range)
				req=urllib2.Request(url,headers=headers)
			if not head:
				tmode=self.tunnel.set_tunnel(tunnel,force=forcetunnel)
				req=self.tunnel.pre(req,tmode,self.cj)
			response = cloudfare.ddos_open(url,self.opener, req, data,tout,self.cj,self.cfagents,self.cflocks,self.tunnel,tmode)
			self.tunnel.cook(self.cj,self.cj.make_cookies(response,req),tmode)
			
			if head :return response
			stream=cloudfare.readzip(response)
			stream=self.tunnel.post(stream,tmode)
			if isinstance(throttle,(int,float)) and not head and not range:
				self.throttle.do(tid,stream)
		if encoding is None:
			#binary data
			src=stream
		else:
			#unicode data
			src=unicode(unescape(stream.decode(encoding,"ignore")))
		return src
	
	def web_search(self,query):
		#to do: implement a new search engine that is not money greedy,this service is down
		return []
		if self.ws_limit:
			return []
		urls=[]
		query={"v":"1.0","q":query}
		j=json.loads(self.get_page("http://ajax.googleapis.com/ajax/services/search/web","utf-8",query=query))
		status=j.get("responseStatus",0)
		if not status==200:
			self.add_log("web search exceeded its limit")
			self.ws_limit=True
			return None
		else:
			results=j["responseData"]["results"]
			for result in results:
				urls.append(result["unescapedUrl"])
		return urls

	def notify_error(self,e,silent=True):
		frm = inspect.trace()[-1]
		mod = inspect.getmodule(frm[0])
		modname = mod.__name__ if mod else frm[1]
		errtype= e.__class__.__name__
		if not silent:
			self.dialog.notification("ERROR","%s : %s"%(modname, errtype))
		if not errtype=="killbill":
			log=traceback.format_exc()
			#self.err_log=datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]+": "+log+"\n"+self.err_log
			if addon.getSetting("tracetolog")=="true":
				xbmc.log(log,defs.loglevel)

	def add_log(self,line):
		line=unidecode(unicode(line))
		self.log=datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]+": "+line+"\n"+self.log
		if hasattr(self,"window") and hasattr(self.window,"status"):
			self.window.status.setText(self.log)
		if addon.getSetting("logtolog")=="true":
			xbmc.log(line,defs.loglevel)

	def add_mirror(self,parts,name,wait=0,missing="drop"):
		hs=re.match("\[HS\:(.*?)\]",name,re.IGNORECASE)
		d=re.match("\[D\:(.*?)\]",name,re.IGNORECASE)
		language=self.backwards.getLanguage(0).lower()
		link_provider=findcaller()
		if not (self.terminate or self.backwards.abortRequested()) and isinstance(parts,list) and len(parts)>0:
			for part in parts:
				part["link_provider_name"]=link_provider
				upname=part.get("url_provider_name",None)
				uphash=part.get("url_provider_hash",None)
				if addon.getSetting("dismiss_sub_other")=="true" and hs and not hs.group(1).lower() in [language,"en"]:
					self.add_log("HARD SUBTITLE, Dismissing : %s, %s , %s" % (str(self.content_type),name,str(upname)))
					return
				if addon.getSetting("dismiss_dub_other")=="true"and d and not d.group(1).lower() in [language,"en"]:
					self.add_log("OVERDUB, Dismissing : %s, %s , %s" % (str(self.content_type),name,str(upname)))
					return
				#sanity check
				if upname is None or uphash is None:
					return False
				#check if there is an appropriate url provider
				if not providers.is_loadable(self.content_type,"url",upname,self.loadable_uprv):
					self.add_log("no appropriate url provider. Skipping : %s , %s" % (str(self.content_type),str(upname)))
					return False
				#check if provider first time. checked ids are dynamic on provider name
				elif upname in self.checked_uids[self.content_type].keys():
				#check if already proccesed
					if uphash in self.checked_uids[self.content_type][upname]:
						self.add_log("already processed, skipping :%s , %s, %s " % (str(self.content_type),str(upname),str(uphash)))
						return False
				else:
				#if first time, create list dynamically
					self.checked_uids[self.content_type][upname]=[]
				self.checked_uids[self.content_type][upname].append(uphash)
			try:
				caller = inspect.getframeinfo(inspect.stack()[1][0])
				lpname=os.path.split(caller.filename)[-1].split(".")[0].split("_")[2]
			except:
				lpname=None
			self.tm.add_queue(target=self._on_new_id, args=(lpname,parts,name,wait,missing),pri=5)
		else:
			return False

	def max_meta(self,parts):
		#get the highest quality info from each part and mirror
		q=0
		max_w=0
		max_h=0
		max_s=0
		part_s=0
		max_key=""
		for part in parts:
			ss=0
			part_s=0
			for key,mirror in part["urls"].iteritems():
				if not part["urls"][key]["meta"] == {}:
					t=part["urls"][key]["meta"]["type"]
					w=part["urls"][key]["meta"]["width"]
					h=part["urls"][key]["meta"]["height"]
					s=part["urls"][key]["meta"]["size"]
					if not (w is None or h is None) and w*h>=q:
						max_w=w
						max_h=h
						q=w*h
					if not s is None and s>ss:
						max_key=key
						part_s=s
						ss=s
			max_s+=part_s
		return max_key,max_w,max_h,max_s

	def _on_new_id(self,lpname,parts,name,wait,missing):
		##validate media providers url first before adding
		self._validateparts(parts,wait)
		ignores=[]
		for k in range(len(parts)):
			if parts[k]["urls"]=={}:
				#if even 1 part is missing drop the mirror!!
				if missing=="drop":
					self.add_log("mirror dropped, has missing parts: %s"%str(parts))
					return False
				elif missing=="ignore":
					self.add_log("part %s,%s ignored"%(parts[k]["url_provider_name"],parts[k]["url_provider_hash"]))
					ignores.append(k)
		
		for ignore in sorted(ignores,reverse=True):
			parts.pop(ignore)
		
		if not len(parts):
			return None

		#if payer is not yet ready init it.
		if self.player is None:
			self.player=ui.xplayer(ump=self)

		max_k,max_w,max_h,max_s=self.max_meta(parts)
		prefix_q=prefix_s=""

		if max_w*max_h>0:
			prefix_q="[R:%s]"%humanres(max_w,max_h)

		if max_s>0: 
			prefix_s="[F:%s]"%humanint(max_s)
		mname=prefix_q+prefix_s+name
		autoplay=False
		if self.content_type==self.defs.CT_VIDEO and addon.getSetting("auto_en_video")=="true":
			if addon.getSetting("video_val_method") in ["Check if Alive & Quality","Check if Alive + Quality"]:
				if unicode(prefix_q[3:-2]).isnumeric() and int(prefix_q[3:-2])>=int(float(addon.getSetting("min_vid_res"))):
					autoplay=True
			if addon.getSetting("video_val_method")=="Check if Alive Only" or addon.getSetting("video_val_method") in ["Check if Alive & Quality","Check if Alive + Quality"] and autoplay:
				tags=re.findall("\[(.*?)\]",name)
				required=addon.getSetting("require_tag").split(",")
				filtered=addon.getSetting("dont_require_tag").split(",")
				autoplay=True
				for tag in tags:
					if not tag=="" and tag.lower().replace(" ","") in [x.lower().replace(" ","") for x in filtered]:
						autoplay=False
						break
				
				for require in required:
					if not require=="" and not require.lower().replace(" ","") in [x.lower().replace(" ","") for x in tags]:
						autoplay=False
						break
				
		if self.content_type==self.defs.CT_AUDIO and addon.getSetting("auto_en_audio")=="true" and addon.getSetting("audio_val_method")=="Check if Alive Only":
			autoplay=True

		if self.content_type==self.defs.CT_IMAGE and addon.getSetting("auto_en_image")=="true" and addon.getSetting("audio_val_method") in ["Check if Alive & Quality","Check if Alive + Quality"]:
			autoplay=True

		item=xbmcgui.ListItem()
		item.setLabel(mname)
		item.setLabel2(self.info["title"])
		item.setProperty("parts",json.dumps(parts))
		item.setProperty("lpname",lpname)
		upname=parts[0].get("url_provider_name",None)
		art={}
		if not upname is None:
			art["icon"]=defs.arturi+parts[0]["url_provider_name"]+".png"
			item.setIconImage(defs.arturi+parts[0]["url_provider_name"]+".png")
		if not lpname is None:
			#art["thumb"]=defs.arturi+lpname+".png"
			item.setProperty("lpimg",defs.arturi+lpname+".png")
		self.backwards.setArt(item,art)
		#if there is no more mirrors and media does not require a provider directly play it.
		if autoplay:
			try:
				state=self.player.create_list(item,True)
				if state:
					self.shut(True,3)
				return None
			except Exception,e:
				self.notify_error(e)

		self.window.addListItem(item)
		#self.stat._query("click",parts[0]["url_provider_name"],parts[0]["link_provider_name"])
		
	def _validateparts(self,parts,wait):
		gid=self.tm.create_gid()
		def wrap(i):
			parts[i]=self._validatepart(parts[i])

		for k in range(len(parts)):
			self.tm.add_queue(wrap,(k,),gid=gid,pri=5)
			time.sleep(wait)
		self.tm.join(gid)

	def _validatepart(self,part):
		metaf=getattr(meta,self.content_type)
		timeout=self.urlval_tout
		provider=providers.load(self.content_type,"url",part["url_provider_name"])
		if hasattr(provider,"timeout") and isinstance(provider.timeout,int):
			timeout=provider.timeout
		#if urls require validation and url is not validated or timed out
		if not "uptime" in part.keys() or time.time()-part["uptime"]>timeout:

			try:
				self.add_log("retrieving url from %s:%s"%(part["url_provider_name"],part["url_provider_hash"]))
				part["urls"]=provider.run(part["url_provider_hash"],self,part.get("referer",""))
			except (socket.timeout,urllib2.URLError,urllib2.HTTPError),e:
				self.add_log("dismissed due to timeout: %s " % part["url_provider_name"])
				part["urls"]={}
			except Exception,e:
				self.notify_error(e)
				part["urls"]={}
			#validate url by downloading header (and check quality)
			if not isinstance(part["urls"],dict):
				part["urls"]={}
			for key in part["urls"].keys():
				if not isinstance(key,str):
					try:
						part["urls"][str(key)]=part["urls"].pop(key)
						key=str(key)
					except:
						self.add_log("unsupport url key type '%s' in url provider %s"%(type(key),part["url_provider_name"]))
						part["urls"].pop(key)
						continue
				try:
					u=part["urls"][key]
					#overide the referer from url provider when it sends dict mirrors
					if not isinstance(u,dict):
						part["urls"][key]={}
						part["urls"][key]["referer"]=part.get("referer","")
						part["urls"][key]["url"]=u
					method=addon.getSetting(self.content_type+"_val_method")
					m=metaf("",method,self.get_page,part["urls"][key]["url"],part["urls"][key]["referer"])
					part["urls"][key]["meta"]=m
				except (socket.timeout,urllib2.URLError,urllib2.HTTPError),e:
					part["urls"].pop(key)
					self.add_log(" dismissed due to network error: %s" % part["url_provider_name"])
					#print part
					#print e
				except Exception,e:
					self.notify_error(e)
					part["urls"].pop(key)
					self.add_log("validation failed: key removed : %s, %s"%(key,part["url_provider_name"]))
			part["uptime"]=time.time()
			k,w,h,s=self.max_meta([part])
			part["defmir"]=k
		return part

	def shut(self,play=False,noblock=0):
		self.terminate=True
		prefs.set("cfagents",self.cfagents)
		if hasattr(self,"tm"):
			self.tm.stop()
		if hasattr(self,"dialogpg"):
			self.dialogpg.close()
			del(self.dialogpg)
		if self.backwards.abortRequested():
			return
		if hasattr(self,"window"):
			self.window.close()
		try:
			self.cj.save()
		except:
			try:
				os.remove(defs.addon_cookfile)
			except:
				pass
		if play:
			self.player.xplay()
			self.stats.markseen(self.info)
			cnt=0
		else:
			cnt="all"	
		if hasattr(self,"iwindow"):
			self.iwindow.close()
		if int(self.handle)==-1:
			self.tm.join(noblock=noblock,cnt=cnt)
		if hasattr(self,"dialogpg"):
			self.dialogpg.close()

	def _clean(self):
		if hasattr(self,"dialogpg"):
			del(self.dialogpg.bg)
		if hasattr(self,"dialog"):
			del(self.dialog)
		if hasattr(self,"window"):
			if hasattr(self.window,"status"):
				del(self.window.status)
			del(self.window.items)
			del(self.window)
		if hasattr(self,"iwindow"):
			if hasattr(self.iwindow,"img"):
				del(self.iwindow.img)
			del(self.iwindow)
		if hasattr(self,"player"):
			del(self.player)
		if hasattr(self,"backwards"):
			del(self.backwards.m)
			del(self.backwards)
		del self.index_items
		if hasattr(self,"tm"):
			del(self.tm.m)
		del gc.garbage[:]
		gc.collect()