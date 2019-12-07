# -*- coding: UTF-8 -*-
#######################################################################
 # ----------------------------------------------------------------------------
 # "THE BEER-WARE LICENSE" (Revision 42):
 # @Daddy_Blamo wrote this file.  As long as you retain this notice you
 # can do whatever you want with this stuff. If we meet some day, and you think
 # this stuff is worth it, you can buy me a beer in return. - Muad'Dib
 # ----------------------------------------------------------------------------
#######################################################################

# Addon Name: Placenta
# Addon id: plugin.video.placenta
# Addon Provider: Mr.Blamo

import requests, re, traceback,urllib, urlparse
from bs4 import BeautifulSoup
from resources.lib.modules import client
from resources.lib.modules import source_utils
from resources.lib.modules import log_utils
from resources.lib.modules import debrid


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domain = 'rlsscn.in'
        self.base_link = 'http://tvdownload.net/'
        self.search_link = self.base_link+'?s=%s'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            return url
        except:
            failure = traceback.format_exc()
            log_utils.log('RLSSCN - Exception: \n' + str(failure))
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            url['episode'] = episode
            url['season'] = season
            url['premiered'] = premiered
            return url
        except:
            failure = traceback.format_exc()
            log_utils.log('RLSSCN - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            hostDict = hostDict + hostprDict
        
            log_utils.log("RLSSCN debug")
            
            sources      = []
            query_bases  = []
            options      = []
            html         = None

            log_utils.log("RLSSCN url : "+ str(url))

            if url == None: return sources

            if debrid.status() == False: raise Exception()

            data = url
            #data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])        
            title = (data['tvshowtitle'] if 'tvshowtitle' in data else data['title'])
            hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']
            premDate = ''

            # tvshowtitle
            if 'tvshowtitle' in data: 
                query_bases.append('%s ' % (data['tvshowtitle']))  # (ex 9-1-1 become 911)
                # tvshowtitle + year (ex Titans-2018-s01e1 or Insomnia-2018-S01)
                query_bases.append('%s %s ' % (data['tvshowtitle'], data['year']))

                # season and episode (classic)
                options.append('S%02dE%02d' % (int(data['season']), int(url['episode'])))
                # season space episode (for double episode like S02E02-E03)
                options.append('S%02d E%02d' % (int(data['season']), int(data['episode'])))
                # season and episode1 - epsiode2 (two episodes at a time)
                #options.append('S%02dE%02d-E%02d' % (int(data['season']), int(data['episode']),   int(data['episode'])+1))
                #options.append('S%02dE%02d-E%02d' % (int(data['season']), int(data['episode'])-1, int(data['episode'])))
                # season only (ex ozark-S02, group of episodes)
                options.append('S%02d' % (int(data['season'])))

                html = self.search(query_bases, options)

            else:
                #log_utils.log("RLSSCN Movie")
                #  Movie
                query_bases.append('%s ' % (data['title']))
                options.append('%s' % (data['year']))
                html = self.search(query_bases, options)
       
            # this split is based on TV shows, soooo... might screw up movies
            # grab the relevent div and chop off the footer
            if html != None:
            	html = client.parseDOM(html, "div", attrs={"id": "content"})[0]
            	html = re.sub('class="wp-post-navigation.+','', html, flags=re.DOTALL)
            	sects = html.split('<p>')

            	log_utils.log("RLSSCN html links : " + str(sects))

            	for sect in sects:
                	hrefs = client.parseDOM(sect, "a", attrs={"class": "autohyperlink"}, ret='href')
                	if not hrefs: continue
        
                	# filenames (with useful info) seem predictably located
                	try: fn = re.match('(.+?)</strong>',sect).group(1)
                	except: fn = ''
                	log_utils.log('*** fn: %s' % fn)
            
                	# sections under filenames usually have sizes (for tv at least)
                	size = ""
                	try: 
                    	size = re.findall('([0-9,\.]+ ?(?:GB|GiB|MB|MiB))', sect)[0]
                    	div = 1 if size.endswith(('GB', 'GiB')) else 1024
                    	size = float(re.sub('[^0-9\.]', '', size)) / div
                    	size = '%.2f GB' % size
                	except: pass
            
                	for url in hrefs:
                    	quality, info = source_utils.get_release_quality(url,fn)
                    	info.append(size)
                    	info = ' | '.join(info)
                    	log_utils.log(' ** (%s %s) url=%s' % (quality,info,url)) #~~~~~~~~~~~

                    	url = url.encode('utf-8')
                    	hostDict = hostDict + hostprDict

                    	valid, host = source_utils.is_host_valid(url, hostDict)
                    	if not valid: continue
                
                    	log_utils.log(' ** VALID! (host=%s)' % host) #~~~~~~~~~~~~~~~
                    	sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url,
                                		'info': info, 'direct': False, 'debridonly': False})

            return sources
        except:
            log_utils.log("RLSSCN oups..." + str(traceback.format_exc()))

    def search(self, query_bases, options):
        i = 0
        j = 0
        result = None
        for option in options:
            
            for query_base in query_bases :
                q = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', '', query_base+option)
                q = q.replace("  ", " ").replace(" ", "+")

                log_utils.log("RLSSCN query : " + q)
                
                url = self.search_link % (q)
                html = requests.get(url)

                log_utils.log("RLSSCN try test " + str(i) + " - html : " + str(html))

                if html.status_code == 200 :
                    log_utils.log("RLSSCN test " + str(i) + " Ok")
                    url = client.parseDOM(html.content, "h2", attrs={"class": "title"})
                    url = client.parseDOM(url, "a", ret='href')
                    log_utils.log("RLSSCN test " + str(i) + " : " + str(url))
                    if len(url) > 0:
                    	html = requests.get(url[0])
                    	if html.status_code == 200 :
                        	return html.content
                else :    
                    log_utils.log("RLSSCN test "+ str(i) + " return code : " + result.status_code + "- next test " + str(i+1))
                    i += 1
                    
        return None

    def resolve(self, url):
        return url

