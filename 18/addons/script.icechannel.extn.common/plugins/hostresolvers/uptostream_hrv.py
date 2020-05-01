'''
    http://uptostream.com/
    for Istream ONLY
    14/06/2014

    Coolwave

    A thank you to all members of the Xunity team.

    (c)2014 Xunity.

    This resolver IS NOT OPEN SOURCE, It is to be used as
    part of Istream ONLY.

    version 0.1
'''
from entertainment import jsunpack
from entertainment.plugnplay.interfaces import HostResolver
from entertainment.plugnplay import Plugin
from entertainment import common

import xbmcgui
import xbmc
import os
                    


class uptostream(HostResolver):
    implements = [HostResolver]
    name = "uptostream"
    match_list = ['uptostream.com']

    
    def Resolve(self, url):

        from entertainment.net import Net
        import re
        import time

        net = Net()

        try:

        
            content = net.http_GET(url).content

            r = re.search(r'<video.+?src="([^"]+?)"',content,re.I|re.DOTALL)
            
            if r:                
                return play_url

            

        except Exception, e:
            common.addon.log(self.name.upper() + ' - Exception occured: %s' % e)
            return None

        
