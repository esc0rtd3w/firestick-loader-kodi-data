#-------------------------------------------------------------------------------
# Name:		get_image_size
# Purpose:	 extract image dimensions given a file path using just
#			  core modules
#
# Author:	  Paulo Scardine (based on code from Emmanuel VAISSE)
#             Ported to stream data by Huseyin BIYIK
#
# Created:	 26/09/2013
# Copyright:   (c) Paulo Scardine 2013
# Licence:	 MIT
#-------------------------------------------------------------------------------
#!/usr/bin/env python
import struct


class UnknownImageFormat(Exception):
	pass

class NotEnoughData(Exception):
	pass

def read(offset,ln,data):
	if offset>len(data):
		raise NotEnoughData("Not Enough stream  legth ( %d ) for header"%len(data))
	return offset+ln,data[offset:offset+ln]


def get_image_size(data):
	"""
	Return (width, height) for a given img file content - no external
	dependencies except the os and struct modules from core
	"""
	size=len(data)
	height = -1
	width = -1
	type= -1
	if (size >= 10) and data[:6] in ('GIF87a', 'GIF89a'):
		# GIFs
		w, h = struct.unpack("<HH", data[6:10])
		width = int(w)
		height = int(h)
		type= "gif"
	elif ((size >= 24) and data.startswith('\211PNG\r\n\032\n')
		  and (data[12:16] == 'IHDR')):
		# PNGs
		w, h = struct.unpack(">LL", data[16:24])
		width = int(w)
		height = int(h)
		type= "png"
	elif (size >= 16) and data.startswith('\211PNG\r\n\032\n'):
		# older PNGs?
		w, h = struct.unpack(">LL", data[8:16])
		width = int(w)
		height = int(h)
		type = "png"
	elif (size >= 2) and data.startswith('\377\330'):
		# JPEG
		type= "jpeg"
		msg = " raised while trying to decode as JPEG."
		offs=0
		offs,c = read(offs,2,data)
		offs,byte = read(offs,1,data)
		try:
			while byte != b"":
				while byte != b'\xff': 
					offs,byte = read(offs,1,data)
				while byte == b'\xff': 
					offs,byte = read(offs,1,data)
				hasChunk = ord(byte) not in range( 0xD0, 0xDA) + [0x00]
				if hasChunk:
					offs,cs=read(offs,2,data)
					ChunkSize   =  struct.unpack( ">H", cs)[0]  - 2
					Next_ChunkOffset = offs + ChunkSize
				
				if (byte >= b'\xC0' and byte <= b'\xC3'):
					# Found  SOF1..3 data chunk - Read it and quit
					offs,c = read(offs,1,data)
					offs,h=read(offs,2,data)
					h = struct.unpack( ">H", h)[0]
					offs,w=read(offs,2,data)
					w = struct.unpack( ">H", w)[0]
					break

				elif (byte == b'\xD9') or offs >=len(data):
					# Found End of Image
					EOI = offs
					break
#				else:
				# Seek to next data chunk
#					print "Pos: %.4x %x" % (offs, ChunkSize)

				if hasChunk :
					offs=Next_ChunkOffset

				byte = read(offs,1,data)

			width = int(w)
			height = int(h)
		except struct.error:
			raise UnknownImageFormat("StructError" + msg)
		except ValueError:
			raise UnknownImageFormat("ValueError" + msg)
#		except Exception as e:
#			raise UnknownImageFormat(e.__class__.__name__ + msg)
	else:
		raise UnknownImageFormat(
			"Sorry, don't know how to get information from this file."
		)

	return type,width, height