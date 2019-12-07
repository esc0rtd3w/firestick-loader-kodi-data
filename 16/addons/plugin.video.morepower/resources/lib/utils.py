import os
import re
import sys
import xbmc,xbmcaddon,xbmcgui,xbmcplugin,xbmcgui

from addon.common.net import Net
from addon.common.addon import Addon

net = Net()

addon_id = 'plugin.video.morepower'
addon = Addon(addon_id, sys.argv)
Addon = xbmcaddon.Addon(addon_id)

sys.path.append(os.path.join(addon.get_path(), 'resources', 'lib'))
data_path = addon.get_profile()


try:
  import StorageServer
except:
  import storageserverdummy as StorageServer
cache = StorageServer.StorageServer(addon_id)
               


def MESSAGE(url):
    html = net.http_GET(url).content
    l = []
    r = re.findall('info>(.*?)</info', html, re.I|re.DOTALL)[0]
    r = r.replace('<message>','').replace('</message>','')
    r = r.replace('<message1>','').replace('</message1>','')
    r = r.replace('<message2>','').replace('</message2>','')
    r = r.replace('<message3>','').replace('</message3>','')
    r = r.replace('<message4>','').replace('</message4>','')
    r = r.replace('<message5>','').replace('</message5>','')
    r = r.replace('<message6>','').replace('</message6>','')
    r = r.replace('<message7>','').replace('</message7>','')
    r = r.replace('<message8>','').replace('</message8>','')
    r = r.replace('<message9>','').replace('</message9>','')
    r = r.replace('<message10>','').replace('</message10>','')
    r = r.replace('<thumbnail>','').replace('</thumbnail>','')
    for text in r:
        final = text
        l.append(final)
        
    t = ''.join(l)
    tt = addon.unescape(t)
    return (tt)
