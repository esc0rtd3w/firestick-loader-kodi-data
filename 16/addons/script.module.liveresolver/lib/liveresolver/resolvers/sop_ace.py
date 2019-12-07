# -*- coding: utf-8 -*-
import urllib

def resolve(url,name):
	if 'sop://'in url:
		url = urllib.quote(url)
		url='plugin://program.plexus/?mode=2&url=%s&name=%s'%(url,name.replace(' ','+'))
	elif 'acestream://' in url or '.acelive' in url:
		url = urllib.quote(url)
		url='plugin://program.plexus/?mode=1&url=%s&name=%s'%(url,name.replace(' ','+'))
	return url

