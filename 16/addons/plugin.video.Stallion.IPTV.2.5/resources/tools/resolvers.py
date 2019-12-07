# -*- coding: utf-8 -*-
#------------------------------------------------------------
# BassFox - Kodi Add-on 
# Plugin multimedia para el add-on
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a las librerías de Jesús (www.mimediacenter.info)


import os
import sys
import urllib
import urllib2
import re
import string
import shutil
import zipfile
import time
import urlparse
import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin
import scrapertools, plugintools, unwise, unpackerjs, requests

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")

from __main__ import *

art = addonPath + "/art/"



def allmyvideos(params):
    plugintools.log('[%s %s] Allmyvideos %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    url_fixed = page_url.split("/")
    url_fixed = 'http://www.allmyvideos.net/' +  'embed-' + url_fixed[3] +  '.html'
    plugintools.log("url_fixed= "+url_fixed)

    # Leemos el código web
    headers = {'user-agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14'}
    r = requests.get(page_url, headers=headers)
    data = r.text    

    if "<b>File Not Found</b>" in data or "<b>Archivo no encontrado</b>" in data or '<b class="err">Deleted' in data or '<b class="err">Removed' in data or '<font class="err">No such' in data:
        xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Bassfox', "Archivo borrado!", 3 , art+'icon.png'))

    else:
        # Normaliza la URL
        videoid = page_url.replace("http://allmyvideos.net/","").replace("https://allmyvideos.net/","").strip()
        page_url = "http://allmyvideos.net/embed-"+videoid+"-728x400.html"
        #data = scrapertools.cache_page(page_url)
        r = requests.get(page_url, headers=headers)
        data = r.text

        if "File was banned" in data:
            #data = scrapertools.cache_page(page_url,post="op=download1&usr_login=&id="+videoid+"&fname=&referer=&method_free=1&x=147&y=25")
            payload = {'op': 'download1', 'usr_login': '', 'id': videoid, 'fname': '', 'referer': '', 'method_free': '1', 'x': '147', 'y': '25'}
            r = requests.get(page_url, params=payload)
            data = r.text            

        # Extrae la URL
        match = re.compile('"file" : "(.+?)",').findall(data)
        media_url = ""
        if len(match) > 0:
            for tempurl in match:
                if not tempurl.endswith(".png") and not tempurl.endswith(".srt"):
                    media_url = tempurl
                    print media_url

            if media_url == "":
                media_url = match[0]
                print media_url

        if media_url!="":
            media_url+= "&direct=false"
            plugintools.log("media_url= "+media_url)
            plugintools.play_resolved_url(media_url)
        
        



def streamcloud(params):
    plugintools.log('[%s %s]Streamcloud %s' % (addonName, addonVersion, repr(params)))

    url = params.get("url")

    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)
    plugintools.log("data= "+body)

    # Barra de progreso para la espera de 10 segundos
    progreso = xbmcgui.DialogProgress()
    progreso.create("Bassfox", "Abriendo Streamcloud..." , url )

    i = 13000
    j = 0
    percent = 0
    while j <= 13000 :
        percent = ((j + ( 13000 / 10.0 )) / i)*100
        xbmc.sleep(i/10)  # 10% = 1,3 segundos
        j = j + ( 13000 / 10.0 )
        msg = "Espera unos segundos, por favor... "
        percent = int(round(percent))
        print percent
        progreso.update(percent, "" , msg, "")
        

    progreso.close()
    
    media_url = plugintools.find_single_match(body , 'file\: "([^"]+)"')
    
    if media_url == "":
        op = plugintools.find_single_match(body,'<input type="hidden" name="op" value="([^"]+)"')
        usr_login = ""
        id = plugintools.find_single_match(body,'<input type="hidden" name="id" value="([^"]+)"')
        fname = plugintools.find_single_match(body,'<input type="hidden" name="fname" value="([^"]+)"')
        referer = plugintools.find_single_match(body,'<input type="hidden" name="referer" value="([^"]*)"')
        hashstring = plugintools.find_single_match(body,'<input type="hidden" name="hash" value="([^"]*)"')
        imhuman = plugintools.find_single_match(body,'<input type="submit" name="imhuman".*?value="([^"]+)">').replace(" ","+")

        post = "op="+op+"&usr_login="+usr_login+"&id="+id+"&fname="+fname+"&referer="+referer+"&hash="+hashstring+"&imhuman="+imhuman
        request_headers.append(["Referer",url])
        body,response_headers = plugintools.read_body_and_headers(url, post=post, headers=request_headers)
        plugintools.log("data= "+body)
        

        # Extrae la URL
        media_url = plugintools.find_single_match( body , 'file\: "([^"]+)"' )
        plugintools.log("media_url= "+media_url)
        plugintools.play_resolved_url(media_url)

        if 'id="justanotice"' in body:
            plugintools.log("[streamcloud.py] data="+body)
            plugintools.log("[streamcloud.py] Ha saltado el detector de adblock")
            return -1

  

def playedto(params):
    plugintools.log('[%s %s] Played.to %s' % (addonName, addonVersion, repr(params)))

    url = params.get("url")
    url = url.split("/")
    url_fixed = "http://played.to/embed-" + url[3] +  "-640x360.html"
    plugintools.log("url_fixed= "+url_fixed)

    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    body,response_headers = plugintools.read_body_and_headers(url_fixed, headers=request_headers)
    body = body.strip()
    
    if body == "<center>This video has been deleted. We apologize for the inconvenience.</center>":
        xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Bassfox', "Enlace borrado...", 3 , art+'icon.png'))
    elif body.find("Removed for copyright infringement") >= 0:
        xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Bassfox', "Removed for copyright infringement", 3 , art+'icon.png'))
    else:
        r = re.findall('file(.+?)\n', body)

        for entry in r:
            entry = entry.replace('",', "")
            entry = entry.replace('"', "")
            entry = entry.replace(': ', "")
            entry = entry.strip()
            plugintools.log("vamos= "+entry)
            if entry.endswith("flv"):
                plugintools.play_resolved_url(entry)
                xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Bassfox', "Resolviendo enlace...", 3 , art+'icon.png'))
                params["url"]=entry
                plugintools.log("URL= "+entry)



def vidspot(params):
    plugintools.log('[%s %s] Vidspot %s' % (addonName, addonVersion, repr(params)))
    
    url = params.get("url")
    url = url.split("/")
    url_fixed = 'http://www.vidspot.net/' +  'embed-' + url[3] +  '.html'
    plugintools.log("url_fixed= "+url_fixed)

    # Leemos el código web
    headers = {'user-agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14'}
    r = requests.get(url_fixed, headers=headers)
    body = r.text

    try:
        if body.find("File was deleted") >= 0:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Bassfox', "Archivo borrado", 3 , art+'icon.png'))
        else:
            r = re.findall('"file" : "(.+?)"', body)
            for entry in r:
                plugintools.log("vamos= "+entry)
                if entry.endswith("mp4?v2"):
                    url = entry + '&direct=false'
                    params["url"]=url
                    plugintools.log("url= "+url)
                    plugintools.play_resolved_url(url)
                    xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Bassfox', "Resolviendo enlace...", 3 , art+'icon.png'))
    except:
            pass


				
def vk(params):
    plugintools.log('[%s %s] Vk %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    #url = url.replace('http://', 'https://')
    #data = data.replace("amp;", "")
    #data = scrapertools.cache_page(page_url)
    data = plugintools.read(page_url)
    plugintools.log("data= "+data)

    if "This video has been removed from public access" in data:
        xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Bassfox', "Archivo borrado!", 3 , art+'icon.png'))
    else:
        #data = scrapertools.cache_page(page_url.replace("amp;",""))
        data = plugintools.read(page_url.replace("amp;",""))
        plugintools.log("data= "+data)
        videourl = ""
        match = plugintools.find_single_match(data, r'vkid=([^\&]+)\&')
        print match
        vkid = ""

        # Lee la página y extrae el ID del vídeo
        data2 = data.replace("\\","")
        patron = '"vkid":"([^"]+)"'
        matches = re.compile(patron,re.DOTALL).findall(data2)
        if len(matches)>0:
            vkid = matches[0]
        else:
            plugintools.log("No encontró vkid")

        plugintools.log("vkid="+vkid)

        # Extrae los parámetros del vídeo y añade las calidades a la lista
        patron  = "var video_host = '([^']+)'.*?"
        patron += "var video_uid = '([^']+)'.*?"
        patron += "var video_vtag = '([^']+)'.*?"
        patron += "var video_no_flv = ([^;]+);.*?"
        patron += "var video_max_hd = '([^']+)'"
        matches = re.compile(patron,re.DOTALL).findall(data)
        print matches

        if len(matches)>0:
            #01:44:52 T:2957156352  NOTICE: video_host=http://cs509601.vk.com/, video_uid=149623387, video_vtag=1108941f4c, video_no_flv=1, video_max_hd=1

            video_host = matches[0][0]
            video_uid = matches[0][1]
            video_vtag = matches[0][2]
            video_no_flv = matches[0][3]
            video_max_hd = matches[0][4]
            
        else:
            #{"uid":"97482389","vid":"161509127\",\"oid\":\"97482389\","host":"507214",\"vtag\":\"99bca9d028\",\"ltag\":\"l_26f55018\",\"vkid\":\"161509127\",\"md_title\":\"El Libro de La Selva - 1967 - tetelx - spanish\",\"md_author\":\"Tetelx Tete\",\"hd\":1,\"no_flv\":1,\"hd_def\":-1,\"dbg_on\":0,\"t\":\"\",\"thumb\":\"http:\\\/\\\/cs507214.vkontakte.ru\\\/u97482389\\\/video\\\/l_26f55018.jpg\",\"hash\":\"3a576695e9f0bfe3093eb21239bd322f\",\"hash2\":\"be750b8971933dd6\",\"is_vk\":\"1\",\"is_ext\":\"0\",\"lang_add\":\"Add to My Videos\",\"lang_share\":\"Share\",\"lang_like\":\"Like\",\"lang_volume_on\":\"Unmute\",\"lang_volume_off\":\"Mute\",\"lang_volume\":\"Volume\",\"lang_hdsd\":\"Change Video Quality\",\"lang_fullscreen\":\"Full Screen\",\"lang_window\":\"Minimize\",\"lang_rotate\":\"Rotate\",\"video_play_hd\":\"Watch in HD\",\"video_stop_loading\":\"Stop Download\",\"video_player_version\":\"VK Video Player\",\"video_player_author\":\"Author - Alexey Kharkov\",\"goto_orig_video\":\"Go to Video\",\"video_get_video_code\":\"Copy vdeo code\",\"video_load_error\":\"The video has not uploaded yet or the server is not available\",\"video_get_current_url\":\"Copy frame link\",\"nologo\":1,\"liked\":0,\"add_hash\":\"67cd39a080ad6e0ad7\",\"added\":1,\"use_p2p\":0,\"p2p_group_id\":\"fb2d8cfdcbea4f3c\"}
            #01:46:05 T:2955558912  NOTICE: video_host=507214, video_uid=97482389, video_vtag=99bca9d028, video_no_flv=1, video_max_hd=1
            data2 = data.replace("\\","")
            video_host = scrapertools.get_match(data2,'"host":"([^"]+)"')
            video_uid = scrapertools.get_match(data2,'"uid":"([^"]+)"')
            video_vtag = scrapertools.get_match(data2,'"vtag":"([^"]+)"')
            video_no_flv = scrapertools.get_match(data2,'"no_flv":([0-9]+)')
            video_max_hd = scrapertools.get_match(data2,'"hd":([0-9]+)')
            
            if not video_host.startswith("http://"):
                video_host = "http://cs"+video_host+".vk.com/"

        plugintools.log("video_host="+video_host+", video_uid="+video_uid+", video_vtag="+video_vtag+", video_no_flv="+video_no_flv+", video_max_hd="+video_max_hd)

        video_urls = []

        if video_no_flv.strip() == "0" and video_uid != "0":
            tipo = "flv"
            if "http://" in video_host:
                videourl = "%s/u%s/video/%s.%s" % (video_host,video_uid,video_vtag,tipo)
            else:
                videourl = "http://%s/u%s/video/%s.%s" % (video_host,video_uid,video_vtag,tipo)
            
            # Lo añade a la lista
            video_urls.append( ["FLV [vk]",videourl])

        elif video_uid== "0" and vkid != "":     #http://447.gt3.vkadre.ru/assets/videos/2638f17ddd39-75081019.vk.flv 
            tipo = "flv"
            if "http://" in video_host:
                videourl = "%s/assets/videos/%s%s.vk.%s" % (video_host,video_vtag,vkid,tipo)
            else:
                videourl = "http://%s/assets/videos/%s%s.vk.%s" % (video_host,video_vtag,vkid,tipo)
            
            # Lo añade a la lista
            video_urls.append( ["FLV [vk]",videourl])
            
        else:                                   #http://cs12385.vkontakte.ru/u88260894/video/d09802a95b.360.mp4
            #Se reproducirá el stream encontrado de mayor calidad
            if video_max_hd=="3":
                plugintools.log("Vamos a por el vídeo 720p")
                if video_host.endswith("/"):
                    videourl = "%su%s/videos/%s.%s" % (video_host,video_uid,video_vtag,"720.mp4")
                else:
                    videourl = "%s/u%s/videos/%s.%s" % (video_host,video_uid,video_vtag,"720.mp4")
                plugintools.log("videourl= "+videourl)
            elif video_max_hd=="2":
                plugintools.log("Vamos a por el vídeo 480p")
                if video_host.endswith("/"):
                    videourl = "%su%s/videos/%s.%s" % (video_host,video_uid,video_vtag,"480.mp4")
                else:
                    videourl = "%s/u%s/videos/%s.%s" % (video_host,video_uid,video_vtag,"480.mp4")
                plugintools.log("videourl= "+videourl)
            elif video_max_hd=="1":
                plugintools.log("Vamos a por el vídeo 360p")
                if video_host.endswith("/"):
                    videourl = "%su%s/videos/%s.%s" % (video_host,video_uid,video_vtag,"360.mp4")
                else:
                    videourl = "%s/u%s/videos/%s.%s" % (video_host,video_uid,video_vtag,"360.mp4")
                plugintools.log("videourl= "+videourl) 
                
        plugintools.play_resolved_url(videourl)
        plugintools.log("videourl= "+videourl)





def nowvideo(params):
    plugintools.log('[%s %s] Nowvideo %s' % (addonName, addonVersion, repr(params)))

    data = plugintools.read(params.get("url"))
    #data = data.replace("amp;", "")
    
    if "The file is being converted" in data:
        xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Bassfox', "El archivo está en proceso", 3 , art+'icon.png'))
    elif "no longer exists" in data:
        xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Bassfox', "El archivo ha sido borrado", 3 , art+'icon.png'))        
    else:
        #plugintools.log("data= "+data)
        domain = plugintools.find_single_match(data, 'flashvars.domain="([^"]+)')
        video_id = plugintools.find_single_match(data, 'flashvars.file="([^"]+)')
        filekey = plugintools.find_single_match(data, 'flashvars.filekey=([^;]+)')

        # En la página nos da el token de esta forma (siendo fkzd el filekey): var fkzd="83.47.1.12-8d68210314d70fb6506817762b0d495e";

        token_txt = 'var '+filekey
        #plugintools.log("token_txt= "+token_txt)
        token = plugintools.find_single_match(data, filekey+'=\"([^"]+)')
        token = token.replace(".","%2E").replace("-","%2D")
        
        #plugintools.log("domain= "+domain)   
        #plugintools.log("video_id= "+video_id)
        #plugintools.log("filekey= "+filekey)
        #plugintools.log("token= "+token)
        
        if video_id == "":
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Bassfox', "Error!", 3 , art+'icon.png'))
        else:
            #http://www.nowvideo.sx/api/player.api.php?user=undefined&pass=undefined&cid3=undefined&numOfErrors=0&cid2=undefined&key=83%2E47%2E1%2E12%2D8d68210314d70fb6506817762b0d495e&file=b5c8c44fc706f&cid=1
            url = 'http://www.nowvideo.sx/api/player.api.php?user=undefined&pass=undefined&cid3=undefined&numOfErrors=0&cid2=undefined&key=' + token + '&file=' + video_id + '&cid=1'

            # Vamos a lanzar una petición HTTP de esa URL
            referer = 'http://www.nowvideo.sx/video/b5c8c44fc706f'
            request_headers=[]
            request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
            request_headers.append(["Referer",referer])
            body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)
            # plugintools.log("data= "+body)
            # body= url=http://s173.coolcdn.ch/dl/04318aa973a3320b8ced6734f0c20da3/5440513e/ffe369cb0656c0b8de31f6ef353bcff192.flv&title=The.Black.Rider.Revelation.Road.2014.DVDRip.X264.AC3PLAYNOW.mkv%26asdasdas&site_url=http://www.nowvideo.sx/video/b5c8c44fc706f&seekparm=&enablelimit=0

            body = body.replace("url=", "")
            body = body.split("&")

            if len(body) >= 0:
                print 'body',body
                url = body[0]
                plugintools.play_resolved_url(url)
                xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Bassfox', "Cargando vídeo...", 1 , art+'icon.png'))
            else:
                xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Bassfox', "Error!", 3 , art+'icon.png'))                

         
''' En el navegador...

        flashvars.domain="http://www.nowvideo.sx";
        flashvars.file="b5c8c44fc706f";
        flashvars.filekey=fkzd;
        flashvars.advURL="0";
        flashvars.autoplay="false";
        flashvars.cid="1";

'''


def tumi(params):
    plugintools.log('[%s %s] Tumi %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    data = scrapertools.cache_page(page_url)
    
    if "Video is processing now" in data:
        xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Bassfox', "El archivo está en proceso", 3 , art+'icon.png'))       
    else:
        try:
            x = scrapertools.find_single_match(data, "\|type\|(.*?)\|file\|").replace("||","|").split("|")
            n = scrapertools.find_single_match(data, "//k.j.h.([0-9]+):g/p/v.o")

            printf = "http://%s.%s.%s.%s:%s/%s/%s.%s"
            if n:
                url = printf % (x[3], x[2], x[1],    n, x[0], x[8], "v", x[7])
            else:
                url = printf % (x[4], x[3], x[2], x[1], x[0], x[9], "v", x[8])
        except:
            url = scrapertools.find_single_match(data, "file:'([^']+)'")

        plugintools.log("url_final= "+url)
        plugintools.play_resolved_url(url)


            
def veehd(params):
    plugintools.log('[%s %s] VeeHD %s' % (addonName, addonVersion, repr(params)))
    
    uname = plugintools.get_setting("veehd_user")
    pword = plugintools.get_setting("veehd_pword")
    if uname == '' or pword == '':
        xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Bassfox', "Debes configurar el identificador para Veehd.com", 3 , art+'icon.png'))
        return
    
    url = params.get("url")
    url_login = 'http://veehd.com/login'
    
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer",url])
    
    post = {'ref': url, 'uname': uname, 'pword': pword, 'submit': 'Login', 'terms': 'on'}
    post = urllib.urlencode(post)
    
    body,response_headers = plugintools.read_body_and_headers(url_login, post=post, headers=request_headers, follow_redirects=True)
    vpi = plugintools.find_single_match(body, '"/(vpi.+?h=.+?)"')
    
    if not vpi:
        if 'type="submit" value="Login" name="submit"' in body:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Bassfox', "Error al identificarse en Veehd.com", 3 , art+'icon.png'))
        else:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Bassfox', "Error buscando el video en Veehd.com", 3 , art+'icon.png'))            
        return
    
    req = urllib2.Request('http://veehd.com/'+vpi)
    for header in request_headers:
        req.add_header(header[0], header[1]) # User-Agent
    response = urllib2.urlopen(req)
    body = response.read()
    response.close()

    va = plugintools.find_single_match(body, '"/(va/.+?)"')
    if va:
        req = urllib2.Request('http://veehd.com/'+va)
        for header in request_headers:
            req.add_header(header[0], header[1]) # User-Agent
        urllib2.urlopen(req)

    req = urllib2.Request('http://veehd.com/'+vpi)
    for header in request_headers:
        req.add_header(header[0], header[1]) # User-Agent
    response = urllib2.urlopen(req)
    body = response.read()
    response.close()

    video_url = False
    if 'application/x-shockwave-flash' in body:
        video_url = urllib.unquote(plugintools.find_single_match(body, '"url":"(.+?)"'))
    elif 'video/divx' in body:
        video_url = urllib.unquote(plugintools.find_single_match(body, 'type="video/divx"\s+src="(.+?)"'))

    if not video_url:
        xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Bassfox', "Error abriendo el video en Veehd.com", 3 , art+'icon.png'))
        return

    plugintools.log("video_url= "+video_url)
    plugintools.play_resolved_url(video_url)

    



def streaminto(params):
    plugintools.log('[%s %s] streaminto %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    if page_url.startswith("http://streamin.to/embed-") == False:
        videoid = plugintools.find_single_match(page_url,"streamin.to/([a-z0-9A-Z]+)")
        page_url = "http://streamin.to/embed-"+videoid+".html"

    plugintools.log("page_url= "+page_url)
    
    # Leemos el código web
    headers = {'user-agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14'}
    r = requests.get(page_url, headers=headers)
    data = r.text
        
    plugintools.log("data= "+data)
    if data == "File was deleted":
        xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Bassfox', "Archivo borrado!", 3 , art+'icon.png'))        
    else:        
        # TODO: Si "video not found" en data, mostrar mensaje "Archivo borrado!"
        patron_flv = 'file: "([^"]+)"'    
        patron_jpg = 'image: "(http://[^/]+/)'    
        try:
            host = scrapertools.get_match(data, patron_jpg)
            plugintools.log("[streaminto.py] host="+host)
            flv_url = scrapertools.get_match(data, patron_flv)
            plugintools.log("[streaminto.py] flv_url="+flv_url)
            flv = host+flv_url.split("=")[1]+"/v.flv"
            plugintools.log("[streaminto.py] flv="+flv)
            page_url = flv
        except:
            plugintools.log("[streaminto] opcion 2")
            op = plugintools.find_single_match(data,'<input type="hidden" name="op" value="([^"]+)"')
            plugintools.log("[streaminto] op="+op)
            usr_login = ""
            id = plugintools.find_single_match(data,'<input type="hidden" name="id" value="([^"]+)"')
            plugintools.log("[streaminto] id="+id)
            fname = plugintools.find_single_match(data,'<input type="hidden" name="fname" value="([^"]+)"')
            plugintools.log("[streaminto] fname="+fname)
            referer = plugintools.find_single_match(data,'<input type="hidden" name="referer" value="([^"]*)"')
            plugintools.log("[streaminto] referer="+referer)
            hashstring = plugintools.find_single_match(data,'<input type="hidden" name="hash" value="([^"]*)"')
            plugintools.log("[streaminto] hashstring="+hashstring)
            imhuman = plugintools.find_single_match(data,'<input type="submit" name="imhuman".*?value="([^"]+)"').replace(" ","+")
            plugintools.log("[streaminto] imhuman="+imhuman)
            
            import time
            time.sleep(10)
            
            # Lo pide una segunda vez, como si hubieras hecho click en el banner
            #op=download1&usr_login=&id=z3nnqbspjyne&fname=Coriolanus_DVDrip_Castellano_by_ARKONADA.avi&referer=&hash=nmnt74bh4dihf4zzkxfmw3ztykyfxb24&imhuman=Continue+to+Video
            post = "op="+op+"&usr_login="+usr_login+"&id="+id+"&fname="+fname+"&referer="+referer+"&hash="+hashstring+"&imhuman="+imhuman
            request_headers.append(["Referer",page_url])
            data_video = plugintools.read_body_and_headers( page_url , post=post, headers=request_headers )
            data_video = data_video[0]
            rtmp = plugintools.find_single_match(data_video, 'streamer: "([^"]+)"')
            print 'rtmp',rtmp
            video_id = plugintools.find_single_match(data_video, 'file: "([^"]+)"')
            print 'video_id',video_id
            swf = plugintools.find_single_match(data_video, 'src: "(.*?)"')
            print 'swf',swf
            page_url = rtmp+' swfUrl='+swf + ' playpath='+video_id+"/v.flv"  

        plugintools.play_resolved_url(page_url)    
    


def powvideo(params):
    plugintools.log('[%s %s] Powvideo %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")

    # Leemos el código web
    headers = [['User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14']]
    data = scrapertools.cache_page( page_url , headers=headers )      
    #plugintools.log("data= "+data)

    '''
    <input type="hidden" name="op" value="download1">
    <input type="hidden" name="usr_login" value="">
    <input type="hidden" name="id" value="auoxxtvyquoy">
    <input type="hidden" name="fname" value="Star.Trek.Into.Darkness.2013.HD.m720p.LAT.avi">
    <input type="hidden" name="referer" value="">
    <input type="hidden" name="hash" value="1624-83-46-1377796069-b5e6b8f9759d080a3667adad637f00ac">
    <input type="submit" name="imhuman" value="Continue to Video" id="btn_download">
    '''
    option = plugintools.find_single_match(data,'<input type="hidden" name="op" value="(down[^"]+)')
    usr_login = ""
    id = plugintools.find_single_match(data,'<input type="hidden" name="id" value="([^"]+)')
    fname = plugintools.find_single_match(data,'<input type="hidden" name="fname" value="([^"]+)')
    referer = plugintools.find_single_match(data,'<input type="hidden" name="referer" value="([^"]*)')
    hashvalue = plugintools.find_single_match(data,'<input type="hidden" name="hash" value="([^"]*)')
    submitbutton = plugintools.find_single_match(data,'<input type="submit" name="imhuman" value="([^"]+)').replace(" ","+")    
    time.sleep(30)

    # Lo pide una segunda vez, como si hubieras hecho click en el banner
    #op=download1&usr_login=&id=auoxxtvyquoy&fname=Star.Trek.Into.Darkness.2013.HD.m720p.LAT.avi&referer=&hash=1624-83-46-1377796019-c2b422f91da55d12737567a14ea3dffe&imhuman=Continue+to+Video
    #op=search&usr_login=&id=auoxxtvyquoy&fname=Star.Trek.Into.Darkness.2013.HD.m720p.LAT.avi&referer=&hash=1624-83-46-1377796398-8020e5629f50ff2d7b7de99b55bdb177&imhuman=Continue+to+Video
    post = "op="+option+"&usr_login="+usr_login+"&id="+id+"&fname="+fname+"&referer="+referer+"&hash="+hashvalue+"&imhuman="+submitbutton
    plugintools.log("post= "+post)
    headers.append(["Referer",page_url])
    data = scrapertools.cache_page(page_url, post=post, headers=headers)    
    plugintools.log("data= "+data)
    
    # Extrae la URL
    data = plugintools.find_single_match(data,"<script type='text/javascript'>(.*?)</script>")
    plugintools.log("data= "+data)
    from resources.tools.jsunpack import *
    data = unpack(data)    
    data = data.replace("\\","")
    
    media_url = plugintools.find_single_match(data,"file:'([^']+)'")
    plugintools.log("media_url= "+media_url)
    plugintools.play_resolved_url(media_url)



def mailru(params):
    plugintools.log('[%s %s] Mail.ru %s' % (addonName, addonVersion, repr(params)))
    
    url = params.get("url")
    url = url.replace('/my.mail.ru/video/', '/api.video.mail.ru/videos/embed/')
    url = url.replace('/videoapi.my.mail.ru/', '/api.video.mail.ru/')
    plugintools.log("URL = "+url)
    result = getUrl(url).result
    plugintools.log("result= "+result)    
    url = re.compile('metadataUrl":"(.+?)"').findall(result)[0]
    cookie = getUrl(url, output='cookie').result
    h = "|Cookie=%s" % urllib.quote(cookie)
    result = getUrl(url).result
    plugintools.log("result= "+result)
    #result = json.loads(result)
    result = data['videos']
    url = []
    url += [{'quality': '1080p', 'url': i['url'] + h} for i in result if i['key'] == '1080p']
    url += [{'quality': 'HD', 'url': i['url'] + h} for i in result if i['key'] == '720p']
    url += [{'quality': 'SD', 'url': i['url'] + h} for i in result if not (i['key'] == '1080p' or i ['key'] == '720p')]
    #if url == []: return
    plugintools.play_resolved_url(url)



def mediafire(params):
    plugintools.log('[%s %s] Mediafire %s' % (addonName, addonVersion, repr(params)))

    # Solicitud de página web
    url = params.get("url")
    data = plugintools.read(url)

    # Espera un segundo y vuelve a cargar
    plugintools.log("[Bassfox] Espere un segundo...")
    import time
    time.sleep(1)
    data = plugintools.read(url)
    plugintools.log("data= "+data)
    pattern = 'kNO \= "([^"]+)"'
    matches = re.compile(pattern,re.DOTALL).findall(data)
    for entry in matches:
        plugintools.log("entry= "+entry)
    # Tipo 1 - http://www.mediafire.com/download.php?4ddm5ddriajn2yo
    pattern = 'mediafire.com/download.php\?([a-z0-9]+)'
    matches = re.compile(pattern,re.DOTALL).findall(data)    
    for entry in matches:
        if entry != "":
            url = 'http://www.mediafire.com/?'+entry
            plugintools.log("URL Tipo 1 = "+url)
            
'''
    # Tipo 2 - http://www.mediafire.com/?4ckgjozbfid
    pattern  = 'http://www.mediafire.com/\?([a-z0-9]+)'
    matches = re.compile(pattern,re.DOTALL).findall(data)
    for entry in matches:
        if entry != "":
            url = 'http://www.mediafire.com/?'+entry
            plugintools.log("URL Tipo 2 = "+url)
        
    # Tipo 3 - http://www.mediafire.com/file/c0ama0jzxk6pbjl
    pattern  = 'http://www.mediafire.com/file/([a-z0-9]+)'
    plugintools.log("[mediafire.py] find_videos #"+pattern+"#")
    matches = re.compile(pattern,re.DOTALL).findall(data)
    for entry in matches:
        if entry != "":
            url = 'http://www.mediafire.com/?'+entry
            plugintools.log("URL Tipo 3 = "+url)

'''
            

def novamov(params):
    plugintools.log('[%s %s] Novamov %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    media_id = page_url.replace("http://www.novamov.com/video/", "").strip()

    # Comprobamos que existe el vídeo
    data = scrapertools.cache_page(page_url)    
    if "This file no longer exists on our servers" in data:
        xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Bassfox', "No existe vídeo en Novamov", 3 , art+'icon.png'))
    elif "is being converted" in data:
        xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Bassfox', "Vídeo no disponible", 3 , art+'icon.png'))

    plugintools.log("[novamov.py] get_video_url(page_url='%s')" % page_url)

    html = scrapertools.cache_page(page_url)
    html = unwise.unwise_process(html)
    filekey = unwise.resolve_var(html, "flashvars.filekey")

    #get stream url from api
    api = 'http://www.novamov.com/api/player.api.php?key=%s&file=%s' % (filekey, media_id)
    data = scrapertools.cache_page(api)
    data = data.replace("url=", "").strip()
    data = data.split("&title=")
    url_final = data[0]+'?client=FLASH'
    # http://s91.coolcdn.ch/dl/dfdb3d051c3e71db62cf8379259ffcbd/552254ab/ff2e9e3dc0489c213e868d43e74bd1b356.flv?client=FLASH
    # http://s181.coolcdn.ch/dl/003aa7721702b4db5598faf880d76386/55225401/fffadbdfcba93c7515995141bcf8b1a95a.flv&title=The.Walking.Dead.S05E13.Vose%26asdasdas&site_http://www.novamov.com/video/f664cf727c58c&seekparm=&enablelimit=0]

    plugintools.log("url_final= "+url_final)
    plugintools.play_resolved_url(url_final)


def gamovideo(params):
    plugintools.log('[%s %s] Gamovideo %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    headers = [['User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14']]
    data = scrapertools.cache_page( page_url , headers=headers )
    
    if "is no longer available" in data:
        xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Bassfox', "Archivo borrado!", 3 , art+'icon.png'))
    else:
        headers = [['User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14']]
        data = scrapertools.cache_page( page_url , headers=headers )
    try:
        '''
        <input type="hidden" name="op" value="download1">
        <input type="hidden" name="usr_login" value="">
        <input type="hidden" name="id" value="auoxxtvyquoy">
        <input type="hidden" name="fname" value="Star.Trek.Into.Darkness.2013.HD.m720p.LAT.avi">
        <input type="hidden" name="referer" value="">
        <input type="hidden" name="hash" value="1624-83-46-1377796069-b5e6b8f9759d080a3667adad637f00ac">
        <input type="submit" name="imhuman" value="Continue to Video" id="btn_download">
        '''
        op = scrapertools.get_match(data,'<input type="hidden" name="op" value="(down[^"]+)"')
        usr_login = ""
        id = scrapertools.get_match(data,'<input type="hidden" name="id" value="([^"]+)"')
        fname = scrapertools.get_match(data,'<input type="hidden" name="fname" value="([^"]+)"')
        referer = scrapertools.get_match(data,'<input type="hidden" name="referer"\s+value="([^"]*)"')
        hashvalue = scrapertools.get_match(data,'<input type="hidden" name="hash" value="([^"]*)"')
        submitbutton = scrapertools.get_match(data,'<input type="submit" name="imhuman" value="([^"]+)"').replace(" ","+")

        import time
        time.sleep(5)

        # Lo pide una segunda vez, como si hubieras hecho click en el banner
        #op=download1&usr_login=&id=auoxxtvyquoy&fname=Star.Trek.Into.Darkness.2013.HD.m720p.LAT.avi&referer=&hash=1624-83-46-1377796019-c2b422f91da55d12737567a14ea3dffe&imhuman=Continue+to+Video
        #op=search&usr_login=&id=auoxxtvyquoy&fname=Star.Trek.Into.Darkness.2013.HD.m720p.LAT.avi&referer=&hash=1624-83-46-1377796398-8020e5629f50ff2d7b7de99b55bdb177&imhuman=Continue+to+Video
        post = "op="+op+"&usr_login="+usr_login+"&id="+id+"&fname="+fname+"&referer="+referer+"&hash="+hashvalue+"&imhuman="+submitbutton
        headers.append(["Referer",page_url])
        data = scrapertools.cache_page( page_url , post=post, headers=headers )
        plugintools.log("data="+data)
    except:
        import traceback
        traceback.print_exc()
    
    # Extrae la URL
    plugintools.log("data="+data)
    data = scrapertools.find_single_match(data,"<script type='text/javascript'>(.*?)</script>")
    plugintools.log("data="+data)
    data = unpackerjs.unpackjs(data)
    plugintools.log("data="+data)
    # ('jwplayer("vplayer").setup({playlist:[{image:"http://192.99.35.229:8777/i/01/00048/ibw5pte06up4.jpg",sources:[{file:"rtmp://192.99.35.229:1935/vod?h=7ax23yxze4pskjwff5zcce7uyyqvxf5ullx3urse54oyq2tepqiko5s6xsoq/mp4:35/3779312894_n.mp4?h=7ax23yxze4pskjwff5zcce7uyyqvxf5ullx3urse54oyq2tepqiko5s6xsoq"},{file:"35/3779312894_n.mp4?h=7ax23yxze4pskjwff5zcce7uyyqvxf5ullx3urse54oyq2tepqiko5s6xsoq"}],tracks:[]}],rtmp:{bufferlength:5},height:528,primary:"flash",width:950,captions:{color:\'#FFFFFF\',fontSize:15,fontFamily:"Verdana"}});var vvplay;var tt243542=0;var p0243542=0;jwplayer().onTime(function(x){if(p0243542>0)tt243542+=x.position-p0243542;p0243542=x.position;if(0!=0&&tt243542>=0){p0243542=-1;jwplayer().stop();jwplayer().setFullscreen(false);$(\'#play_limit_box\').show();$(\'div.video_ad\').show()}});jwplayer().onSeek(function(x){p0243542=-1});jwplayer().onPlay(function(x){doPlay(x)});jwplayer().onComplete(function(){$(\'div.video_ad\').show()});function doPlay(x){$(\'div.video_ad\').hide();if(vvplay)return;vvplay=1;}',,355,

    data = data.replace('file:"rtmp://', 'streamer:"')
    pfile = plugintools.find_single_match(data,'file\s*\:\s*"([^"]+)"') 
    pstreamer = 'rtmp://'+plugintools.find_single_match(data,'streamer\s*\:\s*"([^"]+)"')
    media_url = pstreamer + " playpath=" + pfile.replace("playpath=", "").strip()
    plugintools.log("media_url= "+media_url)
    plugintools.play_resolved_url(media_url)



def moevideos(params):
    plugintools.log('[%s %s] Moevideos %s' % (addonName, addonVersion, repr(params)))

    # No existe / borrado: http://www.moevideos.net/online/27991
    page_url = params.get("url")
    data = scrapertools.cache_page(page_url)
    plugintools.log("data= "+data)
    if "<span class='tabular'>No existe</span>" in data:
        return False,"No existe o ha sido borrado de moevideos"
    else:
        # Existe: http://www.moevideos.net/online/18998
        patron  = "<span class='tabular'>([^>]+)</span>"
        headers = []
        headers.append(['User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14'])
        data = scrapertools.cache_page( page_url , headers=headers )            
        # Descarga el script (no sirve para nada, excepto las cookies)
        headers.append(['Referer',page_url])
        post = "id=1&enviar2=ver+video"
        data = scrapertools.cache_page( page_url , post=post, headers=headers )
        ### Modificado 12-6-2014
        #code = scrapertools.get_match(data,'flashvars\="file\=([^"]+)"')
        #<iframe width="860" height="440" src="http://moevideo.net/framevideo/16363.1856374b43bbd40c7f8d2b25b8e5?width=860&height=440" frameborder="0" allowfullscreen ></iframe>
        code = scrapertools.get_match(data,'<iframe width="860" height="440" src="http://moevideo.net/framevideo/([^\?]+)\?width=860\&height=440" frameborder="0" allowfullscreen ></iframe>')
        plugintools.log("code="+code)

        # API de letitbit
        headers2 = []
        headers2.append(['User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14'])
        ### Modificado 12-6-2014
        url = "http://api.letitbit.net"
        #url = "http://api.moevideo.net"
        #post = "r=%5B%22tVL0gjqo5%22%2C%5B%22preview%2Fflv%5Fimage%22%2C%7B%22uid%22%3A%2272871%2E71f6541e64b0eda8da727a79424d%22%7D%5D%2C%5B%22preview%2Fflv%5Flink%22%2C%7B%22uid%22%3A%2272871%2E71f6541e64b0eda8da727a79424d%22%7D%5D%5D"
        #post = "r=%5B%22tVL0gjqo5%22%2C%5B%22preview%2Fflv%5Fimage%22%2C%7B%22uid%22%3A%2212110%2E1424270cc192f8856e07d5ba179d%22%7D%5D%2C%5B%22preview%2Fflv%5Flink%22%2C%7B%22uid%22%3A%2212110%2E1424270cc192f8856e07d5ba179d%22%7D%5D%5D
        #post = "r=%5B%22tVL0gjqo5%22%2C%5B%22preview%2Fflv%5Fimage%22%2C%7B%22uid%22%3A%2268653%2E669cbb12a3b9ebee43ce14425d9e%22%7D%5D%2C%5B%22preview%2Fflv%5Flink%22%2C%7B%22uid%22%3A%2268653%2E669cbb12a3b9ebee43ce14425d9e%22%7D%5D%5D"
        post = 'r=["tVL0gjqo5",["preview/flv_image",{"uid":"'+code+'"}],["preview/flv_link",{"uid":"'+code+'"}]]'
        data = scrapertools.cache_page(url,headers=headers2,post=post)
        plugintools.log("data="+data)
        if ',"not_found"' in data:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Bassfox', "Archivo borrado!", 3 , art+'icon.png'))
        else:
            data = data.replace("\\","")
            plugintools.log("data="+data)
            patron = '"link"\:"([^"]+)"'
            matches = re.compile(patron,re.DOTALL).findall(data)
            video_url = matches[0]+"?ref=www.moevideos.net|User-Agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:15.0) Gecko/20100101 Firefox/15.0.1&Range=bytes:0-"
            plugintools.log("[moevideos.py] video_url="+video_url)

            video_urls = []
            video_urls.append( [ scrapertools.get_filename_from_url(video_url)[-4:] + " [moevideos]",video_url ] )
            plugintools.play_resolved_url(video_url[1])
     


def movshare(params):
    plugintools.log('[%s %s] Movshare %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    data = scrapertools.cache_page(page_url)
    
    if "This file no longer exists on our servers" in data:
        xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Bassfox', "Archivo borrado!", 3 , art+'icon.png'))
    else:
        videoid = scrapertools.get_match(page_url,"http://www.movshare.net/video/([a-z0-9]+)")
        video_urls = []
        # Descarga la página
        headers = []
        headers.append( ['User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'] )
        data = scrapertools.cache_page(page_url , headers = headers)
    
        # La vuelve a descargar, como si hubieras hecho click en el botón
        #html = scrapertools.cache_page(page_url , headers = headers)
        filekey = plugintools.find_single_match(data,'flashvars.filekey="([^"]+)"')
            
        #get stream url from api
        api = 'http://www.movshare.net/api/player.api.php?key=%s&file=%s' % (filekey, videoid)
        headers.append( ['Referer',page_url] )

        html = scrapertools.cache_page(api,headers=headers)
        plugintools.log("html="+html)
        stream_url = plugintools.find_single_match(html,'url=(.+?)&title')

        if stream_url!="":
            video_urls.append( [ scrapertools.get_filename_from_url(stream_url)[-4:]+" [movshare]" , stream_url ] )

        for video_url in video_urls:
            plugintools.log("[movshare.py] %s - %s" % (video_url[0],video_url[1]))

        plugintools.log("url_final= "+video_url[1])
        plugintools.play_resolved_url(video_url[1])


def movreel(params):
    plugintools.log('[%s %s] Movreel %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    video_urls = []

    data = scrapertools.cache_page(page_url)

    op = plugintools.find_single_match(data,'<input type="hidden" name="op" value="([^"]+)">')
    file_code = plugintools.find_single_match(data,'<input type="hidden" name="file_code" value="([^"]+)">')
    w = plugintools.find_single_match(data,'<input type="hidden" name="w" value="([^"]+)">')
    h = plugintools.find_single_match(data,'<input type="hidden" name="h" value="([^"]+)">')
    method_free = plugintools.find_single_match(data,'<input type="submit" name="method_free" value="([^"]+)">')

    #op=video_embed&file_code=yrwo5dotp1xy&w=600&h=400&method_free=Close+Ad+and+Watch+as+Free+User
    #post = 'op=video_embed&file_code='+file_code+'+&w='+w+'&h='+h+'$method_free='+method_free
    post = urllib.urlencode( {"op":op,"file_code":file_code,"w":w,"h":h,"method_free":method_free} )
    print 'post',post

    data = scrapertools.cache_page(page_url,post=post)
    #plugintools.log("data="+data)
    data = unpackerjs.unpackjs(data)
    plugintools.log("data="+data)

    media_url = plugintools.find_single_match(data,'file\:"([^"]+)"')
    video_urls.append( [ scrapertools.get_filename_from_url(media_url)[-4:]+" [movreel]",media_url])

    for video_url in video_urls:
        plugintools.log("[movreel.py] %s - %s" % (video_url[0],video_url[1]))

    print video_urls
    # PENDIENTE DE RESOLVER URL !!!


   
def videobam(params):
    plugintools.log('[%s %s] Videobam %s' % (addonName, addonVersion, repr(params)))
    page_url = params.get("url")
    data = scrapertools.cache_page(page_url)
    videourl = ""
    match = ""
    if "Video is processing" in data:
        xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Bassfox', "Archivo no disponible temporalmente!", 3 , art+'icon.png'))
    else:
        patronHD = " high: '([^']+)'"
        matches = re.compile(patronHD,re.DOTALL).findall(data)
        for match in matches:
            videourl = match
            plugintools.log("Videobam HQ :"+match)

        if videourl == "":
            patronSD= " low: '([^']+)'"
            matches = re.compile(patronSD,re.DOTALL).findall(data)
            for match in matches:
                videourl = match
                plugintools.log("Videobam LQ :"+match)

            if match == "":
                if len(matches)==0:
                    # "scaling":"fit","url":"http:\/\/f10.videobam.com\/storage\/11\/videos\/a\/aa\/AaUsV\/encoded.mp4
                    patron = '[\W]scaling[\W]:[\W]fit[\W],[\W]url"\:"([^"]+)"'
                    matches = re.compile(patron,re.DOTALL).findall(data)
                    for match in matches:
                        videourl = match.replace('\/','/')
                        videourl = urllib.unquote(videourl)
                        plugintools.log("Videobam scaling: "+videourl)
                        if videourl != "":
                            plugintools.play_resolved_url(videourl)

        else:
            
            plugintools.play_resolved_url(videourl)


def vimeo(params):
    plugintools.log("servers.vimeo get_video_url(page_url='%s')" % repr(params))

    page_url = params.get("url")
    
    headers = []
    headers.append( ['User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'] )
    data = scrapertools.cache_page(page_url, headers=headers)

    '''
    <div class="player" style="background-image: url(http://b.vimeocdn.com/ts/433/562/433562952_960.jpg);" id="player_1_53086fb0f413f" data-config-url="http://player.vimeo.com/v2/video/63073570/config?autoplay=0&amp;byline=0&amp;bypass_privacy=1&amp;context=clip.main&amp;default_to_hd=1&amp;portrait=0&amp;title=0&amp;s=4268c7772994be693b480b75b5d84452f3e81f96" data-fallback-url="//player.vimeo.com/v2/video/63073570/fallback?js"
    '''
    url = scrapertools.find_single_match(data,'<div class="player" style="[^"]+" id="[^"]+" data-config-url="([^"]+)"')
    url = url.replace("&amp;","&")
    headers.append( ['Referer',page_url] )
    data = scrapertools.cache_page(url, headers=headers)
    json_object = jsontools.load_json(data)
    '''
    http://player.vimeo.com/v2/video/63073570/config?autoplay=0&byline=0&bypass_privacy=1&context=clip.main&default_to_hd=1&portrait=0&title=0&s=4268c7772994be693b480b75b5d84452f3e81f96

    > GET /v2/video/63073570/config?autoplay=0&byline=0&bypass_privacy=1&context=clip.main&default_to_hd=1&portrait=0&title=0&s=4268c7772994be693b480b75b5d84452f3e81f96 HTTP/1.1
    > User-Agent: curl/7.24.0 (x86_64-apple-darwin12.0) libcurl/7.24.0 OpenSSL/0.9.8y zlib/1.2.5
    > Host: player.vimeo.com
    > Accept: */*
    > 
    < HTTP/1.1 200 OK
    < Expires: Sun, 23 02 2014 09:39:32 GMT
    < Vary: Origin, Accept-Encoding
    < Etag: "009d88dc9b151e402faf10efb7ba4cabe0412385"
    < P3p: CP="This is not a P3P policy! See http://vimeo.com/privacy"
    < Content-Type: application/json
    < Transfer-Encoding: chunked
    < Date: Sat, 22 Feb 2014 09:39:32 GMT
    < X-Varnish: 1162931632
    < Age: 0
    < Via: 1.1 varnish
    < Cache-Control: no-store, no-cache, must-revalidate, post-check=0, pre-check=0
    < X-Player2: 1
    < X-Varnish-Cache: 0
    < nnCoection: close
    < X-VServer: 10.90.128.193
    < 
    * Connection #0 to host player.vimeo.com left intact
    {"cdn_url":"http://a.vimeocdn.com","view":1,"request":{"files":{"h264":{"hd":{"profile":113,"origin":"ns3.pdl","url":"http://pdl.vimeocdn.com/72437/773/155150233.mp4?token2=1393065072_197f0ca458049c7217e9e8969c373af1&aksessionid=358994b3a75767bb","height":720,"width":1280,"id":155150233,"bitrate":2658,"availability":60},"sd":{"profile":112,"origin":"ns3.pdl","url":"http://pdl.vimeocdn.com/44925/440/155100150.mp4?token2=1393065072_cd5b62387758a46798e02dbd0b19bd3e&aksessionid=56c93283ac081129","height":360,"width":640,"id":155100150,"bitrate":860,"availability":60}},"hls":{"all":"http://av70.hls.vimeocdn.com/i/,44925/440/155100150,72437/773/155150233,.mp4.csmil/master.m3u8?primaryToken=1393065072_fe1a557fd7460bc8409bf09960614694","hd":"http://av70.hls.vimeocdn.com/i/,72437/773/155150233,.mp4.csmil/master.m3u8?primaryToken=1393065072_8ba190ee7643f318c75dc265a14b750d"},"codecs":["h264"]},"ga_account":"UA-76641-35","timestamp":1393061972,"expires":3100,"prefix":"/v2","session":"9d8f0ce5a2de113df027f1f1d2428648","cookie":{"scaling":1,"volume":1.0,"hd":null,"captions":null},"cookie_domain":".vimeo.com","referrer":null,"conviva_account":"c3.Vimeo","flags":{"login":1,"preload_video":1,"plays":1,"partials":1,"conviva":1},"build":{"player":"d854ba1a","js":"2.3.7"},"urls":{"zeroclip_swf":"http://a.vimeocdn.com/p/external/zeroclipboard/ZeroClipboard.swf","js":"http://a.vimeocdn.com/p/2.3.7/js/player.js","proxy":"https://secure-a.vimeocdn.com/p/2.3.7/proxy.html","conviva":"http://livepassdl.conviva.com/ver/2.72.0.13589/LivePass.js","flideo":"http://a.vimeocdn.com/p/flash/flideo/1.0.3b10/flideo.swf","canvas_js":"http://a.vimeocdn.com/p/2.3.7/js/player.canvas.js","moog":"http://a.vimeocdn.com/p/flash/moogaloop/6.0.7/moogaloop.swf?clip_id=63073570","conviva_service":"http://livepass.conviva.com","moog_js":"http://a.vimeocdn.com/p/2.3.7/js/moogaloop.js","zeroclip_js":"http://a.vimeocdn.com/p/external/zeroclipboard/ZeroClipboard-patch.js","css":"http://a.vimeocdn.com/p/2.3.7/css/player.css"},"signature":"67ef54c1e894448dd7c38e7da8a3bdba"},"player_url":"player.vimeo.com","video":{"allow_hd":1,"height":720,"owner":{"account_type":"basic","name":"Menna Fit\u00e9","img":"http://b.vimeocdn.com/ps/446/326/4463264_75.jpg","url":"http://vimeo.com/user10601457","img_2x":"http://b.vimeocdn.com/ps/446/326/4463264_300.jpg","id":10601457},"thumbs":{"1280":"http://b.vimeocdn.com/ts/433/562/433562952_1280.jpg","960":"http://b.vimeocdn.com/ts/433/562/433562952_960.jpg","640":"http://b.vimeocdn.com/ts/433/562/433562952_640.jpg"},"duration":2200,"id":63073570,"hd":1,"embed_code":"<iframe src=\"//player.vimeo.com/video/63073570\" width=\"500\" height=\"281\" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>","default_to_hd":1,"title":"No le digas a la Mama que me he ido a Mongolia en Moto","url":"http://vimeo.com/63073570","privacy":"anybody","share_url":"http://vimeo.com/63073570","width":1280,"embed_permission":"public","fps":25.0},"build":{"player":"d854ba1a","rpc":"dev"},"embed":{"player_id":null,"outro":"nothing","api":2,"context":"clip.main","time":0,"color":"00adef","settings":{"fullscreen":1,"instant_sidedock":1,"byline":0,"like":1,"playbar":1,"title":0,"color":1,"branding":0,"share":1,"scaling":1,"logo":0,"info_on_pause":0,"watch_later":1,"portrait":0,"embed":1,"badge":0,"volume":1},"on_site":1,"loop":0,"autoplay":0},"vimeo_url":"vimeo.com","user":{"liked":0,"account_type":"none","logged_in":0,"owner":0,"watch_later":0,"id":0,"mod":0}}* Closing connection #0
    '''

    media_url = json_object['request']['files']['h264']['hd']['url']
    video_urls.append( [ "HD [vimeo]",media_url ] )    
    media_url = json_object['request']['files']['h264']['sd']['url']
    video_urls.append( [ "SD [vimeo]",media_url ] )          
                        
