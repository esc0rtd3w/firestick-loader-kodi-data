# -*- coding: utf-8 -*-

'''
#:::'##::::'#######:::'######::'##::::::::'#######::'##:::::'##:'##::: ##::'######::
#:'####:::'##.... ##:'##... ##: ##:::::::'##.... ##: ##:'##: ##: ###:: ##:'##... ##:
#:.. ##:::..::::: ##: ##:::..:: ##::::::: ##:::: ##: ##: ##: ##: ####: ##: ##:::..::
#::: ##::::'#######:: ##::::::: ##::::::: ##:::: ##: ##: ##: ##: ## ## ##:. ######::
#::: ##::::...... ##: ##::::::: ##::::::: ##:::: ##: ##: ##: ##: ##. ####::..... ##:
#::: ##:::'##:::: ##: ##::: ##: ##::::::: ##:::: ##: ##: ##: ##: ##:. ###:'##::: ##:
#:'######:. #######::. ######:: ########:. #######::. ###. ###:: ##::. ##:. ######::
#:......:::.......::::......:::........:::.......::::...::...:::..::::..:::......:::

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



import re
import urllib
import urlparse
from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import proxy


class source:
    def __init__(self):
        self.name = 'Movie Trailers'       
        self.priority = 1
        self.language = ['en']
        self.domains = ['hdm.to']
        self.base_link = 'https://hdm.to'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = cleantitle.geturl(title)
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            url = '%s/%s/' % (self.base_link,url)
            r = client.request(url)
            try:
                match = re.compile('<iframe.+?src="(.+?)"').findall(r)
                for url in match:
#                    if 'openload' in url:
#                        Provider = 'Openload.co'
#                        Direct = False
#                        Quality = 'HD'
                    if 'youtube' in url:
                        Provider = 'DirectLink'
                        Direct = True
                        Quality = 'HD'
                        sources.append({'source': Provider,'quality': Quality,'language': 'en','url': url,'direct': False,'debridonly': False}) 
#                    sources.append({'source': Provider,'quality': Quality,'language': 'en','url': url,'direct': False,'debridonly': False}) 
                return sources

            except:
                return
        except Exception:
            return
        # return sources

    def resolve(self, url):
         return url
