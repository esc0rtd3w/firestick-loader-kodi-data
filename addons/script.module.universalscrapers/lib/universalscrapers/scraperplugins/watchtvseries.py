# -*- coding: utf-8 -*-
# Universal Scrapers Bug
#checked 29/10/2018

import re, xbmcaddon, xbmc, time
import urllib, urlparse

from universalscrapers.common import clean_title, clean_search, filter_host, send_log, error_log
from universalscrapers.scraper import Scraper
from universalscrapers.modules import client, dom_parser as dom

dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")


class Watchepisodes(Scraper):
    domains = ['watchtvseries.ag']
    name = "WatchTVseries"

    def __init__(self):
        self.base_link = 'https://watchtvseries.ag/'
        self.search_link = 'search/%s'#the%20walking%20dead
        self.sources = []

    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid=False):
        try:
            start_time = time.time()
            start_url = urlparse.urljoin(self.base_link, self.search_link % urllib.quote(clean_search(title)))
            #xbmc.log('@#@START: %s' % start_url, xbmc.LOGNOTICE)
            html = client.request(start_url)
            posts = client.parseDOM(html, 'ul', attrs={'class': 'list-group'})[0]
            posts = dom.parse_dom(posts, 'a')
            posts = [(i.attrs['href'], client.parseDOM(i, 'h3')[0]) for i in posts if show_year in i.content]
            post = [i[0] for i in posts if clean_title(title) == clean_title(i[1])][0]
            #xbmc.log('@#@POST: %s' % post, xbmc.LOGNOTICE)

            title = post[:-1].split('/')[-1] #/tvshow/328724/young-sheldon/
            tvid = post[:-1].split('/')[-2]
            epi = 'episode/%s/%01d/%01d/%s' % (tvid, int(season), int(episode), title)
            epi_link = urlparse.urljoin(self.base_link, epi)
            #xbmc.log('@#@EPI_LINK: %s' % epi_link, xbmc.LOGNOTICE)

            self.get_sources(epi_link, title, year, season, episode, start_time)

            return self.sources
        except Exception, argument:
            if dev_log == 'true':
                error_log(self.name, argument)
            return self.sources

    def get_sources(self, episode_url, title, year, season, episode, start_time):
        try:
            r = client.request(episode_url)
            links = client.parseDOM(r, 'div', attrs={'class': 'host-link'})
            try:
                links += client.parseDOM(r, 'IFRAME', ret='SRC')[0]
            except:
                pass
            count = 0
            for link in links:
                host = client.parseDOM(link, 'span')[0]
                host = client.replaceHTMLCodes(host)
                host = host.encode('utf-8')
                if not filter_host(host): continue
                # icon('ciaHR0cDovL3d3dy5zcGVlZHZpZC5uZXQvMGZvcjBqbTYwcDdzd')
                # icon(\'ciaHR0cDovL3d3dy5zcGVlZHZpZC5uZXQvMGZvcjBqbTYwcDdzd\')
                url = re.findall('''icon\(.+?(\w+).+?\)''', link, re.DOTALL)[0]
                url = urlparse.urljoin(self.base_link, '/cale/%s' % url)

                count += 1
                self.sources.append(
                    {'source': host, 'quality': 'DVD', 'scraper': self.name, 'url': url, 'direct': False})
            if dev_log == 'true':
                end_time = time.time() - start_time
                send_log(self.name, end_time, count, title, year, season=season, episode=episode)

        except Exception, argument:
            if dev_log == 'true':
                error_log(self.name, argument)
            return self.sources

    def resolve(self, link):
        try:
            from universalscrapers.modules import jsunpack
            data = client.request(link, referer=self.base_link)
            data = re.findall('\s*(eval.+?)\s*</script', data, re.DOTALL)[0]
            url = jsunpack.unpack(data)
            url = url.replace('\\', '')
            url = client.parseDOM(url, 'iframe', ret='src')[0]
            url = 'http:' + url if url.startswith('//') else url
            url = url.split('-"+')[0] if '+window' in url else url
            return url
        except:
            return link
