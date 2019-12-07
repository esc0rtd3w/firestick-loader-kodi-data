from socket import socket
from defs import kodi_guixml
import dom

from third.socksipy import socks


def get_set(genset,n):
	nd=genset.getElementsByTagName(n)[0]
	if nd.lastChild is None:
		return nd.lastChild
	else:
		return nd.lastChild.data

def getsocket():
	gen_set=None
	try:
		gen_set=dom.read(kodi_guixml)
		if not get_set(gen_set,"usehttpproxy").lower() == "false":
			s=[3,1,1,2,2][int(get_set(gen_set,"httpproxytype"))]
			socks.setdefaultproxy(s, get_set(gen_set,"httpproxyserver"), int(get_set(gen_set,"httpproxyport")),int(get_set(gen_set,"httpproxytype"))==4,get_set(gen_set,"httpproxyusername"),get_set(gen_set,"httpproxypassword"))
			ret= socks.socksocket
		else:
			ret= socket
	except:
		ret= socket
	if gen_set:
		gen_set.unlink()
	return ret