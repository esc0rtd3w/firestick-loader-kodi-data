import sys, xbmc, json

try:
    from urlparse import parse_qsl
    from urllib import quote
except:
    from urllib.parse import parse_qsl, quote

if __name__ == '__main__':

    item = sys.listitem

    path = item.getPath()
    plugin = 'plugin://plugin.video.seren/'
    args = path.split(plugin, 1)

    params = dict(parse_qsl(args[1].replace('?', '')))
    action = params.get('action')
    actionArgs = params.get('actionArgs')

    actionArgs = json.loads(actionArgs)

    actionArgs['item_type'] = 'season'
    actionArgs.pop('episode', '')

    path = '%s?action=seasonEpisodes&actionArgs=%s' % (plugin, quote(json.dumps(actionArgs)))

    xbmc.executebuiltin('ActivateWindow(Videos,%s)' % path)
