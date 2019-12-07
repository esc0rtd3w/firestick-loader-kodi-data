# -*- coding: utf-8 -*-

import re
import urllib2
import HTMLParser
import urllib,urlparse
import xbmcgui
import xbmcplugin
import xbmcaddon
import requests
from BeautifulSoup import BeautifulSoup as bs
from utils.webutils import *
import json


try:
    from addon.common.addon import Addon

    from addon.common.net import Net
except:
    print 'Failed to import script.module.addon.common'
    xbmcgui.Dialog().ok("Import Failure", "Failed to import addon.common", "A component needed by P2P Sport is missing on your system", "Please visit www.tvaddons.ag.com for support")

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])
params=urlparse.parse_qs(sys.argv[2][1:])

addon = Addon('plugin.video.p2psport', sys.argv)
AddonPath = addon.get_path()


def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

mode = args.get('mode', None)

my_addon = xbmcaddon.Addon()

def cleanex(text):
    text = text.replace(u'\xda','U').replace(u'\xc9','E').replace(u'\xd3','O').replace(u'\xd1','N').replace(u'\xcd','I').replace(u'\xc1','A').replace(u'\xf8','o').replace(u'\xf1','n')
    return text

def read_url(url):
    net = Net()

    html=net.http_GET(url).content

    h = HTMLParser.HTMLParser()
    html = h.unescape(html)
    return html

def play_sop(url,name):
    if 'sop://'in url:
        url='plugin://program.plexus/?mode=2&url=%s&name=%s'%(url,name.replace(' ','+'))
        xbmc.Player().play(url)
    else:
        resolve_roja(url,name)
#############################################################################################################################################################3
#############################################################################################################################################################3
#############################################################################################################################################################3
def get_ttv():
    url='http://www.acesportstream.com'
    url=read_url(url)
    soup=bs(url)
    channels1=soup.find('div',{'id':'hd'}).findAll('a')
    channels2=soup.find('div',{'id':'blue'}).findAll('a')


    for channel in channels1:
        link=channel['href']
        img=channel.find('img')['src']
        name=clean(cleanex(channel['title']))

        url = build_url({'mode': 'open_ttv_stream','url':link, 'name':name.encode('ascii','ignore')})
        li = xbmcgui.ListItem('%s'%name, iconImage=img)
        li.setProperty('IsPlayable', 'true')

        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
    for channel in channels2:
        link=channel['href']
        img=channel.find('img')['src']
        name=clean(cleanex(channel['title']))

        url = build_url({'mode': 'open_ttv_stream','url':link, 'name':name.encode('ascii','ignore')})
        li = xbmcgui.ListItem('%s'%name, iconImage=img)
        li.setProperty('IsPlayable', 'true')

        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)


    xbmcplugin.endOfDirectory(addon_handle)

def ttv_sport():
    base_url = 'http://super-pomoyka.us.to/trash/ttv-list/ttv.m3u'
    source = read_url(base_url)
    if source:
        match= re.compile("#EXTINF:-1,Sky Sports News \(.+?\)\n(.*)").findall(source)
        if match:
            name='Sky Sports News'
            ace=match[0]
            url='plugin://program.plexus/?mode=1&url=%s&name=%s'%(ace,name.replace(' ','+'))
            li = xbmcgui.ListItem('%s'%name, iconImage='http://addons.tvaddons.ag/cache/images/bc591d6d5ec442d4ddb43a347a8be6_icon.png')
            li.setProperty('IsPlayable', 'true')
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

        match= re.compile("#EXTINF:-1,(.+?)\(Спорт\)\n(.*)").findall(source)
        for titulo,acestream in match:
            name=titulo
            ace=acestream
            clean = re.compile("\((.+?)\)").findall(name)
            for categorie in clean:
                name = name.replace("(" + categorie +")","")
                ace=acestream
            url='plugin://program.plexus/?mode=1&url=%s&name=%s'%(ace,name.replace(' ','+'))
            li = xbmcgui.ListItem('%s'%name, iconImage='http://addons.tvaddons.ag/cache/images/bc591d6d5ec442d4ddb43a347a8be6_icon.png')
            li.setProperty('IsPlayable', 'true')
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
    xbmcplugin.endOfDirectory(addon_handle)
def open_ttv_stream(url,name):

    resolve_roja(url,name)


def get_ttv_cat(cat,tag):
	url="http://super-pomoyka.us.to/trash/ttv-list/ttv.m3u"
	html=read_url(url)
	dicty=json.loads(tag)
	channels=dicty[cat]
	for channel in channels:
		name=channel[0]
		ace=channel[1]
		url='plugin://program.plexus/?mode=1&url=%s&name=%s'%(ace,name.replace(' ','+'))
		li = xbmcgui.ListItem('%s'%name, iconImage='http://addons.tvaddons.ag/cache/images/bc591d6d5ec442d4ddb43a347a8be6_icon.png')
		li.setProperty('IsPlayable', 'true')
		xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
	xbmcplugin.endOfDirectory(addon_handle)


def ttv_cats():
	dict_torrent = {}
	url="http://super-pomoyka.us.to/trash/ttv-list/ttv.m3u"
	html_source=read_url(url)
	match = re.compile('#EXTINF:-1,(.+?)\n(.*)').findall(html_source)
	for title, acehash in match:
    		channel_name = re.compile('(.+?) \(').findall(title)
    		match_cat = re.compile('\((.+?)\)').findall(title)
    		for i in xrange(0,len(match_cat)):
    			if match_cat[i] == "Для взрослых" :
    				pass
    			elif match_cat[i] == "Ночной канал" :
                                pass
    			else:
                		categorie = russiandictionary(match_cat[i])

                		if categorie not in dict_torrent.keys():
                			try:
            					dict_torrent[categorie] = [(channel_name[0],acehash)]
            				except: pass
            			else:
            				try:
            					dict_torrent[categorie].append((channel_name[0],acehash))
            				except: pass
	for cat in dict_torrent.keys():
		url = build_url({'mode': 'open_ttv_cat','channels':json.dumps(dict_torrent),'cat':cat})
		li = xbmcgui.ListItem(cat,iconImage='http://addons.tvaddons.ag/cache/images/bc591d6d5ec442d4ddb43a347a8be6_icon.png')
		xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
				listitem=li, isFolder=True)


	xbmcplugin.endOfDirectory(addon_handle)

def russiandictionary(string):
	if string == "Eng": return "English"
	elif string == "Спорт": return "Sport"
	elif string == "Новостные": return "News"
	elif string == "Свадебный": return "Wedding"
	elif string == "Общие": return "General"
	elif string == "Познавательные": return "Educational"
	elif string == "СНГ": return "СIС"
	elif string == "Мужские": return "Men"
	elif string == "Ukraine": return "Ukraine"
 	elif string == "резерв": return "Reserved"
 	elif string == "Донецк": return "Donetsk"
 	elif string == "Региональные": return "Regional"
 	elif string == "Для взрослых": return "Adult"
 	elif string == "TV21": return string
 	elif string == "Украина": return "Ukraine"
 	elif string == "Детские": return "Kids"
 	elif string == "Фильмы": return "Movies"
 	elif string == "Ночной канал": return "Night Channels"
 	elif string == "Европа": return "Europe"
 	elif string == "укр": return "Ukraine"
 	elif string == "Музыка": return "Music"
 	elif string == "Религиозные": return "Religious"
 	elif string == "Развлекательные": return "Entertainment"
	elif string == "украина": return "Ukraine"
	elif string == "Казахстан": return "Kazakstan"
	elif string=='Екатеринбург': return 'Ekaterinburg'
 	else: return string

#############################################################################################################################################################3
#############################################################################################################################################################3
#############################################################################################################################################################3

def play_arena(url,name):
    headers = {
        "Cookie" : "beget=begetok; has_js=1;"
    }

    html = requests.get(url,headers=headers).text
    match = re.compile('this.loadPlayer\("(.+?)"').findall(html)[0]
    try:
    	url='plugin://program.plexus/?mode=1&url=acestream://%s&name=%s'%(match,urllib.quote_plus(name))
    except:
    	url='plugin://program.plexus/?mode=1&url=acestream://%s&name=%s'%(match,name.replace(' ','+'))

    xbmc.Player().play(url)
def play_arena_sop(url,name):
    headers = {
        "Cookie" : "beget=begetok; has_js=1;"
    }

    html = requests.get(url,headers=headers).text
    match = re.compile('sop://(.+?)"').findall(html)[0]
    url='plugin://program.plexus/?mode=2&url=sop://%s&name=%s'%(match,urllib.quote_plus(name))
    xbmc.Player().play(url)

def arenavision_schedule():
    url='http://arenavision.in/agenda'
    headers = {
        "Cookie" : "beget=begetok; has_js=1;"
    }
    try:
        source = requests.get(url,headers=headers).text
    except: source=""
    if source:
        match = re.findall('Bruselas(.*?)</footer>', source, re.DOTALL)
        for event in match:
            eventmatch = re.compile('(\d+)/(\d+)/(\d+) (.+?):(.+?) CET (.+?)<').findall(event)
            for dia,mes,year,hour,minute,evento in eventmatch:

                import datetime
                from utils import pytzimp
                d = pytzimp.timezone(str(pytzimp.timezone('Europe/Madrid'))).localize(datetime.datetime(2000 + int(year), int(mes), int(dia), hour=int(hour), minute=int(minute)))
                timezona= addon.get_setting('timezone_new')
                my_location=pytzimp.timezone(pytzimp.all_timezones[int(timezona)])
                convertido=d.astimezone(my_location)
                fmt = "%d-%m-%y %H:%M"
                time=convertido.strftime(fmt)
                time='[COLOR orange]('+str(time)+')[/COLOR] '
                try:
                    index=evento.index(')')
                    event_name = clean(cleanex(evento[:index+1]))
                    evento=evento.replace(event_name,'')
                    channels=re.compile('AV(\d+)').findall(evento)
                except:
                    index=evento.index('/AV')
                    channels=re.compile('AV(\d+)').findall(evento)
                    event_name = clean(cleanex(evento[:index]))
                    evento=evento.replace(event_name,'')







                url = build_url({'mode': 'av_open','channels': channels, 'name':event_name})
                li = xbmcgui.ListItem(time + event_name,iconImage='http://kodi.altervista.org/wp-content/uploads/2015/07/arenavision.jpg')
                xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                           listitem=li, isFolder=True)
        xbmcplugin.endOfDirectory(addon_handle)

#############################################################################################################################################################3
#############################################################################################################################################################3
#############################################################################################################################################################3


def livefootballol():
    url='http://www.livefootballol.com/live-football-streaming.html'
    html=get_page_source(url)
    soup=bs(html)
    #items=re.compile('<li>\s*<div><img src=".+?" alt=".+?"/> (.+?) [(.+?)] <a href="(.+?)">(.+?)</a></div>\s*</li>')
    #time,league,link,name
    daty=soup.findAll('h3')
    lists=soup.findAll('list')
    for i in range(6):
        itel=daty[i]
        if 'CET' in itel.getText():
            date=itel.getText()
            index=date.index(',')+2
            date=date[index:]
            dates=date.split('/')
            day,month,year=dates[0],dates[1],dates[2].replace('CET','').strip()
            items=re.compile('<li>\s*<div><img src=".+?" alt=".+?"\s*\/>\s*(.+?)\s*\[(.+?)\]\s*<a\s*href="(.+?)"\s*(?:target="_blank"|)\s*>\s*(.+?)<\/a>').findall(str(lists[i]))
            for tem in items:
                time,league,link,name = tem[0],tem[1],tem[2],tem[3]
                time=time.split(':')
                hour,minute=time[0],time[1]
                import datetime
                from utils import pytzimp
                d = pytzimp.timezone(str(pytzimp.timezone('Europe/Berlin'))).localize(datetime.datetime(2000 + int(year), int(month), int(day), hour=int(hour), minute=int(minute)))
                timezona= addon.get_setting('timezone_new')
                my_location=pytzimp.timezone(pytzimp.all_timezones[int(timezona)])
                convertido=d.astimezone(my_location)
                fmt = "%d-%m-%y [COLOR green]%H:%M[/COLOR]"
                time=convertido.strftime(fmt)
                competition=league
                match=name

                title='([COLOR blue][B]%s[/B][/COLOR]) [B][COLOR orange]%s[/COLOR][/B] %s'%(time,match,competition)
                if 'streaming/' in link:
                    url = build_url({'mode': 'open_livefoot','url':link,'name':match})
                    li = xbmcgui.ListItem(title,iconImage='')
                    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)



    xbmcplugin.endOfDirectory(addon_handle)




def get_livefoot(url,name):
    names,links=[],[]
    html=read_url(url)
    soup=bs(html)
    tag=soup.find('div',{'id':'maininner'})
    tag=tag.find('div',{'class':'content clearfix'})
    trs=tag.findAll('tr')
    for item in trs:
        try:
            language=item.findAll('td')[0].getText()
            txt=item.findAll('td')[1].getText()
        except:
            language='[N/A]'
            txt=''
        if language=='':
            language='[N/A]'
        if 'acestream' in txt.lower() or 'sopcast' in txt.lower():
            link=item.findAll('td')[1].find('a')['href']
            title='%s %s'%(txt,language)
            links+=[link]
            names+=[title]
        else:
            pass

    if links!=[]:
        dialog = xbmcgui.Dialog()
        index = dialog.select('Select a channel:', names)

        if index>-1:
            name=names[index]
            url=links[index]

            play_livefoot(url,name)
    else:
        xbmcgui.Dialog().ok('No stream','No stream available yet!')


def play_livefoot(url,name):
    html=read_url(url)
    try:
        ace=re.compile('acestream://(.+?)"').findall(html)[0]
        url='plugin://program.plexus/?mode=1&url=acestream://%s&name=%s'%(ace,urllib.quote_plus(name))
        xbmc.Player().play(url)
    except:
        try:
            sop=re.compile('sop://(.+?)"').findall(html)[0]
            url='plugin://program.plexus/?mode=2&url=sop://%s&name=%s'%(sop,urllib.quote_plus(name))
            xbmc.Player().play(url)
        except:
            pass

def livefootF1():
    url='http://www.livefootballol.com/f1-steaming.html'
    html=read_url(url)
    soup=bs(html)
    table=soup.find('table',{'id':'customers'})
    trs=table.findAll('tr')

    competition=trs[0].findAll('td')[1].getText()
    date=trs[2].findAll('td')[1].getText()
    time=trs[4].findAll('td')[1].getText()
    title=competition+' ('+date+' '+time+')'
    li = xbmcgui.ListItem('[COLOR yellow]%s:[/COLOR]'%title)
    li.setProperty('IsPlayable', 'false')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=None,
                                    listitem=li)

    name=competition
    tag=soup.find('div',{'id':'maininner'})
    tag=tag.find('div',{'class':'content clearfix'})
    trs=tag.findAll('tr')
    for item in trs:
        try:
            language=item.findAll('td')[0].getText()
            txt=item.findAll('td')[1].getText()
        except:
            language='N/A'
            txt=''
        if language=='':
            language='N/A'
        if 'acestream' in txt.lower() or 'sopcast' in txt.lower():
            link=item.findAll('td')[1].find('a')['href']
            title='[COLOR yellow]--- %s [/COLOR][COLOR green](%s)[/COLOR]'%(language,txt)
            url = build_url({'mode': 'open_livefoot_stream','url':link,'name':name})
            li = xbmcgui.ListItem(title,iconImage='')
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
        else:
            pass
    xbmcplugin.endOfDirectory(addon_handle)

#############################################################################################################################################################3
#############################################################################################################################################################3
#############################################################################################################################################################3


def livefootballws_events():
    url='http://livefootball.ws'
    source = read_url(url)
    #except: source = ""; xbmcgui.Dialog().ok('No stream','No stream available!')

    if source:
        items = re.findall('<div class="base custom" align="center"(.*?)</div><br></div>', source, re.DOTALL)
        number_of_items= len(items)
        for item in reversed(items):
            data = re.compile('<div style="text-align: center;">(.+?)</div>').findall(item)
            try:
                check = re.compile(">.+? (.+?):(.+?)").findall(data[-1].replace("color:",""))
                if not check and "Online" not in data[-1]:pass
                else:
                    data_item = data[-1].replace("<strong>","").replace("</strong>","").replace('<span style="color: #008000;">','').replace("</span>","")
                    url = re.compile('<a href="(.+?)">').findall(item)
                    teams = re.compile('/.+?-(.+?).html').findall(url[0])
                    try:
                        match = re.compile('(.+?) (.+?) (.+?):(.*)').findall(data_item)
                        import datetime
                        from utils import pytzimp
                        timezona= addon.get_setting('timezone_new')
                        d = pytzimp.timezone(str(pytzimp.timezone('Europe/Athens'))).localize(datetime.datetime(2014, 6, int(match[0][0]), hour=int(match[0][2]), minute=int(match[0][3])))
                        my_place=pytzimp.timezone(pytzimp.all_timezones[int(timezona)])
                        convertido=d.astimezone(my_place)
                        fmt = "%d %H:%M"
                        time=convertido.strftime(fmt)
                        title="[B][COLOR orange]("+'Day'+time+")[/COLOR][/B] "+teams[0]
                        url = build_url({'mode': 'open_ws_stream','name':teams[0],'url':url[0]})
                        li = xbmcgui.ListItem(title,iconImage='')
                        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

                    except:

                        if '<span style="color: #000000;">' not in data_item:
                            data_item=data_item.replace('<strong style="font-size: 10.6666669845581px; text-align: center;">','')
                            title="[B][COLOR green]("+data_item+")[/COLOR][/B] "+teams[0]
                            url = build_url({'mode': 'open_ws_stream','name':teams[0],'url':url[0]})
                            li = xbmcgui.ListItem(title,iconImage='')
                            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
                        else: pass
            except: pass
        xbmcplugin.endOfDirectory(addon_handle)

def livefootballws_streams(url):
    names=[]
    links=[]
    try:
        source = read_url(url)
    except: source = "";
    if source:
        items = re.findall('<td style="text-align: center;">(.*?)</tr>', source, re.DOTALL)
        number_of_items = len(items)
        if items:
            for item in items:
                match =re.compile('href="(.+?)"').findall(item)
                if match:
                    if "sop://" or "torrentstream" or "acestream://" in match[-1]:
                        stream_quality = re.compile('>(.+?) kbps</td>').findall(item)
                        channel_info_arr = bs(item).getText()
                        try:
                            channel = channel_info_arr[-4].replace('<span style="text-align: center;">','').replace('</span>','')
                        except: channel = 'N/A'
                        if "sop://" in match[-1]:
                            try:
                                title=("[SopCast] "+channel+" ("+stream_quality[0]+' Kbps)').replace('] p',']')
                                url = match[-1]
                                names+=[title]
                                links+=[url]

                            except: pass
                        elif "acestream://" in match[-1]:
                            link = re.compile("acestream://(.*)").findall(match[-1])
                            try:
                                title=("[Acestream] "+channel.replace('<br />','')+" ("+stream_quality[0]+' Kbps)').replace('] p',']')
                                url='acestream://'+link[0]
                                names+=[title]
                                links+=[url]
                            except: pass
                        elif "torrentstream" in match[-1]:
                            link = re.compile("http://torrentstream.org/stream/test.php\?id=(.*)").findall(match[-1])
                            try:
                                title=("[Acestream] "+channel.replace('<br />','')+" ("+stream_quality[0]+' Kbps)').replace('] p',']')
                                url='acestream://'+link[0]
                                names+=[title]
                                links+=[url]
                            except: pass
                        else:pass
        else:
            xbmcgui.Dialog().ok('No stream','No stream available!')
            return

    if links!=[]:
        dialog = xbmcgui.Dialog()
        index = dialog.select('Select a channel:', names)

        if index>-1:
            name=names[index]
            url=links[index]

            play_sop(url,name)
    else:
        xbmcgui.Dialog().ok('No stream','No stream available yet!')

############################################################################################################################################################3
#############################################################################################################################################################3
#############################################################################################################################################################3

def rojadirecta_events():
  thumbnail='http://www.rojadirecta.me/static/roja.jpg'

  url='http://www.rojadirecta.me'
  try:
   source = read_url(url)

  except: source = ""
  if source:
    match = re.findall('<span class="(\d+)".*?<div class="menutitle".*?<span class="t">([^<]+)</span>(.*?)</div>',source,re.DOTALL)
    print match
    for id,time,eventtmp in match:
            try:

                import datetime
                from utils import pytzimp
                d = pytzimp.timezone(str(pytzimp.timezone('Europe/Madrid'))).localize(datetime.datetime(2014, 6, 7, hour=int(time.split(':')[0]), minute=int(time.split(':')[-1])))
                timezona= addon.get_setting('timezone_new')
                my_location=pytzimp.timezone(pytzimp.all_timezones[int(timezona)])
                convertido=d.astimezone(my_location)
                fmt = "%H:%M"
                time=convertido.strftime(fmt)
            except:
                pass
            eventnospanish = re.compile('<span class="es">(.+?)</span>').findall(eventtmp)
            if eventnospanish:
                for spanishtitle in eventnospanish:
                    eventtmp = eventtmp.replace('<span class="es">' + spanishtitle + '</span>','')
            eventclean=eventtmp.replace('<span class="en">','').replace('</span>','').replace(' ()','').replace('</time>','').replace('<span itemprop="name">','')
            matchdois = re.compile('(.*)<b>\s*(.*?)\s*</b>').findall(eventclean)
            for sport,event in matchdois:
                event=clean(cleanex(event))

                express = '<span class="submenu" id="sub' + id+ '">.*?</span>\s*</span>'
                streams = re.findall(express,source,re.DOTALL)
                for streamdata in streams:
                    p2pstream = re.compile('<td>P2P</td>\n.+?<td>([^<]*)</td>\n.+?<td>([^<]*)</td>\n.+?<td>([^<]*)</td>\n.+?<td>([^<]*)</td>\n.+?<td><b><a.+?href="(.+?)"').findall(streamdata)
                    already = False
                    for canal,language,tipo,qualidade,urltmp in p2pstream:
                        if "Sopcast" in tipo or "Acestream" in tipo:
                            if already == False:
                                title="[B][COLOR orange]"+time+ " - " + sport + " - " + event + "[/B][/COLOR]"
                                li = xbmcgui.ListItem(title,iconImage=thumbnail)
                                li.setProperty('IsPlayable', 'false')
                                xbmcplugin.addDirectoryItem(handle=addon_handle, url=None,
                                    listitem=li)
                                already = True
                            title="[B]["+tipo.replace("<","").replace(">","")+"][/B]-"+canal.replace("<","").replace(">","")+" - ("+language.replace("<","").replace(">","")+") - ("+qualidade.replace("<","").replace(">","")+" Kbs)"
                            try:
                                url = build_url({'mode': 'open_roja_stream','name':event,'url':urltmp})
                            except:
                                url = build_url({'mode': 'open_roja_stream','name':event.encode('ascii','ignore'),'url':urltmp})
                            li = xbmcgui.ListItem(title,iconImage=thumbnail)
                            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
                            p2pdirect = re.compile('<td>P2P</td><td></td><td></td><td>(.+?)</td><td></td><td>.+?href="(.+?)"').findall(streamdata)
                            for tipo,link in p2pdirect:
                                if tipo == "SopCast" and "sop://" in link:
                                    url='plugin://program.plexus/?mode=2&url=%s&name=%s'%(link,urllib.quote_plus(event))

                                    li = xbmcgui.ListItem('Sopcast (No info)', iconImage=thumbnail)
                                    li.setProperty('IsPlayable', 'true')
                                    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

    xbmcplugin.endOfDirectory(addon_handle)

def resolve_roja(url,name):
    if'serbia' in url:
        source = get_page_source(url)
        soup=bs(source)
        urls=soup.findAll('iframe')
        for urly in urls:
            if 'ttv.net' in urly['src']:
                url=urly['src']
                resolve_roja(url,name)
                return



    if "sop://" not in url and "acestream://" not in url:
        if "http://" not in url:
            url="http://"+url

        if 'arenavision' in url:
            headers = {
                "Cookie" : "beget=begetok; has_js=1;"
            }

            source = requests.get(url,headers=headers).text
        else:
            source = get_page_source(url)
        if 'click here..' in source.lower():
            try:
                url=re.compile('<a href="(.+?)">click here...').findall(source)[0]

                resolve_roja(url,name)
                return
            except:
            	pass
        elif 'iframe' in source:

        	soup=bs(source)
        	urls=soup.findAll('iframe')
        	for urly in urls:
        		try:
        			cc=urly['id']
        		except:
        			cc=''
        		if 'free' in urly['src'] or 'timeanddate' in urly['src']:
        			pass
        		else:
        			if (cc=='refresh' or cc=='ifi'):
        				url=url+ '/'+ urly['src']
        				resolve_roja(url,name)
        				return
	        		elif 'ttv.net' in urly['src']:
	        			url=urly['src']
	            		resolve_roja(url,name)
	            		return


        matchsop = re.compile('sop://(.+?)"').findall(source)
        if matchsop:
            url='plugin://program.plexus/?mode=2&url=sop://%s&name=%s'%(matchsop[0],urllib.quote_plus(name))
            xbmc.Player().play(url)
        else:
            match = re.compile('this.loadPlayer\("(.+?)"').findall(source)
            if match:
                url='plugin://program.plexus/?mode=1&url=%s&name=%s'%(match[0],urllib.quote_plus(name))
                xbmc.Player().play(url)
            else:
            	xbmcgui.Dialog().ok('No stream','No stream available!')
    elif "sop://" in url:
        url='plugin://program.plexus/?mode=2&url=sop://%s&name=%s'%(url,name.replace(' ','+'))
        xbmc.Player().play(url)
    elif "acestream://" in url:
        url='plugin://program.plexus/?mode=1&url=%s&name=%s'%(url,name.replace(' ','+'))
        xbmc.Player().play(url)
    else: xbmcgui.Dialog().ok('No stream','No stream available!')

#############################################################################################################################################################3
#############################################################################################################################################################3
#############################################################################################################################################################3
def one_ttv_cats():
	cats=['General','News','Entertainment','Baby','Movies','Sport','Cognitive','Music','Men','Regional','Religious','x','HD Channels','In Moderation']
	for i in range(len(cats)):
		if cats[i]!='x':
			tag='tcon_%s'%(i+1)
			title='%s'%(cats[i])
			url = build_url({'mode': 'open_1ttv_cat','tag':tag,'name':title})
			li = xbmcgui.ListItem(title,iconImage='http://s3.hostingkartinok.com/uploads/images/2013/06/6e4452212490ac0a66e358c97707ef77.png')
			xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
				listitem=li, isFolder=True)
	xbmcplugin.endOfDirectory(addon_handle)

def open_1ttv_cat(tag,name):
	url='http://1torrent.tv/channels.php'
	html=read_url(url)
	soup=bs(html)
	table=soup.find('div',{'id': tag})
	divs=table.findAll('div',{'class':'elem_small_channel_white_wrapper'})
	for item in divs:
		x=re.compile('<img src="(.+?)"').findall(str(item))[0]
		thumb='http://1torrent.tv'+ x
		channel=item.findAll('div',{'class':'cell'})[1].find('a').getText()
		link='http://1torrent.tv'+ item.findAll('div',{'class':'cell'})[1].find('a')['href']

		url = build_url({'mode': 'open_1ttv_channel','url':link})
		li = xbmcgui.ListItem(channel,iconImage=thumb)
		xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
			listitem=li, isFolder=True)
	xbmcplugin.endOfDirectory(addon_handle)

def open_1ttv_channel(url):
	html=read_url(url)
	soup=bs(html)
	name=soup.find('div',{'id':'cur_name'}).getText()

	play_arena(url,name)

#############################################################################################################################################################3
#############################################################################################################################################################3
#############################################################################################################################################################3


def all_live247():
    url='http://pilkalive.weebly.com/en.html'
    html=read_url(url)
    soup=bs(html)
    lis=soup.findAll('li')
    for li in lis:
        link=li.find('a')['href']
        name=li.getText().lstrip().rstrip()
        if '>' not in name and 'other' not in name.lower() and 'home' not in name.lower():
            url = build_url({'mode': 'open_247_stream','name':name,'url':link})
            li = xbmcgui.ListItem(name,iconImage='')
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)

def schedule247():
    import datetime
    import time
    i = datetime.datetime.now()
    day,month,year=i.day, i.month, i.year
    s="%s/%s/%s"%(day,month,year)
    time=time.mktime(datetime.datetime.strptime(s, "%d/%m/%Y").timetuple())
    time=str(time).replace('.0','')+'000'
    url='https://tockify.com/api/readEventView?calname=pilkalive&max=30&start-inclusive=true&startms='+time
    txt=json.loads(read_url(url))
    events=txt['events']
    for i in range (len(events)):
        time=events[i]['when']['start']['millis']
        time=str(time)[:-3]
        event=events[i]['content']['summary']['text']
        link=events[i]['content']['description']['text']

        ts = datetime.datetime.fromtimestamp(float(time))
        year,month,day,hour,minute=ts.strftime('%Y'),ts.strftime('%m'),ts.strftime('%d'),ts.strftime('%H'),ts.strftime('%M')
        from utils import pytzimp
        d = pytzimp.timezone(str(pytzimp.timezone('Europe/Madrid'))).localize(datetime.datetime(2000 + int(year), int(month), int(day), hour=int(hour), minute=int(minute)))
        timezona= addon.get_setting('timezone_new')
        my_location=pytzimp.timezone(pytzimp.all_timezones[int(timezona)])
        convertido=d.astimezone(my_location)
        fmt = "%d-%m-%y [COLOR green]%H:%M[/COLOR]"

        time=convertido.strftime(fmt)
        event=event[5:]
        title='([COLOR blue][B]%s[/B][/COLOR]) [B][COLOR orange]%s[/COLOR][/B]'%(time,event)
        url = build_url({'mode': 'open_247_event','url':link})
        li = xbmcgui.ListItem(title,iconImage='')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)

def open_247_event(url):
    soup=bs(url)
    a=soup.findAll('a')
    choice,urls=[],[]
    for link in a:
        url=link['href']
        name=link.getText().replace('(','').replace(')','')
        choice+=[name]
        urls+=[url]
    dialog = xbmcgui.Dialog()
    index = dialog.select('Select a channel:', choice)

    if index>-1:
        name=choice[index]
        url=urls[index]

        play247(url,name)


def play247(url,name):
    resolve_roja(url,name)
#############################################################################################################################################################3
#############################################################################################################################################################3
#############################################################################################################################################################3
def phace():
    url='http://shanghai.watchkodi.com/Sections/Sports/Acestream%20Sports.xml'
    html=read_url(url)
    titles=re.compile('<title>(.+?)</title>').findall(html)
    links=re.compile('<link>(.+?)</link>').findall(html)
    img=re.compile('<thumbnail>(.+?)</thumbnail>').findall(html)

    for i in range(len(links)):
        url=links[i].replace('plugin.video.p2p-streams','program.plexus')
        li = xbmcgui.ListItem(titles[i], iconImage=img[i])
        li.setProperty('IsPlayable', 'true')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
    xbmcplugin.endOfDirectory(addon_handle)

def serbplus():
    url='http://www.serbiaplus.com/menu.html'
    html=read_url(url)
    soup=bs(html)
    tags=soup.findAll('a')
    for  tag in tags:
        if 'torrent' in tag['href']:
            link='http://www.serbiaplus.com/' + tag['href']

            name=tag.getText().title()
            name=name.encode('ascii','ignore')
            url = build_url({'mode': 'play_serb','name':name,'url':link})
            li = xbmcgui.ListItem(name,iconImage='')
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)
#############################################################################################################################################################3
#############################################################################################################################################################3
#############################################################################################################################################################3
#socer188

def soccer188():
    url='http://soccer188.net/link-sopcast/live-sopcast-link'
    html=read_url(url)
    channels=bs(html).findAll('tr',{'class':'tr-channels'})
    for channel in channels:
        infos=channel.findAll('td')
        try:
            link=channel.find('a')['href']
        except:
            link=''
        if link!='':
            title=infos[0].getText()
            lang=infos[1].getText()
            kbps=infos[2].getText()
            title='%s [%s] (%s)'%(title,lang,kbps)
            name=title
            name=name.encode('ascii','ignore')
            url = build_url({'mode': 'play_sopc','name':name,'url':link})
            li = xbmcgui.ListItem(title,iconImage='')
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)






#############################################################################################################################################################3
#############################################################################################################################################################3
#############################################################################################################################################################3


def livefoot_com():
    url='http://livefootballvideo.com/streaming'
    html=read_url(url)
    soup=bs(html)
    table=soup.find('div',{'class':'listmatch'})
    lis=table.findAll('li')
    for item in lis:
        league=item.find('div',{'class':'leaguelogo column'}).find('img')['alt']
        time=item.find('span',{'class':'starttime time'})['rel']
        import datetime
        ts = datetime.datetime.fromtimestamp(float(time))
        year,month,day,hour,minute=ts.strftime('%Y'),ts.strftime('%m'),ts.strftime('%d'),ts.strftime('%H'),ts.strftime('%M')
        from utils import pytzimp
        d = pytzimp.timezone(str(pytzimp.timezone('Europe/Madrid'))).localize(datetime.datetime(2000 + int(year), int(month), int(day), hour=int(hour), minute=int(minute)))
        timezona= addon.get_setting('timezone_new')
        my_location=pytzimp.timezone(pytzimp.all_timezones[int(timezona)])
        convertido=d.astimezone(my_location)
        fmt = "%d-%m-%y [COLOR green]%H:%M[/COLOR]"
        time=convertido.strftime(fmt)
        try:
            team1=item.find('div',{'class':'team column'}).find('img')['alt']
            team2=item.find('div',{'class':'team away column'}).find('img')['alt']
        except:
            team1=item.find('div',{'class':'program column'}).getText()
            team2=''

        link=item.find('div',{'class':'live_btn column'}).find('a')['href']
        name='%s - %s'%(team1,team2)
        if team2=='':
            name=team1
        name=clean(cleanex(name))
        title='([COLOR blue][B]%s[/B][/COLOR]) [B][COLOR orange]%s[/COLOR][/B] [%s]'%(time,name,league)
        url = build_url({'mode': 'open_livefoot.com_stream','name':name,'url':link})
        li = xbmcgui.ListItem(title,iconImage='')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)

def open_com_event(name,url):
    html=read_url(url)
    names,links=[],[]
    soup=bs(html)
    try:
        table=soup.find('div',{'id':'sopcastlist'}).find('tbody').findAll('tr')
        for i in range(1,len(table)):
            tds=table[i].findAll('td')
            channel_name=tds[1].getText()
            lang=tds[2].getText().replace('-','N/A')
            bitrate=tds[3].getText().replace('-','N/A')

            title='%s [%s] (%s)'%(channel_name,lang,bitrate)
            sop=table[i].findAll('a')[1]['href']

            names+=[title]
            links+=[sop]
    except:
        names=[]
        links=[]
    try:
        table=soup.find('div',{'id':'livelist'}).find('tbody').findAll('tr')
        for i in range(3,len(table)):
            if table[i].find('a')['title']=='acestream':
                tds=table[i].findAll('td')
                channel_name=tds[1].getText()
                lang=tds[2].getText().replace('-','N/A')
                bitrate=tds[3].getText().replace('-','N/A')
                title='%s [%s] (%s)'%(channel_name,lang,bitrate)
                sop=table[i].findAll('a')[1]['href']
                names+=[title]
                links+=[sop]
    except:
        names=[]
        links=[]

    if links!=[]:
        dialog = xbmcgui.Dialog()
        index = dialog.select('Select a channel:', names)

        if index>-1:
            name=names[index]
            url=links[index]

            play_sop(url,name)
    else:
        xbmcgui.Dialog().ok('No stream','No stream available yet!')
#############################################################################################################################################################3
#############################################################################################################################################################3
#############################################################################################################################################################3
