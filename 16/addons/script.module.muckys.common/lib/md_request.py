# -*- coding: utf-8 -*- 

#
#    Copyright (C) 2017 Mucky Duck (class sucuri Derived from Lambda's client module)
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


import base64,cfscrape,re
from incapsula import crack


User_Agent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.4; en-US; rv:1.9.2.2) Gecko/20100316 Firefox/3.6.2'
scraper = cfscrape.CloudflareScraper()




class sucuri:

        def __init__(self):
                self.cookie = None


        def get(self, result):

                try:

                    s = re.compile("S\s*=\s*'([^']+)").findall(result)[0]
                    s = base64.b64decode(s)
                    s = s.replace(' ', '')
                    s = re.sub('String\.fromCharCode\(([^)]+)\)', r'chr(\1)', s)
                    s = re.sub('\.slice\((\d+),(\d+)\)', r'[\1:\2]', s)
                    s = re.sub('\.charAt\(([^)]+)\)', r'[\1]', s)
                    s = re.sub('\.substr\((\d+),(\d+)\)', r'[\1:\1+\2]', s)
                    s = re.sub(';location.reload\(\);', '', s)
                    s = re.sub(r'\n', '', s)
                    s = re.sub(r'document\.cookie', 'cookie', s)

                    cookie = '' ; exec(s)
                    self.cookie = re.compile('([^=]+)=(.*)').findall(cookie)[0]
                    self.cookie = '%s=%s' % (self.cookie[0], self.cookie[1])

                    return self.cookie

                except:
                        pass




def open_url(url, method='get', headers=None, cookies=None, params={}, data={},
             redirects=True, verify=True, timeout=None, files=None, auth=None,
             proxies=None, hooks=None, stream=None, cert=None, json=None):

        if headers == None:

                headers = {}
                headers['User-Agent'] = User_Agent

        link = getattr(scraper,method)(url, headers=headers, cookies=cookies, params=params, data=data,
                                       allow_redirects=redirects, verify=verify, timeout=timeout, files=files,
                                       auth=auth, proxies=proxies, hooks=hooks, stream=stream, cert=cert, json=json)

        try:

                su = sucuri().get(link.content)
                if su:
                        headers['Cookie'] = su

                        if not url[-1] == '/':
                                url = '%s/' %url

                        link = getattr(scraper,method)(url, headers=headers, cookies=cookies, params=params, data=data,
                                                       allow_redirects=redirects, verify=verify, timeout=timeout,
                                                       files=files, auth=auth, proxies=proxies, hooks=hooks,
                                                       stream=stream, cert=cert, json=json)

        except:
                pass

        if '_Incapsula_' in link.content:

                link = crack(scraper, link)

        return link
