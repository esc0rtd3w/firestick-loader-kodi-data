'''
    Ice Channel
'''

from entertainment.plugnplay.interfaces import FileFormat
from entertainment.plugnplay import Plugin
from entertainment import common

class rss(FileFormat):
    implements = [FileFormat]
    
    name = "rss"
    display_name = "RSS FEED"
    
    extensions = '.rss'
    
    def CanParse(self, raw_data):
        try:
            import feedparser
            fp = feedparser.parse(raw_data)
            title = fp['feed']['title']
            print title
            return self.ff_can_parse_maybe
        except:
            pass
        
        return self.ff_can_parse_no
    
    def ParseHeader(self, data):
        title = 'NA'
        img = ''
        fanart = ''
        
        try:
            import feedparser
            fp = feedparser.parse(data)
            title = fp['feed']['title']
            print title
        except:
            pass
            
        return (title, img, fanart)

    def ParseData(self, data):
        title = 'NA'
        img = ''
        fanart = ''
        list = []
        
        try:
            import feedparser
            fp = feedparser.parse(data)
            
            title = fp['feed']['title']
            
            import hashlib
            
            for entry in fp.entries:
                
                line_data = {}
                
                line_data['type'] = 'video'
                line_data['name'] = entry.title
                line_data['title'] = entry.title                
                line_data['fanart'] = ''
                line_data['img'] = ''
                
                for link in entry['links']:
                    if 'video' in link['type'].lower():
                        line_data['url'] = link['href']
                        line_data['id'] = hashlib.md5(link['href'].lower()).hexdigest()
                        
                        list.append(line_data)
                
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