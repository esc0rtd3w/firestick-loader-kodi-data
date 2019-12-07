# -*- coding: utf-8 -*-

import process, re, requests, threading, xbmc, xbmcgui, os, xbmcaddon

Stream_file = xbmc.translatePath('special://home/userdata/addon_data/plugin.video.quantum/streams.txt')
Addon_data = xbmc.translatePath('special://home/userdata/addon_data/plugin.video.quantum/')

def Live_Menu():
    process.Menu('By Country','',20,'','','','')
    process.Menu('M3u8 Lists','',23,'','','','')


def Live_Main():
	HTML = requests.get('http://www.shadow-net.org').text
	match = re.compile('<li class=""><a href="(.+?)">(.+?)</a>').findall(HTML)
	for url, name in match:
		name = name.replace('&amp;','&')
		if 'p2p' in name.lower():
			pass
		else:
			process.Menu(name,url,21,'','','','')
		
def Get_Channel(url):
	List = []
	HTML = requests.get(url).text
	block = re.compile('<div class="Block CategoryContent Moveable Panel"(.+?)<br class="Clear" />',re.DOTALL).findall(HTML)
	for item in block:
		match = re.compile('<div class="ProductImage">.+?<a href="(.+?)".+?img src="(.+?)" alt="(.+?)" />',re.DOTALL).findall(str(item.encode('utf-8')))
		for url,image,name in match:
			process.PLAY(name,url,22,image,'','','')
	next = re.compile('<div class="FloatRight"><a href="(.+?)">.+?</a>').findall(HTML)
	for url in next:
		if 'skippy' not in List:
			process.Menu('Next Page',url,21,'','','','')
			List.append('skippy')
			
def Get_Playlink(name,url):
	playlink = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url=' + url
	HTML = requests.get(url).text
	m3u8 = re.compile('<source src="(.+?)"').findall(HTML)
	for item in m3u8:
		playlink = item
	process.Big_Resolve(name,playlink)
	
def Ultra():
	headers = {"User-Agent": "Mozilla/5.0"}
	process.Menu('[COLORwhite]Search All Lists[/COLOR]','',25,'','','','')
	process.Menu('________________________________________________________','',25,'','','','')
	process.Menu('[COLORwhite]Check for response off streams[/COLOR]','',26,'','','','')
	process.Menu('[COLORred]AVERAGE RUN TIME FOR ABOVE IS 30 MINUTES!!!![/COLOR]','',23,'','','','')
	process.Menu('[COLORred]This will check every single stream for a response[/COLOR]','',23,'','','','')
	process.Menu('[COLORred]It will take a while but should only need doing every couple of days[/COLOR]','',23,'','','','')
	process.Menu('[COLORred]It\'s not a guarantee they will work and be perfect just that they exist[/COLOR]','',23,'','','','')
	process.Menu('________________________________________________________','',25,'','','','')
	process.Menu('[COLORwhite]Search pre-checked list of streams - run above first!!![/COLOR]','',27,'','','','')
	process.Menu('________________________________________________________','',25,'','','','')
	process.Menu('[COLORred]Streams are not checked manually so may be hit or miss!!!![/COLOR]','',23,'','','','')
	process.Menu('[COLORred]But enjoy what does work, don\'t enjoy what doesn\'t ;-)[/COLOR]','',23,'','','','')
	process.Menu('________________________________________________________','',25,'','','','')
	HTML = requests.get('http://www.iptvultra.com/',headers=headers).text
	match = re.compile('<span class="link"><a href="(.+?)">(.+?)</a>').findall(HTML)
	for url, name in match:
		process.Menu(name,url,24,'','','','')
		
def Get_Ultra_Channel(url):
	headers = {"User-Agent": "Mozilla/5.0"}
	HTML = requests.get(url,headers=headers).text
	match = re.compile('".+?[@](.+?)[@].+?[@].+?[@](.+?)"').findall(HTML)
	for name,url in match:
		name = name.replace('[','').replace(']','')
		if name[0] == ' ':
			name = name[1:]
		if name[-1] == ' ':
			name = name[:-1]
		url = 'plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&amp;url='+url.replace('[','').replace(']','')+';name=quantum'
		process.PLAY(name,url,906,'','','','')


		
def Search_Ultra():
	Dialog = xbmcgui.Dialog()
	Search_title = Dialog.input('Search', type=xbmcgui.INPUT_ALPHANUM)
	Search_name = Search_title.lower()
	search_next(Search_name)
	
def search_next(name):
#	try:
		f4murl = 'plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&amp;url='
		sports = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url='
		addon_id = 'plugin.video.quantum'
		ADDON = xbmcaddon.Addon(id=addon_id)
		freeview = [['4Music | Direct','http://llnw.live.btv.simplestream.com/coder9/coder.channels.channel6/hls/4/playlist.m3u8',1201],
			['4Music | TVPlayer','128',1202],
			['5* | FilmOn','https://www.filmon.com/tv/5-star',1201],
			['5USA | FilmOn','https://www.filmon.com/tv/5usa',1201],
			['Al Jazeera | TVPlayer','146',1202],
			['Al Jazeera | FilmOn','https://www.filmon.com/tv/al-jazeera',1201],
			['BBC Alba | TVPlayer','236',1202],
			['BBC Alba | BBC iPlayer','http://vs-hls-uk-live.edgesuite.net/pool_1/live/bbc_alba/bbc_alba.isml/bbc_alba-pa3%3d96000-video%3d1604032.norewind.m3u8',1201],
			['BBC Four HD | BBC iPlayer','http://vs-hls-uk-live.akamaized.net/pool_33/live/bbc_four_hd/bbc_four_hd.isml/bbc_four_hd-pa4%3d128000-video%3d5070016.m3u8',1201],
			['BBC Four | TVPlayer','110',1202],
			['BBC Four | FilmOn','https://www.filmon.com/tv/cbeebiesbbc-four',1201],
			['BBC News HD | BBC iPlayer','http://vs-hls-uk-live.edgesuite.net/pool_34/live/bbc_news_channel_hd/bbc_news_channel_hd.isml/bbc_news_channel_hd-pa4%3d128000-video%3d5070016.m3u8',1201],
			['BBC News | TVPlayer','111',1202],
			['BBC News | FilmOn','https://www.filmon.com/tv/bbc-news',1201],
			['BBC 1 HD | BBC iPlayer','http://vs-hls-uk-live.akamaized.net/pool_30/live/bbc_one_hd/bbc_one_hd.isml/bbc_one_hd-pa4%3d128000-video%3d5070016.m3u8',1201],
			['BBC 1 | TVPlayer','89',1202],
			['BBC 1 | FilmOn','https://www.filmon.com/tv/bbc-one',1201],
			['BBC 1 Northern Ireland | BBC iPlayer','http://vs-hls-uk-live.edgesuite.net/pool_4/live/bbc_one_northern_ireland_hd/bbc_one_northern_ireland_hd.isml/bbc_one_northern_ireland_hd-pa4%3d128000-video%3d5070016.m3u8',1201],
			['BBC 1 Northern Ireland | FilmOn','https://www.filmon.com/tv/bbc-1-north-ireland',1201],
			['BBC 1 Scotland | BBC iPlayer','http://vs-hls-uk-live.edgesuite.net/pool_5/live/bbc_one_scotland_hd/bbc_one_scotland_hd.isml/bbc_one_scotland_hd-pa4%3d128000-video%3d5070016.m3u8',1201],
			['BBC 1 Scotland | FilmOn','https://www.filmon.com/tv/bbc-1-scotland',1201],
			['BBC 1 Wales | BBC iPlayer','http://vs-hls-uk-live.edgesuite.net/pool_3/live/bbc_one_wales_hd/bbc_one_wales_hd.isml/bbc_one_wales_hd-pa4%3d128000-video%3d5070016.m3u8',1201],
			['BBC 1 Wales | FilmOn','https://www.filmon.com/tv/bbc-1-wales',1201],
			['BBC 2 Northern Ireland | BBC iPlayer','http://vs-hls-uk-live.edgesuite.net/pool_5/live/bbc_two_northern_ireland_digital/bbc_two_northern_ireland_digital.isml/bbc_two_northern_ireland_digital-pa3%3d96000-video%3d1604032.norewind.m3u8',1201],
			['BBC 2 Scotland | BBC iPlayer','http://vs-hls-uk-live.edgesuite.net/pool_5/live/bbc_two_scotland/bbc_two_scotland.isml/bbc_two_scotland-pa3%3d96000-video%3d1604032.norewind.m3u8',1201],
			['BBC 2 Wales | BBC iPlayer','http://vs-hls-uk-live.edgesuite.net/pool_5/live/bbc_two_wales_digital/bbc_two_wales_digital.isml/bbc_two_wales_digital-pa3%3d96000-video%3d1604032.norewind.m3u8',1201],
			['BBC Parliament | BBC iPlayer','http://vs-hls-uk-live.edgesuite.net/pool_1/live/bbc_parliament/bbc_parliament.isml/bbc_parliament-pa3%3d96000-video%3d1604032.norewind.m3u8',1201],
			['BBC Parliament | TVPlayer','345',1202],
			['BBC Parliament | FilmOn','https://www.filmon.com/tv/bbc-parliament',1201],
			['BBC 2 HD | BBC iPlayer','http://vs-hls-uk-live.edgesuite.net/pool_31/live/bbc_two_hd/bbc_two_hd.isml/bbc_two_hd-pa4%3d128000-video%3d5070016.m3u8',1201],
			['BBC 2 | TVPlayer','90',1202],
			['BBC 2 | FilmOn','https://www.filmon.com/tv/bbc-two',1201],
			['Bloomberg | TVPlayer','514',1202],
			['Bloomberg | FilmOn','https://www.filmon.com/tv/bloomberg',1201],
			['The Box | Direct','http://llnw.live.btv.simplestream.com/coder9/coder.channels.channel12/hls/4/playlist.m3u8',1201],
			['The Box | TVPlayer','129',1202],
			['Box Hits | Direct','http://llnw.live.btv.simplestream.com/coder9/coder.channels.channel2/hls/4/playlist.m3u8',1201],
			['Box Hits | TVPlayer','130',1202],
			['Box Upfront | Direct','http://llnw.live.btv.simplestream.com/coder9/coder.channels.channel8/hls/4/playlist.m3u8',1201],
			['Box Upfront | TVPlayer','158',1202],
			['Capital TV | Direct','http://ooyalahd2-f.akamaihd.net/i/globalradio01_delivery@156521/index_656_av-p.m3u8?sd=10&rebase=on',1201],
			['Capital TV | TVPlayer','157',1202],
			['CBBC HD | BBC iPlayer','http://vs-hls-uk-live.edgesuite.net/pool_1/live/cbbc_hd/cbbc_hd.isml/cbbc_hd-pa4%3d128000-video%3d5070016.m3u8',1201],
			['CBBC | TVPlayer','113',1202],
			['CBBC | FilmOn','https://www.filmon.com/tv/cbbc',1201],
			['CBeebies HD | BBC iPlayer','http://vs-hls-uk-live.edgesuite.net/pool_2/live/cbeebies_hd/cbeebies_hd.isml/cbeebies_hd-pa4%3d128000-video%3d5070016.m3u8',1201],
			['CBeebies | TVPlayer','114',1202],
			['CBeebies | FilmOn','https://www.filmon.com/tv/cbeebies',1201],
			['CBS Action | FilmOn','https://www.filmon.com/tv/cbs-action',1201],
			['CBS Drama | FilmOn','https://www.filmon.com/tv/cbs-drama',1201],
			['CBS Reality | FilmOn','https://www.filmon.com/tv/cbs-reality',1201],
			['CBS Reality+1 | FilmOn','https://www.filmon.com/tv/cbs-reality1',1201],
			['Channel 4 | TVPlayer','92',1202],
			['Channel 4 | FilmOn','https://www.filmon.com/tv/channel-4',1201],
			['Channel 5 | TVPlayer','93',1202],
			['Channel 5 | FilmOn','https://www.filmon.com/tv/channel-5',1201],
			['Channel AKA | Direct','http://rrr.sz.xlcdn.com/?account=AATW&file=akanew&type=live&service=wowza&protocol=http&output=playlist.m3u8',1201],
			['Channel AKA | TVPlayer','227',1202],
			['Chilled | TVPlayer','226',1202],
			['CITV | ITV Hub','http://citvliveios-i.akamaihd.net/hls/live/207267/itvlive/CITVMN/master_Main1800.m3u8',1201],
			['Clubbing TV | FilmOn','https://www.filmon.com/tv/clubbing-tv',1201],
			['Clubland | TVPlayer','225',1202],
			['CNN International | TVPlayer','286',1202],
			['Community Channel | TVPlayer','259',1202],
			['The Craft Channel | TVPlayer','554',1202],
			['Dave | TVPlayer','300',1202],
			['Dave ja vu | TVPlayer','317',1202],
			['Drama | TVPlayer','346',1202],
			['E4 | FilmOn','https://www.filmon.com/tv/e4',1201],
			['Film4 | FilmOn','https://www.filmon.com/tv/film-4',1201],
			['Food Network | TVPlayer','125',1202],
			['Food Network | FilmOn','http://www.filmon.com/tv/food-network',1201],
			['Food Network+1 | TVPlayer','254',1202],
			['Food Network+1 | FilmOn','http://www.filmon.com/tv/food-network-plus-1',1201],
			['Forces TV | TVPlayer','555',1202],
			['Heart TV | Direct','http://ooyalahd2-f.akamaihd.net/i/globalradio02_delivery@156522/master.m3u8',1201],
			['Heart TV | TVPlayer','153',1202],
			['Home | TVPlayer','512',1202],
			['Horror Channel | FilmOn','https://www.filmon.com/tv/horror-channel',1201],
			['ITV1 | ITV Hub','http://itv1liveios-i.akamaihd.net/hls/live/203437/itvlive/ITV1MN/master_Main1800.m3u8',1201],
			['ITV1 | TVPlayer','204',1202],
			['ITV1 | FilmOn','http://www.filmon.com/tv/itv1',1201],
			['ITV1+1 | FilmOn','https://www.filmon.com/tv/itv-plus-1',1201],
			['ITV2 | ITV Hub','http://itv2liveios-i.akamaihd.net/hls/live/203495/itvlive/ITV2MN/master_Main1800.m3u8',1201],
			['ITV2 | FilmOn','http://www.filmon.com/tv/itv2',1201],
			['ITV2+1 | FilmOn','https://www.filmon.com/tv/itv2-plus-1',1201],
			['ITV3 | ITV Hub','http://itv3liveios-i.akamaihd.net/hls/live/207262/itvlive/ITV3MN/master_Main1800.m3u8',1201],
			['ITV3 | FilmOn','http://www.filmon.com/tv/itv3',1201],
			['ITV3+1 | FilmOn','https://www.filmon.com/tv/itv3-plus-1',1201],
			['ITV4 | ITV Hub','http://itv4liveios-i.akamaihd.net/hls/live/207266/itvlive/ITV4MN/master_Main1800.m3u8',1201],
			['ITV4 | FilmOn','http://www.filmon.com/tv/itv4',1201],
			['ITV4+1 | FilmOn','https://www.filmon.com/tv/itv4-plus-1',1201],
			['ITVBe | ITV Hub','http://itvbeliveios-i.akamaihd.net/hls/live/219078/itvlive/ITVBE/master_Main1800.m3u8',1201],
			['ITVBe | FilmOn','http://www.filmon.com/tv/itvbe',1201],
			['The Jewellery Channel | Direct','https://d2hee8qk5g0egz.cloudfront.net/live/tjc_sdi1/bitrate1.isml/bitrate1-audio_track=64000-video=1800000.m3u8',1201],
			['The Jewellery Channel | TVPlayer','545',1202],
			['Keep It Country | TVPlayer','569',1202],
			['Kerrang! | Direct','http://llnw.live.btv.simplestream.com/coder11/coder.channels.channel4/hls/4/playlist.m3u8',1201],
			['Kerrang! | TVPlayer','133',1202],
			['Kiss | Direct','http://llnw.live.btv.simplestream.com/coder9/coder.channels.channel14/hls/4/playlist.m3u8',1201],
			['Kiss | TVPlayer','131',1202],
			['Kix! | FilmOn','https://www.filmon.com/tv/kix',1201],
			['London Live | Direct','http://bcoveliveios-i.akamaihd.net/hls/live/217434/3083279840001/master_900.m3u8',1201],
			['Magic | Direct','http://llnw.live.btv.simplestream.com/coder11/coder.channels.channel2/hls/4/playlist.m3u8',1201],
			['Magic | TVPlayer','132',1202],
			['More4 | FilmOn','https://www.filmon.com/tv/more4',1201],
			['NOW Music | Direct','http://rrr.sz.xlcdn.com/?account=AATW&file=nowmusic&type=live&service=wowza&protocol=http&output=playlist.m3u8',1201],
			['NOW Music | TVPlayer','228',1202],
			['POP | FilmOn','https://www.filmon.com/tv/pop',1201],
			['Pick | FilmOn','https://www.filmon.com/tv/pick-tv',1201],
			['QUEST | TVPlayer','327',1202],
			['QUEST | FilmOn','http://www.filmon.tv/tv/quest',1201],
			['QUEST+1 | TVPlayer','336',1202],
			['QVC Beauty | TVPlayer','250',1202],
			['QVC Extra | TVPlayer','248',1202],
			['QVC Plus | TVPlayer','344',1202],
			['QVC Style | TVPlayer','249',1202],
			['QVC | TVPlayer','247',1202],
			['Really | TVPlayer','306',1202],
			['Really | FilmOn','http://www.filmon.tv/tv/really',1201],
			['S4C | BBC iPlayer','http://vs-hls-uk-live.edgesuite.net/pool_9/live/s4cpbs/s4cpbs.isml/s4cpbs-pa3%3d96000-video%3d1604032.norewind.m3u8',1201],
			['S4C | TVPlayer','251',1202],
			['Sky News | YouTube','https://www.youtube.com/watch?v=y60wDzZt8yg',1201],
			['Tiny Pop | FilmOn','https://www.filmon.com/tv/tiny-pop',1201],
			['Travel Channel | TVPlayer','126',1202],
			['Travel Channel+1 | TVPlayer','255',1202],
			['Travel Channel+1 | FilmOn','http://www.filmon.tv/tv/travel-channel1',1201],
			['Yesterday | TVPlayer','308',1202],
			['Yesterday | FilmOn','http://www.filmon.tv/tv/yesterday',1201],
			['Yesterday+1 | TVPlayer','318',1202],
			['truTV | Direct','http://llnw.live.btv.simplestream.com/coder5/coder.channels.channel2/hls/4/playlist.m3u8',1201],
			['truTV | TVPlayer','295',1202],
			['truTV | FilmOn','http://www.filmon.tv/tv/tru-tv',1201],
			['Blaze | Direct','http://live.blaze.simplestreamcdn.com/live/blaze/bitrate1.isml/bitrate1-audio_track=64000-video=3500000.m3u8',1201]]	

		liveonline = [['Sony SIX','http://www.liveonlinetv247.info/watch.php?title=Sony SIX&channel=sonysix'],
			 ['TEN 1','http://www.liveonlinetv247.info/watch.php?title=TEN 1&channel=ten1'],
			 ['Sky Sports 1','http://www.liveonlinetv247.info/watch.php?title=Sky Sports 1&channel=skysports1'],
			 ['Sky Sports 2','http://www.liveonlinetv247.info/watch.php?title=Sky Sports 2&channel=skysports2'],
			 ['Sky Sports 3','http://www.liveonlinetv247.info/watch.php?title=Sky Sports 3&channel=skysports3'],
			 ['Sky Sports 4','http://www.liveonlinetv247.info/watch.php?title=Sky Sports 4&channel=skysports4'],
			 ['Sky Sports 5','http://www.liveonlinetv247.info/watch.php?title=Sky Sports 5&channel=skysports5'],
			 ['Sky Sports News','http://www.liveonlinetv247.info/watch.php?title=Sky Sports News&channel=skysportsnews'],
			 ['Sky Sports F1','http://www.liveonlinetv247.info/watch.php?title=Sky Sports F1&channel=skysportsf1'],
			 ['Sky Sports Cricket','http://www.liveonlinetv247.info/watch.php?title=Sky Sports Cricket&channel=skysportscricket'],
			 ['Sky Sports Box Office','http://www.liveonlinetv247.info/watch.php?title=Sky Sports Box Office&channel=skysportsboxoffice'],
			 ['BT Sport 1','http://www.liveonlinetv247.info/watch.php?title=BT Sport 1&channel=btsport1'],
			 ['BT Sport 2','http://www.liveonlinetv247.info/watch.php?title=BT Sport 2&channel=btsport2'],
			 ['BT Sport Europe','http://www.liveonlinetv247.info/watch.php?title=BT Sport Europe&channel=btsporteurope'],
			 ['BT Sport ESPN','http://www.liveonlinetv247.info/watch.php?title=BT Sport ESPN&channel=btsportespn'],
			 ['ESPN','http://www.liveonlinetv247.info/watch.php?title=ESPN&channel=espn'],
			 ['Canal+ Fútbol','http://www.liveonlinetv247.info/watch.php?title=Canal%2B Fútbol&channel=canal%2Bfutbol'],
			 ['Canal+ Liga','http://www.liveonlinetv247.info/watch.php?title=Canal%2B Liga&channel=canal%2Bliga'],
			 ['Canal+ Sport','http://www.liveonlinetv247.info/watch.php?title=Canal%2B Sport&channel=canal%2Bsport'],
			 ['Eurosport','http://www.liveonlinetv247.info/watch.php?title=Eurosport&channel=eurosport'],
			 ['Eurosport 2','http://www.liveonlinetv247.info/watch.php?title=Eurosport 2&channel=eurosport2'],
			 ['WWE Network','http://www.liveonlinetv247.info/watch.php?title=WWE Network&channel=wwenetwork'],
			 ['Premier Sports','http://www.liveonlinetv247.info/watch.php?title=Premier Sports&channel=premiersports'],
			 ['BoxNation','http://www.liveonlinetv247.info/watch.php?title=BoxNation&channel=boxnation'],
			 ['Willow TV','http://www.liveonlinetv247.info/watch.php?title=Willow TV&channel=willowtv'],
			 ['Fox Sports 1','http://www.liveonlinetv247.info/watch.php?title=Fox Sports 1&channel=foxsports1'],
			 ['Fox Sports 2','http://www.liveonlinetv247.info/watch.php?title=Fox Sports 2&channel=foxsports2'],
			 ['NBA TV','http://www.liveonlinetv247.info/watch.php?title=NBA TV&channel=nbatv'],
			 ['beIN Sports News','http://www.liveonlinetv247.info/watch.php?title=beIN Sports News&channel=beinsportsnews'],
			 ['beIN Sports 1','http://www.liveonlinetv247.info/watch.php?title=beIN Sports 1&channel=beinsports1'],
			 ['beIN Sports 2','http://www.liveonlinetv247.info/watch.php?title=beIN Sports 2&channel=beinsports2'],
			 ['beIN Sports 3','http://www.liveonlinetv247.info/watch.php?title=beIN Sports 3&channel=beinsports3'],
			 ['beIN Sports 4','http://www.liveonlinetv247.info/watch.php?title=beIN Sports 4&channel=beinsports4'],
			 ['beIN Sports 5','http://www.liveonlinetv247.info/watch.php?title=beIN Sports 5&channel=beinsports5'],
			 ['beIN Sports 6','http://www.liveonlinetv247.info/watch.php?title=beIN Sports 6&channel=beinsports6'],
			 ['beIN Sports 7','http://www.liveonlinetv247.info/watch.php?title=beIN Sports 7&channel=beinsports7'],
			 ['beIN Sports 8','http://www.liveonlinetv247.info/watch.php?title=beIN Sports 8&channel=beinsports8'],
			 ['beIN Sports 9','http://www.liveonlinetv247.info/watch.php?title=beIN Sports 9&channel=beinsports9'],
			 ['beIN Sports 10','http://www.liveonlinetv247.info/watch.php?title=beIN Sports 10&channel=beinsports10'],
			 ['beIN Sports 11 English','http://www.liveonlinetv247.info/watch.php?title=beIN Sports 11 English&channel=beinsports11'],
			 ['beIN Sports 12 English','http://www.liveonlinetv247.info/watch.php?title=beIN Sports 12 English&channel=beinsports12'],
			 ['beIN Sports 13 English','http://www.liveonlinetv247.info/watch.php?title=beIN Sports 13 English&channel=beinsports13'],
			 ['beIN Sports 1 France','http://www.liveonlinetv247.info/watch.php?title=beIN Sports 1 France&channel=beinsports1france'],
			 ['beIN Sports 2 France','http://www.liveonlinetv247.info/watch.php?title=beIN Sports 2 France&channel=beinsports2france'],
			 ['beIN Sports 3 France','http://www.liveonlinetv247.info/watch.php?title=beIN Sports 3 France&channel=beinsports3france'],
			 ['Sky Sport 1 Italia','http://www.liveonlinetv247.info/watch.php?title=Sky Sport 1 Italia&channel=skysport1italia'],
			 ['Sky Sport 2 Italia','http://www.liveonlinetv247.info/watch.php?title=Sky Sport 2 Italia&channel=skysport2italia'],
			 ['Sky Sport 3 Italia','http://www.liveonlinetv247.info/watch.php?title=Sky Sport 3 Italia&channel=skysport3italia'],
			 ['Sky Sport 24 Italia','http://www.liveonlinetv247.info/watch.php?title=Sky Sport 24 Italia&channel=skysport24italia'],
			 ['Sky Calcio','http://www.liveonlinetv247.info/watch.php?title=Sky Calcio&channel=skycalcio'],
			 ['Sky Sport MotoGP','http://www.liveonlinetv247.info/watch.php?title=Sky Sport MotoGP&channel=skysportmotogp'],
			 ['Racing UK','http://www.liveonlinetv247.info/watch.php?title=Racing UK&channel=racinguk'],
			 ['At The Races','http://www.liveonlinetv247.info/watch.php?title=At The Races&channel=attheraces'],
			 ['LFCTV','http://www.liveonlinetv247.info/watch.php?title=LFCTV&channel=lfctv'],
			 ['MUTV','http://www.liveonlinetv247.info/watch.php?title=MUTV&channel=mutv'],
			 ['Chelsea TV','http://www.liveonlinetv247.info/watch.php?title=Chelsea TV&channel=chelseatv'],
			 ['Motors TV','http://www.liveonlinetv247.info/watch.php?title=Motors TV&channel=motorstv'],
			 ['Golf Channel','http://www.liveonlinetv247.info/watch.php?title=Golf Channel&channel=golfchannel'],
			 ['Setanta Sports','http://www.liveonlinetv247.info/watch.php?title=Setanta Sports&channel=setantasports'],
			 ['TSN','http://www.liveonlinetv247.info/watch.php?title=TSN&channel=tsn'],
			 ['TSN2','http://www.liveonlinetv247.info/watch.php?title=TSN2&channel=tsn2'],
			 ['Sport TV 1','http://www.liveonlinetv247.info/watch.php?title=Sport TV 1&channel=sporttv1'],
			 ['Sport TV 2','http://www.liveonlinetv247.info/watch.php?title=Sport TV 2&channel=sporttv2'],
			 ['Sport TV 3','http://www.liveonlinetv247.info/watch.php?title=Sport TV 3&channel=sporttv3'],
			 ['Sport TV 4','http://www.liveonlinetv247.info/watch.php?title=Sport TV 4&channel=sporttv4'],
			 ['Sport TV 5','http://www.liveonlinetv247.info/watch.php?title=Sport TV 5&channel=sporttv5'],
			 ['NFL Network','http://www.liveonlinetv247.info/watch.php?title=NFL Network&channel=nflnetwork'],
			 ['PTV Sports','http://www.liveonlinetv247.info/watch.php?title=PTV Sports&channel=ptvsports'],
			 ['NBCSN','http://www.liveonlinetv247.info/watch.php?title=NBCSN&channel=nbcsn'],
			 ['Geo Super','http://www.liveonlinetv247.info/watch.php?title=Geo Super&channel=geosuper'],
			 ['Star Sports','http://www.liveonlinetv247.info/watch.php?title=Star Sports&channel=starsports'],
			 ['Star Cricket','http://www.liveonlinetv247.info/watch.php?title=Star Cricket&channel=starcricket'],
			 ['Sportsnet World','http://www.liveonlinetv247.info/watch.php?title=Sportsnet World&channel=sportsnetworld'],
			 ['Sportsnet ONE','http://www.liveonlinetv247.info/watch.php?title=Sportsnet ONE&channel=sportsnetone'],
			 ['Sportsnet Ontario','http://www.liveonlinetv247.info/watch.php?title=Sportsnet Ontario&channel=sportsnetontario'],
			 ['WWE TV','http://www.liveonlinetv247.info/watch.php?title=WWE TV&channel=wwetv'],
			 ['BBC One','http://www.liveonlinetv247.info/bbcone.php'],
			 ['BBC Two','http://www.liveonlinetv247.info/bbctwo.php'],
			 ['ITV1','http://www.liveonlinetv247.info/itv1.php'],
			 ['ITV2','http://www.liveonlinetv247.info/itv2.php'],
			 ['AMC','http://www.liveonlinetv247.info/amc.php'],
			 ['HBO','http://www.liveonlinetv247.info/hbo.php'],
			 ['HBO HD','http://www.liveonlinetv247.info/hbohd.php'],
			 ['Sky Atlantic','http://www.liveonlinetv247.info/skyatlantic.php'],
			 ['FOX','http://www.liveonlinetv247.info/fox.php'],
			 ['FX','http://www.liveonlinetv247.info/fx.php'],
			 ['AXN','http://www.liveonlinetv247.info/axn.php'],
			 ['Star Movies','http://www.liveonlinetv247.info/starmovies.php'],
			 ['TLC','http://www.liveonlinetv247.info/tlc.php'],
			 ['Syfy','http://www.liveonlinetv247.info/syfy.php'],
			 ['TNT','http://www.liveonlinetv247.info/tnt.php'],
			 ['ABC','http://www.liveonlinetv247.info/abc.php'],
			 ['ABC Family','http://www.liveonlinetv247.info/abcfamily.php'],
			 ['CBS','http://www.liveonlinetv247.info/cbs.php'],
			 ['USA Network','http://www.liveonlinetv247.info/usanetwork.php'],
			 ['CW TV','http://www.liveonlinetv247.info/cwtv.php'],
			 ['Star World','http://www.liveonlinetv247.info/starworld.php'],
			 ['Channel 5','http://www.liveonlinetv247.info/channel5.php'],
			 ['beIN Movies 1','http://www.liveonlinetv247.info/beinmovies1.php'],
			 ['beIN Movies 2','http://www.liveonlinetv247.info/beinmovies2.php'],
			 ['beIN Movies 3','http://www.liveonlinetv247.info/beinmovies3.php'],
			 ['Sky Movies Action','http://www.liveonlinetv247.info/watch.php?title=Sky Movies Action&channel=skymoviesaction'],
			 ['Sky Movies Comedy','http://www.liveonlinetv247.info/watch.php?title=Sky Movies Comedy&channel=skymoviescomedy'],
			 ['Sky Movies Crime','http://www.liveonlinetv247.info/watch.php?title=Sky Movies Crime&channel=skymoviescrime'],
			 ['Sky Movies Disney','http://www.liveonlinetv247.info/watch.php?title=Sky Movies Disney&channel=skymoviesdisney'],
			 ['Sky Movies Family','http://www.liveonlinetv247.info/watch.php?title=Sky Movies Family&channel=skymoviesfamily'],
			 ['Sky Movies Premiere','http://www.liveonlinetv247.info/watch.php?title=Sky Movies Premiere&channel=skymoviespremiere'],
			 ['Sky Movies Select','http://www.liveonlinetv247.info/watch.php?title=Sky Movies Select&channel=skymoviesselect'],
			 ['Sky Movies Showcase','http://www.liveonlinetv247.info/watch.php?title=Sky Movies Showcase&channel=skymoviesshowcase']]

			
		mamahd = [['http://mamahd.com/sky-sports-1-live-free-stream-1.html','Sky Sports 1'],
				['http://mamahd.com/sky-sports-2-live-stream-1.html','Sky Sports 2'],
				['http://mamahd.com/sky-sports-3-live-stream-1.html','Sky Sports 3'],
				['http://mamahd.com/sky-sports-4-live-stream-1.html','Sky Sports 4'],
				['http://mamahd.com/sky-sports-5-live-stream-1.html','Sky Sports 5'],
				['http://mamahd.com/sky-sports-formula-1-live-stream-1.html','Sky Sports F1'],
				['http://mamahd.com/bt-sport-1-live-stream1-1.html','BT Sport 1'],
				['http://mamahd.com/bt-sport-2-live-stream-1.html','BT Sport 2'],
				['http://mamahd.com/bt-sport-3-live-stream-1.html','BT Sport 3'],
				['http://mamahd.com/foxsports-1-live-stream-1.html','Foxsports 1'],
				['http://mamahd.com/foxsports-live-stream-1.html','Foxsports 2'],
				['http://mamahd.com/box-nation-live-streaming-free-1.html','Boxnation'],
				['http://mamahd.com/nfl-network-live-stream-free-1.html','NFL Network'],
				['http://mamahd.com/sky-sports-hd1-germany-live-stream-1.html','Sky HD1 DE'],
				['http://mamahd.com/sky-sports-hd2-germany-live-stream-1.html','Sky HD2 DE'],
				['http://mamahd.com/watch-sky-bundesliga-1-live-streaming-1.html','Bundesliga 1'],
				['http://mamahd.com/watch-bein-1-france-live-stream-1.html','BeIn 1 FR'],
				['http://mamahd.com/watch-bein-2-france-live-stream-1.html','BeIn 2 FR']]

		shadow = [['A&E','http://www.shadow-net.org/channels/A%26E.html','http://www.shadow-net.org/product_images/h/192/ae_tv__99609_thumb.jpg'],
			 ['ABC 2 Atlanta','http://www.shadow-net.org/channels/ABC-2-Atlanta.html','http://www.shadow-net.org/product_images/q/384/WSB-TV_ABC_1994__68454_thumb.PNG'],
			 ['ABC 27','http://www.shadow-net.org/channels/ABC-27.html','http://www.shadow-net.org/product_images/q/639/abc27__39425_thumb.jpg'],
			 ['ABC 7 New York','http://www.shadow-net.org/channels/ABC-7-New-York.html','http://www.shadow-net.org/product_images/b/900/wabc_abc7_new_york__26026_thumb.jpg'],
			 ['ABC Family','http://www.shadow-net.org/channels/ABC-Family.html','http://www.shadow-net.org/product_images/t/232/abc_family__05204_thumb.jpg'],
			 ['ABC News','http://www.shadow-net.org/channels/ABC-News.html','http://www.shadow-net.org/product_images/f/799/abc_news_now__18019_thumb.jpg'],
			 ['AFN Sports 2','http://www.shadow-net.org/channels/AFN-Sports-2.html','http://www.shadow-net.org/product_images/g/369/afn_sports2__04612_thumb.jpg'],
			 ['Al Jazeera America','http://www.shadow-net.org/channels/Al-Jazeera-America.html','http://www.shadow-net.org/product_images/r/030/Al_Jazeera_America_Logo__32655_thumb.png'],
			 ['AMC East','http://www.shadow-net.org/channels/AMC-East.html','http://www.shadow-net.org/product_images/r/604/amc__85163_thumb.jpg'],
			 ['Animal Planet US','http://www.shadow-net.org/channels/Animal-Planet-US.html','http://www.shadow-net.org/product_images/z/026/Animal_Planet_logo_%28black_and_green%29__59139_thumb.png'],
			 ['Bloomberg TV','http://www.shadow-net.org/channels/Bloomberg-TV.html','http://www.shadow-net.org/product_images/f/355/bloomberg__80284_thumb.jpg'],
			 ['Bravo','http://www.shadow-net.org/channels/Bravo.html','http://www.shadow-net.org/product_images/g/338/bravo_us__11790_thumb.jpg'],
			 ['Cartoon Network US','http://www.shadow-net.org/channels/Cartoon-Network-US.html','http://www.shadow-net.org/product_images/n/286/cartoon_network__82102_thumb.jpg'],
			 ['CBS 2 New York','http://www.shadow-net.org/channels/CBS-2-New-York.html','http://www.shadow-net.org/product_images/a/024/wcbs_cbs2_new_york__91850_thumb.jpg'],
			 ['CBS East','http://www.shadow-net.org/channels/CBS-East.html','http://www.shadow-net.org/product_images/z/021/cbs__60685_thumb.jpg'],
			 ['CBS News','http://www.shadow-net.org/channels/CBS-News.html','http://www.shadow-net.org/product_images/i/269/CBS_News2__07317_thumb.jpg'],
			 ['CNN International','http://www.shadow-net.org/channels/CNN-International.html','http://www.shadow-net.org/product_images/j/051/cnn_international__19122_thumb.jpg'],
			 ['CNN USA','http://www.shadow-net.org/channels/CNN-USA.html','http://www.shadow-net.org/product_images/p/470/cnn_usa__34139_thumb.jpg'],
			 ['Comedy Central','http://www.shadow-net.org/channels/Comedy-Central.html','http://www.shadow-net.org/product_images/o/226/comedy_central_us__62938_thumb.jpg'],
			 ['CW','http://www.shadow-net.org/channels/CW.html','http://www.shadow-net.org/product_images/r/672/CW_logo_color_v__09334_thumb.jpg'],
			 ['Discovery Investigation US','http://www.shadow-net.org/channels/Discovery-Investigation-US.html','http://www.shadow-net.org/product_images/w/036/investigation_discovery__91066_thumb.jpg'],
			 ['Discovery US','http://www.shadow-net.org/channels/Discovery-US.html','http://www.shadow-net.org/product_images/k/583/discovery_us__51096_thumb.jpg'],
			 ['Disney Channel US','http://www.shadow-net.org/channels/Disney-Channel-US.html','http://www.shadow-net.org/product_images/e/907/disney_channel__34733_thumb.jpg'],
			 ['ESPN 2','http://www.shadow-net.org/channels/ESPN-2.html','http://www.shadow-net.org/product_images/a/831/ESPN2_logo__59298_thumb.png'],
			 ['ESPN US','http://www.shadow-net.org/channels/ESPN-US.html','http://www.shadow-net.org/product_images/y/742/ESPN__66232_thumb.png'],
			 ['Fight Network','http://www.shadow-net.org/channels/Fight-Network.html','http://www.shadow-net.org/product_images/s/834/Fight_network_logo__56393_thumb.png'],
			 ['Food Network US','http://www.shadow-net.org/channels/Food-Network-US.html','http://www.shadow-net.org/product_images/z/857/food_network_uk__16280_thumb.jpg'],
			 ['FOX 13 News Tampa Bay','http://www.shadow-net.org/channels/FOX-13-News-Tampa-Bay.html','http://www.shadow-net.org/product_images/e/939/WTVT_Fox_13_logo__37207_thumb.png'],
			 ['FOX 2 St. Louis','http://www.shadow-net.org/channels/FOX-2-St.-Louis.html','http://www.shadow-net.org/product_images/v/930/KTVI_2_logo__11697_thumb.png'],
			 ['Fox 5 Washington DC','http://www.shadow-net.org/channels/Fox-5-Washington-DC.html','http://www.shadow-net.org/product_images/x/136/Wttg__90022_thumb.jpg'],
			 ['FOX News','http://www.shadow-net.org/channels/FOX-News.html','http://www.shadow-net.org/product_images/k/488/Fox_News_Channel_logo__03178_thumb.png'],
			 ['Golf Channel','http://www.shadow-net.org/channels/Golf-Channel.html','http://www.shadow-net.org/product_images/s/418/golf_channel_us__36323_thumb.jpg'],
			 ['H2','http://www.shadow-net.org/channels/H2.html','http://www.shadow-net.org/product_images/a/786/H2_TV_logo__18213_thumb.png'],
			 ['Hallmark Channel','http://www.shadow-net.org/channels/Hallmark-Channel.html','http://www.shadow-net.org/product_images/m/968/Hallmark-Channel-The-Heart-of-TV-Logo__99555_thumb.jpg'],
			 ['HGTV','http://www.shadow-net.org/channels/HGTV.html','http://www.shadow-net.org/product_images/v/595/HGTV_logo_2015__20364_thumb.png'],
			 ['History US','http://www.shadow-net.org/channels/History-US.html','http://www.shadow-net.org/product_images/c/576/history_europe__24065_thumb.jpg'],
			 ['HLN','http://www.shadow-net.org/channels/HLN.html','http://www.shadow-net.org/product_images/z/904/hln__89483_thumb.jpg'],
			 ['KRON 4 News San Francisco','http://www.shadow-net.org/channels/KRON-4-News-San-Francisco.html','http://www.shadow-net.org/product_images/v/424/KRON_4_Main_Logo__41805_thumb.png'],
			 ['KTLA 5','http://www.shadow-net.org/channels/KTLA-5.html','http://www.shadow-net.org/product_images/j/728/ktla_cw5_los_angeles__81822_thumb.jpg'],
			 ['Lifetime','http://www.shadow-net.org/channels/Lifetime.html','http://www.shadow-net.org/product_images/b/056/Lifetime_logo_2013__32042_thumb.png'],
			 ['MLB Network','http://www.shadow-net.org/channels/MLB-Network.html','http://www.shadow-net.org/product_images/o/660/mlb_network__27352_thumb.jpg'],
			 ['MSNBC','http://www.shadow-net.org/channels/MSNBC.html','http://www.shadow-net.org/product_images/e/114/msnbc__44837_thumb.jpg'],
			 ['MTV US','http://www.shadow-net.org/channels/MTV-US.html','http://www.shadow-net.org/product_images/w/104/MTV_Logo_2010__92640_thumb.png'],
			 ['NASA TV','http://www.shadow-net.org/channels/NASA-TV.html','http://www.shadow-net.org/product_images/m/506/nasa_tv_us__35798_thumb.jpg'],
			 ['National Geographic US','http://www.shadow-net.org/channels/National-Geographic-US.html','http://www.shadow-net.org/product_images/w/100/National_Geographic_Channel__77803_thumb.png'],
			 ['NBA TV','http://www.shadow-net.org/channels/NBA-TV.html','http://www.shadow-net.org/product_images/u/073/nba_tv__20518_thumb.jpg'],
			 ['NBC 4 New York','http://www.shadow-net.org/channels/NBC-4-New-York.html','http://www.shadow-net.org/product_images/c/970/wnbc_nbc4_new_york__88786_thumb.jpg'],
			 ['NBC East','http://www.shadow-net.org/channels/NBC-East.html','http://www.shadow-net.org/product_images/w/554/nbc__14605_thumb.gif'],
			 ['NBC Sports Netw.','http://www.shadow-net.org/channels/NBC-Sports-Netw..html','http://www.shadow-net.org/product_images/q/063/nbc_sports_network__66246_thumb.jpg'],
			 ['NFL Network','http://www.shadow-net.org/channels/NFL-Network.html','http://www.shadow-net.org/product_images/n/410/nfl_network__08611_thumb.jpg'],
			 ['NHL Network','http://www.shadow-net.org/channels/NHL-Network.html','http://www.shadow-net.org/product_images/v/462/NHL_Network_2011__53239_thumb.png'],
			 ['Nickelodeon US','http://www.shadow-net.org/channels/Nickelodeon-US.html','http://www.shadow-net.org/product_images/w/877/Nickelodeon_logo_new__07923_thumb.png'],
			 ['Pac 12 Arizona','http://www.shadow-net.org/channels/Pac-12-Arizona.html','http://www.shadow-net.org/product_images/f/860/Pac-12_Networks_logo__13866_thumb.png'],
			 ['Pac 12 Bay Area','http://www.shadow-net.org/channels/Pac-12-Bay-Area.html','http://www.shadow-net.org/product_images/c/453/Pac-12_Networks_logo__07345_thumb.png'],
			 ['Pac 12 Los Angeles','http://www.shadow-net.org/channels/Pac-12-Los-Angeles.html','http://www.shadow-net.org/product_images/y/660/Pac-12_Networks_logo__02467_thumb.png'],
			 ['Pac 12 Mountain','http://www.shadow-net.org/channels/Pac-12-Mountain.html','http://www.shadow-net.org/product_images/n/028/Pac-12_Networks_logo__03916_thumb.png'],
			 ['Pac 12 National Network','http://www.shadow-net.org/channels/Pac-12-National-Network.html','http://www.shadow-net.org/product_images/f/759/Pac-12_Networks_logo__13527_thumb.png'],
			 ['Pac 12 Oregon','http://www.shadow-net.org/channels/Pac-12-Oregon.html','http://www.shadow-net.org/product_images/d/706/Pac-12_Networks_logo__50740_thumb.png'],
			 ['Pac 12 Washington','http://www.shadow-net.org/channels/Pac-12-Washington.html','http://www.shadow-net.org/product_images/d/574/Pac-12_Networks_logo__54056_thumb.png'],
			 ['PBS Wisconsin','http://www.shadow-net.org/channels/PBS-Wisconsin.html','http://www.shadow-net.org/product_images/p/766/pbs_east__81153_thumb.jpg'],
			 ['RT America','http://www.shadow-net.org/channels/RT-America.html','http://www.shadow-net.org/product_images/l/726/Russia-today-logo__86701_thumb.png'],
			 ['Spike','http://www.shadow-net.org/channels/Spike.html','http://www.shadow-net.org/product_images/z/232/Spike_logo_2015__98357_thumb.png'],
			 ['Sportsnet 360','http://www.shadow-net.org/channels/Sportsnet-360.html','http://www.shadow-net.org/product_images/a/095/Sportsnet-360-Logo__31086_thumb.jpg'],
			 ['Sportsnet One','http://www.shadow-net.org/channels/Sportsnet-One.html','http://www.shadow-net.org/product_images/x/985/Sportsnetone2011__31537_thumb.png'],
			 ['Sportsnet World','http://www.shadow-net.org/channels/Sportsnet-World.html','http://www.shadow-net.org/product_images/e/626/SportsnetWorld__37094_thumb.png'],
			 ['Starz','http://www.shadow-net.org/channels/Starz.html','http://www.shadow-net.org/product_images/f/200/Starz_2008__56778_thumb.png'],
			 ['Syfy','http://www.shadow-net.org/channels/Syfy.html','http://www.shadow-net.org/product_images/f/954/syfy__52943_thumb.jpg'],
			 ['TBS','http://www.shadow-net.org/channels/TBS.html','http://www.shadow-net.org/product_images/f/523/TBS.svg__23453_thumb.png'],
			 ['TLC','http://www.shadow-net.org/channels/TLC.html','http://www.shadow-net.org/product_images/g/894/TLC_USA_logo__18952_thumb.png'],
			 ['TNT','http://www.shadow-net.org/channels/TNT.html','http://www.shadow-net.org/product_images/e/600/tnt__28275_thumb.jpg'],
			 ['Travel Channel US','http://www.shadow-net.org/channels/Travel-Channel-US.html','http://www.shadow-net.org/product_images/f/359/Travel_Channel_HD_2013__46217_thumb.png'],
			 ['TruTV','http://www.shadow-net.org/channels/TruTV.html','http://www.shadow-net.org/product_images/l/545/TruTV_logo_2014__51891_thumb.png'],
			 ['TSN 1','http://www.shadow-net.org/channels/TSN-1.html','http://www.shadow-net.org/product_images/u/487/tsn__98863_thumb.jpg'],
			 ['TSN 2','http://www.shadow-net.org/channels/TSN-2.html','http://www.shadow-net.org/product_images/b/342/tsn2__61112_thumb.jpg'],
			 ['TSN 3','http://www.shadow-net.org/channels/TSN-3.html','http://www.shadow-net.org/product_images/f/245/tsn3__97431_thumb.png'],
			 ['TSN 4','http://www.shadow-net.org/channels/TSN-4.html','http://www.shadow-net.org/product_images/y/045/tsn4__75023_thumb.png'],
			 ['USA Network','http://www.shadow-net.org/channels/USA-Network.html','http://www.shadow-net.org/product_images/a/517/usa_network__57030_thumb.jpg'],
			 ['VH1','http://www.shadow-net.org/channels/VH1.html','http://www.shadow-net.org/product_images/l/556/VH1_logonew__62136_thumb.png'],
			 ['WeatherNation','http://www.shadow-net.org/channels/WeatherNation.html','http://www.shadow-net.org/product_images/h/491/WeatherNation_logo__53910_thumb.png'],
			 ['WJHL Tennessee','http://www.shadow-net.org/channels/WJHL-Tennessee.html','http://www.shadow-net.org/product_images/l/084/WJHL-TV_2012_logo__63534_thumb.png'],
			 ['WTHI Terre Haute','http://www.shadow-net.org/channels/WTHI-Terre-Haute.html','http://www.shadow-net.org/product_images/j/981/WTHI_2012_Logo__76059_thumb.png'],
			 ['WWE Network','http://www.shadow-net.org/channels/WWE-Network.html','http://www.shadow-net.org/product_images/h/880/world_wrestling_entertainment__70123_thumb.jpg'],
			 ['5Star','http://www.shadow-net.org/channels/5Star.html','http://www.shadow-net.org/product_images/i/018/channel_5_uk_star__59646_thumb.png'],
			 ['5USA','http://www.shadow-net.org/channels/5USA.html','http://www.shadow-net.org/product_images/s/311/channel5_usa__70905_thumb.jpg'],
			 ['Animal Planet UK','http://www.shadow-net.org/channels/Animal-Planet-UK.html','http://www.shadow-net.org/product_images/w/160/Animal_Planet_logo_%28black_and_green%29__98995_thumb.png'],
			 ['At The Races','http://www.shadow-net.org/channels/At-The-Races.html','http://www.shadow-net.org/product_images/s/772/at_the_races_uk__25721_thumb.jpg'],
			 ['BBC 1','http://www.shadow-net.org/channels/BBC-1.html','http://www.shadow-net.org/product_images/r/418/BBC_One_2002__20962_thumb.png'],
			 ['BBC 2','http://www.shadow-net.org/channels/BBC-2.html','http://www.shadow-net.org/product_images/x/270/BBC_Two.svg_%281%29__18552_thumb.png'],
			 ['BBC 3','http://www.shadow-net.org/channels/BBC-3.html','http://www.shadow-net.org/product_images/z/431/bbc3__58300_thumb.jpg'],
			 ['BBC 4','http://www.shadow-net.org/channels/BBC-4.html','http://www.shadow-net.org/product_images/u/402/bbc4__60255_thumb.jpg'],
			 ['BBC News','http://www.shadow-net.org/channels/BBC-News.html','http://www.shadow-net.org/product_images/u/125/bbc_news__39343_thumb.jpg'],
			 ['BBC Wold News','http://www.shadow-net.org/channels/BBC-Wold-News.html','http://www.shadow-net.org/product_images/p/302/bbc_world__60450_thumb.jpg'],
			 ['BoxNation','http://www.shadow-net.org/channels/BoxNation.html','http://www.shadow-net.org/product_images/h/426/box_nation__84194_thumb.jpg'],
			 ['British Eurosport 1','http://www.shadow-net.org/channels/British-Eurosport-1.html','http://www.shadow-net.org/product_images/g/814/british_eurosport__44049_thumb.jpg'],
			 ['British Eurosport 2','http://www.shadow-net.org/channels/British-Eurosport-2.html','http://www.shadow-net.org/product_images/f/591/british_eurosport2__58698_thumb.jpg'],
			 ['BT Sport 1','http://www.shadow-net.org/channels/BT-Sport-1.html','http://www.shadow-net.org/product_images/z/622/bt_sport_1__18746_thumb.jpg'],
			 ['BT Sport 2','http://www.shadow-net.org/channels/BT-Sport-2.html','http://www.shadow-net.org/product_images/y/951/bt_sport_2__63983_thumb.jpg'],
			 ['BT Sport ESPN','http://www.shadow-net.org/channels/BT-Sport-ESPN.html','http://www.shadow-net.org/product_images/t/735/BT_Sport_ESPN_logo__79357_thumb.png'],
			 ['BT Sport Europe','http://www.shadow-net.org/channels/BT-Sport-Europe.html','http://www.shadow-net.org/product_images/b/335/bt_sport_europe_uk__81016_thumb.jpg'],
			 ['Capital','http://www.shadow-net.org/channels/Capital.html','http://www.shadow-net.org/product_images/r/954/Capital_TV_logo__27138_thumb.png'],
			 ['Cartoon Network UK','http://www.shadow-net.org/channels/Cartoon-Network-UK.html','http://www.shadow-net.org/product_images/x/048/cartoon_network__02584_thumb.jpg'],
			 ['CBS Action','http://www.shadow-net.org/channels/CBS-Action.html','http://www.shadow-net.org/product_images/k/353/cbs_action_uk__54811_thumb.png'],
			 ['CBS Drama','http://www.shadow-net.org/channels/CBS-Drama.html','http://www.shadow-net.org/product_images/u/097/cbs_drama_eu__13760_thumb.png'],
			 ['CBS Reality','http://www.shadow-net.org/channels/CBS-Reality.html','http://www.shadow-net.org/product_images/u/279/cbs_reality__44213_thumb.jpg'],
			 ['CBS Reality +1','http://www.shadow-net.org/channels/CBS-Reality-%252b1.html','http://www.shadow-net.org/product_images/n/056/cbs_reality_plus1__81996_thumb.png'],
			 ['Channel 4','http://www.shadow-net.org/channels/Channel-4.html','http://www.shadow-net.org/product_images/s/715/channel4__56690_thumb.jpg'],
			 ['Channel 5','http://www.shadow-net.org/channels/Channel-5.html','http://www.shadow-net.org/product_images/m/671/channel5_uk__99265_thumb.jpg'],
			 ['Chelsea TV','http://www.shadow-net.org/channels/Chelsea-TV.html','http://www.shadow-net.org/product_images/s/436/chelsea_tv__40010_thumb.jpg'],
			 ['Comedy Central UK','http://www.shadow-net.org/channels/Comedy-Central-UK.html','http://www.shadow-net.org/product_images/u/379/comedy_central_us__55592__60778_thumb.jpg'],
			 ['Dave','http://www.shadow-net.org/channels/Dave.html','http://www.shadow-net.org/product_images/q/672/dave__30048_thumb.jpg'],
			 ['Discovery History','http://www.shadow-net.org/channels/Discovery-History.html','http://www.shadow-net.org/product_images/q/707/Discovery_History_2010__01621_thumb.png'],
			 ['Discovery Investigation UK','http://www.shadow-net.org/channels/Discovery-Investigation-UK.html','http://www.shadow-net.org/product_images/x/369/investigation_discovery__87602_thumb.jpg'],
			 ['Discovery Science UK','http://www.shadow-net.org/channels/Discovery-Science-UK.html','http://www.shadow-net.org/product_images/t/726/Discovery_Science_h__96606_thumb.png'],
			 ['Discovery UK','http://www.shadow-net.org/channels/Discovery-UK.html','http://www.shadow-net.org/product_images/j/140/discovery_us__02242_thumb.jpg'],
			 ['Disney Channel UK','http://www.shadow-net.org/channels/Disney-Channel-UK.html','http://www.shadow-net.org/product_images/g/535/disney_channel__10345_thumb.jpg'],
			 ['E! Entertainment','http://www.shadow-net.org/channels/E%21-Entertainment.html','http://www.shadow-net.org/product_images/r/548/E%21_Logo_2012__59361_thumb.png'],
			 ['E4','http://www.shadow-net.org/channels/E4.html','http://www.shadow-net.org/product_images/x/573/e4_uk__72574_thumb.jpg'],
			 ['Euronews','http://www.shadow-net.org/channels/Euronews.html','http://www.shadow-net.org/product_images/l/724/euronews__73752_thumb.jpg'],
			 ['Film 4','http://www.shadow-net.org/channels/Film-4.html','http://www.shadow-net.org/product_images/v/827/film4__52400_thumb.jpg'],
			 ['Food Network +1','http://www.shadow-net.org/channels/Food-Network-%252b1.html','http://www.shadow-net.org/product_images/m/359/food_network_uk__23707_thumb.jpg'],
			 ['Food Network UK','http://www.shadow-net.org/channels/Food-Network-UK.html','http://www.shadow-net.org/product_images/q/298/food_network_uk__02476_thumb.jpg'],
			 ['Gold','http://www.shadow-net.org/channels/Gold.html','http://www.shadow-net.org/product_images/c/241/gold_black_background__91302_thumb.jpg'],
			 ['Heart TV','http://www.shadow-net.org/channels/Heart-TV.html','http://www.shadow-net.org/product_images/z/606/Heart_TV_logo__58712_thumb.png'],
			 ['History UK','http://www.shadow-net.org/channels/History-UK.html','http://www.shadow-net.org/product_images/z/917/history_europe__17235_thumb.jpg'],
			 ['ITV 1','http://www.shadow-net.org/channels/ITV-1.html','http://www.shadow-net.org/product_images/p/615/itv_uk__27094_thumb.jpg'],
			 ['ITV 1+1','http://www.shadow-net.org/channels/ITV-1%252b1.html','http://www.shadow-net.org/product_images/y/695/itv1_plus1__81714_thumb.jpg'],
			 ['ITV 2','http://www.shadow-net.org/channels/ITV-2.html','http://www.shadow-net.org/product_images/x/104/itv2__44555_thumb.jpg'],
			 ['ITV 2+1','http://www.shadow-net.org/channels/ITV-2%252b1.html','http://www.shadow-net.org/product_images/p/722/itv2_plus1__56577_thumb.jpg'],
			 ['ITV 3','http://www.shadow-net.org/channels/ITV-3.html','http://www.shadow-net.org/product_images/k/294/itv3__61186_thumb.jpg'],
			 ['ITV 3+1','http://www.shadow-net.org/channels/ITV-3%252b1.html','http://www.shadow-net.org/product_images/z/673/itv3_plus1__43817_thumb.jpg'],
			 ['ITV 4','http://www.shadow-net.org/channels/ITV-4.html','http://www.shadow-net.org/product_images/r/387/itv4__95441_thumb.jpg'],
			 ['ITV 4+1','http://www.shadow-net.org/channels/ITV-4%252b1.html','http://www.shadow-net.org/product_images/i/517/itv4_plus1__96475_thumb.jpg'],
			 ['ITV Be','http://www.shadow-net.org/channels/ITV-Be.html','http://www.shadow-net.org/product_images/x/968/ITVBe_logo_2014-__58951_thumb.png'],
			 ['London Live','http://www.shadow-net.org/channels/London-Live.html','http://www.shadow-net.org/product_images/v/648/london_live__38073_thumb.png'],
			 ['Manchester United TV','http://www.shadow-net.org/channels/Manchester-United-TV.html','http://www.shadow-net.org/product_images/i/675/mutv__18782_thumb.jpg'],
			 ['More 4','http://www.shadow-net.org/channels/More-4.html','http://www.shadow-net.org/product_images/w/935/more4__90180_thumb.jpg'],
			 ['Motors TV','http://www.shadow-net.org/channels/Motors-TV.html','http://www.shadow-net.org/product_images/s/922/MotorsTV-logo__73046_thumb.png'],
			 ['MTV Classic UK','http://www.shadow-net.org/channels/MTV-Classic-UK.html','http://www.shadow-net.org/product_images/z/697/MTV_Classic_logo_2013__65812_thumb.png'],
			 ['MTV Dance','http://www.shadow-net.org/channels/MTV-Dance.html','http://www.shadow-net.org/product_images/x/506/MTV_Dance_2013__40554_thumb.png'],
			 ['MTV Hits','http://www.shadow-net.org/channels/MTV-Hits.html','http://www.shadow-net.org/product_images/b/347/MTV_Hits_Logo_2012__61325_thumb.png'],
			 ['MTV Rocks','http://www.shadow-net.org/channels/MTV-Rocks.html','http://www.shadow-net.org/product_images/w/993/MTV_Rocks_logo_2013__21136_thumb.png'],
			 ['Nat Geo Wild UK','http://www.shadow-net.org/channels/Nat-Geo-Wild-UK.html','http://www.shadow-net.org/product_images/s/246/nat_geo_wild__16696_thumb.jpg'],
			 ['National Geographic UK','http://www.shadow-net.org/channels/National-Geographic-UK.html','http://www.shadow-net.org/product_images/h/958/National_Geographic_Channel__15826_thumb.png'],
			 ['Premier Sports','http://www.shadow-net.org/channels/Premier-Sports.html','http://www.shadow-net.org/product_images/i/771/Premier_Sports_logo__59689_thumb.png'],
			 ['Quest','http://www.shadow-net.org/channels/Quest.html','http://www.shadow-net.org/product_images/e/017/quest__28625_thumb.jpg'],
			 ['Racing UK','http://www.shadow-net.org/channels/Racing-UK.html','http://www.shadow-net.org/product_images/h/544/racing_uk__87840_thumb.jpg'],
			 ['Really','http://www.shadow-net.org/channels/Really.html','http://www.shadow-net.org/product_images/c/248/Really_logo_2013__65352_thumb.png'],
			 ['RTE One','http://www.shadow-net.org/channels/RTE-One.html','http://www.shadow-net.org/product_images/m/283/rte_one__12324_thumb.jpg'],
			 ['RTE Two','http://www.shadow-net.org/channels/RTE-Two.html','http://www.shadow-net.org/product_images/c/249/rte_two__61649_thumb.jpg'],
			 ['Setanta Ireland','http://www.shadow-net.org/channels/Setanta-Ireland.html','http://www.shadow-net.org/product_images/t/788/setanta_sports_ie__75006_thumb.jpg'],
			 ['Sky 1','http://www.shadow-net.org/channels/Sky-1.html','http://www.shadow-net.org/product_images/a/865/sky_uk_1__64403_thumb.jpg'],
			 ['Sky 2','http://www.shadow-net.org/channels/Sky-2.html','http://www.shadow-net.org/product_images/n/296/sky_uk_2__94151_thumb.jpg'],
			 ['Sky Atlantic','http://www.shadow-net.org/channels/Sky-Atlantic.html','http://www.shadow-net.org/product_images/t/541/sky_uk_atlantic__46552_thumb.jpg'],
			 ['Sky News','http://www.shadow-net.org/channels/Sky-News.html','http://www.shadow-net.org/product_images/j/542/sky_news__04995_thumb.jpg'],
			 ['Sky Sports 5','http://www.shadow-net.org/channels/Sky-Sports-5.html','http://www.shadow-net.org/product_images/k/949/sky_uk_sports5__60555_thumb.png'],
			 ['Sky Sports F1','http://www.shadow-net.org/channels/Sky-Sports-F1.html','http://www.shadow-net.org/product_images/m/296/sky_uk_sports_f1__96235_thumb.jpg'],
			 ['Sky Sports News','http://www.shadow-net.org/channels/Sky-Sports-News.html','http://www.shadow-net.org/product_images/j/929/sky_uk_sports_news_hq__53705_thumb.jpg'],
			 ['Sky Sports1','http://www.shadow-net.org/channels/Sky-Sports1.html','http://www.shadow-net.org/product_images/g/437/sky_sports1__15526_thumb.jpg'],
			 ['TG4 Ireland','http://www.shadow-net.org/channels/TG4-Ireland.html','http://www.shadow-net.org/product_images/i/427/TG4_logo__50346_thumb.png'],
			 ['The Vault','http://www.shadow-net.org/channels/The-Vault.html','http://www.shadow-net.org/product_images/x/145/The_Vault_TV_channel_logo_2014__13912_thumb.png'],
			 ['Travel Channel +1','http://www.shadow-net.org/channels/Travel-Channel-%252b1.html','http://www.shadow-net.org/product_images/w/588/Travel_Channel_HD_2013__76743_thumb.png'],
			 ['TruTV UK','http://www.shadow-net.org/channels/TruTV-UK.html','http://www.shadow-net.org/product_images/s/962/TruTV_logo_2014__66876_thumb.png'],
			 ['Yesterday','http://www.shadow-net.org/channels/Yesterday.html','http://www.shadow-net.org/product_images/m/948/Yesterday_logo_2012__75992_thumb.png'],
			 ['1 Music Channel','http://www.shadow-net.org/channels/1-Music-Channel.html','http://www.shadow-net.org/product_images/j/674/1music_channel__45014_thumb.jpg'],
			 ['2 Plus Moldova','http://www.shadow-net.org/channels/2-Plus-Moldova.html','http://www.shadow-net.org/product_images/f/797/2plus__71764_thumb.jpg'],
			 ['Acasa TV','http://www.shadow-net.org/channels/Acasa-TV.html','http://www.shadow-net.org/product_images/y/598/acasatv__35745_thumb.jpg'],
			 ['Acasa TV Gold','http://www.shadow-net.org/channels/Acasa-TV-Gold.html','http://www.shadow-net.org/product_images/t/614/acasatv_gold__73715_thumb.jpg'],
			 ['Antena 3','http://www.shadow-net.org/channels/Antena-3.html','http://www.shadow-net.org/product_images/x/167/antena_3__63718_thumb.jpg'],
			 ['Antena Stars','http://www.shadow-net.org/channels/Antena-Stars.html','http://www.shadow-net.org/product_images/d/566/antena_stars_ro__84231_thumb.png'],
			 ['AXN Black','http://www.shadow-net.org/channels/AXN-Black.html','http://www.shadow-net.org/product_images/v/621/axn_black__67969_thumb.jpg'],
			 ['AXN Romania','http://www.shadow-net.org/channels/AXN-Romania.html','http://www.shadow-net.org/product_images/w/585/axn__49217_thumb.jpg'],
			 ['AXN Spin','http://www.shadow-net.org/channels/AXN-Spin.html','http://www.shadow-net.org/product_images/p/623/axn_spin__27350_thumb.jpg'],
			 ['AXN White','http://www.shadow-net.org/channels/AXN-White.html','http://www.shadow-net.org/product_images/t/218/axn_white__53602_thumb.jpg'],
			 ['B1 TV','http://www.shadow-net.org/channels/B1-TV.html','http://www.shadow-net.org/product_images/o/122/b__04086_thumb.JPG'],
			 ['Boomerang RO','http://www.shadow-net.org/channels/Boomerang-RO.html','http://www.shadow-net.org/product_images/o/308/Boomerang_2014_logo__68388_thumb.png'],
			 ['Busuioc TV','http://www.shadow-net.org/channels/Busuioc-TV.html','http://www.shadow-net.org/product_images/y/696/busuioc-tv1__38947_thumb.png'],
			 ['Cartoon Network RO','http://www.shadow-net.org/channels/Cartoon-Network-RO.html','http://www.shadow-net.org/product_images/l/311/cartoon_network__89253_thumb.jpg'],
			 ['Discovery Channel RO','http://www.shadow-net.org/channels/Discovery-Channel-RO.html','http://www.shadow-net.org/product_images/t/481/discovery_us__36360_thumb.jpg'],
			 ['Discovery Investigation RO','http://www.shadow-net.org/channels/Discovery-Investigation-RO.html','http://www.shadow-net.org/product_images/c/338/investigation_discovery__43034_thumb.jpg'],
			 ['Discovery Science RO','http://www.shadow-net.org/channels/Discovery-Science-RO.html','http://www.shadow-net.org/product_images/v/176/discovery_science__39598_thumb.jpg'],
			 ['Discovery World RO','http://www.shadow-net.org/channels/Discovery-World-RO.html','http://www.shadow-net.org/product_images/a/473/discovery_world__84339_thumb.jpg'],
			 ['Disney Channel RO','http://www.shadow-net.org/channels/Disney-Channel-RO.html','http://www.shadow-net.org/product_images/d/186/disney_channel__22318_thumb.jpg'],
			 ['Disney Junior RO','http://www.shadow-net.org/channels/Disney-Junior-RO.html','http://www.shadow-net.org/product_images/x/975/disney_junior__56938_thumb.jpg'],
			 ['DIVA Universal','http://www.shadow-net.org/channels/DIVA-Universal.html','http://www.shadow-net.org/product_images/b/137/diva_universal__81331_thumb.jpg'],
			 ['Euforia TV','http://www.shadow-net.org/channels/Euforia-TV.html','http://www.shadow-net.org/product_images/b/079/euforia__17340_thumb.jpg'],
			 ['Europa Plus TV','http://www.shadow-net.org/channels/Europa-Plus-TV.html','http://www.shadow-net.org/product_images/t/445/europa_plus_tv__13286_thumb.jpg'],
			 ['Film Cafe','http://www.shadow-net.org/channels/Film-Cafe.html','http://www.shadow-net.org/product_images/k/094/film_cafe__88821_thumb.jpg'],
			 ['History Channel RO','http://www.shadow-net.org/channels/History-Channel-RO.html','http://www.shadow-net.org/product_images/c/633/history_europe__92303_thumb.jpg'],
			 ['Kanal D','http://www.shadow-net.org/channels/Kanal-D.html','http://www.shadow-net.org/product_images/k/016/kanald__51428_thumb.jpg'],
			 ['Kanal D SOP','http://www.shadow-net.org/channels/Kanal-D-SOP.html','http://www.shadow-net.org/product_images/w/449/kanald__77882_thumb.jpg'],
			 ['Look TV','http://www.shadow-net.org/channels/Look-TV.html','http://www.shadow-net.org/product_images/w/748/look_tv_ro__91074_thumb.jpg'],
			 ['MBC Moldova','http://www.shadow-net.org/channels/MBC-Moldova.html','http://www.shadow-net.org/product_images/e/655/mbc_md__92415_thumb.jpg'],
			 ['Minimax RO','http://www.shadow-net.org/channels/Minimax-RO.html','http://www.shadow-net.org/product_images/a/080/minimax__47002_thumb.jpg'],
			 ['Moldova 1','http://www.shadow-net.org/channels/Moldova-1.html','http://www.shadow-net.org/product_images/x/931/moldova1__66582_thumb.jpg'],
			 ['Nat Geo Wild RO','http://www.shadow-net.org/channels/Nat-Geo-Wild-RO.html','http://www.shadow-net.org/product_images/a/060/nat_geo_wild__45489_thumb.jpg'],
			 ['National Geographic RO','http://www.shadow-net.org/channels/National-Geographic-RO.html','http://www.shadow-net.org/product_images/q/711/nat_geo_channel__71158_thumb.jpg'],
			 ['National TV','http://www.shadow-net.org/channels/National-TV.html','http://www.shadow-net.org/product_images/a/855/ntv_ro__82947_thumb.jpg'],
			 ['Nick Jr. RO','http://www.shadow-net.org/channels/Nick-Jr.-RO.html','http://www.shadow-net.org/product_images/l/551/nick_jr__68462_thumb.jpg'],
			 ['Nickelodeon RO','http://www.shadow-net.org/channels/Nickelodeon-RO.html','http://www.shadow-net.org/product_images/k/445/nickelodeon_us__87438_thumb.jpg'],
			 ['Noroc TV','http://www.shadow-net.org/channels/Noroc-TV.html','http://www.shadow-net.org/product_images/g/451/noroc_tv__33489_thumb.jpg'],
			 ['Paramount Channel','http://www.shadow-net.org/channels/Paramount-Channel.html','http://www.shadow-net.org/product_images/o/159/paramount_channel__04267_thumb.jpg'],
			 ['Prima TV','http://www.shadow-net.org/channels/Prima-TV.html','http://www.shadow-net.org/product_images/a/793/prima_tv__85329_thumb.jpg'],
			 ['Pro Cinema','http://www.shadow-net.org/channels/Pro-Cinema.html','http://www.shadow-net.org/product_images/c/484/pro_cinema__85098_thumb.jpg'],
			 ['PRO TV Chisinau','http://www.shadow-net.org/channels/PRO-TV-Chisinau.html','http://www.shadow-net.org/product_images/l/060/pro_tv_chisinau__82297_thumb.jpg'],
			 ['ProTV','http://www.shadow-net.org/channels/ProTV.html','http://www.shadow-net.org/product_images/a/051/pro_tv_hd__02175_thumb.jpg'],
			 ['Publika Moldova','http://www.shadow-net.org/channels/Publika-Moldova.html','http://www.shadow-net.org/product_images/o/560/publika_md__63811_thumb.jpg'],
			 ['PV TV','http://www.shadow-net.org/channels/PV-TV.html','http://www.shadow-net.org/product_images/r/202/pv_tv__21819_thumb.jpg'],
			 ['Realitatea TV','http://www.shadow-net.org/channels/Realitatea-TV.html','http://www.shadow-net.org/product_images/t/836/realitatea_tv__98067_thumb.jpg'],
			 ['Realitatea TV Sop','http://www.shadow-net.org/channels/Realitatea-TV-Sop.html','http://www.shadow-net.org/product_images/y/807/realitatea_tv__90437_thumb.jpg'],
			 ['REN TV','http://www.shadow-net.org/channels/REN-TV.html','http://www.shadow-net.org/product_images/r/761/ren_tv__86337_thumb.jpg'],
			 ['Romania TV Sop','http://www.shadow-net.org/channels/Romania-TV-Sop.html','http://www.shadow-net.org/product_images/u/201/rtv__77670_thumb.jpg'],
			 ['Romania TV VLC','http://www.shadow-net.org/channels/Romania-TV-VLC.html','http://www.shadow-net.org/product_images/s/251/rtv__06919_thumb.jpg'],
			 ['Taraf TV','http://www.shadow-net.org/channels/Taraf-TV.html','http://www.shadow-net.org/product_images/k/042/taraftv__74457_thumb.jpg'],
			 ['TV 1000','http://www.shadow-net.org/channels/TV-1000.html','http://www.shadow-net.org/product_images/y/342/tv1000__26849_thumb.jpg'],
			 ['TV7 Moldova','http://www.shadow-net.org/channels/TV7-Moldova.html','http://www.shadow-net.org/product_images/k/609/tv7_md__03464_thumb.jpg'],
			 ['TVC 21','http://www.shadow-net.org/channels/TVC-21.html','http://www.shadow-net.org/product_images/f/539/tvc_21_md__08116_thumb.jpg'],
			 ['TVR1','http://www.shadow-net.org/channels/TVR1.html','http://www.shadow-net.org/product_images/y/593/tvr1__58209_thumb.jpg'],
			 ['TVR2','http://www.shadow-net.org/channels/TVR2.html','http://www.shadow-net.org/product_images/o/307/tvr2__87976_thumb.jpg'],
			 ['UTV','http://www.shadow-net.org/channels/UTV.html','http://www.shadow-net.org/product_images/c/088/u_tv__51904_thumb.jpg'],
			 ['Viasat Explore','http://www.shadow-net.org/channels/Viasat-Explore.html','http://www.shadow-net.org/product_images/f/967/viasat_explore__28460_thumb.jpg'],
			 ['Viasat History','http://www.shadow-net.org/channels/Viasat-History.html','http://www.shadow-net.org/product_images/j/357/viasat_history__39867_thumb.jpg'],
			 ['Viasat Nature','http://www.shadow-net.org/channels/Viasat-Nature.html','http://www.shadow-net.org/product_images/n/686/viasat_nature_east__80761_thumb.jpg'],
			 ['Das Erste','http://www.shadow-net.org/channels/Das-Erste.html','http://www.shadow-net.org/product_images/w/786/ard__19793_thumb.jpg'],
			 ['Deutsche Welle','http://www.shadow-net.org/channels/Deutsche-Welle.html','http://www.shadow-net.org/product_images/a/044/dw_tv__63402_thumb.jpg'],
			 ['Disney Channel DE','http://www.shadow-net.org/channels/Disney-Channel-DE.html','http://www.shadow-net.org/product_images/y/352/disney_channel__26154_thumb.jpg'],
			 ['Kabel Eins','http://www.shadow-net.org/channels/Kabel-Eins.html','http://www.shadow-net.org/product_images/t/152/kabel1__63893_thumb.jpg'],
			 ['KiKa','http://www.shadow-net.org/channels/KiKa.html','http://www.shadow-net.org/product_images/g/009/kinderkanal__49484_thumb.jpg'],
			 ['N-TV','http://www.shadow-net.org/channels/N%252dTV.html','http://www.shadow-net.org/product_images/l/779/ntv_de__93235_thumb.jpg'],
			 ['One','http://www.shadow-net.org/channels/One.html','http://www.shadow-net.org/product_images/b/702/One_TV_Logo__93960_thumb.png'],
			 ['ORF 1','http://www.shadow-net.org/channels/ORF-1.html','http://www.shadow-net.org/product_images/q/474/orf1__10981_thumb.jpg'],
			 ['ORF 2','http://www.shadow-net.org/channels/ORF-2.html','http://www.shadow-net.org/product_images/i/440/orf2__54577_thumb.jpg'],
			 ['ORF 3','http://www.shadow-net.org/channels/ORF-3.html','http://www.shadow-net.org/product_images/o/172/orf3__13173_thumb.jpg'],
			 ['ORF Sport Plus','http://www.shadow-net.org/channels/ORF-Sport-Plus.html','http://www.shadow-net.org/product_images/l/294/orf_sport_plus__00985_thumb.jpg'],
			 ['Phoenix','http://www.shadow-net.org/channels/Phoenix.html','http://www.shadow-net.org/product_images/x/727/Phoenix_Logo_2012.svg__42553_thumb.png'],
			 ['ProSieben','http://www.shadow-net.org/channels/ProSieben.html','http://www.shadow-net.org/product_images/j/009/pro7__88480_thumb.jpg'],
			 ['RBB Berlin','http://www.shadow-net.org/channels/RBB-Berlin.html','http://www.shadow-net.org/product_images/j/738/rbb_de__66295_thumb.jpg'],
			 ['RTL','http://www.shadow-net.org/channels/RTL.html','http://www.shadow-net.org/product_images/i/119/rtl__48257_thumb.jpg'],
			 ['RTL 2','http://www.shadow-net.org/channels/RTL-2.html','http://www.shadow-net.org/product_images/p/269/rtl__41751_thumb.jpg'],
			 ['Sat.1','http://www.shadow-net.org/channels/Sat.1.html','http://www.shadow-net.org/product_images/f/936/sat1__13963_thumb.jpg'],
			 ['Servus TV','http://www.shadow-net.org/channels/Servus-TV.html','http://www.shadow-net.org/product_images/o/951/servus_tv_de__91079_thumb.jpg'],
			 ['Sky Sport News','http://www.shadow-net.org/channels/Sky-Sport-News.html','http://www.shadow-net.org/product_images/w/904/ssn-de__00706_thumb.jpg'],
			 ['SWR','http://www.shadow-net.org/channels/SWR.html','http://www.shadow-net.org/product_images/m/405/swr__19794_thumb.jpg'],
			 ['tagesschau24','http://www.shadow-net.org/channels/tagesschau24.html','http://www.shadow-net.org/product_images/f/462/301px-Tagesschau24-2012__84641_thumb.png'],
			 ['WDR Fernsehen','http://www.shadow-net.org/channels/WDR-Fernsehen.html','http://www.shadow-net.org/product_images/p/281/wdr_fernsehen_koln__11515_thumb.jpg'],
			 ['ZDF','http://www.shadow-net.org/channels/ZDF.html','http://www.shadow-net.org/product_images/l/154/zdf__67759_thumb.jpg'],
			 ['ZDF Neo','http://www.shadow-net.org/channels/ZDF-Neo.html','http://www.shadow-net.org/product_images/a/558/zdf_neo__47353_thumb.jpg'],
			 ['Cielo','http://www.shadow-net.org/channels/Cielo.html','http://www.shadow-net.org/product_images/c/953/cielo__18877_thumb.jpg'],
			 ['Moto GP','http://www.shadow-net.org/channels/Moto-GP.html','http://www.shadow-net.org/product_images/b/103/Moto_Gp_logo__65728_thumb.png'],
			 ['Rai 1','http://www.shadow-net.org/channels/Rai-1.html','http://www.shadow-net.org/product_images/m/362/Rai_1_logo__67635_thumb.png'],
			 ['Rai 2','http://www.shadow-net.org/channels/Rai-2.html','http://www.shadow-net.org/product_images/t/148/Rai_2_logo__79173_thumb.png'],
			 ['Rai 3','http://www.shadow-net.org/channels/Rai-3.html','http://www.shadow-net.org/product_images/w/005/Rai_3_logo__60097_thumb.png'],
			 ['Rai 4','http://www.shadow-net.org/channels/Rai-4.html','http://www.shadow-net.org/product_images/o/852/Rai_4_2010__78387_thumb.png'],
			 ['Rai 5','http://www.shadow-net.org/channels/Rai-5.html','http://www.shadow-net.org/product_images/a/799/Rai_5_logo__81811_thumb.png'],
			 ['Rai Movie','http://www.shadow-net.org/channels/Rai-Movie.html','http://www.shadow-net.org/product_images/l/506/RAI_Movie_2010_Logo__63887_thumb.png'],
			 ['RSI La 1','http://www.shadow-net.org/channels/RSI-La-1.html','http://www.shadow-net.org/product_images/i/330/rsi_la1__95748_thumb.jpg'],
			 ['RSI La 2','http://www.shadow-net.org/channels/RSI-La-2.html','http://www.shadow-net.org/product_images/q/536/rsi_la2__31571_thumb.jpg'],
			 ['Sky Calcio','http://www.shadow-net.org/channels/Sky-Calcio.html','http://www.shadow-net.org/product_images/a/134/sky_it_calcio__42011_thumb.png'],
			 ['Sky Sport 1','http://www.shadow-net.org/channels/Sky-Sport-1.html','http://www.shadow-net.org/product_images/z/059/sky_iit_sport1__99735_thumb.jpg'],
			 ['Sky Sport 2','http://www.shadow-net.org/channels/Sky-Sport-2.html','http://www.shadow-net.org/product_images/j/187/sky_iit_sport2__17630_thumb.jpg'],
			 ['Sky Sport 24','http://www.shadow-net.org/channels/Sky-Sport-24.html','http://www.shadow-net.org/product_images/h/134/skysport24italia__08307_thumb.png'],
			 ['Sky TG24','http://www.shadow-net.org/channels/Sky-TG24.html','http://www.shadow-net.org/product_images/u/637/SKY_TG24__09392_thumb.png'],
			 ['Bein Sport 1 FR','http://www.shadow-net.org/channels/Bein-Sport-1-FR.html','http://www.shadow-net.org/product_images/b/770/beinsport-2012_logo_chaine1__77633_thumb.jpg'],
			 ['Bein Sport 3 FR','http://www.shadow-net.org/channels/Bein-Sport-3-FR.html','http://www.shadow-net.org/product_images/s/959/bein_sports3__90672_thumb.png'],
			 ['BFM TV','http://www.shadow-net.org/channels/BFM-TV.html','http://www.shadow-net.org/product_images/j/523/BFMTV__21435_thumb.png'],
			 ['Canal+ Sport','http://www.shadow-net.org/channels/Canal%252b-Sport.html','http://www.shadow-net.org/product_images/l/502/Canal__Sport_logo_2009__01668_thumb.png'],
			 ['Clubbing TV','http://www.shadow-net.org/channels/Clubbing-TV.html','http://www.shadow-net.org/product_images/z/053/Clubbing_TV__57209_thumb.png'],
			 ['Euronews FR','http://www.shadow-net.org/channels/Euronews-FR.html','http://www.shadow-net.org/product_images/f/716/euronews__96297_thumb.jpg'],
			 ['Eurosport France','http://www.shadow-net.org/channels/Eurosport-France.html','http://www.shadow-net.org/product_images/g/221/eurosport__72244_thumb.jpg'],
			 ['FashionTV','http://www.shadow-net.org/channels/FashionTV.html','http://www.shadow-net.org/product_images/f/442/fashion_tv__10290_thumb.jpg'],
			 ['France 2','http://www.shadow-net.org/channels/France-2.html','http://www.shadow-net.org/product_images/y/747/france2__29267_thumb.jpg'],
			 ['France 24 FR','http://www.shadow-net.org/channels/France-24-FR.html','http://www.shadow-net.org/product_images/i/642/FRANCE_24_logo__69539_thumb.png'],
			 ['France 3','http://www.shadow-net.org/channels/France-3.html','http://www.shadow-net.org/product_images/j/518/france3__66917_thumb.jpg'],
			 ['France 4','http://www.shadow-net.org/channels/France-4.html','http://www.shadow-net.org/product_images/z/320/france4__06723_thumb.jpg'],
			 ['France 5','http://www.shadow-net.org/channels/France-5.html','http://www.shadow-net.org/product_images/x/498/france5__26772_thumb.jpg'],
			 ['France Ã”','http://www.shadow-net.org/channels/France-%C3%94.html','http://www.shadow-net.org/product_images/n/983/france_o__96943_thumb.jpg'],
			 ['M6','http://www.shadow-net.org/channels/M6.html','http://www.shadow-net.org/product_images/t/686/m6__79935_thumb.jpg'],
			 ['RTS Deux','http://www.shadow-net.org/channels/RTS-Deux.html','http://www.shadow-net.org/product_images/y/153/rts_deux__51855_thumb.jpg'],
			 ['RTS Un','http://www.shadow-net.org/channels/RTS-Un.html','http://www.shadow-net.org/product_images/y/407/rts_un__92413_thumb.jpg'],
			 ['TF1','http://www.shadow-net.org/channels/TF1.html','http://www.shadow-net.org/product_images/w/668/tf1__68155_thumb.jpg'],
			 ['SRF 1','http://www.shadow-net.org/channels/SRF-1.html','http://www.shadow-net.org/product_images/p/122/srf_1_ch__27802_thumb.jpg'],
			 ['SRF 2','http://www.shadow-net.org/channels/SRF-2.html','http://www.shadow-net.org/product_images/u/790/srf_2_ch__91017_thumb.png'],
			 ['SRF Info','http://www.shadow-net.org/channels/SRF-Info.html','http://www.shadow-net.org/product_images/k/191/srf_info_ch__59722_thumb.jpg'],
			 ['SVT1','http://www.shadow-net.org/channels/SVT1.html','http://www.shadow-net.org/product_images/j/839/svt_1__03141_thumb.jpg'],
			 ['SVT2','http://www.shadow-net.org/channels/SVT2.html','http://www.shadow-net.org/product_images/d/662/svt_2__30340_thumb.jpg'],
			 ['TV4 Sweden','http://www.shadow-net.org/channels/TV4-Sweden.html','http://www.shadow-net.org/product_images/k/588/tv4__72223_thumb.jpg'],
			 ['Al Jazeera Arabic','http://www.shadow-net.org/channels/Al-Jazeera-Arabic.html','http://www.shadow-net.org/product_images/n/253/aljazeera__84338_thumb.png'],
			 ['Al Jazeera Documentary','http://www.shadow-net.org/channels/Al-Jazeera-Documentary.html','http://www.shadow-net.org/product_images/b/160/Al_Jazeera_Documentary_Channel__34510_thumb.png'],
			 ['BBC Arabic','http://www.shadow-net.org/channels/BBC-Arabic.html','http://www.shadow-net.org/product_images/x/782/bbc_arabic__71485_thumb.PNG'],
			 ['Bein Sports 1','http://www.shadow-net.org/channels/Bein-Sports-1.html','http://www.shadow-net.org/product_images/h/891/bein_sports1__51322_thumb.png'],
			 ['Bein Sports 10','http://www.shadow-net.org/channels/Bein-Sports-10.html','http://www.shadow-net.org/product_images/k/284/bein_sports10__25010_thumb.png'],
			 ['Bein Sports 11','http://www.shadow-net.org/channels/Bein-Sports-11.html','http://www.shadow-net.org/product_images/g/582/bein_sports11__25618_thumb.png'],
			 ['Bein Sports 12','http://www.shadow-net.org/channels/Bein-Sports-12.html','http://www.shadow-net.org/product_images/f/600/bein_sports12__01362_thumb.png'],
			 ['Bein Sports 2','http://www.shadow-net.org/channels/Bein-Sports-2.html','http://www.shadow-net.org/product_images/x/414/BeIN_SPORTS_2HD_Couleur__35070_thumb.jpg'],
			 ['Bein Sports 3','http://www.shadow-net.org/channels/Bein-Sports-3.html','http://www.shadow-net.org/product_images/s/745/bein-sports-3-hd_14gzpciv0r55j1l92btw93npju__75859_thumb.png'],
			 ['Bein Sports 4','http://www.shadow-net.org/channels/Bein-Sports-4.html','http://www.shadow-net.org/product_images/g/293/Bein_4__71534_thumb.png'],
			 ['Bein Sports 5','http://www.shadow-net.org/channels/Bein-Sports-5.html','http://www.shadow-net.org/product_images/k/320/bein_sports5__41625_thumb.png'],
			 ['Bein Sports 6','http://www.shadow-net.org/channels/Bein-Sports-6.html','http://www.shadow-net.org/product_images/y/276/bein_sports6__65337_thumb.png'],
			 ['Bein Sports 7','http://www.shadow-net.org/channels/Bein-Sports-7.html','http://www.shadow-net.org/product_images/v/858/bein_sports7__44128_thumb.png'],
			 ['Bein Sports 8','http://www.shadow-net.org/channels/Bein-Sports-8.html','http://www.shadow-net.org/product_images/g/028/bein_sports8__04092_thumb.png'],
			 ['Bein Sports 9','http://www.shadow-net.org/channels/Bein-Sports-9.html','http://www.shadow-net.org/product_images/w/291/bein_sport_9hd__26067_thumb.png'],
			 ['Dubai Racing 2','http://www.shadow-net.org/channels/Dubai-Racing-2.html','http://www.shadow-net.org/product_images/a/902/dubai_ae_racing_2__14904_thumb.png'],
			 ['Dubai Sports','http://www.shadow-net.org/channels/Dubai-Sports.html','http://www.shadow-net.org/product_images/g/112/dubai_sports_1__09676_thumb.jpg'],
			 ['Rotana','http://www.shadow-net.org/channels/Rotana.html','http://www.shadow-net.org/product_images/h/109/rotana__51692_thumb.png'],
			 ['Rotana Aflam','http://www.shadow-net.org/channels/Rotana-Aflam.html','http://www.shadow-net.org/product_images/s/576/rotana-aflam__90584_thumb.jpg'],
			 ['Rotana Cinema','http://www.shadow-net.org/channels/Rotana-Cinema.html','http://www.shadow-net.org/product_images/v/166/rotana_cinema__49210_thumb.png'],
			 ['Sky News Arabia','http://www.shadow-net.org/channels/Sky-News-Arabia.html','http://www.shadow-net.org/product_images/z/091/Sky_News_Arabia_logo__60552_thumb.png'],
			 ['Cartoon Network India','http://www.shadow-net.org/channels/Cartoon-Network-India.html','http://www.shadow-net.org/product_images/c/252/cartoon_network__59462_thumb.jpg'],
			 ['Geo News','http://www.shadow-net.org/channels/Geo-News.html','http://www.shadow-net.org/product_images/a/380/Geo_News_logo__24770_thumb.png'],
			 ['Geo Super','http://www.shadow-net.org/channels/Geo-Super.html','http://www.shadow-net.org/product_images/z/651/Geo_Super_logo__26737_thumb.png'],
			 ['PTV Sports','http://www.shadow-net.org/channels/PTV-Sports.html','http://www.shadow-net.org/product_images/f/847/ptv_sports_pk__13660_thumb.jpg'],
			 ['Sony Six','http://www.shadow-net.org/channels/Sony-Six.html','http://www.shadow-net.org/product_images/l/133/sony_six_in__32068_thumb.jpg'],
			 ['Astro Supersport 1','http://www.shadow-net.org/channels/Astro-Supersport-1.html','http://www.shadow-net.org/product_images/o/658/astro_supersport__73976_thumb.png'],
			 ['Astro Supersport 2','http://www.shadow-net.org/channels/Astro-Supersport-2.html','http://www.shadow-net.org/product_images/m/406/Astro_SuperSport2__81600_thumb.jpg'],
			 ['Astro Supersport 3','http://www.shadow-net.org/channels/Astro-Supersport-3.html','http://www.shadow-net.org/product_images/y/587/Astro_SuperSport_3_logo__27574_thumb.png'],
			 ['Astro Supersport 4','http://www.shadow-net.org/channels/Astro-Supersport-4.html','http://www.shadow-net.org/product_images/i/619/gambar_astro_supersport_4__72673_thumb.JPG'],
			 ['Real Madrid TV','http://www.shadow-net.org/channels/Real-Madrid-TV.html','http://www.shadow-net.org/product_images/u/980/real_madrid_tv_es__39458_thumb.png'],
			 ['BritAsia TV','http://www.shadow-net.org/channels/BritAsia-TV.html','http://www.shadow-net.org/product_images/a/374/brit_asia_tv__34173_thumb.jpg']]		
		Search_name = name
		headers = {"User-Agent": "Mozilla/5.0"}
		result = []
		sources = []
		Freeworld_count = []
		dp =  xbmcgui.DialogProgress()
		result.append('a')
		dp_add = int(ADDON.getSetting('Results')) / float(len(result)) * 100
		HTML = requests.get('http://www.iptvultra.com/',headers=headers).text
		match = re.compile('<span class="link"><a href="(.+?)">(.+?)</a>').findall(HTML)
		dp.create('Checking for stream - '+Search_name)
		dp.update(int(dp_add),'You can always cancel if you\'re happy with results',str(len(result)-1)+'/'+str(int(ADDON.getSetting('Results')))+' Results')
		if ADDON.getSetting('Live_Online')=='true':
			dp.update(int(dp_add),'Checking Live Online',str(len(result)-1)+'/'+str(int(ADDON.getSetting('Results')))+' Results')
			if int(len(result)-1)<= int(ADDON.getSetting('Results')):		
				for thing in liveonline:
					name = thing[0]
					url = sports+thing[1]
					if (Search_name).replace(' ','').replace('sports','sport') in (name).lower().replace(' ','').replace('sports','sport'):
						if int(len(result)-1)<= int(ADDON.getSetting('Results')):		
							result.append(url[0])
							process.PLAY('LiveOnline | '+name,url,906,'','','','')
			else:
				pass
		if ADDON.getSetting('Shadow')=='true':
			dp.update(int(dp_add),'Checking Shadow',str(len(result)-1)+'/'+str(int(ADDON.getSetting('Results')))+' Results')
			if int(len(result)-1)<= int(ADDON.getSetting('Results')):
				for item in shadow:
					name = item[0]
					url = item[1]
					image = item[2]
					if (Search_name).replace(' ','').replace('sports','sport') in (name).lower().replace(' ','').replace('sports','sport'):
						if int(len(result)-1)<= int(ADDON.getSetting('Results')):		
							result.append(url[0])
							process.PLAY('Shadow | '+name,url,22,image,'','','')
			else:
				pass
		if ADDON.getSetting('Freeview')=='true':
			dp.update(int(dp_add),'Checking Freeview',str(len(result)-1)+'/'+str(int(ADDON.getSetting('Results')))+' Results')
			if int(len(result)-1)<= int(ADDON.getSetting('Results')):
				for object in freeview:
					playlink = object[1]
					name = object[0]
					playlink = object[1]
					mode = object [2]
					if (Search_name).replace(' ','').replace('sports','sport') in (name).lower().replace(' ','').replace('sports','sport'):
						if int(len(result)-1)<= int(ADDON.getSetting('Results')):		
							result.append(playlink[0])
							try:
								from freeview import freeview
								freeview.addLink('Freeview | '+name,playlink,mode,'')
							except:
								pass
			else:
				pass
		if ADDON.getSetting('Mama_HD')=='true':
			dp.update(int(dp_add),'Checking Mama HD',str(len(result)-1)+'/'+str(int(ADDON.getSetting('Results')))+' Results')
			if int(len(result)-1)<= int(ADDON.getSetting('Results')):
				for list_item in mamahd:
					link = list_item[0]
					name = list_item[1]
					if (Search_name).replace(' ','').replace('sports','sport') in (name).lower().replace(' ','').replace('sports','sport'):
						if int(len(result)-1)<= int(ADDON.getSetting('Results')):		
							result.append(url[0])
							process.PLAY('Mama Hd | '+name,sports+link,906,'','','','')
			else:
				pass
		if ADDON.getSetting('Freeworld')=='true':
			if int(len(result)-1)<= int(ADDON.getSetting('Results')):		
				HTML6 = process.OPEN_URL('http://freeworldwideiptv.com/')
				match6 = re.compile('<h2 class="title">.+?<a href="(.+?)"',re.DOTALL).findall(HTML6)
				for URL in match6:
					dp.update(int(dp_add),'Checking Freeworld '+str(len(Freeworld_count))+'/'+str(len(match6)),str(len(result)-1)+'/'+str(int(ADDON.getSetting('Results')))+' Results')
					Freeworld_count.append(URL[0])
					HTML7 = requests.get(URL.replace('https','http')).content
					match7 = re.compile('EXTINF:.+?,(.+?)\n(.+?)\n#').findall(HTML7)
					for final_name,fin_url in match7:
						if (Search_name).replace(' ','').replace('sports','sport') in (final_name).lower().replace(' ','').replace('sports','sport'):
							if int(len(result)-1)<= int(ADDON.getSetting('Results')):		
								result.append(fin_url[0])
								fin_url = f4murl+fin_url
								process.PLAY('Freeworld | '+final_name,fin_url,906,'','','','')
			else:
				pass
		if ADDON.getSetting('IPTVsat')=='true':
			dp.update(int(dp_add),'Checking IPTVsat',str(len(result)-1)+'/'+str(int(ADDON.getSetting('Results')))+' Results')
			if int(len(result)-1)<= int(ADDON.getSetting('Results')):
				HTML2 = process.OPEN_URL('http://www.iptvsat.com/')
				match2 = re.compile("<h2 class='post-title entry-title.+?<a href='(.+?)'>(.+?)</a>",re.DOTALL).findall(HTML2)
				for url,name in match2:
					HTML3 = process.OPEN_URL(url)
					match3 = re.compile('#EXTINF:-1,(.+?)</h4>\n<h4 style="clear: both; text-align: center;">\n(.+?)</h4>').findall(HTML3)
					for name2,url2 in match3:
						if (Search_name).replace(' ','').replace('sports','sport') in (name2).lower().replace(' ','').replace('sports','sport'):
							result.append(url[0])
							process.PLAY('IPTVSat | '+name2,f4murl+link,906,'','','','')
			else:
				pass
		if ADDON.getSetting('IPTVUrl')=='true':
			dp.update(int(dp_add),'Checking IPTVUrl',str(len(result)-1)+'/'+str(int(ADDON.getSetting('Results')))+' Results')
			if int(len(result)-1)<= int(ADDON.getSetting('Results')):
				HTML4 = process.OPEN_URL('http://www.iptvurllist.com/')
				match4 = re.compile('<h1><a href="(.+?)">').findall(HTML4)
				for new_url in match4:
					fin_url = 'http://www.iptvurllist.com/'+new_url
					HTML5 = process.OPEN_URL(fin_url)
					match5 = re.compile('EXTINF:.+?,(.+?)\n(.+?)\n').findall(HTML5)
					for name,url5 in match5:
						if (Search_name).replace(' ','').replace('sports','sport') in (name).lower().replace(' ','').replace('sports','sport'):
							result.append(url[0])
							process.PLAY('IPTVUrl | '+name,f4murl+url5,906,'','','','')
			else:
				pass
		if ADDON.getSetting('Ingenious')=='true':
			for url, name in match:
				try:
					sources.append(url[0])
					if int(len(sources))<= int(ADDON.getSetting('Sources')) and int(len(result)-1)<= int(ADDON.getSetting('Results')):
						dp.update(int(dp_add),'Checking Ingenious list '+str(len(sources))+'/'+str(int(ADDON.getSetting('Sources'))),str(len(result))+'/'+str(int(ADDON.getSetting('Results')))+' Results')
						if dp.iscanceled():
							return
						HTML2 = requests.get(url,headers=headers).text
						match2 = re.compile('".+?[@](.+?)[@].+?[@].+?[@](.+?)"').findall(HTML2)
						for name,url2 in match2:
							name = name.replace('[','').replace(']','')
							if name[0] == ' ':
								name = name[1:]
							elif name[-1] == ' ':
								name = name[:-1]
							playlink = 'plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&amp;url='+url2.replace('[','').replace(']','')+';name=vendetta'
							if (Search_name).replace(' ','').replace('sports','sport') in (name).lower().replace(' ','').replace('sports','sport'):
								result.append(url[0])
								try:
									process.PLAY('Ingenious | '+name,playlink,906,'','','','')
								except:
									pass
					else:
						pass
				except:
					pass

				