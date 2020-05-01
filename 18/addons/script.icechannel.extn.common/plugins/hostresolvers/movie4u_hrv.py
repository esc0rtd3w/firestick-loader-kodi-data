'''
    movie4u.org
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
                    


class movie4u(HostResolver):
    implements = [HostResolver]
    name = "movie4u"
    match_list = ['movie4u.org']
    profile_path = common.profile_path
    cookie_file = os.path.join(profile_path, 'cookies', '%s.cookies') % name
    puzzle_img = os.path.join(profile_path, 'captchas', '%s.png') % name
    icon = common.notify_icon
    try:
        os.makedirs(os.path.dirname(cookie_file))
    except OSError:
        pass

    
    def Resolve(self, url):

        from entertainment.net import Net
        import re
        import time

        net = Net()

        try:

            common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: [B][COLOR white]' + self.name.upper() + '[/B][/COLOR]',
                                          'Resolving', 700, self.icon)
        
            content = net.http_GET(url).content

            new_url = re.search('streamContinueButton.+?href="(.+?)"', content,re.I)

            from entertainment import istream
            html = net.http_GET(new_url.group(1)).content
            r = re.search(r'<iframe\s*src="(.+?)"\s*allowfullscreen',html,re.I|re.DOTALL)
            
            if r:
                play_url = istream.ResolveUrl(r.group(1))
                return play_url

            

        except Exception, e:
            common.addon.log(self.name.upper() + ' - Exception occured: %s' % e)
            common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: [B][COLOR white]' + self.name.upper() + '[/B][/COLOR]', '[COLOR red]'+str(e)+'[/COLOR]', 700, self.icon)                
            return None

        
