#!/usr/bin/python
#encoding: utf-8

#/*
# *      Copyright (C) 2015-2016 gerikss, modded with permission by podgod
# *
# *  This Program is free software; you can redistribute it and/or modify
# *  it under the terms of the GNU General Public License as published by
# *  the Free Software Foundation; either version 2, or (at your option)
# *  any later version.
# *
# *  This Program is distributed in the hope that it will be useful,
# *  but WITHOUT ANY WARRANTY; without even the implied warranty of
# *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# *  GNU General Public License for more details.
# *
# *  You should have received a copy of the GNU General Public License
# *  along with this program; see the file COPYING.  If not, write to
# *  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
# *  http://www.gnu.org/copyleft/gpl.html
# *
# *  ===================
# *
# *  Sbnation API in this plugin belongs to sbnation.com and being used 
# *  only to find NBA/NHL/NFL/MLB games and scores (the same way as on sbnation.com/scoreboard website)
# *  
# *  All Reddit resources used in this plugin belong to their owners and reddit.com
# *  
# *  All logos used in this plugin belong to their owners
# *  
# *  All video streams used in this plugin belong to their owners
# *  
# *  
# */



import urllib, urllib2, sys, cookielib, base64, re
import xbmc, xbmcgui, xbmcplugin, xbmcaddon
from datetime import datetime, timedelta
import json
import calendar, time
import CommonFunctions
import praw
import urlparse
import random
import checkaddon
common = CommonFunctions

__addon__ = xbmcaddon.Addon('plugin.video.prosport')
__addonname__ = __addon__.getAddonInfo('name')
path = __addon__.getAddonInfo('path')
display_score = __addon__.getSetting('score')
display_status = __addon__.getSetting('status')
display_start_time = __addon__.getSetting('start_time')
display_pattern = __addon__.getSetting('pattern')
username  = __addon__.getSetting('username')
password = __addon__.getSetting('password')
show_tor = __addon__.getSetting('show_tor')
#checkaddon.do_block_check()


logos ={'nba':'http://bethub.org/wp-content/uploads/2015/09/NBA_Logo_.png',
'nhl':'https://upload.wikimedia.org/wikipedia/de/thumb/1/19/Logo-NHL.svg/2000px-Logo-NHL.svg.png',
'nfl':'http://www.shermanreport.com/wp-content/uploads/2012/06/NFL-Logo1.gif',
'mlb':'http://content.sportslogos.net/logos/4/490/full/1986.gif',
'soccer':'http://images.clipartpanda.com/soccer-ball-clipart-soccer-ball-clip-art-4.png'}


sd_streams = ['goindexsport','multi-sports.eu', 'watchnfl.live', 'streamhd.eu', 'vines.tn', 'apollofm.website',
			'giostreams.eu','watch-sportstv.boards.net', 'hdstream4u.com', 'stream24k.com', 'wizhdsports.com', 'antenasport.com', 
			'sportsnewsupdated.com', 'watchnba.tv', 'feedredsoccer.at.ua', 'jugandoes.com', 'wiz1.net', 'bosscast.net', 
			'watchsportstv.boards.net', 'tv-link.in', 'klivetv.co', 'videosport.me', 'livesoccerg.com', 'zunox.hk', 'singidunum.', 
			'zona4vip.com', 'ciscoweb.ml', 'streamendous.com','streamm.eu', 'sports-arena.net', 'stablelivestream.com', 
			'iguide.to', 'sportsleague.me','kostatz.com', 'soccerpluslive.com', 'zunox', 'apkfifa.com','watchhdsports.xyz','lovelysports2016.ml',
			'sports4u.live','tusalavip3.es.tl', 'neymargoals.com', 'crichd.sx', 'unitedstream.live','stream4us.info','freecast.xyz','focustream.info',
			's4power.club', 'footystreams.net', 'topstream.es.tl', 'pushmycar.cf','zifootball.us','hehestreams.xyz/nba/games',
			'bubbysports.ml', 'streamhdeu.net','sportz-hd.com','immortal-tv.net','besasport.top', 'nbalivestreams.net','genti.stream', 'yaboy.xyz',
			'eplstreams.club', 'gentistream.com','streamtoday.us','yoursportsinhd.com','nbastream.pw', 'apkadsense.com']

def utc_to_local(utc_dt):
    timestamp = calendar.timegm(utc_dt.timetuple())
    local_dt = datetime.fromtimestamp(timestamp)
    assert utc_dt.resolution >= timedelta(microseconds=1)
    return local_dt.replace(microsecond=utc_dt.microsecond)


UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'

def GetURL(url, referer=None, output=None, timeout=None, headers=None):
	if 'streamm.eu' in url:
		import cfscrape
		scraper = cfscrape.create_scraper()
		if headers:
			return scraper.get(url, headers=headers).content
		else: return scraper.get(url).content
	url = url.replace('///','//')
	request = urllib2.Request(url)
	request.add_header('User-agent', UA)
	if referer:
		request.add_header('Referer', referer)
	try:
		if timeout:
			response = urllib2.urlopen(request, timeout=int(timeout))
		else:
			response = urllib2.urlopen(request, timeout=20)
		if output == 'geturl':
			return response.geturl()
		if output == 'cookie':
			return response.info()['Set-Cookie']
		html = response.read()
		return html
	except:
		if 'reddit' in url:
			xbmcgui.Dialog().ok(__addonname__, 'Looks like '+url+' is down... Please try later...')
		return None


def getUrl(url,data=None,header={},cookies=None):
    if not header:
        header = {'User-Agent':UA}
    req = urllib2.Request(url,data,headers=header)
    response = urllib2.urlopen(req, timeout=15)
    if cookies=='':
        cookies=response.info()['Set-Cookie']
    link = response.read()
    response.close()
    return link


def GetJSON(url, referer=None):
    request = urllib2.Request(url)
    request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:36.0) Gecko/20100101 Firefox/36.0')
    if referer:
    	request.add_header('Referer', referer)
    try:
    	response = urllib2.urlopen(request, timeout=5)
    	f = response.read()
    	jsonDict = json.loads(f)
    	return jsonDict
    except:
    	xbmcgui.Dialog().ok(__addonname__, 'Looks like '+url+' is down... Please try later...')
    	return None

def GameStatus(status):
	statuses = {'pre-event':'Not started', 'mid-event':'[COLOR green]In progress[/COLOR]', 'post-event':'Completed', 'postponed':'Postponed'}
	if status in statuses:
		return statuses[status]
	else: return ''	

def Main():
	addDir("[COLOR=FF00FF00][ NBA GAMES ][/COLOR]", '', iconImg='http://bethub.org/wp-content/uploads/2015/09/NBA_Logo_.png', mode="nba")
	addDir("[COLOR=FF00FF00][ NHL GAMES ][/COLOR]", '', iconImg='https://upload.wikimedia.org/wikipedia/de/thumb/1/19/Logo-NHL.svg/2000px-Logo-NHL.svg.png', mode="nhl")
	addDir("[COLOR=FF00FF00][ NFL GAMES ][/COLOR]", '', iconImg='http://www.shermanreport.com/wp-content/uploads/2012/06/NFL-Logo1.gif', mode="nfl")
	addDir("[COLOR=FF00FF00][ MLB GAMES ][/COLOR]", '', iconImg='http://content.sportslogos.net/logos/4/490/full/1986.gif', mode="mlb")
	addDir("[COLOR=blue][ MY SUBREDDITS ][/COLOR]", '', iconImg='http://scitechconnect.elsevier.com/wp-content/uploads/2014/07/1reddit-logo2.png', mode="myreddit")
	addDir("[COLOR=FFFFFF00][ Archive ][/COLOR]", '', iconImg='special://home/addons/plugin.video.prosport/icon.png', mode="archive")
	xbmcplugin.endOfDirectory(h)

def Arch():
	addDir("[COLOR=FFFFFF00][ NBA Archive ][/COLOR]", '', iconImg='http://bethub.org/wp-content/uploads/2015/09/NBA_Logo_.png', mode="nbaarch")
	addDir("[COLOR=FFFFFF00][ NFL Archive ][/COLOR]", '', iconImg='http://www.shermanreport.com/wp-content/uploads/2012/06/NFL-Logo1.gif', mode="nflarch")
	addDir("[COLOR=FFFFFF00][ NHL Archive ][/COLOR]", '', iconImg='https://upload.wikimedia.org/wikipedia/de/thumb/1/19/Logo-NHL.svg/2000px-Logo-NHL.svg.png', mode="nhlarch")
	xbmcplugin.endOfDirectory(h)
	
def Games(mode):
	today = datetime.utcnow() - timedelta(hours=8)
	today_from = str(today.strftime('%Y-%m-%d'))+'T00:00:00.000-05:00'
	today_to = str(today.strftime('%Y-%m-%d'))+'T23:59:00.000-05:00'
	url = 'http://www.sbnation.com/sbn_scoreboard/ajax_leagues_and_events?ranges['+mode+'][from]='+today_from+'&ranges['+mode+'][until]='+today_to+'&_='+str(int(time.time()))
	js = GetJSON(url)
	js = js['leagues'][mode]
	if js:	
		if mode == 'nfl':
			addDir('[COLOR=FF00FF00][B]NFL Redzone[/B][/COLOR]', mode, iconImg=logos[mode], home='red zone', away='red zone', mode="prostreams")
		for game in js:
			home = game['away_team']['name']
			away = game['home_team']['name']
			if 'mlb' in mode:
				try:
					hs = str(game['score']['home'][game['score']['cols'].index('R')])
					if not hs:
						hs = '0'
				except:
					hs = '0'
				try:
					avs = str(game['score']['away'][game['score']['cols'].index('R')])
					if not avs:
						avs = '0'
				except:
					avs = '0'
			else:
				hs = str(game['score']['home'][game['score']['cols'].index('Total')])
				if not hs:
					hs = '0'
				avs = str(game['score']['away'][game['score']['cols'].index('Total')])
				if not avs:
					avs = '0'
			score = ' - '+avs+':'+hs
			start_time = game['start_time']
			try:
				plus = False
				st = start_time.replace('T', ' ')
				if '+' in st:
					plus = True
					str_new = st.split('+')[-1]
					st = st.replace('+'+str_new,'')
				else:
					str_new = st.split('-')[-1]
					st = st.replace('-'+str_new,'')
				str_new = str_new.split(':')[0]
				if plus:
					st_time_utc = datetime(*(time.strptime(st, '%Y-%m-%d %H:%M:%S')[0:6]))-timedelta(hours=int(str_new))
				else:
					st_time_utc = datetime(*(time.strptime(st, '%Y-%m-%d %H:%M:%S')[0:6]))+timedelta(hours=int(str_new))
				local_game_time = utc_to_local(st_time_utc)
				local_time_str = ' - '+local_game_time.strftime(xbmc.getRegion('dateshort')+' '+xbmc.getRegion('time').replace('%H%H','%H').replace(':%S',''))
			except:
				local_time_str = ''
			status = GameStatus(game['status'])
			status = ' - '+status
			title = '[COLOR=FF00FF00][B]'+game['title'].replace(game['title'].split()[-1],'')+'[/B][/COLOR]'
			if display_start_time=='true':
				title = title+'[COLOR=FFFFFF00]'+local_time_str+'[/COLOR]'
			if display_status=='true':
				title = title+'[COLOR=FFFF0000]'+status+'[/COLOR]'
			if display_score=='true':
				title = title+'[COLOR=FF00FFFF]'+score+'[/COLOR]'
			addDir(title, mode, iconImg=logos[mode], home=home, away=away, mode="prostreams")
	else:
		addDir("[COLOR=FFFF0000]Could not fetch today's "+mode.upper()+" games... Probably no games today?[/COLOR]", '', iconImg="", mode="")
	xbmcplugin.endOfDirectory(h, cacheToDisc=True)

def MyReddits():
	sys_url = sys.argv[0] + '?mode=addnew'
	item = xbmcgui.ListItem('[COLOR=FFFF0000][ Add new subreddit ][/COLOR]', iconImage='', thumbnailImage='')
	xbmcplugin.addDirectoryItem(handle=h, url=sys_url, listitem=item, isFolder=False)
	reddits = __addon__.getSetting('reddits').split(',')
	if len(reddits)>0:
		for reddit in reddits:
			popup = []
			uri = sys.argv[0] + "?url="+reddit+"&mode=edit"
			popup.append(('Edit subreddit', 'RunPlugin(%s)'%uri,))
			uri2 = sys.argv[0] + "?url="+reddit+"&mode=remove"
			popup.append(('Remove subreddit', 'RunPlugin(%s)'%uri2,))
			if ':' in reddit:
				title = reddit.split(":")[0]
				pattern = ''
				if display_pattern == 'true':
					pattern = " - "+reddit.split(":")[-1]
				if len(title)>0:
					addDir2("[COLOR=FF00FF00][ "+title.upper()+" ]"+pattern+"[/COLOR]", reddit, '', iconImg='', popup=popup, mode="topics")
			else:
				if len(reddit)>0:
					addDir2("[COLOR=FF00FF00][ "+reddit.upper()+" ][/COLOR]", reddit, '', iconImg='', popup=popup, mode="topics")
	xbmcplugin.endOfDirectory(h)

def Topics(url):
	r = praw.Reddit(user_agent='xbmc pro sport addon')
	if username and password:
		try:
			r.login(username, password)
		except:
			dialog = xbmcgui.Dialog()
			dialog.notification('Pro Sport', 'Please make sure reddit login and password are correct', xbmcgui.NOTIFICATION_WARNING, 3000)
	r.config.api_request_delay = 0
	for submission in r.get_subreddit(url.split(':')[0]).get_hot(limit=30):
		if ":" in url:
			pattern = url.split(":")[-1]
			if pattern.lower() in submission.title.encode('utf-8').lower():
				addDir("[COLOR=FFFFFF00][ "+submission.title.encode('utf-8')+" ][/COLOR]", submission.id, iconImg='', home=submission.title.encode('utf-8'), away='', mode="mystreams")
		else:
			addDir("[COLOR=FFFFFF00][ "+submission.title.encode('utf-8')+" ][/COLOR]", submission.id, iconImg='', home=submission.title.encode('utf-8'), away='', mode="mystreams")
	xbmcplugin.endOfDirectory(h)

def Addnew():
	kbd = xbmc.Keyboard()
	kbd.setDefault('')
	kbd.setHeading("Add new subreddit")
	kbd.doModal()
	s = None
	if kbd.isConfirmed():
	    s = kbd.getText()
	words = []
	history = __addon__.getSetting('reddits')
	if history:
	    words = history.split(",")
	if s and s not in words:
	    words.append(s)
	    __addon__.setSetting('reddits', ','.join(words))
	xbmc.executebuiltin("Container.Refresh")

def Edit(url):
	kbd = xbmc.Keyboard()
	kbd.setDefault(url)
	kbd.setHeading("Edit subreddit")
	kbd.doModal()
	s = None
	if kbd.isConfirmed():
	    s = kbd.getText()
	words = []
	history = __addon__.getSetting('reddits')
	if history:
	    words = history.split(",")
	for el in words:
		if el==url and s:
			words[words.index(el)] = s
	__addon__.setSetting('reddits', ','.join(words))
	xbmc.executebuiltin("Container.Refresh")

def Remove(url):
	title = xbmc.getInfoLabel('ListItem.Title')
	title = title.replace('[COLOR=FFFFFF00][','').replace('][/COLOR]','').strip()
	reddits = __addon__.getSetting('reddits').split(',')
	reddits = [x.lower() for x in reddits]
	reddits.remove(url.lower())
	__addon__.setSetting('reddits', ','.join(reddits))
	xbmc.executebuiltin("Container.Refresh")

def getProStreams(ur, home, away):
	orig_title = '[COLOR=FF00FF00][B]'+away+' at '+home+'[/B][/COLOR]'
	if 'redzone' in orig_title:
		orig_title = '[COLOR=FF00FF00][B]NFL Redzone[/B][/COLOR]'
	home_f = home.lower().split()[0]
	away_f = away.lower().split()[0]
	home_l = home.lower().split()[-1]
	away_l = away.lower().split()[-1]
	r = praw.Reddit(user_agent='xbmc pro sport addon')
	r.config.api_request_delay = 0
	links=[]
	for submission in r.get_subreddit(ur+'streams').get_hot(limit=30):
		if (home_l in submission.title.lower() and away_l in submission.title.lower()) or (home_f in submission.title.lower() and away_l in submission.title.lower()) or (home_l in submission.title.lower() and away_f in submission.title.lower()) or (home_f in submission.title.lower() and away_f in submission.title.lower()):
			regex = re.compile(r'(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))',re.IGNORECASE)
			link = re.findall(regex, submission.selftext.encode('utf-8'))
			links = links + link
			flat_comments = praw.helpers.flatten_tree(submission.comments)
			for comment in flat_comments:
				if not isinstance(comment,praw.objects.Comment):
					flat_comments.remove(comment)
			try:
				flat_comments.sort(key=lambda comment: comment.score , reverse=True)
			except:
				pass
			for comment in flat_comments:
				try:
					link = re.findall(regex, comment.body.encode('utf-8'))
					links = links + link
				except:
					pass	
	if links:
		DisplayLinks(links, orig_title)
	else:
		addDir("[COLOR=FFFF0000]Could not find any streams on reddit...[/COLOR]", '', iconImg="", mode="")
		xbmcplugin.endOfDirectory(h, cacheToDisc=True)

def getMyStreams(url, home):
	r = praw.Reddit(user_agent='xbmc pro sport addon')
	if username and password:
		try:
			r.login(username, password)
		except:
			dialog = xbmcgui.Dialog()
			dialog.notification('Pro Sport', 'Please make sure reddit login and password are correct', xbmcgui.NOTIFICATION_WARNING, 3000)
	r.config.api_request_delay = 0
	submission = r.get_submission(submission_id=url)
	links=[]
	regex = re.compile(r'(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))',re.IGNORECASE)
	link = re.findall(regex, submission.selftext.encode('utf-8'))
	links = links + link
	flat_comments = praw.helpers.flatten_tree(submission.comments)
	for comment in flat_comments:
		if not isinstance(comment,praw.objects.Comment):
			flat_comments.remove(comment)
	try:
		flat_comments.sort(key=lambda comment: comment.score , reverse=True)
	except:
		pass
	for comment in flat_comments:
		try:
			link = re.findall(regex, comment.body.encode('utf-8'))
			links = links + link
		except:
			pass
	if links:
		DisplayLinks(links, home)
	else:
		addDir("[COLOR=FFFF0000]Could not find any streams...[/COLOR]", '', iconImg="", mode="")
		xbmcplugin.endOfDirectory(h, cacheToDisc=True)


def DisplayLinks(links, orig_title):	
	urls = []
	for url in links:
		url = url[0]
		if 'http://' not in url and 'https://' not in url and 'sop://' not in url and 'acestream://' not in url:
			url = 'http://www.'+url
		if url not in urls and 'blabseal.com' in url:
			addLink('Blabseal.com', orig_title, url, mode="play")
			urls.append(url)
		if url not in urls and 'iceballet' in url:
			addLink('Iceballet', orig_title, url, mode="play")
			urls.append(url)
		if url not in urls and 'nbastreams.pw' in url:
			addLink('nbastreams.pw', orig_title, url, mode="play")
			urls.append(url)
		elif url not in urls and '1apps.com' in url:
			addLink('Oneapp', orig_title, url, mode="play")
			urls.append(url)
		elif url not in urls and '//youtu' in url or '.youtu' in url and 'list' not in url:
			addLink('Youtube.com', orig_title, url, mode="play")
			urls.append(url)
		elif url not in urls and 'freecast.in' in url:
			addLink('Freecast.in', orig_title, url, mode="play")
			urls.append(url)
		elif url not in urls and 'streamsus.com' in url:
			addLink('Streamsus.com', orig_title, url, mode="play")
			urls.append(url)
		elif url not in urls and 'streamboat.tv' in url:
			addLink('Streamboat.tv', orig_title, url, mode="play")
			urls.append(url)
		elif url not in urls and '305sports.xyz' in url:
			addLink('305sports.xyz', orig_title, url, mode="play")
			urls.append(url)
		elif url not in urls and 'nbastream.net' in url:
			addLink('Nbastream.net', orig_title, url, mode="play")
			urls.append(url)
		elif url not in urls and 'nhlstream.net' in url:
			addLink('Nhlstream.net', orig_title, url, mode="play")
			urls.append(url)
		elif url not in urls and 'livenflstream.net' in url:
			addLink('Livenflstream.net', orig_title, url, mode="play")
			urls.append(url)
		elif url not in urls and 'fs.anvato.net' in url:
			addLink('Fox ToGo (US IP Only)', orig_title, url, mode="play")
			urls.append(url)
		elif url not in urls and 'mlblive-akc' in url:
			addLink('MLB app', orig_title, url, mode="play")
			urls.append(url)
		elif url not in urls and 'streamsarena.eu' in url:
			addLink('Streamsarena.eu', orig_title, url, mode="play")
			urls.append(url)
		elif url not in urls and 'ustream.tv' in url:
			addLink('Ustream.tv', orig_title, url, mode="play")
			urls.append(url)
		elif url not in urls and 'streamup.com' in url and 'm3u8' not in url:
			addLink('Streamup.com', orig_title, url, mode="play")
			urls.append(url)
		elif url not in urls and 'torula' in url:
			addLink('Torula.us', orig_title, url, mode="play")
			urls.append(url)
		elif url not in urls and 'webm' in url or ('caststreams' in url and 'getGame' in url):
			addLink('caststreams', orig_title, url, mode="play")
			urls.append(url)
		elif url not in urls and 'gstreams.tv' in url:
			addLink('Gstreams.tv', orig_title, url, mode="play")
			urls.append(url)
		elif url not in urls and 'nfl-watch.com/live/watch' in url or 'nfl-watch.com/live/-watch' in url or 'nfl-watch.com/live/nfl-network' in url:
			addLink('Nfl-watch.com', orig_title, url, mode="play")
			urls.append(url)
		elif url not in urls and 'ducking.xyz' in url:
			addLink('Ducking.xyz', orig_title, url, mode="play")
			urls.append(url)
		elif url not in urls and 'streamandme' in url:
			addLink('Streamandme', orig_title, url, mode="play")
			urls.append(url)
		elif url not in urls and 'henno.info' in url:
			addLink('Henno', orig_title, url, mode="play")
			urls.append(url)
		elif url not in urls and 'stream2hd.net' in url:
			addLink('Stream2hd', orig_title, url, mode="play")
			urls.append(url)
		elif url not in urls and 'moonfruit.com' in url:
			addLink('Moonfruit', orig_title, url, mode="play")
			urls.append(url)
		elif url not in urls and 'castalba.tv' in url:
			addLink('Castalba', orig_title, url, mode="play")
			urls.append(url)
		elif ('room' in url or 'YES' in url) and 'm3u8' in url:
			room = url.split('/')[6]
			if room not in urls:
				addLink('Room HD (US IP Only)', orig_title, url, mode="play")
				urls.append(room)
		elif url not in urls and '101livesportsvideos.com' in url and 'ace' not in url:
			addLink('101livesportsvideos.com', orig_title, url, mode="play")
			urls.append(url)
		elif url not in urls and '.m3u8' in url and 'room' not in url and 'anvato' not in url and 'mlblive-akc' not in url and 'YES' not in url:
			addLink('M3U8 stream', orig_title, url, mode="play")
			urls.append(url)
		if url not in urls and any(el in url for el in sd_streams):
			title = '(stream)'
			try:
				title = urlparse.urlparse(url).netloc
			except:
				pass
			addLink(title, orig_title, url, mode="play")
			urls.append(url)
		if show_tor=='true':
			if url not in urls and'acestream://' in url:
				addLink('Acestream', orig_title, url, mode="play")
				urls.append(url)
			if url not in urls and'sop://' in url:
				addLink('Sopcast', orig_title, url, mode="play")
				urls.append(url)			
	xbmcplugin.endOfDirectory(h, cacheToDisc=True)
	
def ParseLink(el, orig_title):
	el = el.replace('www.www','www')
	if 'caststreams' in el:
		url = Caststreams(orig_title)
		return url
	elif any(e in el for e in sd_streams):
		url = Universal(el)
		return url
	elif 'blabseal.com' in el:
		url = Blabseal(el)
		return url
	elif 'openload.co' in el:
		url = Openload(el)
		return url
	elif 'iceballet' in el:
		url = Universal(el)
		return url
	elif 'youtu' in el and 'list' not in el:
		url = Universal(el)
		return url
	elif 'freecast.in' in el:
		url = Freecastin(el)
		return url
	elif 'nbastreams.pw' in el:
		url = Universal(el)
		return url
	elif '1apps.com' in el:
		url = Oneapp(el)
		return url
	elif 'streamsus.com' in el:
		url = Universal(el)
		return url
	elif '305sports.xyz' in el:
		url = Threesports(el)
		return url
	elif 'ustream.tv' in el:
		url = Ustream(el)
		return url
	elif 'streamboat.tv' in el:
		url = Streambot(el)
		return url
	elif 'nbastream.net' in el:
		url = Universal(el)
		return url
	elif 'nhlstream.net' in el:
		url = Universal(el)
		return url
	elif 'livenflstream.net' in el:
		url = Universal(el)
		return url
	elif 'fs.anvato.net' in el:
		url = Getanvato(el)
		return url
	elif 'mlblive-akc' in el:
		url = Getmlb(el)
		return url
	elif 'streamsarena.eu' in el:
		url = Universal(el)
		return url
	elif 'streamup.com' in el and 'm3u8' not in el:
		url = GetStreamup(el.split('/')[3])
		return url
	elif 'torula' in el:
		url = Torula(el)
		return url
	elif 'acestream' in el or 'sop:' in el:
		url = Torrent(el)
		return url
	elif 'gstreams.tv' in el:
		url = Universal(el)
		return url
	elif 'nfl-watch.com/live/watch' in el or 'nfl-watch.com/live/-watch' in el or 'nfl-watch.com/live/nfl-network' in el:
		url = Nflwatch(el)
		return url
	elif 'ducking.xyz' in el:
		url = Ducking(el)
		return url
	elif 'webm' in el or ('caststreams' in el and 'getGame' in el):
		url = el
		return url
	elif 'streamandme' in el:
		url = Universal(el)
		return url
	elif 'henno.info' in el:
		url = Henno(el)
		return url
	elif 'stream2hd.net' in el:
		url = Stream2hd(el)
		return url
	elif 'moonfruit.com' in el:
		url = Moonfruit(el)
		return url
	elif 'castalba.tv' in el:
		url = Castalba(None, el)
		return url
	elif ('room' in el or 'YES' in el) and 'm3u8' in el:
		url = Getroom(el)
		return url
	elif '101livesportsvideos.com' in el:
		url = Universal(el)
		return url
	elif '.m3u8' in el and 'room' not in el and 'anvato' not in el and 'mlblive-akc' not in el:
		return el
				

def strip_non_ascii(string):
    stripped = (c for c in string if 0 < ord(c) < 127)
    return ''.join(stripped)

def Archive(page, mode):
	if mode == 'nhlarch':
		url = 'http://www.life2sport.com/category/hockey/page/'+str(page)
	if mode == 'nbaarch':
		url = 'http://www.life2sport.com/category/basketbol/nba/page/'+str(page)
	elif mode == 'nflarch':
		url = 'http://www.life2sport.com/category/american-football/page/'+str(page)
	html = GetURL(url)
	links = common.parseDOM(html, "a", attrs={"rel": "bookmark"}, ret="href")
	titles = common.parseDOM(html, "a", attrs={"rel": "bookmark"}, ret="title")
	if links:
		del links[1::2]
	for i, el in enumerate(links):
		if '-nba-' in el or '-nfl-' in el or '-nhl-' in el:
			title = common.parseDOM(html, "a", attrs={"href": el}, ret="title")[0]
			title = strip_non_ascii(title)
			title = title.replace('&#8211;','').strip()
			#title = title.replace('[RU]','')
			titles = title.split('/')
			week = ''
			for tit in titles:
				if len(tit)>25:
					title = tit
				if 'week' in tit or 'Week' in tit or 'WEEK' in tit:
					week = tit
			title = title + week
			addDir(title, el, iconImg=logos[mode[0:3]], mode="playarchive")
	uri = sys.argv[0] + '?mode=%s&page=%s' % (mode, str(int(page)+1))
	item = xbmcgui.ListItem("next page...", iconImage='', thumbnailImage='')
	xbmcplugin.addDirectoryItem(h, uri, item, True)
	xbmcplugin.endOfDirectory(h, cacheToDisc=True)

def Nhlarchive(url, page, mode):
	page = int(page)-1
	link = 'https://my.mail.ru/cgi-bin/my/ajax?user=atl17@bk.ru&xemail=&ajax_call=1&func_name=video.get_list&mna=&mnb=&arg_type=album_items&arg_all=1&sort=default&arg_offset='+str(page)+'&arg_limit=20'
	json = GetJSON(link)
	json = json[2]['items']
	for el in json:
		title = el['Title']
		videoUrl = el['MetaUrl']
		img = el['UrlJpg']
		if 'NHL' in title:
			addDir(title, videoUrl, iconImg=img, mode="playnhlarchive")
	uri = sys.argv[0] + '?mode=%s&page=%s&url=%s' % (mode, str(int(page)+10),url)
	item = xbmcgui.ListItem("next page...", iconImage='', thumbnailImage='')
	xbmcplugin.addDirectoryItem(h, uri, item, True)
	xbmcplugin.endOfDirectory(h, cacheToDisc=True)

def Playnhlarchive(url):
	orig_title = xbmc.getInfoLabel('ListItem.Title')
	cookieJar = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar), urllib2.HTTPHandler())
	conn = urllib2.Request(url)
	connection = opener.open(conn)
	f = connection.read()
	connection.close()
	js = json.loads(f)
	for cookie in cookieJar:
		token = cookie.value
	js = js['videos']
	for el in js:
		addDirectLink('mail.ru - '+el['key'], {'Title': orig_title}, 'http:'+el['url']+'|Cookie=video_key='+token)
	xbmcplugin.endOfDirectory(h, cacheToDisc=True)
	
def PlayArchive(url):
	orig_title = xbmc.getInfoLabel('ListItem.Title')
	html = GetURL(url)
	html = html.split('>ENGLISH<')[-1]
	links = common.parseDOM(html, "iframe", ret="src")
	lnks = common.parseDOM(html, "a", ret="href")
	links = links+lnks
	for i, link in enumerate(links):
		if 'mail.ru/vid' in link:
			link = link.replace('https://videoapi.my.mail.ru/videos/embed/mail/','https://my.mail.ru/+/video/meta/')
			link = link.replace('https://my.mail.ru/video/embed/','https://my.mail.ru/+/video/meta/')
			link = link.replace('html','json')
			cookieJar = cookielib.CookieJar()
			opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar), urllib2.HTTPHandler())
			conn = urllib2.Request(link)
			connection = opener.open(conn)
			f = connection.read()
			connection.close()
			js = json.loads(f)
			for cookie in cookieJar:
				token = cookie.value
			js = js['videos']
			for el in js:
				addDirectLink('mail.ru - '+el['key'], {'Title': orig_title}, 'https:'+el['url']+'|Cookie=video_key='+token)
		elif 'openload.co' in link:
			addLink('openload', orig_title, link, mode="play")
	xbmcplugin.endOfDirectory(h, cacheToDisc=True)


def GetStreamup(channel):
	try:
		chan = GetJSON('https://api.streamup.com/v1/channels/'+channel)
		if chan['channel']['live']:
			videoId = chan['channel']['capitalized_slug'].lower()
			domain = GetURL('https://lancer.streamup.com/api/redirect/'+videoId)
			return 'https://'+domain+'/app/'+videoId+'_aac/playlist.m3u8'
	except:
		return None	

def GetYoutube(url):
	try:
		url = url.replace('*','')
		if ('channel' in url or 'user' in url) and 'live' in url:
			html = GetURL(url)
			videoId = html.split("'VIDEO_ID':")[-1].split('",')[0].replace('"','').replace(' ','')
			link = 'plugin://plugin.video.youtube/play/?video_id=' + videoId
			return link
		regex = (r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
		youtube_regex_match = re.match(regex, url)
		videoId = youtube_regex_match.group(6)
		link = 'plugin://plugin.video.youtube/play/?video_id=' + videoId
		return link
	except:
		return None
		
def Torrent(url):
	if 'sop://'in url:
		url = urllib.quote(url.rstrip('`#$%^&*@!":;.,?[]{}+=-_<>'))
		url='plugin://program.plexus/?mode=2&url=%s&name=%s'%(url,'Sopcast')
	elif 'acestream://' in url or '.acelive' in url:
		url = urllib.quote(url.rstrip('`#$%^&*@!":;.,?[]{}+=-_<>'))
		url='plugin://program.plexus/?mode=1&url=%s&name=%s'%(url,'Acestream')
	return url
		
def Getmlb(url):
	try:
		if 'master' in url:
			return url
		else:	 
			lst = url.split('/')
			link = url.replace(lst[len(lst)-2],'3000K').replace(lst[len(lst)-1],'3000_slide.m3u8')
			return link
	except:
		return None
		
def Openload(url):
	import urlresolver
	media_url = urlresolver.resolve(url)
	return media_url 

def Threesports(url):
	try:
		html = GetURL(url)
		links = common.parseDOM(html, "h1")
		for link in links:
			if 'go to stream' in link.lower():
				html = link
				break
		link = common.parseDOM(html, "a", ret="href")[0]
		link = Universal(link)
		return link
	except:
		return None

def Getanvato(url):
	try:
		if 'master' in url:
			return url
		else:	 
			lst = url.split('/')
			link = url.replace(lst[len(lst)-2],'4028k')
			return link
	except:
		return None
		
def Getroom(url):
	try:
		if 'master' in url:
			return url
		else:	 
			lst = url.split('/')
			link = url.replace(lst[len(lst)-2],'4028k')
			return link
	except:
		return url
		
def Blabseal(url):
	try:
		url = GetURL(url, output='geturl')
		if not url.endswith('/'):
			url = url+'/'
		html = GetURL(url, referer=url)
		link = common.parseDOM(html, "iframe", ret="src")[0]
		if 'philpastrami.tk' in link:
			return 'http://philpastrami.tk/serve/hd.m3u8'
		link = url+link
		html = GetURL(link, referer=link)
		if 'Clappr.Player' in html and 'm3u8' in html:
			lnk = re.findall("source: '(.*?)'", html)[0]
			if 'http' not in lnk:
				return link+lnk		
			else:
				return link
		javasc = re.findall('(eval.*\))', html)[0]
		import js2py
		context = js2py.EvalJs()
		if 'jwplayer' in html:
			jsplayers = '''var jwobject = [];
            	jwobject.results = null;
            	jwobject.setup = function(args) {jwobject.results = args};
            	var jwplayer = function() {return jwobject};'''
			context.execute(jsplayers)
			context.execute(javasc)
			return context.jwobject.results.file
		else:
			context.execute('''pyimport jstools;
           		var escape = jstools.escape;
            	var unescape = jstools.unescape;
            	var document = [];
            	document.result = "";
            	document.domain = "";
            	document.write = function(markup){ document.result = document.result + markup };''')
			context.swidth = '400'
			context.sheight = '400'
			context.document.domain = urlparse.urlparse(link).netloc
			context.execute(javasc)
			html = context.document.result
			if '<iframe' in html:
				link = common.parseDOM(html, "iframe", ret="src")[0]
				if 'youtu' in link:
					lnk = GetYoutube(link)
					return lnk
				elif 'dailymotion.com/embed' in link:
					lnk = Dailymotion(link)
					return lnk
				elif 'ustream.tv' in link:
					lnk = Ustream(link)
					return lnk
			elif '<video' in html:
				link = re.findall("src=[\"\'](.*?)[\"\']", html)[0]
				if 'http' in link:
					return link
				elif link.startswith('/'):
					return 'http://blabseal.com'+link
	except:
		return None
		
def Dailymotion(url):
	try:
		html = GetURL(url)
		link = 	re.findall('stream_chromecast_url":"(.*?)"', html)[0].replace("\\", "")
		link = GetURL(link, output='geturl')
		return link
	except:
		return None

def Ustream(url):
	try:
		html = GetURL(url)
		link = 	re.findall('"hls":"(.*?)"', html)[0].replace("\\", "")
		return link
	except:
		return None
	
		
def Torula(url):
	try:
		html = GetURL(url)
		block_content = common.parseDOM(html, "input", attrs={"id": "vlc"}, ret="value")[0]
		link = block_content
		return link
	except:
		return None


def Nbastreamspw(url):
	try:
		html = GetURL(url)
		block_content = common.parseDOM(html, "iframe", ret="src")[0]
		link = block_content.split('#')[-1]
		return link
	except:
		return None

def Freecastin(url):
	try:
		html = GetURL(url)
		block_content = common.parseDOM(html, "iframe", attrs={"width": "100%"}, ret="src")[0]
		link = GetYoutube(block_content)
		return link
	except:
		return None
		
def Oneapp(url):
	try:
		html = GetURL(url)
		link = re.findall("(http.+?dotstream.tv/.+?)[\"\']",html)[0]
		link = link.replace('/pl?','/player.php?')
		html = GetURL(link)
		a=int(re.search('a = ([0-9]+)',html).group(1))
		b=int(re.search('b = ([0-9]+)',html).group(1))
		c=int(re.search('c = ([0-9]+)',html).group(1))
		d=int(re.search('d = ([0-9]+)',html).group(1))
		f=int(re.search('f = ([0-9]+)',html).group(1))
		v_part = re.search('v_part = \'(.*?)\';',html).group(1)
		swfUrl='http://dotstream.tv/jwp/jwplayer.flash.swf'
		video_link = 'rtmp://%d.%d.%d.%d/'%(a/f,b/f,c/f,d/f) + v_part.split('/')[1]+'/'+' playpath='+v_part.split('/')[-1]
		video_link = video_link + ' swfUrl='+swfUrl + ' swfVfy=1 live=1 timeout=13 pageUrl='+link
		return video_link
	except:
		return None
		
def Streamsus(url):
	try:
		html = GetURL(url)
		block_content = common.parseDOM(html, "iframe", ret="src")[0]
		link = GetYoutube(block_content)
		return link
	except:
		pass
	try:
		html = GetURL(url)
		block_content = common.parseDOM(html, "a", ret="href")[0]
		if 'streamboat' in block_content:
			link = Streambot(block_content)
			return link
	except:
		pass
	try:
		html = GetURL(url)
		link = re.findall("'file':(.*?)'", html)[0].replace("'","")
		if 'm3u8' in link:
			return link
		elif 'youtu' in link:
			link = GetYoutube(link)
			return link
	except:
		return None

			
def Streambot(url):
	try:
		html = GetURL(url, referer=url)
		link2 = re.findall('playlist_url": "(.*?)"', html)[0]
		link1 = re.findall('cdn_host": "(.*?)"', html)[0]
		link = 'http://'+link1+link2
		return link
	except:
		return None
	

def Henno(url):
	try:
		url = 'http://henno.info/stream?stream=Streamup&source=&template=any&ticket=&user='
		html = GetURL(url)
		link = common.parseDOM(html, "iframe",  ret="src")[0]
		channel = link.split('/')[3]
		link = GetStreamup(channel)
		return link
	except:
		return None
		
def Stream2hd(url):
	try:
		html = GetURL(url)
		link = common.parseDOM(html, "iframe",  ret="src")[0]
		if 'streamup' in link:
			channel = link.split('/')[3]
			link = GetStreamup(channel)
			return link
	except:
		return None
	
		
def Moonfruit(url):
	try:
		cookieJar = cookielib.CookieJar()
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar), urllib2.HTTPHandler())
		conn = urllib2.Request(url)
		connection = opener.open(conn, timeout=5)
		for cookie in cookieJar:
			token = cookie.value
		headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:36.0) Gecko/20100101 Firefox/36.0",
            "Content-Type" : "application/x-www-form-urlencoded",
            "Cookie":"markc="+token,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.8,bg;q=0.6,it;q=0.4,ru;q=0.2,uk;q=0.2",
		}
		html = connection.read()
		link = common.parseDOM(html, "iframe",  ret="src")
		link = url+link[-1]
		conn = urllib2.Request(link, headers=headers)
		connection = opener.open(conn, timeout=5)
		html = connection.read()
		link = common.parseDOM(html, "iframe",  ret="src")[0]
		if 'streamup.com' in link:
			channel = link.split('/')[3]
			link = GetStreamup(channel)
			return link
	except:
		return None

def Nflwatch(url):
	try:
		html = GetURL(url)
		links = common.parseDOM(html, "iframe",  ret="src")
		for link in links:
			if 'streamup' in link:
				channel = link.split('/')[3]
				link = GetStreamup(channel)
				return link
			else:
				continue
		if 'p2pcast' in html:
			id = html.split("'text/javascript'>id='")[-1]
			id = id.split("';")[0]
			link = p2pcast(id)
			return link
	except:
		return None

def Ducking(url):
	try:
		html = GetURL(url)
		link = common.parseDOM(html, "iframe", ret="src")[1]
		url = 'http://www.ducking.xyz/quack/'+link
		html = GetURL(url, referer=url)
		if 'p2pcast' in html:
			id = html.split('php?id=')[-1].split('&')[0]
			link = p2pcast(id)
			return link
	except:
		return None
	

def Castalba(id, url):
	try:
		try:
			cid  = urlparse.parse_qs(urlparse.urlparse(url).query)['cid'][0] 
		except:
			try:
				cid = re.compile('channel/(.+?)(?:/|$)').findall(url)[0]
			except:
				pass
		try:
			referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
		except:
			referer='http://castalba.tv'        
		if id:
			cid = id
		url = 'http://castalba.tv/embed.php?cid=%s&wh=600&ht=380&r=%s'%(cid,urlparse.urlparse(referer).netloc)
		pageUrl=url
		request = urllib2.Request(url)
		request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:36.0) Gecko/20100101 Firefox/36.0')
		request.add_header('Referer', referer)
		response = urllib2.urlopen(request, timeout=5)
		result = response.read()
		result=urllib.unquote(result)
		if 'm3u8' in result:
			link = re.findall("var filez = '(.+?)'", result)[0]
			link = 'http://' + link + '.m3u8'
			link += '|User-Agent='+UA+'&Referer='+url+'&X-Requested-With=ShockwaveFlash/23.0.0.166'       
		else:
			try:
				filePath = re.compile("'file'\s*:\s*(?:unescape\()?'(.+?)'").findall(result)[0]
			except:
				file = re.findall('var file\s*=\s*(?:unescape\()?(?:\'|\")(.+?)(?:\'|\")',result)[0]
				try:
					file2 = re.findall("'file':\s*unescape\(file\)\s*\+\s*unescape\('(.+?)'\)",result)[0]
					filePath = file+file2
				except:
					filePath = file
			swf = re.compile("'flashplayer'\s*:\s*\"(.+?)\"").findall(result)[0]
			'''try:
				streamer=re.findall('streamer\(\)\s*\{\s*return \'(.+?)\';\s*\}',result)
				if 'rtmp' not in streamer:
					streamer = 'rtmp://' + streamer
			except:
				try:
					streamer = re.compile("var sts\s*=\s*'(.+?)'").findall(result)
				except:
					streamer=re.findall('streamer\(\)\s*\{\s*return \'(.+?)\';\s*\}',result)'''
			try:
				streamer = re.findall("('://.+?\live)",result)[-1]
				streamer = 'rtmp' + streamer.replace("'","")
			except:
				streamer = re.findall("(rtmp://.+?\live)",result)[0]
			link = streamer.replace('///','//') + ' playpath=' + filePath +' swfUrl=' + swf + ' flashver=WIN\\2020,0,0,228 live=true timeout=15 swfVfy=true pageUrl=' + pageUrl
		return link
	except:
		return None


def Universal(url):
	if 's4power.club' in url:
		url = url.replace('s4zona','zona')
	if 'sawlive' in url:
		lnk = sawresolve(url, url)
		return lnk
	if 'streamup' in url:
		if 'm3u8' in url:
			return url
		channel = url.split('/')[3]
		link = GetStreamup(channel)
		return link
	if 'youtu' in url:
		link = GetYoutube(url)
		return link
	if 'dailymotion.com/embed' in url:
		link = Dailymotion(url)
		return link
	if 'ustream.tv' in url:
		link = Ustream(url)
		return link
	if 'kostatz.com' in url:
		url = 'http://admin1.ninacdn.com/iframe.php?c=peanutly&s=peanutly'
	if 'iguide.to' in url:
		link = iguide(url)
		return link
	if 'lshstream' in url:
		link = lshstream(url)
		return link
	if 'player.twitch.tv' in url:
		videoId = url.split('=')[-1]
		link = 'plugin://plugin.video.twitch/playLive/'+videoId+'/'
		return link
	if 'rocktv.co' in url:
		id = url.split("live=")[-1].split("&")[0]
		link = rocktv(id)
		return link
	if 'p2pcast' in url and 'streamcdn' in url:
		link = p2pcast2(url)
		return link
	if 'hdcast.org' in url:
		id = url.split('u=')[-1].split('&')[0]
		link = hdcast(id)
		return link
	if 'm3u8' in url:
		return url
	if 'adplus/adpluslive.html?id=/' in url:
		url = url.replace('adplus/adpluslive.html?id=/','')
	if 'http://www.nullrefer.com/?' in url:
		url = url.replace('http://www.nullrefer.com/?','')
	html = GetURL(url, referer=url)
	if html and 'weplayer.pw' in html:
		id = html.split("'text/javascript'>id='")[-1]
		id = id.split("';")[0]
		link = weplayer(id)
		return link
	if html and 'player.twitch.tv' in html:
		videoId = re.findall('channel=(.*?)[\"\']', html)[0]
		link = 'plugin://plugin.video.twitch/playLive/'+videoId+'/'
		return link
	elif html and 'castalba.tv' in html:
		id = html.split('<script type="text/javascript"> id="')[-1]
		id = id.split('";')[0]
		link = Castalba(id, url)
		return link
	elif html and 'p2pcast' in html and 'streamcdn' not in html:
		id = html.split("'text/javascript'>id='")[-1]
		id = id.split("';")[0]
		link = p2pcast(id)
		return link
	elif html and 'castup' in html:
		id = html.split('fid="')[-1].split('";')[0]
		link = castup(id)
		return link
	elif html and 'cast4u' in html and 'fid=' in html:
		id = html.split("fid='")[-1].split("';")[0]
		link = cast4u(id)
		return link
	elif html and 'rocktv.co' in html and 'live=' not in html:
		id = html.split("fid='")[-1].split("';")[0]
		link = rocktv(id)
		return link
	elif html and 'castamp.com' in html:
		id = html.split('<script type="text/javascript">channel="')[-1].split('";')[0]
		link = castamp(id)
		return link
	elif html and ('101livesportsvideos' in url or 'watchhdsports' in url) and 'youtu' in html: 
		url = re.findall('(youtu.+?)"',html)[0]
		link = GetYoutube(url)
		return link
	elif html and 'bro.adca.st' in html and 'broadcast/close.gif' not in html:
		id = html.split("<script type='text/javascript'>id='")[-1].split("';")[0]
		link = broadcast(id, url)
		return link
	elif html and 'streamking.cc' in html:
		id = re.findall("(http://streamking.+?)[\"\']",html)[0]
		link = streamking(id)
		return link
	elif html and 'hdcast.org' in html and 'fid=' in html:
		id = html.split('fid="')[-1].split('";')[0]
		link = re.findall("(http.+?hdcast.org/.+?)[\"\']",html)[0]
		html = GetURL(link)
		link = re.findall("(http.+?hdcast.org/.+?)[\"\']",html)[0]
		link = link+id
		link = hdcast(link, url)
		return link
	elif html and 'sostart.pw' in html and 'fid=' in html:
		id = html.split('fid="')[-1]
		id = id.split('";')[0]
		url = 'http://www.sostart.pw/jwplayer6.php?channel='+id
		link = sostart(url)
		return link
	elif html and 'https://streamboat.tv/@' in html:
		url = html.split('https://streamboat.tv/@')[-1].split('"')[0]
		url = 'https://streamboat.tv/@'+url
		url = Streambot(url)
		return url
	elif html and 'sawlive.tv' in html:
		link = re.findall("src=[\"\'](http.+?sawlive.tv/embed/.+?)[\"\']",html)[0]
		link = sawresolve(link, url)
		return link
	elif html and 'shidurlive.com' in html:
		link = re.findall("src='(http.+?shidurlive.com/embed/.+?)'",html)[0]
		link = sawresolve(link, url)
		return link
	elif html and 'pushmycar.cf' in url and 'embed.js' in html and 'fid=' in html:
		fid = html.split('fid="')[-1].split('";')[0]
		link = 'http://wizhdsports.be/live/'+ fid +'.php'
		link = Universal(link)
		return link
	elif html and ('.m3u8' in html or 'rtmp:' in html or '.f4m' in html or 'chrome-extension' in html or 'contentgate' in html):
		html = urllib.unquote_plus(html)
		links = re.findall("[file|source|hls|src|stream1|videoLink]\s*[:|=]\s*[\"\'](.*?)[\"\']", html)
		for link in links:
			if '.m3u8' in link or 'rtmp:' in link or 'f4m' in link or 'chrome-extension' in link or 'contentgate' in link:
				link = link.replace('src=','')
				link = link.replace('amp;','')	
				if 'chrome-extension' in link:
					link = link.split('#')[-1]
				if 'smotrimult' in link or 'widestream' in link:
					headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36','Referer':url, 'Host':'cdn.widestream.io:8081', 'Origin':'http://widestream.io'}
					link = link+'|'+urllib.urlencode(headers)
				if 'livesport.pw' in link:
					cookie = GetURL(url, output='cookie')
					link = link+'|Referer='+url+'&Cookie='+cookie.split(';')[0]+'&User-Agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
				if 'eplstreams' in link or 'nbastreams.pw' in link:
					link = link +'|Cookie=access=true'
				return link
	else:
		domain = urlparse.urlparse(url).netloc
		scheme = urlparse.urlparse(url).scheme
		urls = common.parseDOM(html, 'iframe', ret='src')
		urls2 = common.parseDOM(html, 'frame', ret='SRC')
		urls = urls+urls2
		if urls:
			for url in urls:
				if '../../' in url:
					url = url.replace('../../', '/')
				if '../' in url:
					url = url.replace('../', '/')
				if url.startswith('//'):
					url = 'http:'+url
				if 'http://' not in url and 'https://' not in url:
					if not url.startswith('/'):
						url = '/'+url
					if scheme:
						url = scheme+'://'+domain+url
					else:
						url = 'http://'+domain+url
				ss = Universal(url)
				if ss:
					return ss

	
def sawresolve(query, referer):
	try:
		import js2py
		import cfscrape
		scraper = cfscrape.create_scraper()
		decoded = scraper.get(query).content
		context = js2py.EvalJs()
		context.execute('''pyimport jstools;
           		var escape = jstools.escape;
            	var unescape = jstools.unescape;
            	var document = [];
            	document.result = "";
            	document.domain = "";
            	document.write = function(markup){ document.result = document.result + markup };''')
		context.swidth = '400'
		context.sheight = '400'
		context.document.domain = urlparse.urlparse(query).netloc
		context.execute(decoded)
		if '</script>' in context.document.result:
			if 'src' in context.document.result:
				src = common.parseDOM(context.document.result, 'script', ret='src')
				result = ''
				for s in src:
					context.execute(GetURL(s))
					s = context.document.result
					result = result+s
			else:
				decoded = decoded+';'+context.document.result.replace('<script>','').replace('</script>','')
				context.execute(decoded)
				result = context.document.result
		else:
			result = context.document.result
		src = common.parseDOM(result, 'iframe', ret='src')[-1]
		src = src.replace("'","").replace('"','')
		if src:
			decoded = scraper.get(src).content
			swf = re.compile("SWFObject\('(.+?)'").findall(decoded)[0].replace(' ', '')
			scripts = decoded.split('javascript">')
			for script in scripts:
				script = script.split('</script>')[0]
				if 'SWFObject' in script:
					decoded = script
					break
			so = re.findall('(so.addVariable\(.*?\))', decoded)
			for s in so:
				o = s.replace("so.addVariable('", "var ").replace("',", " = ").replace(")","").replace("rtmp.tunneling","rtmptunneling")
				decoded = decoded.replace(s, o)
			so = re.findall('(so.addParam\(.*?\))', decoded)
			for s in so:
				o = s.replace("so.addParam('", "var ").replace("',", " = ").replace(")","")
				decoded = decoded.replace(s, o)
			context = js2py.EvalJs()
			context.execute('''pyimport jstools;
           		var escape = jstools.escape;
            	var unescape = jstools.unescape;
            	var SWFObject = function(){ };''')
			context.execute(decoded)
			try:
				streamer = context.streamer
			except: streamer = ''
			url = '%s playpath=%s swfUrl=%s pageUrl=%s live=1 timeout=60' % (streamer, context.file, swf, src)
			return url
	except:
		return None
		
def castup(id):
	try:
		url = 'http://www.castup.tv/embed.php?channel='+id
		result = GetURL(url, url)
		json_url = re.compile('\$.getJSON\("(.+?)", function\(json\){').findall(result)[0]
		data = GetJSON(json_url, url)
		file = data['streamname']
		rtmp = data['rtmp']
		url = 'http://'+rtmp+'/player.php?ch='+file
		data = GetURL(url, json_url)
		token = re.findall('token=(.+?)"',data)[0]
		url = "http://"+rtmp+"/live/"+file+".m3u8?token="+token
		return url
	except:
		return None


def castamp(id):
	try:
		url = 'http://castamp.com/embed.php?c=%s&tk=H0SKNbzC&vwidth=640&vheight=380'%id
		pageUrl=url
		result = GetURL(url, referer=url)
		result = urllib.unquote(result).replace('unescape(','').replace("'+'",'')
		result = re.sub('\/\*[^*]+\*\/','',result)
		var = re.compile('var\s(.+?)\s*=\s*[\'\"](.+?)[\'\"]').findall(result)
		var_dict = dict(var)
		file = re.compile('\'file\'\s*:\s*(.+?),').findall(result)[-1]
		fle = var_dict[file]
		if file+'.replace' in result:
			rslt = result.split(file+'.replace(')[-1].split(');')[0].replace("'","").strip()
			vars = rslt.split(',')
			fle = fle.replace(vars[0].strip(),vars[1].strip())
		rtmp = re.compile('(rtmp://[^\"\']+)').findall(result)[0]
		url = rtmp + ' playpath=' + fle + ' swfUrl=http://p.castamp.com/cplayer.swf' + ' flashver=WIN/2019,0,0,185 live=true timeout=15 swfVfy=1 pageUrl=' + pageUrl
		return url
	except:
		return None
	

def p2pcast(id):
	try:
		agent = 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:36.0) Gecko/20100101 Firefox/36.0'
		url = 'http://p2pcast.tech/stream.php?id='+id+'&live=0&p2p=0&stretching=uniform'
		request = urllib2.Request(url)
		request.add_header('User-Agent', agent)
		request.add_header('Referer', url)
		response = urllib2.urlopen(request, timeout=5)
		html = response.read()
		token = html.split('murl = "')[1].split('";')[0]
		link = base64.b64decode(token)
		request = urllib2.Request('http://p2pcast.tech/getTok.php')
		request.add_header('User-Agent', agent)
		request.add_header('Referer', url)
		request.add_header('X-Requested-With', 'XMLHttpRequest')
		response = urllib2.urlopen(request, timeout=5)
		html = response.read()
		js = json.loads(html)
		tkn = js['token']
		link = link+tkn
		link = link + '|User-Agent='+agent+'&Referer='+url
		return link
	except:
		return None
		
def broadcast(id, ur):
	try:
		import base64           
		url = 'http://bro.adca.st/stream.php?id=' + id + '&width=640&height=480'
		ur = ur.replace('wizhdsports.be','wizhdsports.to')
		source = GetURL(url, referer=ur)
		curl = re.findall('trap = "(.*?)"', source)[0]
		m3u8 = base64.b64decode(curl)
		url2 = 'http://bro.adca.st/fckymom.php'    
		headers2 = {'User-Agent': UA, 'Referer': url, 'X-Requested-With': 'XMLHttpRequest'}
		source2 = getUrl(url2, header = headers2)
		token = re.findall('"rumba":"(.*?)"', source2)[0]
		headers2 = {'User-Agent': UA, 'Referer': url, 'X-Requested-With': 'ShockwaveFlash/23.0.0.207'}
		return m3u8 + token + '|'+urllib.urlencode(headers2)
	except:
		return None

def p2pcast2(url):
	try:
		agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'
		request = urllib2.Request(url)
		request.add_header('User-Agent', agent)
		request.add_header('Referer', url)
		response = urllib2.urlopen(request, timeout=5)
		html = response.read()
		token = html.split('murl = "')[1].split('";')[0]
		link = base64.b64decode(token)
		link = link + '|User-Agent='+agent+'&Referer='+url
		return link
	except:
		return None


def weplayer(id):
	try:
		url = 'http://weplayer.pw/stream.php?id='+id
		request = urllib2.Request(url)
		request.add_header('Host', urlparse.urlparse(url).netloc)
		request.add_header('Referer', 'http://wizhdsports.com')
		request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:36.0) Gecko/20100101 Firefox/36.0')
		response = urllib2.urlopen(request, timeout=5)
		result = response.read()
		id = result.split("'text/javascript'>id='")[-1]
		id = id.split("';")[0]
		url2 = 'http://deltatv.xyz/stream.php?id='+id
		request = urllib2.Request(url2)
		request.add_header('Referer', url)
		request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:36.0) Gecko/20100101 Firefox/36.0')
		response = urllib2.urlopen(request, timeout=5)
		result = response.read()
		streamer = result.split("streamer=")[-1].split("&amp;")[0]
		file = result.split("file=")[-1].split("&amp;")[0]
		url = streamer+' playpath='+file+' swfUrl=http://cdn.deltatv.xyz/players.swf token=Fo5_n0w?U.rA6l3-70w47ch pageUrl='+url2+' live=1'
		return url
	except:
		return None

def streamking(url):
	try:
		html = GetURL(url, referer=url)
		link = re.findall('(http://.+?\.m3u8)',html)[0]
		link += '|User-Agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36&Referer='+url
		return link
	except:
		return None	


def hdcast(link, url):
	try:
		header = {'Referer':  url, 'User-Agent': UA, 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
					'Accept-Language':'en-US,en;q=0.8,bg;q=0.6,it;q=0.4,ru;q=0.2,uk;q=0.2',
					'Connection':'keep-alive', 'Host':urlparse.urlparse(link).netloc,'Upgrade-Insecure-Requests':'1'}
		result = getUrl(link,header=header)
		src = common.parseDOM(result, 'iframe', ret='src')
		if not src:
			src = 'http://94.102.50.97:8081/player.php?ch='+id
		else:
			src = src[-1]
			src = src.split('&')[0]
		header = {'Referer':  link, 'User-Agent': UA, 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
					'Accept-Language':'en-US,en;q=0.8,bg;q=0.6,it;q=0.4,ru;q=0.2,uk;q=0.2',
					'Connection':'keep-alive', 'Host':urlparse.urlparse(src).netloc,'Upgrade-Insecure-Requests':'1'}
		result = getUrl(src,header=header)
		url = re.findall('file:"(.*?)"', result)[0]
		return url
	except:
		return None


def cast4u(id):
	try:
		url = 'http://www.cast4u.tv/embedp4u.php?v='+id+'&vw=620&vh=490'
		result = GetURL(url, referer=url)
		url = re.findall('file: "(.+?)"',result)[0]
		return url
	except:
		return None
    

def lshstream(url):
	try:
		url = 'http://'+url.split('http://')[-1]
		id = urlparse.parse_qs(urlparse.urlparse(url).query)['u'][0]
		result = GetURL(url, referer=url)
		streamer = result.replace('//file', '')
		streamer = re.compile("file *: *'(.+?)'").findall(streamer)[-1]
		url=streamer + ' swfUrl=http://www.lshstream.com/jw/jwplayer.flash.swf flashver=WIN/2019,0,0,185 live=1 token=SECURET0KEN#yw%.?()@W! timeout=14 swfVfy=1 pageUrl=http://cdn.lshstream.com/embed.php?u=' + id
		return url
	except:
		return None


def iguide(url):
	try:
		result = GetURL(url, referer=url)
		token_url =re.compile('\$.getJSON\("(.+?)", function\(json\){').findall(result)[0]
		token = json.loads(GetURL(token_url, referer=url))['token']
		file = re.compile('(?:\'|\")?file(?:\'|\")?\s*:\s*(?:\'|\")(.+?)(?:\'|\")').findall(result)[0].replace('.flv','')
		rtmp = re.compile('(?:\'|\")?streamer(?:\'|\")?\s*:\s*(?:\'|\")(.+?)(?:\'|\")').findall(result)[0].replace(r'\\','\\').replace(r'\/','/')
		app = re.compile('.*.*rtmp://[\.\w:]*/([^\s]+)').findall(rtmp)[0]
		url=rtmp +  ' playpath=' + file + ' swfUrl=http://www.iguide.to/player/secure_player_iguide_token.swf flashver=WI/2020,0,0,286 live=1 timeout=15 token=' + token + ' swfVfy=1 pageUrl='+url
		return url
	except:
		return None

def rocktv(id):
	try:
		url = 'http://www.rocktv.co/embed.php?live='+id
		result = GetURL(url, referer=url)
		token = re.findall('securetoken\s*:\s*(?:\'|\")(.+?)(?:\'|\")',result)[0]
		rtmp = re.findall('file\s*:\s*(?:\'|\")(.+?)(?:\'|\")',result)[0]
		url = rtmp + ' swfUrl=http://p.jwpcdn.com/6/12/jwplayer.flash.swf live=1 flashver=WI/2020,0,0,286 token='  + token + ' timeout=14 swfVfy=1 pageUrl=' + url
		return url
	except:
		return None
		
def sostart(url):
	try:
		try:
			referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
		except:
			referer=url
		result = GetURL(url, referer=referer)
		rtmp = re.findall('.*?[\'"]?file[\'"]?[:,]\s*[\'"]([^\'"]+)[\'"].*',result)[0]
		url = rtmp+' swfUrl=http://sostart.org/jw/jwplayer.flash.swf flashver=WI/2020,0,0,286 token=SECURET0KEN#yw%.?()@W! live=1 timeout=14 swfVfy=1 pageUrl='+url
		return url
	except:
		return None



###################TVA############################
'''
This check has been put in place to stop the inclusion of TVA (and friends) addons in builds
from build makers that publicly insult or slander TVA's developers and friends. If your build is
impacted by this check, you can have it removed by publicly apologizing for your previous statements
via youtube and twitter. Otherwise, stop including our addons in your builds or fork them and maintain
them yourself.
                                                                                           http://i.imgur.com/TqIEnYB.gif
                                                                                           TVA developers (and friends)
'''
def do_block_check(uninstall=True):
    import hashlib
    import xbmcvfs
    f = xbmcvfs.File('special://home/media/splash.png')
    splash_md5 = hashlib.md5(f.read()).hexdigest()
    bad_md5s = ['926dc482183da52644e08658f4bf80e8', '084e2bc2ce2bf099ce273aabe331b02e']
    bad_addons = ['plugin.program.targetin1080pwizard', 'plugin.video.targetin1080pwizard']
    has_bad_addon = any(xbmc.getCondVisibility('System.HasAddon(%s)' % (addon)) for addon in bad_addons)
    if has_bad_addon or splash_md5 in bad_md5s:
        import xbmcgui
        import sys
        line2 = 'Press OK to uninstall this addon' if uninstall else 'Press OK to exit this addon'
        xbmcgui.Dialog().ok('Incompatible System', 'This addon will not work with the build you have installed', line2)
        if uninstall:
            import xbmcaddon
            import shutil
            addon_path = xbmcaddon.Addon().getAddonInfo('path').decode('utf-8')
            shutil.rmtree(addon_path)
        sys.exit()
		
######################################

def Play(url, orig_title):
    url = ParseLink(url, orig_title)
    if not url:
    	dialog = xbmcgui.Dialog()
    	dialog.notification('Pro Sport', 'Stream not found', xbmcgui.NOTIFICATION_INFO, 3000)
    else:
    	print url
    	item = xbmcgui.ListItem(path=url)
    	item.setInfo('video', { 'Title': orig_title })
    	xbmcplugin.setResolvedUrl(h, True, item)

    	
def addDir(title, url, iconImg="DefaultVideo.png", home="", away="", mode=""):
    sys_url = sys.argv[0] + '?url=' + urllib.quote_plus(url) + '&home=' + urllib.quote_plus(str(home)) +'&away=' + urllib.quote_plus(str(away)) +'&mode=' + urllib.quote_plus(str(mode))
    item = xbmcgui.ListItem(title, iconImage=iconImg, thumbnailImage=iconImg)
    item.setInfo(type='Video', infoLabels={'Title': title})
    xbmcplugin.addDirectoryItem(handle=h, url=sys_url, listitem=item, isFolder=True)

def addDir2(title, url, next_url, iconImg="DefaultVideo.png", popup=None, mode=""):
    sys_url = sys.argv[0] + '?url=' + urllib.quote_plus(url)+'&next_url=' + urllib.quote_plus(next_url) +'&mode=' + urllib.quote_plus(str(mode))
    item = xbmcgui.ListItem(title, iconImage=iconImg, thumbnailImage=iconImg)
    item.setInfo(type='Video', infoLabels={'Title': title})
    if popup:
    	item.addContextMenuItems(popup, True)
    xbmcplugin.addDirectoryItem(handle=h, url=sys_url, listitem=item, isFolder=True)

def addLink(title, orig_title, url, iconImg="DefaultVideo.png", mode=""):
    sys_url = sys.argv[0] + '?url=' + urllib.quote_plus(url) + '&mode=' + urllib.quote_plus(str(mode))+ '&orig=' + urllib.quote_plus(str(orig_title))
    item = xbmcgui.ListItem(title, iconImage=iconImg, thumbnailImage=iconImg)
    item.setLabel(title)
    item.setInfo(type='Video', infoLabels={'Title': title})
    item.setProperty('IsPlayable', 'true')
    xbmcplugin.addDirectoryItem(handle=h, url=sys_url, listitem=item)
    
def addDirectLink(title, infoLabels, url, iconImg="DefaultVideo.png"):
    item = xbmcgui.ListItem(title, iconImage=iconImg, thumbnailImage=iconImg)
    item.setInfo(type='Video', infoLabels=infoLabels)
    xbmcplugin.addDirectoryItem(handle=h, url=url, listitem=item)
       
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

h = int(sys.argv[1])
params = get_params()

mode = None
url = None

try: mode = urllib.unquote_plus(params['mode'])
except: pass

try: url = urllib.unquote_plus(params['url'])
except: pass

try: home = urllib.unquote_plus(params['home'])
except: pass

try: away = urllib.unquote_plus(params['away'])
except: pass

try: orig_title = urllib.unquote_plus(params['orig'])
except: pass

try: page = params['page'] if 'page' in params else 1
except: pass

if mode == None: Main()
elif mode == 'nfl': Games(mode)
elif mode == 'nba': Games(mode)
elif mode == 'nhl': Games(mode)
elif mode == 'mlb': Games(mode)
elif mode == 'soccer': Games(mode)
elif mode == 'myreddit': MyReddits()
elif mode == 'nbaarch': Archive(page, mode)
elif mode == 'nflarch': Archive(page, mode)
elif mode == 'nhlarch': Nhlarchive(url, page, mode)
elif mode == 'archive': Arch()
elif mode == 'playarchive': PlayArchive(url)
elif mode == 'playnhlarchive': Playnhlarchive(url)
elif mode == 'prostreams': getProStreams(url, home, away)
elif mode == 'mystreams': getMyStreams(url, home)
elif mode == 'play': Play(url, orig_title)
elif mode == 'topics': Topics(url)
elif mode == 'addnew': Addnew()
elif mode == 'remove': Remove(url)
elif mode == 'edit': Edit(url)

xbmcplugin.endOfDirectory(h)