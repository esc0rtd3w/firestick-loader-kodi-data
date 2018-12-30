# -*- coding: utf-8 -*-
import ctypes


domain="https://listen2.musicmp3.ru"
timeout=60*60*24

def boo(d):
	a = 1234554321
	b = 305419896
	c = 7
	e = 0

	while True:
		if not e < len(d): break
		f = ord(d[e]) & 255
		a = a ^ ((a & 63) + c) * f + (ctypes.c_int(a << 8).value)
		b = b + (ctypes.c_int(b << 8).value ^ a)
		c = c + f
		e+=1
	a =  ctypes.c_int(a&-2147483649).value
	b =  ctypes.c_int(b&-2147483649).value
	d = hex(a)[2:]
	c = hex(b)[2:]
	return ("0000" + hex(a)[2:])[len(d)-4:] + ("0000" + hex(b)[2:])[(len(c)- 4):]


def run(hash,ump,referer=""):
	session=None
	for cookie in ump.cj:
		if "musicmp3.ru" in cookie.domain and cookie.name.lower()=="sessionid":
			session=cookie.value
			break
#	if session is None:
#		for cookie in ump.cj:
#			if cookie.name=="c[musicmp3.ru][/][SessionId]":
#				session=cookie.value
	return {"url":{"url":"%s/%s/%s"%(domain,boo(referer[5:]+session[8:]),hash),"referer":"https://musicmp3.ru/"}}
