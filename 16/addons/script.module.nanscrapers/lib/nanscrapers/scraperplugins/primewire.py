import base64
import re,xbmcaddon,time
import urllib
import urlparse

from BeautifulSoup import BeautifulSoup
from nanscrapers import proxy
from ..common import clean_title, replaceHTMLCodes, filter_host,send_log,error_log
from ..scraper import Scraper
import xbmcaddon

dev_log = xbmcaddon.Addon('script.module.nanscrapers').getSetting("dev_log")


class Primewire(Scraper):
    domains = ['primewire.ag']
    name = "primewire"

    def __init__(self):
        self.base_link = xbmcaddon.Addon('script.module.nanscrapers').getSetting("%s_baseurl" % (self.name))
        self.search_link = '%s/index.php?search' % (self.base_link)
        self.moviesearch_link = '/index.php?search_keywords=%s&key=%s&search_section=1'
        self.tvsearch_link = '/index.php?search_keywords=%s&key=%s&search_section=2'
        if dev_log=='true':
            self.start_time = time.time()

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            html = BeautifulSoup(self.get_html(title, self.moviesearch_link))
            index_items = html.findAll('div', attrs={'class': 'index_item index_item_ie'})
            title = 'watch' + clean_title(title).replace(": ", "").replace("'", "")
            years = ['(%s)' % str(year), '(%s)' % str(int(year) + 1), '(%s)' % str(int(year) - 1)]
            fallback = None

            for index_item in index_items:
                try:
                    links = index_item.findAll('a')
                    for link in links:
                        href = link['href']
                        link_title = link['title']

                        if any(x in link_title for x in years) or not "(" in link_title:
                            try:
                                href = urlparse.parse_qs(urlparse.urlparse(href).query)['u'][0]
                            except:
                                pass
                            try:
                                href = urlparse.parse_qs(urlparse.urlparse(href).query)['q'][0]
                            except:
                                pass
                            if title.lower() == clean_title(link_title):

                                if '(%s)' % str(year) in link_title:
                                    return self.sources(href)
                                else:
                                    fallback = href

                except:
                    continue
            return []
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,'Check Search')
            return []


    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            html = BeautifulSoup(self.get_html(title, self.tvsearch_link))
            index_items = html.findAll('div', attrs={'class': re.compile('index_item.+?')})
            title = 'watch' + clean_title(" ".join(title.translate(None, '\'"?:!@#$&-,')))

            for index_item in index_items:
                try:
                    links = index_item.findAll('a')
                    for link in links:
                        href = link['href']
                        link_title = link['title']
                        try:
                            href = urlparse.parse_qs(urlparse.urlparse(href).query)['u'][0]
                        except:
                            pass
                        try:
                            href = urlparse.parse_qs(urlparse.urlparse(href).query)['q'][0]
                        except:
                            pass
                        clean_link_title = clean_title(" ".join(link_title.encode().translate(None, '\'"?:!@#$&-,')))
                        if title == clean_link_title:  # href is the show page relative url
                            show_url = urlparse.urljoin(self.base_link, href)
                            html = BeautifulSoup(proxy.get(show_url, 'tv_episode_item'))

                            seasons = html.findAll('div', attrs={'class': 'show_season'})
                            for scraped_season in seasons:
                                if scraped_season['data-id'] == season:
                                    tv_episode_items = scraped_season.findAll('div', attrs={'class': 'tv_episode_item'})
                                    for tv_episode_item in tv_episode_items:
                                        links = tv_episode_item.findAll('a')
                                        for link in links:
                                            if link.contents[0].strip() == "E%s" % episode:
                                                episode_href = link['href']
                                                try:
                                                    episode_href = \
                                                        urlparse.parse_qs(urlparse.urlparse(episode_href).query)['u'][0]
                                                except:
                                                    pass
                                                try:
                                                    episode_href = \
                                                        urlparse.parse_qs(urlparse.urlparse(episode_href).query)['q'][0]
                                                except:
                                                    pass
                                                return self.sources(episode_href)
                except:
                    continue
            return []
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,'Check Search')
            return []


    def get_key(self):
        url = self.search_link
        html = proxy.get(url, 'searchform')
        parsed_html = BeautifulSoup(html)
        key = parsed_html.findAll('input', attrs={'name': 'key'})[0]["value"]
        return key

    def get_html(self, title, search_link):
        key = self.get_key()
        query = search_link % (
        urllib.quote_plus(" ".join(title.translate(None, '\'"?:!@#$&-,').split()).rsplit(':', 1)[0]), key)
        query = urlparse.urljoin(self.base_link, query)

        html = proxy.get(query, ('index_item'))
        if 'index_item' in html:
            if 'page=2' in html or 'page%3D2' in html:
                html2 = proxy.get(query + '&page=2', 'index_item')
                html += html2
            return html

    def sources(self, url):
        sources = []
        try:
            if url == None: return sources

            url = urlparse.urljoin(self.base_link, url)
            html = proxy.get(url, 'choose_tabs')
            parsed_html = BeautifulSoup(html)

            table_bodies = parsed_html.findAll('tbody')
            count = 0
            for table_body in table_bodies:
                try:
                    link = table_body.findAll('a')[0]["href"]
                    try:
                        link = urlparse.parse_qs(urlparse.urlparse(link).query)['u'][
                            0]  # replace link with ?u= part if present
                    except:
                        pass
                    try:
                        link = urlparse.parse_qs(urlparse.urlparse(link).query)['q'][
                            0]  # replace link with ?q= part if present
                    except:
                        pass

                    link = urlparse.parse_qs(urlparse.urlparse(link).query)['url'][
                        0]  # replace link with ?url= part if present
                    link = base64.b64decode(link)  # decode base 64

                    if link.startswith("//"):
                        link = "http:" + link
                    link = replaceHTMLCodes(link)
                    link = link.encode('utf-8')

                    host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(link.strip().lower()).netloc)[0]
                    host = replaceHTMLCodes(host)
                    host = host.encode('utf-8')

                    quality = table_body.findAll('span')[0]["class"]
                    if quality == 'quality_cam' or quality == 'quality_ts':
                        quality = 'CAM'
                    elif quality == 'quality_dvd':
                        quality = 'SD'
                        
                    if not filter_host(host):
                        continue
                    count +=1
                    sources.append(
                        {'source': host, 'quality': quality, 'scraper': 'Primewire', 'url': link, 'direct': False})


                except:
                    pass
            if dev_log=='true':
                end_time = time.time() - self.start_time
                send_log(self.name,end_time,count)
            return sources
        except:
            return sources

    @classmethod
    def get_settings_xml(clas):
        xml = [
            '<setting id="%s_enabled" ''type="bool" label="Enabled" default="true"/>' % (clas.name),
            '<setting id= "%s_baseurl" type="text" label="Base Url" default="http://www.primewire.ag"/>' % (clas.name)
        ]
        return xml
