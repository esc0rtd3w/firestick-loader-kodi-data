import re,process,urllib,search,base64

def Todays_Football_Menu():
	process.Menu('Mainstream Channels','',1751,'','','','')
	process.Menu('[COLORred]BETA [/COLOR]LiveOnSat Channels - Some searchs may take a sec - if empty menu means no results','',1753,'','','','')
	process.Menu('Pyramid - Today\'s Matches','http://tombraiderbuilds.co.uk/addon/liveevents/liveevents.txt',1101,'','','','')
	process.Menu('Maverick - Today\'s Matches','http://164.132.106.213/data/sportslinks/prem.xml',1101,'','','','')
	process.Menu('Lily Sports - Today\'s Matches','http://kodeeresurrection.com/LILYSPORTStxts/LiveEvents.txt',1101,'','','','')

def Todays_Football():
	HTML = process.OPEN_URL('http://www.live-footballontv.com/')
	block = re.compile('<div id="listings"><div class="container" align="center"><div class="row-fluid"><div class="span12 matchdate">(.+?)<div class="span12 matchdate">',re.DOTALL).findall(HTML)
	items = re.compile('span4 matchfixture">(.+?)</div>.+?span4 competition">(.+?)</div>.+?span1 kickofftime">(.+?)</div>.+?span3 channels">(.+?)</div>').findall(str(block))
	for name,comp,time,channels in items:
		name2 = (name).replace('&nbsp;','-').replace('---',' - ').replace('&#039;','\'').replace('&#39;','\'').replace('&amp;','&').replace('&quot;','"')
		comp2 = (comp).replace('&nbsp;','-').replace('---',' - ').replace('&#039;','\'').replace('&#39;','\'').replace('&amp;','&').replace('&quot;','"')
		channels2 = (channels).replace('&nbsp;','-').replace('-','').replace('&#039;','\'').replace('&#39;','\'').replace('&amp;','&').replace('&quot;','"')
		process.Menu(time+' : '+name2+' - '+channels2,channels2,1752,'','',comp2,'')
		
def Live_On_Sat():
    HTML = process.OPEN_URL('http://liveonsat.com/daily.php')
    game = re.compile('comp_head>(.*?)</span>.*?<div class = fLeft width = ".*?"><img src="(.*?)">.*?</div>.*?ST:(.*?)</div>(.+?)<!-- around all of channel types ENDS 2-->',re.DOTALL).findall(HTML)
    for comp,img,time,chan in game:
        channel = re.compile(",CAPTION, '(.+?)&nbsp").findall(chan)
        channel_final = (str(channel)).replace('[$]','').replace('\\xc3','n').replace('\'','').replace('[','').replace(']','').replace('\\xe2','').replace('\\x80','').replace('\\x99','').replace('\\xb1a','i')
        name = str(comp) + ' - ' + str(time)
        image = 'http://liveonsat.com' + str(img)
        process.Menu(name,(channel_final).replace(',','/').replace('|',''),1752,image,'',channel_final,'')
			
def Search_Channels_Mainstream(url):
	List = []
	splitter = url + '/'
	match = re.compile('(.+?)/').findall(str(splitter))
	for url in match:
		if 'HD' in url:
			url = (url).replace('HD','')
		elif '(' in url:
			second_split = re.compile('(.+?)\(').findall(str(url))
			for item in second_split:
				url = item 
				if url not in List:
					Search_name = (url).lower()
					search.Live_TV(Search_name)
					List.append(url)
		else:
			if url not in List:
				Search_name = (url).lower()
				search.Live_TV(Search_name)
				List.append(url)
				