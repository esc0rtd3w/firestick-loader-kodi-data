import datetime
import xbmc
from addon import update_library
from resources.lib.xswift2 import plugin
from resources.lib.video_player import PLAYER


def go_idle(duration):
	while not xbmc.Monitor().abortRequested() and duration > 0:
		if PLAYER.isPlayingVideo():
			PLAYER.currentTime = PLAYER.getTime()
		xbmc.sleep(1000)
		duration -= 1

def future(seconds):
	return datetime.datetime.now() + datetime.timedelta(seconds=seconds)

if __name__ == '__main__':
	go_idle(5)
	if plugin.get_setting('total_setup_done', bool) == False:
		xbmc.executebuiltin('RunPlugin(plugin://plugin.video.openmeta/setup/total)')
		plugin.set_setting('total_setup_done', 'true')
	next_update = future(0)
	while not xbmc.Monitor().abortRequested():
		if next_update <= future(0):
			next_update = future(8*60*60)
			update_library()
		go_idle(30*60)