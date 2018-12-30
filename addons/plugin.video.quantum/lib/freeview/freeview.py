'''This section was kindly donated by the dev of the addon - RayW1986, give him a follow on twitter to say thanks for this amazing section - @raywilson1986'''



import urllib,urllib2,re,xbmcplugin,xbmcgui,os,sys,datetime,string,hashlib,net,xbmc,process
import plugintools
import xbmcaddon
import liveresolver
import xbmcaddon
from cookielib import CookieJar

net = net.Net()
USERDATA_PATH = xbmc.translatePath('special://home/userdata/addon_data')
ADDON_DATA = USERDATA_PATH + '/quantum/'
ADDON = xbmcaddon.Addon(id='plugin.video.quantum')
addon_id = xbmcaddon.Addon().getAddonInfo('id')
selfAddon = xbmcaddon.Addon(id=addon_id)
logos = 'http://herovision.x10host.com/freeview/'
icon = logos + 'freeview.png'
fanart = xbmc.translatePath('special://home/addons/plugin.video.quantum/fanart.jpg')
logos_tvp = 'https://assets.tvplayer.com/common/logos/256/Inverted/'
favourites = ADDON_DATA + 'favourites'
if os.path.exists(favourites)==True:
    FAV = open(favourites).read()
else: FAV = []

def CATEGORIES():
	if selfAddon.getSetting('list_all') == 'true':  
		addLink('4Music | Direct','http://llnw.live.btv.simplestream.com/coder9/coder.channels.channel6/hls/4/playlist.m3u8',1201,logos_tvp+'128.png')
		addLink('4Music | TVPlayer','128',1202,logos_tvp+'128.png')
		addLink('5* | FilmOn','https://www.filmon.com/tv/5-star',1201,logos+'5star.png')
		addLink('5USA | FilmOn','https://www.filmon.com/tv/5usa',1201,logos+'5usa.png')
		addLink('Al Jazeera | TVPlayer','146',1202,logos_tvp+'146.png')
		addLink('Al Jazeera | FilmOn','https://www.filmon.com/tv/al-jazeera',1201,logos_tvp+'146.png')
		addLink('BBC Alba | TVPlayer','236',1202,logos_tvp+'236.png')
		addLink('BBC Alba | BBC iPlayer','http://vs-hls-uk-live.edgesuite.net/pool_1/live/bbc_alba/bbc_alba.isml/bbc_alba-pa3%3d96000-video%3d1604032.norewind.m3u8',1201,logos_tvp+'236.png')
		addLink('BBC Four HD | BBC iPlayer','http://vs-hls-uk-live.akamaized.net/pool_33/live/bbc_four_hd/bbc_four_hd.isml/bbc_four_hd-pa4%3d128000-video%3d5070016.m3u8',1201,logos_tvp+'110.png')
		addLink('BBC Four | TVPlayer','110',1202,logos_tvp+'110.png')
		addLink('BBC Four | FilmOn','https://www.filmon.com/tv/cbeebiesbbc-four',1201,logos_tvp+'110.png')
		addLink('BBC News HD | BBC iPlayer','http://vs-hls-uk-live.edgesuite.net/pool_34/live/bbc_news_channel_hd/bbc_news_channel_hd.isml/bbc_news_channel_hd-pa4%3d128000-video%3d5070016.m3u8',1201,logos_tvp+'111.png')
		addLink('BBC News | TVPlayer','111',1202,logos_tvp+'111.png')
		addLink('BBC News | FilmOn','https://www.filmon.com/tv/bbc-news',1201,logos_tvp+'111.png')
		addLink('BBC One HD | BBC iPlayer','http://vs-hls-uk-live.akamaized.net/pool_30/live/bbc_one_hd/bbc_one_hd.isml/bbc_one_hd-pa4%3d128000-video%3d5070016.m3u8',1201,logos_tvp+'89.png')
		addLink('BBC One | TVPlayer','89',1202,logos_tvp+'89.png')
		addLink('BBC One | FilmOn','https://www.filmon.com/tv/bbc-one',1201,logos_tvp+'89.png')
		addLink('BBC One Northern Ireland | BBC iPlayer','http://vs-hls-uk-live.edgesuite.net/pool_4/live/bbc_one_northern_ireland_hd/bbc_one_northern_ireland_hd.isml/bbc_one_northern_ireland_hd-pa4%3d128000-video%3d5070016.m3u8',1201,logos_tvp+'89.png')
		addLink('BBC One Northern Ireland | FilmOn','https://www.filmon.com/tv/bbc-1-north-ireland',1201,logos_tvp+'89.png')
		addLink('BBC One Scotland | BBC iPlayer','http://vs-hls-uk-live.edgesuite.net/pool_5/live/bbc_one_scotland_hd/bbc_one_scotland_hd.isml/bbc_one_scotland_hd-pa4%3d128000-video%3d5070016.m3u8',1201,logos_tvp+'89.png')
		addLink('BBC One Scotland | FilmOn','https://www.filmon.com/tv/bbc-1-scotland',1201,logos_tvp+'89.png')
		addLink('BBC One Wales | BBC iPlayer','http://vs-hls-uk-live.edgesuite.net/pool_3/live/bbc_one_wales_hd/bbc_one_wales_hd.isml/bbc_one_wales_hd-pa4%3d128000-video%3d5070016.m3u8',1201,logos_tvp+'89.png')
		addLink('BBC One Wales | FilmOn','https://www.filmon.com/tv/bbc-1-wales',1201,logos_tvp+'89.png')
		addLink('BBC Two Northern Ireland | BBC iPlayer','http://vs-hls-uk-live.edgesuite.net/pool_5/live/bbc_two_northern_ireland_digital/bbc_two_northern_ireland_digital.isml/bbc_two_northern_ireland_digital-pa3%3d96000-video%3d1604032.norewind.m3u8',1201,logos_tvp+'90.png')
		addLink('BBC Two Scotland | BBC iPlayer','http://vs-hls-uk-live.edgesuite.net/pool_5/live/bbc_two_scotland/bbc_two_scotland.isml/bbc_two_scotland-pa3%3d96000-video%3d1604032.norewind.m3u8',1201,logos_tvp+'90.png')
		addLink('BBC Two Wales | BBC iPlayer','http://vs-hls-uk-live.edgesuite.net/pool_5/live/bbc_two_wales_digital/bbc_two_wales_digital.isml/bbc_two_wales_digital-pa3%3d96000-video%3d1604032.norewind.m3u8',1201,logos_tvp+'90.png')
		addLink('BBC Parliament | BBC iPlayer','http://vs-hls-uk-live.edgesuite.net/pool_1/live/bbc_parliament/bbc_parliament.isml/bbc_parliament-pa3%3d96000-video%3d1604032.norewind.m3u8',1201,logos_tvp+'345.png')
		addLink('BBC Parliament | TVPlayer','345',1202,logos_tvp+'345.png')
		addLink('BBC Parliament | FilmOn','https://www.filmon.com/tv/bbc-parliament',1201,logos_tvp+'345.png')
		addLink('BBC Two HD | BBC iPlayer','http://vs-hls-uk-live.edgesuite.net/pool_31/live/bbc_two_hd/bbc_two_hd.isml/bbc_two_hd-pa4%3d128000-video%3d5070016.m3u8',1201,logos_tvp+'90.png')
		addLink('BBC Two | TVPlayer','90',1202,logos_tvp+'90.png')
		addLink('BBC Two | FilmOn','https://www.filmon.com/tv/bbc-two',1201,logos_tvp+'90.png')
		addLink('Bloomberg | TVPlayer','514',1202,logos_tvp+'514.png')
		addLink('Bloomberg | FilmOn','https://www.filmon.com/tv/bloomberg',1201,logos_tvp+'514.png')
		addLink('The Box | Direct','http://llnw.live.btv.simplestream.com/coder9/coder.channels.channel12/hls/4/playlist.m3u8',1201,logos_tvp+'129.png')
		addLink('The Box | TVPlayer','129',1202,logos_tvp+'129.png')
		addLink('Box Hits | Direct','http://llnw.live.btv.simplestream.com/coder9/coder.channels.channel2/hls/4/playlist.m3u8',1201,logos_tvp+'158.png')
		addLink('Box Hits | TVPlayer','130',1202,logos_tvp+'130.png')
		addLink('Box Upfront | Direct','http://llnw.live.btv.simplestream.com/coder9/coder.channels.channel8/hls/4/playlist.m3u8',1201,logos_tvp+'158.png')
		addLink('Box Upfront | TVPlayer','158',1202,logos_tvp+'158.png')
		addLink('Capital TV | Direct','http://ooyalahd2-f.akamaihd.net/i/globalradio01_delivery@156521/index_656_av-p.m3u8?sd=10&rebase=on',1201,logos_tvp+'157.png')
		addLink('Capital TV | TVPlayer','157',1202,logos_tvp+'157.png')
		addLink('CBBC HD | BBC iPlayer','http://vs-hls-uk-live.edgesuite.net/pool_1/live/cbbc_hd/cbbc_hd.isml/cbbc_hd-pa4%3d128000-video%3d5070016.m3u8',1201,logos_tvp+'113.png')
		addLink('CBBC | TVPlayer','113',1202,logos_tvp+'113.png')
		addLink('CBBC | FilmOn','https://www.filmon.com/tv/cbbc',1201,logos_tvp+'113.png')
		addLink('CBeebies HD | BBC iPlayer','http://vs-hls-uk-live.edgesuite.net/pool_2/live/cbeebies_hd/cbeebies_hd.isml/cbeebies_hd-pa4%3d128000-video%3d5070016.m3u8',1201,logos_tvp+'114.png')
		addLink('CBeebies | TVPlayer','114',1202,logos_tvp+'114.png')
		addLink('CBeebies | FilmOn','https://www.filmon.com/tv/cbeebies',1201,logos_tvp+'114.png')
		addLink('CBS Action | FilmOn','https://www.filmon.com/tv/cbs-action',1201,logos+'cbsaction.png')
		addLink('CBS Drama | FilmOn','https://www.filmon.com/tv/cbs-drama',1201,logos+'cbsdrama.png')
		addLink('CBS Reality | FilmOn','https://www.filmon.com/tv/cbs-reality',1201,logos+'cbsreality.png')
		addLink('CBS Reality+1 | FilmOn','https://www.filmon.com/tv/cbs-reality1',1201,logos+'cbsreality.png')
		addLink('Channel 4 | TVPlayer','92',1202,logos_tvp+'92.png')
		addLink('Channel 4 | FilmOn','https://www.filmon.com/tv/channel-4',1201,logos_tvp+'92.png')
		addLink('Channel 5 | TVPlayer','93',1202,logos_tvp+'93.png')
		addLink('Channel 5 | FilmOn','https://www.filmon.com/tv/channel-5',1201,logos_tvp+'93.png')
		addLink('Channel AKA | Direct','http://rrr.sz.xlcdn.com/?account=AATW&file=akanew&type=live&service=wowza&protocol=http&output=playlist.m3u8',1201,logos_tvp+'227.png')
		addLink('Channel AKA | TVPlayer','227',1202,logos_tvp+'227.png')
		addLink('Chilled | TVPlayer','226',1202,logos_tvp+'226.png')
		addLink('CITV | ITV Hub','http://citvliveios-i.akamaihd.net/hls/live/207267/itvlive/CITVMN/master_Main1800.m3u8',1201,logos+'citv.png')
		addLink('Clubbing TV | FilmOn','https://www.filmon.com/tv/clubbing-tv',1201,logos+'clubbingtv.png')
		addLink('Clubland | TVPlayer','225',1202,logos_tvp+'225.png')
		addLink('CNN International | TVPlayer','286',1202,logos_tvp+'286.png')
		addLink('Community Channel | TVPlayer','259',1202,logos_tvp+'259.png')
		addLink('The Craft Channel | TVPlayer','554',1202,logos_tvp+'554.png')
		addLink('Dave | TVPlayer','300',1202,logos_tvp+'300.png')
		addLink('Dave ja vu | TVPlayer','317',1202,logos_tvp+'317.png')
		addLink('Drama | TVPlayer','346',1202,logos_tvp+'346.png')
		addLink('E4 | FilmOn','https://www.filmon.com/tv/e4',1201,logos+'e4.png')
		addLink('Film4 | FilmOn','https://www.filmon.com/tv/film-4',1201,logos+'film4.png')
		addLink('Food Network | TVPlayer','125',1202,logos_tvp+'125.png')
		addLink('Food Network | FilmOn','http://www.filmon.com/tv/food-network',1201,logos_tvp+'125.png')
		addLink('Food Network+1 | TVPlayer','254',1202,logos_tvp+'254.png')
		addLink('Food Network+1 | FilmOn','http://www.filmon.com/tv/food-network-plus-1',1201,logos_tvp+'254.png')
		addLink('Forces TV | TVPlayer','555',1202,logos_tvp+'555.png')
		addLink('Heart TV | Direct','http://ooyalahd2-f.akamaihd.net/i/globalradio02_delivery@156522/master.m3u8',1201,logos_tvp+'153.png')
		addLink('Heart TV | TVPlayer','153',1202,logos_tvp+'153.png')
		addLink('Home | TVPlayer','512',1202,logos_tvp+'512.png')
		addLink('Horror Channel | FilmOn','https://www.filmon.com/tv/horror-channel',1201,logos+'horrorchannel.png')
		addLink('ITV1 | ITV Hub','http://itv1liveios-i.akamaihd.net/hls/live/203437/itvlive/ITV1MN/master_Main1800.m3u8',1201,logos_tvp+'204.png')
		addLink('ITV1 | TVPlayer','204',1202,logos_tvp+'204.png')
		addLink('ITV1 | FilmOn','http://www.filmon.com/tv/itv1',1201,logos_tvp+'204.png')
		addLink('ITV1+1 | FilmOn','https://www.filmon.com/tv/itv-plus-1',1201,logos_tvp+'204.png')
		addLink('ITV2 | ITV Hub','http://itv2liveios-i.akamaihd.net/hls/live/203495/itvlive/ITV2MN/master_Main1800.m3u8',1201,logos+'itv2.png')
		addLink('ITV2 | FilmOn','http://www.filmon.com/tv/itv2',1201,logos+'itv2.png')
		addLink('ITV2+1 | FilmOn','https://www.filmon.com/tv/itv2-plus-1',1201,logos+'itv2.png')
		addLink('ITV3 | ITV Hub','http://itv3liveios-i.akamaihd.net/hls/live/207262/itvlive/ITV3MN/master_Main1800.m3u8',1201,logos+'itv3.png')
		addLink('ITV3 | FilmOn','http://www.filmon.com/tv/itv3',1201,logos+'itv3.png')
		addLink('ITV3+1 | FilmOn','https://www.filmon.com/tv/itv3-plus-1',1201,logos+'itv3.png')
		addLink('ITV4 | ITV Hub','http://itv4liveios-i.akamaihd.net/hls/live/207266/itvlive/ITV4MN/master_Main1800.m3u8',1201,logos+'itv4.png')
		addLink('ITV4 | FilmOn','http://www.filmon.com/tv/itv4',1201,logos+'itv4.png')
		addLink('ITV4+1 | FilmOn','https://www.filmon.com/tv/itv4-plus-1',1201,logos+'itv4.png')
		addLink('ITVBe | ITV Hub','http://itvbeliveios-i.akamaihd.net/hls/live/219078/itvlive/ITVBE/master_Main1800.m3u8',1201,logos+'itvbe.png')
		addLink('ITVBe | FilmOn','http://www.filmon.com/tv/itvbe',1201,logos+'itvbe.png')
		addLink('The Jewellery Channel | Direct','https://d2hee8qk5g0egz.cloudfront.net/live/tjc_sdi1/bitrate1.isml/bitrate1-audio_track=64000-video=1800000.m3u8',1201,logos_tvp+'545.png')
		addLink('The Jewellery Channel | TVPlayer','545',1202,logos_tvp+'545.png')
		addLink('Keep It Country | TVPlayer','569',1202,logos_tvp+'569.png')
		addLink('Kerrang! | Direct','http://llnw.live.btv.simplestream.com/coder11/coder.channels.channel4/hls/4/playlist.m3u8',1201,logos_tvp+'133.png')
		addLink('Kerrang! | TVPlayer','133',1202,logos_tvp+'133.png')
		addLink('Kiss | Direct','http://llnw.live.btv.simplestream.com/coder9/coder.channels.channel14/hls/4/playlist.m3u8',1201,logos_tvp+'131.png')
		addLink('Kiss | TVPlayer','131',1202,logos_tvp+'131.png')
		addLink('Kix! | FilmOn','https://www.filmon.com/tv/kix',1201,logos+'kix.png')
		addLink('London Live | Direct','http://bcoveliveios-i.akamaihd.net/hls/live/217434/3083279840001/master_900.m3u8',1201,logos+'londonlive.png')
		addLink('Magic | Direct','http://llnw.live.btv.simplestream.com/coder11/coder.channels.channel2/hls/4/playlist.m3u8',1201,logos_tvp+'132.png')
		addLink('Magic | TVPlayer','132',1202,logos_tvp+'132.png')
		addLink('More4 | FilmOn','https://www.filmon.com/tv/more4',1201,logos+'more4.png')
		addLink('NOW Music | Direct','http://rrr.sz.xlcdn.com/?account=AATW&file=nowmusic&type=live&service=wowza&protocol=http&output=playlist.m3u8',1201,logos_tvp+'228.png')
		addLink('NOW Music | TVPlayer','228',1202,logos_tvp+'228.png')
		addLink('POP | FilmOn','https://www.filmon.com/tv/pop',1201,logos+'pop.png')
		addLink('Pick | FilmOn','https://www.filmon.com/tv/pick-tv',1201,logos+'pick.png')
		addLink('QUEST | TVPlayer','327',1202,logos_tvp+'327.png')
		addLink('QUEST | FilmOn','http://www.filmon.tv/tv/quest',1201,logos_tvp+'327.png')
		addLink('QUEST+1 | TVPlayer','336',1202,logos_tvp+'336.png')
		addLink('QVC Beauty | TVPlayer','250',1202,logos_tvp+'250.png')
		addLink('QVC Extra | TVPlayer','248',1202,logos_tvp+'248.png')
		addLink('QVC Plus | TVPlayer','344',1202,logos_tvp+'344.png')
		addLink('QVC Style | TVPlayer','249',1202,logos_tvp+'249.png')
		addLink('QVC | TVPlayer','247',1202,logos_tvp+'247.png')
		addLink('Really | TVPlayer','306',1202,logos_tvp+'306.png')
		addLink('Really | FilmOn','http://www.filmon.tv/tv/really',1201,logos_tvp+'306.png')
		addLink('S4C | BBC iPlayer','http://vs-hls-uk-live.edgesuite.net/pool_9/live/s4cpbs/s4cpbs.isml/s4cpbs-pa3%3d96000-video%3d1604032.norewind.m3u8',1201,logos_tvp+'251.png')
		addLink('S4C | TVPlayer','251',1202,logos_tvp+'251.png')
		addLink('Sky News | YouTube','https://www.youtube.com/watch?v=y60wDzZt8yg',1201,logos+'skynews.png')
		addLink('Tiny Pop | FilmOn','https://www.filmon.com/tv/tiny-pop',1201,logos+'tinypop.png')
		addLink('Travel Channel | TVPlayer','126',1202,logos_tvp+'126.png')
		addLink('Travel Channel+1 | TVPlayer','255',1202,logos_tvp+'255.png')
		addLink('Travel Channel+1 | FilmOn','http://www.filmon.tv/tv/travel-channel1',1201,logos_tvp+'255.png')
		addLink('Yesterday | TVPlayer','308',1202,logos_tvp+'308.png')
		addLink('Yesterday | FilmOn','http://www.filmon.tv/tv/yesterday',1201,logos_tvp+'308.png')
		addLink('Yesterday+1 | TVPlayer','318',1202,logos_tvp+'318.png')
		addLink('truTV | Direct','http://llnw.live.btv.simplestream.com/coder5/coder.channels.channel2/hls/4/playlist.m3u8',1201,logos_tvp+'295.png')
		addLink('truTV | TVPlayer','295',1202,logos_tvp+'295.png')
		addLink('truTV | FilmOn','http://www.filmon.tv/tv/tru-tv',1201,logos_tvp+'295.png')
		addLink('Blaze | Direct','http://live.blaze.simplestreamcdn.com/live/blaze/bitrate1.isml/bitrate1-audio_track=64000-video=3500000.m3u8',1201,logos+'blaze.png')
		xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)
		xbmcplugin.endOfDirectory(int(sys.argv[1]))

	else:
		#4Music
		if selfAddon.getSetting('four_music') == 'Direct': addLink('4Music','http://llnw.live.btv.simplestream.com/coder9/coder.channels.channel6/hls/4/playlist.m3u8',1201,logos_tvp+'128.png')
		if selfAddon.getSetting('four_music') == 'TVPlayer': addLink('4Music','128',1202,logos_tvp+'128.png')
		
		#5*
		if selfAddon.getSetting('five_star') == 'FilmOn': addLink('5*','https://www.filmon.com/tv/5-star',1201,logos+'5star.png')
		
		#5USA
		if selfAddon.getSetting('five_usa') == 'FilmOn': addLink('5USA','https://www.filmon.com/tv/5usa',1201,logos+'5usa.png')
		
		#Al Jazeera
		if selfAddon.getSetting('al_jazeera') == 'TVPlayer': addLink('Al Jazeera','146',1202,logos_tvp+'146.png')
		if selfAddon.getSetting('al_jazeera') == 'FilmOn': addLink('Al Jazeera','https://www.filmon.com/tv/al-jazeera',1201,logos_tvp+'146.png')
		
		#BBC ALBA
		if selfAddon.getSetting('bbc_alba') == 'TVPlayer': addLink('BBC Alba','236',1202,logos_tvp+'236.png')
		if selfAddon.getSetting('bbc_alba') == 'BBC iPlayer': addLink('BBC Alba','http://vs-hls-uk-live.edgesuite.net/pool_1/live/bbc_alba/bbc_alba.isml/bbc_alba-pa3%3d96000-video%3d1604032.norewind.m3u8',1201,logos_tvp+'236.png')
		
		#BBC Four
		if selfAddon.getSetting('bbc_four') == 'BBC iPlayer': addLink('BBC Four HD','http://vs-hls-uk-live.akamaized.net/pool_33/live/bbc_four_hd/bbc_four_hd.isml/bbc_four_hd-pa4%3d128000-video%3d5070016.m3u8',1201,logos_tvp+'110.png')
		if selfAddon.getSetting('bbc_four') == 'TVPlayer': addLink('BBC Four','110',1202,logos_tvp+'110.png')
		if selfAddon.getSetting('bbc_four') == 'FilmOn': addLink('BBC Four','https://www.filmon.com/tv/cbeebiesbbc-four',1201,logos_tvp+'110.png')
		
		#BBC News
		if selfAddon.getSetting('bbc_news') == 'BBC iPlayer': addLink('BBC News HD','http://vs-hls-uk-live.edgesuite.net/pool_34/live/bbc_news_channel_hd/bbc_news_channel_hd.isml/bbc_news_channel_hd-pa4%3d128000-video%3d5070016.m3u8',1201,logos_tvp+'111.png')
		if selfAddon.getSetting('bbc_news') == 'TVPlayer': addLink('BBC News','111',1202,logos_tvp+'111.png')
		if selfAddon.getSetting('bbc_news') == 'FilmOn': addLink('BBC News','https://www.filmon.com/tv/bbc-news',1201,logos_tvp+'111.png')
		
		#BBC One
		if selfAddon.getSetting('bbc_one') == 'BBC iPlayer': addLink('BBC One HD','http://vs-hls-uk-live.akamaized.net/pool_30/live/bbc_one_hd/bbc_one_hd.isml/bbc_one_hd-pa4%3d128000-video%3d5070016.m3u8',1201,logos_tvp+'89.png')
		if selfAddon.getSetting('bbc_one') == 'TVPlayer': addLink('BBC One','89',1202,logos_tvp+'89.png')
		if selfAddon.getSetting('bbc_one') == 'FilmOn': addLink('BBC One','https://www.filmon.com/tv/bbc-one',1201,logos_tvp+'89.png')
		
		#BBC One Northern Ireland
		if selfAddon.getSetting('bbc_one_ni') == 'BBC iPlayer': addLink('BBC One Northern Ireland','http://vs-hls-uk-live.edgesuite.net/pool_4/live/bbc_one_northern_ireland_hd/bbc_one_northern_ireland_hd.isml/bbc_one_northern_ireland_hd-pa4%3d128000-video%3d5070016.m3u8',1201,logos_tvp+'89.png')
		if selfAddon.getSetting('bbc_one_ni') == 'FilmOn': addLink('BBC One Northern Ireland','https://www.filmon.com/tv/bbc-1-north-ireland',1201,logos_tvp+'89.png')
		
		#BBC Scotland
		if selfAddon.getSetting('bbc_one_scotland') == 'BBC iPlayer': addLink('BBC One Scotland','http://vs-hls-uk-live.edgesuite.net/pool_5/live/bbc_one_scotland_hd/bbc_one_scotland_hd.isml/bbc_one_scotland_hd-pa4%3d128000-video%3d5070016.m3u8',1201,logos_tvp+'89.png')
		if selfAddon.getSetting('bbc_one_scotland') == 'FilmOn': addLink('BBC Scotland','https://www.filmon.com/tv/bbc-1-scotland',1201,logos_tvp+'89.png')
		
		#BBC One Wales
		if selfAddon.getSetting('bbc_one_wales') == 'BBC iPlayer': addLink('BBC One Wales','http://vs-hls-uk-live.edgesuite.net/pool_3/live/bbc_one_wales_hd/bbc_one_wales_hd.isml/bbc_one_wales_hd-pa4%3d128000-video%3d5070016.m3u8',1201,logos_tvp+'89.png')
		if selfAddon.getSetting('bbc_one_wales') == 'FilmOn': addLink('BBC One Wales','https://www.filmon.com/tv/bbc-1-wales',1201,logos_tvp+'89.png')
		
		#BBC Two Northern Ireland
		if selfAddon.getSetting('bbc_two_ni') == 'BBC iPlayer': addLink('BBC Two Northern Ireland','http://vs-hls-uk-live.edgesuite.net/pool_5/live/bbc_two_northern_ireland_digital/bbc_two_northern_ireland_digital.isml/bbc_two_northern_ireland_digital-pa3%3d96000-video%3d1604032.norewind.m3u8',1201,logos_tvp+'90.png')
		
		#BBC Two Scotland
		if selfAddon.getSetting('bbc_two_scotland') == 'BBC iPlayer': addLink('BBC Two Scotland','http://vs-hls-uk-live.edgesuite.net/pool_5/live/bbc_two_scotland/bbc_two_scotland.isml/bbc_two_scotland-pa3%3d96000-video%3d1604032.norewind.m3u8',1201,logos_tvp+'90.png')
		
		#BBC Two Wales
		if selfAddon.getSetting('bbc_two_wales') == 'BBC iPlayer': addLink('BBC Two Wales','http://vs-hls-uk-live.edgesuite.net/pool_5/live/bbc_two_wales_digital/bbc_two_wales_digital.isml/bbc_two_wales_digital-pa3%3d96000-video%3d1604032.norewind.m3u8',1201,logos_tvp+'90.png')
		
		#BBC Parliament
		if selfAddon.getSetting('bbc_par') == 'BBC iPlayer': addLink('BBC Parliament','http://vs-hls-uk-live.edgesuite.net/pool_1/live/bbc_parliament/bbc_parliament.isml/bbc_parliament-pa3%3d96000-video%3d1604032.norewind.m3u8',1201,logos_tvp+'345.png')
		if selfAddon.getSetting('bbc_par') == 'TVPlayer': addLink('BBC Parliament','345',1202,logos_tvp+'345.png')
		if selfAddon.getSetting('bbc_par') == 'FilmOn': addLink('BBC Parliament','https://www.filmon.com/tv/bbc-parliament',1201,logos_tvp+'345.png')
		
		#BBC Two
		if selfAddon.getSetting('bbc_two') == 'BBC iPlayer': addLink('BBC Two HD','http://vs-hls-uk-live.edgesuite.net/pool_31/live/bbc_two_hd/bbc_two_hd.isml/bbc_two_hd-pa4%3d128000-video%3d5070016.m3u8',1201,logos_tvp+'90.png')
		if selfAddon.getSetting('bbc_two') == 'TVPlayer': addLink('BBC Two','90',1202,logos_tvp+'90.png')
		if selfAddon.getSetting('bbc_two') == 'FilmOn': addLink('BBC Two','https://www.filmon.com/tv/bbc-two',1201,logos_tvp+'90.png')
		
		#Blaze
		if selfAddon.getSetting('blaze') == 'Direct': addLink('Blaze','http://live.blaze.simplestreamcdn.com/live/blaze/bitrate1.isml/bitrate1-audio_track=64000-video=3500000.m3u8',1201,logos+'blaze.png')

		#Bloomberg
		if selfAddon.getSetting('bloomberg') == 'TVPlayer': addLink('Bloomberg','514',1202,logos_tvp+'514.png')
		if selfAddon.getSetting('bloomberg') == 'FilmOn': addLink('Bloomberg','https://www.filmon.com/tv/bloomberg',1201,logos_tvp+'514.png')
		
		#The Box
		if selfAddon.getSetting('the_box') == 'Direct': addLink('The Box','http://llnw.live.btv.simplestream.com/coder9/coder.channels.channel12/hls/4/playlist.m3u8',1201,logos_tvp+'129.png')
		if selfAddon.getSetting('the_box') == 'TVPlayer': addLink('The Box','129',1202,logos_tvp+'129.png')
		
		#Box Hits
		if selfAddon.getSetting('box_hits') == 'Direct': addLink('Box Hits','http://llnw.live.btv.simplestream.com/coder9/coder.channels.channel2/hls/4/playlist.m3u8',1201,logos_tvp+'130.png')
		if selfAddon.getSetting('box_hits') == 'TVPlayer': addLink('Box Hits','130',1202,logos_tvp+'130.png')
		
		#Box Upfront
		if selfAddon.getSetting('box_up') == 'Direct': addLink('Box Upfront','http://llnw.live.btv.simplestream.com/coder9/coder.channels.channel8/hls/4/playlist.m3u8',1201,logos_tvp+'158.png')
		if selfAddon.getSetting('box_up') == 'TVPlayer': addLink('Box Upfront','158',1202,logos_tvp+'158.png')
		
		#Capital TV
		if selfAddon.getSetting('capital') == 'Direct': addLink('Capital TV','http://ooyalahd2-f.akamaihd.net/i/globalradio01_delivery@156521/index_656_av-p.m3u8?sd=10&rebase=on',1201,logos_tvp+'157.png')
		if selfAddon.getSetting('capital') == 'TVPlayer': addLink('Capital TV','157',1202,logos_tvp+'157.png')
		
		#CBBC
		if selfAddon.getSetting('cbbc') == 'BBC iPlayer': addLink('CBBC HD','http://vs-hls-uk-live.edgesuite.net/pool_1/live/cbbc_hd/cbbc_hd.isml/cbbc_hd-pa4%3d128000-video%3d5070016.m3u8',1201,logos_tvp+'113.png')
		if selfAddon.getSetting('cbbc') == 'TVPlayer': addLink('CBBC','113',1202,logos_tvp+'113.png')
		if selfAddon.getSetting('cbbc') == 'FilmOn': addLink('CBBC','https://www.filmon.com/tv/cbbc',1201,logos_tvp+'113.png')
		
		#CBeebies
		if selfAddon.getSetting('cbeebies') == 'BBC iPlayer': addLink('CBeebies HD','http://vs-hls-uk-live.edgesuite.net/pool_2/live/cbeebies_hd/cbeebies_hd.isml/cbeebies_hd-pa4%3d128000-video%3d5070016.m3u8',1201,logos_tvp+'114.png')
		if selfAddon.getSetting('cbeebies') == 'TVPlayer': addLink('CBeebies','114',1202,logos_tvp+'114.png')
		if selfAddon.getSetting('cbeebies') == 'FilmOn': addLink('CBeebies','https://www.filmon.com/tv/cbeebies',1201,logos_tvp+'114.png')
		
		#CBS Action
		if selfAddon.getSetting('cbs_a') == 'FilmOn': addLink('CBS Action','https://www.filmon.com/tv/cbs-action',1201,logos+'cbsaction.png')
		
		#CBS Drama
		if selfAddon.getSetting('cbs_d') == 'FilmOn': addLink('CBS Drama','https://www.filmon.com/tv/cbs-drama',1201,logos+'cbsdrama.png')
		
		#CBS Reality
		if selfAddon.getSetting('cbs_r') == 'FilmOn': addLink('CBS Reality','https://www.filmon.com/tv/cbs-reality',1201,logos+'cbsreality.png')
		
		#CBS Reality+1
		if selfAddon.getSetting('cbs_r+1') == 'FilmOn': addLink('CBS Reality+1','https://www.filmon.com/tv/cbs-reality1',1201,logos+'cbsreality.png')
		
		#Channel 4
		if selfAddon.getSetting('channel_4') == 'TVPlayer': addLink('Channel 4','92',1202,logos_tvp+'92.png')
		if selfAddon.getSetting('channel_4') == 'FilmOn': addLink('Channel 4','https://www.filmon.com/tv/channel-4',1201,logos_tvp+'92.png')
		
		#Channel 5
		if selfAddon.getSetting('channel_5') == 'TVPlayer': addLink('Channel 5','93',1202,logos_tvp+'93.png')
		if selfAddon.getSetting('channel_5') == 'FilmOn': addLink('Channel 5','https://www.filmon.com/tv/channel-5',1201,logos_tvp+'93.png')
		
		#Channel AKA
		if selfAddon.getSetting('channel_aka') == 'Direct': addLink('Channel AKA','http://rrr.sz.xlcdn.com/?account=AATW&file=akanew&type=live&service=wowza&protocol=http&output=playlist.m3u8',1201,logos_tvp+'227.png')
		if selfAddon.getSetting('channel_aka') == 'TVPlayer': addLink('Channel AKA','227',1202,logos_tvp+'227.png')
		
		#Chilled
		if selfAddon.getSetting('chilled') == 'TVPlayer': addLink('Chilled','226',1202,logos_tvp+'226.png')
		
		#CITV
		if selfAddon.getSetting('citv') == 'ITV Hub': addLink('CITV','http://citvliveios-i.akamaihd.net/hls/live/207267/itvlive/CITVMN/master_Main1800.m3u8',1201,logos+'citv.png')
		
		#Clubbing TV
		if selfAddon.getSetting('clubbingtv') == 'FilmOn': addLink('Clubbing TV','https://www.filmon.com/tv/clubbing-tv',1201,logos+'clubbingtv.png')
		
		#Clubland
		if selfAddon.getSetting('clubland') == 'TVPlayer': addLink('Clubland','225',1202,logos_tvp+'225.png')
		
		#CNN International
		if selfAddon.getSetting('cnn') == 'TVPlayer': addLink('CNN International','286',1202,logos_tvp+'286.png')
		
		#Community Channel
		if selfAddon.getSetting('community') == 'TVPlayer': addLink('Community Channel','259',1202,logos_tvp+'259.png')
		
		#The Craft Channel
		if selfAddon.getSetting('craft_chan') == 'TVPlayer': addLink('The Craft Channel','554',1202,logos_tvp+'554.png')
		
		#Dave
		if selfAddon.getSetting('dave') == 'TVPlayer': addLink('Dave','300',1202,logos_tvp+'300.png')
		
		#Dave ja vu
		if selfAddon.getSetting('dave_ja_vu') == 'TVPlayer': addLink('Dave ja vu','317',1202,logos_tvp+'317.png')
		
		#Drama
		if selfAddon.getSetting('drama') == 'TVPlayer': addLink('Drama','346',1202,logos_tvp+'346.png')
		
		#E4
		if selfAddon.getSetting('e4') == 'FilmOn': addLink('E4','https://www.filmon.com/tv/e4',1201,logos+'e4.png')
		
		#Film4
		if selfAddon.getSetting('film4') == 'FilmOn': addLink('Film4','https://www.filmon.com/tv/film-4',1201,logos+'film4.png')
		
		#Food Network
		if selfAddon.getSetting('food_net') == 'TVPlayer': addLink('Food Network','125',1202,logos_tvp+'125.png')
		if selfAddon.getSetting('food_net') == 'FilmOn': addLink('Food Network','http://www.filmon.com/tv/food-network',1201,logos_tvp+'125.png')
		
		#Food Network+1
		if selfAddon.getSetting('food_net+1') == 'TVPlayer': addLink('Food Network+1','254',1202,logos_tvp+'254.png')
		if selfAddon.getSetting('food_net+1') == 'FilmOn': addLink('Food Network+1','http://www.filmon.com/tv/food-network-plus-1',1201,logos_tvp+'254.png')
		
		#Forces TV
		if selfAddon.getSetting('forces_tv') == 'TVPlayer': addLink('Forces TV','555',1202,logos_tvp+'555.png')
		
		#Heart TV
		if selfAddon.getSetting('heart') == 'Direct': addLink('Heart TV','http://ooyalahd2-f.akamaihd.net/i/globalradio02_delivery@156522/master.m3u8',1201,logos_tvp+'153.png')
		if selfAddon.getSetting('heart') == 'TVPlayer': addLink('Heart TV','153',1202,logos_tvp+'153.png')
		
		#Home
		if selfAddon.getSetting('home') == 'TVPlayer': addLink('Home','512',1202,logos_tvp+'512.png')
		
		#Horror Channel
		if selfAddon.getSetting('horror_ch') == 'FilmOn': addLink('Horror Channel','https://www.filmon.com/tv/horror-channel',1201,logos+'horrorchannel.png')
		
		#ITV1
		if selfAddon.getSetting('itv1') == 'ITV Hub': addLink('ITV1','http://itv1liveios-i.akamaihd.net/hls/live/203437/itvlive/ITV1MN/master_Main1800.m3u8',1201,logos_tvp+'204.png')
		if selfAddon.getSetting('itv1') == 'TVPlayer': addLink('ITV1','204',1202,logos_tvp+'204.png')
		if selfAddon.getSetting('itv1') == 'FilmOn': addLink('ITV1','http://www.filmon.com/tv/itv1',1201,logos_tvp+'204.png')
		
		#ITV1+1
		if selfAddon.getSetting('itv1+1') == 'FilmOn': addLink('ITV1+1','https://www.filmon.com/tv/itv-plus-1',1201,logos_tvp+'204.png')
		
		#ITV2
		if selfAddon.getSetting('itv2') == 'ITV Hub': addLink('ITV2','http://itv2liveios-i.akamaihd.net/hls/live/203495/itvlive/ITV2MN/master_Main1800.m3u8',1201,logos+'itv2.png')
		if selfAddon.getSetting('itv2') == 'FilmOn': addLink('ITV2','http://www.filmon.com/tv/itv2',1201,logos+'itv2.png')
		
		#ITV2+1
		if selfAddon.getSetting('itv2+1') == 'FilmOn': addLink('ITV2+1','https://www.filmon.com/tv/itv2-plus-1',1201,logos+'itv2.png')
		
		#ITV3
		if selfAddon.getSetting('itv3') == 'ITV Hub': addLink('ITV3','http://itv3liveios-i.akamaihd.net/hls/live/207262/itvlive/ITV3MN/master_Main1800.m3u8',1201,logos+'itv3.png')
		if selfAddon.getSetting('itv3') == 'FilmOn': addLink('ITV3','http://www.filmon.com/tv/itv3',1201,logos+'itv3.png')
		
		#ITV3+1
		if selfAddon.getSetting('itv3+1') == 'FilmOn': addLink('ITV3+1','https://www.filmon.com/tv/itv3-plus-1',1201,logos+'itv3.png')
		
		#ITV4
		if selfAddon.getSetting('itv4') == 'ITV Hub': addLink('ITV4','http://itv4liveios-i.akamaihd.net/hls/live/207266/itvlive/ITV4MN/master_Main1800.m3u8',1201,logos+'itv4.png')
		if selfAddon.getSetting('itv4') == 'FilmOn': addLink('ITV4','http://www.filmon.com/tv/itv4',1201,logos+'itv4.png')
		
		#ITV4+1
		if selfAddon.getSetting('itv4+1') == 'FilmOn': addLink('ITV4+1','https://www.filmon.com/tv/itv4-plus-1',1201,logos+'itv4.png')
		
		#ITVBe
		if selfAddon.getSetting('itvbe') == 'ITV Hub': addLink('ITVBe','http://itvbeliveios-i.akamaihd.net/hls/live/219078/itvlive/ITVBE/master_Main1800.m3u8',1201,logos+'itvbe.png')
		if selfAddon.getSetting('itvbe') == 'FilmOn': addLink('ITVBe','http://www.filmon.com/tv/itvbe',1201,logos+'itvbe.png')
		
		#The Jewellery Channel
		if selfAddon.getSetting('tjc') == 'Direct': addLink('The Jewellery Channel','https://d2hee8qk5g0egz.cloudfront.net/live/tjc_sdi1/bitrate1.isml/bitrate1-audio_track=64000-video=1800000.m3u8',1201,logos_tvp+'545.png')
		if selfAddon.getSetting('tjc') == 'TVPlayer': addLink('The Jewellery Channel','545',1202,logos_tvp+'545.png')
		
		#Keep It Country
		if selfAddon.getSetting('kic') == 'TVPlayer': addLink('Keep It Country','569',1202,logos_tvp+'569.png')
		
		#Kerrang
		if selfAddon.getSetting('kerrang') == 'Direct': addLink('Kerrang!','http://llnw.live.btv.simplestream.com/coder11/coder.channels.channel4/hls/4/playlist.m3u8',1201,logos_tvp+'133.png')
		if selfAddon.getSetting('kerrang') == 'TVPlayer': addLink('Kerrang!','133',1202,logos_tvp+'133.png')
		
		#Kiss
		if selfAddon.getSetting('kiss') == 'Direct': addLink('Kiss','http://llnw.live.btv.simplestream.com/coder9/coder.channels.channel14/hls/4/playlist.m3u8',1201,logos_tvp+'131.png')
		if selfAddon.getSetting('kiss') == 'TVPlayer': addLink('Kiss','131',1202,logos_tvp+'131.png')
		
		#Kix
		if selfAddon.getSetting('kix') == 'FilmOn': addLink('Kix!','https://www.filmon.com/tv/kix',1201,logos+'kix.png')
		
		#London Live
		if selfAddon.getSetting('london_live') == 'Direct': addLink('London Live','http://bcoveliveios-i.akamaihd.net/hls/live/217434/3083279840001/master_900.m3u8',1201,logos+'londonlive.png')
		
		#Magic
		if selfAddon.getSetting('magic') == 'Direct': addLink('Magic','http://llnw.live.btv.simplestream.com/coder11/coder.channels.channel2/hls/4/playlist.m3u8',1201,logos_tvp+'132.png')
		if selfAddon.getSetting('magic') == 'TVPlayer': addLink('Magic','132',1202,logos_tvp+'132.png')
		
		#More4
		if selfAddon.getSetting('more4') == 'FilmOn': addLink('More4','https://www.filmon.com/tv/more4',1201,logos+'more4.png')
		
		#NOW Music
		if selfAddon.getSetting('now') == 'Direct': addLink('NOW Music','http://rrr.sz.xlcdn.com/?account=AATW&file=nowmusic&type=live&service=wowza&protocol=http&output=playlist.m3u8',1201,logos_tvp+'228.png')
		if selfAddon.getSetting('now') == 'TVPlayer': addLink('NOW Music','228',1202,logos_tvp+'228.png')
		
		#POP
		if selfAddon.getSetting('pop') == 'FilmOn': addLink('POP','https://www.filmon.com/tv/pop',1201,logos+'pop.png')
		
		#Pick
		if selfAddon.getSetting('pick') == 'FilmOn': addLink('Pick','https://www.filmon.com/tv/pick-tv',1201,logos+'pick.png')
		
		#QUEST
		if selfAddon.getSetting('quest') == 'TVPlayer': addLink('QUEST','327',1202,logos_tvp+'327.png')
		if selfAddon.getSetting('quest') == 'FilmOn': addLink('QUEST','http://www.filmon.tv/tv/quest',1201,logos_tvp+'327.png')
		
		#QUEST+1
		if selfAddon.getSetting('quest+1') == 'TVPlayer': addLink('QUEST+1','336',1202,logos_tvp+'336.png')
		
		#QVC Beauty
		if selfAddon.getSetting('qvc_b') == 'TVPlayer': addLink('QVC Beauty','250',1202,logos_tvp+'250.png')
		
		#QVC Extra
		if selfAddon.getSetting('qvc_e') == 'TVPlayer': addLink('QVC Extra','248',1202,logos_tvp+'248.png')
		
		#QVC Plus
		if selfAddon.getSetting('qvc_p') == 'TVPlayer': addLink('QVC Plus','344',1202,logos_tvp+'344.png')
		
		#QVC Style
		if selfAddon.getSetting('qvc_s') == 'TVPlayer': addLink('QVC Style','249',1202,logos_tvp+'249.png')
		
		#QVC
		if selfAddon.getSetting('qvc') == 'TVPlayer': addLink('QVC','247',1202,logos_tvp+'247.png')
		
		#Really
		if selfAddon.getSetting('really') == 'TVPlayer': addLink('Really','306',1202,logos_tvp+'306.png')
		if selfAddon.getSetting('really') == 'FilmOn': addLink('Really','http://www.filmon.tv/tv/really',1201,logos_tvp+'306.png')
		
		#S4C
		if selfAddon.getSetting('s4c') == 'BBC iPlayer': addLink('S4C','http://vs-hls-uk-live.edgesuite.net/pool_9/live/s4cpbs/s4cpbs.isml/s4cpbs-pa3%3d96000-video%3d1604032.norewind.m3u8',1201,logos_tvp+'251.png')
		if selfAddon.getSetting('s4c') == 'TVPlayer': addLink('S4C','251',1202,logos_tvp+'251.png')
		
		#Sky News
		if selfAddon.getSetting('sky_news') == 'YouTube': addLink('Sky News','https://www.youtube.com/watch?v=y60wDzZt8yg',1201,logos+'skynews.png')
		
		#Tiny Pop
		if selfAddon.getSetting('tiny_pop') == 'FilmOn': addLink('Tiny Pop','https://www.filmon.com/tv/tiny-pop',1201,logos+'tinypop.png')
		
		#Travel Channel
		if selfAddon.getSetting('travel') == 'TVPlayer': addLink('Travel Channel','126',1202,logos_tvp+'126.png')
		
		#Travel Channel+1
		if selfAddon.getSetting('travel+1') == 'TVPlayer': addLink('Travel Channel+1','255',1202,logos_tvp+'255.png')
		if selfAddon.getSetting('travel+1') == 'FilmOn': addLink('Travel Channel+1','http://www.filmon.tv/tv/travel-channel1',1201,logos_tvp+'255.png')
		
		#Yesterday
		if selfAddon.getSetting('yesterday') == 'TVPlayer': addLink('Yesterday','308',1202,logos_tvp+'308.png')
		if selfAddon.getSetting('yesterday') == 'FilmOn': addLink('Yesterday','http://www.filmon.tv/tv/yesterday',1201,logos_tvp+'308.png')
		
		#Yesterday+1
		if selfAddon.getSetting('yesterday+1') == 'TVPlayer': addLink('Yesterday+1','318',1202,logos_tvp+'318.png')
		
		#truTV
		if selfAddon.getSetting('trutv') == 'Direct': addLink('truTV','http://llnw.live.btv.simplestream.com/coder5/coder.channels.channel2/hls/4/playlist.m3u8',1201,logos_tvp+'295.png')
		if selfAddon.getSetting('trutv') == 'TVPlayer': addLink('truTV','295',1202,logos_tvp+'295.png')
		if selfAddon.getSetting('trutv') == 'FilmOn': addLink('truTV','http://www.filmon.tv/tv/tru-tv',1201,logos_tvp+'295.png')
		xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)
		xbmcplugin.endOfDirectory(int(sys.argv[1]))

def play(url):
	resolved = liveresolver.resolve(url)
	item = xbmcgui.ListItem(path=resolved)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
	
def getCookiesString(cookieJar):
    try:
        cookieString=""
        for index, cookie in enumerate(cookieJar):
            cookieString+=cookie.name + "=" + cookie.value +";"
    except: pass
    #print 'cookieString',cookieString
    return cookieString
def open_url(url,data=None,headers=None, cj=None):
    cookie_handler = urllib2.HTTPCookieProcessor(cj)
    opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
        
    req = urllib2.Request(url)

    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    if headers:
        for h in headers:
            req.add_header(h, headers[h])
    response = opener.open(req,data=data)
    link=response.read()
    response.close()
    return link
    
    
def get_treabaAia():
    val=""
    import math
    for d in [5.6
            ,12.1
            ,7.5
            ,3.3
            ,11.8
            ,7
            ,11.6
            ,9
            ,10.7
            ,6.6
            ,3.5
            ,10.1
            ,11.8
            ,7.1
            ,11.5]:
        val +=  chr(int(math.floor(d * 10)));
    return val
import md5
#print 
def generateKey(tokenexpiry):
    return md5.new(tokenexpiry+get_treabaAia()).hexdigest()


def tvplayer(url):
    import re,urllib,json
    watchHtml=open_url("http://tvplayer.com/watch/")
    channelid=url#re.findall('resourceId = "(.*?)"' ,watchHtml)[0]
    validate=re.findall('var validate = "(.*?)"' ,watchHtml)[0]

    cj = CookieJar()
    data = urllib.urlencode({'service':'1','platform':'website','token':'null','validate':validate ,'id' : channelid})
    headers={'Referer':'http://tvplayer.com/watch/','Origin':'http://tvplayer.com','User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
    retjson=open_url("http://api.tvplayer.com/api/v2/stream/live",data=data, headers=headers,cj=cj);
    jsondata=json.loads(retjson)
    #    print cj
    cj = CookieJar()
    playurl=jsondata["tvplayer"]["response"]["stream"]
    open_url(playurl, headers=headers,cj=cj);
    playurl=playurl+'|Cookie=%s&User-Agent=Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36&X-Requested-With=ShockwaveFlash/22.0.0.209&Referer=http://tvplayer.com/watch/'%getCookiesString(cj)
    play(playurl)
    return
        
def tvplayerFlashVersion(url):
    import re,urllib,json
    watchHtml=open_url('http://tvplayer.com/watch/')
    hashval=urllib.unquote(re.findall('hash = "(.*?)"' ,watchHtml)[0])
    expval=re.findall('exp = "(.*?)"' ,watchHtml)[0]
    keyval=generateKey(expval)
    cj = CookieJar()
    data = urllib.urlencode({'id' : url})
    headers={'Token-Expiry':expval ,'Hash': hashval,'Key':keyval,'Referer':'http://assets.tvplayer.com/web/flash/tvplayer/TVPlayer-DFP-3.swf','X-Requested-With':'ShockwaveFlash/22.0.0.209'}
    retjson=open_url("http://live.tvplayer.com/stream-web-encrypted.php",data=data, headers=headers,cj=cj);
    jsondata=json.loads(retjson)
#    print cj
    url=jsondata["tvplayer"]["response"]["stream"]
    play(url+'|Cookie=%s&User-Agent=Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36&X-Requested-With=ShockwaveFlash/22.0.0.209&Referer=http://tvplayer.com/watch/'%getCookiesString(cj))
    return 
    
    #url='http://api.tvplayer.com/api/v2/stream/live/?id=%s&service=1&platform=website&token=A5roOFiAkvbuD7USnF76j9HbnpZJPFhTeojsN0zaLik=&validate=eyJ0b2tlbiI6IjRjNTdkZTVjOTFkNzJjOGNlZjI2OTNjYTFiMzFhMTJjIiwiZXhwaXJ5IjoiMjAxNi0wOS0xMVQxODowMjoyNCswMDAwIn0=&device=null' % url
    
    #iconimage=""
    #req = urllib2.Request(url)
    #req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    #response = urllib2.urlopen(req)
    #link=response.read()
    #response.close()

    #pattern = ""
    #matches = plugintools.find_multiple_matches(link,'"tvplayer":(.*?)"drmToken"')
    
    #for entry in matches:
       
    #    url = plugintools.find_single_match(entry,'"stream": "(.+?)",')

    #    play(url)
	
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param
        
def addLink(name,url,mode,iconimage,showcontext=True,allinfo={}):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setProperty('fanart_image', fanart)
        liz.setProperty("IsPlayable","true")
        if showcontext:
            contextMenu = []
            if showcontext == 'fav':
                contextMenu.append(('Remove from Quantum Favorites','XBMC.RunPlugin(%s?mode=12&name=%s)'
                                    %(sys.argv[0], urllib.quote_plus(name))))
            if not name in FAV:
                contextMenu.append(('Add to Quantum Favorites','XBMC.RunPlugin(%s?mode=11&name=%s&url=%s&iconimage=%s&fanart=%s&fav_mode=%s)'
                         %(sys.argv[0], urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(iconimage), urllib.quote_plus(fanart), mode)))
            liz.addContextMenuItems(contextMenu)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok

def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        
              
params=get_params()
url=None
name=None
mode=None
iconimage=None
fav_mode=None

try:
    fav_mode=int(params["fav_mode"])
except:
    pass

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass

print "Mode: "+str(mode)
print "Name: "+str(name)

if mode==1200:CATEGORIES()	
elif mode==1201: play(url)
elif mode==1202: tvplayer(url)
elif mode==11:
    try:
        name = name.split('\\ ')[1]
    except:
        pass
    try:
        name = name.split('  - ')[0]
    except:
        pass
    process.addFavorite(name,url,iconimage,fanart,fav_mode)
elif mode==12:
    try:
        name = name.split('\\ ')[1]
    except:
        pass
    try:
        name = name.split('  - ')[0]
    except:
        pass
    process.rmFavorite(name)