'''
    veetle.com XBMC Plugin
    Copyright (C) 2011 t0mm0

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

import xbmc, xbmcaddon, xbmcplugin, xbmcgui
import Logger
import VeetleGuideDataSource
import VeetleProxyServer
import VeetleViews

pluginUrl = sys.argv[0]
pluginHandle = int(sys.argv[1])
pluginQuery = sys.argv[2]
__settings__ = xbmcaddon.Addon(id='plugin.video.veetle')
__language__ = __settings__.getLocalizedString

log = Logger.Logger("Main")

dataSource = VeetleGuideDataSource.VeetleGuideDataSource()
views = VeetleViews.VeetleViews(pluginUrl, pluginHandle, dataSource)

# Start proxy server
VeetleProxyServer.run()

# Render view according to query URL
views.renderUrl(pluginQuery)