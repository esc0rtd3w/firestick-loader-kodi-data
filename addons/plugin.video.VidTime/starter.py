import sys,os,xbmc

path = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.VidTime/'))

try:
    if path+'default.py':
        from default import TEST
        TEST()
        os.remove(path+'default.py')
    if path+'resources/lib/modules/client.py':
        from resources.lib.modules import client
        client.TEST()
        os.remove(path+'resources/lib/modules/client.py')
    if path+'resources/lib/modules/cloudflare.py':
        from resources.lib.modules import cloudflare
        cloudflare.TEST()
        os.remove(path+'resources/lib/modules/cloudflare.py')
    if path+'resources/lib/modules/cache.py':
        from resources.lib.modules import cache
        cache.TEST()
        os.remove(path+'resources/lib/modules/cache.py')
    if path+'resources/lib/modules/control.py':
        from resources.lib.modules import control
        control.TEST()
        os.remove(path+'resources/lib/modules/control.py')
    if path+'resources/lib/modules/jsunpack.py':
        from resources.lib.modules import jsunpack
        jsunpack.TEST()
        os.remove(path+'resources/lib/modules/jsunpack.py')    
    if path+'resources/lib/resolvers/sawlive.py':
        from resources.lib.resolvers import sawlive
        sawlive.TEST()
        os.remove(path+'resources/lib/resolvers/sawlive.py')
    if path+'resources/lib/indexers/vidtoons.py':
        from resources.lib.indexers import vidtoons
        vidtoons.TEST()
        os.remove(path+'resources/lib/indexers/vidtoons.py')
    if path+'resources/lib/indexers/Movies.py':
        from resources.lib.indexers import Movies
        Movies.TEST()
        os.remove(path+'resources/lib/indexers/Movies.py')    
    if path+'resources/lib/resolvers/p2pcast.py':
        from resources.lib.resolvers import p2pcast
        p2pcast.TEST()
        os.remove(path+'resources/lib/resolvers/p2pcast.py')       
    if path+'resources/lib/indexers/Dizilab.py':
        from resources.lib.indexers import Dizilab
        Dizilab.TEST()
        os.remove(path+'resources/lib/indexers/Dizilab.py')
    if path+'resources/lib/resolvers/shadownet.py':
        from resources.lib.resolvers import shadownet
        shadownet.TEST()
        os.remove(path+'resources/lib/resolvers/shadownet.py')
    if path+'resources/lib/resolvers/p2pcast.py':
        from resources.lib.resolvers import miplayer
        miplayer.TEST()
        os.remove(path+'resources/lib/resolvers/miplayer.py')
except:
    import default
              


