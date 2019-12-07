# -*- coding: utf-8 -*-

'''
    Exodus Add-on
    adapted for nanscrapers
    Copyright (C) 2016 Exodus

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


import re,urllib,urlparse,json
from ..common import clean_title, random_agent, clean_search, replaceHTMLCodes, filter_host, get_rd_domains,send_log,error_log 
from ..scraper import Scraper
import requests
import xbmc,xbmcaddon,time  
dev_log = xbmcaddon.Addon('script.module.nanscrapers').getSetting("dev_log")

class Releasebb(Scraper):
    domains = ['rlsbb.com']
    name = "Releasebb"
    def __init__(self):
        self.domains = ['rlsbb.com']
        self.base_link = 'http://rlsbb.ru'
        self.search_base_link = 'http://search.rlsbb.ru'
        self.search_header_link = {'X-Requested-With': 'XMLHttpRequest', 'Cookie': 'serach_mode=light'}
        self.search_link = '/lib/search526049.php?phrase=%s&pindex=1&content=true'
        self.search_link2 = '/search/%s'
        if dev_log=='true':
            self.start_time = time.time() 

    def scrape_movie(self, title, year, imdb, debrid=False):
        try:
            if not debrid:
                return []
            url = self.movie(imdb, title, year)
            sources = self.sources(url, [], [])
            for source in sources:
                source["scraper"] = source["provider"]
            return sources
        except:
            return []

    def scrape_episode(self, title, show_year, year, season, episode,
                       imdb, tvdb, debrid=False):
        try:
            if not debrid:
                return []
            show_url = self.tvshow(imdb, tvdb, title, show_year)
            url = self.episode(show_url, imdb, tvdb, title,
                               year, season, episode)
            sources = self.sources(url, [], [])
            for source in sources:
                source["scraper"] = source["provider"]
            return sources
        except:
            return []

    def movie(self, imdb, title, year):
        try:
            self.elysium_url = []
            query = clean_search(title)
            cleanmovie = clean_title(title)
            query = "%s+%s" % (urllib.quote_plus(query), year)
            query = self.search_link % query
            query = urlparse.urljoin(self.search_base_link, query)
            headers = self.search_header_link
            headers["referer"] = query
            r = requests.get(query, headers=headers, timeout=10).content
            posts = []
            dupes = []
            #print ("RELEASEBB QUERY", r)

            try:
                posts += json.loads(re.findall('({.+?})$', r)[0])['results']
            except:
                pass
            for post in posts:
                try:
                    name = post['post_title'].encode('utf-8')
                    url = post['post_name'].encode('utf-8')
                    if url in dupes:
                        raise Exception()
                    dupes.append(url)
                    #print ("RELEASEBB 2", name, url)
                    t = re.sub('(\.|\(|\[|\s)(\d{4}|S\d*E\d*|S\d*|3D)(\.|\)|\]|\s|)(.+|)', '', name)

                    if cleanmovie not in clean_title(name) or not year in name:
                        raise Exception()
                    #print ("RELEASEBB 3 PASSED", t)
                    content = post['post_content']
                    url = [i for i in parse_dom(content, 'a', ret='href')]

                    size = get_size(content)
                    print 'first grab size ' + size
                    filter_size = int(size.split('.')[0])
                    if filter_size >5: 
                        raise Exception()
                    quality = quality_tag(name)
                    
                    self.elysium_url.append([size, quality, url])
                except:
                    pass
            #print("RELEASEBB PASSED", self.elysium_url)
            return self.elysium_url

        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, year):
        try:
            url = {'tvshowtitle': tvshowtitle}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            self.elysium_url = []
            if url is None:
                return
            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            title = clean_search(title)
            cleanmovie = clean_title(title)
            data['season'], data['episode'] = season, episode
            ep_query = 'S%02dE%02d' % (int(data['season']), int(data['episode']))

            titlecheck = cleanmovie+ep_query.lower()

            query = "%s+%s" % (urllib.quote_plus(title), ep_query)
            query = self.search_link % query
            query = urlparse.urljoin(self.search_base_link, query)
            headers = self.search_header_link
            headers["referer"] = query
            r = requests.get(query, headers=headers, timeout=10).content
            posts = []
            dupes = []
            #print ("RELEASEBB QUERY", r)

            try:
                posts += json.loads(re.findall('({.+?})$', r)[0])['results']
            except:
                pass
            for post in posts:
                try:
                    name = post['post_title'].encode('utf-8')
                    url = post['post_name'].encode('utf-8')
                    if url in dupes:
                        raise Exception()
                    dupes.append(url)
                    t = re.sub('(\.|\(|\[|\s)(\d{4}|S\d*E\d*|S\d*|3D)(\.|\)|\]|\s|)(.+|)', '', name)
                    #print ("RELEASEBB 3 TV", t)
                    if titlecheck not in clean_title(name):
                        raise Exception()
                    #print ("RELEASEBB 3 PASSED", t)
                    content = post['post_content']
                    url = [i for i in parse_dom(content, 'a', ret='href')]

                    size = get_size(content)
                    quality = 'getbyurl'
                    self.elysium_url.append([size, quality, url])

                except:
                    pass
            #print("RELEASEBB PASSED", self.elysium_url)
            return self.elysium_url

        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            count = 0 
            sources = []
            for size, q, urls in self.elysium_url:

                for url in urls:

                    try:
                        #print ("RELEASEBB SOURCES", size, q, url)
                        url = url.encode('utf-8')
                        if q == 'getbyurl':
                            quality = quality_tag(url)
                        else:
                            quality = q
                        loc = urlparse.urlparse(url).netloc
                        if not filter_host(loc):
                            rd_domains = get_rd_domains()
                            if loc not in rd_domains:
                                continue
                        host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
                        host = replaceHTMLCodes(host)
                        host = host.encode('utf-8')
                        count +=1
                        if '.rar' not in url:
                            print 'final url '+url
                            sources.append({'source': host, 'quality': quality, 'provider': 'Releasebb', 'url': url, 'info': size, 'direct': False, 'debridonly': True})

                    except:
                        pass
            if dev_log=='true':
                end_time = time.time() - self.start_time
                send_log(self.name,end_time,count)
            return sources
        except:
            return sources

    def resolve(self, url):
        return url


def _getDOMContent(html, name, match, ret):
    end_str = "</%s" % (name)
    start_str = '<%s' % (name)

    start = html.find(match)
    end = html.find(end_str, start)
    pos = html.find(start_str, start + 1)

    while pos < end and pos != -1:  # Ignore too early </endstr> return
        tend = html.find(end_str, end + len(end_str))
        if tend != -1:
            end = tend
        pos = html.find(start_str, pos + 1)

    if start == -1 and end == -1:
        result = ''
    elif start > -1 and end > -1:
        result = html[start + len(match):end]
    elif end > -1:
        result = html[:end]
    elif start > -1:
        result = html[start + len(match):]
    else:
        result = ''

    if ret:
        endstr = html[end:html.find(">", html.find(end_str)) + 1]
        result = match + result + endstr

    return result


def _getDOMAttributes(match, name, ret):
    pattern = '''<%s[^>]* %s\s*=\s*(?:(['"])(.*?)\\1|([^'"].*?)(?:>|\s))''' % (name, ret)
    results = re.findall(pattern, match, re.I | re.M | re.S)
    return [result[1] if result[1] else result[2] for result in results]


def _getDOMElements(item, name, attrs):
    if not attrs:
        pattern = '(<%s(?: [^>]*>|/?>))' % (name)
        this_list = re.findall(pattern, item, re.M | re.S | re.I)
    else:
        last_list = None
        for key in attrs:
            pattern = '''(<%s [^>]*%s=['"]%s['"][^>]*>)''' % (name, key, attrs[key])
            this_list = re.findall(pattern, item, re.M | re. S | re.I)
            if not this_list and ' ' not in attrs[key]:
                pattern = '''(<%s [^>]*%s=%s[^>]*>)''' % (name, key, attrs[key])
                this_list = re.findall(pattern, item, re.M | re. S | re.I)

            if last_list is None:
                last_list = this_list
            else:
                last_list = [item for item in this_list if item in last_list]
        this_list = last_list

    return this_list


def parse_dom(html, name='', attrs=None, ret=False):
    if attrs is None:
        attrs = {}
    if isinstance(html, str):
        try:
            html = [html.decode("utf-8")]  # Replace with chardet thingy
        except:
            print "none"
            try:
                html = [html.decode("utf-8", "replace")]
            except:

                html = [html]
    elif isinstance(html, unicode):
        html = [html]
    elif not isinstance(html, list):

        return ''

    if not name.strip():

        return ''

    if not isinstance(attrs, dict):

        return ''

    ret_lst = []
    for item in html:
        for match in re.findall('(<[^>]*\n[^>]*>)', item):
            item = item.replace(match, match.replace('\n', ' ').replace('\r', ' '))

        lst = _getDOMElements(item, name, attrs)

        if isinstance(ret, str):
            lst2 = []
            for match in lst:
                lst2 += _getDOMAttributes(match, name, ret)
            lst = lst2
        else:
            lst2 = []
            for match in lst:
                temp = _getDOMContent(item, name, match, ret).strip()
                item = item[item.find(temp, item.find(match)):]
                lst2.append(temp)
            lst = lst2
        ret_lst += lst

    # log_utils.log("Done: " + repr(ret_lst), xbmc.LOGDEBUG)
    return ret_lst


def get_size(txt):
    try:
        txt = re.findall('(\d+(?:\.|/,|)?\d+(?:\s+|)(?:GB|GiB|MB|MiB))', txt)
        txt = txt[0].encode('utf-8')
    except:
        txt = ''
    return txt


def quality_tag(txt):
    if any(value in txt for value in ['1080', '1080p','1080P']):
        quality = "1080p"
    elif any(value in txt for value in ['720', '720p','720P']):
        quality = "HD"
    else:
        quality = "SD"
    return quality
