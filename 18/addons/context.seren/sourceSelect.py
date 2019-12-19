import sys
import xbmc

if __name__ == '__main__':
    item = sys.listitem
    message = item.getLabel()
    path = item.getPath()

    if '?action=getSources' in path:
        path = path.replace('getSources', 'getSources&source_select=true')
    if '?action=smartPlay' in path:
        path = path.replace('smartPlay', 'getSources&source_select=true')

    xbmc.executebuiltin('PlayMedia(%s)' % path)
