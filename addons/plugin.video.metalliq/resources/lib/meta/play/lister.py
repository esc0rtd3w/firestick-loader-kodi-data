import re
import copy
from threading import Event, Thread, RLock, Lock, current_thread
from xbmcswift2 import xbmc, xbmcgui

from meta import plugin
from meta.gui import dialogs
from meta.utils.text import urlencode_path, to_utf8, to_unicode, apply_parameters
from meta.utils.rpc import RPC

# These are replace with whitespace in labels and parameters
IGNORE_CHARS = ('.', '%20')#('+', '-', '%20', '.', ' ')

from settings import *

                
class KeyboardMonitor(Thread):
    def __init__(self):
        Thread.__init__(self)
        
        self.active = True
        self.search_term = None
        self.owner_thread = None
        self.lock = Lock()
        self.access_lock = RLock()

        self.hide_keyboard = plugin.get_setting(SETTING_AUTO_HIDE_DIALOGS, bool) and plugin.get_setting(SETTING_AUTO_HIDE_DIALOGS_KEYBOARD, bool)
        
    def stop(self):
        self.active = False
                
    def set_term(self, search_term):
        self.lock.acquire()
        self.owner_thread = current_thread()
        self.search_term = search_term
        
    def release(self):
        with self.access_lock:
            if self.owner_thread is not None:
                self.search_term = None
                self.owner_thread = None
                self.lock.release()
                
    def release_if_owner(self):
        with self.access_lock:
            if self.owner_thread is current_thread():
                self.release()
                    
    def prep_search_str(self, text):
        t_text = to_unicode(text)
        for chr in t_text:
            if ord(chr) >= 1488 and ord(chr) <= 1514:
                return to_utf8(text[::-1])
        return to_utf8(text)

    def run(self):
        while self.active and not xbmc.abortRequested:
            if dialogs.wait_for_dialog("virtualkeyboard", timeout=5,interval=100):
                if self.search_term is not None:
                    if self.hide_keyboard:
                        xbmc.executebuiltin('Dialog.Close(virtualkeyboard, true)')
                        
                    # Send search term
                    text = self.prep_search_str(self.search_term)
                    RPC.Input.SendText(text=text, done=True)
                    # TODO: needed?
                    #while xbmc.getCondVisibility("Window.IsActive(virtualkeyboard)"):
                    #    xbmc.sleep(100)
                    self.release()

def regex_escape(string):
    for c in "\\.$^{[(|)*+?":
        string = string.replace(c, "\\"+c)
    return string
    
@plugin.cached(TTL=5, cache="browser")
def cached_list_dir(path, keyboard_hint=None):
    return list_dir(path)
    
def list_dir(path):
    path = urlencode_path(path)

    try:
        response = RPC.files.get_directory(media="files", directory=path, properties=["season","episode"])
    except:
        plugin.log.error(path)
        raise
    dirs = []
    files = []
    
    for item in response.get('files', []):
        if item.has_key('file') and item.has_key('filetype') and item.has_key('label'):
            if item['filetype'] == 'directory':
                # ignore .xsp and .xml directories
                for ext in (".xsp", ".xml"):
                    if item['file'].endswith(ext) or item['file'].endswith(ext+"/"):
                        continue
                dirs.append({'path':item['file'], 'label':item['label'], 'season': item.get('season')})
            else:
                files.append({'path':item['file'], 'label':item['label'], 'season': item.get('season'), 'episode': item.get('episode')})
                
    return [path,dirs,files]
    
class Lister:
    def __init__(self, preserve_viewid=None, stop_flag=None):
        if stop_flag is None:
            stop_flag = Event()
        self.stop_flag = stop_flag
        
        if preserve_viewid is None:
            window = xbmcgui.Window(xbmcgui.getCurrentWindowId())
            preserve_viewid = window.getFocusId()
        self.preserve_viewid = preserve_viewid
        
        self.keyboardMonitor = KeyboardMonitor()
        self.keyboardMonitor.start()
        
    def get(self, path, guidance, parameters):            
        # Escape parameters
        unescaped_parameters = parameters
        parameters = copy.deepcopy(parameters)
        for key, value in parameters.items():
            if isinstance(value, basestring):
                for c in IGNORE_CHARS:
                    value = value.replace(c, ' ')
                #parameters[key] = re.escape(value)
                parameters[key] = regex_escape(value)
        
        try:
            return self._browse_external(path, guidance, parameters, unescaped_parameters)
        finally:
            self._restore_viewid()

    def is_active(self):
        return not self.stop_flag.is_set()
        
    def stop(self):
        if not self.stop_flag.is_set():
            self.stop_flag.set()
        self.keyboardMonitor.stop()
            
#    @staticmethod
#    def _replace_special_chars(text):
#        for c in ('\+', '\-', '\%20', '\.', '\ '):
#            text = text.replace(c, ' ')
#        return text
        
    @staticmethod
    def _has_match(item, pattern, parameters):
        # Match by season info label
        season_infolabel_match = False
        if item.get('season'):
            item_season = str(item.get('season'))
            param_season = str(parameters.get('season', ''))
            if item_season == param_season:
                season_infolabel_match = True
        if pattern == "{season}" and season_infolabel_match:
            return True
        
        # Match by episode info label
        episode_infolabel_match = False
        if item.get('episode'):
            item_episode = str(item.get('episode'))
            param_episode = str(parameters.get('episode', ''))
            if item_episode == param_episode:
                episode_infolabel_match = True
        if pattern == "{episode}" and episode_infolabel_match:
            return True
        
        # Match by season and episode info labels
        if pattern == "{season}x{episode}" and \
         season_infolabel_match and episode_infolabel_match:
            return True
                
        # Match by label
        label = item['label']
        pattern = to_unicode(pattern)
        # Custom $$ shortcut for unicode word boundary
        pattern = pattern.replace("$$", r"($|^|\s|\]|\[)")
                
        # Detect season number if searching for season 1
        #   to later allow first season to have no number
        first_season = False
        if '{season}' in pattern and '1' == str(parameters.get('season')):
            pattern = pattern.replace('{season}', '(?P<season>\d*)')
            first_season = True
            
        # Apply parameters to pattern
        pattern = apply_parameters(pattern, parameters)    
        
        # Remove special chars
        for c in IGNORE_CHARS:
            #pattern = pattern.replace("\\"+c, ' ')
            label = label.replace(c, ' ')

        # Make sure both label and pattern are unicode
        pattern = to_unicode(to_utf8(pattern))
        label = to_unicode(to_utf8(label))
        #pattern = re.sub(r'\[[^)].*?\]', '', pattern)
        if pattern.startswith("><"):
            label = re.sub(r'\[[^)].*?\]', '', label)
            pattern = pattern.strip('><')
        plugin.log.debug("matching pattern {0} to label {1}".format(to_utf8(pattern), to_utf8(label)))
         
        # Test for a match
        r = re.compile(pattern, re.I|re.UNICODE)
        match = r.match(label)
        if ", The" in label and match is None:
            label = u"The " + label.replace(", The", "")
            match = r.match(label)
        
        # If full match
        if match is not None and match.end() == len(label):
            # Special handling of first season
            if first_season and not match.group('season') in ('1', '', '01', None):
                return False
            
            # Matched!
            plugin.log.debug("match: " + to_utf8(label))
            return True
            
        return False

    def _restore_viewid(self):
        xbmc.executebuiltin("Container.SetViewMode(%d)" % self.preserve_viewid)
    
    def _browse_external(self, path, guidance, parameters, unescaped_parameters, depth=0):
        result_dirs = []
        result_files = []
        
        keyboard_hint = None
        
        for i, hint in enumerate(guidance):
            # Stop early if requested
            if self.stop_flag.isSet() or xbmc.abortRequested:
                return [],[]
            
            # Path not found?
            if not path:
                break

            # Send keyboard data iff not last guidance
            # TODO backward compatibility
            if hint.startswith("keyboard:"):
                hint = u"@" + hint
                
            if hint.startswith("@keyboard:") and i != len(guidance) - 1:
                term = hint[len("@keyboard:"):].lstrip()
                term = term.format(**unescaped_parameters)
                self.keyboardMonitor.set_term(term)
                keyboard_hint = term
                continue
                
            # List path directory
            try:
                _, dirs, files = cached_list_dir(path, keyboard_hint)
            except:
                break
            finally:
                #if xbmc.getCondVisibility("Window.IsActive(infodialog)"):
                #    xbmc.executebuiltin('Dialog.Close(infodialog, true)')
                
                if keyboard_hint is not None:
                    self.keyboardMonitor.release_if_owner()
                    keyboard_hint = None
                self._restore_viewid()
                
            path = None
            
            if hint.startswith("><"):
                hint = hint.strip("><")
            if hint == "@any":
                for dir in dirs:
                    rec_files, rec_dirs = self._browse_external(dir['path'], guidance[i+1:], parameters, unescaped_parameters, depth)
                    result_files += rec_files
                    result_dirs += rec_dirs
                    if result_files:
                        break
            elif hint.startswith("@anyexcept:") and len(hint) >= 14:
                exceptions = []
                exclusion = hint[len("@anyexcept:"):].lstrip()
                if "|" in exclusion: exceptions = exclusion.split("|", )
                else: exceptions.append(exclusion)
                for dir in dirs:
                    if dir['label'] not in exceptions:
                        rec_files, rec_dirs = self._browse_external(dir['path'], guidance[i+1:], parameters, unescaped_parameters, depth)
                        result_files += rec_files
                        result_dirs += rec_dirs
                        if result_files:
                            break
            elif hint.startswith("@anynotcontaining:") and len(hint) >= 21:
                exceptions = []
                exclusion = hint[len("@anynotcontaining:"):].lstrip()
                if "|" in exclusion: exceptions = exclusion.split("|", )
                else: exceptions.append(exclusion)
                for dir in dirs:
                    for exception in exceptions:
                        if not exception in dir['label']:
                            rec_files, rec_dirs = self._browse_external(dir['path'], guidance[i+1:], parameters, unescaped_parameters, depth)
                            result_files += rec_files
                            result_dirs += rec_dirs
                            if result_files:
                                break
            elif hint.startswith("@anycontaining:") and len(hint) >= 18:
                rules = []
                inclusion = hint[len("@anycontaining:"):].lstrip()
                if "|" in inclusion: rules = inclusion.split("|", )
                else: rules.append(inclusion)
                for dir in dirs:
                    for rule in rules:
                        if rule in dir['label']:
                            rec_files, rec_dirs = self._browse_external(dir['path'], guidance[i+1:], parameters, unescaped_parameters, depth)
                            result_files += rec_files
                            result_dirs += rec_dirs
                            if result_files:
                                break
            else:
                next_page_hint = None
                maxdepth = 10
                if "@page:" in hint:
                    hint, next_page_hint = hint.split("@page:")
                    if "@depth:" in next_page_hint: next_page_hint, maxdepth = next_page_hint.split("@depth:")
                maxdepth = int(maxdepth)
                # Get matching directories
                matched_dirs = [x for x in dirs \
                 if Lister._has_match(x, hint, parameters)]

                # Next path is first matched directory
                if matched_dirs:
                    path = matched_dirs[0]['path']

                # Last hint
                if i == len(guidance) - 1:
                    # Get matching files
                    result_files = [x for x in files \
                     if Lister._has_match(x, hint, parameters)]
                    result_dirs = matched_dirs
                
                if next_page_hint and depth < maxdepth and path is None and not result_files:
                    next_page_dirs = [x for x in dirs \
                     if Lister._has_match(x, next_page_hint, parameters)]
                    if next_page_dirs:
                        rec_files, rec_dirs = self._browse_external(next_page_dirs[0]['path'], guidance[i:], parameters, unescaped_parameters, depth+1)
                        result_files += rec_files
                        result_dirs += rec_dirs
                        if result_files:
                            break
                
        # Always return some list (and not None)
        result_files = result_files or []
        result_dirs = result_dirs or []
        
        return result_files, result_dirs
