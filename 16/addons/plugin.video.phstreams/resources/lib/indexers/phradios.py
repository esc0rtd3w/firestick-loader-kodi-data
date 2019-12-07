# -*- coding: utf-8 -*-

'''
    Phoenix Add-on

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


import re,sys,urllib,urlparse,json,base64

from resources.lib.modules import control
from resources.lib.modules import client


radio1fmicon = 'http://phoenixtv.offshorepastebin.com/art/radio1fm/icon.png'
radio1fmfanart = 'http://phoenixtv.offshorepastebin.com/art/radio1fm/fanart.jpg'
radio181fmicon = 'http://phoenixtv.offshorepastebin.com/art/radio181fm/icon.png'
radio181fmfanart = 'http://phoenixtv.offshorepastebin.com/art/radio181fm/fanart.jpg'
radiocasticon = 'http://phoenixtv.offshorepastebin.com/art/radiocast/icon.png'
radiocastfanart = 'http://phoenixtv.offshorepastebin.com/art/radiocast/fanart.jpg'


def radios():
    addCategoryItem('1FM', 'radio1fm', radio1fmicon, radio1fmfanart)
    addCategoryItem('181FM', 'radio181fm', radio181fmicon, radio181fmfanart)
    addCategoryItem('Radiocast','radiocast', radiocasticon, radiocastfanart)
    endCategory()


def radio1fm():
    try:
        url = 'http://rad.io/info/index/searchembeddedbroadcast?q=1%20FM&streamcontentformats=aac%2Cmp3&start=0&rows=1000'

        result = client.request(url, headers={'User-Agent': base64.b64decode('WEJNQyBBZGRvbiBSYWRpbw==')})

        index = []
        items = json.loads(result)
    except:
        return

    for item in items:
        try:
            name = item['name']
            if not name.lower().startswith('1.fm'): raise Exception()
            name = name.split('-', 1)[-1].strip().capitalize()
            name = name.encode('utf-8')

            url = item['id']
            url = 'http://rad.io/info/broadcast/getbroadcastembedded?broadcast=%s' % url
            url = url.encode('utf-8')

            index.append({'name': name, 'url': url, 'thumb': '0', 'image': radio1fmicon, 'fanart': radio1fmfanart})
        except:
            pass

    index = [i for x, i in enumerate(index) if i not in index[x+1:]]
    index = sorted(index, key=lambda k: k['name'])
    for i in index: addDirectoryItem(i['name'], i['url'], i['thumb'], i['image'], i['fanart'])

    endDirectory()


def radio1fmResolve(url):
    try:
        domain = (urlparse.urlparse(url).netloc).lower()
        if not domain == 'rad.io': return url

        url = client.request(url, headers={'User-Agent': base64.b64decode('WEJNQyBBZGRvbiBSYWRpbw==')})
        url = json.loads(url)['streamURL']
        return url
    except:
        return


def radio181fm():
    try:
        url = 'http://www.181.fm/index.php?p=mp3links'

        result = client.request(url)

        index = []
        items = client.parseDOM(result, 'td', attrs={'id': 'rightlinks'})
    except:
        pass

    for item in items:
        try:
            if not item.startswith('http://'): raise Exception()

            name = items[:items.index(item)]
            name = [i for i in name if not 'http://' in i][-1]
            name = client.replaceHTMLCodes(name)
            name = name.encode('utf-8')

            url = item.split('<')[0].replace('///', '://')
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            index.append({'name': name, 'url': url, 'thumb': '0', 'image': radio181fmicon, 'fanart': radio181fmfanart})
        except:
            pass

    index = [i for x, i in enumerate(index) if i not in index[x+1:]]
    index = sorted(index, key=lambda k: k['name'])
    for i in index: addDirectoryItem(i['name'], i['url'], i['thumb'], i['image'], i['fanart'])

    endDirectory()


def kickinradio():
    try:
        url = 'https://www.internet-radio.com/stations/'
        result = client.request(url)
        items = client.parseDOM(result, 'dt', attrs={'style': 'font-size: 22px;'})    
    except:
        return

    for item in items:
        try:
            url = client.parseDOM(item, 'a', ret="href")[0]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            addCategoryItem('[UPPERCASE]'+url[10:-1]+'[/UPPERCASE]', 'kickinradiocats', radiocasticon, radiocastfanart, url=url)   
        except:
            pass

    endDirectory()


def kickinradiocats(url):
    try:
        url = urlparse.urljoin('https://www.internet-radio.com', url)

        result = client.request(url)
        result = client.parseDOM(result, 'div', attrs={'class': 'col-md-7'})

        a = client.parseDOM(result, 'h4', attrs={'class': 'text-danger'})
        b = client.parseDOM(result, 'samp')
        items = zip(a, b)
    except:
        return

    for item in items:
        try:
            try: a = client.parseDOM(item[0], 'a')[0]
            except: a = ''
            try: b = [i for i in client.parseDOM(item[0], 'a', ret='href')[0].split('/') if not i == ''][-1]
            except: b = ''
            if not a == '': name = a
            elif not b == '': name = b
            else: name = item[0]
            name = name.capitalize()
            name = client.replaceHTMLCodes(name)
            name = name.encode('utf-8')

            url = item[1].split()
            url = [i for i in url if i.startswith('http')][0]
            url = re.sub('[0-9a-zA-Z]+\.pls(?:.+|)|\.m3u(?:.+|)', '', url)
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            addDirectoryItem(name, url, '0', radiocasticon, radiocastfanart)
        except:
            pass

    try:
        next = client.parseDOM(result, 'ul', attrs={'class': 'pagination'})
        next = client.parseDOM(next, 'li', attrs={'class': 'next'})
        next = client.parseDOM(next, 'a', ret='href')[0]
        next = client.replaceHTMLCodes(next)
        next = next.encode('utf-8')

        addCategoryItem('[B][I]NEXT[/I][/B]', 'kickinradiocats', radiocasticon, radiocastfanart, url=next)
    except:
        pass

    endDirectory()


def addCategoryItem(name, action, image, fanart, url='0'):
    u = '%s?action=%s&url=%s&image=%s&fanart=%s' % (sys.argv[0], str(action), urllib.quote_plus(url), urllib.quote_plus(image), urllib.quote_plus(fanart))
    item = control.item(name, iconImage=image, thumbnailImage=image)
    try: item.setArt({'icon': image})
    except: pass
    item.addContextMenuItems([], replaceItems=False)
    item.setProperty('Fanart_Image', fanart)
    control.addItem(handle=int(sys.argv[1]),url=u,listitem=item,isFolder=True)


def endCategory():
    #control.do_block_check(False)
    if control.skin == 'skin.confluence': control.execute('Container.SetViewMode(500)')
    control.directory(int(sys.argv[1]), cacheToDisc=True)


def addDirectoryItem(name, url, thumb, image, fanart):
    if not thumb == '0': image = thumb

    u = '%s?action=radioResolve&name=%s&url=%s&image=%s&fanart=%s' % (sys.argv[0], urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(image), urllib.quote_plus(fanart))

    meta = {'title': name, 'album': name, 'artist': name, 'comment': name}

    item = control.item(name, iconImage=image, thumbnailImage=image)
    try: item.setArt({'icon': image})
    except: pass
    item.setInfo(type='Music', infoLabels = meta)
    item.addContextMenuItems([], replaceItems=False)
    item.setProperty('Fanart_Image', fanart)
    control.addItem(handle=int(sys.argv[1]),url=u,listitem=item,isFolder=False)


def endDirectory():
    #control.do_block_check(False)
    control.directory(int(sys.argv[1]), cacheToDisc=True)


def radioResolve(url):
    url = radio1fmResolve(url)
    url = client.request(url, output='geturl')
    title = control.infoLabel('ListItem.Label')
    image = control.infoLabel('ListItem.Icon')
    meta = {'title': title, 'album': title, 'artist': title, 'comment': title}
    item = control.item(path=url, iconImage=image, thumbnailImage=image)
    item.setArt({'icon': image})
    item.setInfo(type='Music', infoLabels = meta)
    control.player.play(url, item)


