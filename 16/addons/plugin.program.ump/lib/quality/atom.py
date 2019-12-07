#atoms=["ainf","avcn", "bloc" ,"bpcc" ,"buff" ,"bxml" ,"ccid" ,"cdef" ,"clip" ,"cmap" ,"co64" ,"colr" ,"crgn" ,"crhd" ,"cslg" ,"ctab" ,"ctts" ,"cvru" ,"dinf" ,"dref" ,"dsgd" ,"dstg" ,"edts" ,"elst" ,"fdel" ,"feci" ,"fecr" ,"fiin" ,"fire" ,"fpar" ,"free" ,"frma" ,"ftyp" ,"gitn" ,"grpi" ,"hdlr" ,"hmhd" ,"hpix" ,"icnu" ,"ID32" ,"idat" ,"ihdr" ,"iinf" ,"iloc" ,"imap" ,"imif" ,"infe" ,"infu" ,"iods" ,"iphd" ,"ipmc" ,"ipro" ,"iref" ,"jP$20$20" ,"jp2c" ,"jp2h" ,"jp2i" ,"kmat" ,"leva" ,"load" ,"lrcu" ,"m7hd" ,"matt" ,"mdat" ,"mdhd" ,"mdia" ,"mdri" ,"meco" ,"mehd" ,"mere" ,"meta" ,"mfhd" ,"mfra" ,"mfro" ,"minf" ,"mjhd" ,"moof" ,"moov" ,"mvcg" ,"mvci" ,"mvex" ,"mvhd" ,"mvra" ,"nmhd" ,"ochd" ,"odaf" ,"odda" ,"odhd" ,"odhe" ,"odrb" ,"odrm" ,"odtt" ,"ohdr" ,"padb" ,"paen" ,"pclr" ,"pdin" ,"pitm" ,"pnot" ,"prft" ,"res$20" ,"resc" ,"resd" ,"rinf" ,"saio" ,"saiz" ,"sbgp" ,"schi" ,"schm" ,"sdep" ,"sdhd" ,"sdtp" ,"sdvp" ,"segr" ,"senc" ,"sgpd" ,"sidx" ,"sinf" ,"skip" ,"smhd" ,"srmb" ,"srmc" ,"srpp" ,"ssix" ,"stbl" ,"stco" ,"stdp" ,"sthd" ,"strd" ,"stri" ,"stsc" ,"stsd" ,"stsg" ,"stsh" ,"stss" ,"stsz" ,"stts" ,"styp" ,"stz2" ,"subs" ,"swtc" ,"tfad" ,"tfdt" ,"tfhd" ,"tfma" ,"tfra" ,"tibr" ,"tiri" ,"tkhd" ,"traf" ,"trak" ,"tref" ,"trex" ,"trgr" ,"trik" ,"trun" ,"udta" ,"uinf" ,"UITS" ,"ulst" ,"url$20" ,"uuid" ,"vmhd" ,"vwdi" ,"xml$20" ,"xml$20" ,"albm" ,"angl" ,"auth" ,"clfn" ,"clid" ,"clsf" ,"cmid" ,"cmnm" ,"coll" ,"cprt" ,"date" ,"dscp" ,"gnre" ,"hinf" ,"hnti" ,"hpix" ,"kywd" ,"loci" ,"manu" ,"modl" ,"perf" ,"reel" ,"rtng" ,"scen" ,"shot" ,"slno" ,"strk" ,"thmb" ,"titl" ,"tsel" ,"tsel" ,"urat" ,"yrrc" ,"albm" ,"auth" ,"clip" ,"clsf" ,"cprt" ,"crgn" ,"ctab" ,"dcfD" ,"elng" ,"imap" ,"kmat" ,"load" ,"matt" ,"pnot" ,"wide"]
def get_int(asci):
	try:
		val=int(asci.encode("hex"),16)
	except Exception, e:
		print "Exception Returned: " + str(e)
		return 0
	return val

def parse_hdlr(stream):
	hdlr={}
	hdlr["version"]=get_int(stream[0:1])
	hdlr["flags"]=get_int(stream[1:4]) # 0
	hdlr["component_type"]=stream[4:8]
	hdlr["component_subtype"]=stream[8:12]
	hdlr["component_manufacturer"]=get_int(stream[12:16]) #0
	hdlr["component_flags"]=get_int(stream[16:20]) #0
	hdlr["component_flags_mask"]=get_int(stream[20:24]) # 0
	hdlr["component_name"]=stream[24:-8]
	return hdlr

def parse_ftyp(stream):
	ftype={}
	ftype["major_brand"]=stream[0:4]
	ftype["minor_version"]=get_int(stream[4:8])
	ftype["compatible_brands"]=[stream[i:i+4] for i in range(8, len(stream[8:])+4, 4)]
	return ftype

def parse_tkhd(stream):
	tkhd={}
	tkhd["version"]=get_int(stream[0:1])
	tkhd["flags"]=get_int(stream[1:4]) #1: enabled, 2:used in movie, 4: used in preview, 8: used in poster
	tkhd["creation_time"]=get_int(stream[4:8])
	tkhd["modification_time"]=get_int(stream[8:12])
	tkhd["track_id"]=get_int(stream[12:16])
	tkhd["duration"]=get_int(stream[20:24])
	tkhd["layer"]=get_int(stream[32:34])
	tkhd["alternate_group"]=get_int(stream[34:36]) # 0: vide , 1:soun ,2:subt
	tkhd["volume"]=get_int(stream[36:38])
	tkhd["width"]=get_int(stream[74:78])
	tkhd["height"]=get_int(stream[78:82])
	return tkhd

def parse_stsz(stream):
	stsz={}
	stsz["version"]=get_int(stream[0:1])
	stsz["flags"]=get_int(stream[1:4]) 
	stsz["sample_size"]=get_int(stream[4:8])
	stsz["number_of_entries"]=get_int(stream[8:12])
	stsz["sample_size_table"]=[get_int(stream[i:i+4]) for i in range(12, len(stream[12:])+4, 4)]
	return stsz

def parse_stsd(stream):
	stsd={}
	stsd["version"]=get_int(stream[0:1])
	stsd["flags"]=get_int(stream[1:4]) 
	stsd["number_of_entries"]=get_int(stream[4:8])
	stsd["desc_table_size"]=get_int(stream[8:12])
	stsd["desc_table_data_format"]=stream[12:16]
	stsd["des_table_ref_index"]=stream[22:24]
	if stsd["desc_table_data_format"] in ("mp4a","samr","ac-3"):
		stsd["desc_version"]=get_int(stream[24:26])
		if stsd["desc_version"]==0:
			stsd["desc_num_channel"]=get_int(stream[32:34])
			stsd["desc_sample_size"]=get_int(stream[34:36])
			stsd["desc_sample_rate"]=get_int(stream[38:42])
	return stsd

def get_audio_codec(code):
	codecs=["AAC Main","AAC LC (Low Complexity)","AAC SSR (Scalable Sample Rate)","AAC LTP (Long Term Prediction)","SBR (Spectral Band Replication)","AAC Scalable","TwinVQ","CELP (Code Excited Linear Prediction)","HXVC (Harmonic Vector eXcitation Coding)","NA","NA","TTSI (Text-To-Speech Interface)","Main Synthesis","Wavetable Synthesis","General MIDI","Algorithmic Synthesis and Audio Effects","ER (Error Resilient) AAC LC","NA","ER AAC LTP","ER AAC Scalable","ER TwinVQ","ER BSAC (Bit-Sliced Arithmetic Coding)","ER AAC LD (Low Delay)","ER CELP","ER HVXC","ER HILN (Harmonic and Individual Lines plus Noise)","ER Parametric","SSC (SinuSoidal Coding)","PS (Parametric Stereo)","MPEG Surround","NA","Layer-1","Layer-2","Layer-3","DST (Direct Stream Transfer)","ALS (Audio Lossless)","SLS (Scalable LosslesS)","SLS non-core","ER AAC ELD (Enhanced Low Delay)","SMR (Symbolic Music Representation) Simple","SMR Main","USAC (Unified Speech and Audio Coding) (no SBR)","SAOC (Spatial Audio Object Coding)","LD MPEG Surround","USAC"]
	return codecs[code]

def parse_esds(stream):
	esds={}
	esds["version"]=get_int(stream[0:1])
	esds["flags"]=get_int(stream[1:4])
	esds["codec"]=get_audio_codec(get_int(stream[4:5]))


def find_atoms(stream,name):
	atoms=[]
	i=0
	offset=0
	while True:
		i+=1
		try:
			ind=stream.index(name)
		except ValueError:
			break
		offset=int(stream[ind-4:ind].encode("hex"),16)
		value=stream[ind+4:ind+offset]
		atoms.append([name,value])
		stream=stream[ind-4+offset:]
	return atoms

def parse_mp4(meta):
	ftyp=find_atoms(meta,"ftyp")
	if len(ftyp) > 0 :
		ftyp= parse_ftyp(ftyp[0][1])
	else :
		return None
	videos=[]
	audios=[]
	for trak in find_atoms(meta,"trak"):
		mdia=find_atoms(trak[1],"mdia")
		hdlr=find_atoms(mdia[0][1],"hdlr")
		hdlr=parse_hdlr(hdlr[0][1])
		if hdlr["component_subtype"]=="vide":
			prop={}
			#print "Video Stream Found : " + hdlr["component_name"]
			tkhd=find_atoms(trak[1],"tkhd")
			tkhd=parse_tkhd(tkhd[0][1])
			prop["video_duration"]=float(tkhd["duration"])/1000
			prop["video_width"]=tkhd["width"]
			prop["video_height"]=tkhd["height"]
			stbl=find_atoms(find_atoms(mdia[0][1],"minf")[0][1],"stbl")
			stsz=find_atoms(stbl[0][1],"stsz")
			stsz_atom=parse_stsz(stsz[0][1])
			if stsz_atom["sample_size"]==0 :
				data_size=sum(stsz_atom["sample_size_table"])
			else:
				data_size=stsz_atom["sample_size"]*stsz_atom["number_of_entries"]
			prop["video_size"]=float(data_size)/1024
			prop["video_bitrate"]=data_size/tkhd["duration"]*8.192
			stsd=find_atoms(stbl[0][1],"stsd")
			#Determine the codec:
			found_codec=stsd[0][1][12:16]
			prop["video_codec"]=found_codec
			videos.append(prop)
		elif hdlr["component_subtype"]=="soun":
			#print "Sound Stream Found : " + hdlr["component_name"]
			prop={}
			tkhd=find_atoms(trak[1],"tkhd")
			tkhd=parse_tkhd(tkhd[0][1])
			prop["sound_duration"]=float(tkhd["duration"])/1000
			stbl=find_atoms(find_atoms(mdia[0][1],"minf")[0][1],"stbl")
			stsz=find_atoms(stbl[0][1],"stsz")
			stsz_atom=parse_stsz(stsz[0][1])
			if stsz_atom["sample_size"]==0 :
				data_size=sum(stsz_atom["sample_size_table"])
			else:
				data_size=stsz_atom["sample_size"]*stsz_atom["number_of_entries"]
			prop["sound_size"]=float(data_size)/1024
			prop["sound_bitrate"]=data_size/tkhd["duration"]*8.192
			stsd=find_atoms(stbl[0][1],"stsd")
			stsd=parse_stsd(stsd[0][1])
			prop["sound_codec"]=stsd["desc_table_data_format"]
			prop["sound_channels"]=stsd["desc_num_channel"]
			prop["sound_sample_size"]=stsd["desc_sample_size"]
			prop["sound_sample_rate"]=stsd["desc_sample_rate"]
			audios.append(prop)
		else:
			print "Skipping " + hdlr["component_subtype"] + " stream : " + hdlr["component_name"]
		for tkhd in find_atoms(trak[1],"tkhd"):
			continue
			#print parse_tkhd(tkhd[1])
		continue

	return [ftyp, sorted(videos), sorted(audios)]