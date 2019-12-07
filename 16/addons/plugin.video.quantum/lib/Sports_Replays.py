import re, urllib, process

base_icons = 'http://herovision.x10host.com/freeview/'
ORIGIN_FANART = base_icons + 'origin.jpg'
ORIGIN_ICON = base_icons + 'origin.png'
RENEGADES_ICON = base_icons + 'renegades.png'

def Sports_Repeats():
    process.Menu('Football Replays','',400,ORIGIN_ICON,ORIGIN_FANART,'','')
    process.Menu('Motor Replays','http://www.gpreplay.com/index.htm',2101,ORIGIN_ICON,ORIGIN_FANART,'','')
    process.Menu('F1 Replays','http://f1fullraces.com/',2105,ORIGIN_ICON,ORIGIN_FANART,'','')
    process.Menu('Renegades Darts','',2150,RENEGADES_ICON,ORIGIN_FANART,'','')
	
def F1_Replays(url):
	process.Menu('Items before 2015 are nosvideo links, ','','','','','','')
	process.Menu('Url Resolver does not seem to be able to resolve these atm','','','','','','')
	process.Menu('Will leave in for now incase a fix occurs','','','','','','')
	HTML = process.OPEN_URL(url)
	match = re.compile('<li id=".+?" class=".+?category.+?"><a href="(.+?)">(.+?)</a></li>').findall(HTML)
	for url,name in match:
		process.Menu(name,url,2106,'','','','')
		
def F1_page(url):
	HTML = process.OPEN_URL(url)
	match = re.compile('<div class="content-list-thumb">.+?<a href="(.+?)" title="(.+?)">.+?src="(.+?)"',re.DOTALL).findall(HTML)
	for url,name,image in match:
		name = name.replace('&#8211;',':').replace('watch online free','')
		process.Menu(name,url,2107,image,'','','')
	next = re.compile('<a class="next page-numbers" href="(.+?)">.+?</a>').findall(HTML)
	for url in next:
		process.Menu('Next Page',url,2106,'','','','')
		
def F1_items(url,iconimage):
	List = ['pre','qualify','race','post','Pre','Qualify','Race','Post']
	HTML = process.OPEN_URL(url)
	for item in List:
		name = item.replace('qualify','Qualifying').replace('race','Race').replace('post','Post-Race').replace('Pre','Pre-Race').replace('Qualify','Qualifying').replace('pre','Pre-Race')
		regex = re.compile(str(item)+'.+?"(.+?)"',re.DOTALL).findall(HTML)
		for url in regex:
			Play_url(name,url,iconimage)
		else:
			try_single = re.compile('<iframe src="(.+?)"').findall(HTML)
			for url in try_single:
				Play_url('Play',url,iconimage)
			try_single_2 = re.compile('<IFRAME SRC="(.+?)"').findall(HTML)
			for url in try_single_2:
				Play_url('Play',url,iconimage)
			
def Play_url(name,url,iconimage):
	url_List = []
	if 'pcloud' in url:
		pass
	elif 'nosvideo' in url:
		if url not in url_List:
			process.PLAY('[COLORred]nosvideo[/COLOR] - '+name,url,906,iconimage,'','','')
			url_List.append(url)
	elif 'drive' in url:
		if url not in url_List:
			process.Play('[COLORred]gdrive[/COLOR] - '+name,url,906,iconimage,'','','')
			url_List.append(url)
	else:
		pass
		
def Motor_Replays(url):
	HTML = process.OPEN_URL(url)
	block = re.compile('<b>videos<br>(.+?)<p>',re.DOTALL).findall(HTML)
	match = re.compile('<a href="(.+?)">(.+?)</a>').findall(str(block))
	for url, name in match:
		if '2013' in name:
			pass
		else:
			url = 'http://www.gpreplay.com/'+url
			process.Menu(name,url,2102,'','','','')

def motor_name(url):
	HTML = process.OPEN_URL(url)
	match = re.compile('<font color="#FFFFFF">(.+?)</font>(.+?)<a name=',re.DOTALL).findall(HTML)
	for name,block in match:
		name = name.replace('<b>','').replace('</b>','')
		process.Menu(name.replace('\n',' ').replace('  ',''),'',2103,'','','',block)



def motor_race(block):
	match = re.compile('(.+?)</b>(.+?)<b>',re.DOTALL).findall(str(block))
	for name,block in match:
		name = (name).replace('<b>','').replace('&iuml;','i').replace('<br>','').replace('&quot;','"').replace('<p>','').replace('\n','').replace('  ','').replace('</td>','').replace('</tr>','').replace('</table>','')
		process.Menu(name,'',2104,'','','',block)
		
def motor_single(name,block):
	ALPHANUM = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0','1','2','3','4','5','6','7','8','9','#']
	fallback = name
	List = []
	match = re.compile('(.+?)<a href="(.+?)".+?\n',re.DOTALL).findall(str(block))
	for name, url in match:
		name = name.replace('  ','').replace('	','').replace('\n','').replace('%0D','')
		if name=='':
			if len(List)>=1:
				name = List[-1]
			else:
				name = fallback
		name = name.replace('<b>','').replace('  ','').replace('<br>','')
		if 'utube' in url:
			url = url.replace('https://www.youtube.com/watch?v=','').replace('http://www.youtube.com/watch?v=','')
			fin_url = 'plugin://plugin.video.youtube/play/?video_id='+url
			process.Play('Play - '+name,fin_url,906,'','','','')
			List.append(name)
		if 'itv' in url:
			process.Menu('Unfortunately i cannot grab this stream, it is available at itv.com for uk viewers','',906,'','','','')
