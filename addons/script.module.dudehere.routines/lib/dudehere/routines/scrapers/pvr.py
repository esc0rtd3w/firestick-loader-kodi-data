import re
import json
import xbmc

from dudehere.routines import *
from dudehere.routines.scrapers import CommonScraper, ScraperResult
from dudehere.routines.vfs import VFSClass
from BeautifulSoup import BeautifulSoup, Tag
vfs = VFSClass()

class pvrScraper(CommonScraper):
	broken = xbmc.getCondVisibility( "Pvr.HasTVChannels" ) == 0
	def __init__(self):
		self.service='pvr'
		self.name = 'LocalPVR'
		self.referrer = 'http://localhost'
		self.base_url = 'http://localhost'
		self.is_cachable = False
		self.setup_source()
		self.get_debrid_hosts()
	
	def setup_source(self):
		source_path = vfs.join('special://profile/', 'sources.xml')
		try:
			soup = vfs.read_file(source_path, soup=True)
		except:
			soup = BeautifulSoup()
			sources_tag = Tag(soup, "sources")
			soup.insert(0, sources_tag)
			
		if soup.find("video") == None:
			sources = soup.find("sources")
			if not sources: return
			video_tag = Tag(soup, "video")
			sources.insert(0, video_tag)
		
		video = soup.find("video")
		if len(soup.findAll(text="PVR Recordings")) < 1:
			pvr_source_tag = Tag(soup, "source")
			pvr_name_tag = Tag(soup, "name")
			pvr_name_tag.insert(0, "PVR Recordings")
			PVR_PATH_tag = Tag(soup, "path")
			PVR_PATH_tag['pathversion'] = 1
			PVR_PATH_tag.insert(0, "pvr://recordings/active/Default/")
			pvr_source_tag.insert(0, pvr_name_tag)
			pvr_source_tag.insert(1, PVR_PATH_tag)
			video.insert(2, pvr_source_tag)
			string = ""
			for i in soup:
				string = string + str(i)

			vfs.write_file(source_path, string)
			
	def search_tvshow(self, args):
		results = []
		path = self.prepair_query('tvshow', args['showname'], args['season'], args['episode'], args['imdb_id'])
		if path:
			results = self.process_results(path)
		return self.get_response(results)
	
	def process_results(self, path):
		results = []
		url = "%s://%s" % (self.service, path)
		result = ScraperResult(self.debrid_hosts, self.service, self.name, url)
		result.quality = QUALITY.LOCAL
		results += [result]
		return results
	
	def get_resolved_url(self, raw_url):
		resolved_url = raw_url
		return resolved_url
	
	def aired_match(self, aired):
		date = aired.split('T')[0]
		return date.replace('-', '')
		
		
	def prepair_query(self, media, *args, **kwards):
		if media == 'tvshow':
			title = args[0]
			season = args[1]
			episode = args[2]
			imdb_id = args[3]
			cmd = '{"jsonrpc":"2.0","method":"Files.GetDirectory","id":1,"params":["pvr://recordings/active/Default/%s/","video",["title","file"],{"method":"title","order":"ascending"}]}'
			data = json.loads(xbmc.executeJSONRPC(cmd % title))
			if 'result' in data and 'files' in data['result']:
				from dudehere.routines.trakt import TraktAPI
				trakt = TraktAPI()
				metadata = trakt.get_metadata('episode', imdb_id, '', '', '', season, episode)
				aired_match = self.aired_match(metadata['premiered'])
				aired = re.compile(', (\d+)_\d+.pvr$')
				for f in data['result']['files']:
					match = aired.search(f['file'])
					if match:
						if aired_match == match.group(1):
							return f['file']

			
		return False
