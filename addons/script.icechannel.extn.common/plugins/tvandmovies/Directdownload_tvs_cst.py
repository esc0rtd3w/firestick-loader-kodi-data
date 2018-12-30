'''
    directdownload    
    Copyright (C) 2013 Coolwave
'''

from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay.interfaces import CustomSettings
from entertainment.plugnplay import Plugin
from entertainment import common
import re
import xbmc,os
datapath = xbmc.translatePath(os.path.join('special://home/userdata/addon_data','script.icechannel'))
cookie_path = os.path.join(datapath, 'cookies')

do_no_cache_keywords_list = ["alert('Please Login!');"]

class directdownload(TVShowSource,CustomSettings):
    implements = [TVShowSource,CustomSettings]
    
    name = "directdownload"
    display_name = "Direct Download"
    base_url = 'https://directdownload.tv/'
    source_enabled_by_default = 'false'
    cookie_file = os.path.join(common.cookies_path, 'DDlogin.cookie')
    
    def __init__(self):
        xml = '<settings>\n'
        xml += '<category label="Account">\n'
        xml += '<setting id="tv_user" type="text" label="Username" default="xunity" />\n'
        xml += '<setting id="tv_pwd" type="text" option="hidden" label="Password" default="xunity" />'
        xml += '</category>\n' 
        xml += '</settings>\n'
        self.CreateSettings(self.name, self.display_name, xml)

    
    def GetFileHosts(self, url, list, lock, message_queue): 
        
        import re
        
        from entertainment.net import Net
        
        net = Net(do_not_cache_if_any=do_no_cache_keywords_list)
        net._cached = False
        tv_user = self.Settings().get_setting('tv_user')
        tv_pwd = self.Settings().get_setting('tv_pwd')
        loginurl = 'https://directdownload.tv'
        data     = {'password': tv_pwd,'username': tv_user,'Login':'Login','mode':'normal'}
        headers  = {'Referer':'https://directdownload.tv','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','Connection':'keep-alive','Content-Type':'application/x-www-form-urlencoded','Host':'directdownload.tv','Origin':'http://directdownload.tv','User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'}
        net.http_POST(loginurl, data, headers).content
        net.save_cookies(self.cookie_file)
        net.set_cookies(self.cookie_file)
        
        content = net.http_GET(url).content
        
        r='{"url":"(.+?)","hostname":".+?"}'
        match=re.compile(r).findall(content)

        urlselect  = []

        for url in match:            
            #print url
            if url not in urlselect:
                urlselect.append(url)

                quality = 'SD'
                url_lower = '.' + url.lower() + '.'
                for quality_key, quality_value in common.quality_dict.items():
                    if re.search('[^a-zA-Z0-0]' + quality_key + '[^a-zA-Z0-0]', url_lower):
                        quality = quality_value
                        break
                    
                self.AddFileHost(list, quality, url.replace('\/', '/'))
            
                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):                 
        
        name = self.CleanTextForSearch(name) 
        season = self.CleanTextForSearch(season) 
        episode = self.CleanTextForSearch(episode)
        
        season_pull = "0%s"%season if len(season)<2 else season
        episode_pull = "0%s"%episode if len(episode)<2 else episode

        search_term = name
        #match=re.compile('{"release":"([^"]+?)","when":.+?,"size":".+?","links":(.+?),"idtvs".+?"quality":"([^"]+?)".+?}').findall(html)
        
        searchUrl='https://directdownload.tv/index/search/keyword/%s s%se%s/qualities/pdtv,dsr,hdtv,realhd,dvdrip,webdl,webdl1080p/from/0/search' %(name.lower(),season_pull,episode_pull)        
        searchUrl = searchUrl.replace(' ','%20')

        self.GetFileHosts(searchUrl, list, lock, message_queue)

        
