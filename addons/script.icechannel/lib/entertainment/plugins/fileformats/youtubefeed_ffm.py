'''
    Ice Channel
'''

from entertainment.plugnplay.interfaces import FileFormat
from entertainment.plugnplay import Plugin
from entertainment import common

class youtubefeed(FileFormat):
    implements = [FileFormat]
    
    name = "youtubefeed"
    display_name = "YOUTUBE FEED"
    
    extensions = '.rss'
    
    def CanParseRawData(self):
        return False
    
    def CanParse(self, raw_data):
        import re
        
        xmlns_re = re.search("xmlns.yt.{1,2}[\"']http\://gdata\.youtube\.com/schemas/", raw_data)
        
        if xmlns_re:        
            return self.ff_can_parse_yes
            
        return self.ff_can_parse_no
    
    def ReadHttpFile(self, path):
        from entertainment.net import Net
        net = Net( cached = True if common.addon.get_setting('cache_playlists')=='true' else False )
        
        http_response = net.http_GET(path, auto_read_response=False)
        feed_url = http_response.get_url()
        feed_queries = ''
        
        q_index = feed_url.find('?')
        if q_index >= 0:
            feed_queries = feed_url[q_index+1:]
            feed_url = feed_url[:q_index]            

        refetch = False
        
        feed_queries = common.parse_query(feed_queries)
        
        feed_query_v = feed_queries.get('v', None)
        if not feed_query_v or feed_query_v != '2':
            feed_queries.update({'v':'2'})
            refetch = True
            
        feed_query_alt = feed_queries.get('alt', None)
        if not feed_query_alt or feed_query_alt != 'json':
            feed_queries.update({'alt':'json'})
            refetch = True
            
        feed_query_start_index = feed_queries.get('start-index', None)
        if not feed_query_start_index:
            feed_queries.update({'start-index':'1'})
            refetch = True
            
        feed_query_max_results = feed_queries.get('max-results', None)
        if not feed_query_max_results:
            feed_queries.update({'max-results':'50'})
            refetch = True
        
        if refetch:
            feed_url = feed_url + '?' + common.dict_to_paramstr(feed_queries)
            http_response = net.http_GET(feed_url, auto_read_response=False)
        
        
        content = http_response.read_response()
        
        return content
    
    def ParseHeader(self, data):
        
        title = 'NA'
        img = ''
        fanart = ''
        
        try:
            import json
        except:
            import simplejson as json
            
        parsed_data = json.loads(data)
        
        title = parsed_data['feed']['title']['$t']
            
        return (title, img, fanart)

    def ParseData(self, data):
        title = 'NA'
        img = ''
        fanart = ''
        list = []
        
        try:
            try:
                import json
            except:
                import simplejson as json
                
            parsed_data = json.loads(data)
            
            feed = parsed_data['feed']
            title = feed['title']['$t']
            
            import hashlib
            
            previous_item = {}
            next_item = {}
            
            links = feed['link']
            for link in links:
                if link['rel'] == 'previous':
                    previous_item = { 'type':'playlist', 'name':'<< Previous', 'title':'<< Previous', 'fanart':'', 'img':'', 
                        'url':link['href'], 'id':hashlib.md5(link['href'].lower()).hexdigest()}
                elif link['rel'] == 'next':
                    next_item = { 'type':'playlist', 'name':'Next >>', 'title':'Next >>', 'fanart':'', 'img':'', 
                        'url':link['href'], 'id':hashlib.md5(link['href'].lower()).hexdigest()}
            
            #if previous_item: list.append(previous_item)
            
            entries = feed['entry']
            
            for entry in entries:
            
                #print entry
                
                line_data = {}
                
                entry_media_player = entry.get('media$player', None)
                entry_id = entry['id']['$t']
                entry_content = entry.get('content', None)
                entry_content_src = None if not entry_content else entry_content.get('src', None)
                entry_link = entry.get('link', None)
                
                if entry_media_player or 'video' in entry_id or ( entry_content and entry_content_src and entry_content_src.startswith('http://www.youtube.com/v/') ) or ( entry_link and entry_link[0]['href'].startswith('http://www.youtube.com/watch?v=') ):
                    line_data['type'] = 'video'
                elif 'subscription' in entry_id:
                    line_data['type'] = 'subscriptions'
                else:
                    line_data['type'] = 'playlist'
                
                line_data['name'] = entry['title']['$t']
                line_data['title'] = entry['title']['$t']
                line_data['fanart'] = ''
                
                len_media = 0
                media_group = entry.get('media$group', None)
                if media_group:
                    media = media_group.get('media$thumbnail', None)
                    if media:
                        len_media = len(media)
                line_data['img'] = media[len_media-1]['url'] if len_media > 0 else ''
                
                if line_data['type'] == 'playlist':
                    if entry_content and entry_content_src:
                        line_data['url'] = entry_content_src
                    else:
                        continue
                elif line_data['type'] == 'video':
                    if entry_content and entry_content_src:
                        line_data['url'] = entry_content_src
                    elif entry_link:
                        line_data['url'] = entry_link[0]['href']
                    elif entry_media_player:
                        line_data['url'] = entry_media_player['url']
                    else:
                        continue
                elif line_data['type'] == 'subscriptions':
                    if entry_link:
                        
                        upl_link = ''
                        alt_link = ''
                        print line_data
                        for el in entry_link:
                            if 'uploads' in el['rel']:
                                upl_link = el['href']
                            elif 'alternate' in el['rel']:
                                alt_link = el['href']
                                
                        print upl_link
                        print alt_link
                        
                        if alt_link and 'videos' in alt_link:
                            if upl_link:
                                line_data['url'] = upl_link.replace('uploads', 'playlists')
                            else:
                                continue
                        elif upl_link:
                            line_data['url'] = upl_link
                        else:
                            continue
                            
                        line_data['type'] = 'playlist'
                        
                    else:
                        continue
                else:
                    continue
                        
                
                if line_data['url'].startswith('http://www.youtube.com/v/'): 
                    line_data['type'] = 'video'
                    import re
                    video_id = re.search('http://www.youtube.com/v/(.+?)\?', line_data['url']).group(1)
                    line_data['url'] = 'http://www.youtube.com/watch?v=' + video_id + '&feature=youtube_gdata'
                    
                line_data['id'] = hashlib.md5(line_data['url'].lower()).hexdigest()
                
                #print line_data
                
                list.append(line_data)
                
            if next_item: list.append(next_item)
                
        except:
            pass
            
        return (title, img, fanart, list)
         
    def IsItemAList(self, item):
        return ( item['type'] == 'playlist' )
        
    def AddItem(self, item, title, name, parents):
        self.Add(name, title, item['url'], code, parents, item['type'], item.get('img', ''), item.get('fanart', ''), version='0.0.1')
        
    def IsItemPlayable(self, item):
        return ( item['type'] == 'video' )
        
    def IsISTREAMImportSupported(self):
        return False