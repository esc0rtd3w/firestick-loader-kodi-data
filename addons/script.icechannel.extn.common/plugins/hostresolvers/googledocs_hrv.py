'''
    Ice Channel    
'''

from entertainment.plugnplay.interfaces import HostResolver
from entertainment.plugnplay import Plugin
from entertainment import common
import xbmcgui

class googledocs(HostResolver):
    implements = [HostResolver]
    
    name = 'googledocs'
    
    match_list = ['docs.google.com']
    
    def Resolve(self, url):
    
        try:
            from entertainment.net import Net
            net = Net(cached=False)
    
            html = net.http_GET(url).content.encode("utf-8").rstrip()
            
            import re
            
            video_url=re.search('fmt_stream_map".+?(http.+?),', html).group(1)
            video_url=video_url.replace('|', '').replace('\u003d','=').replace('\u0026','&')
            
            return video_url

        except Exception, e:
            common.addon.log(self.name.upper() + ' - Exception occured: %s' % e)
            common.addon.show_small_popup('[B][COLOR white]' + self.name.upper() + '[/COLOR][/B]', '[COLOR red]Exception occured, check logs.[/COLOR]')                
            return None
            
