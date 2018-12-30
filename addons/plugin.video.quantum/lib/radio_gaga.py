import sys, base64
import urllib,re,os,xbmcplugin
import process

Decode = base64.decodestring
addon_handle = int(sys.argv[1])
List = []


def Radio_Country():  
    html=process.OPEN_URL(Decode('aHR0cDovL3d3dy5saXN0ZW5saXZlLmV1Lw=='))
    match = re.compile('<tr>.+?<a href="(.+?)">(.+?)</a>',re.DOTALL).findall(html)
    for url,name in match:
        if name not in List:
    	    process.Menu((name).replace('email me','').replace('External services',''),Decode('aHR0cDovL3d3dy5saXN0ZW5saXZlLmV1LyVz')%url,501,'','','','')
            List.append(name)
	
def Radio(url):
    process.Menu('Please allow loading to finish before pressing back','','','','','','')
    process.Menu('To save potentially crashing kodi','','','','','','')
    html=process.OPEN_URL(url)
    match = re.compile('<tr>.+?<td><a href=".+?"><b>(.+?)</b>.+?<td><a href="(.+?)">',re.DOTALL).findall(html)
    for name,url in match:
		process.Play(name,url,502,'','','','')

			
    xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_TITLE);
