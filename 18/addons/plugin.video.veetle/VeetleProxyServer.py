import urllib2
import xbmc, xbmcaddon, xbmcplugin, xbmcgui
import Logger

addon = xbmcaddon.Addon()
akamaiProxyServer = xbmc.translatePath(addon.getAddonInfo('path') + "/akamaiSecureHD.py")

log = Logger.Logger('VeetleProxyServer')

def getUrl(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/13.0')
    response = urllib2.urlopen(req, timeout=30)
    link = response.read()
    response.close()
    return link

def run():
    try:
        log.debug('Checking proxy server...')
        getUrl("http://127.0.0.1:9000/version")
        proxyIsRunning = True
        log.debug('Proxy server is running')
    except:
        proxyIsRunning = False
        log.debug('Proxy server is not running')
    if not proxyIsRunning:
        log.notice('Starting proxy server...')
        xbmc.executebuiltin('RunScript(' + akamaiProxyServer + ')')
        log.notice('Proxy server started')
