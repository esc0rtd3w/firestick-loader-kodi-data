""" youtube_playlist_ripper rips a youtube playlist for XMBC.

    based on Mark Wolstenholme <markfiend at gmail dot com> youtube_playlist_ripper

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

"""

import urllib2
import json
import os
import time

class PlayListRipper:
	"""Given a youtube playlist, convert it to a playlist for XBMC.

	Requires the youtube plugin for XBMC.

	PROPERTIES:
	url:        string: Base URL for the youtube playlist API
	output:     string: Unicode output for the output playlist

	METHODS:
	__init__:   Initialisation.
	output_add: Append a line to the output
	save:       Write the output to file
	rip:        Translate the JSON from the youtube API into format for XBMC
	usage:      Print out some help.

	You will need a free youtube API key from Google. Generate a
	public API access key for server applications and paste it into
	the code just below.  
	"""
	API_KEY = 'AIzaSyDp7v84376jtBeSkWZxZNaIZoJH7ehH_L8'

	def __init__(self):
		"Initialise the object."
		self.url = 'https://www.googleapis.com/youtube/v3/playlistItems'
		self.output = ''		

	def output_add(self, string):
		"Append a line to the output."
		self.output += string		
		
	def getRipped(self, file_name, cacheDir, duration):
		"get the ripped data file"						
		content=None		
		cacheFile = os.path.join(cacheDir, file_name)		
		if len(cacheFile) > 255:			
			cacheFile = cacheFile[:255]		
		if os.path.exists(cacheFile) and duration!=0 and (time.time()-os.path.getmtime(cacheFile) < 60*60*24*duration):				
			fh = open(cacheFile, 'r')
			content = fh.read()
			fh.close()		
		return content

	def save(self, file_name, cacheDir):
		"Actually write the output to the file."		
		cacheFile = os.path.join(cacheDir, file_name)
		if len(cacheFile) > 255:
			cacheFile = cacheFile[:255]		
		else:		
			fh = open(cacheFile, 'wb')		
			fh.write(self.output.encode('utf-8'))
			fh.close()
		return self.output

	def rip(self, playlist_id):
		"""Get the JSON object from the playlist and translate it.

		The youtube API will not allow you to retrieve the entire
		playlist in one go; we have to do it a page at a time. The
		JSON will contain a nextPageToken item if there is a next
		page.
		"""
		pl_url = self.url + '?part=snippet&key=' + \
				 self.API_KEY + '&playlistId=' + playlist_id

		nextpage = None
		self.output_add('{\n"items": [\n')
		first_item = True
		
		while True:
			# Loop through the playlist's pages. 
			if nextpage is None:
				url = pl_url
			else:
				url = pl_url + '&pageToken=' + nextpage

			response = urllib2.urlopen(url)
			str_response = response.read().decode('utf-8')
			data = json.loads(str_response)

			for item in data['items']:
				if not first_item:
					self.output_add(',\n')
				else:
					first_item = False
				item['snippet']['title'] = item['snippet']['title'].replace('"','')
				self.output_add('{\n"title": "'+ item['snippet']['title']+
								'",\n"video_id": "'+item['snippet']['resourceId']['videoId']+'",\n')
				if ('thumbnails' in item['snippet']):
					if ('standard' in item['snippet']['thumbnails']):
						self.output_add('"img": "'+item['snippet']['thumbnails']['standard']['url']+'"\n}')
					elif ('high'in item['snippet']['thumbnails']):
						self.output_add('"img": "'+item['snippet']['thumbnails']['high']['url']+'"\n}')
					elif ('medium' in item['snippet']['thumbnails'] != None):
						self.output_add('"img: "'+item['snippet']['thumbnails']['medium']['url']+'"\n}')
					elif ('default' in item['snippet']['thumbnails'] != None):
						self.output_add('"img: "'+item['snippet']['thumbnails']['default']['url']+'"\n}')
				else:
					self.output_add('"img": ""\n}')

			if 'nextPageToken' in data:
				nextpage = data['nextPageToken']
			else:
				self.output_add('\n]\n}\n')
				break