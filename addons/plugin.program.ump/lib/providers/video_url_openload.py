# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
from third import youtube_dl
domain="https://openload.co/"
timeout=60*60*24
def run(hash,ump,referer=""):
	ydl = youtube_dl.YoutubeDL({"quiet":True,"nocheckcertificate":True})

	with ydl:
		result = ydl.extract_info(domain+"embed/"+hash,	download=False)

	if 'entries' in result:
		# Can be a playlist or a list of videos
		audio = result['entries'][0]
	else:
		# Just a video
		audio = result
	
	return {"audio":audio["url"]}