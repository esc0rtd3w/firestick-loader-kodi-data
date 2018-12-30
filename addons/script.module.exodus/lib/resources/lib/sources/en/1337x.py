'''
    Created by others
    Refactored for exodusscrapers
    Nov 20 2018
'''

import re, requests
from resolveurl.plugins.premiumize_me import PremiumizeMeResolver
from resources.lib.modules import source_utils

class source:

    def __init__(self):
        self.api_key = PremiumizeMeResolver.get_setting('password')
        self.priority = 1
        self.language = ['en']
        self.domain = 'https://1337xx.top'
        self.search_link = 'https://1337xx.top/search.php?q=%s'
        self.checkc = 'https://www.premiumize.me/api/torrent/checkhashes?apikey=%s&hashes[]=%s&apikey=%s'
        self.pr_link = 'https://www.premiumize.me/api/transfer/directdl?apikey=%s&src=magnet:?xt=urn:btih:%s'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'title': title, 'year': year}
            return url
        except:
            print("Unexpected error in 1337xx Script: episode", sys.exc_info()[0])
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(exc_type, exc_tb.tb_lineno)
            return url

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = tvshowtitle
            return url
        except:
            print("Unexpected error in 1337xx Script: TV", sys.exc_info()[0])
            return url
        return url

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            url = url
            url = {'tvshowtitle': url, 'season': season, 'episode': episode, 'premiered': premiered}
            return url
        except:
            print("Unexpected error in 1337xx Script: episode", sys.exc_info()[0])
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(exc_type, exc_tb.tb_lineno)
            return url

    def sources(self, url, hostDict, hostprDict):
        sources = []
        try:
            with requests.Session() as s:
                if 'episode' in url:
                    iep = url['episode'].zfill(2)
                    ise = url['season'].zfill(2)
                    se = 's' + ise + 'e' + iep
                    sel = url['tvshowtitle'].replace(' ','+') + '+' + se
                   
                else:
                    se = url['year']
                    sel = url['title'].replace(' ','+') + '+' + se
                    
                   
                gs = s.get(self.search_link % (sel)).text
                gl = re.compile('f\W+(/t.*?)"\st.*?'+se, re.I).findall(gs)
                for res in gl:
                    rih = s.get(self.domain+res).text
                    gih = re.compile('Size.*?n>(.*?)<.*?hash.*?n\W+(.*?)\W.*?>D\w+(.*?)<', re.DOTALL).findall(rih)
                    for si,hass,nam in gih:
                        checkca = s.get(self.checkc % (self.api_key, hass, self.api_key)).text
                        quality = source_utils.check_sd_url(nam)
                        if 'finished' in checkca:
                            url = self.pr_link % (self.api_key, hass)
                            sources.append({
                                'source': 'cached',
                                'quality': quality,
                                'language': 'en',
                                'url': url,
                                'direct': False,
                                'debridonly': False,
                                'info': si+'|'+nam,
                            })
                            
            return sources
        except:
            print("Unexpected error in 1337xx Script: Sources", sys.exc_info()[0])
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(exc_type, exc_tb.tb_lineno)
            return sources

        
    def resolve(self, url):
        getpl = requests.get(url).text
        sl = re.compile('link.*?"(h.*?)["\'].\n.*?s.*?http', re.I).findall(getpl)[0]
        url = sl.replace('\\','')
        return url