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

class xbmcxml(FileFormat):
    implements = [FileFormat]
    
    name = "xbmcxml"
    display_name = "XBMC XML"
    
    extensions = '.xml'
    
    def CanParse(self, raw_data):
        import re
        
        if re.search('<poster>(.+?)</poster>', raw_data) and re.search('<name>|<item>|<dir>|<title>|<info>|<message>', raw_data):
            return self.ff_can_parse_yes
            
        return self.ff_can_parse_no
    
    def ParseHeader(self, data):
        title = 'NA'
        img = ''
        fanart = ''

        import re
        title_re = re.search('<poster>(.+?)</poster>', data)
        if title_re:
            title = title_re.group(1)
            
        fanart_re = re.search('<fanart>(.+?)</fanart>', data)
        if fanart_re:
            fanart = fanart_re.group(1)
            
        return (title, img, fanart)
        
    def ParseData(self, data):
        title = 'NA'
        img = ''
        fanart = ''
        list = []
        
        import re
        remove_header_item = re.search('(?s)(.+?)((?:<name>|<item>|<dir>|<title>|<info>|<message>).*)', data)
        if remove_header_item:
            (title, img, fanart) = self.ParseHeader(remove_header_item.group(1))
            data = remove_header_item.group(2)
            
        else:
            return (title, img, fanart, list)
        
        data = data.replace('&nbsp;',' ')
        data = re.sub('>[ \t\n\r\f\v]+<', '><', data)
        data = re.sub('[\t\n\r\f\v]+', '', data)

        data = re.sub('<(\w+)>', '\n<\g<1>>', data)
        data = re.sub('</(\w+)>', '</\g<1>>\n', data)

        data = re.sub('[\n]{2,}', '\n', data)

        lines = data.splitlines()
        line_data = {}
        sublinks = []
        
        import hashlib
        
        for line in lines:  
            line = line.strip()
            if (not line) or ( (line.startswith('<name>') or line.startswith('<title>') or line.startswith('<message>')  or line.startswith('<item>') or line.startswith('<dir>') or line.startswith('<info>') ) and line_data and line_data.get('name', None)):
                if line_data and line_data.get('name', None): 
                    if line_data.get('type', None) and line_data.get('type', None) == 'playlist' and line_data.get('url', None) and not re.search( '.+?[/\\\\]{1}.+?', line_data.get('url', 'dummy')):
                        line_data['type'] = 'info'
                    if ( line_data.get('url', None) or line_data.get('type', None) == 'info' ) and line_data.get('type', None)   :
                        line_data['fanart'] = fanart
                        list.append(line_data)
                        line_data = {}
                    elif sublinks:
                        line_data['type'] = 'video'
                        line_data['fanart'] = fanart
                        for sublink in sublinks:
                            sub_line_data = line_data
                            line_data.update({'url':sublink})
                            line_data['id'] = hashlib.md5(sublink).hexdigest()
                            list.append(line_data.copy())
                        sublinks = []
                        line_data = {}
                if not line: continue
            
            if line.startswith('<dir>'):
                line_data['type'] = 'playlist'
            elif line.startswith('<item>'):
                line_data['type'] = 'video'
            elif line.startswith('<message>'):
                l_name = re.search('<message>(.*)</message>', line)
                if not l_name: continue
                l_name = l_name.group(1)
                if not l_name: continue
                line_data['name'] = l_name
                line_data['title'] = line_data['name']
                line_data['type'] = 'info'                
            elif line.startswith('<name>'):
                l_name = re.search('<name>(.*)</name>', line)
                if not l_name: continue
                l_name = l_name.group(1)
                if not l_name: continue
                line_data['name'] = l_name
                line_data['title'] = line_data['name']
                line_data['type'] = 'playlist'
            elif line.startswith('<title>'):
                l_name = re.search('<title>(.*)</title>', line)
                if not l_name: continue
                l_name = l_name.group(1)
                if not l_name: continue
                line_data['name'] = l_name
                line_data['title'] = line_data['name']
                line_data['type'] = 'video'
            elif line.startswith('<link>') and '</link>' in line:
                l_link = re.search('<link>(.*)</link>', line)
                if not l_link: continue
                l_link = l_link.group(1)
                if not l_link: continue
                l_link = l_link.strip()
                if l_link.startswith('<sublink>'):

                    for sublink in re.finditer('<sublink>(.+?)</sublink>', l_link):
                        if not sublink: continue
                        sublink = sublink.group(1)
                        if not sublink: continue                        

                        sublinks.append(sublink)
                else:                    
                    line_data['url'] = l_link
                    line_data['id'] = hashlib.md5(line_data['url'].lower()).hexdigest()
                    if not line_data.get('type', None):
                        if line_data['url'].endswith('.xml'):
                            line_data['type'] = 'playlist'
                        else:
                            line_data['type'] = 'video'
            elif line.startswith('<link>') and '</link>' not in line:
                continue
            elif line.startswith('<sublink>'):            
                for sublink in re.finditer('<sublink>(.+?)</sublink>', line):
                    if not sublink: continue
                    sublink = sublink.group(1)
                    if not sublink: continue
                    sublinks.append(sublink)    
            elif line.startswith('<thumbnail>'):
                l_thumb = re.search('<thumbnail>(.*)</thumbnail>', line)
                if not l_thumb: continue
                line_data['img'] = l_thumb.group(1)
        
        if line_data and line_data.get('name', None): 
            if line_data.get('type', None) and line_data.get('type', None) == 'playlist' and line_data.get('url', None) and not re.search( '.+?[/\\\\]{1}.+?', line_data.get('url', 'dummy')):
                line_data['type'] = 'info'
            if ( line_data.get('url', None) or line_data.get('type', None) == 'info') and line_data.get('type', None)   :
                line_data['fanart'] = fanart
                list.append(line_data)
                line_data = {}
            elif sublinks:
                line_data['type'] = 'video'
                line_data['fanart'] = fanart
                for sublink in sublinks:
                    sub_line_data = line_data
                    line_data.update({'url':sublink})
                    line_data['id'] = hashlib.md5(sublink).hexdigest()
                    list.append(line_data.copy())
                sublinks = []
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
        self.Add(name, title, item['url'], complete_code, parents, item['type'], item.get('img', ''), item.get('fanart', ''), version='0.0.7')
        
    def IsItemPlayable(self, item):
        return ( item['type'] == 'video' )