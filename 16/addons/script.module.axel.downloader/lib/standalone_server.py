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


import axelcommon
import axelproxy
# This is xbmc linked class. TODO: read the settings here and send it to proxy for port etc
#TODO: check if start at launch setting is configured!

#Address and IP for Proxy to listen on
HOST_NAME = '127.0.0.1'
#HOST_NAME = 'localhost'
PORT_NUMBER = 45550 ##move this somewhere which could be configured by UI


if __name__ == '__main__':  
    file_dest = axelcommon.profile_path #replace this line if you want to be specific about the download folder
    print file_dest
    axelproxy.ProxyManager().start_proxy(port=PORT_NUMBER, host_name=HOST_NAME,download_folder=file_dest), #more param to come

