# most code developed by demons_are_real - https://www.reddit.com/user/demons_are_real

import xbmcaddon
import xbmcgui
import xbmcplugin
import xbmc
import sys
import os
import utils
import ConfigParser
import urllib, json
import socket
from datetime import datetime

from game import Game
from urlparse import parse_qsl

addonUrl = sys.argv[0]
addonHandle = int(sys.argv[1])
addonId = "plugin.video.nhlstreams"
addon = xbmcaddon.Addon(id = addonId)
addonPath = addon.getAddonInfo('path')
addonName = addon.getAddonInfo('name')

iniFilePath = os.path.join(addonPath, 'resources', 'nhlstreams.ini')

config = ConfigParser.ConfigParser()
config.read(iniFilePath)

hostname = socket.gethostbyname("mf.svc.nhl.com")
server = config.get("NHLstreams","Host")

def games(date): return Game.fromDate(config,date)

def listyears(yesterday = True):
  items = []  
  if yesterday:	
    listItem = xbmcgui.ListItem(label = 'Yesterday - ' + utils.yesterday().strftime("%B, %d - %Y"))
    listItem.setInfo( type="Video", infoLabels={ "Title": "Yesterday" } )
    url = '{0}?action=listgamesyest'.format(addonUrl)
    items.append((url, listItem, True))  
  for y in utils.years():
    listItem = xbmcgui.ListItem(label = str(y))
    listItem.setInfo( type="Video", infoLabels={ "Title": str(y) } )
    url = '{0}?action=listmonths&year={1}'.format(addonUrl,y)
    items.append((url, listItem, True))

  ok = xbmcplugin.addDirectoryItems(addonHandle, items, len(items)) 
  xbmcplugin.endOfDirectory(addonHandle)

def listmonths(year):
  items = []
  for (mn,m) in utils.months(year):
    listItem = xbmcgui.ListItem(label = mn)
    listItem.setInfo( type="Video", infoLabels={ "Title": mn } )
    url = '{0}?action=listdays&year={1}&month={2}'.format(addonUrl,year,m)
    items.append((url, listItem, True))

  ok = xbmcplugin.addDirectoryItems(addonHandle, items, len(items)) 
  xbmcplugin.endOfDirectory(addonHandle)

def listdays(year,month):
  items = []
  for d in utils.days(year,month):
    listItem = xbmcgui.ListItem(label = str(d))
    listItem.setInfo( type="Video", infoLabels={ "Title": str(d) } )
    url = '{0}?action=listgames&year={1}&month={2}&day={3}'.format(addonUrl,year,month,d)
    items.append((url, listItem, True))

  ok = xbmcplugin.addDirectoryItems(addonHandle, items, len(items)) 
  xbmcplugin.endOfDirectory(addonHandle)

def listgames(date,previous = False,settings = True):
  items = []
  dategames = games(date)
  for g in dategames: 
    label = "%s vs. %s [%s]" % (g.awayFull,g.homeFull,g.timeRemaining if g.timeRemaining != "N/A" else utils.asCurrentTz(date,g.time))
    listItem = xbmcgui.ListItem(label = label)
    listItem.setInfo( type="Video", infoLabels={ "Title": label } )
    url = '{0}?action=feeds&game={1}&date={2}'.format(addonUrl,g.id,date)
    items.append((url, listItem, True))
  if len(items) == 0:
    xbmcgui.Dialog().ok(addonName, "No games scheduled today")   
  if previous:
    listItem = xbmcgui.ListItem(label = "[COLOR red][ Games Archive ][/COLOR]")
    listItem.setInfo( type="Video", infoLabels={ "Title": "Previous" } )
    url = '{0}?action=listyears'.format(addonUrl)
    items.append((url, listItem, True))		
  if settings:	
    listItem = xbmcgui.ListItem(label = "[COLOR red][ Add-on Settings ][/COLOR]")
    listItem.setInfo( type="Video", infoLabels={ "Title": "Settings" } )
    url = '{0}?action=settings'.format(addonUrl)
    items.append((url, listItem, True))
	
  ok = xbmcplugin.addDirectoryItems(addonHandle, items, len(items)) 
  xbmcplugin.endOfDirectory(addonHandle)
  print "Added %d games" % len(items)

def listfeeds(game,date):  
  if hostname != server:
    xbmcgui.Dialog().ok(addonName, "Your Hosts file wasn't modified correctly !", "You will need to manually modify hosts file...", "Modify your hosts file with - [COLOR red]104.251.218.27 mf.svc.nhl.com[/COLOR]")
  else:
    items = []
    for f in filter(lambda f: f.viewable(), game.feeds):
      label = str(f)
      listItem = xbmcgui.ListItem(label = label)
      listItem.setInfo( type="Video", infoLabels={ "Title": label } )
      url = '{0}?action=play&date={1}&feedId={2}'.format(addonUrl,date,f.mediaId)
      items.append((url, listItem, False))

    ok = xbmcplugin.addDirectoryItems(addonHandle, items, len(items)) 
    xbmcplugin.endOfDirectory(addonHandle)

def playgame(date,feedId):
  def adjustQuality(masterUrl):
    defaultQuality = "720p 60fps"
    qualityUrlDict = {
      "360p": "1200K/1200_complete.m3u8",
      "540p": "2500K/2500_complete.m3u8",
      "720p": "3500K/3500_complete.m3u8",
      "720p 60fps": "5000K/5000_complete.m3u8",
    }
    m3u8Path = qualityUrlDict.get(addon.getSetting("quality"), qualityUrlDict[defaultQuality])
    return masterUrl.rsplit('/',1)[0] + "/" + m3u8Path

  def xbmcPlayer(url,mediaAuth):
    print "XBMC trying to play URL [%s]" % (url)
    completeUrl = url + ("|Cookie=mediaAuth%%3D%%22%s%%22" % (mediaAuth))
    xbmc.Player().play(adjustQuality(url) + ("|Cookie=mediaAuth%%3D%%22%s%%22" % (mediaAuth)))
    
  cdn = 'akc' if addon.getSetting("cdn") == "Akamai" else 'l3c'
  contentUrl = "http://mf.svc.nhl.com/m3u8/%s/%s%s" % (date,feedId,cdn)
  print "Content url [%s]" % (contentUrl)
  response = urllib.urlopen(contentUrl)
  playUrl = response.read().replace('l3c',cdn)
  print "Using CDN %s, play url is [%s]" % (cdn,playUrl)
  mediaAuthSalt = utils.salt()
  if utils.head(playUrl,dict(mediaAuth=mediaAuthSalt)):
    xbmcPlayer(playUrl,mediaAuthSalt)
  else:
    otherCdn = 'akc' if cdn == 'l3c' else 'l3c' 
    print "URL [%s] failed on HEAD, switching CDN from %s to %s" % (playUrl,cdn,otherCdn)
    xbmcPlayer(playUrl.replace(cdn,otherCdn), mediaAuthSalt)

def router(paramstring):
  params = dict(parse_qsl(paramstring))
  if params:
    if params['action'] == 'feeds':
      dategames = games(params['date'])
      gameDict = dict(map(lambda g: (g.id, g), dategames))
      listfeeds(gameDict[int(params['game'])], params['date'])
    elif params['action'] == 'play':
      playgame(params['date'],params['feedId'])
    elif params['action'] == 'listyears':
      listyears()
    elif params['action'] == 'listmonths':
      listmonths(params['year'])
    elif params['action'] == 'listdays':
      listdays(params['year'],params['month'])
    elif params['action'] == 'listgames':
      listgames("%d-%02d-%02d" % (int(params['year']),int(params['month']),int(params['day'])))  
    elif params['action'] == 'settings':
	  addon.openSettings()	  
    elif params['action'] == 'listgamesyest':
      listgames(utils.yesterday().strftime("%Y-%m-%d"),True)  
  else:	
	listgames(utils.today().strftime("%Y-%m-%d"),True)
  
if __name__ == '__main__':
  if hostname != server:
    if xbmcgui.Dialog().yesno("NHL Streams", "This Add-on will modify your [COLOR red]Hosts[/COLOR] file",  "Select [B]Yes[/B] to Continue, or [B]No[/B] to Cancel"):
      try:
	    #thanks to Vinman for hosts modifier code
        xbmc.executebuiltin('RunScript(special://home/addons/plugin.video.nhlstreams/hosts.py)')				
      except:
        pass	
      router(sys.argv[2][1:])
  else:	
    router(sys.argv[2][1:])
