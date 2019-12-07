import re,time,xbmcaddon,requests
from ..common import clean_title,clean_search, random_agent,send_log,error_log
from ..scraper import Scraper
from nanscrapers.modules import cfscrape
dev_log = xbmcaddon.Addon('script.module.nanscrapers').getSetting("dev_log")

class filepursuit(Scraper):
    domains = ['filepursuit.com']
    name = "FilePursuit"

    def __init__(self):
        self.base_link = 'https://filepursuit.com'
        if dev_log=='true':
            self.start_time = time.time() 
        self.scraper = cfscrape.create_scraper()
        self.sources = []

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            headers = {'User_Agent':random_agent(),'referer':self.base_link}
            grab_token = self.scraper.get(self.base_link, headers=headers,timeout=10).content
            cftok = re.compile(',petok:"(.+?)"',re.DOTALL).findall(grab_token)[0]
            #print 'check Token= '+cftok
            
            scrape = clean_search(title.lower())
            start_url = '%s/search2/%s+%s/type/videos' %(self.base_link,scrape.replace(' ','+'),year)
            #print "filepursuit start>>> " + start_url
            headers = {'User_Agent':random_agent(),'referer':self.base_link,'cf_clearance':cftok}
            results_page = self.scraper.get(start_url, headers=headers,timeout=10).content
            #print 'search page '+results_page
            grab_html = re.compile('<a href="(/file/.+?)">(.+?)</a>',re.DOTALL).findall(results_page)
            count = 0 
            pass_count = 0
            for item_url,title_info in grab_html:
                name_chk = clean_title(title).lower()+year 
                if not name_chk in clean_title(title_info).lower():
                    continue
                if 'trailer' not in item_url.lower():
                        if 'sample' not in item_url.lower():
                            item_url = self.base_link + item_url
                            pass_count +=1
                            if pass_count <=4:
                                #print 'Pass this filepursuit> '+ item_url
                                link = self.get_source(item_url)
                                if '1080' in link:
                                    res = '1080p'
                                elif '720' in link:
                                    res  = '720p'
                                else:
                                    res='DVD'
                                count +=1
                                self.sources.append({'source': 'IndexLink','quality': res,'scraper': self.name,'url': link,'direct': True})
            if dev_log=='true':
                end_time = time.time()
                total_time = end_time - self.start_time 
                send_log(self.name,total_time,count)
            return self.sources
        except Exception, argument:
            return self.sources 
        
    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid=False):
        try:
                        
            season_pull = "s0%s"%season if len(season)<2 else 's'+season
            episode_pull = "e0%s"%episode if len(episode)<2 else 'e'+episode        
            BOTH=season_pull+episode_pull
            
            headers = {'User_Agent':random_agent(),'referer':self.base_link}
            grab_token = self.scraper.get(self.base_link, headers=headers,timeout=10).content
            cftok = re.compile(',petok:"(.+?)"',re.DOTALL).findall(grab_token)[0]
            #print 'check Token= '+cftok
            
            
            scrape = clean_search(title.lower()) 
            
            start_url = '%s/search2/%s+%s/' %(self.base_link,scrape.replace(' ','+'),BOTH)
            
            #print "filepursuit start>>> " + start_url
            headers = {'User_Agent':random_agent(),'referer':self.base_link,'cf_clearance':cftok}
            results_page = self.scraper.get(start_url, headers=headers,timeout=5).content

            grab_html = re.compile('<a href="(/file/.+?)">(.+?)</a>',re.DOTALL).findall(results_page)
            count = 0 
            pass_count = 0
            for item_url,title_info in grab_html:

                name_chk = clean_title(title).lower()+BOTH 
                if not name_chk in clean_title(title_info).lower():
                    continue
                item_url = self.base_link + item_url
                #print 'Pass this filepursuit> '+ item_url
                pass_count +=1
                if pass_count <=4:
                    link = self.get_source(item_url)
                    if '1080' in link:
                        res = '1080p'
                    elif '720' in link:
                        res  = '720p'
                    else:
                        res='DVD'
                    count +=1
                    self.sources.append({'source': 'IndexLink','quality': res,'scraper': self.name,'url': link,'direct': True})
            if dev_log=='true':
                end_time = time.time()
                total_time = end_time - self.start_time 
                send_log(self.name,total_time,count)
            return self.sources
        except Exception, argument:
            return self.sources

    def get_source(self,item_url):
        try:
            headers = {'User_Agent':random_agent()}
            linkpage = self.scraper.get(item_url, headers=headers, timeout=5).content
            url = re.compile('data-clipboard-text="(.+?)"',re.DOTALL).findall(linkpage)[0]
            
            # if '1080' in link:
                # res = '1080p'
            # elif '720' in link:
                # res  = '720p'
            # else:
                # res='DVD'
            # self.sources.append({'source': 'IndexLink','quality': res,'scraper': self.name,'url': link,'direct': True})

        except:pass
        return url