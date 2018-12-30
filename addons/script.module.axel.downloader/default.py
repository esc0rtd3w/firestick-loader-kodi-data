'''
    AxelProxy XBMC Addon
    Copyright (C) 2013 Eldorado

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
    MA 02110-1301, USA.
'''


from lib import axelcommon
from lib import axelproxy
# This is xbmc  class. TODO: read the settings here and send it to proxy for port etc
#TODO: check if start at launch setting is configured!
#todo find a better way to pass port and host and make it persist as Singleton is not working in xbmc
import xbmc 

if __name__ == '__main__':  
    file_dest = axelcommon.profile_path #todo: get everything we need to read from settings of xbmc
    pm = axelproxy.ProxyManager()
    pm.start_proxy(download_folder=file_dest), #more param to come
    while (not xbmc.abortRequested):
        xbmc.sleep(1)
        
    pm.abort=True

