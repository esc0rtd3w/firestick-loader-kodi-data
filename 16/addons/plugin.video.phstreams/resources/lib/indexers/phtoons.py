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


import urlparse,urllib,random,re,os,sys
try: import xbmc
except: pass

from resources.lib.modules import control
from resources.lib.modules import client
from resources.lib.modules import cache


class indexer:
    def __init__(self):
        self.list = []

        self.cartoons_link = 'http://9cartoon.me'
        self.newcartoons_link = '/CartoonList/NewAndHot'
        self.topcartoons_link = '/CartoonList/MostViewed'
        self.cartoongenres_link = '/genre/%s/'
        self.cartoonsearch_link = '/Search?s=%s'

        self.cartoons_image = 'http://phoenixtv.offshorepastebin.com/art/cartoon/art%s.png'
        self.cartoons_fanart = 'http://phoenixtv.offshorepastebin.com/art/cartoon/fanart.jpg'

        self.anime_link = 'http://www.animedreaming.tv'
        self.newanime_link = '/latest-anime-episodes/'
        self.animegenres_link = '/genres/%s/?filter=newest&req=anime'
        self.animeimage_link = '/anime-images-big/%s.jpg'
        self.animesearch_link = '/search.php?searchquery=%s'

        self.anime_image = 'http://phoenixtv.offshorepastebin.com/art/anime/art%s.png'
        self.anime_fanart = 'http://phoenixtv.offshorepastebin.com/art/anime/fanart.jpg'


    def root(self):
        try:
            self.list = [
            {
            'title': 'Cartoon Search',
            'action': 'phtoons.cartoons',
            'url': self.cartoonsearch_link,
            'image': self.cartoons_image % (random.randint(1,10)),
            'fanart': self.cartoons_fanart
            },

            {
            'title': 'Cartoon Genres',
            'action': 'phtoons.cartoongenres',
            'image': self.cartoons_image % (random.randint(1,10)),
            'fanart': self.cartoons_fanart
            },

            {
            'title': 'Cartoon Latest',
            'action': 'phtoons.cartoons',
            'url': self.newcartoons_link,
            'image': self.cartoons_image % (random.randint(1,10)),
            'fanart': self.cartoons_fanart
            },

            {
            'title': 'Cartoon Popular',
            'action': 'phtoons.cartoons',
            'url': self.topcartoons_link,
            'image': self.cartoons_image % (random.randint(1,10)),
            'fanart': self.cartoons_fanart
            },

            {
            'title': 'Anime Search',
            'action': 'phtoons.anime',
            'url': self.animesearch_link,
            'image': self.anime_image % (random.randint(1,10)),
            'fanart': self.anime_fanart
            },

            {
            'title': 'Anime Genres',
            'action': 'phtoons.animegenres',
            'image': self.anime_image % (random.randint(1,10)),
            'fanart': self.anime_fanart
            },

            {
            'title': 'Anime Latest',
            'action': 'phtoons.animestreams',
            'url': self.newanime_link,
            'image': self.anime_image % (random.randint(1,10)),
            'fanart': self.anime_fanart
            }
            ]

            self.addDirectory(self.list)
            return self.list
        except:
            pass


    def cartoons(self, url):
        try:
            if url == self.cartoonsearch_link:
                k = control.keyboard('', '') ; k.setHeading(control.infoLabel('ListItem.Label')) ; k.doModal()
                if k.getText() == '' or not k.isConfirmed(): return
                url = self.cartoonsearch_link % urllib.quote_plus(k.getText().split()[0])

            self.list = cache.get(self.cartoon_list, 0, url)

            for i in self.list: i.update({'nextaction': 'phtoons.cartoons', 'nexticon': self.cartoons_image % (random.randint(1,10)), 'nextfanart': self.cartoons_fanart})

            for i in self.list: i.update({'action': 'phtoons.cartoonstreams'})
            for i in self.list: i.update({'fanart': self.cartoons_fanart})

            self.addDirectory(self.list)
            return self.list
        except:
            pass


    def cartoongenres(self):
        try:
            genres = ['action', 'adventure', 'comedy', 'crime', 'Documentary', 'family', 'fantasy', 'drama', 'romance', 'game', 'historical', 'horror', 'movie', 'music', 'mystery', 'sci-fi', 'short', 'Sport', 'Thriller']

            for i in genres: self.list.append({'title': i.title(), 'url': self.cartoongenres_link % i, 'image': self.cartoons_image % (random.randint(1,10)), 'fanart': self.cartoons_fanart, 'action': 'phtoons.cartoons'})

            self.addDirectory(self.list)
            return self.list
        except:
            pass


    def cartoonstreams(self, url, image, fanart):
        try:
            self.list = cache.get(self.cartoon_list_2, 0, url, image, fanart)

            if len(self.list) == 1: return self.cartoonplay(self.list[0]['url'])

            for i in self.list: i.update({'action': 'phtoons.cartoonplay'})
            for i in self.list: i.update({'fanart': self.cartoons_fanart})

            self.addDirectory(self.list, content='files')
            return self.list
        except:
            pass


    def cartoonplay(self, url):
        try:
            url = self.cartoon_resolver(url)
            if not url == None: player().run(url)
        except:
            pass


    def anime(self, url):
        try:
            if url == self.animesearch_link:
                k = control.keyboard('', '') ; k.setHeading(control.infoLabel('ListItem.Label')) ; k.doModal()
                if k.getText() == '' or not k.isConfirmed(): return
                url = self.animesearch_link % urllib.quote_plus(k.getText())

            self.list = cache.get(self.anime_list, 0, url)

            for i in self.list: i.update({'action': 'phtoons.animestreams'})
            for i in self.list: i.update({'fanart': self.anime_fanart})

            self.addDirectory(self.list)
            return self.list
        except:
            pass


    def animegenres(self):
        try:
            genres = ['Action', 'Adventure', 'Airforce', 'Aliens', 'Angels', 'Angst', 'Anthropomorphism', 'Art',
            'Bakumatsu - Meiji Era', 'Band', 'Baseball', 'Basketball', 'Bishounen', 'Bounty Hunters', 'Boxing', 'Cars',
            'Catgirls', 'Clubs', 'College', 'Combat', 'Comedy', 'Coming of Age', 'Conspiracy', 'Contemporary Fantasy',
            'Cooking', 'CopsCrime', 'Crossdressing', 'Cyberpunk', 'Cyborgs', 'Dark Fantasy', 'Delinquents', 'Dementia',
            'Demons', 'Detective', 'Dragons', 'Drama', 'Driving', 'Dystopia', 'Ecchi', 'Elementary School', 'Elves',
            'Fantasy', 'Female Students', 'Female Teachers', 'Feudal Warfare', 'Football', 'Gambling', 'Game',
            'Gender switch', 'Genetic Modification', 'Goddesses', 'Gunfights', 'Gymnastics', 'Harem', 'High Fantasy',
            'High School', 'Historical', 'Horror', 'Human Enhancement', 'Humanoid', 'Idol', 'Josei', 'Juujin', 'Kids',
            'Law and Order', 'Lolicon', 'Love', 'Love Polygon', 'Mafia', 'Magic', 'Mahou Shoujo', 'Maids', 'Manga',
            'Martial Arts', 'Mecha', 'Middle School', 'Military', 'Music', 'Mystery', 'Navy', 'Ninja', 'Ninjas',
            'Parallel Universe', 'Parasites', 'Parody', 'Performance', 'Piloted Robots', 'Pirates', 'Police',
            'Post-apocalyptic', 'Power Suits', 'Proxy Battles', 'Psychological', 'Revenge', 'Reverse Harem',
            'Robot Helpers', 'Robots', 'Romance', 'Samurai', 'School', 'School Life', 'Sci-Fi', 'SciFi', 'Scifi',
            'Seinen', 'Shoujo', 'Shoujo Ai', 'Shounen', 'Shounen Ai', 'Slapstick', 'Slice of Life', 'Space',
            'Space Travel', 'Special Squads', 'Sports', 'Sudden Girlfriend Appearance', 'Super Deformed', 'Super Power',
            'Super Powers', 'Supernatural', 'Swordplay', 'Tennis', 'Thriller', 'Time Travel', 'Tournament', 'Tragedy',
            'Transforming Robots', 'Underworld', 'Vampire', 'Vampires', 'Violence', 'Virtual Reality', 'WWII', 'Waitresses',
            'Witches', 'Yakuza', 'Yuri']

            for i in genres: self.list.append({'title': i, 'url': self.animegenres_link % i.replace(' ','%20'), 'image': self.anime_image % (random.randint(1,10)), 'fanart': self.anime_fanart, 'action': 'phtoons.anime'})

            self.addDirectory(self.list)
            return self.list
        except:
            pass


    def animestreams(self, url, image, fanart):
        try:
            if url == self.newanime_link:
                self.list = cache.get(self.anime_list_3, 0, url)

            else:
                self.list = cache.get(self.anime_list_2, 0, url, image, fanart)


            if len(self.list) == 1: return self.animeplay(self.list[0]['url'])

            for i in self.list: i.update({'action': 'phtoons.animeplay'})
            for i in self.list: i.update({'fanart': self.anime_fanart})

            self.addDirectory(self.list, content='files')
            return self.list
        except:
            pass


    def animeplay(self, url):
        try:
            url = self.anime_resolver(url)
            if not url == None: player().run(url)
        except:
            pass


    def cartoon_list(self, url):
        try:
            url = urlparse.urljoin(self.cartoons_link, url)

            r = client.request(url, output='extended')
            result = r[0] ; headers = r[3]

            items = client.parseDOM(result, 'div', attrs = {'class': 'anime_movies_items'})

            try: items += client.parseDOM(result, 'ul', attrs = {'class': 'listin.+?'})[0].split('</li>')
            except: pass
        except:
        	return

        try:
            next = client.parseDOM(result, 'li', attrs = {'class': 'page'})
            next = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a')) for i in next]
            next = [(i[0][0], i[1][0]) for i in next if len(i[0]) > 0 and len(i[1]) > 0]
            next = [i[0] for i in next if 'raquo' in i[1]][0]
            next = urlparse.urljoin(self.cartoons_link, next)
            next = client.replaceHTMLCodes(next)
            next = next.encode('utf-8')
        except:
            next = ''

        for item in items:
            try:
                try: title = client.parseDOM(item, 'a')[0]
                except: pass
                try: title = client.parseDOM(item, 'a', ret='title')[0]
                except: pass
                title = client.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                url = client.parseDOM(item, 'a', ret='href')[0]
                url = urlparse.urljoin(self.cartoons_link, url)
                url = client.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = client.parseDOM(item, 'img', ret='src')[0]
                image = urlparse.urljoin(self.cartoons_link, image)
                image += '|' + urllib.urlencode(headers)
                image = client.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                self.list.append({'title': title, 'url': url, 'image': image, 'next': next})
            except:
                pass

        return self.list


    def cartoon_list_2(self, url, image, fanart):
        try:
            url = urlparse.urljoin(self.cartoons_link, url)

            result = client.request(url)

            items = client.parseDOM(result, 'ul', attrs = {'id': 'episode_related'})[0]
            items = client.parseDOM(items, 'li')
        except:
        	return

        for item in items:
            try:
                title = client.parseDOM(item, 'a')[0]
                title = title.strip()
                title = client.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                url = client.parseDOM(item, 'a', ret='href')[0]
                url = urlparse.urljoin(self.cartoons_link, url)
                url = client.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                self.list.append({'title': title, 'url': url, 'image': image})
            except:
                pass

        return self.list


    def cartoon_resolver(self, url):
        try:
            url = urlparse.urljoin(self.cartoons_link, url)

            u = client.request(url)
            u = client.parseDOM(u, 'div', attrs = {'id': 'player'})[0]
            u = client.parseDOM(u, 'iframe', ret='src')[0]
            u = client.request(u, referer=url)
            u = client.parseDOM(u, 'source', ret='src', attrs = {'type': 'video.+?'})[0]

            return u
        except:
            pass


    def anime_list(self, url):
        try:
            url = urlparse.urljoin(self.anime_link, url)

            result = client.request(url)

            items = client.parseDOM(result, 'div', attrs={'id': 'left_content'})[0]
            items = client.parseDOM(items, 'li')
        except:
        	return

        for item in items:
            try:
                title = client.parseDOM(item, 'a')[0]
                if '>Movie<' in title: raise Exception()
                title = re.sub('<.+?>|</.+?>|\\\\|\n', '', title).strip()
                title = client.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                url = client.parseDOM(item, 'a', ret='href')[0]
                url = urlparse.urljoin(self.anime_link, url)
                url = url.replace(' ','%20')
                url = client.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = [i for i in url.split('/') if not i == ''][-1]
                image = self.animeimage_link % image
                image = urlparse.urljoin(self.anime_link, image)
                image = image.encode('utf-8')

                self.list.append({'title': title, 'url': url, 'image': image})
            except:
                pass

        return self.list


    def anime_list_2(self, url, image, fanart):
        try:
            url = urlparse.urljoin(self.anime_link, url)

            result = client.request(url)

            items = client.parseDOM(result, 'ul', attrs={'class': 'cat_page_box'})[-1]
            items = client.parseDOM(items, 'li')
            items = items[::-1]
        except:
        	return

        for item in items:
            try:
                title = client.parseDOM(item, 'a')[0]
                title = re.sub('<.+?>|</.+?>|\\\\|\n', ' ', title).strip()
                title = re.sub('Watch$', '', title).strip()
                title = client.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                url = client.parseDOM(item, 'a', ret='href')[0]
                url = urlparse.urljoin(self.anime_link, url)
                url = url.replace(' ','%20')
                url = client.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                self.list.append({'title': title, 'url': url, 'image': image})
            except:
                pass

        return self.list


    def anime_list_3(self, url):
        try:
            url = urlparse.urljoin(self.anime_link, url)

            result = client.request(url)

            items = client.parseDOM(result, 'div', attrs={'id': 'left_content'})[0]
            items = client.parseDOM(items, 'zi')
        except:
        	return

        for item in items:
            try:
                title = client.parseDOM(item, 'a')[0]
                if '>Movie<' in title: raise Exception()
                title = re.sub('<.+?>|</.+?>|\\\\|\n', '', title).strip()
                title = client.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                url = client.parseDOM(item, 'a', ret='href')[0]
                url = urlparse.urljoin(self.anime_link, url)
                url = url.replace(' ','%20')
                url = client.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = client.parseDOM(item, 'img', ret='src')[0]
                image = urlparse.urljoin(self.anime_link, image)
                image = image.encode('utf-8')

                self.list.append({'title': title, 'url': url, 'image': image})
            except:
                pass

        return self.list


    def anime_resolver(self, url):
        try:
            import urlresolver

            result = client.request(url)

            items = client.parseDOM(result, 'div', attrs = {'class': 'generic-video-item'})
            items = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'span', attrs = {'class': 'type'})) for i in items]
            items = [(i[0][0], i[1][0].lower()) for i in items if len(i[0]) > 0 and len(i[1]) > 0]


            host = 'veevr'
            pattern = '(?://|\.)(veevr.com)/(?:videos|embed)/([A-Za-z0-9]+)'
            link = 'http://veevr.com/embed/%s'

            try: url = [link % re.search(pattern, result).groups()[1]]
            except: url = []
            try: url += [i[0] for i in items if i[1] == host]
            except: pass
            for i in url:
                try:
                    if 'animedreaming.' in i: i = link % re.search(pattern, client.request(i)).groups()[1]

                    u = client.request(i)
                    u = client.parseDOM(u, 'source', ret='src', attrs = {'type': 'video.+?'})[-1]
                    u = client.request(u, output='geturl')

                    r = int(urllib2.urlopen(u, timeout=15).headers['Content-Length'])
                    if r > 1048576: return u
                except:
                    pass


            host = 'mp4upload'
            pattern = '(?://|\.)(mp4upload\.com)/(?:embed-)?([0-9a-zA-Z]+)'
            link = 'http://www.mp4upload.com/embed-%s.html'

            try: url = [link % re.search(pattern, result).groups()[1]]
            except: url = []
            try: url += [i[0] for i in items if i[1] == host]
            except: pass
            for i in url:
                try:
                    if 'animedreaming.' in i: i = link % re.search(pattern, client.request(i)).groups()[1]

                    u = urlresolver.HostedMediaFile(i).resolve()
                    if not u == False: return u
                except:
                    pass


            host = 'engine'
            pattern = '(?://|\.)(auengine\.com)/embed.php\?file=([0-9a-zA-Z\-_]+)[&]*'
            link = 'http://www.auengine.com/embed.php?file=%s'

            try: url = [link % re.search(pattern, result).groups()[1]]
            except: url = []
            try: url += [i[0] for i in items if i[1] == host]
            except: pass
            for i in url:
                try:
                    if 'animedreaming.' in i: i = link % re.search(pattern, client.request(i)).groups()[1]

                    u = urlresolver.HostedMediaFile(i).resolve()
                    if not u == False: return u
                except:
                    pass
        except:
            return


    def addDirectory(self, items, content=None):
        if items == None or len(items) == 0: return

        sysaddon = sys.argv[0]
        sysicon = os.path.join(control.addonInfo('path'), 'resources', 'media')
        sysimage = control.addonInfo('icon')
        sysfanart = control.addonInfo('fanart')

        for i in items:
            try:
                try: label = control.lang(i['title']).encode('utf-8')
                except: label = i['title']

                if 'image' in i and not i['image'] == '0': image = i['image']
                elif 'icon' in i and not i['icon'] == '0': image = os.path.join(sysicon, i['icon'])
                else: image = sysimage

                fanart = i['fanart'] if 'fanart' in i and not i['fanart'] == '0' else sysfanart

                isFolder = False if 'isFolder' in i and not i['isFolder'] == '0' else True

                url = '%s?action=%s' % (sysaddon, i['action'])

                try: url += '&url=%s' % urllib.quote_plus(i['url'])
                except: pass
                try: url += '&tvshowtitle=%s' % urllib.quote_plus(i['tvshowtitle'])
                except: pass
                try: url += '&title=%s' % urllib.quote_plus(i['title'])
                except: pass
                try: url += '&image=%s' % urllib.quote_plus(i['image'])
                except: pass
                try: url += '&fanart=%s' % urllib.quote_plus(i['fanart'])
                except: pass

                meta = dict((k,v) for k, v in i.iteritems() if not v == '0')
                try: meta.update({'duration': str(int(meta['duration']) * 60)})
                except: pass

                item = control.item(label=label, iconImage=image, thumbnailImage=image)

                try: item.setArt({'poster': image, 'tvshow.poster': image, 'season.poster': image, 'banner': image, 'tvshow.banner': image, 'season.banner': image})
                except: pass

                item.setProperty('Fanart_Image', fanart)

                item.addContextMenuItems([])
                item.setInfo(type='Video', infoLabels = meta)
                if isFolder == False: item.setProperty('IsPlayable', 'true')
                control.addItem(handle=int(sys.argv[1]), url=url, listitem=item, isFolder=isFolder)
            except:
                pass

        try:
            i = items[0]
            if i['next'] == '': raise Exception()
            url = '%s?action=%s&url=%s' % (sysaddon, i['nextaction'], urllib.quote_plus(i['next']))
            icon = i['nexticon'] if 'nexticon' in i else os.path.join(sysicon, 'next.png')
            fanart = i['nextfanart'] if 'nextfanart' in i else sysfanart
            item = control.item(label=control.lang(30500).encode('utf-8'), iconImage=icon, thumbnailImage=icon)
            item.setProperty('Fanart_Image', fanart)
            control.addItem(handle=int(sys.argv[1]), url=url, listitem=item, isFolder=True)
        except:
            pass

        if not content == None: control.content(int(sys.argv[1]), content)
        #control.do_block_check(False)
        control.directory(int(sys.argv[1]), cacheToDisc=True)


class player(xbmc.Player):
    def __init__ (self):
        xbmc.Player.__init__(self)

    def run(self, url):
        control.idle()
        title = control.infoLabel('ListItem.Label')
        image = control.infoLabel('ListItem.Icon')
        item = control.item(path=url, iconImage=image, thumbnailImage=image)
        item.setInfo(type='Video', infoLabels = {'title': title})
        control.player.play(url, item)

        for i in range(0, 240):
            if self.isPlayingVideo(): break
            control.sleep(1000)

    def onPlayBackStarted(self):
        control.sleep(200)
        control.idle()


