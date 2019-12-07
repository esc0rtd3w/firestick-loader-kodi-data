# -*- coding: utf-8 -*- 

#      Copyright (C) 2017 Mucky Duck
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.

#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.

#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.


import sys,xbmc,xbmcplugin
from common import Addon


def setView(addon_id, content, viewType):

        addon = Addon(addon_id, sys.argv)

        if content:

                xbmcplugin.setContent(int(sys.argv[1]), content)

        if addon.get_setting('auto-view') == 'true':

                print addon.get_setting(viewType)

                if addon.get_setting(viewType) == 'Info':
                        VT = '504'

                elif addon.get_setting(viewType) == 'Info2':
                        VT = '503'

                elif addon.get_setting(viewType) == 'Info3':
                        VT = '515'

                elif addon.get_setting(viewType) == 'Fanart':
                        VT = '508'

                elif addon.get_setting(viewType) == 'Poster Wrap':
                        VT = '501'

                elif addon.get_setting(viewType) == 'Big List':
                        VT = '51'

                elif addon.get_setting(viewType) == 'Low List':
                        VT = '724'

                elif addon.get_setting(viewType) == 'List':
                        VT = '50'

                elif addon.get_setting(viewType) == 'Default Menu View':
                        VT = addon.get_setting('default-view1')

                elif addon.get_setting(viewType) == 'Default TV Shows View':
                        VT = addon.get_setting('default-view2')

                elif addon.get_setting(viewType) == 'Default Episodes View':
                        VT = addon.get_setting('default-view3')

                elif addon.get_setting(viewType) == 'Default Movies View':
                        VT = addon.get_setting('default-view4')

                elif addon.get_setting(viewType) == 'Default Docs View':
                        VT = addon.get_setting('default-view5')

                elif addon.get_setting(viewType) == 'Default Cartoons View':
                        VT = addon.get_setting('default-view6')

                elif addon.get_setting(viewType) == 'Default Anime View':
                        VT = addon.get_setting('default-view7')

                print viewType
                print VT

                xbmc.executebuiltin("Container.SetViewMode(%s)" % ( int(VT) ) )

        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_UNSORTED )
        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RATING )
        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_DATE )
        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_PROGRAM_COUNT )
        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RUNTIME )
        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_GENRE )
        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_MPAA_RATING )
