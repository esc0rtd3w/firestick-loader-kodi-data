from quality import atom


def mp4qual(meta,dfunc,u):
	try:
		atoms=atom.parse_mp4(meta)
	except IndexError:
		print "Too Short MP4 Header: %d bytes, Downloading 1M More" %(len(meta))
		h=dfunc(u,None,range=(len(meta)-1,len(meta)-1+1000000),tout=3)
		return mp4qual(meta+h,dfunc,u)
	if not atoms is None:
		videos=atoms[1]
		sounds=atoms[2]
		if len(videos)<1 or len(sounds)<1: 
			print "Too Short MP4 Header: %d bytes, Downloading 1M More" %(len(meta))
			h=dfunc(u,None,range=(len(meta)-1,len(meta)-1+1000000))
			return mp4qual(meta+h,dfunc,u)
		result={"stream_width":0,"stream_height":0,"stream_duration":0,"stream_sample_rate":0,"stream_audio_channels":0,"stream_sample_size":0}
		vid_size=0
		aud_size=0
		for video in videos:
			if result["stream_width"]*result["stream_height"] < video["video_width"]*video["video_height"] : 
				result["stream_width"]=video["video_width"]
				result["stream_height"]=video["video_height"]
				result["stream_video_codec"]=video["video_codec"]
			if result["stream_duration"] < video["video_duration"] : result["stream_duration"]=video["video_duration"]
			if vid_size < video["video_size"] : vid_size=video["video_size"]
		
		for sound in sounds:
			if result["stream_sample_rate"]*result["stream_audio_channels"]*result["stream_sample_size"] < sound["sound_sample_rate"]*sound["sound_sample_size"]*sound["sound_channels"]:
				result["stream_audio_codec"]=sound["sound_codec"]
				result["stream_audio_channels"]=sound["sound_channels"]
				result["stream_sample_size"]=sound["sound_sample_size"]
				result["stream_sample_rate"]=sound["sound_sample_rate"]
			if aud_size < sound["sound_size"] : aud_size=sound["sound_size"]
			if result["stream_duration"] < sound["sound_duration"] : result["stream_duration"]=sound["sound_duration"]

		result["stream_size"]=aud_size+vid_size
		result["stream_bitrate"]=result["stream_size"]/result["stream_duration"]*8.192
		result["stream_quality_rank"]=result["stream_width"]*result["stream_height"]*result["stream_bitrate"]/(18041918)
		return result
	else:
		print "Not an mp4 file try flv"
		return {}