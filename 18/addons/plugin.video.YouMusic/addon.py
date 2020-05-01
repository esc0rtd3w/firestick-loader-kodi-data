# Addon Name: YouMusic
# Addon id: plugin.video.YouMusic
# Addon Provider: spanky
"""

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.
 
 """

import urllib,urllib2,re,xbmcplugin,xbmcgui,os,sys,datetime
from resources.lib.common_variables import *
from resources.lib.directory import *
from resources.lib.youtubewrapper import *
from resources.lib.watched import * 

fanart = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.YouMusic', 'fanart.jpg'))
art = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.YouMusic/resources/img', ''))

def CATEGORIES():
        addDir('[COLOR blue]Popular Music Videos[/COLOR]','PLFgquLnL59alCl_2TQvOiD5Vgm1hCaGSI',1,art + 'Music.png')
        addDir('[COLOR blue]New Music This Week[/COLOR]','PLFgquLnL59alW3xmYiWRaoz0oM3H17Lth',1,art + 'Music.png')
        addDir('[COLOR blue]Spotlight On: Leonard Cohen[/COLOR]','PLFgquLnL59alFaD6qZtCpJgV2CB9L-Boq',1,art + 'Music.png')
        addDir('[COLOR blue]Latest Music Videos[/COLOR]','PLFgquLnL59akA2PflFpeQG9L01VFg90wS',1,art + 'Music.png')
        addDir('[COLOR blue]Top Tracks - Electronic Music[/COLOR]','PLFPg_IUxqnZNnACUGsfn50DySIOVSkiKI',1,art + 'Music.png')
        addDir('[COLOR blue]Spotlight On: Visually Stunning[/COLOR]','PLFgquLnL59ansZbAyA-OqSvImU8yo9j5I',1,art + 'Music.png')
        addDir('[COLOR blue]Top Tracks - House Music[/COLOR]','PLhInz4M-OzRUsuBj8wF6383E7zm2dJfqZ',1,art + 'Music.png')
        addDir('[COLOR blue]Top Tracks - Latin Music [/COLOR]','PLcfQmtiAG0X-fmM85dPlql5wfYbmFumzQ',1,art + 'Music.png')
        addDir('[COLOR blue]The Electronic Index[/COLOR]','PLFgquLnL59akXPIHrEZci0oouw4dArE0D',1,art + 'Music.png')
        addDir('[COLOR blue]Top Tracks - House Music [/COLOR]','PLhInz4M-OzRUsuBj8wF6383E7zm2dJfqZ',1,art + 'Music.png')
        addDir('[COLOR blue]Spotlight On: October Recap[/COLOR]','PLFgquLnL59amdobdR5OfC5OW3YoGtavfT',1,art + 'Music.png')
        addDir('[COLOR blue]Spotlight On: Weekend Soundtrack[/COLOR]','PLFgquLnL59akYTGd40gT26IYoL2kuhQZO',1,art + 'Music.png')
        addDir('[COLOR blue]The Hip-Hop Index[/COLOR]','PLFgquLnL59amBBTCULGWSotJu2CkioYkj',1,art + 'Music.png')
        addDir('[COLOR blue]Top Tracks - Pop Music [/COLOR]','PLDcnymzs18LWrKzHmzrGH1JzLBqrHi3xQ',1,art + 'Music.png')
        addDir('[COLOR blue]Top Tracks - Hip Hop Music[/COLOR]','PLH6pfBXQXHEC2uDmDy5oi3tHW6X8kZ2Jo',1,art + 'Music.png')
        addDir('[COLOR blue]Top Tracks - Alternative Rock[/COLOR]','PL47oRh0-pTouthHPv6AbALWPvPJHlKiF7',1,art + 'Music.png')
        addDir('[COLOR blue]Top Tracks - Reggae[/COLOR]','PLYAYp5OI4lRLf_oZapf5T5RUZeUcF9eRO',1,art + 'Music.png')
        addDir('[COLOR blue]Top Tracks - Trap[/COLOR]','PLL4IwRtlZcbvbCM7OmXGtzNoSR0IyVT02',1,art + 'Music.png')
        addDir('[COLOR blue]Spotlight On: Global Discoveries [/COLOR]','PLFgquLnL59an78ZI25rXfkTnpkrLFVXJ8',1,art + 'Music.png')
        addDir('[COLOR blue]Top Tracks - Country[/COLOR]','PLvLX2y1VZ-tFJCfRG7hi_OjIAyCriNUT2',1,art + 'Music.png')
        addDir('[COLOR blue]The Country Index[/COLOR]','PLFgquLnL59amI45Go39kM7ha2evwjOxzs',1,art + 'Music.png')
        addDir('[COLOR blue]Top Tracks - Pop Rock[/COLOR]','PLr8RdoI29cXIlkmTAQDgOuwBhDh3yJDBQ',1,art + 'Music.png')
        addDir('[COLOR blue]Top Tracks - R&B[/COLOR]','PLFRSDckdQc1th9sUu8hpV1pIbjjBgRmDw',1,art + 'Music.png')
        addDir('[COLOR blue]Spotlight On: Dance Off[/COLOR]','PLFgquLnL59am3gKxgT7Tvw-CMAlT4lQiC',1,art + 'Music.png')
        addDir('[COLOR blue]Spotlight On: Surreal and Unreal[/COLOR]','PLFgquLnL59akoZ1GetztyRuu1jtSwOvMi',1,art + 'Music.png')
        addDir('[COLOR blue]Top Tracks - Asian Music[/COLOR]','PL0zQrw6ZA60Z6JT4lFH-lAq5AfDnO2-aE',1,art + 'Music.png')
        addDir('[COLOR blue]Top Tracks - Mexican Music[/COLOR]','PLXupg6NyTvTxw5-_rzIsBgqJ2tysQFYt5',1,art + 'Music.png')
        addDir('[COLOR blue]Top Tracks - Soul[/COLOR]','PLQog_FHUHAFUDDQPOTeAWSHwzFV1Zz5PZ',1,art + 'Music.png')
        addDir('[COLOR blue]The Indie Index[/COLOR]','PLFgquLnL59amVPzpNpN5bNLcZCld7JfI8',1,art + 'Music.png')
        addDir('[COLOR blue]On the Rise[/COLOR]','PLFgquLnL59ak5gmnz28ZiMd59ryeTPXjT',1,art + 'Music.png')
        addDir('[COLOR blue]Top Tracks - Rhythm & Blues[/COLOR]','PLWNXn_iQ2yrKzFcUarHPdC4c_LPm-kjQy',1,art + 'Music.png')
        addDir('[COLOR blue]Top Tracks - Christian Music[/COLOR]','PLLMA7Sh3JsOQQFAtj1no-_keicrqjEZDm',1,art + 'Music.png')
        addDir('[COLOR blue]Top Tracks - Hard Rock[/COLOR]','PL9NMEBQcQqlzwlwLWRz5DMowimCk88FJk',1,art + 'Music.png') 
        addDir('[COLOR blue]Top Tracks - Heavy Metal[/COLOR]','PLfY-m4YMsF-OM1zG80pMguej_Ufm8t0VC',1,art + 'Music.png')
        addDir('[COLOR blue]Top Tracks - Classical Music[/COLOR]','PLVXq77mXV53-Np39jM456si2PeTrEm9Mj',1,art + 'Music.png')
        addDir('[COLOR blue]PlayLists[/COLOR]','url',10,art + 'PlayLists.png')
        logo = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.YouMusic','logo.png'))
        xbmcgui.Dialog().notification('YouTube Music is brought to you','In association with TvAddons',logo,5000,False)
        

def PlayLists():
        addDir('[COLOR blue]Just-Released Music[/COLOR]','PLrEnWoR732-D67iteOI6DPdJH1opjAuJt',1,art + 'Music.png')
        addDir('[COLOR blue]Billboard Top Songs 2015[/COLOR]','PL55713C70BA91BD6E',1,art + 'Music.png')
        addDir('[COLOR blue]Popular Music[/COLOR]','PLFgquLnL59alCl_2TQvOiD5Vgm1hCaGSI',1,art + 'Music.png')
        addDir('[COLOR blue]80s & 90s Rock[/COLOR]','PL3485902CC4FB6C67',1,art + 'Music.png')
        addDir('[COLOR blue]Greatest Hits Of The 70s[/COLOR]','PLGBuKfnErZlAkaUUy57-mR97f8SBgMNHh',1,art + 'Music.png')
        addDir('[COLOR blue]60s Classic Hits[/COLOR]','PLuK6flVU_Aj5EJ9Pp-C9N7XA0YJr_GrJI',1,art + 'Music.png')
        addDir('[COLOR blue]50s Classic Hits[/COLOR]','PLuK6flVU_Aj45QZ_A5ld0-pP3CIkoNQDk',1,art + 'Music.png')
        addDir('[COLOR blue]Hottest Country Songs 2016[/COLOR]','PLi7ihgkEws7RB7W89lEjK2qvItmbyLBLl',1,art + 'Music.png')
        addDir('[COLOR blue]Country Music Mix[/COLOR]','PLnpWcMv6bu2X0xfAD6Kt-MgIIFOCNb067',1,art + 'Music.png')
        addDir('[COLOR blue]Hot Country Songs[/COLOR]','PL2BN1Zd8U_MsyMeK8r9Vdv1lnQGtoJaSa',1,art + 'Music.png')
        addDir('[COLOR blue]Country Radio Mix 2000 - 2014[/COLOR]','PLh__qJ1ro4JgQI6aAgk5dduKLZUGr1Tiw',1,art + 'Music.png')
        addDir('[COLOR blue]90s Country Music[/COLOR]','PLCEE7B2A4B9C9BCE7',1,art + 'Music.png')
        addDir('[COLOR blue]80s Country Music[/COLOR]','PL04199B0AF6C7C9F8',1,art + 'Music.png')


def get_params():
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


params=get_params()
url=None
name=None
mode=None
iconimage=None
page = None
token = None

try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except:
	try: 
		mode=params["mode"]
	except: pass
try: iconimage=urllib.unquote_plus(params["iconimage"])
except: pass
try: token=urllib.unquote_plus(params["token"])
except: pass
try: page=int(params["page"])
except: page = 1

print ("Mode: "+str(mode))
print ("URL: "+str(url))
print ("Name: "+str(name))
print ("iconimage: "+str(iconimage))
print ("Page: "+str(page))
print ("Token: "+str(token))

		
def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def create_directory(dir_path, dir_name=None):
    if dir_name:
        dir_path = os.path.join(dir_path, dir_name)
    dir_path = dir_path.strip()
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return dir_path

if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
       
elif mode==1:
        return_youtubevideos(name,url,token,page)

elif mode==5: 
        play_youtube_video(url)

elif mode==6:
        mark_as_watched(url)

elif mode==7:
        removed_watched(url)

elif mode==8:
        add_to_bookmarks(url)

elif mode==9:
        remove_from_bookmarks(url)
		
elif mode==10:
        print ""+url
        PlayLists()
	

xbmcplugin.endOfDirectory(int(sys.argv[1]))
