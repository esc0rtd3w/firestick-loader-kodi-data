'''
    universal XBMC module
    Copyright (C) 2013 the-one @ XUNITYTALK.COM

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import sys
import xbmc
import xbmcgui
import xbmcplugin
import xbmcvfs
import socket
import xbmcaddon
import cookielib
import urllib2

settings = xbmcaddon.Addon(id='script.module.universal')
language = settings.getLocalizedString
version = "1.0.8"
plugin = "Universal-AnAddonsToolkit-" + version
core = ""
common = ""
downloader = ""
dbg = False
dbglevel = 3

# load lib directory
# begin
import xbmc
import re
xbmc_version =  re.search('^(\d+)', xbmc.getInfoLabel( "System.BuildVersion" ))
if xbmc_version:
    xbmc_version = int(xbmc_version.group(1))
else:
    xbmc_version = 1


if xbmc_version >= 16.9:
        dependencies = ['repository.duckpool','script.module.elementtree', 'script.module.muckys.common',
                        'script.common.plugin.cache','script.icechannel.dialogs', 'script.module.addon.common',
                        'script.module.beautifulsoup', 'script.module.dnspython', 'script.video.F4mProxy',
                        'script.module.feedparser', 'script.module.metahandler', 'script.module.myconnpy',
                        'script.module.parsedom', 'script.module.pyamf', 'script.module.simple.downloader',
                        'script.module.socksipy', 'script.module.t0mm0.common', 'script.module.unidecode',
                        'script.module.universal', 'script.module.urlresolver','script.icechannel.theme.default',]
        
        import glob


        folder = xbmc.translatePath('special://home/addons/')

        for DEPEND in glob.glob(folder+'script.icechannel*'):
            try:dependencies.append(DEPEND.rsplit('\\', 1)[1])
            except:dependencies.append(DEPEND.rsplit('/', 1)[1])


        for THEPLUGIN in dependencies:
            xbmc.log(str(THEPLUGIN))
            query = '{"jsonrpc":"2.0", "method":"Addons.SetAddonEnabled","params":{"addonid":"%s","enabled":true}, "id":1}' % (THEPLUGIN)
         
            xbmc.executeJSONRPC(query)
    




if xbmc_version >= 13.9:
    addon_id = 'script.module.universal'
    lib_addon_dir_name = "lib"
    import xbmcaddon
    import os
    from os.path import join, basename
    import sys
    addon = xbmcaddon.Addon(id=addon_id)
    addon_path = addon.getAddonInfo('path')
    sys.path.append(addon_path)
    lib_addon_dir_path = os.path.join( addon_path, lib_addon_dir_name)
    sys.path.append(lib_addon_dir_path)
    for dirpath, dirnames, files in os.walk(lib_addon_dir_path):
        sys.path.append(dirpath)
# end


from universal import watchhistory

print 'Universal - An Addons Toolkit: - watchhistory - -Auto Cleanup Start'
wh = watchhistory.WatchHistory('script.module.watchhistory')
wh.cleanup_history()
print 'Universal - An Addons Toolkit: - watchhistory - -Auto Cleanup End'
