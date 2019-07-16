
import re, requests
import xbmc, xbmcaddon, time, urllib
from universalscrapers.scraper import Scraper
from universalscrapers.common import clean_title, clean_search, send_log, error_log
from universalscrapers.modules import client, dom_parser, quality_tags

dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")


class seriesonline8(Scraper):
    domains = ['seriesonline8.co', 'series9.io']
    name = "SeriesOnline8"
    sources = []

    def __init__(self):
        self.base_link = 'https://www2.seriesonline8.co'
        self.search_link = '/movie/search'

    def scrape_movie(self, title, year, imdb, debrid=False):
        try:
            start_time = time.time()
            search = clean_search(title)
            start_url = '%s/%s/%s' % (self.base_link, self.search_link, search.replace(' ', '-'))
            headers={'User-Agent': client.agent()}
            html = client.request(start_url, headers=headers)
            match = re.compile('class="ml-item".+?href="(.+?)".+?alt="(.+?)"',re.DOTALL).findall(html)
            for item_url1, name in match:
                item_url = 'https://www2.seriesonline8.co'+item_url1+'/watching.html'
                if clean_title(search) == clean_title(name):
                    self.get_source(item_url, title, year, start_time)
            return self.sources
        except Exception, argument:
            if dev_log=='true':
                error_log(self.name,argument) 


    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid=False):
        try:
            start_time = time.time()
            season_chk = '-season-%s' %(season)
            search_id = clean_search(title.lower())
            start_url = '%s/%s/%s' % (self.base_link, self.search_link, search_id.replace(' ', '-'))
            headers = {'User-Agent': client.agent()}
            html = client.request(start_url, headers=headers, redirect=True)
            match = re.compile('class="ml-item".+?href="(.+?)".+?title="(.+?)"',re.DOTALL).findall(html)
            for season_url, title in match:
                if not season_chk in season_url:
                    continue
                episode_grab = 'Season %s Episode %s ' % (season, episode)
                item_url = 'https://www2.seriesonline8.co'+season_url+'/watching.html'
                self.get_source(item_url, title, episode_grab, start_time)
            return self.sources
        except Exception, argument:
            if dev_log == 'true':
                error_log(self.name, argument)


    def get_source(self, item_url, title, year, start_time):
        try:
            count = 0
            headers = {'User-Agent': client.agent()}
            OPEN = client.request(item_url, headers=headers)
            Endlinks = dom_parser.parse_dom(OPEN, 'a', req='player-data')
            Endlinks = [(i.attrs['player-data'], i.content) for i in Endlinks if i]
            if 'Season' in year:
                Endlinks = [(i[0], 'SD') for i in Endlinks if i[1] in year]
            else:
                Endlinks = [(i[0], i[1]) for i in Endlinks if i]
            for link, quality in Endlinks:
                qual = quality_tags.check_sd_url(quality)
                if 'vidcloud' in link:
                    link = 'https:' + link if link.startswith('//') else link
                    data = client.request(link, headers=headers)
                    link = re.findall('''file\s*:\s*['"](.+?)['"].+?type['"]\s*:\s*['"](.+?)['"]''', data, re.DOTALL)[0]
                    host = link[1]
                    link = link[0] + '|User-Agent=%s&Referer=https://vidcloud.icu/' % client.agent()
                    direct = True
                else:
                    host = link.split('//')[1].replace('www.', '')
                    host = host.split('/')[0].split('.')[0].title()
                    direct = False
                count += 1
                self.sources.append({'source': host, 'quality': qual, 'scraper': self.name, 'url': link, 'direct': direct})
            if dev_log == 'true':
                end_time = time.time() - start_time
                send_log(self.name, end_time, count, title, year)
        except Exception, argument:
            if dev_log=='true':
                error_log(self.name, argument)
            return[]


