import re
import struct


def find_atom(url,referer,cur,name):
	while True:
		offset,atom=name_atom(url,referer,cur)
		if atom==name:
			return cur,offset
		else:
			cur+=offset

def name_atom(url,referer,cur):
	return struct.unpack(">i4s", dfunc(url,None,referer=referer,range=(cur,cur+7)))


def vidqual(url,dfunc,referer):
	globals()['dfunc'] = dfunc
	ret={}
	first8=dfunc(url,None,range=(0,7),referer=referer)
	offset,atom=struct.unpack(">i4s", first8)
	if atom=="ftyp":
		ret["type"]="mp4"
		cur,offset=find_atom(url,referer,offset,"moov")
		while True:
			cur,offset=find_atom(url,referer,cur+8,"trak")
			##it is possible not to meet first trak as video
			cur2,offset2=find_atom(url,referer,cur+8,"tkhd")
			w,h = struct.unpack(">II", dfunc(url,None,referer=referer,range=(cur2+82,cur2+89)))
			if abs(w) < 5000 and abs(h)< 5000:
				ret["width"]=int(w)
				ret["height"]=int(h)
				resp=dfunc(url,None,referer=referer,head=True)
				ret["size"]=int(resp.info().getheader('Content-Length'))
				break
	elif first8[:3]=="FLV":
		b1,b2,b3=struct.unpack("3B",dfunc(url,None,referer=referer,range=(14,16)))
		size=(b1 << 16) + (b2 << 8) + b3
		header=dfunc(url,None,referer=referer,range=(27,27+size))
		width=re.findall("width.(........)",header)
		height=re.findall("height.(........)",header)
		if len(width)>0:
			ret["width"]=int(struct.unpack(">d",width[0])[0])
		if len(height)>0:
			ret["height"]=int(struct.unpack(">d",height[0])[0])
		resp=dfunc(url,None,referer=referer,head=True)
		ret["size"]=int(resp.info().getheader('Content-Length'))
		ret["type"]="flv"
	return ret
#u1="http://download.wavetlan.com/SVV/Media/HTTP/MP4/ConvertedFiles/SUPER/SUPER_Test2_2m40s_AVC_VBR_540kbps_480x320_25fps_AMRNB_CBR_6.4kbps_Stereo_8000Hz.MP4"
#print extract_mp4(u1)
#print time.time()-t1