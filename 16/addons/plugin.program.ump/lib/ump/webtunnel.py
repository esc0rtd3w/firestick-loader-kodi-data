import random
import re
from urllib import urlencode
from urllib import unquote
import urlparse
import urllib2
from prefs import settingsActive
import copy
from time import time,ctime

import xbmcaddon
noredirs=["buka.link/includes/process.php","multiwebproxy.com/includes/process.php","http://muchproxy.com/","https://muchproxy.com/"]
addon = xbmcaddon.Addon('plugin.program.ump')
testpage="http://cdn.rawgit.com/boogiekodi/distro/a60947c9adcc2b5933cdd418aa33ec0a2a1db5d2/dataserver/ump/htdocs/test.html"
tunnels={
		"proxyduck":("cookie","referer"),
		"buka":("cookie",),
		"multiwebproxy":("cookie",),
		"muchproxy_bestserver":("cookie",),
		"muchproxy_france":("cookie",),
		"muchproxy_usa":("cookie",),
		"muchproxy_singapore":("cookie","redmp3"),
		"muchproxy_indonesia":("cookie","redmp3"),
		}

def check_health(ump,force=False):
	if addon.getSetting("disabletunnels").lower()=="true":	return
	if addon.getSetting("tn_chk_en").lower()=="false" and not force:	return
	tout=1
	t1=time()
	try:
		page=ump.get_page(testpage,"utf-8",tunnel="disabled",tout=1)
		basetime=time()-t1
	except Exception,e:
		ump.dialogpg.update(message="[COLOR red]Tunnel test page is down[/COLOR]")
		return 
	
	import prefs
	interval=int(float(addon.getSetting("tn_chk_prd")))
	attrs=[]
	for tunnel in tunnels.keys():
		lasttime=prefs.get("tunnelstates",tunnel,"lastcheck")
		if isinstance(lasttime,float) and time()-lasttime<interval*60*60 and not force:
			continue
		prefs.set("tunnelstates",tunnel,"lastcheck",time())		
		page=""
		reason="Tunnel Error"
		t1=time()
		ping=tout*1000
		try:
			page=ump.get_page(testpage,"utf-8",tunnel=tunnel,tout=tout,forcetunnel=True)
			ping=int((time()-t1-basetime)*1000)
			reason=str(ping)
		except Exception,e:
			reason=str(e.message)
			pass
		name=tunnel.replace("_"," ").title()
		if page=="<html>ump</html>":
			state="[COLOR green]up[/COLOR]"
			msg="Ping: %s ms"%reason
			en="true"
		else:
			state="[COLOR red]down[/COLOR]"
			msg="Reason: %s"%reason
			en="false"
		if ping<500:
			en="true"
		elif not "down" in state:
			state="[COLOR orange]slow[/COLOR]"
			en="false"
			reason=str(ping)
		msg="%s : %s %s,%s"%(name,state,msg,ctime())
		ump.dialogpg.update(message=msg)
		addon.setSetting("entn_%s"%tunnel,en)
		attrs.append(("entn_%s"%tunnel,"label",msg))
	prefs.set_setting_attrs(attrs)

def much_pre(domain,process,data,request,opener,cj,keyname=None,rediruri=None,session="s",timeout=86400):
	if keyname is None:
		keyname="u"
	if rediruri is None:
		rediruri="%s/browse.php"%domain
	uri=request.get_full_url()
	#if uri.startswith("http") and not uri.startswith("https"):
	#	uri="https"+uri[4:]
	data[keyname]=uri
	login=False
	cdomain=urlparse.urlparse(domain).netloc
	for cookie in cj:
		if cookie.domain==cdomain and cookie.name==session:
			login=True
			break
	if not login:
		new_req=urllib2.Request("%s/%s"%(domain,process),headers={"Referer":domain})
		resp=opener.open(new_req,data=urlencode(data))
		for cookie in cj.make_cookies(resp,new_req):
			cookie.discard=False
			#set session cookies for 1 day
			cookie.expires=time()+timeout
			cookie.domain_specified=True
			cj.set_cookie(cookie)
		del(new_req)
		del(resp)
	r="norefer"
	if request.has_header("Referer"):
		r=request.get_header("Referer")
		
	request.add_header("Referer",domain)
	request._Request__original="%s?%s"%(rediruri,urlencode({"u":uri,"f":r}))
	return request

def much_post(stream,browse):
	stream=stream.split("<!--[proxied]-->")
	if len(stream)>1:
		stream=stream[1]
	else:
		stream=stream[0]
	def clean(match):
		return match.group(1)+urlparse.parse_qs(match.group(2))["u"][0]+match.group(3)
	stream=re.sub("(\"|\'|\()\/"+browse+"\?(.*?)(\"|\'|\))", clean, stream)		
	return stream

def much_cook(cj,cookies):
	for cookie in cookies:
		try:
			newcook=copy.copy(cookie)
			cooks=re.findall("c\[(.*?)\]\[\/\]\[(.*?)\]",cookie.name)
			if len(cooks):
				[(domain,name)]=cooks
				newcook.value=unquote(cookie.value)
			else:
				[(val)]=re.findall("c\[(.*?)\]",unquote(cookie.name))
				domain,name=val.decode("base-64").split(" / ")
				newcook.value=unquote(cookie.value).decode("base-64")
			newcook.domain=domain
			newcook.name=name
			cj.set_cookie(newcook)
		except:
			print "cant cook cookie: %s"%str(cookie.name)

class tunnel():
	def __init__(self,opener):
		self.entunnels={}
		self.opener=opener
		self.activetunnels=settingsActive(["entn_%s"%x for x in tunnels.keys()])
		for tunnel in tunnels.keys():
			if addon.getSetting("entn_%s"%tunnel)=="true" and "entn_%s"%tunnel in self.activetunnels:
				self.entunnels[tunnel]=tunnels[tunnel]
		
	def set_tunnel(self,mode,force):
		tmode="disabled"
		if addon.getSetting("disabletunnels").lower()=="true":
			tmode="disabled"
		elif isinstance(mode,str):
			if force:
				tmode=mode 
			elif mode in self.entunnels.keys():
				tmode=mode
			else:
				tmode="disabled"
		elif isinstance(mode,list) or isinstance(mode,tuple):
			capables=[]
			for k,v in self.entunnels.iteritems():
				capable=True
				for capability in mode:
					if not capability in v:
						capable=False
						break
				if capable:
					capables.append(k)
			if len(capables):
				tmode=random.choice(capables)
			else:
				tmode="disabled"
		
		#print "#################################"
		#print tmode
		#print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
		return tmode
		
	def pre(self,request,tmode,cj):
		if tmode == "disabled":
			return request
		elif tmode == "proxyduck":
			r="norefer"
			if request.has_header("Referer"):
				r=request.get_header("Referer")
			request._Request__original="http://proxyduck.net/proxy/browse.php?%s"%urlencode({"u":request.get_full_url(),"f":r})
			return request
		elif tmode == "buka":
			return much_pre("http://buka.link","includes/process.php?action=update",{},request,self.opener,cj)
		elif tmode == "multiwebproxy":
			return much_pre("http://multiwebproxy.com","includes/process.php?action=update",{},request,self.opener,cj)
		elif tmode == "muchproxy_bestserver":
			return much_pre("http://muchproxy.com","",{"server":"1","submit":"GO !"},request,self.opener,cj,"url","http://hide.muchproxy.com/browse.php",True)
		elif tmode == "muchproxy_france":
			return much_pre("http://muchproxy.com","",{"server":"2","submit":"GO !"},request,self.opener,cj,"url","http://fr.muchproxy.com/browse.php",True)
		elif tmode == "muchproxy_usa":
			return much_pre("http://muchproxy.com","",{"server":"3","submit":"GO !"},request,self.opener,cj,"url","http://us.muchproxy.com/browse.php",True)
		elif tmode == "muchproxy_singapore":
			return much_pre("http://muchproxy.com","",{"server":"4","submit":"GO !"},request,self.opener,cj,"url","http://sg.muchproxy.com/browse.php",True)
		elif tmode == "muchproxy_indonesia":
			return much_pre("http://muchproxy.com","",{"server":"5","submit":"GO !"},request,self.opener,cj,"url","http://id.muchproxy.com/browse.php",True)
			

	def post(self,stream,tmode):
		if tmode == "disabled":
			return stream
		
		elif tmode == "proxyduck":
			stream=re.sub("\n.*?ginf={url:'http://proxyduck.net/proxy'.*?</script>","",stream)
			stream=re.sub('\n.*?<script type="text/javascript" src="http://proxyduck.net/proxy/includes.*?</script>',"",stream)
			stream=re.sub('\s*?<!-- PopAds.net Popunder Code for proxyduck.net -->.*?<!-- PopAds.net Popunder Code End -->',"\n",stream,flags=re.DOTALL)
			def clean(match):
				return match.group(1)+urlparse.parse_qs(match.group(2))["u"][0]+match.group(3)
			stream=re.sub("(\"|\')\/proxy\/browse\.php\?(.*?)(\"|\')", clean, stream)
			return stream
		
		elif tmode in ["buka","multiwebproxy","muchproxy_bestserver","muchproxy_france","muchproxy_usa","muchproxy_singapore","muchproxy_indonesia"]:
			return much_post(stream,"browse\.php")
	
	def cook(self,cj,cookies,tmode):
		if tmode in ["buka","multiwebproxy","muchproxy_bestserver","muchproxy_france","muchproxy_usa","muchproxy_singapore","muchproxy_indonesia"]:
			much_cook(cj, cookies)