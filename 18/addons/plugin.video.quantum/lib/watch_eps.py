import requests, urllib2, urllib, xbmcgui, xbmcplugin, xbmcaddon, xbmc, re, sys, os, process
from lib import cloudflare




def watch_Main (url):
    html = requests.get(url).content
    match = re.compile('<div title=".+?" class=".+?" style="background-image: url(.+?)"></div>.+?<a title="(.+?)\(.+?\)" href="https://watch-episode.tv/watch_series_online_series?(.+?)&title=.+?" class=',re.DOTALL).findall(html)
    for image, name, extra in match:
        image = image.replace('(','').replace('\'','').replace(')','')
        process.Menu(name,'',100011,image,'','',extra)

def name_grab(name,extra):
    name = name.replace(' ','+')
    
    html = requests.get('http://www.tvmaze.com/search?q='+name).content
    match = re.compile('<div class="row" id="search">.+?<a href="(.+?)"><img src="(.+?)" alt="(.+?)"></a>',re.DOTALL).findall(html)
    for url2, img, name2 in match:
        img = 'http'+img
        url2 = 'http://www.tvmaze.com'+url2+'/episodes'
        html = requests.get(url2).content
        block = re.compile('<h2 data-magellan-destination=.+?><a href=".+?">(.+?)</a>(.+?)</tbody>',re.DOTALL).findall(html)
        for seas,rest in block:
            match = re.compile('<td>(.+?)</td><td>(.+?)</td><td><a href=".+?">(.+?)</a></td><td>',re.DOTALL).findall(str(rest))
            for ep, aired, ep_name in match:
                seas = seas.replace(' ','_')
                ep = 'episode_'+ep
                lknd= seas+'_'+ep
                process.Menu(ep_name+'--'+seas+'--'+ep+'--'+aired,'https://watch-episode.tv/watch_series_online_episodes'+extra+'&title='+name.replace('+','_')+seas+'_'+ep,100012,'','','','')
            
def grab_sourcelink(name,url):
    sources = []
    html = requests.get(url).content
    match = re.compile('<a class="report-button" href="(.+?)".+?<a href="javascript:setblock2(.+?)">.+?<div class="site-link" style=".+?">(.+?)</div>',re.DOTALL).findall(html)
    for site_link, souce_link, sc_name in match:
        sources.append({'source': sc_name, 'playlink': source_link})
        if len(sources) == len(match):
            choice = Dialog.select('Select Playlink',[link["quality"] for link in sources])
            if choice != -1:
                playlink = sources[choice]['playlink']
                isFolder=False
                xbmc.Player().play(playlink)
    

