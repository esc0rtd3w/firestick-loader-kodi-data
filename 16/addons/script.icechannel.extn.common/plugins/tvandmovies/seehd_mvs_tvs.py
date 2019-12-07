

#iStream Extension
#SeeHD
#Copyright (C) 2017 mucky duck


from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay import Plugin
import xbmc

class seehd(MovieSource,TVShowSource):

    implements = [MovieSource,TVShowSource]

    name = 'SeeHD'
    display_name = 'SeeHD'
    base_url = 'http://www.seehd.ws'
    User_Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'

    source_enabled_by_default = 'true'




    def AddMedia(self, list, data):

        for final_url, res in data: 

            if '.srt' not in final_url:
                if '1080' in res:
                    res='1080P'                   
                elif '720' in res:
                    res='720P'
                elif  '480' in res:
                    res='DVD'
                elif '360' in res:
                    res='SD'
                else:
                    res='DVD'

                self.AddFileHost(list, res, final_url)



    def googletag(self,url):
        import re
        quality = re.compile('itag=(\d*)').findall(url)
        quality += re.compile('=m(\d*)$').findall(url)
        try: quality = quality[0]
        except: return []

        if quality in ['37', '137', '299', '96', '248', '303', '46']:
            return [{'quality': '1080P', 'url': url}]
        elif quality in ['22', '84', '136', '298', '120', '95', '247', '302', '45', '102']:
            return [{'quality': '720P', 'url': url}]
        elif quality in ['35', '44', '135', '244', '94']:
            return [{'quality': 'SD', 'url': url}]
        elif quality in ['18', '34', '43', '82', '100', '101', '134', '243', '93']:
            return [{'quality': 'SD', 'url': url}]
        elif quality in ['5', '6', '36', '83', '133', '242', '92', '132']:
            return [{'quality': 'SD', 'url': url}]
        else:
            return []




    def GetFileHosts(self, url, list, lock, message_queue, season, episode, type):

        from entertainment import jsunpack
        from md_request import open_url
        import urlresolver,re,urllib

        referer = url
        
        headers = {'User-Agent':self.User_Agent}
        sources = []

        link = open_url(url, headers=headers, timeout=3).content
                
        try:
            RES = re.findall(r'Quality:</strong>([^<>]*)<', str(link), re.I|re.DOTALL)[0].upper()
        except:
            RES = ''

        if '4K' in RES:
            res='4K'
        elif '3D' in RES:
            res='3D'
        elif '1080' in RES:
            res='1080P'                   
        elif '720' in RES:
            res='720P'
        elif 'HD' in RES:
            res='HD'
        elif 'DVD' in RES:
            res='DVD'
        elif 'HDTS' in RES:
            res='TS'
        elif 'TS' in RES:
            res='TS'
        elif 'CAM' in RES:
            res='CAM'
        elif 'HDCAM' in RES:
            res='CAM'
        else:
            res='720P'

        try:
            url2 = re.findall(r'<source src="([^"]+)"', str(link), re.I|re.DOTALL)[0]
            sources.append(url2)
        except:pass

        try:
            iframe_url = re.findall(r'iframe.*?src="([^"]+)"', str(link), re.I|re.DOTALL)
            for url3 in iframe_url:
                headers = {'User-Agent':self.User_Agent, 'Referer':referer}
                if 'songs2dl' in url3:
                    link2 = open_url(url3, headers=headers, timeout=3).content
                    if jsunpack.detect(link2):
                        js_data = jsunpack.unpack(link2)
                        match = re.findall(r'"file":"([^"]+)".*?"label":"([^"]+)"', str(js_data), re.I|re.DOTALL)
                        self.AddMedia(list,match)

                elif '.php' in url3:
                    link2 = open_url(url3, headers=headers, timeout=3).content
                    match = re.findall(r'iframe.*?src="([^"]+)"', str(link2), re.I|re.DOTALL)[0]
                    link3 = open_url(match, headers=headers, timeout=3).content
                    match2 = re.findall(r'iframe.*?src="([^"]+)"', str(link3), re.I|re.DOTALL)[0]
                    match2 = match2.replace('/preview','/view').replace('/edit','/view')
                    link4 = open_url(match2, headers=headers, verify=False, timeout=3)
                    match3 = re.compile('itag\\\u003d.*?\\\u0026url\\\u003d(.*?)%3B').findall(link4.content)
                    for doc_url in match3:
                        doc_url = urllib.unquote(doc_url)
                        doc_url = doc_url.replace('\\u003d','=').replace('\\u0026','&')
                        if 'video/x-flv' in doc_url:
                                doc_url = doc_url.partition('url=')[2]
                        for a in self.googletag(doc_url):
                            cookie = link4.cookies.get_dict()
                            cookie = urllib.quote('Cookie:DRIVE_STREAM=%s; NID=%s' %(cookie['DRIVE_STREAM'],cookie['NID']))
                            g_url = a['url'] + '|' + cookie
                            self.AddFileHost(list, a['quality'], g_url)
                    
                
                else:
                    if urlresolver.HostedMediaFile(url3):
                        sources.append(url3)
        except:pass

        try:
            mirror_url = re.findall(r'href="([^"]+)" rel="nofollow">', str(link), re.I|re.DOTALL)
            for url4 in mirror_url:
                if urlresolver.HostedMediaFile(url4):
                    sources.append(url4)
        except:pass
            
        for final_url in sources:
            self.AddFileHost(list, res, final_url)




    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):

        from md_request import open_url
        import re

        name = self.CleanTextForSearch(name.lower()).strip()
        search =  '%s/?s=%s' %(self.base_url,name.replace(' ','+'))
        headers = {'User-Agent':self.User_Agent}
        link = open_url(search, headers=headers, timeout=3).content
        
        try:
            
            links = link.split('article id=')[2:]
            
            for p in links:

                media_url = re.compile('href="([^"]+)"',re.DOTALL).findall(p)[0]
                media_title = re.compile('<p>([^<>]*)</p>',re.DOTALL).findall(p)[0]

                if type == 'tv_episodes':
                    if name in self.CleanTextForSearch(media_title.lower()):
                        season_pull = "0%s"%season if len(season)<2 else season
                        episode_pull = "0%s"%episode if len(episode)<2 else episode
                        sep = 's%se%s' %(season_pull,episode_pull)
                        if sep in self.CleanTextForSearch(media_title.lower()):
                            self.GetFileHosts(media_url, list, lock, message_queue, season, episode, type)
                else:
                    if name in self.CleanTextForSearch(media_title.lower()):
                        if year in media_title:
                            self.GetFileHosts(media_url, list, lock, message_queue, '', '', type)

        except:pass
            
