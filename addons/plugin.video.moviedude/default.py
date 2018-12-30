# -*- coding: utf-8 -*-

'''
    Dr Stream Fork Add-on

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


import urlparse,sys,re

params = dict(urlparse.parse_qsl(sys.argv[2].replace('?','')))

action = params.get('action')

content = params.get('content')

name = params.get('name')

url = params.get('url')

image = params.get('image')

fanart = params.get('fanart')


if action == None:
    from resources.lib.indexers import phstreams
    phstreams.indexer().root()

elif action == 'directory':
    from resources.lib.indexers import phstreams
    phstreams.indexer().get(url)

elif action == 'qdirectory':
    from resources.lib.indexers import phstreams
    phstreams.indexer().getq(url)

elif action == 'xdirectory':
    from resources.lib.indexers import phstreams
    phstreams.indexer().getx(url)

elif action == 'developer':
    from resources.lib.indexers import phstreams
    phstreams.indexer().developer()

elif action == 'tvtuner':
    from resources.lib.indexers import phstreams
    phstreams.indexer().tvtuner(url)

elif 'youtube' in str(action):
    from resources.lib.indexers import phstreams
    phstreams.indexer().youtube(url, action)

elif action == 'play':
    from resources.lib.indexers import phstreams
    phstreams.player().play(url, content)

elif action == 'browser':
    from resources.lib.indexers import phstreams
    phstreams.resolver().browser(url)

elif action == 'search':
    from resources.lib.indexers import phstreams
    phstreams.indexer().search(url=None)

elif action == 'addSearch':
    from resources.lib.indexers import phstreams
    phstreams.indexer().addSearch(url)

elif action == 'delSearch':
    from resources.lib.indexers import phstreams
    phstreams.indexer().delSearch()

elif action == 'queueItem':
    from resources.lib.modules import control
    control.queueItem()

elif action == 'openSettings':
    from resources.lib.modules import control
    control.openSettings()

elif action == 'urlresolverSettings':
    from resources.lib.modules import control
    control.openSettings(id='script.module.urlresolver')

elif action == 'addView':
    from resources.lib.modules import views
    views.addView(content)

elif action == 'downloader':
    from resources.lib.modules import downloader
    downloader.downloader()

elif action == 'addDownload':
    from resources.lib.modules import downloader
    downloader.addDownload(name,url,image)

elif action == 'removeDownload':
    from resources.lib.modules import downloader
    downloader.removeDownload(url)

elif action == 'startDownload':
    from resources.lib.modules import downloader
    downloader.startDownload()

elif action == 'startDownloadThread':
    from resources.lib.modules import downloader
    downloader.startDownloadThread()

elif action == 'stopDownload':
    from resources.lib.modules import downloader
    downloader.stopDownload()

elif action == 'statusDownload':
    from resources.lib.modules import downloader
    downloader.statusDownload()

elif action == 'trailer':
    from resources.lib.modules import trailer
    trailer.trailer().play(name)

elif action == 'clearCache':
    from resources.lib.modules import cache
    cache.clear()

elif action == 'radios':
    from resources.lib.indexers import phradios
    phradios.radios()

elif action == 'radioResolve':
    from resources.lib.indexers import phradios
    phradios.radioResolve(url)

elif action == 'radio1fm':
    from resources.lib.indexers import phradios
    phradios.radio1fm()

elif action == 'radio181fm':
    from resources.lib.indexers import phradios
    phradios.radio181fm()

elif action == 'radiocast':
    from resources.lib.indexers import phradios
    phradios.kickinradio()

elif action == 'kickinradiocats':
    from resources.lib.indexers import phradios
    phradios.kickinradiocats(url)

elif action == 'phtoons.root' or action == 'cartoon':
    from resources.lib.indexers import phtoons
    phtoons.indexer().root()

elif action == 'phtoons.cartoons':
    from resources.lib.indexers import phtoons
    phtoons.indexer().cartoons(url)

elif action == 'phtoons.cartoongenres':
    from resources.lib.indexers import phtoons
    phtoons.indexer().cartoongenres()

elif action == 'phtoons.cartoonstreams':
    from resources.lib.indexers import phtoons
    phtoons.indexer().cartoonstreams(url, image, fanart)

elif action == 'phtoons.cartoonplay':
    from resources.lib.indexers import phtoons
    phtoons.indexer().cartoonplay(url)

elif action == 'phtoons.anime':
    from resources.lib.indexers import phtoons
    phtoons.indexer().anime(url)

elif action == 'phtoons.animegenres':
    from resources.lib.indexers import phtoons
    phtoons.indexer().animegenres()

elif action == 'phtoons.animestreams':
    from resources.lib.indexers import phtoons
    phtoons.indexer().animestreams(url, image, fanart)

elif action == 'phtoons.animeplay':
    from resources.lib.indexers import phtoons
    phtoons.indexer().animeplay(url)

else:
    if 'search' in action:
        url = action.split('search=')[1]
        url = url + '|SECTION|'
        from resources.lib.indexers import phstreams
        phstreams.indexer().search(url)
    else: quit()
