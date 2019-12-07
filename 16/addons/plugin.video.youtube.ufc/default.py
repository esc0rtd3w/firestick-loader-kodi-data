import re, urllib2, urlparse, urllib, json
import xbmc, xbmcgui,xbmcplugin,xbmcaddon
import channel

base_url=sys.argv[0]
pluginhandle = int(sys.argv[1])
channelId = channel.Id

addonname = base_url.replace('plugin://','').replace('/','')
addon = xbmcaddon.Addon(addonname)
thumbsEnabled = addon.getSetting('thumbs')

def addVideos(user, pageToken=None):
    jsonUrl = "https://www.googleapis.com/youtube/v3/search?part=snippet&channelId="+user+"&maxResults=50&order=date&key=AIzaSyDMcuNvJSgtAec6Vvm3gyJrQeY6AWcDA54"
    if pageToken is not None :
        jsonUrl = jsonUrl + '&pageToken='+pageToken
    content = getUrl(jsonUrl)
    data = json.loads(content)
    for item in data['items'] :
        title = item['snippet']['title']
        if 'videoId' in item['id'] :
            ytId=item['id']['videoId']
            videoUrl='plugin://plugin.video.youtube/play/?video_id='+ytId
        elif 'playlistId' in item['id'] :
            continue
            ytId=item['id']['playlistId']
            videoUrl='plugin://plugin.video.youtube/play/?playlist_id='+ytId+'/'
        else :
            continue
        description=item['snippet']['description']
        icon = item['snippet']['thumbnails']['high']['url']
        li = xbmcgui.ListItem(label=title, iconImage=icon, thumbnailImage=icon)
        li.setProperty('fanart_image',icon)
        li.setProperty('IsPlayable', 'true')
        li.addContextMenuItems([ ('Vernieuwen...', 'Container.Refresh') ])
        xbmcplugin.addDirectoryItem(handle=pluginhandle, url=videoUrl, listitem=li)
    if data['nextPageToken'] :
        addNextPage(data['nextPageToken'])
    if(thumbsEnabled == "true") :
        xbmc.executebuiltin('Container.SetViewMode(500)')
    xbmcplugin.endOfDirectory(pluginhandle)

def getIcon(ytId):
    try:
        url = 'http://i.ytimg.com/vi/'+ytId+'/hqdefault.jpg'
        req = urllib2.Request(url)
        response = urllib2.urlopen(req,timeout=5)
        return url
    except:
        return 'http://i.ytimg.com/vi/'+ytId+'/default.jpg'

def getUrl(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:19.0) Gecko/20100101 Firefox/19.0')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
  
def addNextPage(pageNr):
    url = build_url({'page': str(pageNr)})
    li = xbmcgui.ListItem('Volgende pagina', iconImage='DefaultFolder.png')
    xbmcplugin.addDirectoryItem(handle=pluginhandle, url=url, listitem=li, isFolder=True)

def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

args = urlparse.parse_qs(sys.argv[2][1:])
pnr = args.get('page', None)
if(pnr is None):
    pagenr = None
else:
    pagenr = pnr[0]

addVideos(channelId, pagenr)

