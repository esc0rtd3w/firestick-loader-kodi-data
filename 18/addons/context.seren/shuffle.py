import sys
import xbmc

if __name__ == '__main__':
    item = sys.listitem
    message = item.getLabel()
    path = item.getPath()

    if 'action=showSeasons' in path:
        path = path.replace('action=showSeasons', 'action=shufflePlay')

    if 'action=smartPlay' in path:
        path = path.replace('action=smartPlay', 'action=shufflePlay')

    if 'action=getSources' in path:
        path = path.replace('action=getSources', 'action=shufflePlay')

    if 'action=playbackResume' in path:
        path = path.replace('action=playbackResume', 'action=shufflePlay')

    xbmc.executebuiltin('RunPlugin(%s)' % path)
