# Old Time Radio
# We do not own or publish the content delivered by the plugin
# streaming old time radio

import sys
import xbmcgui
import xbmcplugin
 
addon_handle = int(sys.argv[1])
xbmcplugin.setContent(addon_handle, 'audio')
url = 'http://s8.voscast.com:7372'
li = xbmcgui.ListItem('[COLOR red][B]Relic Radio[/B][/COLOR] >>', iconImage='http://media.relicradio.com/scifilogo.jpg', thumbnailImage= 'http://media.relicradio.com/scifilogo.jpg')
li.setProperty('fanart_image', 'http://www.relicradio.com/otr/wp-content/uploads/2015/11/cat-scifi.jpg')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
 
addon_handle = int(sys.argv[1])
xbmcplugin.setContent(addon_handle, 'audio')
url = 'http://www.otrfan.com:8000/stream.m3u'
li = xbmcgui.ListItem('[COLOR deepskyblue][B]Old Time Radio Fans[/B][/COLOR] >>', iconImage='http://socorock.com/uploads/radio-9.png', thumbnailImage= 'http://socorock.com/uploads/radio-9.png')
li.setProperty('fanart_image', 'http://farm3.staticflickr.com/2750/5796934203_cca4a7aa3a_z.jpg')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
 
addon_handle = int(sys.argv[1])
xbmcplugin.setContent(addon_handle, 'audio')
url = 'http://lin2.ash.fast-serv.com:9022'
li = xbmcgui.ListItem('[COLOR red][B]ABN Old Time Radio[/B][/COLOR] >>', iconImage='http://www.talkshoe.com/custom/images/icons/TC-19082-MainIcon.jpg', thumbnailImage= 'http://www.talkshoe.com/custom/images/icons/TC-19082-MainIcon.jpg')
li.setProperty('fanart_image', 'http://radio.macinmind.com/abn_const2_logo.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

addon_handle = int(sys.argv[1])
xbmcplugin.setContent(addon_handle, 'audio')
url = 'http://audioartsradio.com:6006/listen.pls#sthash.6QJKLcaV.dpuf'
li = xbmcgui.ListItem('[COLOR deepskyblue][B]20th Century Radio[/B][/COLOR] >>', iconImage='http://findicons.com/files/icons/2533/vintage_radio/256/radio_1.png', thumbnailImage= 'http://findicons.com/files/icons/2533/vintage_radio/256/radio_1.png')
li.setProperty('fanart_image', 'http://img13.deviantart.net/050c/i/2009/362/d/7/old_radio___by_q8ieng.jpg')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

addon_handle = int(sys.argv[1])
xbmcplugin.setContent(addon_handle, 'audio')
url = 'http://s1.myradiostream.com:4962'
li = xbmcgui.ListItem('[COLOR red][B]Hanks Old Time Radio[/B][/COLOR] >>', iconImage='http://png-2.findicons.com/files/icons/2533/vintage_radio/256/radio_4.png', thumbnailImage= 'http://png-2.findicons.com/files/icons/2533/vintage_radio/256/radio_4.png')
li.setProperty('fanart_image', 'http://www.redhead.co.nz/wp-content/uploads/2012/06/Radio_feat1.jpg')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

addon_handle = int(sys.argv[1])
xbmcplugin.setContent(addon_handle, 'audio')
url = 'http://s1.viastreaming.net:9165/listen.pls'
li = xbmcgui.ListItem('[COLOR deepskyblue][B]Crime and Suspense[/B][/COLOR] >>', iconImage='http://www.onesmedia.com/images/OTR/Suspense2.png', thumbnailImage= 'http://www.onesmedia.com/images/OTR/Suspense2.png')
li.setProperty('fanart_image', 'http://www.townradio.ca/beausejour/wp-content/uploads/2009/10/Suspense.jpg')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

addon_handle = int(sys.argv[1])
xbmcplugin.setContent(addon_handle, 'audio')
url = 'http://s1.viastreaming.net:9185/listen.pls'
li = xbmcgui.ListItem('[COLOR red][B]Science Fiction[/B][/COLOR] >>', iconImage='http://www.botar.us/foto/spacepatrolicon.jpg', thumbnailImage= 'http://www.botar.us/foto/spacepatrolicon.jpg')
li.setProperty('fanart_image', 'http://cdn8.openculture.com/wp-content/uploads/2014/06/xminusone.jpg')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
 
addon_handle = int(sys.argv[1])
xbmcplugin.setContent(addon_handle, 'audio')
url = 'http://s1.viastreaming.net:9155/listen.pls'
li = xbmcgui.ListItem('[COLOR deepskyblue][B]British Comedy[/B][/COLOR] >>', iconImage='http://www.babyboomercentral.com.au/images/icons_goons1.jpg', thumbnailImage= 'http://www.babyboomercentral.com.au/images/icons_goons1.jpg')
li.setProperty('fanart_image', 'http://www.bbc.co.uk/comedy/games/wallpaper/images/3goons1024.jpg')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
 
addon_handle = int(sys.argv[1])
xbmcplugin.setContent(addon_handle, 'audio')
url = 'http://s1.viastreaming.net:9160/listen.pls'
li = xbmcgui.ListItem('[COLOR red][B]American Comedy[/B][/COLOR] >>', iconImage='https://bogiefilmblog.files.wordpress.com/2013/10/benny-title-card.png', thumbnailImage= 'https://bogiefilmblog.files.wordpress.com/2013/10/benny-title-card.png')
li.setProperty('fanart_image', 'https://upload.wikimedia.org/wikipedia/en/4/43/Amosnandy.jpg')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

addon_handle = int(sys.argv[1])
xbmcplugin.setContent(addon_handle, 'audio')
url = 'http://s1.viastreaming.net:9180/listen.pls'
li = xbmcgui.ListItem('[COLOR deepskyblue][B]Old Time GOLD[/B][/COLOR] >>', iconImage='http://www.officialpsds.com/images/thumbs/Gold-Mic-psd3308.png', thumbnailImage= 'http://www.officialpsds.com/images/thumbs/Gold-Mic-psd3308.png')
li.setProperty('fanart_image', 'http://orig08.deviantart.net/152f/f/2010/047/a/3/old_time_radio_microphone_big_by_mackingster.jpg')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

addon_handle = int(sys.argv[1])
xbmcplugin.setContent(addon_handle, 'audio')
url = 'http://streaming.radio.co:80/sf5708c004/listen'
li = xbmcgui.ListItem('[COLOR red][B]Yesterday USA Radio Red[/B][/COLOR] >>', iconImage='https://universalgeni.files.wordpress.com/2010/08/radio-red-icon.png', thumbnailImage= 'https://universalgeni.files.wordpress.com/2010/08/radio-red-icon.png')
li.setProperty('fanart_image', 'http://ecx.images-amazon.com/images/I/41HS8HfRQSL.jpg')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

addon_handle = int(sys.argv[1])
xbmcplugin.setContent(addon_handle, 'audio')
url = 'http://streaming.radio.co:80/sa37b728bf/listen '
li = xbmcgui.ListItem('[COLOR deepskyblue][B]Yesterday USA Radio Blue[/B][/COLOR] >>', iconImage='https://images.duckduckgo.com/iu/?u=http%3A%2F%2Fwww.thebakeliteradio.com%2Fpage119%2Ffiles%2Fbellblue.png&f=1', thumbnailImage= 'https://images.duckduckgo.com/iu/?u=http%3A%2F%2Fwww.thebakeliteradio.com%2Fpage119%2Ffiles%2Fbellblue.png&f=1')
li.setProperty('fanart_image', 'https://thefullblog.files.wordpress.com/2010/12/old-microphone.jpg')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

addon_handle = int(sys.argv[1])
xbmcplugin.setContent(addon_handle, 'audio')
url = 'https://albireo.shoutca.st/tunein/starcrea.pls'
li = xbmcgui.ListItem('[COLOR red][B]CrimeTime[/B][/COLOR] >>', iconImage='http://www.otrnow.com/crimetime/CRIMETIME300.png', thumbnailImage= 'http://www.otrnow.com/crimetime/CRIMETIME300.png')
li.setProperty('fanart_image', 'http://kingsacademy.com/mhodges/03_The-World-since-1900/04_The-Roaring-20s/pictures/radio-programming.jpg')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

addon_handle = int(sys.argv[1])
xbmcplugin.setContent(addon_handle, 'audio')
url = 'https://rosetta.shoutca.st/tunein/riradtke.pls'
li = xbmcgui.ListItem('[COLOR deepskyblue][B]Amazing Tales[/B][/COLOR] >>', iconImage='http://amazingstoriesmag.com/wp-content/uploads/2014/10/featured-wow-cover.png', thumbnailImage= 'http://amazingstoriesmag.com/wp-content/uploads/2014/10/featured-wow-cover.png')
li.setProperty('fanart_image', 'http://www.retroactivedame.com/wp-content/uploads/2009/11/old-time-radio-couple.jpg')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

addon_handle = int(sys.argv[1])
xbmcplugin.setContent(addon_handle, 'audio')
url = 'https://albireo.shoutca.st/tunein/riradt00.pls'
li = xbmcgui.ListItem('[COLOR red][B]OTRNow Radio Program[/B][/COLOR] >>', iconImage='http://www.wpclipart.com/recreation/entertainment/radio/radio_old.png', thumbnailImage= 'http://www.wpclipart.com/recreation/entertainment/radio/radio_old.png')
li.setProperty('fanart_image', 'http://www.otrcat.com/z/william-conrad-gunsmoke-kickin-it.jpg')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

addon_handle = int(sys.argv[1])
xbmcplugin.setContent(addon_handle, 'audio')
url = 'http://s21.myradiostream.com:9714/listen.pls'
li = xbmcgui.ListItem('[COLOR deepskyblue][B]Hanks Gumshoe OTR[/B][/COLOR] >>', iconImage='http://www.botar.us/foto/philipmarloweicon.jpg', thumbnailImage= 'http://www.botar.us/foto/philipmarloweicon.jpg')
li.setProperty('fanart_image', 'http://i1.ytimg.com/vi/n04MpeH48qo/hqdefault.jpg')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
 
addon_handle = int(sys.argv[1])
xbmcplugin.setContent(addon_handle, 'audio')
url = 'http://cp.usa11.fastcast4u.com:2199/tunein/darkarts.pls'
li = xbmcgui.ListItem('[COLOR red][B]Dark Arts Horror Radio[/B][/COLOR] >>', iconImage='http://www.botar.us/foto/escapeicon.jpg', thumbnailImage= 'http://www.botar.us/foto/escapeicon.jpg')
li.setProperty('fanart_image', 'http://www.tasteofcinema.com/wp-content/uploads/2014/10/universal-horror-films.jpg')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

addon_handle = int(sys.argv[1])
xbmcplugin.setContent(addon_handle, 'audio')
url = 'http://cent5.serverhostingcenter.com:2199/tunein/barryinindy.pls'
li = xbmcgui.ListItem('[COLOR deepskyblue][B]Suspense Radio[/B][/COLOR] >>', iconImage='http://www.otrcat.com/z/listening-to-old-time-radio-otrcat.com2.png', thumbnailImage= 'http://www.otrcat.com/z/listening-to-old-time-radio-otrcat.com2.png')
li.setProperty('fanart_image', 'http://www.sherylfranklin.com/images/sherlock/rathbone/rathbone01.jpg')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
 
addon_handle = int(sys.argv[1])
xbmcplugin.setContent(addon_handle, 'audio')
url = 'http://96.31.83.87:8095'
li = xbmcgui.ListItem('[COLOR red][B]Mystery Play Internet Radio OTR[/B][/COLOR] >>', iconImage='http://www.botar.us/foto/sherlockholmesicon.jpg', thumbnailImage= 'http://www.botar.us/foto/sherlockholmesicon.jpg')
li.setProperty('fanart_image', 'http://www.cbsrmt.com/img/cbsrmt-ad.jpg')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

addon_handle = int(sys.argv[1])
xbmcplugin.setContent(addon_handle, 'audio')
url = 'http://laradiofm.kz/download/65-en-pls/'
li = xbmcgui.ListItem('[COLOR deepskyblue][B]Old Time Radio[/B][/COLOR] >>', iconImage='http://www.botar.us/foto/fibbericon.jpg', thumbnailImage= 'http://www.botar.us/foto/fibbericon.jpg')
li.setProperty('fanart_image', 'http://www.deniscarl.com/previous/20060914/Pictureoftheday_1440x900.jpg')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
 
addon_handle = int(sys.argv[1])
xbmcplugin.setContent(addon_handle, 'audio')
url = 'http://dir.xiph.org/listen/922508/listen.m3u'
li = xbmcgui.ListItem('[COLOR red][B]Old Time Radio Classics[/B][/COLOR] >>', iconImage='http://www.botar.us/foto/bostonblackieicon.jpg', thumbnailImage= 'http://www.botar.us/foto/bostonblackieicon.jpg')
li.setProperty('fanart_image', 'http://www.otrcat.com/z/jack-benny-fred-allen-feud.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

addon_handle = int(sys.argv[1])
xbmcplugin.setContent(addon_handle, 'audio')
url = 'http://dir.xiph.org/listen/795703/listen.m3u'
li = xbmcgui.ListItem('[COLOR deepskyblue][B]Crime Fighter Detectives[/B][/COLOR] >>', iconImage='http://www.botar.us/foto/greenhorneticon.jpg', thumbnailImage= 'http://www.botar.us/foto/greenhorneticon.jpg')
li.setProperty('fanart_image', 'http://images2.fanpop.com/images/photos/4400000/Orson-Welles-classic-movies-4432474-1024-768.jpg')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

xbmcplugin.endOfDirectory(addon_handle)

