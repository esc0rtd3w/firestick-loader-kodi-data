import sys
import os
import platform
import xbmc
import time
import uuid
import md5
import random
import urllib
import xbmcaddon
siteid="100993492"
sitedomain="http://cdn.rawgit.com"
searchkey="umpsearch"

ostoua={
		"xp":"Windows NT 5.1",
		"2000":"Windows NT 5.1",
		"7":"Windows NT 6.1",
		"post2008Server":"Windows NT 6.2",
		"8":"Windows NT 6.2",
		"post2012Server":"Windows NT 10.0",
		"10":"Windows NT 10.0",
		}

uatohuman={
		   "Windows NT 5.1":"Windows XP",
		   "Windows NT 6.1":"Windows 7",
		   "Windows NT 6.2":"Windows 8",
		   "Windows NT 10.0":"Windows 10",
		   "Windows CE":"Windows CE"
		   }

customptr={"download":"played","click":"found"}
addon = xbmcaddon.Addon('plugin.program.ump')

class clicky():
	def __init__(self,ump):
		self.ump=ump
		env=os.environ
		release=platform.release()
		osname=os.name.lower()
		build="1.2.3"
		ostr=""
		if "ANDROID_SYSTEM_LIBS" in str(env):
			ostr="Linux; Android 4.4; %s"%(build)
			cos="Android"
		elif osname in ["linux","posix"]:
			ostr="Linux; Linux %s; %s"%(release,build)
			cos="Linux"
		elif osname in ["windows","nt"]:
			ostr="%s; %s"%(ostoua.get(release,"Windows CE"),build)
			cos=uatohuman[ostoua.get(release,"Windows CE")]
		else:
			ostr="%s_%s; %s"%(osname,build,build)
			cos="unknown:%s_%s"%(osname,build)
		self.os_ua=ostr
		self.os_human=cos
		
	def _getsession(self):
		cval=str(int(random.random()*4294967295))
		for cookie in self.ump.cj:
			if "getclicky.com" in cookie.domain and cookie.name=="cluid":
				cval=cookie.value
				break   
		return cval
	
   
	def _query(self,mode="pageview",urlprovider=None,linkprovider=None,search=None):
		if not addon.getSetting("allowstats").lower()=="true":return
		cookie=self._getsession()
	
		#get language
		lang=self.ump.backwards.getLanguage(0).lower()
		if lang=="": lang="en"
	
		query={
			"site_id":siteid,
			"res":"%sx%s"%(xbmc.getInfoLabel("System.ScreenWidth"),xbmc.getInfoLabel("System.ScreenHeight")),
			"lang":lang,
			"type":mode,
			"href":"/%s/%s/%s/%s"%(self.ump.content_type,self.ump.module,self.ump.page,self.ump.args),
			"title":"%s:%s"%(self.ump.module,self.ump.page),
			"mime":"js",
			"jsuid":cookie,
			"custom[osname]":self.os_human,
			"custom[kodiversion]":xbmc.getInfoLabel( "System.BuildVersion" ),
			"custom[pythonversion]":platform.python_version(),
			"custom[addonversion]":addon.getAddonInfo('version'),
			}

		if mode in ["download","click"]:
			str=customptr[mode]
			if self.ump.content_type==self.ump.defs.CT_VIDEO:
				id1=self.ump.info.get("season","season")
				id2=self.ump.info.get("episode","episode")
				id3="%s/%s"%(self.ump.info.get("tvshowtitle",""),self.ump.info.get("etitle",self.ump.info.get("title","title")))
				media=id3
			elif self.ump.content_type==self.ump.defs.CT_AUDIO:
				id1=self.ump.info.get("artist","artist")
				id2=self.ump.info.get("album","album")
				id3=self.ump.info.get("title","title")
				media="%s/%s"%(id1,id3)
			elif self.ump.content_type==self.ump.defs.CT_IMAGE:
				id1=self.ump.info.get("season","volume")
				id2=self.ump.info.get("episode","chapter")
				id3=self.ump.info.get("title","title")
				media="%s/Chapter %s"%(id3,id2)
			query["href"]="/%s/%s/%s/%s/%s"%(
											self.ump.content_type,
											self.ump.info.get("code","code"),
											id1,
											id2,
											id3
											)
			query["title"]=media
			query["custom[%s_urlprovider]"%str]=urlprovider
			query["custom[%s_linkprovider]"%str]=linkprovider
			query["custom[%s_media]"%str]=media
			query["custom[%s_mediatype]"%str]=self.ump.content_type
			query["custom[%s_code]"%str]=self.ump.info.get("code","code")
		
		if not search is None:
		   query["href"]="/search?"+urllib.urlencode({searchkey:search})
		   query["custom[search]"]=search
		
		#manipulate user agent string so web ui will understand os, hardware
		ua=self.ump.ua[12:].split(")")
		ua[0]=self.os_ua
		ua=")".join(ua)
		ua="Mozilla/5.0 ("+ua
		
		d=self.ump.get_page("http://in.getclicky.com/in.php",None,query=query,referer=sitedomain,header={"User-Agent":ua},throttle=False)

	def query(self,mode="pageview",urlprovider=None,linkprovider=None,search=None):
		if not addon.getSetting("allowstats").lower()=="true":return
		gid=self.ump.tm.create_gid()
		self.ump.tm.add_queue(self._query,(mode,urlprovider,linkprovider,search),gid=gid)
