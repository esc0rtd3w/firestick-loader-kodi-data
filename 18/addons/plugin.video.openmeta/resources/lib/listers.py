import re, copy, time, threading
import xbmc, xbmcgui, xbmcaddon
from resources.lib import text
from resources.lib.rpc import RPC
from resources.lib.xswift2 import plugin

IGNORE_CHARS = ('.', '%20')

def wait_for_dialog(dialog_id, timeout=None, interval=500):
	start = time.time()
	while not xbmc.getCondVisibility('Window.IsActive(%s)' % dialog_id):
		if xbmc.Monitor().abortRequested() or (timeout and time.time() - start >= timeout):
			return False
		xbmc.sleep(interval)
	return True

def list_dir(path):
	path = text.urlencode_path(path)
	try:
		response = RPC.Files.GetDirectory(media='files', directory=path, properties=['season','episode'])
	except:
		plugin.log.error(path)
		raise
	dirs = []
	files = []
	for item in response.get('files', []):
		if item.has_key('file') and item.has_key('filetype') and item.has_key('label'):
			if item['filetype'] == 'directory':
				for ext in ('.xsp', '.xml'):
					if item['file'].endswith(ext) or item['file'].endswith(ext+'/'):
						continue
				dirs.append({'path': item['file'], 'label': item['label'], 'season': item.get('season')})
			else:
				files.append({'path': item['file'], 'label': item['label'], 'season': item.get('season'), 'episode': item.get('episode')})
	return [path,dirs,files]

def regex_escape(string):
	for c in '\\.$^{[(|)*+?':
		string = string.replace(c, '\\' + c)
	return string

@plugin.cached(TTL=5, cache='browser')
def cached_list_dir(path, keyboard_hint=None):
	return list_dir(path)

class KeyboardMonitor(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.active = True
		self.search_term = None
		self.owner_thread = None
		self.lock = threading.Lock()
		self.access_lock = threading.RLock()
        
	def stop(self):
		self.active = False

	def set_term(self, search_term):
		self.lock.acquire()
		self.owner_thread = threading.current_thread()
		self.search_term = search_term

	def release(self):
		with self.access_lock:
			if self.owner_thread is not None:
				self.search_term = None
				self.owner_thread = None
				self.lock.release()

	def release_if_owner(self):
		with self.access_lock:
			if self.owner_thread is threading.current_thread():
				self.release()

	def prep_search_str(self, string):
		t_text = text.to_unicode(string)
		for chr in t_text:
			if ord(chr) >= 1488 and ord(chr) <= 1514:
				return text.to_utf8(string[::-1])
		return text.to_utf8(string)

	def run(self):
		while self.active and not xbmc.Monitor().abortRequested():
			if wait_for_dialog('virtualkeyboard', timeout=5, interval=100):
				if self.search_term is not None:
					xbmc.executebuiltin('Dialog.Close(virtualkeyboard, true)')
					text = self.prep_search_str(self.search_term)
					RPC.Input.SendText(text=text, done=True)
					self.release()

class Lister:
	def __init__(self, preserve_viewid=None, stop_flag=None):
		if stop_flag is None:
			stop_flag = threading.Event()
		self.stop_flag = stop_flag
		if preserve_viewid is None:
			window = xbmcgui.Window(xbmcgui.getCurrentWindowId())
			preserve_viewid = window.getFocusId()
		self.preserve_viewid = preserve_viewid
		self.keyboardMonitor = KeyboardMonitor()
		self.keyboardMonitor.start()

	def get(self, path, guidance, parameters):
		unescaped_parameters = parameters
		parameters = copy.deepcopy(parameters)
		for key, value in parameters.items():
			if isinstance(value, basestring):
				for c in IGNORE_CHARS:
					value = value.replace(c, ' ')
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

	@staticmethod
	def _has_match(item, pattern, parameters):
		season_infolabel_match = False
		if item.get('season'):
			item_season = str(item.get('season'))
			param_season = str(parameters.get('season', ''))
			if item_season == param_season:
				season_infolabel_match = True
		if pattern == '{season}' and season_infolabel_match:
			return True
		episode_infolabel_match = False
		if item.get('episode'):
			item_episode = str(item.get('episode'))
			param_episode = str(parameters.get('episode', ''))
			if item_episode == param_episode:
				episode_infolabel_match = True
		if pattern == '{episode}' and episode_infolabel_match:
			return True
		if pattern == '{season}x{episode}' and season_infolabel_match and episode_infolabel_match:
			return True
		label = item['label']
		pattern = text.to_unicode(pattern)
		pattern = pattern.replace('$$', r'($|^|\s|\]|\[)')
		first_season = False
		if '{season}' in pattern and '1' == str(parameters.get('season')):
			pattern = pattern.replace('{season}', '(?P<season>\d*)')
			first_season = True
		pattern = text.apply_parameters(pattern, parameters)    
		for c in IGNORE_CHARS:
			label = label.replace(c, ' ')
		pattern = text.to_unicode(text.to_utf8(pattern))
		label = text.to_unicode(text.to_utf8(label))
		if '$INFO[' in pattern:
			m = re.search('\\[(.*?)\]', pattern)
			info = m.group(1)
			pattern = pattern.replace('$INFO[%s]' % info, xbmc.getInfoLabel(info))
		if '$LOCALIZE[' in pattern:
			m = re.search('\[(\d+)\]', pattern)
			id = int(m.group(1))
			pattern = pattern.replace('$LOCALIZE[%s]' % id, xbmc.getLocalizedString(id).encode('utf-8'))
		if '$ADDON[' in pattern:
			m = re.search('\[.*\ (\d+)\]', pattern)
			aid = m.group(0).strip('[]').split(' ')[0]
			id = int(m.group(1))
			pattern = pattern.replace('$ADDON[%s %s]' % (aid, id), xbmcaddon.Addon(aid).getLocalizedString(id).encode('utf-8'))
		if pattern.startswith('><'):
			label = re.sub(r'\[[^)].*?\]', '', label)
			pattern = pattern.strip('><')
		plugin.log.debug('matching pattern %s to label %s' % (text.to_utf8(pattern), text.to_utf8(label)))
		r = re.compile(pattern, re.I|re.UNICODE)
		match = r.match(label)
		if ', The' in label and match is None:
			label = u'The ' + label.replace(', The', '')
			match = r.match(label)
		if match is not None and match.end() == len(label):
			if first_season and not match.group('season') in ('1', '', '01', None):
				return False
			plugin.log.debug('match: ' + text.to_utf8(label))
			return True
		return False

	def _restore_viewid(self):
		xbmc.executebuiltin('Container.SetViewMode(%d)' % self.preserve_viewid)

	def _browse_external(self, path, guidance, parameters, unescaped_parameters, depth=0):
		result_dirs = []
		result_files = []
		keyboard_hint = None
		for i, hint in enumerate(guidance):
			if self.stop_flag.isSet() or xbmc.Monitor().abortRequested():
				return [],[]
			if not path:
				break
			if hint.startswith('keyboard:'):
				hint = u'@' + hint
			if hint.startswith('@keyboard:') and i != len(guidance) - 1:
				term = hint[len('@keyboard:'):].lstrip()
				term = term.format(**unescaped_parameters)
				self.keyboardMonitor.set_term(term)
				keyboard_hint = term
				continue
			try:
				_, dirs, files = cached_list_dir(path, keyboard_hint)
			except:
				break
			finally:
				if keyboard_hint is not None:
					self.keyboardMonitor.release_if_owner()
					keyboard_hint = None
				self._restore_viewid()
			path = None
			if hint.startswith('><'):
				hint = hint.strip('><')
			if hint == '@any':
				for dir in dirs:
					rec_files, rec_dirs = self._browse_external(dir['path'], guidance[i+1:], parameters, unescaped_parameters, depth)
					result_files += rec_files
					result_dirs += rec_dirs
					if result_files:
						break
			elif hint.startswith('@anyexcept:') and len(hint) >= 14:
				exceptions = []
				exclusion = hint[len('@anyexcept:'):].lstrip()
				if '|' in exclusion:
					exceptions = exclusion.split('|', )
				else:
					exceptions.append(exclusion)
				for dir in dirs:
					if dir['label'] not in exceptions:
						rec_files, rec_dirs = self._browse_external(dir['path'], guidance[i+1:], parameters, unescaped_parameters, depth)
						result_files += rec_files
						result_dirs += rec_dirs
						if result_files:
							break
			elif hint.startswith('@anynotcontaining:') and len(hint) >= 21:
				exceptions = []
				exclusion = hint[len('@anynotcontaining:'):].lstrip()
				if '|' in exclusion:
					exceptions = exclusion.split('|', )
				else:
					exceptions.append(exclusion)
				for dir in dirs:
					for exception in exceptions:
						if not exception in dir['label']:
							rec_files, rec_dirs = self._browse_external(dir['path'], guidance[i+1:], parameters, unescaped_parameters, depth)
							result_files += rec_files
							result_dirs += rec_dirs
							if result_files:
								break
			elif hint.startswith('@anycontaining:') and len(hint) >= 18:
				rules = []
				inclusion = hint[len('@anycontaining:'):].lstrip()
				if '|' in inclusion:
					rules = inclusion.split('|', )
				else:
					rules.append(inclusion)
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
				if '@page:' in hint:
					if '$INFO[' in hint:
						m = re.search('\\[(.*?)\]', hint)
						info = m.group(1)
						hint = hint.replace('$INFO[%s]' % info, xbmc.getInfoLabel(info))
					if '$LOCALIZE[' in hint:
						m = re.search('\[(\d+)\]', hint)
						id = int(m.group(1))
						hint = hint.replace('$LOCALIZE[%s]' % id, xbmc.getLocalizedString(id).encode('utf-8'))
					if '$ADDON[' in hint:
						m = re.search('\[.*\ (\d+)\]', hint)
						aid = m.group(0).strip('[]').split(' ')[0]
						id = int(m.group(1))
						hint = hint.replace('$ADDON[%s %s]' % (aid, id), xbmcaddon.Addon(aid).getLocalizedString(id).encode('utf-8'))
					hint, next_page_hint = hint.split('@page:')
					if '@depth:' in next_page_hint:
						next_page_hint, maxdepth = next_page_hint.split('@depth:')
				maxdepth = int(maxdepth)
				matched_dirs = [x for x in dirs if Lister._has_match(x, hint, parameters)]
				if matched_dirs:
					path = matched_dirs[0]['path']
				if i == len(guidance) - 1:
					result_files = [x for x in files if Lister._has_match(x, hint, parameters)]
					result_dirs = matched_dirs
				if next_page_hint and depth < maxdepth and path is None and not result_files:
					next_page_dirs = [x for x in dirs if Lister._has_match(x, next_page_hint, parameters)]
					if next_page_dirs:
						rec_files, rec_dirs = self._browse_external(next_page_dirs[0]['path'], guidance[i:], parameters, unescaped_parameters, depth+1)
						result_files += rec_files
						result_dirs += rec_dirs
						if result_files:
							break
		result_files = result_files or []
		result_dirs = result_dirs or []
		return result_files, result_dirs