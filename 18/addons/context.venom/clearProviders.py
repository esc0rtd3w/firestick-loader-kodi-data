import xbmc


if __name__ == '__main__':
	plugin = 'plugin://plugin.video.venom/'
	path = 'RunPlugin(%s?action=clearSources&opensettings=false)' % plugin
	xbmc.executebuiltin(path)