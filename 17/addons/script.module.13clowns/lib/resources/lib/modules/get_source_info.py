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


import requests.sessions
from BeautifulSoup import BeautifulSoup

def get_source_info(url):
    source_info = {}
    if 'thevideo' in url:
        source_info['source'] = 'thevideo.me'
        with requests.session() as s:
            p = s.get(url)
            soup = BeautifulSoup(p.text, 'html.parser')
            title = soup.findAll('script', src=False, type=False)
            for i in title:
                if "title" in i.prettify():
                    for line in i.prettify().split('\n'):
                        if " title" in line:
                            line = line.replace("title: '", '').replace("',", '')
                            if "720" in line:
                                source_info['qual'] = "720p"
                            elif "1080" in line:
                                source_info['qual'] = "1080p"
                            else:
                                source_info['qual'] = "SD"
        return source_info
    elif 'vidzi' in url:
        #Not completed
        return "SD"