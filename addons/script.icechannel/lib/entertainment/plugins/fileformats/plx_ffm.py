'''
    Ice Channel
'''

from entertainment.plugnplay.interfaces import FileFormat
from entertainment.plugnplay import Plugin
from entertainment import common

code_LiveTVSource = """

    def GetFileHosts(self, id, other_names, region, language, list, lock, message_queue):
    
        import re
        ff = self.GetFileFormatObj('<file_format_name>')
        if not ff:
            return            
        
        (title, items) = ff.ReadFileForSearch(self.base_url)
        
        stws = id.lower().split('_')
        len_stws = len(stws)
        
        for item in items:
            item_name = '.' + item['name'].lower() + '.'
            matches = 0
            for stw in stws:
                if re.search("[^a-z0-9]" + stw + "[^a-z0-9]", item_name):
                    matches += 1
                else:
                    break
                    
            if matches != len_stws:
                if other_names:
                    others = other_names[1:-1].split(',')
                    for other in others:
                        other_stws = other.split('_')
                        len_other_stws = len(other_stws)
                        other_matches = 0
                        for other_stw in other_stws:
                            if re.search("[^a-z0-9]" + other_stw + "[^a-z0-9]", item_name):
                                other_matches += 1
                            else:
                                break
                                
                        if other_matches != len_other_stws:
                            continue
                        else:
                            self.AddLiveLink( list, item['name'], item['url'], host=self.name)
                            break
                    continue
                else:
                    continue
                
            self.AddLiveLink( list, item['name'], item['url'], host=self.name)

    def Resolve(self, url):
        return url
        
    def Search(self, srcr, keywords, type, list, lock, message_queue, page='', total_pages=''): 
        self.GetFileHosts(keywords, '', '', '', list, lock, message_queue)
        
"""

code_MovieSource = """

    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):                 
    
        if type != 'movies':
            return
            
        import re
        
        quality_from_plug_name = 'NA'        
        plug_name = '.' + self.name.lower() + '.'
        for key, val in common.quality_dict.items():
            if re.search('[^a-z0-9]' + key + '[^a-z0-9]', plug_name):
                quality_from_plug_name = val
                break
                
        quality_from_description = 'NA'        
        desc = '.' + self.description.lower() + '.'
        for key, val in common.quality_dict.items():
            if re.search('[^a-z0-9]' + key + '[^a-z0-9]', desc):
                quality_from_description = val
                break
        
        title = self.CleanTextForSearch(title) 
        name = self.CleanTextForSearch(name) 
        
        st = name.lower()
        stws = st.split(' ')
        len_stws = len(stws)
        
        ff = self.GetFileFormatObj('<file_format_name>')
        if not ff:
            return            
        
        (title, items) = ff.ReadFileForSearch(self.base_url)
        
        for item in items:
            item_name = '.' + item['name'].lower() + '.'
            matches = 0
            for stw in stws:
                if re.search("[^a-z0-9]" + stw + "[^a-z0-9]", item_name):
                    matches += 1
                else:
                    break
                    
            if matches != len_stws:
                continue
                
            quality = 'NA'
            # check name for quality
            for key, val in common.quality_dict.items():
                if re.search('[^a-z0-9]' + key + '[^a-z0-9]', item_name):
                    quality = val
                    break
                    
            if quality == 'NA': quality = quality_from_plug_name
            
            if quality == 'NA': quality = quality_from_description
            
            self.AddFileHost(list, quality, item['url'])

"""

code = """

from entertainment.plugnplay.interfaces import <parents>
from entertainment.plugnplay import Plugin
from entertainment import common

class <classname>(<parents>):
    implements = [<parents>]
    
    base_url = "<url>"
    name = "<name>"
    display_name = "<name>"
    description = "<description>"
    
    source_enabled_by_default = "true"
    
    def GetFileFormatObj(self, format):    
        ff = None
        
        from entertainment.plugnplay.interfaces import FileFormat
        for fs in FileFormat.implementors():
            if fs.name == format:
                ff = fs
                break
                
        return ff   

"""

class plx(FileFormat):
    implements = [FileFormat]
    
    name = "xbmcplx"
    display_name = "XBMC PLX"
    
    extensions = '.plx'
    
    def CanParse(self, raw_data):
        import re
        if re.search('type=(.*)', raw_data) and re.search('name=(.*)', raw_data) and re.search('URL=(.*)', raw_data):
            return self.ff_can_parse_yes
            
        return self.ff_can_parse_no
    
    def ParseHeader(self, data):
        title = 'NA'
        img = ''
        fanart = ''
        
        import re
        
        title_re = re.search('title=(.*)', data)
        if title_re:
            title = title_re.group(1)
            
        fanart_re = re.search('background=(.*)', data)
        if fanart_re:
            fanart = fanart_re.group(1)
            
        img_re = re.search('logo=(.*)', data)
        if img_re:
            img = img_re.group(1)
            
        return (title, img, fanart)

    def ParseData(self, data):
        title = 'NA'
        img = ''
        fanart = ''
        list = []
        
        import re
        remove_playlist_sort_item = re.search('(?s)(.+?)((?:\#|type=).*)', data)
        if remove_playlist_sort_item:
            (title, img, fanart) = self.ParseHeader(remove_playlist_sort_item.group(1))
            data = remove_playlist_sort_item.group(2)
        else:
            return (title, img, fanart, list)
            
        lines = data.splitlines()
        line_data = {}
        
        import hashlib

        for line in lines:   

            if not line or line[0] == '#' :
                if line_data and line_data.get('name', None) and line_data.get('url', None) and line_data.get('type', None): 
                    line_data['fanart'] = fanart
                    list.append(line_data)
                line_data = {}                
                continue
        
            if line.startswith('type='):
                line_data['type'] = line[5:]
                if line_data['type'] == 'rss:': line_data['type'] = 'playlist'
            elif line.startswith('name='):
                line_data['name'] = line[5:]
                line_data['title'] = line[5:]
            elif line.startswith('URL='):
                line_data_url = line[4:]
                try:
                    line_data['url'] = line_data_url
                    line_data['id'] = hashlib.md5(line_data_url.lower()).hexdigest()
                except:
                    try:
                        line_data['url'] = common.CleanText2(line_data_url, True, True)
                        line_data['id'] = hashlib.md5(line_data['url'].lower()).hexdigest()
                    except:
                        line_data['url'] = None
                        line_data['id'] = None
                        continue
            elif line.startswith('thumb='):
                line_data['img'] = line[6:]
                
        if line_data and line_data.get('name', None): 
            line_data['fanart'] = fanart
            list.append(line_data)
            line_data = {}
        
        return (title, img, fanart, list)
         
    def IsItemAList(self, item):
        return ( item['type'] == 'playlist' )
        
    def AddItem(self, item, title, name, parents):
        additional_code = ''
        if parents == 'MovieSource':
            additional_code = code_MovieSource
        elif parents == 'LiveTVSource':
            additional_code = code_LiveTVSource
        complete_code = code + additional_code
        self.Add(name, title, item['url'], complete_code, parents, item['type'], item.get('img', ''), item.get('fanart', ''), version='0.0.8')
        
    def IsItemPlayable(self, item):
        return ( item['type'] == 'video' )