# -*- coding: utf-8 -*- 

#
#      Copyright (C) 2017 SchisM fork from MuckyDuck Modules
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


import base64,cfscrape,re,random,urlparse
from incapsula import crack
import requests
User_Agent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.4; en-US; rv:1.9.2.2) Gecko/20100316 Firefox/3.6.2"'
scraper = cfscrape.create_scraper()

session = requests.Session()

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


def OPEN_URL(url, method='get', headers=None, params=None, data=None, redirects=True, verify=True, mobile=False, timeout=None, output=None, XHR=False):
       
        if timeout == None: timeout = 30	
        if headers == None:
                headers = {}
                headers['User-Agent'] = random_agent()
				
        if not 'User-Agent' in headers:
			if not 'user-agent' in headers: headers['User-Agent'] = random_agent()	
				
        elif  mobile == True:			
				headers['User-Agent'] = ''
				headers['User-Agent'] = 'Apple-iPhone/701.341'
				
        if output == 'geturl':
                link = requests.head(url, allow_redirects=True)
                link = str(link.url)	
                return link	

        if output == 'cookie':
                cookie = [] 
                r = session.get(url, headers=headers)
                cookie_dict = session.cookies.get_dict()
                for k,v in cookie_dict.items(): cookie ="%s=%s" % (k,v)
                return cookie
        if XHR == True:
			print ("REQUESTING WITH XMLHttpRequest")
			headers['X-Requested-With'] = 'XMLHttpRequest'
			
        if not 'Accept-Language' in headers:
            headers['Accept-Language'] = 'en-US'
			
        if not 'referer' in headers: 
			if not 'Referer' in headers: headers['Referer'] = '%s://%s/' % (urlparse.urlparse(url).scheme, urlparse.urlparse(url).netloc)		
		
        link = requests.get(url, headers=headers, params=params, data=data, allow_redirects=redirects, verify=verify, timeout=int(timeout))
        response_code = link.status_code
        print ("RESPONSE CODE", response_code)
        try: resp_header = link.headers['Server']
        except: resp_header = 'none'

				
        try:
                if resp_header.lower() == 'cloudflare-nginx' and response_code == 503 and not "sucuri_cloudproxy_js" in link.content:
                    print ("DETECTED CLOUDFLARE", url)
                    link = scraper.get(url)
        except:
                pass
				
        try:
                if "sucuri_cloudproxy_js" in link.content:
                        print ("DETECTED SUCURI", url)
                        su = sucuri().get(link.content)
                        headers['Cookie'] = su
                        link = session.get(url, headers=headers, params=params, data=data, allow_redirects=redirects, verify=verify, timeout=int(timeout))
        except:
                pass


        if '_Incapsula_' in link.content:
                print ("DETECTED _Incapsula_", url)
                response = session.get(url)  # url is blocked by incapsula
                link = crack(session, response)
               

        return link
		
		
def OPEN_URL_POST(url, method='get', headers=None, params=None, data=None, redirects=True, verify=True, mobile=False, timeout=None, output=None, XHR=False):
        if timeout == None: timeout = 30	
        if headers == None:

                headers = {}
                headers['User-Agent'] = random_agent()
				
        elif  mobile == True:			
				headers['User-Agent'] = ''
				headers['User-Agent'] = 'Apple-iPhone/701.341'
				
        if output == 'geturl':
                link = requests.head(url, allow_redirects=True)
                link = str(link.url)	
                return link	

        if output == 'cookie':
                cookie = [] 
                r = session.get(url, headers=headers)
                cookie_dict = session.cookies.get_dict()
                for k,v in cookie_dict.items(): cookie ="%s=%s" % (k,v)
                return cookie
        if XHR == True:
			print ("REQUESTING WITH XMLHttpRequest")
			headers['X-Requested-With'] = 'XMLHttpRequest'
			
        if not 'Accept-Language' in headers:
            headers['Accept-Language'] = 'en-US'
			
        if 'referer' in headers or 'Referer' in headers: pass
        else: headers['Referer'] = '%s://%s/' % (urlparse.urlparse(url).scheme, urlparse.urlparse(url).netloc)
        if 'User-Agent' in headers or 'user-agent' in headers: pass
        else: headers['User-Agent'] = random_agent()				
        link = session.get(url, headers=headers, params=params, data=data, allow_redirects=redirects, verify=verify, timeout=int(timeout))
        response_code = link.status_code
        print ("RESPONSE CODE", response_code)
        try: resp_header = link.headers['Server']
        except: resp_header = 'none'

				
        try:
                if resp_header.lower() == 'cloudflare-nginx' and response_code == 503 and not "sucuri_cloudproxy_js" in link.content:
                    print ("DETECTED CLOUDFLARE", url)
                    link = scraper.get(url)
        except:
                pass
				
        try:
                if "sucuri_cloudproxy_js" in link.content:
                        print ("DETECTED SUCURI", url)
                        su = sucuri().get(link.content)
                        headers['Cookie'] = su
                        link = session.get(url, headers=headers, params=params, data=data, allow_redirects=redirects, verify=verify, timeout=int(timeout))
        except:
                pass


        if '_Incapsula_' in link.content:
                print ("DETECTED _Incapsula_", url)
                response = session.get(url)  # url is blocked by incapsula
                link = crack(session, response)
               

        return link


def OPEN_POST(url, method='post', headers=None, params=None, data=None, redirects=True, verify=True, mobile=False, timeout=None, output=None, XHR=False):
        if timeout == None: timeout = 30	

        if headers == None:
                headers = {}
                headers['User-Agent'] = random_agent()
				
        elif  mobile == True:			
				headers['User-Agent'] = ''
				headers['User-Agent'] = 'Apple-iPhone/701.341'
				
        if output == 'geturl':
                link = requests.head(url, allow_redirects=True)
                link = str(link.url)	
                return link	

        if output == 'cookie':
                cookie = [] 
                r = session.get(url, headers=headers)
                cookie_dict = session.cookies.get_dict()
                for k,v in cookie_dict.items(): cookie ="%s=%s" % (k,v)
                return cookie
        if XHR == True:
			print ("REQUESTING WITH XMLHttpRequest")
			headers['X-Requested-With'] = 'XMLHttpRequest'
			
        if not 'Accept-Language' in headers:
            headers['Accept-Language'] = 'en-US'
			
        if 'referer' in headers or 'Referer' in headers: pass
        else: headers['Referer'] = '%s://%s/' % (urlparse.urlparse(url).scheme, urlparse.urlparse(url).netloc)
        if 'User-Agent' in headers or 'user-agent' in headers: pass
        else: headers['User-Agent'] = random_agent()		
        link = requests.post(url, headers=headers, params=params, data=data, allow_redirects=redirects, verify=verify, timeout=int(timeout))
        return link
		
		

def OPEN_CF(url):
        link = scraper.get(url)
        return link		
		
def random_agent():
    BR_VERS = [
        ['%s.0' % i for i in xrange(18, 43)],
        ['37.0.2062.103', '37.0.2062.120', '37.0.2062.124', '38.0.2125.101', '38.0.2125.104', '38.0.2125.111',
         '39.0.2171.71', '39.0.2171.95', '39.0.2171.99', '40.0.2214.93', '40.0.2214.111',
         '40.0.2214.115', '42.0.2311.90', '42.0.2311.135', '42.0.2311.152', '43.0.2357.81', '43.0.2357.124',
         '44.0.2403.155', '44.0.2403.157', '45.0.2454.101', '45.0.2454.85', '46.0.2490.71',
         '46.0.2490.80', '46.0.2490.86', '47.0.2526.73', '47.0.2526.80'],
        ['11.0']]
    WIN_VERS = ['Windows NT 10.0', 'Windows NT 7.0', 'Windows NT 6.3', 'Windows NT 6.2', 'Windows NT 6.1',
                'Windows NT 6.0', 'Windows NT 5.1', 'Windows NT 5.0']
    FEATURES = ['; WOW64', '; Win64; IA64', '; Win64; x64', '']
    RAND_UAS = ['Mozilla/5.0 ({win_ver}{feature}; rv:{br_ver}) Gecko/20100101 Firefox/{br_ver}',
                'Mozilla/5.0 ({win_ver}{feature}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{br_ver} Safari/537.36',
                'Mozilla/5.0 ({win_ver}{feature}; Trident/7.0; rv:{br_ver}) like Gecko']
    index = random.randrange(len(RAND_UAS))
    return RAND_UAS[index].format(win_ver=random.choice(WIN_VERS), feature=random.choice(FEATURES),
                                  br_ver=random.choice(BR_VERS[index]))


								  
								  
								  
# ======================================= GET SOURCES BLOCKS ========================================



def get_sources(txt):
	sources = re.compile('sources\s*:\s*\[(.+?)\]').findall(txt)
	return sources
	
def get_sources_content(txt):
	sources = re.compile('\{(.+?)\}').findall(txt)
	return sources
	
def get_files(txt):
	files = re.compile('''['"]?file['"]?\s*:\s*['"]([^'"]*)''').findall(txt)
	return files
	
	
	
# match = re.findall('''['"]?file['"]?\s*:\s*['"]([^'"]*)''', x) GET FILES