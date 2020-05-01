# -*- coding: utf-8 -*-

import base64
import urlparse
import urllib
import hashlib
import re

from resources.lib.modules import client
from resources.lib.modules import directstream
from resources.lib.modules import pyaes


HDCAM = ['hdcam', 'hd cam', 'hd-cam', 'hd.cam', 'hdts', 'hd ts', 'hd-ts', 'hd.ts']

CODEC_H265 = ['hevc', 'h265', 'h.265', 'x265', 'x.265']
CODEC_H264 = ['avc', 'h264', 'h.264', 'x264', 'x.264']
CODEC_XVID = ['xvid', 'x.vid', 'x-vid']
CODEC_DIVX = ['divx', 'divx ', 'div2', 'div2 ', 'div3']
CODEC_MPEG = ['mp4', 'mpeg', 'm4v', 'mpg', 'mpg1', 'mpg2', 'mpg3', 'mpg4', 'mp4 ', 'mpeg ', 'msmpeg', 'msmpeg4', 'mpegurl']
CODEC_AVI = ['avi']
CODEC_MKV = ['mkv', '.mkv', 'matroska']

AUDIO_8CH = ['ch8', '8ch', '7.1', '7-1']
AUDIO_7CH = ['ch7', '7ch', '6.1', '6-1']
AUDIO_6CH = ['ch6', '6ch', '5.1', '5-1']
AUDIO_2CH = ['ch2', '2ch', '2.0', 'stereo']
AUDIO_1CH = ['ch1', '1ch', 'mono', 'monoaudio']

MULTI_LANG = ['hindi.eng', 'ara.eng', 'ces.eng', 'chi.eng', 'cze.eng', 'dan.eng', 'dut.eng', 'ell.eng', 'esl.eng',
							'esp.eng', 'fin.eng', 'fra.eng', 'fre.eng', 'frn.eng', 'gai.eng', 'ger.eng', 'gle.eng', 'gre.eng', 'gtm.eng',
							'heb.eng', 'hin.eng', 'hun.eng', 'ind.eng', 'iri.eng', 'ita.eng', 'jap.eng', 'jpn.eng', 'kor.eng', 'lat.eng',
							'lebb.eng', 'lit.eng', 'nor.eng', 'pol.eng', 'por.eng', 'rus.eng', 'som.eng', 'spa.eng', 'sve.eng',
							'swe.eng', 'tha.eng', 'tur.eng', 'uae.eng', 'ukr.eng', 'vie.eng', 'zho.eng', 'dual audio', 'dual-audio',
							'dual.audio', 'multi']

SUBS = ['subs', 'subtitula', 'subfrench', 'subspanish', 'swesub']
ADDS = ['1xbet', 'betwin']



def getFileType(url):
	try:
		url = url.lower()
		url = url.replace(' ', '.')
	except:
		url = str(url)
	type = ''
	if any(value in url for value in ['bluray', 'blu-ray', 'blu.ray']):
		type += ' BLURAY /'
	if any(value in url for value in ['bd-r', 'bd.r', 'bdr', 'bd-rip', 'bd.rip', 'bdrip', 'brrip', 'br.rip']):
		type += ' BR-RIP /'
	if 'remux' in url:
		type += ' REMUX /'
	if any(i in url for i in ['dvd-rip', 'dvd.rip', 'dvdrip']):
		type += ' DVD /'
	if any(value in url for value in ['web-dl', 'web.dl', 'webdl', 'web-rip', 'web.rip', 'webrip']):
		type += ' WEB /'
	if 'hdtv' in url:
		type += ' HDTV /'
	if 'sdtv' in url:
		type += ' SDTV /'
	if any(value in url for value in ['hd-rip', 'hd.rip', 'hdrip']):
		type += ' HDRIP /'
	if 'hdr.' in url:
		type += ' HDR /'
	if any(value in url for value in ['dd5.1', 'dd-5.1', 'dd5-1', 'dolby-digital', 'dolby.digital']):
		type += ' DOLBYDIGITAL /'
	if any(value in url for value in ['.ddex', 'dd-ex', 'dolby-ex', 'dolby.digital.ex']):
		type += ' DD-EX /'
	if any(value in url for value in ['dolby-digital-plus', 'dolby.digital.plus', 'ddplus', 'dd-plus']):
		type += ' DD+ /'
	if any(value in url for value in ['true-hd', 'truehd', '.ddhd']):
		type += ' DOLBY-TRUEHD /'
	if 'atmos' in url:
		type += ' ATMOS /'
	if '.dts.' in url:
		type += ' DTS /'
	if any(value in url for value in ['dts-hd', 'dtshd', 'dts.hd']):
		type += ' DTS-HD /'
	if any(value in url for value in ['dts-es', 'dtses', 'dts.es']):
		type += ' DTS-ES /'
	if any(value in url for value in ['dts-neo', 'dtsneo', 'dts.neo']):
		type += ' DTS-NEO /'
	if '.thx.' in url:
		type += ' THX /'
	if any(value in url for value in ['.thx-ex', 'thxex']):
		type += ' THX-EX /'
	if any(value in url for value in AUDIO_8CH):
		type += ' 8CH /'
	if any(value in url for value in AUDIO_7CH):
		type += ' 7CH /'
	if any(value in url for value in AUDIO_6CH):
		type += ' 6CH /'
	if 'xvid' in url:
		type += ' XVID /'
	if 'divx' in url:
		type += ' DIVX /'
	if any(value in url for value in CODEC_MPEG):
		type += ' MPEG /'
	if '.avi' in url:
		type += ' AVI /'
	if 'ac3' in url:
		type += ' AC3 /'
	if any(value in url for value in CODEC_H264):
		type += ' X264 /'
	if any(value in url for value in CODEC_H265):
		type += ' X265 /'
	if any(value in url for value in CODEC_MKV):
		type += ' MKV /'
	if any(value in url for value in HDCAM):
		type += ' HDCAM /'
	if any(value in url for value in MULTI_LANG):
		type += ' MULTI-LANG /'
	if any(value in url for value in ADDS):
		type += ' ADDS /'
	if any(value in url for value in SUBS):
		if type != '':
			type += ' WITH SUBS'
		else:
			type = 'SUBS'
	type = type.rstrip('/')
	return type


def ck_CamSd():
	from resources.lib.modules import control
	try:
		return True if control.setting('remove.CamSd.sources') == 'true' else False
	except:
		return False