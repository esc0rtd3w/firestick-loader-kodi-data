# -*- coding: utf-8 -*-
# Universal Scrapers Bug
#checked 29/10/2018

import re, xbmcaddon, xbmc, time
import urllib, urlparse

from universalscrapers.common import clean_title, filter_host, clean_search, send_log, error_log
from universalscrapers.scraper import Scraper
from universalscrapers.modules import client, dom_parser as dom, jsunpack

dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")

class Watchepisodes(Scraper):
    domains = ['www.primewire.site']
    name = "Primewire"

    def __init__(self):
        self.base_link = 'https://www.primewire.site/'
        self.moviesearch_link = '?search_keywords=%s'
        self.tvsearch_link = '?tv=&search_keywords=%s'
        self.sources = []

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            start_time = time.time()
            start_url = urlparse.urljoin(self.base_link, self.moviesearch_link % urllib.quote_plus(clean_search(title)))

            html = client.request(start_url)
            posts = client.parseDOM(html, 'div', attrs={'class': 'index_item.+?'})
            posts = [(dom.parse_dom(i, 'a', req='href')[0]) for i in posts if i]
            post = [(i.attrs['href']) for i in posts if clean_title(title) == clean_title(re.sub('(\.|\(|\[|\s)(\d{4})(\.|\)|\]|\s|)(.+|)', '', i.attrs['title'], re.I))][0]
            #xbmc.log('@#@POST: %s' % post, xbmc.LOGNOTICE)

            self.get_sources(post, title, year, '', '', start_time)
            return self.sources
        except Exception as argument:
            if dev_log == 'true':
                error_log(self.name,argument)
            return[]

    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid=False):
        try:
            start_time = time.time()
            start_url = urlparse.urljoin(self.base_link, self.tvsearch_link % urllib.quote_plus(clean_search(title)))
            #xbmc.log('@#@START: %s' % start_url, xbmc.LOGNOTICE)
            html = client.request(start_url)
            posts = client.parseDOM(html, 'div', attrs={'class': 'index_item.+?'})
            posts = [(dom.parse_dom(i, 'a', req='href')[0]) for i in posts if i]
            post = [(i.attrs['href']) for i in posts if clean_title(title) == clean_title(re.sub('(\.|\(|\[|\s)(S\d+E\d+|S\d+)(\.|\)|\]|\s|)(.+|)', '', i.attrs['title'], re.I))][0]

            r = client.request(post)
            r = client.parseDOM(r, 'div', attrs={'class': 'tv_episode_item'})

            urls = client.parseDOM(r, 'a', ret='href')
            epi_link = [i for i in urls if 'season-%s-episode-%s' % (int(season), int(episode)) in i][0]
            #xbmc.log('@#@EPI-LINK: %s' % epi_link, xbmc.LOGNOTICE)
            self.get_sources(epi_link, title, year, season, episode, start_time)

            return self.sources
        except Exception, argument:
            if dev_log == 'true':
                error_log(self.name, argument)
            return self.sources

    def get_sources(self, url, title, year, season, episode, start_time):
        try:
            count = 0
            url = urlparse.urljoin(self.base_link, url) if url.startswith('/') else url

            r = client.request(url)
            data = re.findall(r'\s*(eval.+?)\s*</script', r, re.DOTALL)[1]
            data = jsunpack.unpack(data).replace('\\', '')

            # https://www.primewire.ink/ajax-78583.php?slug=watch-2809620-Black-Panther&cp=7TYP4N
            # var rtv=\'aja\';var aa=\'x-7\';var ba=\'85\';var ca=\'83\';var da=\'.ph\';var ea=\'p?sl\';var fa=\'ug=\';var ia=\'&cp=7T\';var ja=\'YP\';var ka=\'4N\';var code=ia+ja+ka;var page=rtv+aa+ba+ca+da+ea+fa;function goml(loc){$(\'#div1\').load(domain+page+loc+code)}
            patern = '''rtv='(.+?)';var aa='(.+?)';var ba='(.+?)';var ca='(.+?)';var da='(.+?)';var ea='(.+?)';var fa='(.+?)';var ia='(.+?)';var ja='(.+?)';var ka='(.+?)';'''
            links_url = re.findall(patern, data, re.DOTALL)[0]
            slug = 'slug={}'.format(url.split('/')[-1])
            links_url = self.base_link + [''.join(links_url)][0].replace('slug=', slug)
            links = client.request(links_url)
            links = client.parseDOM(links, 'tbody')

            #xbmc.log('@#@LINKSSSS: %s' % links, xbmc.LOGNOTICE)
            for link in links:
                try:
                    data = [(client.parseDOM(link, 'a', ret='href')[0],
                             client.parseDOM(link, 'span', attrs={'class': 'version_host'})[0])][0]
                    link = urlparse.urljoin(self.base_link, data[0])

                    host = data[1]

                    if not filter_host(host): continue

                    self.sources.append(
                        {'source': host, 'quality': 'SD', 'scraper': self.name, 'url': link, 'direct': False})
                except:
                    pass
            if dev_log == 'true':
                end_time = time.time() - start_time
                send_log(self.name, end_time, count, title, year, season=season, episode=episode)

        except Exception, argument:
            if dev_log == 'true':
                error_log(self.name, argument)
            return self.sources

    def resolve(self, url):
        try:
            # url = 'https://primewire.ink/go.php?title=Black-Panther&url=efdf73e70e3dc1c530e983a5bb2414365d813086==&id=384919&loggedin=0'
            if '/stream/' in url or '/watch/' in url:
                # r = self.scraper.get(url, self.headers).text
                r = client.request(url, referer=self.base_link)
                link = client.parseDOM(r, 'a', ret='data-href', attrs={'id': 'iframe_play'})[0]
            else:
                try:
                    # data = self.scraper.get(url, self.headers).text
                    data = client.request(url, referer=self.base_link)
                    data = re.findall(r'\s*(eval.+?)\s*</script', data, re.DOTALL)[0]
                    link = jsunpack.unpack(data)
                    link = link.replace('\\', '')
                    if 'eval' in link:
                        link = jsunpack.unpack(link)
                    link = link.replace('\\', '')
                    host = re.findall('hosted=\'(.+?)\';var', link, re.DOTALL)[0]
                    if 'streamango' in host:
                        loc = re.findall('''loc\s*=\s*['"](.+?)['"]''', link, re.DOTALL)[0]
                        link = 'https://streamango.com/embed/{0}'.format(loc)
                    elif 'openload' in host:
                        loc = re.findall('''loc\s*=\s*['"](.+?)['"]''', link, re.DOTALL)[0]
                        link = 'https://openload.co/embed/{0}'.format(loc)
                    else:
                        link = re.findall('''loc\s*=\s*['"](.+?)['"]\;''', re.DOTALL)[0]
                except BaseException:
                    link = client.request(url, output='geturl', timeout=10)
                    print link
                    if link == url:
                        return
                    else:
                        return link

            return link
        except BaseException:
            return
