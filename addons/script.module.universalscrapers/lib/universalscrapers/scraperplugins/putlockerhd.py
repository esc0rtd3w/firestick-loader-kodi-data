# -*- coding: utf-8 -*-
# Universal Scrapers checked 30/10/2018 -BUG

import re, time
import urllib, urlparse, json
import xbmcaddon, xbmc
from universalscrapers.scraper import Scraper
from universalscrapers.common import clean_title, clean_search,send_log,error_log
from universalscrapers.modules import client, jsunpack, dom_parser as dom

dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")
User_Agent = 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'


class putlockerhd(Scraper):
    domains = ['putlockerhd.co']
    name = "PutlockerHD"
    sources = []
 
    def __init__(self):
        self.base_link = 'https://putlockerhd.co/'
        self.search_link = 'results?q=%s'

    def scrape_movie(self, title, year, imdb, debrid = False):
        links = []
        try:
            start_time = time.time() 
            search_id = urllib.quote_plus('%s %s' % (clean_search(title), year))
            start_url = urlparse.urljoin(self.base_link, self.search_link % search_id)
            html = client.request(start_url)
            posts = client.parseDOM(html, 'div', attrs={'class': 'cell_container'})
            posts = [i for i in posts if year in i]
            posts = [dom.parse_dom(i, 'a', req='href')[1] for i in posts if i]
            post = [i.attrs['href'] for i in posts if clean_title(title) == clean_title(i.content)][0]

            mov_link = urlparse.urljoin(self.base_link, post)
            r = client.request(mov_link)
            res_chk = client.parseDOM(r, 'h1')[0]

            url = re.findall('''frame_url\s*=\s*["']([^']+)['"]\;''', r, re.DOTALL)[0]
            furl = url if url.startswith('http') else urlparse.urljoin('https://', url)

            try:
                r = client.request(furl)
                ua = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:14.0) Gecko/20100101 Firefox/14.0.1'}
                id_view = client.request('https://vidlink.org/embed/update_views', headers=ua)
                id_view = json.loads(id_view)['id_view'].replace('\/', '/')
                postID = re.findall('''postID\s*=\s*['"]([^'"]+)['"]\;''', r)[0]
                try:
                    plink = 'https://vidlink.org/streamdrive/info'
                    data = {'browserName': 'Firefox',
                            'platform': 'Win32',
                            'postID': postID,
                            'id_view': id_view}
                    headers = ua
                    headers['X-Requested-With'] = 'XMLHttpRequest'
                    headers['Referer'] = url
                    ihtml = client.request(plink, post=data, headers=headers)
                    linkcode = jsunpack.unpack(ihtml).replace('\\', '')
                    linkcode = re.findall('window\.srcs\s*=\s*\[(.+?)\]\;', linkcode, re.DOTALL)[0]
                    frames = json.loads(linkcode)
                    link = frames['url']
                    links.append(link)
                except:
                    pass
                try:
                    plink = 'https://vidlink.org/opl/info'
                    post = 'postID=%s' % postID
                    headers = ua
                    headers['X-Requested-With'] = 'XMLHttpRequest'
                    headers['Referer'] = url
                    ihtml = client.request(plink, post=post, headers=headers)
                    ihtml = json.loads(ihtml)['id']
                    link = 'https://oload.icu/embed/%s' % ihtml
                    links.append(link)
                except:
                    pass
            except:
                pass

            count = 0
            #xbmc.log('@#@-LINKS:%s' % links, xbmc.LOGNOTICE)
            for link in links:
                if '1080' in res_chk:
                    res = '1080p'
                elif '720' in res_chk:
                    res = '720p'
                else:
                    res ='DVD'

                count += 1
                if 'google' in link:
                    self.sources.append({'source': 'Googlelink','quality': res,'scraper': self.name, 'url': link,'direct': True})
                else:
                    self.sources.append(
                        {'source': 'Openload', 'quality': res, 'scraper': self.name, 'url': link, 'direct': False})

                if dev_log == 'true':
                    end_time = time.time() - start_time
                    send_log(self.name,end_time,count,title,year)   
            return self.sources
        except Exception, argument:
            if dev_log == 'true':
                error_log(self.name,argument)


#putlockerhd().scrape_movie('Black Panther', '2018','')