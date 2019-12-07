'''
    Ice Channel
    Furk.Net
'''
import os
import xbmc, xbmcaddon, xbmcgui, xbmcplugin

from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay.interfaces import CustomSettings
from entertainment.plugnplay import Plugin
from entertainment import common
import re

class FurkDotNet(MovieSource, TVShowSource, CustomSettings):
    implements = [MovieSource, TVShowSource, CustomSettings]
    
    name = "Furk.Net"
    display_name = "Furk.Net"
    
    api_url = "http://api.furk.net"
    
    source_enabled_by_default = 'false'
    
    auto_play_supported = False
    
    def __init__(self):
        xml = '<settings>\n'
        xml += '<category label="Account">\n'
        xml += '<setting id="furk_user" type="text" label="Username" default="" />\n'
        xml += '<setting id="furk_pwd" type="text" option="hidden" label="Password" default="" />\n'
        xml += '<setting type="sep" />\n'
        xml += '<setting id="furk_adult_filter" type="bool" label="Adult Filter" default="true"/>\n'
        xml += '</category>\n' 
        xml += '<category label="Movies">\n'
        xml += '<setting id="mfileext" type="labelenum" values="ANY|AVI|MKV|MP4|ISO|DIVX|MPG|FLV|WMV|MOV|ASF|RM" label="File Extension" default="ANY" />\n'
        xml += '<setting id="mminfilesize" type="labelenum" values="ANY|250MB|500MB|750MB|1GB|2GB|3GB|4GB|5GB|8GB|10GB" label="Minimum File Size" default="500MB" />\n'
        xml += '<setting id="mmaxfilesize" type="labelenum" values="ANY|250MB|500MB|750MB|1GB|2GB|3GB|4GB|5GB|8GB|10GB" label="Maximum File Size" default="5GB" />\n'
        xml += '<setting type="sep" />\n'
        xml += '<setting id="mmaxresults" type="number" label="Maximum Results" default="100"/>\n'
        xml += '<setting id="mresolution" type="enum" values="ANY|Up To 720p|720p Exactly|1080p Exactly" label="Resolution" default="0" />\n'
        xml += '</category>\n' 
        xml += '<category label="TV">\n'
        xml += '<setting id="tfileext" type="labelenum" values="ANY|AVI|MKV|MP4|ISO|DIVX|MPG|FLV|WMV|MOV|ASF|RM" label="File Extension" default="ANY" />\n'
        xml += '<setting id="tminfilesize" type="labelenum" values="ANY|250MB|500MB|750MB|1GB|2GB|3GB|4GB|5GB|8GB|10GB" label="Minimum File Size" default="250MB" />\n'
        xml += '<setting id="tmaxfilesize" type="labelenum" values="ANY|250MB|500MB|750MB|1GB|2GB|3GB|4GB|5GB|8GB|10GB" label="Maximum File Size" default="2GB" />\n'
        xml += '<setting type="sep" />\n'
        xml += '<setting id="tmaxresults" type="number" label="Maximum Results" default="100"/>\n'
        xml += '<setting id="tresolution" type="enum" values="ANY|Up To 720p|720p Exactly|1080p Exactly" label="Resolution" default="0" />\n'
        xml += '</category>\n' 
        xml += '</settings>\n'
        
        self.CreateSettings(self.name, self.display_name, xml)
    
    def fileext(self, type):
        return self.Settings().get_setting( type[0:1] + 'fileext')
        
    def minfilesize(self, type):    
        filesz = self.Settings().get_setting( type[0:1] + 'minfilesize')
        
        if filesz == 'ANY':
            return None
        
        import re
        filesznum = float(re.sub("[A-Z]", "", filesz))
        
        if "KB" in filesz:
            filesznum = filesznum * 1024
        elif "MB" in filesz:
            filesznum = filesznum * 1048576
        elif "GB" in filesz:
            filesznum = filesznum * 1073741824
            
        return filesznum
        
    def maxfilesize(self, type):
        filesz = self.Settings().get_setting( type[0:1] + 'maxfilesize')
        
        if filesz == 'ANY':
            return None
        
        import re
        filesznum = float(re.sub("[A-Z]", "", filesz))
        
        if "KB" in filesz:
            filesznum = filesznum * 1024
        elif "MB" in filesz:
            filesznum = filesznum * 1048576
        elif "GB" in filesz:
            filesznum = filesznum * 1073741824
            
        return filesznum
        
    def maxresults(self, type):
        return self.Settings().get_setting( type[0:1] + 'maxresults')
        
    def resolution(self, type):
        return self.Settings().get_setting( type[0:1] + 'resolution')
        
    def get_api_key(self):
        api_key = self.Settings().get_setting('api_key')
        if api_key==None or api_key=='':                                
            furk_user = self.Settings().get_setting('furk_user')
            furk_pwd = self.Settings().get_setting('furk_pwd')
            
            if furk_user != '' and furk_pwd != '':
            
                import json
                from entertainment import requests
            
            
                trans_table = ''.join( [chr(i) for i in range(128)] + [' '] * 128 )
                
                login_command = "/api/login/login"
                login_params = {"login": furk_user, "pwd": furk_pwd}
                login_url = "%s%s" % (self.api_url, login_command)
                #try:login_content = net.http_POST(login_url, login_params).content.translate(trans_table)
                login_content = requests.post(login_url, login_params).content#.translate(trans_table)
                login_data = json.loads(login_content)
                if login_data['status'] == 'ok':
                    api_key = login_data['api_key']
                    self.Settings().set_setting('api_key', api_key)
                
        return api_key
    
    def GetFileHosts(self, url, list, lock, message_queue,bitrate,name): 
        self.AddFileHost(list, bitrate, url, name)
                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):                 
        
        api_key = self.get_api_key()
        if api_key == None or api_key == '':
            return
        
        furk_adult_filter = self.Settings().get_setting('furk_adult_filter')
            
        import json
        from entertainment import requests

                
        name = self.CleanTextForSearch(name) 
        
        match_name = name.lower()
        
        trans_table = ''.join( [chr(i) for i in range(128)] + [' '] * 128 )
        
        search_command = "/api/plugins/metasearch"
        search_query = name
        if 'movie' in type:
            search_query += " " + year
        elif 'tv' in type:
            season_episode = "s%02de%02d" % ( int(season), int(episode) )
            search_query += " " + season_episode
        
        res = self.resolution(type)
        if res == '1':
            search_query += " -1080p"
        elif res == '2':
            search_query += " 720p"
        elif res == '3':
            search_query += " 1080p"
            
        ext = self.fileext(type)
        if ext != "ANY":
            search_query += " " + ext
            
        minsz = self.minfilesize(type)
        maxsz = self.maxfilesize(type)
            
        search_params = {"match" : "extended", "sort" : "relevance", 
            "moderated" : "yes" if furk_adult_filter == "true" else "no", "offset": "0", "filter" : "cached",
            "limit" : self.maxresults(type), "q" : search_query, 'api_key':api_key}
        search_url = "%s%s" % (self.api_url, search_command)

        try:
            search_content = requests.post(search_url, search_params).content.translate(trans_table)
            
        except:
            search_content = requests.post(search_url, search_params).content#.translate(trans_table)

        search_data = json.loads(search_content)
            
        if search_data['status'] != 'ok':
            return
        
        search_stats = search_data['stats']
        total_found = search_stats['total_found']
        if int(total_found) <= 0:
            return
        
        import re
        
        data_files = search_data['files']
    
        
        for data_file in data_files:
        
            file_name = data_file['name']           
            file_name_lower = file_name.lower()
            if self.Match(match_name, file_name_lower) == False:
                continue
            try:
                file_info = data_file['video_info']

                file_id = data_file['id']

                data_file_ready = data_file['is_ready']
                data_file_type  = data_file['type'].lower()

                if data_file_ready == '1' and  data_file_type == 'video':

                    bitrate = re.compile('bitrate: (.+?)\n').findall(file_info)
                    
                    if bitrate:
                        bitrate = bitrate[0]
                        
                        file_size_fmt = '[COLOR orange][FMT: %s, FSZ: %s][/COLOR]'
                        file_size = 'NA'
                        
                        file_size_in_bytes =  data_file['size']
                        if file_size_in_bytes:
                            flt_file_size_in_bytes = float(file_size_in_bytes)

                            
                            if 'tv' in type and 'complete' in file_name_lower:
                                                                        
                                    file_size = "%.2f GB" % (flt_file_size_in_bytes/1073741824)

                                    res = self.ReturnRes(file_name_lower)
                                    
                                    file_name = (file_size_fmt % ('[COLOR red]FULL SET[/COLOR]', file_size)) + " " + file_name

                                    self.GetFileHosts(file_id, list, lock, message_queue, res, file_name)

                            if minsz != None and flt_file_size_in_bytes < minsz:
                                continue
                            if maxsz != None and flt_file_size_in_bytes > maxsz:
                                continue

                            if flt_file_size_in_bytes <= 1048576: 
                                file_size = '.%2f KB' % (flt_file_size_in_bytes/1024)
                            elif flt_file_size_in_bytes <= 1073741824: 
                                file_size = '%.2f MB' % (flt_file_size_in_bytes/1048576)
                            else:
                                file_size = "%.2f GB" % (flt_file_size_in_bytes/1073741824)
                            
                            res = 'NA'
                            for key, value in common.quality_dict.iteritems():
                                if re.search('[^a-zA-Z0-9]' + key + '[^a-zA-Z0-9]', file_name_lower):
                                    res = value
                                    break
                                

                        if 'tv' in type:
                            if '3d' in file_name_lower:
                                res='3D'
                                
                            if res == 'NA':
                                if 'GB' in file_size:
                                    file_sz_flt = float( re.search( '([0-9\.]+)', file_size ).group(1) )
                                    if file_sz_flt >= 2.0:
                                        res = self.ReturnRes(file_name_lower)
                                    else:
                                        res = self.ReturnRes(file_name_lower)
                                else:
                                    res = 'LOW'
                                    
                            file_format = 'NA'
                            for key, value in common.movie_container_dict.iteritems():
                                if re.search('[^a-zA-Z0-9]' + key + '[^a-zA-Z0-9]', file_name_lower) or file_name_lower.endswith(key):
                                    file_format = value
                                    break
                                
                            file_name = (file_size_fmt % (file_format, file_size)) + " " + file_name
                
                            self.GetFileHosts(file_id, list, lock, message_queue, res, file_name)

                                

                        else:
                            if res == 'NA' or 'HD' in res:

                                if 'GB' in file_size:
                                    file_sz_flt = float( re.search( '([0-9\.]+)', file_size ).group(1) )
                                    
                                    if file_sz_flt >= 1.0:
                                        res = self.ReturnRes(file_name_lower)
                                    else:
                                        res = self.ReturnRes(file_name_lower)
                                else:
                                    res = 'LOW'
                                    
                                 
                                file_format = 'NA'
                                for key, value in common.movie_container_dict.iteritems():
                                    if re.search('[^a-zA-Z0-9]' + key + '[^a-zA-Z0-9]', file_name_lower) or file_name_lower.endswith(key):
                                        file_format = value
                                        break
                                    
                                file_name = (file_size_fmt % (file_format, file_size)) + " " + file_name
                    
                                self.GetFileHosts(file_id, list, lock, message_queue, res, file_name)
            except:pass
                                
    def ReturnRes(self, file_name_lower):
        if '2160p' in file_name_lower:
            res ='4K'
        elif '4k' in file_name_lower:
            res ='4K'
        if '3d' in file_name_lower:
            res ='3D'
        elif '1080i' in file_name_lower:
            res ='1080P'
        elif '1080p' in file_name_lower:
            res ='1080P'
        elif '720p' in file_name_lower:
            res ='720P'
        elif 'hd' in file_name_lower:
            res ='HD'
        else:
            res='SD'
        return res    
        
    def Resolve(self, url):
    
        api_key = self.get_api_key()
        if api_key == None or api_key == '':
            return
    
        import json
        from entertainment import requests
        
        
        from entertainment import odict
        resolved_media_urls = odict.odict()
        
        trans_table = ''.join( [chr(i) for i in range(256)] + [' '] * 256 )
    
        file_get_command = "/api/file/get"
        file_get_params = {"id" : url, 't_files':'1', 'api_key':api_key}
        file_get_url = "%s%s" % (self.api_url, file_get_command)

        try:
            file_get_content = requests.post(file_get_url, file_get_params).content.translate(trans_table)
        except:
            file_get_content = requests.post(file_get_url, file_get_params).content#.translate(trans_table)
        file_get_data = json.loads(file_get_content)

        if file_get_data['status'] != 'ok' or file_get_data['found_files'] != '1' :
            return
            
        data_files = file_get_data['files']
        data_files = (data_files[0])['t_files']
        for data_file in data_files:
            data_file_name = data_file['name']
            data_file_format = "[COLOR red][" + (data_file_name[data_file_name.rfind('.')+1:]).upper() + "][/COLOR]"
            if 'video' in data_file['ct'] and 'sample' not in data_file_name.lower():
            
                bitrate = data_file.get('bitrate', None)
                if bitrate:
                    
                    file_url =  data_file.get('url_dl', None)
                    if file_url:
                    
                        file_size_fmt = '[COLOR orange][%s][/COLOR]'
                        file_size = 'NA'
                        
                        file_size_in_bytes =  data_file['size']
                        if file_size_in_bytes:
                            flt_file_size_in_bytes = float(file_size_in_bytes)
                                                    
                            if flt_file_size_in_bytes <= 1024: 
                                file_size = '.%2f KB' % (flt_file_size_in_bytes/1024)
                            elif flt_file_size_in_bytes <= 1048576: 
                                file_size = '%.2f MB' % (flt_file_size_in_bytes/1048576)
                            else:
                                file_size = "%.2f GB" % (flt_file_size_in_bytes/1073741824)
                                
                            file_name = data_file_format + " " + (file_size_fmt % file_size) + " " + data_file_name
                
                            resolved_media_urls[file_name] = file_url

        if len(resolved_media_urls) == 0:
            resolved_media_urls == None
        elif len(resolved_media_urls) == 1:
            resolved_media_urls = ((resolved_media_urls.items())[0])[1]

        return resolved_media_urls
