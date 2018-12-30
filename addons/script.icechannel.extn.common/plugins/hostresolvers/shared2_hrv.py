'''
    Shared2.me Source Resolver
    For iStream Only,
    18/05/2014

    Jas0npc, the-one

    A thank you to all members of the Xunity team.

    (c)2014 Xunity.

    This resolver IS NOT OPEN SOURCE, It is to be used as
    part of Istream ONLY.

    
'''

from entertainment.plugnplay.interfaces import HostResolver
from entertainment.plugnplay.interfaces import CustomSettings
from entertainment.plugnplay import Plugin
from entertainment import common

import xbmcgui
import xbmc
import os

class Shared2(HostResolver, CustomSettings):
    implements = [HostResolver, CustomSettings]
    name = "Shared2"
    resolverName = name.title()+" ([COLOR blue]i[/COLOR]STREAM Resolver)"
    version = "0.1"
    match_list = ['shared2.me']
    profile_path = common.profile_path
    cookie_file = os.path.join(profile_path, 'cookies', '%s.cookies') % name
    puzzle_img = os.path.join(profile_path, 'captchas', '%s.png') % name
    icon = common.notify_icon
    try:
        os.makedirs(os.path.dirname(cookie_file))
    except OSError:
        pass


    def __init__(self):
        xml = '<settings>\n'
        xml += '<category label="">\n'
        xml += '<setting id="version" type="bool" label="'
        xml += '[COLOR blue]Version: '+self.version+'[/COLOR]" />\n'
        xml += '<setting type="sep"/>\n'
        xml += '</category>\n' 
        xml += '</settings>\n'
        self.CreateSettings(self.name, self.resolverName, xml)
                    
    def Resolve(self, url):
        import re
        from entertainment.net import Net
        net = Net(cached=False)

        common.addon.log( self.name.upper() + ' - Link: %s' % url )
        common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: [B][COLOR white]' + self.name.upper() + '[/B][/COLOR]',
                                      'Resolving', 700, self.icon)

        html = net.http_GET(url).content
        net.save_cookies(self.cookie_file)
        net.set_cookies(self.cookie_file)

        try:
            if not re.search(r'value=\"Continue to video',html,re.I):
                raise Exception ('File Not Found')
            
            html = net.http_POST(url,form_data={'Continue':'Continue to video'},
                                 headers={'Content-Type':'application/x-www-form-urlencoded'}
                                 ).content

            finalLink = re.search(r'var\sxxxx\s\=\s\"(.*?)\"',html)
            if finalLink:
                return finalLink.group(1)

            else:
                raise Exception ('No Media Found To Stream')

        except Exception, e:
            common.addon.log(self.name.upper() + ' - Exception occured: %s' % e)
            common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: [B][COLOR white]' + self.name.upper() + '[/B][/COLOR]', '[COLOR red]'+str(e)+'[/COLOR]', 3000, self.icon)                
            return None
        
