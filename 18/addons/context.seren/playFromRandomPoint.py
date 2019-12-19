import sys
import xbmc

if __name__ == '__main__':
    item = sys.listitem
    message = item.getLabel()
    path = item.getPath()

    if 'action=showSeasons' in path:
        path = path.replace('action=showSeasons', 'action=playFromRandomPoint')

    elif 'action=smartPlay' in path:
        path = path.replace('action=smartPlay', 'action=playFromRandomPoint')

    elif 'action=flatEpisodes' in path:
        path = path.replace('action=flatEpisodes', 'action=playFromRandomPoint')

    elif 'action=playbackResume' in path:
        path = path.replace('action=flatEpisodes', 'action=playFromRandomPoint')

    xbmc.executebuiltin('RunPlugin(%s)' % path)
