import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,base64,sys,xbmcvfs
import urllib2,urllib

############################
###GET PARAMS###############
############################

def get_params():
	url=None
	name=None
	buildname=None
	updated=None
	author=None
	version=None
	mode=None
	iconimage=None
	description=None
	video=None
	link=None
	skins=None
	videoaddons=None
	audioaddons=None
	programaddons=None
	audioaddons=None
	sources=None
	local=None

	try:
		url=urllib.unquote_plus(params["url"])
	except:
			pass
	try:
			guisettingslink=urllib.unquote_plus(params["guisettingslink"])
	except:
			pass
	try:
			name=urllib.unquote_plus(params["name"])
	except:
			pass
	try:
			iconimage=urllib.unquote_plus(params["iconimage"])
	except:
			pass
	try:
			fanart=urllib.unquote_plus(params["fanart"])
	except:
			pass
	try:        
			mode=str(params["mode"])
	except:
			pass
	try:
			link=urllib.unquote_plus(params["link"])
	except:
			pass
	try:
			skins=urllib.unquote_plus(params["skins"])
	except:
			pass
	try:
			videoaddons=urllib.unquote_plus(params["videoaddons"])
	except:
			pass
	try:
			audioaddons=urllib.unquote_plus(params["audioaddons"])
	except:
			pass
	try:
			programaddons=urllib.unquote_plus(params["programaddons"])
	except:
			pass
	try:
			pictureaddons=urllib.unquote_plus(params["pictureaddons"])
	except:
			pass
	try:
			local=urllib.unquote_plus(params["local"])
	except:
			pass
	try:
			sources=urllib.unquote_plus(params["sources"])
	except:
			pass
	try:
			adult=urllib.unquote_plus(params["adult"])
	except:
			pass
	try:
			buildname=urllib.unquote_plus(params["buildname"])
	except:
			pass
	try:
			updated=urllib.unquote_plus(params["updated"])
	except:
			pass
	try:
			version=urllib.unquote_plus(params["version"])
	except:
			pass
	try:
			author=urllib.unquote_plus(params["author"])
	except:
			pass
	try:        
			description=urllib.unquote_plus(params["description"])
	except:
			pass
	try:        
			video=urllib.unquote_plus(params["video"])
	except:
			pass		

        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param

def params_end():

	url=None
	name=None
	mode=None
	iconimage=None
	fanart=None
	description=None

	try:
			url=urllib.unquote_plus(params["url"])
	except:
			pass
	try:
			name=urllib.unquote_plus(params["name"])
	except:
			pass
	try:
			iconimage=urllib.unquote_plus(params["iconimage"])
	except:
			pass
	try:        
			mode=int(params["mode"])
	except:
			pass
	try:        
			fanart=urllib.unquote_plus(params["fanart"])
	except:
			pass
	try:        
			description=urllib.unquote_plus(params["description"])
	except:
			pass