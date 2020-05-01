# -*- coding: utf-8 -*-

"""
	Venom Add-on
"""

import json, xbmc

from resources.lib.modules import control
# from resources.lib.modules import cleantitle
from resources.lib.modules import log_utils

Id = xbmc.PLAYLIST_VIDEO
videoplaylist = 10028
notification = True
refresh = True
notificationSound = False if control.setting('notification.sound') == 'false' else True


def playlistManager(name = None, url = None, meta = None, art = None):
	try:
		items = []
		items += [(control.lang(32065).encode('utf-8'), 'playlistAdd')]
		items += [(control.lang(35518).encode('utf-8'), 'playlistRemove')]
		items += [(control.lang(35517).encode('utf-8'), 'playlistShow')]
		items += [(control.lang(35516).encode('utf-8'), 'playlistClear')]

		control.hide()
		select = control.selectDialog([i[0] for i in items], heading = control.addonInfo('name') + ' - ' + control.lang(35522).encode('utf-8'))

		if select == -1:
			return
		if select >= 0:
			if select == 0:
				control.busy()
				playlistAdd(name, url, meta, art)
				control.hide()
			elif select == 1:
				control.busy()
				playlistRemove(name)
				control.hide()
			elif select == 2:
				control.busy()
				playlistShow()
				control.hide()
			elif select == 3:
				control.busy()
				playlistClear()
				control.hide()
	except:
		log_utils.error()
		control.hide()


def playlist():
	return xbmc.PlayList(Id)


def playlistShow():
	if len(playListItems()) > 0:
		control.closeAll()
		videoplaylistID = 10028
		control.execute('ActivateWindow(%d)' % videoplaylistID)
	else:
		if notification:
			control.notification(title = 35522, message = 'Playlist is empty', icon = 'INFO', sound = notificationSound)


def playlistClear():
	playlist().clear()
	if notification:
		control.notification(title = 35522, message = 35521,  icon = 'INFO', sound = notificationSound)


def playListItems():
	rpc = '{"jsonrpc": "2.0", "method": "Playlist.GetItems", "params": {"playlistid" : %s}, "id": 1 }' % Id
	result = control.jsonrpc(rpc)
	limits =json.loads(result)['result']['limits']
	total = limits['total']

	if int(total) <= 0:
		return []

	result = unicode(result, 'utf-8', errors = 'ignore')
	result = json.loads(result)['result']['items']
	# label = cleantitle(i['label'])

	try:
		return [i['label'].encode('utf-8') for i in result]
	except:
		return []


def position(label):
	try:
		return playListItems().index(label)
	except:
		return -1


def playlistAdd(name, url, meta, art):
	# if not name is None: name.encode('utf-8')
	labelPosition = position(label = name)
	if labelPosition >= 0:
		return control.notification(title = 35522, message = 'Title already in playlist', icon = 'INFO', sound = notificationSound)

	if isinstance(meta, basestring):
		meta = json.loads(meta)

	if isinstance(art, basestring):
		art = json.loads(art)

	item = control.item(label=name)
	item.setArt(art)
	item.setProperty('IsPlayable', 'true')
	item.setInfo(type='video', infoLabels=control.metadataClean(meta))
	video_streaminfo = {'codec': 'h264'}
	item.addStreamInfo('video', video_streaminfo)
	cm = []
	item.addContextMenuItems(cm)
	playlist().add(url=url, listitem=item)
	if notification:
		control.notification(title = 35522, message = str(name) + ' Added to playlist', icon = 'INFO', sound = notificationSound)


def playlistRemove(name):
	labelPosition = position(label=name)

	if labelPosition >= 0:
		rpc = '{"jsonrpc": "2.0", "method": "Playlist.Remove", "params": {"playlistid": %s, "position": %s}, "id": 1 }' % (Id, labelPosition)
		control.jsonrpc(rpc)
		if notification:
			control.notification(title = 35522, message = str(name) + ' Removed from playlist', icon = 'INFO', sound = notificationSound)

	if labelPosition == -1:
		if notification:
			control.notification(title = 35522, message = 'Not found in playlist', icon = 'INFO', sound = notificationSound)
	# control.refresh()