
import re, xbmcplugin, xbmcgui, sys, urllib, requests,urllib2, xbmcaddon, xbmc, os
from lib import process


domains = ['onlinemovies.tube']
name = "onlinemovies"
sources = []
Dialog = xbmcgui.Dialog()
List = []
base_link = 'http://onlinemovies.tube/'


def scrape_episode(title, show_year, season, episode):
    process.Menu(title.lower(),'',13,'','','','')
    process.Menu(show_year,'',13,'','','','')
    process.Menu(season,'',13,'','','','')
    process.Menu(episode,'',13,'','','','')
    
    if len(season) == 1:
        season = '0'+str(season)
    if len(episode) == 1:
        episode = '0'+str(episode)
    start_url = base_link+'episode/'+title.replace(' ','-').lower()+'-s'+season+'e'+episode+'/'
    process.Menu(start_url,'',13,'','','','')
    html = requests.get(start_url).text
    match = re.compile('<iframe.+?src="(.+?)"').findall(html)
    for url in match:
        process.Menu(url,'',13,'','','','')
        if 'google' in url:
            pass
        elif 'youtube' in url:
            pass
        elif 'openload' in url:
            pass
        elif 'estream' in url:
            sources.append({'source': 'estream', 'quality': 'SD', 'scraper': self.name, 'url': url})
            if len(sources) == len(match):
                choice = Dialog.select('Select Playlink',[link["quality"] for link in sources])
        '''
        elif 'clxmovies' in url:
            html2 = requests.get(url).text
            match2 = re.compile('{file: "(.+?)",label:"(.+?)",type: ".+?"}').findall(html2)
            for url2,p in match2:
                sources.append({'source': 'google', 'quality': p, 'scraper': self.name, 'url': url2})
        '''


