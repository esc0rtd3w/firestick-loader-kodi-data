# -*- coding: UTF-8 -*-
#######################################################################
 # ----------------------------------------------------------------------------
 # "THE BEER-WARE LICENSE" (Revision 42):
 # @Daddy_Blamo wrote this file.  As long as you retain this notice you
 # can do whatever you want with this stuff. If we meet some day, and you think
 # this stuff is worth it, you can buy me a beer in return. - Muad'Dib
 # ----------------------------------------------------------------------------
#######################################################################

# Addon Name: Placenta
# Addon id: plugin.video.placenta
# Addon Provider: Mr.Blamo

import base64
import json
import random
import re
import urllib

from resources.lib.modules import client
from resources.lib.modules import control


class trailer:
    def __init__(self):
        self.base_link = 'https://www.youtube.com'
        self.key_link = random.choice(['QUl6YVN5RDd2aFpDLTYta2habTVuYlVyLTZ0Q0JRQnZWcnFkeHNz', 'QUl6YVN5Q2RiNEFNenZpVG0yaHJhSFY3MXo2Nl9HNXBhM2ZvVXd3'])
        self.key_link = '&key=%s' % base64.urlsafe_b64decode(self.key_link)
        self.search_link = 'https://www.googleapis.com/youtube/v3/search?part=id&type=video&maxResults=5&q=%s' + self.key_link
        self.youtube_watch = 'https://www.youtube.com/watch?v=%s'

    def play(self, name, url=None, windowedtrailer=0):
        try:
            url = self.worker(name, url)
            if not url: return

            title = control.infoLabel('listitem.title')
            if not title: title = control.infoLabel('listitem.label')
            icon = control.infoLabel('listitem.icon')

            item = control.item(path=url, iconImage=icon, thumbnailImage=icon)
            try: item.setArt({'icon': icon})
            except: pass
            item.setInfo(type='Video', infoLabels={'title': title})
            control.player.play(url, item, windowedtrailer)
            if windowedtrailer == 1:
                # The call to the play() method is non-blocking. So we delay further script execution to keep the script alive at this spot.
                # Otherwise this script will continue and probably already be garbage collected by the time the trailer has ended.
                control.sleep(1000)  # Wait until playback starts. Less than 900ms is too short (on my box). Make it one second.
                while control.player.isPlayingVideo():
                    control.sleep(1000)
                # Close the dialog.
                # Same behaviour as the fullscreenvideo window when :
                # the media plays to the end,
                # or the user pressed one of X, ESC, or Backspace keys on the keyboard/remote to stop playback.
                control.execute("Dialog.Close(%s, true)" % control.getCurrentDialogId)      
        except:
            pass

    def worker(self, name, url):
        try:
            if url.startswith(self.base_link):
                url = self.resolve(url)
                if not url: raise Exception()
                return url
            elif not url.startswith('http:'):
                url = self.youtube_watch % url
                url = self.resolve(url)
                if not url: raise Exception()
                return url
            else:
                raise Exception()
        except:
            query = name + ' trailer'
            query = self.search_link % urllib.quote_plus(query)
            return self.search(query)

    def search(self, url):
        try:
            apiLang = control.apiLanguage().get('youtube', 'en')

            if apiLang != 'en':
                url += "&relevanceLanguage=%s" % apiLang

            result = client.request(url)

            items = json.loads(result).get('items', [])
            items = [i.get('id', {}).get('videoId') for i in items]

            for vid_id in items:
                url = self.resolve(vid_id)
                if url:
                    return url
        except:
            return

    def resolve(self, url):
        try:
            id = url.split('?v=')[-1].split('/')[-1].split('?')[0].split('&')[0]
            result = client.request(self.youtube_watch % id)

            message = client.parseDOM(result, 'div', attrs={'id': 'unavailable-submessage'})
            message = ''.join(message)

            alert = client.parseDOM(result, 'div', attrs={'id': 'watch7-notification-area'})

            if len(alert) > 0: raise Exception()
            if re.search('[a-zA-Z]', message): raise Exception()

            url = 'plugin://plugin.video.youtube/play/?video_id=%s' % id
            return url
        except:
            return
