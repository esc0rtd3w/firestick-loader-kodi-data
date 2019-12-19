import sys, xbmc, json

try:
    from urlparse import parse_qsl
    from urllib import quote
except:
    from urllib.parse import parse_qsl, quote

if __name__ == '__main__':
    item = sys.listitem
    message = item.getLabel()
    path = item.getPath()

    plugin = 'plugin://plugin.video.seren/'
    args = path.split(plugin, 1)

    params = dict(parse_qsl(args[1].replace('?', '')))

    path = 'RunPlugin(%s?action=traktManager&actionArgs=%s)' % (plugin, quote(params.get('actionArgs')))
    xbmc.executebuiltin(path)
