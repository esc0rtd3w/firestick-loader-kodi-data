import sys, xbmc, json

try:
    from urlparse import parse_qsl
except:
    from urllib.parse import parse_qsl

if __name__ == '__main__':

    item = sys.listitem

    path = item.getPath()
    plugin = 'plugin://plugin.video.seren/'
    path = path.split(plugin, 1)

    params = dict(parse_qsl(path[1].replace('?', '')))
    action = params.get('action')
    actionArgs = json.loads(params.get('actionArgs'))

    if actionArgs['item_type'] == 'show':
        xbmc.executebuiltin('ActivateWindow(Videos,plugin://plugin.video.seren/?action=showsRelated&actionArgs=%s)'
                        % actionArgs['trakt_id'])
    else:
        xbmc.executebuiltin('ActivateWindow(Videos,plugin://plugin.video.seren/?action=moviesRelated&actionArgs=%s)'
                        % actionArgs['trakt_id'])
