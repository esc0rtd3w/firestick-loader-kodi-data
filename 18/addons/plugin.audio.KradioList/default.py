# KradioList Radio Plugin
# We do not own or publish the content delivered by the plugin
# Tune in to the best radio stations on the net

import sys
import xbmcgui
import xbmcplugin
  
addon_handle = int(sys.argv[1])
xbmcplugin.setContent(addon_handle, 'audio')
url='http://streaming.radionomy.com/Kradiomix?lang=he-IL%2che%3bq%3d0.8%2cen-US%3bq%3d0.6%2cen%3bq%3d0.4%2cfr%3bq%3d0.2%2cnl%3bq%3d0.2%2cru%3bq%3d0.2'
li = xbmcgui.ListItem('[COLOR deepskyblue][B]Kradiomix[/B][/COLOR]  [COLOR lime][/COLOR] >>', iconImage='http://www.userlogos.org/files/logos/macleod.mac/music3.png', thumbnailImage= 'http://www.userlogos.org/files/logos/macleod.mac/music3.png')
li.setProperty('fanart_image', 'http://onehdwallpaper.com/wp-content/uploads/2015/07/Music-HD-Desktop-Wallpapers-1080p.jpeg?resize=981%2C552')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
    
addon_handle = int(sys.argv[1])
xbmcplugin.setContent(addon_handle, 'audio')
url='http://37.187.141.169/~udi/80s.m3u'
li = xbmcgui.ListItem('[COLOR deepskyblue][B]80s[/B][/COLOR]  [COLOR lime](Live)[/COLOR] >>', iconImage='http://cdn-radiotime-logos.tunein.com/s232847q.png', thumbnailImage= 'http://cdn-radiotime-logos.tunein.com/s232847q.png')
li.setProperty('fanart_image', 'https://s-media-cache-ak0.pinimg.com/736x/82/a2/bb/82a2bb6347c2c6fba6da41fc90fd40aa.jpg?resize=981%2C552')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

addon_handle = int(sys.argv[1])
xbmcplugin.setContent(addon_handle, 'audio')
url='http://37.187.141.169/~udi/90s.m3u'
li = xbmcgui.ListItem('[COLOR deepskyblue][B]90s[/B][/COLOR]  [COLOR lime](Live)[/COLOR] >>', iconImage='https://s3.amazonaws.com/htw/dt-contest-entries/thumbs/23964/canada-media-music-website-entertainment-logo-design.png', thumbnailImage= 'https://s3.amazonaws.com/htw/dt-contest-entries/thumbs/23964/canada-media-music-website-entertainment-logo-design.png')
li.setProperty('fanart_image', 'http://hdwallpaperbackgrounds.net/wp-content/uploads/2015/11/Bruno-Mars-Playing-Guitar-HD-Wallpapers.jpg?resize=981%2C552')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

addon_handle = int(sys.argv[1])
xbmcplugin.setContent(addon_handle, 'audio')
url='http://37.187.141.169/~udi/dance.m3u'
li = xbmcgui.ListItem('[COLOR deepskyblue][B]Dance[/B][/COLOR]  [COLOR lime](Live)[/COLOR] >>', iconImage='http://piter.fm/img/empty/artists/200x200/empty.png', thumbnailImage= 'http://piter.fm/img/empty/artists/200x200/empty.png')
li.setProperty('fanart_image', 'http://storage.googleapis.com/wzukusers/user-500000/images/40KB7I6110y8s3TF6BJy4g.jpg?resize=981%2C552')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

addon_handle = int(sys.argv[1])
xbmcplugin.setContent(addon_handle, 'audio')
url='http://37.187.141.169/~udi/rock.m3u'
li = xbmcgui.ListItem('[COLOR deepskyblue][B]Rock[/B][/COLOR]  [COLOR lime](Live)[/COLOR] >>', iconImage='http://biz.prlog.org/ManessasWorldofMusic/logo.png', thumbnailImage= 'http://biz.prlog.org/ManessasWorldofMusic/logo.png')
li.setProperty('fanart_image', 'http://coolpcwallpapers.com/wp-content/uploads/2014/10/Music-AC-DC-Heavy-Metal-Hard-Rock-Classic-Bands-Wallpaper-1920x1080.jpg?resize=981%2C552')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

addon_handle = int(sys.argv[1])
xbmcplugin.setContent(addon_handle, 'audio')
url='http://37.187.141.169/~udi/black.m3u'
li = xbmcgui.ListItem('[COLOR deepskyblue][B]Rap HipHop R&B[/B][/COLOR]  [COLOR lime](Live)[/COLOR] >>', iconImage='http://piter.fm/img/empty/artists/200x200/empty.png', thumbnailImage= 'http://piter.fm/img/empty/artists/200x200/empty.png')
li.setProperty('fanart_image', 'http://www.publicenemyafrica.com/wp-content/uploads/2011/09/hip-hop-cats.jpg?resize=981%2C552')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)


addon_handle = int(sys.argv[1])
xbmcplugin.setContent(addon_handle, 'audio')
url='http://37.187.141.169/~udi/world.m3u'
li = xbmcgui.ListItem('[COLOR deepskyblue][B]world[/B][/COLOR]  [COLOR lime](Live)[/COLOR] >>', iconImage='http://biz.prlog.org/ManessasWorldofMusic/logo.png', thumbnailImage= 'http://biz.prlog.org/ManessasWorldofMusic/logo.png')
li.setProperty('fanart_image', 'http://www.amozik.net/vegas/2.jpg?resize=981%2C552')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

addon_handle = int(sys.argv[1])
xbmcplugin.setContent(addon_handle, 'audio')
url='http://37.187.141.169/~udi/trance.m3u'
li = xbmcgui.ListItem('[COLOR deepskyblue][B]Electronic[/B][/COLOR]  [COLOR lime](Live)[/COLOR] >>', iconImage='https://lh3.googleusercontent.com/-wrZyN3BJ9kU/AAAAAAAAAAI/AAAAAAAAAAA/P803xd0Y6tU/photo.jpg', thumbnailImage= 'https://lh3.googleusercontent.com/-wrZyN3BJ9kU/AAAAAAAAAAI/AAAAAAAAAAA/P803xd0Y6tU/photo.jpg')
li.setProperty('fanart_image', 'http://hdwallpapers.cat/wallpaper/enjoy_the_music_headphones_trance_dj_hd-wallpaper-207102.jpg?resize=981%2C552')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)



xbmcplugin.endOfDirectory(addon_handle)

