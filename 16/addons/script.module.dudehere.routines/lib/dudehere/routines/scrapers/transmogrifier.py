import xbmcaddon
import xbmcgui
from dudehere.routines import *
from dudehere.routines.scrapers import CommonScraper, ScraperResult
from dudehere.routines import plugin
from dudehere.routines.transmogrifier import TransmogrifierAPI

def validate_transmogrifier():
	try:
		installed = plugin.get_condition_visiblity('System.HasAddon(service.transmogrifier)') == 1
		if installed:
			return plugin.get_setting('enable_transmogrifier', addon_id='service.transmogrifier') == "true"
		else:
			return False
	except:
		return False

class transmogrifierScraper(CommonScraper):
	def __init__(self):
		self.service='transmogrified'
		self.name = 'transmogrified'
		self.referrer = 'http://localhost'
		self.base_url = 'http://localhost'
		self.is_cachable = False
		self.broken = validate_transmogrifier() == False
		try:
			self.working_dir = xbmcaddon.Addon('service.transmogrifier').getSetting('save_directory')
		except:
			self.working_dir = ''
		self.get_debrid_hosts()
			
	def search_tvshow(self, args):
		self.domains = args['domains']
		results = []
		response = self.prepair_query('tvshow', args['showname'], args['season'], args['episode'])
		if response:
			results = self.process_results(response)
		return self.get_response(results)
	
	def search_movie(self, args):
		self.domains = args['domains']
		results = []
		response = self.prepair_query('movie', args['title'], args['year'])
		if response:
			results = self.process_results(response)
		return self.get_response(results)
	
	def process_results(self, response):
		results = []
		url = "%s://%s" % (self.service, response['url'])
		result = ScraperResult(self.debrid_hosts, self.service, 'transmogrified', url)
		result.quality = QUALITY.LOCAL
		result.size = response['size']
		results += [result]
		return results
	
	def get_resolved_url(self, raw_url):
		resolved_url = raw_url
		win = xbmcgui.Window(10000)
		win.setProperty('GenericPlaybackService.Path', resolved_url)
		return resolved_url
		
	def prepair_query(self, media, *args, **kwards):
		TM = TransmogrifierAPI()
		if media == 'tvshow':
			response = TM.get_cached_file(args[0], str(args[1]).zfill(2), str(args[2]).zfill(2))
			if response:
				return response
		else:
			response = TM.get_cached_file(args[0], args[1])
			if response:
				return response
		return False
