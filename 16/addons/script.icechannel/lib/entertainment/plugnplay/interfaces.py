"""
    Ice Channel
"""

from entertainment import common
from entertainment.plugnplay import Interface
from entertainment.plugnplay import Plugin
import sys

def _function_id(obj, nFramesUp):
	'''Create a string naming the function n frames up on the stack.'''
	fr = sys._getframe(nFramesUp+1)
	co = fr.f_code
	return "%s.%s" % (obj.__class__, co.co_name)


def not_implemented(obj=None):
	'''Use this instead of ``pass`` for the body of abstract methods.'''
	raise Exception("Unimplemented abstract method: %s" % _function_id(obj, 1))

class ExtensionStoreParent(Plugin, Interface):
    name='override_me'
    display_name='override_me'
    priority = 100
    
    img = ''
    fanart = ''
    
    def LoadiStreamStoreAndExtensions(self, addons_xml_url, addons_xml_md5_url, list, lock, message_queue):
        from entertainment.net import Net
        net = Net()
        
        #self.addon_xml_md5 = net.http_GET( self.addons_xml_md5_url ).content        
        #print self.addon_xml_md5
        
        content = net.http_GET( addons_xml_url ).content
        
        # verify addons.xml md5
        #import hashlib
        #addon_xml_md5 = hashlib.md5(content).hexdigest()
        #print addon_xml_md5
        
        #if addon_xml_md5 != self.addon_xml_md5: 
        #    return False
        
        import elementtree.ElementTree as ET        
        store_root = ET.fromstring(content) 
        store_repo = None
        for extn in store_root.findall(".//addon"):
            for extnpt in extn.findall(".//extension"):
                if extnpt.get('point') == 'xbmc.addon.repository':
                    store_repo = extn
                    break
        if store_repo == None: return False
        
        store_zip_elm=None
        for dataelm in store_repo.findall(".//extension/datadir"):
            if dataelm.get('zip') == 'true':
                store_zip_elm = dataelm
                break
        if store_zip_elm == None: return False
        
        store_zip_dir_url = store_zip_elm.text
        if not store_zip_dir_url.endswith('/'):
            store_zip_dir_url = store_zip_dir_url + '/'
        
        store_repo_id = store_repo.get('id')
        store_repo_version = store_repo.get('version')
        store_repo_zip = '%s%s/%s-%s.zip' % (store_zip_dir_url, store_repo_id, store_repo_id, store_repo_version)
        
        for extn in store_root.findall(".//addon"):
            extn_id = extn.get('id').strip()

            if extn_id.startswith('script.icechannel.') and extn_id not in ['script.icechannel.extn.common', 'script.icechannel.extn.xunity.tv.common']:
                extn_version = extn.get('version').strip()
                extn_name = extn.get('name').strip()
                extn_provider = extn.get('provider-name').strip()
                extn_zip = '%s%s/%s-%s.zip' % (store_zip_dir_url, extn_id, extn_id, extn_version)
                extn_icon = '%s%s/icon.png' % (store_zip_dir_url, extn_id)
                extn_fanart = '%s%s/fanart.jpg' % (store_zip_dir_url, extn_id)
                
                extn_summary = ''                
                for extn_summary_elm in extn.findall('.//summary'):                    
                    extn_summary_lang = extn_summary_elm.get('lang')
                    if extn_summary_lang == None or extn_summary_lang.lower() == "en":
                        extn_summary = extn_summary_elm.text
                        break
                        
                extn_desc = ''
                for extn_desc_elm in extn.findall('.//description'):
                    extn_desc_lang = extn_desc_elm.get('lang')
                    if extn_desc_lang == None or extn_desc_lang.lower() == "en":
                        extn_desc = extn_desc_elm.text
                        break
                    
                
                list.append(  {     'extn_id':extn_id, 
                                    'extn_version':extn_version, 
                                    'extn_name':extn_name, 
                                    'extn_provider':extn_provider, 
                                    'extn_zip':extn_zip, 
                                    'extn_icon':extn_icon, 
                                    'extn_fanart':extn_fanart, 
                                    'extn_summary':extn_summary,
                                    'extn_desc':extn_desc,
                                    'extn_repo_id':store_repo_id, 
                                    'extn_repo_version':store_repo_version, 
                                    'extn_repo_zip':store_repo_zip 
                                } 
                            ) 
    
class ExtensionStoreConcrete(ExtensionStoreParent):
    filecode='_xstrc'    
    
    def get_addons_xml_and_md5_urls(self):
        not_implemented(self)
        
    def LoadStoreAndExtensions(self, list, lock, message_queue):
        addons_xml_url, addons_xml_md5_url = self.get_addons_xml_and_md5_urls()
        self.LoadiStreamStoreAndExtensions(addons_xml_url, addons_xml_md5_url, list, lock, message_queue)
    
class ExtensionStoreSearch(ExtensionStoreParent):
    filecode='_xstrs'        
    
    def AddInfo(self, list, page='', total_pages=''):
        list.append( { 'website':self.name, 'id':self.name+'_info', 'title':self.name+' Info','mode':common.mode_Info, 'page':str(page), 'total_pages':str(total_pages) } )
    
    def AddExtnProject(self, list, url, title):
        list.append( { 'website':self.name, 'url':url, 'title':title } ) 
    
    def AddExtnRepo(self, list, addons_xml, addons_xml_md5, id=''):
        if id == '':
            id = common.CreateIdFromString(addons_xml)
        list.append( { 'website':self.name, 'id':id, 'addons_xml':addons_xml, 'addons_xml_md5':addons_xml_md5 } ) 
    
    def Search(self, list, lock, message_queue, page='', total_pages=''):
        not_implemented(self)
        
    def GetAddonsXMLAndMD5(self, url, list, lock, message_queue):
        not_implemented(self)
    
class Tools(Plugin, Interface):
    filecode='_tls'
    name='override_me'
    display_name='override_me'
    img = ''
    fanart = ''
    notify_msg_header = ''
    notify_msg_success = ''
    notify_msg_failure = ''
    priority = 100
    show_in_context_menu = False
    
    def Execute(self):
        not_implemented(self)
        
class ProxySupport(Plugin, Interface):
    filecode='_prx'
    name='override_me'
    display_name='override_me'
    priority=100
    domains = []
    
class WebProxy(Plugin, Interface):
    filecode='_wpx'
    name='override_me'
    display_name='override_me'
    priority=100
    
    def SetupRequest(self, url):
        not_implemented(self)
        
    def ResponseReceived(self, response):
        not_implemented(self)
    
class HostResolver(Plugin, Interface):
    filecode='_hrv'
    name='override_me'
    priority = 100
    
    match_list = ['override_me_1', 'override_me_2'] # all lowercase    
    
    def CanResolve(self, url):
    
        domain = common.GetDomainFromUrl(url).lower()
        
        if domain in self.match_list:
            return True
            
        return False
    
    def Resolve(self, url):
        not_implemented(self)
        
class PremiumHostResolver(Plugin, Interface):
    filecode='_prv'
    name='override_me'
    priority = 100
    
    def CanResolve(self, url):
        not_implemented(self)    
        
    def Resolve(self, url):
        not_implemented(self)
        
class CaptchaHandler(Plugin, Interface):
    filecode='_chr'
    name='override_me'
    priority = 100
    
    def CanHandle(self, html, url):
        not_implemented(self)    
        
    def Handle(self, html, url):
        not_implemented(self)
        
    def Solve(self, content, content_type='png'):
        
        solution = ''
        
        import os
        captcha = os.path.join( common.captchas_path, "%s.%s.%s" % ( self.name, common.GetEpochStr(), content_type ) )
        open(captcha, 'wb').write(content)
        
        import xbmcgui
        img = xbmcgui.ControlImage(450,15,400,130, captcha)
        wdlg = xbmcgui.WindowDialog()
        wdlg.addControl(img)
        wdlg.show()
        
        import xbmc
        kb = xbmc.Keyboard('', 'Please enter the text in the image', False)
        kb.doModal()
        capcode = kb.getText()
        
        if (kb.isConfirmed()):
            userInput = kb.getText()
            if userInput != '':
                solution = kb.getText()
            elif userInput == '':
                solution = ''
        else:
            solution = ''
               
        wdlg.close()
        
        try: 
            os.remove(captcha)
        except: 
            pass
        
        return solution
    
class LiveResolver(Plugin, Interface):
    filecode='_lrv'
    name='override_me'
    priority = 100
    
    def Resolve(self, content, url):
        not_implemented(self)
       
class Parent(Plugin, Interface):
    name='override_me'
    display_name='override_me'
    priority = 100
    
    img = ''
    fanart = ''
    
    def AddDummy(self, list, title):
        list.append( {'mode':common.mode_Dummy, 'title':title} )
    
    def AddContent(self, list, indexer, mode, title, id, type, url='', name='', year='', season='', episode='', img='', fanart='', genre='', plot='', imdb_id=''):    
        if id == '':
            id = common.CreateIdFromString(title)
        list.append( {'indexer':indexer, 'mode':mode, 'title':title, 'url':url, 'website':self.name, 'name':name,
                      'year':year, 'season':season, 'episode':episode, 'type':type, 'id':id, 'img':img, 'fanart':fanart,
                      'genre':genre, 'plot':plot, 'imdb_id':imdb_id  } ) 
    
    def Search(self, srcr, keywords, type, list, lock, message_queue, page='', total_pages=''): 
        not_implemented(self)
        
    def AccountSettings(self):
        return ''
        
    def CleanTextForSearch(self, text, strip=False, remove_non_ascii=False):
        from entertainment import htmlcleaner
        import urllib,re
        text = htmlcleaner.clean( urllib.unquote_plus(text), strip, remove_non_ascii )
        return re.sub('[^A-Za-z0-9 ]+', '', text)
        
    def Match(self, search_for, search_in, strict=True):
        matches = False
    
        search_for_words = search_for.strip().lower().split(' ')
        search_in_lower = search_in.lower()
        
        match_total = float( len(search_for_words) )
        match_count = 0
        
        import re        
        for search_for_word in search_for_words:            
            if strict == False and search_for_word in search_in_lower:
                match_count = match_count + 1
            elif strict == True and re.search('(?<![0-9a-zA-Z])' + search_for_word + '[^0-9a-zA-Z]', search_in_lower) != None:
                match_count = match_count + 1
        
        match_fraction = ( match_count / match_total )
        if (match_total==2 and match_fraction>=0.5) or ( match_fraction > 0.65 ):
            matches = True
            
        return matches
        
    
    def GoogleSearchByTitleReturnFirstResultOnlyIfValid(self, site_url, title, srch_kywrds = '', item_count=1, title_extrctr='', exact_match=False, use_site_prefix = True, return_dict=False):
        # Checks for the first valid result in the fetched number of items
        # if item starts with search term
        #    and match is more than 65%...valid result
        
        return_url = ''
        
        from entertainment.xgoogle.search import GoogleSearch
        if title_extrctr != '':
            import re
        
        search_url = 'site:' if use_site_prefix == True else ''
        search_url = search_url + site_url + ' '  + title + ' ' + srch_kywrds

        gs = GoogleSearch(search_url)        
        gs.results_per_page = item_count
        
        title_lower = title.lower().strip()
        title_words = title_lower.split(' ')
        
        for result in gs.get_results():         
            result_title = result.title.lower()
            if str(title_extrctr) != '':
                if isinstance(title_extrctr, list):
                    for ttlextrct in title_extrctr:
                        result_title_re = re.search(ttlextrct, result_title)

                        if result_title_re:
                            result_title = result_title_re.group(1)
                            break
                else:    
                    result_title_re = re.search(title_extrctr, result_title)

                    if result_title_re:
                        result_title = result_title_re.group(1)
                    else:
                        continue
                    
            if exact_match == True:
                if result_title == title_lower or result_title.replace("'", "") == title_lower.replace("'", ""):
                    if return_dict:
                        return_url = result
                    else:
                        return_url = result.url
                    break
                else:
                    continue
                    
            if not result_title.startswith(title_lower) and not title_lower.startswith(result_title):
                continue
            
            match_total = float( len(title_words) )
            match_count = 0

            for title_word in title_words:
                if title_word in result_title:
                    match_count = match_count + 1
            
            match_fraction = ( match_count / match_total )
            if (match_total==2 and match_fraction>=0.5) or ( match_fraction > 0.65 ):
                if return_dict:
                    return_url = result
                else:
                    return_url = result.url
                break;
                
        if not return_url and use_site_prefix == True:
            return_url = self.GoogleSearchByTitleReturnFirstResultOnlyIfValid(site_url, title, srch_kywrds, item_count, title_extrctr, exact_match, use_site_prefix = False, return_dict=return_dict)

        return return_url
        
    def GoogleSearch(self, site_url, srch_term, srch_kywrds = '', page=1):
        # Checks only the first search result
        # if match is more than 65%...valid result
        
        valid_results = []
        
        from entertainment.xgoogle.search import GoogleSearch
        
        search_url = 'site:' + site_url + ' '  + srch_term + ' ' + srch_kywrds
        gs = GoogleSearch(search_url)        
        gs.results_per_page = 20
        gs.page = page-1
        
        title_words = (srch_term + ' ' + srch_kywrds).lower().split(' ')
        
        for result in gs.get_results():
            result_title = (result.title + ' ' + result.url).lower()

            match_total = float( len(title_words) )
            match_count = 0
            for title_word in title_words:
                if title_word in result_title:
                    match_count = match_count + 1
            
            if ( match_count / match_total ) > 0.65 :
                valid_results.append( {'title':result.title, 'url':result.url} )

        return valid_results
        
class FileFormat(Plugin, Interface):
    filecode='_ffm'
    priority = 100
    store = ''    
    extensions = '' # override 

    ff_can_parse_yes = 'YES'
    ff_can_parse_no = 'NO'
    ff_can_parse_maybe = 'MAYBE'
    
    from entertainment import odict
    
    def GetStoreItemType(self):
        return 'playlist'
        
    def CanParse(self, raw_data):
        not_implemented(self)
        
    def CanParseRawData(self):
        return True
    
    def ParseHeader(self, data):
        not_implemented(self)
    
    def ParseData(self, data):
        not_implemented(self)
        
    def ReadItem(self, item):
        not_implemented(self)
        
    def IsItemAList(self, item):
        not_implemented(self)
        
    def IsISTREAMImportSupported(self):
        return True
        
    def IsItemPlayable(self, item):
        not_implemented(self)    
        
    def AddItem(self, item, title, name, parents):
        # title: title of the list retrieved from file
        # name: user entered alias for the list in iStream
        not_implemented(self)    
        
    def GetClassNameFromName(self, name):
        name  = name.lower()
        if name[0] in '1234567890':
            name = '_' + name
        import re
        name = re.sub('[^a-z0-9]', '_', name)
        return name
        
    def GetDisplayNameFromName(self, name):
        import re
        name = re.sub('[^a-z0-9A-z ]', '_', name)
        return name
        
    def ReadHttpFile(self, path):
        from entertainment.net import Net
        net = Net( cached = True if common.addon.get_setting('cache_playlists')=='true' else False )
        content = net.http_GET(path).content
        return content
    
    def ReadFtpFile(self, path):
        not_implemented(self)
    
    def ReadLocalFile(self, path):
        f = open(path, 'r')
        data = f.read()
        f.close()
        
        return data
    
    def ReadFile(self, path, parse_only_title=False, send_raw_data=False):
        data = ''
        try:
            if (path[:4] == 'http'):
                data = self.ReadHttpFile(path)
            elif (path[:3] == 'ftp'):
                data = self.ReadFtpFile(path)
            else:
                data = self.ReadLocalFile(path)
        except:
            data = ''
        if send_raw_data:
            if data:
                return data
            else:
                return None
            
        if parse_only_title:
            if data:
                return self.ParseHeader(data)
            else:
                return (None, None, None)
        else:
            if data:
                return self.ParseData(data)
            else:
                return (None, None, None, None)
        
        
    
    def ReadItem(self, item):
        title = item['name']
        img = item.get('img', '')
        fanart = item.get('fanart', '')
        
        new_title = ''
        new_img = ''
        new_fanart = ''
        
        list = []
        
        if self.IsItemAList(item):
            (new_title, new_img, new_fanart, list) = self.ReadFile(item['url'])
            
        return (new_title if new_title else title, new_img if new_img else img, new_fanart if new_fanart else fanart, list)
    
    def ReadFileForSearch(self, path, max_level=2):    
        
        result = []
        
        try:
            import Queue as queue
        except:
            import queue
        processQ = queue.Queue()
        
        processQ.put( { 'level':1, 'path':path})
        
        item = processQ.get()
        while (item):            
            current_level = item['level']
            current_path = item['path']
        
            (title, img, fanart, list) = self.ReadFile(current_path)
            if not list: 
                try:
                    item = processQ.get_nowait()
                except:
                    item = None
                continue
            for item in list:
                if self.IsItemAList(item) and current_level+1 <= max_level:
                    processQ.put( { 'level':current_level+1, 'path':item['url']})
                elif self.IsItemPlayable(item):
                    result.append(item)
            try:
                item = processQ.get_nowait()
            except:
                item = None

        return ('title', result)
            
                
        

    def Get(self):
        if self.store == '':
        
            from entertainment.addon import Addon
            
            self.store = Addon(self.store_id)
            
        return self.store
        
    def Store(self):
        if self.store == '':
        
            from entertainment.addon import Addon
            
            success = False
            
            import time
            
            while not success:
                try:
                    self.store = Addon(self.store_id)
                    success = True
                except:
                    time.sleep(0.25)
               
            
        return self.store
        
    def Create(self, version = '0.0.1'):

        self.store_id = 'script.icechannel.extn.store.' + self.name.replace(' ', '')
        temp_addon_path = common.addon_path.replace(common.addon_id,self.store_id)
        
        try:
            import os
            
            error = False
            
            if not os.path.exists(temp_addon_path):
                error = True
                try:
                    os.makedirs(temp_addon_path)
                    os.makedirs( os.path.join(temp_addon_path, 'plugins') )
                    os.makedirs( os.path.join(temp_addon_path, 'plugins', 'files') )
                except OSError:
                    pass
            
            if not error:
                try:
                    if self.Get().get_version() != version:
                        error = True
                except:
                    error = True
            
            if error:
                # create addon.xml
                temp_addon_xml_path = os.path.join(temp_addon_path, 'addon.xml')
                
                f = open(temp_addon_xml_path, 'w')                
                try:
                    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
                    f.write('<addon id="%s" version="%s" name="iStream - %s" provider-name="iStream">\n' % (self.store_id, version, self.display_name) )
                    f.write('<extension point="xbmc.python.pluginsource" library="default.py" />\n')
                    f.write('<extension point="xbmc.addon.metadata">\n')
                    f.write('<summary lang="en">%s</summary>\n' % ('iStream - ' + self.display_name ) )
                    f.write('<description lang="en">%s</description>\n' % ('iStream - ' + self.display_name ) )
                    f.write('<platform></platform>\n')
                    f.write('<language></language>\n')
                    f.write('<license></license>\n')
                    f.write('<forum></forum>\n')
                    f.write('<website></website>\n')
                    f.write('<source></source>\n')
                    f.write('<email></email>\n')
                    f.write('</extension>\n')
                    f.write('</addon>\n')
                finally:
                    f.close
                    
                # create default.py
                temp_default_py_path = os.path.join(temp_addon_path, 'default.py')
                f = open(temp_default_py_path, 'w')
                try:
                    f.write('addon_id="%s"\n' % self.store_id)
                    f.write('addon_name="%s"\n' % ('iStream - ' + self.display_name ) )
                    f.write('import xbmcaddon\n')
                    f.write('addon = xbmcaddon.Addon(id=addon_id)\n')
                    f.write('addon.openSettings()\n')
                finally:
                    f.close
                    
                # create resources folder
                temp_resource_folder = os.path.join(temp_addon_path, 'resources')
                try:
                    os.makedirs(temp_resource_folder)
                except OSError:
                    pass
                    
                import xbmc
                xbmc.executebuiltin('UpdateLocalAddons ')
                    
        except IOError:
            common.addon.log_error('error writing store for: ' + self.store_id)  
    
    def Add(self, title, description, url, code, parents, type='playlist', img='', fanart='', version='0.0.1' ):
    
        self.Create(version=version)
        
        name = self.GetClassNameFromName(title)
        
        import os                
        old_py_path = os.path.join(self.Store().get_path(), 'plugins', 'files', name + '.py')
        old_path_exists = os.path.exists(old_py_path)
        
        py_path = os.path.join(self.Store().get_path(), 'plugins', 'files', name + common.playlist_content_map[parents] + '.py')
        path_exists = os.path.exists(py_path)
        
        file_version = ''
        if not path_exists and old_path_exists:
            f = open(old_py_path, 'r')
            data = f.read()
            f.close()
        elif path_exists:
            f = open(py_path, 'r')
            data = f.read()
            f.close()
        
        if path_exists or old_path_exists:
            import re
            file_version = re.search('\#\#--version=(.*)', data)
            if file_version:
                file_version = file_version.group(1)
            else:
                file_version = ''
        
        if (file_version != version and (path_exists or old_path_exists) ) or not path_exists : 
            
            import hashlib
            path = url
            url = hashlib.md5(url.lower()).hexdigest()
                        
            description = description.replace('"', "'")
            
            temp_code = code
            temp_code = temp_code.replace('<classname>', name)
            temp_code = temp_code.replace('<parents>', parents)
            temp_code = temp_code.replace('<url>', path)
            temp_code = temp_code.replace('<name>', title)
            temp_code = temp_code.replace('<display_name>', title)
            temp_code = temp_code.replace('<file_format_name>', self.name)
            temp_code = temp_code.replace('<description>', description)
            
            add_code = '##--version=%s\n' % version
            add_code += '##--id=%s\n' % url
            add_code += '##--title=%s\n' % title
            add_code += '##--format=%s\n' % self.name
            add_code += '##--type=%s\n' % type
            add_code += '##--url=%s\n' % path
            add_code += '##--parents=%s\n' % parents
            add_code += '##--description=%s\n' % description
            add_code += '##--img=%s\n' % img
            add_code += '##--fanart=%s\n' % fanart
            code = add_code + temp_code            
            
            f = open(py_path, 'w')
            try:
                f.write(code)
            finally:
                f.close
                
        if old_path_exists:
            os.remove(old_py_path)
            
    def Remove(self, url):
    
        import hashlib
        id = hashlib.md5(url.lower()).hexdigest()
        
        import os
        from glob import glob
        files = glob( os.path.join( os.path.dirname(common.addon_path), common.addon_id + '.extn.store.' + self.name, 'plugins', 'files', '*.py' ) )
        
        import re
        
        error = False
        
        for file in files:
            f = open(file, 'r')
            data = f.read()
            f.close()
            
            file_id = re.search('\#\#--id=(.*)', data)
            if file_id:
                file_id = file_id.group(1)
                if file_id == id:
                    try:
                        os.remove(file)
                        files_found = glob( file + '*' ) 
                        for file_found in files_found:
                            os.remove(file_found)
                    except:
                        error = True
                        pass
                    break;
                    
        return error

class CustomSettings(Plugin, Interface):
    filecode='_cst'
    settings_id = ''
    settings = ''
    settings_name = ''
    
    settings_img=''
    settings_fanart=''

    def SettingsLauncher(self):
        return '<setting id="%s" type="action" label="%s Settings" action="RunPlugin(plugin://%s/default.py)" />\n' % ( self.settings_id, self.settings_name, self.settings_id )
            
    def Settings(self):
        if self.settings == '':
        
            from entertainment.addon import Addon
            
            success = False
            
            import time
            
            while not success:
                try:
                    self.settings = Addon(self.settings_id)
                    success = True
                except:
                    time.sleep(0.25)
               
            
        return self.settings
        
    def Get(self):
        if self.settings == '':
        
            from entertainment.addon import Addon
            
            self.settings = Addon(self.settings_id)
            
        return self.settings

    def CreateSettings(self, name, display_name, settings_xml, version='0.0.2'):
        self.settings_name = display_name
        self.settings_id = 'script.icechannel.' + name.replace(' ', '') + '.settings'
        temp_addon_path = common.addon_path.replace(common.addon_id,self.settings_id)
        
        try:
            import os
            
            error = False
            
            if not os.path.exists(temp_addon_path):
                error = True
                try:
                    os.makedirs(temp_addon_path)
                except OSError:
                    pass
            
            if not error:
                try:
                    if self.Get().get_version() != version:
                        error = True
                except:
                    error = True
            
            if error:
                # create addon.xml
                temp_addon_xml_path = os.path.join(temp_addon_path, 'addon.xml')
                
                f = open(temp_addon_xml_path, 'w')                
                try:
                    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
                    f.write('<addon id="%s" version="%s" name="iStream - %s" provider-name="iStream">\n' % (self.settings_id, version, name) )
                    f.write('<extension point="xbmc.python.pluginsource" library="default.py" />\n')
                    f.write('<extension point="xbmc.addon.metadata">\n')
                    f.write('<summary lang="en">%s</summary>\n' % ('iStream - ' + name + ' - Settings ') )
                    f.write('<description lang="en">%s</description>\n' % ('iStream - ' + name + ' - Settings ') )
                    f.write('<platform></platform>\n')
                    f.write('<language></language>\n')
                    f.write('<license></license>\n')
                    f.write('<forum></forum>\n')
                    f.write('<website></website>\n')
                    f.write('<source></source>\n')
                    f.write('<email></email>\n')
                    f.write('</extension>\n')
                    f.write('</addon>\n')
                finally:
                    f.close
                    
                # create default.py
                temp_default_py_path = os.path.join(temp_addon_path, 'default.py')
                f = open(temp_default_py_path, 'w')
                try:
                    f.write('addon_id="%s"\n' % self.settings_id)
                    f.write('addon_name="%s"\n' % ('iStream - ' + name + ' - Settings') )
                    f.write('import xbmcaddon\n')
                    f.write('addon = xbmcaddon.Addon(id=addon_id)\n')
                    f.write('addon.openSettings()\n')
                finally:
                    f.close
                    
            # create resources folder
            temp_resource_folder = os.path.join(temp_addon_path, 'resources')
            try:
                os.makedirs(temp_resource_folder)
            except OSError:
                pass
                    
            # settings file
            temp_settings_xml_path = os.path.join(temp_resource_folder, 'settings.xml')
            f = open(temp_settings_xml_path, 'w')
            try:
                f.write(settings_xml)
            finally:
                f.close
             
        except IOError:
            common.addon.log_error('error writing settings for: ' + self.settings_id)  
            
class iStreamSettings(Plugin, Interface):
    filecode='_ist'
    settings_id = ''
    settings = ''
    name = ''
    type = ''
    priority = 100
    
    def Initialize(self): 
        not_implemented(self)

    def SettingsLauncher(self):
        return '<setting id="%s" type="action" label="%s Settings" action="RunPlugin(plugin://%s/default.py)" />\n' % ( self.settings_id, self.name, self.settings_id )
            
    def Settings(self):
        if self.settings == '':
            from entertainment.addon import Addon
            
            success = False
            
            import time
            
            while not success:
                try:
                    self.settings = Addon(self.settings_id)
                    success = True
                except:
                    time.sleep(0.25)
            
        return self.settings
        
    def Get(self):
        if self.settings == '':
        
            from entertainment.addon import Addon
            
            self.settings = Addon(self.settings_id)
            
        return self.settings

    def CreateSettings(self, settings_name, settings_type, settings_xml, version='0.0.2'):
        self.name = settings_name
        self.type = settings_type
        self.settings_id = 'script.icechannel.iStream.' + settings_type + '.settings'
        temp_addon_path = common.addon_path.replace(common.addon_id,self.settings_id)

        try:
            import os
            
            error = False
            
            if not os.path.exists(temp_addon_path):
                error = True
                try:
                    os.makedirs(temp_addon_path)
                except OSError:
                    pass
            
            if not error:
                try:
                    if self.Get().get_version() != version:
                        error = True
                except:
                    error = True
            
            if error:
                # create addon.xml
                temp_addon_xml_path = os.path.join(temp_addon_path, 'addon.xml')
                
                f = open(temp_addon_xml_path, 'w')                
                try:
                    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
                    f.write('<addon id="%s" version="%s" name="iStream - %s" provider-name="iStream">\n' % (self.settings_id, version, settings_name) )
                    f.write('<extension point="xbmc.python.pluginsource" library="default.py" />\n')
                    f.write('<extension point="xbmc.addon.metadata">\n')
                    f.write('<summary lang="en">%s</summary>\n' % ('iStream - ' + settings_name + ' - Settings ') )
                    f.write('<description lang="en">%s</description>\n' % ('iStream - ' + settings_name + ' - Settings ') )
                    f.write('<platform></platform>\n')
                    f.write('<language></language>\n')
                    f.write('<license></license>\n')
                    f.write('<forum></forum>\n')
                    f.write('<website></website>\n')
                    f.write('<source></source>\n')
                    f.write('<email></email>\n')
                    f.write('</extension>\n')
                    f.write('</addon>\n')
                finally:
                    f.close
                    
                # create default.py
                temp_default_py_path = os.path.join(temp_addon_path, 'default.py')
                f = open(temp_default_py_path, 'w')
                try:
                    f.write('addon_id="%s"\n' % self.settings_id)
                    f.write('addon_name="%s"\n' % ('iStream - ' + settings_name + ' - Settings') )
                    f.write('import xbmcaddon\n')
                    f.write('addon = xbmcaddon.Addon(id=addon_id)\n')
                    f.write('addon.openSettings()\n')
                finally:
                    f.close
                    
            # create resources folder
            temp_resource_folder = os.path.join(temp_addon_path, 'resources')
            try:
                os.makedirs(temp_resource_folder)
            except OSError:
                pass
                    
            # settings file
            temp_settings_xml_path = os.path.join(temp_resource_folder, 'settings.xml')
            f = open(temp_settings_xml_path, 'w')
            try:
                f.write(settings_xml)
            finally:
                f.close
             
        except IOError:
            common.addon.log_error('error writing settings for: ' + self.settings_id)              


class Indexer(Parent):
    
    indexer_section_name = 'override_me'    
    indexer_type = 'override_me'
    search_supported = True    
    
    default_indexer_enabled = 'false' # can be overwritten
    
    def __init__(self):
        import os
        if not self.img:
            self.img = common.get_themed_icon(self.name + '.png')
        if not self.fanart:
            self.fanart = common.get_themed_icon(self.name + '_art.png')
    
    def AddInfo(self, list, indexer, section, url, type, page='', total_pages='', sort_by='', sort_order=''):
        list.append( {'indexer':indexer, 'section':section, 'website':self.name, 'id':self.name+'_info',
                      'title':self.name+' Info','mode':common.mode_Info, 'url':url, 'type':type, 'page':page,
                      'total_pages':total_pages, 'sort_by':sort_by, 'sort_order':sort_order } )
    
    def AddSection(self, list, indexer, section, title, url='', type='', hlevel=0, img='', fanart='', plot=''):
        list.append( {'indexer':indexer, 'section':section, 'website':self.name, 'mode':common.mode_Section,
                      'title':title, 'url':url, 'type':type, 'hlevel':str(hlevel), 'img':img, 'fanart':fanart, 'plot':plot} )
        
    def GetSection(self, indexer, section, url, type, list, page='', total_pages='', sort_by='', sort_order=''): 
        '''Use lock for operations other than append on the list'''
        not_implemented(self)
    
    def GetContent(self, indexer, url, title, name, year, season, episode, type, list):
        not_implemented(self)
        
    def GetContent(self, indexer, url, title, name, year, season, episode, type, list):
        not_implemented(self)
        
    def GetSortByOptions(self): 
        not_implemented(self)
    
    def GetSortOrderOptions(self): 
        not_implemented(self)

class ListIndexer(Indexer):
    implements = [Indexer]
    filecode='_lsi'
    priority = 140
    
    indexer_section_name = 'iWatch'
    indexer_type = common.indxr_Lists
    search_supported = False

        
class MovieIndexer(Indexer):
    implements = [Indexer]
    
    filecode='_mvi'
    
    priority = 100
    
    indexer_section_name = 'Movies'
    indexer_type = common.indxr_Movies
        
class TVShowIndexer(Indexer):
    implements = [Indexer]
    filecode='_tvi'
    priority = 110
    
    indexer_section_name = 'TV Shows'
    indexer_type = common.indxr_TV_Shows

'''class LiveTVIndexer(Indexer):
    implements = [Indexer]
    filecode='_ltvi'
    priority = 120
    
    indexer_section_name = 'Live TV'
    indexer_type = common.indxr_Live_TV
    
    default_indexer_enabled = 'true' # can be overwritten
    
    other_names = '' # override, comma separated other names for the channel
    
    regions = [ {'name':'Other', 'img':'', 'fanart':''} ] # override with appropriate regions
    languages = [ {'name':'Other', 'img':'', 'fanart':''} ] # override with appropriate languages   
    genres = [ {'name':'Other', 'img':'', 'fanart':''} ] # override with appropriate genres   

    #search_supported = False
        
    def get_regions_csv(self):
        regions_csv = ''
        for region in self.regions:
            regions_csv += '%s,' % common.CreateIdFromString(region['name'])
        return regions_csv
            
    def get_languages_csv(self):
        languages_csv = ''
        for language in self.languages:
            languages_csv += '%s,' % common.CreateIdFromString(language['name'])
        return languages_csv
            
    def get_genres_csv(self):
        genres_csv = ''
        for genre in self.genres:
            genres_csv += '%s,' % common.CreateIdFromString(genre['name'])
        return genres_csv
        
    def Search(self, srcr, keywords, type, list, lock, message_queue, page='', total_pages=''): 
        from entertainment import istream as entertainment
        stg = entertainment.iStream_settings.get(srcr, None)
        if not stg: return
        for livetvindxr in LiveTVIndexer.implementors():
            if keywords not in livetvindxr.name.replace('_', ' '): continue
            enabled = True if stg.Settings().get_setting( 'live_tv_' + livetvindxr.name + '_indexer_enabled') == 'true' else False
            if not enabled: continue
            list.append( 
                {
                    'id':livetvindxr.name,
                    'indexer':common.indxr_Live_TV, 
                    'indexer_id':livetvindxr.name, 
                    'section':'main', 
                    'title':livetvindxr.display_name, 
                    'mode':common.mode_Live_TV,
                    'img':livetvindxr.img,
                    'fanart':livetvindxr.fanart,
                    'other_names':livetvindxr.other_names,
                    'url':'',
                    'website':livetvindxr.name,
                    'region':livetvindxr.get_regions_csv(),
                    'language':livetvindxr.get_languages_csv(),
                    'genre':livetvindxr.get_genres_csv(),                    
                } )'''
        
    
class SportsIndexer(Indexer):
    implements = []
    filecode='_lspi'
    priority = 130
    
    indexer_section_name = 'Sports (Live)'
    indexer_type = common.indxr_Sports
    search_supported = False
    
        
class Source(Parent):

    source_type = 'override_me'
    source_name = 'override_me'
    source_enabled_by_default = "false" # can be overwritten
    auto_play_supported = True #can be overwritten

    def GetFileHosts(self, url, list, lock, message_queue): 
        '''Use lock for operations other than append on the list'''
        not_implemented(self)
        
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue): 
        '''Use lock for operations other than append on the list'''
        not_implemented(self)
        
    def AddFileHost(self, list, quality, url, host='', views='', votes='', ratings=''):
        if host == '':
            host = common.GetDomainFromUrl(url)
            
        if quality == '':
            quality = 'NA'
        
        list.append( {'id':common.CreateIdFromString(url) + '_', 'website':self.name, 'mode':common.mode_Play, 'host':host, 
            'title':host, 'hosturl':url, 'quality':quality, 'views':views, 'votes':votes, 'ratings':ratings } )
            
    def AddLiveLink(self, list, title, url, host='', img='', fanart='', language='All', region='All', quality='NA'):
        if host == '': host = common.GetDomainFromUrl(url)
        if not language: language = 'All'
        if not region: region = 'Worldwide'
        list.append( {'id':common.CreateIdFromString(url) + '_', 'website':self.name, 'mode':common.mode_Play, 'host':host, 'title':title, 'url':url, 
            'language':language, 'region':region, 'img':img, 'fanart':fanart, 'quality':quality, 'play':'true' } )
            
    def Resolve(self, url):
        
        resolved_media_url = ''
        
        resolved = False
        
        for hr in PremiumHostResolver.implementors():            
            resolved = hr.CanResolve(url)
            if resolved == True:                
                resolved_media_url = hr.Resolve(url)
                if resolved_media_url:
                    break
                else:
                    resolved = False
        
        if resolved == False:
            for hr in HostResolver.implementors():            
                resolved = hr.CanResolve(url)
                if resolved == True:                
                    resolved_media_url = hr.Resolve(url)
                    if resolved_media_url:
                        break
                    else:
                        resolved = False
            
            if resolved == False:
                try:
                    import urlresolver        
                    hosted_media = urlresolver.HostedMediaFile(url=url)        
                    if hosted_media:
                        resolved_url = urlresolver.resolve(url)
                        if resolved_url:
                            resolved_media_url = resolved_url
                except Exception, e:
                    common.addon.log( 'ISTREAM - URL RESOLVER - Exception occured: %s' % e)
                    resolved_media_url = ''
                
        return resolved_media_url
    
        
class MovieSource(Source):
    implements = [Source]
    filecode='_mvs'
    source_type = common.src_Movies
    source_name = 'Movies'
    
class TVShowSource(Source):
    implements = [Source]
    filecode='_tvs'
    source_type = common.src_TV_Shows
    source_name = 'TV Shows'
    
class LiveTVSource(Source):
    implements = [Source]
    filecode='_ltvs'
    source_type = common.src_Live_TV
    source_name = 'Live TV'    
    
    istream_tv_source_id = None
    istream_tv_source_language = None
    istream_tv_source_region = None
    
    def GetFileHosts(self, id, other_names, region, language, list, lock, message_queue):
        # override
        if self.istream_tv_source_id:
            
            url = 'http://xunityrepo.me/xunity/livetv/%s.csv' % self.istream_tv_source_id
            
            from entertainment.net import Net
            net = Net(cached=False)
            content = net.http_GET(url).content
            
            lines = content.split('\n')
            for line in lines:
            
                items = line.split('","')
                
                item_name = items[0]
                item_name = item_name[1:]
                
                item_id = common.CreateIdFromString(item_name)
                
                item_quality = items[1].upper()
                
                item_url = items[2]
                item_url = item_url[:-1]
                
                if id == item_id or item_id in other_names:
                    self.AddLiveLink(list, item_name, item_url, language=self.istream_tv_source_language, region=self.istream_tv_source_region, host='iSTREAM', quality=item_quality)
        
    def Resolve(self, url):
    
        if self.istream_tv_source_id:
            return url

        resolved_media_url = ''
        
        is_resolved = False
        is_content_changed = False
        
        try:
            from entertainment.net import Net
            net = Net()
            content = net.http_GET(url).content
            
            # remove html comments
            import re
            content = re.sub('(?s)<!--.+?-->', '', content)
            
            # urllib unquote html
            import urllib
            content = urllib.unquote(content)
            
        except:
            return ''
        
        while True:
            
            is_resolved = False
            is_content_changed = False
            
            for lr in LiveResolver.implementors():
            
                (is_resolved, is_content_changed, content, url) = lr.ResolveLive(content, url)
                
                if is_resolved == True:
                   resolved_media_url = content 
                   break
                
                if is_content_changed == True:
                    break
                   
            if is_resolved == True or is_content_changed == False:
                break
                   
        return resolved_media_url
    
class SportsSource(Source):
    implements = []
    filecode='_lsps'
    source_type = common.src_Sports
    source_name = 'Sports'
    
    source_sports_list = [] # override
    
    source_time_zone = 0 # 0 = GMT - override accordingly
    
    def GetSportsContent(self, indexer, type, list, lock, message_queue): 
        not_implemented(self)
        
    def AddSportsContent(self, list, indexer, type, mode, title, id='', start_time=None, end_time=None, time_format='%Y %m %d %H:%M', url='', img=''):    
        if id == '':
            teams = title.lower().split(' vs ')
            teams.sort()
            id = common.CreateIdFromString(str(teams))
        
        import datetime        
        import time
        
        if start_time:
            try:
                start_time = (datetime.datetime.strptime(start_time, time_format) + datetime.timedelta(hours=(self.source_time_zone*-1))).strftime('%Y %m %d %H:%M')
            except TypeError:
                start_time = (datetime.datetime.fromtimestamp(time.mktime(time.strptime(start_time, time_format))) + datetime.timedelta(hours=(self.source_time_zone*-1))).strftime('%Y %m %d %H:%M')
                
        if end_time:
            try:
                end_time = (datetime.datetime.strptime(end_time, time_format) + datetime.timedelta(hours=(self.source_time_zone*-1))).strftime('%Y %m %d %H:%M')
            except TypeError:
                end_time = (datetime.datetime.fromtimestamp(time.mktime(time.strptime(end_time, time_format))) + datetime.timedelta(hours=(self.source_time_zone*-1))).strftime('%Y %m %d %H:%M')
        
        list.append( {'indexer':indexer, 'type':type, 'mode':mode, 'title':title, 'url':url, 'website':self.name, 
                'time':start_time, 'start_time':start_time, 'end_time':end_time, 'id':id, 'img':img} ) 
            
    def Resolve(self, url):
        
        resolved_media_url = ''
        
        is_resolved = False
        is_content_changed = False
        
        from entertainment.net import Net
        net = Net()
        content = net.http_GET(url).content
        
        while True:
            
            is_resolved = False
            is_content_changed = False
            
            for lr in LiveResolver.implementors():
            
                (is_resolved, is_content_changed, content, url) = lr.ResolveLive(content, url)
                
                if is_resolved == True:
                   resolved_media_url = content 
                   break
                
                if is_content_changed == True:
                    break
                   
            if is_resolved == True or is_content_changed == False:
                break
                   
        return resolved_media_url
