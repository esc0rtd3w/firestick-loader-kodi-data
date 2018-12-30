'''
    Ice Channel    
'''

from entertainment.plugnplay.interfaces import PremiumHostResolver
from entertainment.plugnplay.interfaces import CustomSettings
from entertainment.plugnplay import Plugin
from entertainment import common

class RealDebrid(PremiumHostResolver, CustomSettings):
    implements = [PremiumHostResolver, CustomSettings]
    
    name = "Real-Debrid"
    
    base_url = 'http://real-debrid.com/'
    
    def __init__(self):
    
        xml = '<settings>\n'       
        xml += '<category label="Real-Debrid">\n'
        xml += '<setting id="realdebrid-enable" type ="bool" label="Enabled" default="false"/>\n'
        xml += '<setting id="realdebrid-username" type="text" label="Username" default="" enable="!eq(-1,false)"/>\n'
        xml += '<setting id="realdebrid-password" type="text" label="Password" default="" option="hidden" enable="!eq(-2,false)"/>\n'
        xml += '</category>\n'
        xml += '</settings>\n'
        self.CreateSettings(self.name, self.name, xml)
        
    def CanResolve(self, url):
    
        if self.Settings().get_setting('realdebrid-enable') == "false": return False
        
        domain = common.GetDomainFromUrl(url).lower()
        from entertainment.net import Net
        net = Net()
        hosters = net.http_GET(self.base_url ).content
        if domain not in hosters: return False

        return True

    def Resolve(self, url):
        try:
            from entertainment.net import Net
            net = Net(cached=False)
            
            import os
            cookie_file = os.path.join(common.cookies_path, 'realdebrid.lwp')
            
            if net.set_cookies(cookie_file) == False:
                import urllib
                credentials = urllib.urlencode({'user' : self.Settings().get_setting('realdebrid-username'), 'pass' : self.Settings().get_setting('realdebrid-password')})
                content = net.http_GET(self.base_url + 'ajax/login.php?' + credentials ).content
                net.save_cookies(cookie_file)
            elif 'My Account' not in net.http_GET(self.base_url).content:
                import urllib
                credentials = urllib.urlencode({'user' : self.Settings().get_setting('realdebrid-username'), 'pass' : self.Settings().get_setting('realdebrid-password')})
                content = net.http_GET(self.base_url + 'ajax/login.php?' + credentials ).content
                net.save_cookies(cookie_file)
                
            content = net.http_GET(self.base_url + 'ajax/unrestrict.php?link=' + url).content
            import re
            r = re.search('[\'"]{1}main_link[\'"]{1}\:[\'"]{1}(.+?)[\'"]{1}', content)
            if r:                
                stream_url = r.group(1)
                if stream_url:
                    return stream_url.replace('\/', '/')
        except Exception, e:
            common.addon.log(self.name.upper() + ' - Exception occured: %s' % e)
            common.addon.show_small_popup('[B][COLOR white]' + self.name.upper() + '[/COLOR][/B]', '[COLOR red]Exception occured, check logs.[/COLOR]')                
            return None

        return None
