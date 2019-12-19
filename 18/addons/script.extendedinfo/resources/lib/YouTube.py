from resources.lib import Utils

API_key = 'AIzaSyA-7-vxSFjNqfcOyCG33rwzRB0UZW30Pic'

def handle_youtube_videos(results, extended=False):
	videos = []
	for item in results:
		thumb = ''
		if 'thumbnails' in item['snippet']:
			thumb = item['snippet']['thumbnails']['high']['url']
		try:
			video_id = item['id']['videoId']
		except:
			video_id = item['snippet']['resourceId']['videoId']
		video = {
			'thumb': thumb,
			'youtube_id': video_id,
			'Play': 'plugin://script.extendedinfo?info=youtubevideo&&id=' + video_id,
			'path': 'plugin://script.extendedinfo?info=youtubevideo&&id=' + video_id,
			'Description': item['snippet']['description'],
			'title': item['snippet']['title'],
			'channel_title': item['snippet']['channelTitle'],
			'channel_id': item['snippet']['channelId'],
			'Date': item['snippet']['publishedAt'].replace('T', ' ').replace('.000Z', '')[:-3]
			}
		videos.append(video)
	if not extended:
		return videos
	video_ids = [item['youtube_id'] for item in videos]
	url = 'https://www.googleapis.com/youtube/v3/videos?id=%s&part=contentDetails%%2Cstatistics&key=AIzaSyA-7-vxSFjNqfcOyCG33rwzRB0UZW30Pic' % (','.join(video_ids))
	ext_results = Utils.get_JSON_response(url=url, cache_days=0.5, folder='YouTube')
	if not ext_results:
		return videos
	for i, item in enumerate(videos):
		for ext_item in ext_results['items']:
			if not item['youtube_id'] == ext_item['id']:
				continue
			item['duration'] = ext_item['contentDetails']['duration'][2:].lower()
			item['dimension'] = ext_item['contentDetails']['dimension']
			item['definition'] = ext_item['contentDetails']['definition']
			item['caption'] = ext_item['contentDetails']['caption']
			if 'statistics' in ext_item:
				if 'viewCount' in ext_item['statistics']:
					item['viewcount'] = Utils.millify(ext_item['statistics']['viewCount'])
				else:
					item['viewcount'] = 'unknown'
				if 'viewCount' in ext_item['statistics']:
					item['likes'] = ext_item['statistics'].get('likeCount')
				else:
					item['likes'] = 'unknown'
				if 'dislikeCount' in ext_item['statistics']:
					item['dislikes'] = ext_item['statistics'].get('dislikeCount')
				else:
					item['dislikes'] = 'unknown'
			else:
				item['viewcount'] = 'unknown'
				item['likes'] = 'unknown'
				item['dislikes'] = 'unknown'
			if item['likes'] and item['likes'] != 'unknown' and item['dislikes'] and item['dislikes'] != 'unknown':
				vote_count = float(int(item['likes']) + int(item['dislikes']))
				if vote_count > 0:
					item['rating'] = format(float(item['likes']) / vote_count * 10, '.2f')
			break
		else:
			item['duration'] = ''
	return videos

def search_youtube(search_str='', hd='', limit=10, extended=True, page='', filter_str=''):
	if page:
		page = '&pageToken=' + page
	if hd and not hd == 'false':
		hd = '&hd=true'
	else:
		hd = ''
	search_str = '&q=' + Utils.url_quote(search_str.replace('"', ''))
	url = 'https://www.googleapis.com/youtube/v3/search?part=id%%2Csnippet&type=video%s%s&order=relevance&%skey=%s%s&maxResults=%i' % (page, search_str, filter_str, API_key, hd, int(limit))
	results = Utils.get_JSON_response(url=url, cache_days=0.5, folder='YouTube')
	videos = handle_youtube_videos(results['items'], extended=extended)
	if videos:
		info = {
			'listitems': videos,
			'results_per_page': results['pageInfo']['resultsPerPage'],
			'total_results': results['pageInfo']['totalResults'],
			'next_page_token': results.get('nextPageToken', ''),
			'prev_page_token': results.get('prevPageToken', '')
			}
		return info
	else:
		return {}