import sys
import xbmc

if __name__ == '__main__':
    item = sys.listitem
    message = item.getLabel()
    path = item.getPath()

    if 'action=showSeasons' in path:
        path = path.replace('action=showSeasons', 'action=playbackResume')

    elif 'action=smartPlay' in path:
        path = path.replace('action=smartPlay', 'action=playbackResume')

    elif 'action=flatEpisodes' in path:
        path = path.replace('action=flatEpisodes', 'action=playbackResume')

    elif 'action=playbackResume' in path:
        pass

    xbmc.executebuiltin('RunPlugin(%s)' % path)
