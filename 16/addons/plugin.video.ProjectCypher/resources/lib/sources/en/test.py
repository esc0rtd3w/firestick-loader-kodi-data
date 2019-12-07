import re,urllib,urlparse

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import log_utils
from resources.lib.modules import source_utils

class source:
    def __init__(self):
        self.priority = 0
        self.language = ['en']
        self.domains = ['dwatchseries.to']                                                                   # List of base urls, such as 'filmfrantic.com'
        self.base_link = 'https://dwatchseries.to/'                                                                      # Base URL, such as 'http://filmfrantic.com'
        self.search_link = '/search/%s'                                                        # part of link on search results page, with %s on any portion where you need to insert title, year, etc.
                                                                                                                # Example: '/s=%s'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            search_id = cleantitle.getsearch(title)                                                             # use 'getsearch' to get clean title 
            log_utils.log('test - Movie - title: ' + str(title))
            log_utils.log('test - Movie - search_id: ' + str(search_id))

            url = urlparse.urljoin(self.base_link, self.search_link)                                            # Here, we combine the base link and search link into a single url
            url = url  % (search_id.replace(':', ' ').replace(' ', '%20'))                                        # This is optional, some sites use + in place of spaces of search url, some use -, and so on.
            log_utils.log('test - Movie - url: ' + str(url))

            search_results = client.request(url)                                                                # Pulls the webpage HTML for search results
            match = re.compile('<a href="(.+?)" title=".+?" target="_blank"><strong>(.+?)</strong></a>',re.DOTALL).findall(search_results)   # Regex info on results page
            for row_url, row_title in match:                                                                    # Each (.+?) gets pulled, so if pulling multiple items in the Regex, have a variable in this line for each
                log_utils.log('test - Movie - row_url: ' + str(row_url))
                log_utils.log('test - Movie - row_title: ' + str(row_title))
                if cleantitle.get(title) in cleantitle.get(row_title):                                          # Cleans title and results title to compare them. They should match if the same movie
                    if year in str(row_title):                                                                  # This line checks for Year, to make sure title is from same year
                        return row_url                                                                          # Returns the url to the page if all matches up. URL is passed to the "sources()" function below to use
            return
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url == None: return sources                                                                      # if no link returned in movie and tvshow searches, nothing to do here, return out.
           log_utils.log('test - Sources - url: ' + str(url))

            html = client.request(url)                                                                          # Get the HTML for the page

            links = re.compile(' <iframe src="(.+?)"',re.DOTALL).findall(html)                                  # Regex info on the html page

            for link in links:
                log_utils.log('test - Sources - link: ' + str(link))
                quality,info = source_utils.get_release_quality(link, url)                                      # Run two strings through this to try to pull Quality and info on the file (such as 1080p, etc)
                log_utils.log('test - Sources - quality: ' + str(quality))
                log_utils.log('test - Sources - info: ' + str(info))
                host = link.split('//')[1].replace('www.','')                                                   # These two lines work to get the Host of the file
                host = host.split('/')[0].split('.')[0].title()                                                 # These two lines work to get the Host of the file
                log_utils.log('test - Sources - host: ' + str(host))
                sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': link, 'info': info, 'direct': False, 'debridonly': False})
            return sources
        except:
            return sources

    def resolve(self, url):
        return url