from resources.lib.modules import client,control,addonInstaller
from resources.lib.modules.log_utils import log
import re,urllib,urlparse,xbmcvfs,os,urllib2

torrent_path = os.path.join(control.dataPath, 'myTorrent.torrent')


def resolve(url):
	actions = [("plugin://plugin.video.yatp/?action=play&torrent=%s","plugin.video.yatp","YATP-Yet Another Torrent Player"),("plugin://plugin.video.quasar/play?uri=%s","plugin.video.quasar","Quasar")]
	if not xbmcvfs.exists(os.path.dirname(torrent_path)):
		try: xbmcvfs.mkdirs(os.path.dirname(torrent_path))
		except: os.mkdir(os.path.dirname(torrent_path))


	file = urllib2.urlopen(url)
	output = open(torrent_path,'wb')
	output.write(file.read())
	output.close()

	choice = int(control.setting('torrentPlayer'))
	action = actions[choice]
	if choice == 0:
		url = torrent_path

	if addonInstaller.isInstalled(action[1]):
		return action[0]%url
	else:
		control.infoDialog('Torrent player not installed. Install it or select a different torrent player.',heading=action[2],time=6000)
	return ''
