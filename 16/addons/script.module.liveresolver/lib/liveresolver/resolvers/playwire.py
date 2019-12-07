# -*- coding: utf-8 -*-


import re,urlparse,json
from liveresolver.modules import client
from BeautifulSoup import BeautifulSoup as bs
import xbmcgui

def resolve(url):
    try:
        result = client.request(url)
        html = result
        result = json.loads(result)
        try:
            f4m=result['content']['media']['f4m']
        except:
            reg=re.compile('"src":"http://(.+?).f4m"')
            f4m=re.findall(reg,html)[0]
            f4m='http://'+pom+'.f4m'
        
        result = client.request(f4m)
        soup = bs(result)
        try:
            base=soup.find('baseURL').getText()+'/'
        except:
            base=soup.find('baseurl').getText()+'/'

        linklist = soup.findAll('media')
        choices,links=[],[]
        for link in linklist:
            url = base + link['url']
            bitrate = link['bitrate']
            choices.append(bitrate)
            links.append(url)
        if len(links)==1:
            return links[0]
        if len(links)>1:
            dialog = xbmcgui.Dialog()
            index = dialog.select('Select bitrate', choices)
            
            if index>-1:
                return links[index]
        
        return


    except:
        return

