#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib, urllib2, re, xbmcplugin, xbmcgui, os
import xml.etree.ElementTree as ET
import cookielib
import settings, time
from t0mm0.common.net import Net
import xbmcaddon
import io
import json
import random
import datetime
import xbmc
from operator import itemgetter
from threading import Thread
from datetime import date
from PlayListRipper import PlayListRipper
from PlayListSearcher import PlayListSearcher

cookie_jar = settings.cookie_jar()
net = Net()
addonID = 'plugin.video.kmusictube'
addon = xbmcaddon.Addon(id=addonID)
ADDON = settings.addon()
xbox = xbmc.getCondVisibility("System.Platform.xbox")
ARTIST_ART = settings.artist_icons()
FAV_ARTIST = settings.favourites_file_artist()
FAV_ALBUM = settings.favourites_file_album()
FAV_SONG = settings.favourites_file_songs()
PLAYLIST_FILE = settings.playlist_file()
cacheDir = settings.music_dir()
MUSIC_DIR = settings.music_dir()
blacklist = addon.getSetting("blacklist").split(',')
infoType = addon.getSetting("infoType")
infoDelay = int(addon.getSetting("infoDelay"))
infoEnabled = addon.getSetting("showInfo") == "true"
infoDuration = int(addon.getSetting("infoDuration"))
forceView = addon.getSetting("forceView") == "true"
viewIDVideos = str(addon.getSetting("viewIDVideos"))
viewIDPlaylists = str(addon.getSetting("viewIDPlaylists"))
viewIDGenres = str(addon.getSetting("viewIDGenres"))
art_db_file = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.kmusictube', 'resources/art_db.json'))
fanart = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.kmusictube', 'fanart.jpg'))
art = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.kmusictube', 'art')) + '/'
artgenre = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.kmusictube/art', 'genre')) + '/'
artbillboard = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.kmusictube/art', 'billboard')) + '/'
itunesShowSubGenres = addon.getSetting("itunesShowSubGenres") == "true"
itunesForceCountry = addon.getSetting("itunesForceCountry") == "true"
itunesCountry = addon.getSetting("itunesCountry")
spotifyForceCountry = addon.getSetting("spotifyForceCountry") == "true"
spotifyCountry = addon.getSetting("spotifyCountry")
region = xbmc.getLanguage(xbmc.ISO_639_1, region=True).split("-")[1]
urllist = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.kmusictube', 'lists', 'mp3url.list'))
audio_fanart = ""
iconart = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.kmusictube', 'icon.png'))
RADIO99_URL = "http://eco99fm.maariv.co.il"
LASTFM_URL = 'http://www.last.fm/music/'
MAKO_URL = 'http://media.shironet.mako.co.il'
urlMainBB = "http://www.billboard.com"
urlMainHypem = "http://hypem.com"
urlMainGLZ = "http://www.glgltz.co.il"

glz_black_list = ["שערי משפט", "קשישים","פרומו","אתנה", "בטיחות וגהות ארגונומיה", "חנה וסע קריין","ביטוח ישיר", "גלגלצ"]

pluginhandle = int(sys.argv[1])
opener = urllib2.build_opener()

if itunesForceCountry and itunesCountry:
    iTunesRegion = itunesCountry
else:
    iTunesRegion = region
if spotifyForceCountry and spotifyCountry:
    spotifyRegion = spotifyCountry
else:
    spotifyRegion = region

favourite_paths = [FAV_ARTIST, FAV_ALBUM, FAV_SONG,PLAYLIST_FILE]

with io.open(art_db_file, 'r', encoding='utf-8') as fh:
    art_dict = json.load(fh)
'''
art_dict = {}
for item in jo["artists"]:
    name = item.pop('artist')
    art_dict[name] = item
'''
'''
**********************************************************************************************************************
general categories functions
**********************************************************************************************************************
'''
'''
=========CATEGORIES============
'''

def CATEGORIES():
    addDir(translation(40000), 'http://shironet.mako.co.il/html/indexes/performers/', 'israeli_artists','', '')
    addDir(translation(40001), 'url', 'ENGLISH_CATEGORIES', '', '')
    addDir(translation(40002), 'url', 'CHARTS_CATEGORIES','', '')
    addDir(translation(40003), 'url', 'youtube_playlist_search', '', '')
    addDir(translation(40004), 'url', 'FAVOURITE_CATEGORIES', '', '')


'''
=========FAVOURITE_CATEGORIES============
'''


def FAVOURITE_CATEGORIES():
    addDir(translation(40010), '0', 'show_favourites', '', '')
    addDir(translation(40016), '1', 'show_favourites', '', '')
    addDir(translation(40011), '2', 'show_favourites', '', '')
    addDir(translation(40012), '3', 'show_favourites', '', '')
    addDir(translation(40013), '2', 'play_favourites_albums', '', '')
    addDir(translation(40014), '2', 'play_favourites_songs', '', '')
    addDir(translation(40015), '2', 'clean_favourites_categories', '', '')
    xbmcplugin.endOfDirectory(pluginhandle)


'''
=========ENGLISH_CATEGORIES============
'''


def ENGLISH_CATEGORIES():
    addDir(translation(40020), 'http://musicmp3.ru/artists.html', 'artists', art + 'artists.jpg', '')
    addDir(translation(40021), 'http://musicmp3.ru/genres.html', 'genres', art + 'topalbums.jpg', '')
    addDir(translation(40022), 'http://musicmp3.ru/new_albums.html', 'genres', art + 'newalbums.jpg', '')
    addDir(translation(40023), 'url', 'compilations_menu', '', '')
    addDir(translation(40024), 'url', 'eng_search_cat', art + 'searchartists.jpg', '')
    xbmcplugin.endOfDirectory(pluginhandle)


def CHARTS_CATEGORIES():
    addYTDir(translation(40030), "url", "billboardMain", "", "")
    addYTDir(translation(40031), "url", "hypemMain", "", "")
    addYTDir(translation(40032), "url", "itunesMain", "", "")
    addYTDir(translation(40033), "url", "spotifyMain", "", "")
    addYTDir(translation(40034), "url", "GalgalatzMain", "http://www.exioma.co.il/wp-content/uploads/2013/11/galgalaz.png")
    addYTDir("ECO99FM", "url", "fm99_main", "http://i.img.co/radio/86/15/21586_290.png")
    addYTDir(translation(40035), "", "OneFmMain", "http://www.onefmonline.com/images/logo.jpg")
    addYTDir(translation(40036), "", "DisiMain", "http://creatives.co.il/upload/files/1ff4b1bc493d86739b256ec6d274b2e4.png")
    xbmcplugin.endOfDirectory(pluginhandle)


'''
**********************************************************************************************************************
hebrew music functions
**********************************************************************************************************************
'''
'''
=========search_heb_songs============
'''


def search_heb_songs(query):
    for item in art_dict.iteritems():
        for song in item[1]['all_songs']:
            if query in song.encode('utf-8'):
                artist = item[0].encode('utf-8')
                songname = song.encode('utf-8')
                fullname = artist + " - " + songname
                url = artist + " " + songname
                img = item[1]["artist_img"].encode('utf-8')
                addYTLink(fullname, url, 'playYTByTitle', img, songname, artist, "", "", "hebrew","search")


'''
=========search_heb_artists============
'''


def search_heb_artists(query):
    for item in art_dict.iteritems():
        if query in item[0].encode('utf-8'):
            addDir(item[0].encode('utf-8'), item[0].encode('utf-8'), 'israeli_artists_works',
                   art_dict.get(item[0]).get("artist_img").encode('utf-8'), 'hebartists','','search')
    if forceView:
        xbmc.executebuiltin('Container.SetViewMode(' + viewIDPlaylists + ')')


'''
=========search_heb_albums============
'''


def search_heb_albums(query):
    for item in art_dict.iteritems():
        for disk in item[1]['disks']:
            if query in disk["disk_name"].encode('utf-8'):
                addDir(item[0].encode('utf-8') + " - " + disk["disk_name"].encode('utf-8'),
                       '/artist?type=single_disk&perf=' + item[0].encode('utf-8').replace(" ", "+") + "&disk=" + disk[
                           "disk_name"].encode('utf-8'), 'play_israeli_album', disk["disk_img"].encode('utf-8'), 'hebalbum','browse',"search")


'''
=========heb_search_input============
'''


def heb_search_input(name):
    keyboard = xbmc.Keyboard('', name, False)
    keyboard.doModal()
    if keyboard.isConfirmed():
        query = keyboard.getText()
        if len(query) > 0:
            if name == translation(40040):
                search_heb_artists(query)
            elif name == translation(40041):
                search_heb_albums(query)
            elif name == translation(40042):
                search_heb_songs(query)


'''
=========heb_search_cat============
'''


def heb_search_cat(name):
    addDir(translation(40040), 'url', 'heb_search_input', art + 'searchartists.jpg', '')
    addDir(translation(40041), 'url', 'heb_search_input', art + 'searchalbums.jpg', '')
    addDir(translation(40042), 'url', 'heb_search_input', art + 'searchsongs.jpg', '')


'''
=========play_israeli_album============
'''


def play_israeli_album(url, action):
    if action == "play":
        musicVideos = []
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
    splitdata = url.split('/')
    type = splitdata[0]
    artist = splitdata[1].replace("+", " ")
    disk_name = splitdata[2].replace("+", " ")
    if type == "single_disk":
        for item in art_dict[artist.decode('utf-8')]["disks"]:
            if item["disk_name"].encode('utf-8') == disk_name:
                for track in item["tracks"]:
                    songname = track.encode('utf-8')
                    url = artist + " " + songname
                    img = item["disk_img"].encode('utf-8')
                    album = item["disk_name"].encode('utf-8')
                    if action == 'browse':
                        addYTLink(songname, url, 'playYTByTitle', img, songname, artist, album, "", "hebrew")
                    else:
                        title = artist + " - " + songname
                        if xbox:
                            url = "plugin://video/Youtube Music/?url=" + urllib.quote_plus(
                                title.replace(" - ", " ")) + "&mode=playYTByTitle&addontype=YTM"
                        else:
                            url = "plugin://" + addonID + "/?url=" + urllib.quote_plus(
                                    title.replace(" - ", " ")) + "&mode=playYTByTitle&addontype=YTM"
                        musicVideos.append([title, url, ""])
    else:
        for song in art_dict.get(artist.decode('utf-8')).get("all_songs"):
            songname = song.encode('utf-8')
            url = artist + " " + songname
            img = art_dict.get(artist.decode('utf-8')).get("artist_img").encode('utf-8')
            album = ""
            if action == 'browse':
                addYTLink(songname, url, 'playYTByTitle', img, songname, artist, album, "", "hebrew")
            else:
                title = artist + " - " + songname
                if xbox:
                    url = "plugin://video/Youtube Music/?url=" + urllib.quote_plus(
                        title.replace(" - ", " ")) + "&mode=playYTByTitle&addontype=YTM"
                else:
                    url = "plugin://" + addonID + "/?url=" + urllib.quote_plus(
                        title.replace(" - ", " ")) + "&mode=playYTByTitle&addontype=YTM"
                musicVideos.append([title, url, ""])
    if action == "browse":
        xbmcplugin.endOfDirectory(pluginhandle)
    else:
        random.shuffle(musicVideos)
        for title, url, thumb in musicVideos:
            listitem = xbmcgui.ListItem(title, thumbnailImage=thumb)
            playlist.add(url, listitem)
        xbmc.Player().play(playlist)



'''
=========israeli_artists_works============
'''


def israeli_artists_works(url):
    artist = url
    addDir(translation(40050), 'all/' + artist.replace(" ", "+") + "/disk=all", 'play_israeli_album',
           art_dict[artist.decode('utf-8')]["artist_img"].encode('utf-8'), '','browse')
    for disk in art_dict[artist.decode('utf-8')]["disks"]:
        addDir(disk["disk_name"].encode('utf-8'),
               'single_disk/' + artist.replace(" ", "+") + "/" + disk["disk_name"].encode('utf-8'),
               'play_israeli_album', disk["disk_img"].encode('utf-8'), 'hebalbum', 'browse')


'''
=========israeli_single_char_artists============
'''


def israeli_single_char_artists(url):
    link = GET_url(url)
    artists_data = re.compile('<a class="index_link" href="(.+?)">\s*(.+?)\s*<\/a>\s*<br>').findall(link)

    page_id = 1
    while (("הבא") in link):
        page_id += 1
        link = GET_url(url + str(page_id))
        artists_data = artists_data + re.compile('<a class="index_link" href="(.+?)">\s*(.+?)\s*<\/a>\s*<br>').findall(
            link)

    for url, artist in artists_data:
        try:
            addDir(artist, artist, 'israeli_artists_works',
                   art_dict[artist.decode('utf-8')]["artist_img"].encode('utf-8'), 'hebartists')
        except:
            print "bad artist name " + artist
            continue
    if forceView:
        xbmc.executebuiltin('Container.SetViewMode(' + viewIDPlaylists + ')')


'''
=========israeli_artists============
'''


def israeli_artists(url):
    heb_chars = ['א', 'ב', 'ג', 'ד', 'ה', 'ו', 'ז', 'ח', 'ט', 'י', 'כ', 'ל', 'מ', 'נ', 'ס', 'ע', 'פ', 'צ', 'ק', 'ר',
                 'ש', 'ת']
    link = GET_url(url)
    addDir(translation(40024), 'url', 'heb_search_cat', art + 'allartists.jpg', '')
    for heb_char in heb_chars:
        addDir(heb_char,
               'http://shironet.mako.co.il/servlet/com.dic.shironet.site.index.servletGetPerformersIndexPrefix?lang=1&prefix=' + heb_char + '&sort=popular&page=1',
               'israeli_single_char_artists', art + 'allartists.jpg', '')


'''
**********************************************************************************************************************
english music search functions
**********************************************************************************************************************
'''
'''
=========eng_search_cat============
'''


def eng_search_cat():
    addDir(translation(40040), 'Search_Artists', 'eng_search_input', art + 'searchartists.jpg', '')
    addDir(translation(40041), 'Search_Albums', 'eng_search_input', art + 'searchalbums.jpg', '')
    addDir(translation(40042), 'Search_Songs', 'eng_search_input', art + 'searchsongs.jpg', '')


'''
=========eng_search_input============
'''


def eng_search_input(url):
    keyboard = xbmc.Keyboard('', name, False)
    keyboard.doModal()
    if keyboard.isConfirmed():
        query = keyboard.getText()
        if len(query) > 0:
            if url == 'Search_Artists':
                search_artists(query)
            elif url == 'Search_Albums':
                search_albums(query)
            elif url == 'Search_Songs':
                search_songs(query)


'''
=========search_artists============
'''


def search_artists(query):
    url = 'http://musicmp3.ru/search.html?text=%s&all=artists' % urllib.quote_plus(query)
    link = GET_url(url)
    all_artists = re.compile('<a class="artist_preview__title" href="(.+?)">(.+?)</a>').findall(link)
    for url1, title in all_artists:
        icon_path = os.path.join(ARTIST_ART, title + '.jpg')
        if os.path.exists(icon_path):
            iconimage = icon_path
        else:
            iconimage = iconart
        addDir(title.replace('&amp;', 'and'), 'http://musicmp3.ru' + url1, 'albums', iconimage, 'artists','',"search")
    if forceView:
        xbmc.executebuiltin('Container.SetViewMode(' + viewIDPlaylists + ')')


'''
=========search_albums============
'''


def search_albums(query):
    url = 'http://musicmp3.ru/search.html?text=%s&all=albums' % urllib.quote_plus(
        query.replace(' - ', ' ').replace('-', ' '))
    link = GET_url(url)
    link = link.replace('<span class="album_report__artist">Various Artists</span>',
                        '<a class="album_report__artist" href="/artist_various-artist.html">Various Artist</a>')
    all_albums = re.compile(
        '<a class="album_report__link" href="(.+?)"><img class="album_report__image" src="(.+?)" /><span class="album_report__name">(.+?)</span></a>(.+?)album_report__artist" href="(.+?)">(.+?)</a>, <span class="album_report__date">(.+?)</span>').findall(
        link)
    for url1, thumb, album, plot, artisturl, artist, year in all_albums:
        title = "%s - %s (%s)" % (artist, album, year)
        thumb = thumb.replace('al', 'alm').replace('covers', 'mcovers')
        addDir(title.replace('&amp;', 'and'), 'http://musicmp3.ru' + url1, 'play_album', thumb, 'albums','browse',"search")
    if forceView:
        xbmc.executebuiltin('Container.SetViewMode(' + viewIDPlaylists + ')')


'''
=========search_songs============
'''


def search_songs(query):
    playlist = []
    url = 'http://musicmp3.ru/search.html?text=%s&all=songs' % urllib.quote_plus(
        query.replace(' - ', ' ').replace('-', ' ').replace(' FT ', ' '))
    link = GET_url(url)
    match = re.compile(
        '<tr class="song"><td class="song__play_button"><a class="player__play_btn js_play_btn" href="#" rel="(.+?)" title="Play track" /></td><td class="song__name song__name--search"><a class="song__link" href="(.+?)">(.+?)</a>(.+?)song__link" href="(.+?)">(.+?)</a>(.+?)<a class="song__link" href="(.+?)">(.+?)</a>').findall(
        link)
    for id, songurl, song, d1, artisturl, artist, d2, albumurl, album in match:
        iconimage = ""
        url = 'http://files.musicmp3.ru/lofi/' + id
        title = "%s - %s - %s" % (
            artist.replace('&amp;', 'and'), song.replace('&amp;', '&'), album.replace('&amp;', '&'))
        addYTLink(title, url, 'playYTByTitle', iconimage, song, artist, album, "", "","search")
        liz = xbmcgui.ListItem(song, iconImage=iconimage, thumbnailImage=iconimage)
        liz.setInfo('music', {'Title': song, 'Artist': artist, 'Album': album})
        liz.setProperty('mimetype', 'audio/mpeg')
        liz.setThumbnailImage(iconimage)
        liz.setProperty('fanart_image', audio_fanart)
        playlist.append((url, liz))
    setView('music', 'song')


'''
**********************************************************************************************************************
english music artists functions
**********************************************************************************************************************
'''
'''
=========artists============
'''


def artists(url):
    link = GET_url(url)
    addDir(translation(40051), 'http://musicmp3.ru/main_artists.html?type=artist&page=1', 'all_artists',
           art + 'allartists.jpg', '')
    sub_dir = re.compile('<li class="menu_sub__item"><a class="menu_sub__link" href="(.+?)">(.+?)</a></li>').findall(
        link)
    for url1, title in sub_dir:
        iconimage = 'http://musicmp3.ru/i' + url1.replace('.html', '.jpg').replace('artists', 'genres').replace(
            'tracks', 'track')
        if title != 'Other':
            addDir(title.replace('&amp;', '&'), 'http://musicmp3.ru' + url1, 'sub_dir',
                       artgenre + title.replace(' ', '').replace('&amp;', '_').lower() + '.jpg', '')
    if forceView:
        xbmc.executebuiltin('Container.SetViewMode(' + viewIDPlaylists + ')')


'''
=========sub_dir============
'''


def sub_dir(name, url, icon):
    link = GET_url(url)
    addDir(translation(40051)+ " - " +name, url + '?page=1', 'all_artists',
           artgenre + name.replace(' ', '').replace('&amp;', '_').lower() + '/' + 'top' + name.replace(' ', '').replace(
               '&amp;', '_').lower() + '.jpg', '')
    sub_dir = re.compile('<li class="menu_sub__item"><a class="menu_sub__link" href="(.+?)">(.+?)</a></li>').findall(
        link)
    for url, title in sub_dir:
        addDir(title.replace('&amp;', 'and'), 'http://musicmp3.ru' + url + '?page=1', 'all_artists',
                   artgenre + name.replace(' ', '').replace('&amp;', '_').lower() + '/' + title.replace(' ',
                                                                                                        '').replace(
                       '&amp;', '_').lower() + '.jpg', '')


'''
=========all_artists============
'''


def all_artists(name, url):
    link = GET_url(url)
    all_artists = re.compile(
        '<li class="small_list__item"><a class="small_list__link" href="(.+?)">(.+?)</a></li>').findall(link)
    for url1, title in all_artists:
        try:
            fh = open(os.path.join(ARTIST_ART, title + '.txt'), 'r')
            iconimage = fh.read()
            fh.close()
        except:
            get_artist_img(title)
            iconimage = ''
        addDir(title.replace('&amp;', 'and'), 'http://musicmp3.ru' + url1, 'albums', iconimage, 'artists')
    pgnumf = url.find('page=') + 5
    pgnum = int(url[pgnumf:]) + 1
    nxtpgurl = url[:pgnumf]
    nxtpgurl = "%s%s" % (nxtpgurl, pgnum)
    addDir(translation(40053), nxtpgurl, 'all_artists',
           xbmc.translatePath(os.path.join('special://home/addons/plugin.video.kmusictube', 'art', 'nextpage.jpg')), '')
    if forceView:
        xbmc.executebuiltin('Container.SetViewMode(' + viewIDPlaylists + ')')
    setView('albums', 'default')


'''
=========albums============
'''


def albums(name, url):
    duplicate = []
    link = GET_url(url)
    all_albums = re.compile(
        '<div class="album_report"><h5 class="album_report__heading"><a class="album_report__link" href="(.+?)"><img alt="(.+?)" class="album_report__image" src="(.+?)" /><span class="album_report__name">(.+?)</span>(.+?)<span class="album_report__date">(.+?)</span>').findall(
        link)
    for url1, d1, thumb, album, plot, year in all_albums:
        title = "%s - %s - %s" % (name, album, year)
        if title not in duplicate:
            duplicate.append(title)
            thumb = thumb.replace('al', 'alm').replace('covers', 'mcovers')
            addDir(title.replace('&amp;', 'and'), 'http://musicmp3.ru' + url1, 'play_album', thumb, 'albums', 'browse')
    if forceView:
        xbmc.executebuiltin('Container.SetViewMode(' + viewIDPlaylists + ')')


'''
**********************************************************************************************************************
english music albums functions
**********************************************************************************************************************
'''
'''
=========genres============
'''


def genres(name, url):
    link = GET_url(url)
    if name == translation(40062):
        addDir(translation(40060), 'http://musicmp3.ru/main_albums.html?gnr_id=&sort=top&type=album&page=1', 'album_list',
               art + 'alltopalbums.jpg', '')
    else:
        addDir(translation(40061), url + '?page=1', 'album_list', art + 'allnewalbums.jpg', '')
    sub_dir = re.compile('<li class="menu_sub__item"><a class="menu_sub__link" href="(.+?)">(.+?)</a></li>').findall(
        link)
    for url1, title in sub_dir:
        iconimage = 'http://musicmp3.ru/i' + url1.replace('.html', '.jpg').replace('tracks', 'track')
        addDir(title.replace('&amp;', 'and'), 'http://musicmp3.ru' + url1, 'genre_sub_dir',
               artgenre + title.replace(' ', '').replace('&amp;', '_').lower() + '.jpg', '')


'''
=========genre_sub_dir============
'''


def genre_sub_dir(name, url, icon):
    link = GET_url(url)
    addDir(translation(40062)+ ' - ' + name, url + '?page=1', 'album_list',
           artgenre + name.replace('and', '&').replace(' ', '').replace('&amp;',
                                                                        '_').lower() + '/' + 'top' + name.replace('and',
                                                                                                                  '_').replace(
               ' ', '').replace('&amp;', '_').lower() + '.jpg', '')
    sub_dir = re.compile('<li class="menu_sub__item"><a class="menu_sub__link" href="(.+?)">(.+?)</a></li>').findall(
        link)
    for url, title in sub_dir:
        addDir(title.replace('&amp;', 'and'), 'http://musicmp3.ru' + url + '?page=1', 'album_list',
                   artgenre + name.replace('and', '&').replace(' ', '').replace('&amp;','_').lower() + '/' + title.replace(' ','').replace('&amp;', '_').lower() + '.jpg', '')

'''
=========album_list============
'''


def album_list(name, url):
    link = GET_url(url)
    all_albums = re.compile(
        '<a class="album_report__link" href="(.+?)"><img alt="(.+?)" class="album_report__image" src="(.+?)" /><span class="album_report__name">(.+?)</span>(.+?)"album_report__artist" href="(.+?)">(.+?)</a>, <span class="album_report__date">(.+?)</span>').findall(
        link)
    for url1, d1, thumb, album, plot, artisturl, artist, year in all_albums:
        title = "%s - %s - %s" % (artist, album, year)
        thumb = thumb.replace('al', 'alm').replace('covers', 'mcovers')
        addDir(title.replace('&amp;', 'and'), 'http://musicmp3.ru' + url1, 'play_album', thumb, 'albums', 'browse')
    pgnumf = url.find('page=') + 5
    pgnum = int(url[pgnumf:]) + 1
    nxtpgurl = url[:pgnumf]
    nxtpgurl = "%s%s" % (nxtpgurl, pgnum)
    addDir(translation(40053), nxtpgurl, 'album_list',
           xbmc.translatePath(os.path.join('special://home/addons/plugin.video.kmusictube', 'art', 'nextpage.jpg')), '')
    if forceView:
        xbmc.executebuiltin('Container.SetViewMode(' + viewIDPlaylists + ')')

'''
**********************************************************************************************************************
english compilations functions
**********************************************************************************************************************
'''
'''
=========compilations_menu============
'''


def compilations_menu():
    addDir(translation(40070), 'http://www.goldenmp3.ru/albums_showcase.html?section=compilations&type=albums&page=',
           'compilations_list', art + 'topalbums.jpg', '1')
    addDir(translation(40071),
           'http://www.goldenmp3.ru/albums_showcase.html?section=compilations&sort=new&type=albums&page=',
           'compilations_list', art + 'newalbums.jpg', '1')
    addDir(translation(40072),
           'http://www.goldenmp3.ru/albums_showcase.html?gnr_id=806&section=compilations&type=albums&page=',
           'compilations_list', art + 'newalbums.jpg', '1')
    addDir(translation(40073),
           'http://www.goldenmp3.ru/albums_showcase.html?gnr_id=822&section=compilations&type=albums&page=',
           'compilations_list', art + 'newalbums.jpg', '1')
    addDir(translation(40074),
           'http://www.goldenmp3.ru/albums_showcase.html?gnr_id=848&section=compilations&type=albums&page=',
           'compilations_list', art + 'newalbums.jpg', '1')
    addDir(translation(40075),
           'http://www.goldenmp3.ru/albums_showcase.html?gnr_id=872&section=compilations&type=albums&page=',
           'compilations_list', art + 'newalbums.jpg', '1')
    addDir(translation(40076), 'http://www.goldenmp3.ru/compilations/events/albums', 'compilations_list', art + 'newalbums.jpg',
           'n')


'''
=========compilations_list============
'''


def compilations_list(name, url, iconimage, page):
    if page != 'n':
        nextpage = int(page) + 1
        nxtpgurl = "%s%s" % (url, nextpage)
        url = "%s%s" % (url, page)
    link = open_url(url)
    match = re.compile(
        '<a href="(.+?)"><img alt="(.+?)" src="(.+?)" /></a><a class="(.+?)" href="(.+?)">(.+?)</a><span class="(.+?)">(.+?)</span><span class="f_year">(.+?)</span><span class="ga_price">(.+?)</span></div>').findall(
        link)
    for url, d1, iconimage, cl, url2, title, cl, artist, year, prc in match:
        url = 'http://www.goldenmp3.ru' + url
        addDir(title.replace('&amp;', 'and'), url, 'play_album', iconimage, 'albums', 'browse')
    addDir(translation(40053), nxtpgurl, 'compilations_list',
           xbmc.translatePath(os.path.join('special://home/addons/plugin.video.kmusictube', 'art', 'nextpage.jpg')),
           str(nextpage))
    if forceView:
        xbmc.executebuiltin('Container.SetViewMode(' + viewIDPlaylists + ')')

'''
**********************************************************************************************************************
billboard functions
**********************************************************************************************************************
'''


def billboardMain():
    addAutoPlayDir(translation(30005), urlMainBB + "/rss/charts/hot-100", "listBillboardCharts", "", "", "browse")
    addAutoPlayDir("Trending 140", "Top 140 in Trending", "listBillboardChartsNew", "", "", "browse")
    addAutoPlayDir("Last 24 Hours", "Top 140 in Overall", "listBillboardChartsNew", "", "", "browse")
    addYTDir(translation(30006), "genre", "listBillboardChartsTypes", "", "", "browse")
    addYTDir(translation(30007), "country", "listBillboardChartsTypes", "", "", "browse")
    addYTDir(translation(30008), "other", "listBillboardChartsTypes", "", "", "browse")
    xbmcplugin.endOfDirectory(pluginhandle)


def listBillboardArchiveMain():
    for i in range(date.today().year, 1957, -1):
        addAutoPlayDir(str(i), urlMainBB + "/archive/charts/" + str(i), "listBillboardArchive", "", "", "browse")
    xbmcplugin.endOfDirectory(pluginhandle)


def listBillboardArchive(url):
    content = cache(url, 30)
    match = re.compile('class="field-content">.+?href="(.+?)">(.+?)<', re.DOTALL).findall(content)
    for url, title in match:
        if not "billboard 200" in title.lower() and not "album" in title.lower():
            addAutoPlayDir(cleanTitle(title), urlMainBB + url, "listBillboardArchiveVideos", "", "", "browse")
    xbmcplugin.endOfDirectory(pluginhandle)


def listBillboardArchiveVideos(type, url, limit):
    if type == "play":
        musicVideos = []
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
    content = cache(url, 30)
    match = re.compile('views-field-field-chart-item-song.+?>(.+?)<.+?href="/artist/.+?">(.+?)<', re.DOTALL).findall(
        content)
    pos = 1
    for title, artist in match:
        title = title.strip()
        songname = title
        if title.lower() != "song":
            title = cleanTitle(artist + " - " + title)
            filtered = False
            for entry2 in blacklist:
                if entry2.strip().lower() and entry2.strip().lower() in title.lower():
                    filtered = True
            if filtered:
                continue
            if type == "browse":
                addYTLink(title, title.replace(" - ", " "), "playYTByTitle", "", songname, artist, "", "", "")
            else:
                if xbox:
                    url = "plugin://video/Youtube Music/?url=" + urllib.quote_plus(
                        title.replace(" - ", " ")) + "&mode=playYTByTitle&addontype=YTM"
                else:
                    url = "plugin://" + addonID + "/?url=" + urllib.quote_plus(
                        title.replace(" - ", " ")) + "&mode=playYTByTitle&addontype=YTM"
                musicVideos.append([title, url, ""])
                if limit and int(limit) == pos:
                    break
                pos += 1
    if type == "browse":
        xbmcplugin.endOfDirectory(pluginhandle)
    else:
        random.shuffle(musicVideos)
        for title, url, thumb in musicVideos:
            listitem = xbmcgui.ListItem(title, thumbnailImage=thumb)
            playlist.add(url, listitem)
        xbmc.Player().play(playlist)


def listBillboardChartsTypes(type):
    if type == "genre":
        addAutoPlayDir(translation(30009), urlMainBB + "/rss/charts/pop-songs", "listBillboardCharts", "", "", "browse")
        addAutoPlayDir(translation(30010), urlMainBB + "/rss/charts/rock-songs", "listBillboardCharts", "", "",
                       "browse")
        addAutoPlayDir(translation(30011), urlMainBB + "/rss/charts/alternative-songs", "listBillboardCharts", "", "",
                       "browse")
        addAutoPlayDir(translation(30012), urlMainBB + "/rss/charts/r-b-hip-hop-songs", "listBillboardCharts", "", "",
                       "browse")
        addAutoPlayDir(translation(30013), urlMainBB + "/rss/charts/r-and-b-songs", "listBillboardCharts", "", "",
                       "browse")
        addAutoPlayDir(translation(30014), urlMainBB + "/rss/charts/rap-songs", "listBillboardCharts", "", "", "browse")
        addAutoPlayDir(translation(30015), urlMainBB + "/rss/charts/country-songs", "listBillboardCharts", "", "",
                       "browse")
        addAutoPlayDir(translation(30016), urlMainBB + "/rss/charts/latin-songs", "listBillboardCharts", "", "",
                       "browse")
        addAutoPlayDir(translation(30017), urlMainBB + "/rss/charts/jazz-songs", "listBillboardCharts", "", "",
                       "browse")
        addAutoPlayDir(translation(30018), urlMainBB + "/rss/charts/dance-club-play-songs", "listBillboardCharts", "",
                       "", "browse")
        addAutoPlayDir(translation(30019), urlMainBB + "/rss/charts/dance-electronic-songs", "listBillboardCharts", "",
                       "", "browse")
        addAutoPlayDir(translation(30020), urlMainBB + "/rss/charts/heatseekers-songs", "listBillboardCharts", "", "",
                       "browse")
    elif type == "country":
        addAutoPlayDir(translation(30021), urlMainBB + "/rss/charts/canadian-hot-100", "listBillboardCharts", "", "",
                       "browse")
        addAutoPlayDir(translation(30022), urlMainBB + "/rss/charts/k-pop-hot-100", "listBillboardCharts", "", "",
                       "browse")
        addAutoPlayDir(translation(30023), urlMainBB + "/rss/charts/japan-hot-100", "listBillboardCharts", "", "",
                       "browse")
        addAutoPlayDir(translation(30024), urlMainBB + "/rss/charts/germany-songs", "listBillboardCharts", "", "",
                       "browse")
        addAutoPlayDir(translation(30025), urlMainBB + "/rss/charts/france-songs", "listBillboardCharts", "", "",
                       "browse")
        addAutoPlayDir(translation(30026), urlMainBB + "/rss/charts/united-kingdom-songs", "listBillboardCharts", "",
                       "", "browse")
    elif type == "other":
        addAutoPlayDir(translation(30028), urlMainBB + "/rss/charts/radio-songs", "listBillboardCharts", "", "",
                       "browse")
        addAutoPlayDir(translation(30029), urlMainBB + "/rss/charts/digital-songs", "listBillboardCharts", "", "",
                       "browse")
        addAutoPlayDir(translation(30030), urlMainBB + "/rss/charts/streaming-songs", "listBillboardCharts", "", "",
                       "browse")
        addAutoPlayDir(translation(30031), urlMainBB + "/rss/charts/on-demand-songs", "listBillboardCharts", "", "",
                       "browse")
    xbmcplugin.endOfDirectory(pluginhandle)


def listBillboardCharts(type, url, limit):
    if type == "play":
        musicVideos = []
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
    content = cache(url, 1)
    match = re.compile('<item>.+?<artist>(.+?)</artist>.+?<chart_item_title>(.+?)</chart_item_title>',
                       re.DOTALL).findall(content)
    pos = 1
    for artist, title in match:
        songname = title[title.find(":") + 1:]
        title = cleanTitle(artist + " - " + title[title.find(":") + 1:]).replace("Featuring", "Feat.")
        if type == "browse":
            addYTLink(title, title.replace(" - ", " "), "playYTByTitle", "", songname, artist, "", "", "")
            # addLink(title, title.replace(" - ", " "), "playYTByTitle", "")
        else:
            if xbox:
                url = "plugin://video/Youtube Music/?url=" + urllib.quote_plus(
                    title.replace(" - ", " ")) + "&mode=playYTByTitle&addontype=YTM"
            else:
                url = "plugin://" + addonID + "/?url=" + urllib.quote_plus(
                    title.replace(" - ", " ")) + "&mode=playYTByTitle&addontype=YTM"
            musicVideos.append([title, url, ""])
            if limit and int(limit) == pos:
                break
            pos += 1
    if type == "browse":
        xbmcplugin.endOfDirectory(pluginhandle)
    else:
        random.shuffle(musicVideos)
        for title, url, thumb in musicVideos:
            listitem = xbmcgui.ListItem(title, thumbnailImage=thumb)
            playlist.add(url, listitem)
        xbmc.Player().play(playlist)


def listBillboardChartsNew(type, url, limit):
    if type == "play":
        musicVideos = []
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
    content = opener.open("http://realtime.billboard.com/").read()
    content = content[content.find("<h1>" + url + "</h1>"):]
    content = content[:content.find("</table>")]
    match = re.compile(
        '<tr>.*?<td>(.+?)</td>.*?<td><a href=".*?">(.+?)</a></td>.*?<td>(.+?)</td>.*?<td>(.+?)</td>.*?</tr>',
        re.DOTALL).findall(content)
    pos = 1
    for nr, artist, title, rating in match:
        if "(" in title:
            title = title[:title.find("(")].strip()
        songname = title
        title = cleanTitle(artist + " - " + title).replace("Featuring", "Feat.")
        if type == "browse":
            addYTLink(title, title.replace(" - ", " "), "playYTByTitle", "", songname, artist, "", "", "")
            # addLink(title, title.replace(" - ", " "), "playYTByTitle", "")
        else:
            if xbox:
                url = "plugin://video/Youtube Music/?url=" + urllib.quote_plus(
                    title.replace(" - ", " ")) + "&mode=playYTByTitle&addontype=YTM"
            else:
                url = "plugin://" + addonID + "/?url=" + urllib.quote_plus(
                    title.replace(" - ", " ")) + "&mode=playYTByTitle&addontype=YTM"
            musicVideos.append([title, url, ""])
            if limit and int(limit) == pos:
                break
            pos += 1
    if type == "browse":
        xbmcplugin.endOfDirectory(pluginhandle)
    else:
        random.shuffle(musicVideos)
        for title, url, thumb in musicVideos:
            listitem = xbmcgui.ListItem(title, thumbnailImage=thumb)
            playlist.add(url, listitem)
        xbmc.Player().play(playlist)


def hypemMain():
    addAutoPlayDir(translation(40080), urlMainHypem + "/popular?ax=1&sortby=shuffle", 'listHypem', "", "", "browse")
    addAutoPlayDir(translation(40081), urlMainHypem + "/popular/lastweek?ax=1&sortby=shuffle", 'listHypem', "", "",
                   "browse")
    addAutoPlayDir(translation(40082), "", 'listTimeMachine', "", "", "browse")
    xbmcplugin.endOfDirectory(pluginhandle)


def listHypem(type, url, limit):
    musicVideos = []
    if type == "play":
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
    parentUrl = url
    if url == urlMainHypem + "/popular?ax=1&sortby=shuffle":
        content = cache(url, 0)
    else:
        content = cache(url, 1)
    match = re.compile('class="rank">(.+?)<.+?href="/artist/.+?">(.+?)<.+?class="base-title">(.+?)<',
                       re.DOTALL).findall(content)
    spl = content.split('class="rank"')
    for i in range(1, len(spl), 1):
        entry = spl[i]
        match = re.compile('>(.+?)<', re.DOTALL).findall(entry)
        rank = match[0]
        match = re.compile('href="/artist/.+?">(.+?)<', re.DOTALL).findall(entry)
        artist = match[0]
        match = re.compile('class="base-title">(.+?)<', re.DOTALL).findall(entry)
        title = match[0]
        match = re.compile('class="remix-link">(.+?)<', re.DOTALL).findall(entry)
        if match:
            title += " - " + match[0]
        match = re.compile('class="thumb".+?background:url\\((.+?)\\)', re.DOTALL).findall(entry)
        thumb = ""
        if match:
            thumb = match[0]
        title = cleanTitle(artist.strip() + " - " + title.strip())
        oTitle = title
        '''match=re.compile('class="toggle-reposts">(.+?)<', re.DOTALL).findall(entry)
        if match:
            reposts = match[0]
            reposts = reposts.replace("Posted by","").replace("blogs","").strip()
            title+=" ["+reposts+"+]"'''
        filtered = False
        for entry2 in blacklist:
            if entry2.strip().lower() and entry2.strip().lower() in title.lower():
                filtered = True
        if filtered:
            continue
        if type == "play":
            if xbox:
                url = "plugin://video/Youtube Music/?url=" + urllib.quote_plus(
                    oTitle.replace(" - ", " ")) + "&mode=playYTByTitle&addontype=YTM"
            else:
                url = "plugin://" + addonID + "/?url=" + urllib.quote_plus(
                    oTitle.replace(" - ", " ")) + "&mode=playYTByTitle&addontype=YTM"
        else:
            url = oTitle
        musicVideos.append([int(rank), title, url, thumb])
    musicVideos = sorted(musicVideos, key=itemgetter(0))
    if type == "browse":
        for rank, title, url, thumb in musicVideos:
            addYTLink(title, url.replace(" - ", " "), "playYTByTitle", "", "", "", "", "", "")
        xbmcplugin.endOfDirectory(pluginhandle)
    else:
        if limit:
            musicVideos = musicVideos[:int(limit)]
        random.shuffle(musicVideos)
        for rank, title, url, thumb in musicVideos:
            listitem = xbmcgui.ListItem(title, thumbnailImage=thumb)
            playlist.add(url, listitem)
        xbmc.Player().play(playlist)


def listTimeMachine():
    for i in range(1, 210, 1):
        dt = datetime.date.today()
        while dt.weekday() != 0:
            dt -= datetime.timedelta(days=1)
        dt -= datetime.timedelta(weeks=i)
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        month = months[int(dt.strftime("%m")) - 1]
        addAutoPlayDir(dt.strftime("%b %d, %Y"),
                       urlMainHypem + "/popular/week:" + month + "-" + dt.strftime("%d-%Y") + "?ax=1&sortby=shuffle",
                       'listHypem', "", "", "browse")
    xbmcplugin.endOfDirectory(pluginhandle)


def itunesMain():
    content = cache("https://itunes.apple.com/" + iTunesRegion + "/genre/music/id34", 30)
    content = content[content.find('id="genre-nav"'):]
    content = content[:content.find('</div>')]
    match = re.compile('<li><a href="https://itunes.apple.com/.+?/genre/.+?/id(.+?)"(.+?)title=".+?">(.+?)<',
                       re.DOTALL).findall(content)
    title = "All Genres"
    if itunesShowSubGenres:
        title = '[B]' + title + '[/B]'
    addAutoPlayDir(title, "0", "listItunesVideos", "", "", "browse")
    for genreID, type, title in match:
        title = cleanTitle(title)
        if 'class="top-level-genre"' in type:
            if itunesShowSubGenres:
                title = '[B]' + title + '[/B]'
            addAutoPlayDir(title, genreID, "listItunesVideos", "", "", "browse")
        elif itunesShowSubGenres:
            title = '   ' + title
            addAutoPlayDir(title, genreID, "listItunesVideos", "", "", "browse")
    xbmcplugin.endOfDirectory(pluginhandle)


def listItunesVideos(type, genreID, limit):
    if type == "play":
        musicVideos = []
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
    url = "https://itunes.apple.com/" + iTunesRegion + "/rss/topsongs/limit=100"
    if genreID != "0":
        url += "/genre=" + genreID
    url += "/explicit=true/json"
    content = cache(url, 1)
    content = json.loads(content)
    pos = 1
    for item in content['feed']['entry']:
        artist = item['im:artist']['label'].encode('utf-8')
        videoTitle = item['im:name']['label'].encode('utf-8')
        if " (" in videoTitle:
            videoTitle = videoTitle[:videoTitle.rfind(" (")]
        title = cleanTitle(artist + " - " + videoTitle)
        songname = videoTitle
        try:
            thumb = item['im:image'][2]['label'].replace("170x170-75.jpg", "400x400-75.jpg")
        except:
            thumb = ""
        filtered = False
        for entry2 in blacklist:
            if entry2.strip().lower() and entry2.strip().lower() in title.lower():
                filtered = True
        if filtered:
            continue
        if type == "browse":
            addYTLink(title, title.replace(" - ", " "), "playYTByTitle", thumb, songname, artist, "", "", "")
            # addLink(title, title.replace(" - ", " "), "playYTByTitle", thumb)
        else:
            if xbox:
                url = "plugin://video/Youtube Music/?url=" + urllib.quote_plus(
                    title.replace(" - ", " ")) + "&mode=playYTByTitle&addontype=YTM"
            else:
                url = "plugin://" + addonID + "/?url=" + urllib.quote_plus(
                    title.replace(" - ", " ")) + "&mode=playYTByTitle&addontype=YTM"
            musicVideos.append([title, url, thumb])
            if limit and int(limit) == pos:
                break
            pos += 1
    if type == "browse":
        xbmcplugin.endOfDirectory(pluginhandle)
        if forceView:
            xbmc.executebuiltin('Container.SetViewMode(' + viewIDVideos + ')')
    else:
        random.shuffle(musicVideos)
        for title, url, thumb in musicVideos:
            listitem = xbmcgui.ListItem(title, thumbnailImage=thumb)
            playlist.add(url, listitem)
        xbmc.Player().play(playlist)


def spotifyMain():
    addYTDir(translation(30041),
             "http://api.tunigo.com/v3/space/toplists?region=" + spotifyRegion + "&page=0&per_page=50&platform=web",
             "listSpotifyPlaylists", "")
    addYTDir(translation(30042),
             "http://api.tunigo.com/v3/space/featured-playlists?region=" + spotifyRegion + "&page=0&per_page=50&dt=" + datetime.datetime.now().strftime(
                 "%Y-%m-%dT%H:%M").replace(":", "%3A") + "%3A00&platform=web", "listSpotifyPlaylists", "")
    addYTDir(translation(30006),
             "http://api.tunigo.com/v3/space/genres?region=" + spotifyRegion + "&per_page=1000&platform=web",
             "listSpotifyGenres", "")
    xbmcplugin.endOfDirectory(pluginhandle)


def listSpotifyGenres(url):
    content = cache(url, 30)
    content = json.loads(content)
    for item in content['items']:
        genreID = item['genre']['templateName']
        try:
            thumb = item['genre']['iconImageUrl']
        except:
            thumb = ""
        title = item['genre']['name'].encode('utf-8')
        if title.strip().lower() != "top lists":
            addYTDir(title,
                     "http://api.tunigo.com/v3/space/" + genreID + "?region=" + spotifyRegion + "&page=0&per_page=50&platform=web",
                     "listSpotifyPlaylists", thumb)
    xbmcplugin.endOfDirectory(pluginhandle)
    if forceView:
        xbmc.executebuiltin('Container.SetViewMode(' + viewIDGenres + ')')


def listSpotifyPlaylists(url):
    content = cache(url, 1)
    content = json.loads(content)
    for item in content['items']:
        uri = item['playlist']['uri'].encode('utf-8')
        try:
            thumb = "http://d3rt1990lpmkn.cloudfront.net/300/" + item['playlist']['image']
        except:
            thumb = ""
        title = item['playlist']['title'].encode('utf-8')
        description = item['playlist']['description'].encode('utf-8')
        addAutoPlayDir(title, uri, "listSpotifyVideos", thumb, description, "browse")
    match = re.compile('page=(.+?)&per_page=(.+?)&', re.DOTALL).findall(url)
    currentPage = int(match[0][0])
    perPage = int(match[0][1])
    nextPage = currentPage + 1
    if nextPage * perPage < content['totalItems']:
        addYTDir(translation(30001), url.replace("page=" + str(currentPage), "page=" + str(nextPage)),
                 "listSpotifyPlaylists", "")
    xbmcplugin.endOfDirectory(pluginhandle)
    if forceView:
        xbmc.executebuiltin('Container.SetViewMode(' + viewIDPlaylists + ')')


def listSpotifyVideos(type, url, limit):
    if type == "play":
        musicVideos = []
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
    content = cache("https://embed.spotify.com/?uri=" + url, 1)
    spl = content.split('music-paused item')
    pos = 1
    for i in range(1, len(spl), 1):
        entry = spl[i]
        match = re.compile('class="artist.+?>(.+?)<', re.DOTALL).findall(entry)
        artist = match[0]
        match = re.compile('class="track-title.+?>(.+?)<', re.DOTALL).findall(entry)
        videoTitle = match[0]
        videoTitle = videoTitle[videoTitle.find(".") + 1:].strip()
        if " - " in videoTitle:
            videoTitle = videoTitle[:videoTitle.rfind(" - ")]
        if " [" in videoTitle:
            videoTitle = videoTitle[:videoTitle.rfind(" [")]
        if ")" in videoTitle:
            videoTitle = videoTitle[:videoTitle.rfind(")")]
        if "," in artist:
            artist = artist.split(",")[0]
        songname = videoTitle
        title = cleanTitle(artist + " - " + videoTitle)
        match = re.compile('data-ca="(.+?)"', re.DOTALL).findall(entry)
        thumb = match[0]
        filtered = False
        for entry2 in blacklist:
            if entry2.strip().lower() and entry2.strip().lower() in title.lower():
                filtered = True
        if filtered:
            continue
        if type == "browse":
            addYTLink(title, title.replace(" - ", " "), "playYTByTitle", thumb, songname, artist, "", "", "")
        else:
            if xbox:
                url = "plugin://video/Youtube Music/?url=" + urllib.quote_plus(
                    title.replace(" - ", " ")) + "&mode=playYTByTitle&addontype=YTM"
            else:
                url = "plugin://" + addonID + "/?url=" + urllib.quote_plus(
                    title.replace(" - ", " ")) + "&mode=playYTByTitle&addontype=YTM"
            musicVideos.append([title, url, thumb])
            if limit and int(limit) == pos:
                break
            pos += 1
    if type == "browse":
        xbmcplugin.endOfDirectory(pluginhandle)
        if forceView:
            xbmc.executebuiltin('Container.SetViewMode(' + viewIDVideos + ')')
    else:
        random.shuffle(musicVideos)
        for title, url, thumb in musicVideos:
            listitem = xbmcgui.ListItem(title, thumbnailImage=thumb)
            playlist.add(url, listitem)
        xbmc.Player().play(playlist)


GLTZ_URLS = ["http://www.glgltz.co.il/Shared/Ajax/GetTophitsByCategory.aspx?FolderId=1183&amp;lang=he",
             "http://www.glgltz.co.il/Shared/Ajax/GetTophitsByCategory.aspx?FolderId=1182&amp;lang=he",
             "http://www.glgltz.co.il/1215-he/Galgalatz.aspx",
             "http://www.glgltz.co.il/1213-he/Galgalatz.aspx",
             "http://www.glgltz.co.il/1236-he/Galgalatz.aspx",
             "http://www.glgltz.co.il/Shared/Ajax/BroadcastMonitor.aspx"]


def GalgalatzMain():
    addAutoPlayDirGlz("המצעד הבינלאומי",
                      "0",
                      "listGalgalatzCharts", "http://www.glgltz.co.il/SIP_STORAGE/files/7/1647.jpg", "", "browse")
    addAutoPlayDirGlz("המצעד הישראלי",
                      "1",
                      "listGalgalatzCharts", "http://www.glgltz.co.il/SIP_STORAGE/files/6/1646.jpg", "", "browse")
    addAutoPlayDirGlz("פלייליסט בינלאומי", "2", "listGalgalatzPlaylist",
                      "http://3.bp.blogspot.com/_bhUS7ZA74pc/S7PPvRLkueI/AAAAAAAABzw/lYSKxhj6beE/s1600/world-music.jpg",
                      "", "browse")
    addAutoPlayDirGlz("פלייליסט ישראלי", "3", "listGalgalatzPlaylist",
                      "http://3.bp.blogspot.com/_bhUS7ZA74pc/S7PPvRLkueI/AAAAAAAABzw/lYSKxhj6beE/s1600/world-music.jpg",
                      "", "browse")
    addAutoPlayDirGlz("פלייליסט מעורב", "", "listGalgalatzPlaylistMix",
                      "http://3.bp.blogspot.com/_bhUS7ZA74pc/S7PPvRLkueI/AAAAAAAABzw/lYSKxhj6beE/s1600/world-music.jpg",
                      "", "browse")
    addAutoPlayDirGlz("מצעד שנות ה-80", "4", "listGalgalatzDecadeChart80",
                      "http://www.bawa.biz/bristol-entertainment-sports/sites/default/files/events/ilovethe80s.jpg", "",
                      "browse")
    addAutoPlayDirGlz("מצעד שנות ה-90", "4", "listGalgalatzDecadeChart90",
                      "https://origin.ih.constantcontact.com/fs145/1102250365124/img/615.jpg", "", "browse")
    addAutoPlayDirGlz("מצעד שנות ה-2000", "4",
                      "listGalgalatzDecadeChart00",
                      "http://8tracks.imgix.net/i/000/570/047/Ultimate2000s-4208.jpg?q=65&sharp=15&vib=10&fm=jpg&fit=crop&w=521&h=521",
                      "", "browse")
    addAutoPlayDirGlz('גלגל"צ live', "5", "PlayGalgalatzRadio",
                      "http://www.glgltz.co.il/Sip_Storage/FILES/9/2099.jpg", "", "browse")
    xbmcplugin.endOfDirectory(pluginhandle)


def listGalgalatzDecadeChart80(type, url, limit):
    url = GLTZ_URLS[int(url)]
    if type == "play":
        musicVideos = []
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
    idx1 = []
    idx2 = []
    idx3 = []
    idx4 = []
    pos = 1
    content = cache(url, 1)
    for it in re.finditer('</h3>', str(content)):
        idx1.append(it.start())
    for it in re.finditer('<ul class="FileLinksList">', str(content)):
        idx2.append(it.start())
    # 80's idx1[1]:idx2[0]
    cut_file = str(content)[idx1[1]:idx2[0]]
    cut_file = cut_file.replace('dir="ltr">', '<br />')
    # for 80's
    for it in re.finditer('<br />', cut_file):
        idx3.append(it.start())
    # for 80's
    cut_file = cut_file[idx3[0]:idx3[len(idx3) - 1]]
    cut_file = cut_file.replace('</p>', '<FINISH!!!>')
    for it in re.finditer('<FINISH!!!>', cut_file):
        idx4.append(it.start())
    clean_file = cut_file[:idx4[len(idx4) - 1]]
    clean_file = clean_file.replace('<FINISH!!!>', '<br />')
    clean_file = clean_file.replace('\n', '')
    clean_file = clean_file.replace('\r', '')
    clean_file = clean_file.replace('<p style="text-align: left;"', '<br />')
    clean_file = clean_file.replace('<br /> <br />', '<br />')
    clean_file = clean_file.replace('<br /><br />', '<br />')
    tokens = clean_file.split("<br />")
    new_t = tokens[1:len(tokens):2]
    for title in new_t:
        title = title[title.find(".") + 2:].replace('\\', '')
        title = title.replace('"', '')
        if type == "browse":
            items = title.split("-")
            artist = items[0]
            songname = items[1]
            addYTLink(title, title.replace(" - ", " "), "playYTByTitle", "", songname, artist, "", "", "")
        else:
            if xbox:
                url = "plugin://video/Youtube Music/?url=" + urllib.quote_plus(
                    title.replace(" - ", " ")) + "&mode=playYTByTitle&addontype=YTM"
            else:
                url = "plugin://" + addonID + "/?url=" + urllib.quote_plus(
                    title.replace(" - ", " ")) + "&mode=playYTByTitle&addontype=YTM"
            musicVideos.append([title, url, ""])
            if limit and int(limit) == pos:
                break
            pos += 1
    if type == "browse":
        xbmcplugin.endOfDirectory(pluginhandle)
    else:
        random.shuffle(musicVideos)
        for title, url, thumb in musicVideos:
            listitem = xbmcgui.ListItem(title, thumbnailImage=thumb)
            playlist.add(url, listitem)
        xbmc.Player().play(playlist)


def listGalgalatzDecadeChart90(type, url, limit):
    url = GLTZ_URLS[int(url)]
    if type == "play":
        musicVideos = []
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
    idx1 = []
    idx2 = []
    idx3 = []
    idx4 = []
    pos = 1
    content = cache(url, 1)
    for it in re.finditer('</h3>', str(content)):
        idx1.append(it.start())
    for it in re.finditer('<ul class="FileLinksList">', str(content)):
        idx2.append(it.start())
    cut_file = str(content)[idx1[2]:idx2[1]]
    cut_file = cut_file.replace('dir="ltr">', '<br />')
    # for 90's
    start_idx = cut_file.index('<p>')
    end_idx = cut_file.index('</p>')
    # for 90's
    cut_file = cut_file[start_idx:end_idx]
    clean_file = cut_file.replace('<p>', '<br />')
    tokens = clean_file.split("<br />")
    tokens = filter(lambda x: x != '', tokens)
    new_t = tokens[0:len(tokens):2]
    for title in new_t:
        title = title[title.find(".") + 1:].replace('\\', '')
        title = title.replace('"', '')
        if type == "browse":
            items = title.split("-")
            artist = items[0]
            songname = items[1]
            addYTLink(title, title.replace(" - ", " "), "playYTByTitle", "", songname, artist, "", "", "")
            # addLink(title, title.replace(" - ", " "), "playYTByTitle", "")
        else:
            if xbox:
                url = "plugin://video/Youtube Music/?url=" + urllib.quote_plus(
                    title.replace(" - ", " ")) + "&mode=playYTByTitle&addontype=YTM"
            else:
                url = "plugin://" + addonID + "/?url=" + urllib.quote_plus(
                    title.replace(" - ", " ")) + "&mode=playYTByTitle&addontype=YTM"
            musicVideos.append([title, url, ""])
            if limit and int(limit) == pos:
                break
            pos += 1
    if type == "browse":
        xbmcplugin.endOfDirectory(pluginhandle)
    else:
        random.shuffle(musicVideos)
        for title, url, thumb in musicVideos:
            listitem = xbmcgui.ListItem(title, thumbnailImage=thumb)
            playlist.add(url, listitem)
        xbmc.Player().play(playlist)


def listGalgalatzDecadeChart00(type, url, limit):
    url = GLTZ_URLS[int(url)]
    if type == "play":
        musicVideos = []
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
    idx1 = []
    idx2 = []
    idx3 = []
    idx4 = []
    pos = 1
    content = cache(url, 1)
    for it in re.finditer('</h3>', str(content)):
        idx1.append(it.start())
    for it in re.finditer('<ul class="FileLinksList">', str(content)):
        idx2.append(it.start())
    cut_file = str(content)[idx1[3]:idx2[2]]
    cut_file = cut_file.replace('dir="ltr">', '<br />')
    start_idx = cut_file.index('<p>')
    end_idx = cut_file.index('</p>')
    cut_file = cut_file[start_idx:end_idx]
    clean_file = cut_file.replace('<p>', '<br />')
    tokens = clean_file.split("<br />")
    tokens = filter(lambda x: x != '', tokens)
    new_t = tokens[0:len(tokens):2]
    for title in new_t:
        title = title[title.find(".") + 1:].replace('\\', '')
        title = title.replace('"', '')
        if type == "browse":
            items = title.split("-")
            artist = items[0]
            songname = items[1]
            addYTLink(title, title.replace(" - ", " "), "playYTByTitle", "", songname, artist, "", "", "")
            # addLink(title, title.replace(" - ", " "), "playYTByTitle", "")
        else:
            if xbox:
                url = "plugin://video/Youtube Music/?url=" + urllib.quote_plus(
                    title.replace(" - ", " ")) + "&mode=playYTByTitle&addontype=YTM"
            else:
                url = "plugin://" + addonID + "/?url=" + urllib.quote_plus(
                    title.replace(" - ", " ")) + "&mode=playYTByTitle&addontype=YTM"
            musicVideos.append([title, url, ""])
            if limit and int(limit) == pos:
                break
            pos += 1
    if type == "browse":
        xbmcplugin.endOfDirectory(pluginhandle)
    else:
        random.shuffle(musicVideos)
        for title, url, thumb in musicVideos:
            listitem = xbmcgui.ListItem(title, thumbnailImage=thumb)
            playlist.add(url, listitem)
        xbmc.Player().play(playlist)

class glz_radio(Thread):
    def __init__(self, url,  curr_title, playlist):
        self.url = url
        self.curr_title = curr_title
        self.playlist = playlist
        Thread.__init__(self)

    def run(self):
        self.play(self.url, self.curr_title, self.playlist)

    def play(self, url,  curr_title, playlist):
        mix_playlist = listGalgalatzPlaylist("add", "3", "")
        mix_playlist += listGalgalatzPlaylist("add", "2", "")
        random.shuffle(mix_playlist)
        main_url = url
        old_title = curr_title
        i = 0
        elapsed_time = 0
        end_thread = False
        list_index = 0
        while not end_thread:
            #handle new title
            if (curr_title != old_title):
                for word in glz_black_list:
                    if word in curr_title:
                        old_title = curr_title
                        xbmc.sleep(5000)
                        continue
                if xbox:
                    url = "plugin://video/Youtube Music/?url=" + urllib.quote_plus(curr_title) + "&mode=playYTByTitle&addontype=YTM"
                else:
                    url = "plugin://" + addonID + "/?url=" + urllib.quote_plus(curr_title) + "&mode=playYTByTitle&addontype=YTM"
                listitem = xbmcgui.ListItem(curr_title, "")
                playlist.add(url, listitem,list_index)
                list_index+=1
                #workaround to overcome bug issue
                if (list_index == 1):
                    playlist.add(url, listitem,list_index)
                    list_index+=1
                old_title = curr_title
                xbmc.sleep(5000)
            else:
                #some debug info
                try:
                    elapsed_time = int(xbmc.Player().getTime())
                    clip_time =xbmc.Player().getTotalTime()
                    i = 0
                except:
                    xbmc.sleep(5000)
                    i+=1
                    #if not playing for 15 seconds close the thread
                    if (i == 3 ):
                        end_thread = True

                #handle commercial and shit
                if clip_time < 140 or clip_time > 600:
                    if playlist.size() != playlist.getposition():
                        xbmc.Player().playnext()
                    else:
                        shuffle_id = random.randint(0, len(mix_playlist) - 1)
                        curr_title = mix_playlist[shuffle_id][0]
                        listitem = xbmcgui.ListItem(curr_title, "")
                        playlist.add(mix_playlist[shuffle_id][1], listitem, list_index)
                        list_index+=1
                        #workaround to overcome bug issue
                        if (list_index == 1):
                            playlist.add(mix_playlist[shuffle_id][1], listitem, list_index)
                            list_index+=1
                        old_title = curr_title
                        xbmc.Player().playnext()
                    continue

                #handle file is alsmost done playing but nothing new come in
                if (playlist.size() == playlist.getposition() and int(clip_time) > 0 and elapsed_time >= int(clip_time) - 10):
                    shuffle_id = random.randint(0, len(mix_playlist) - 1)
                    curr_title = mix_playlist[shuffle_id][0]
                    listitem = xbmcgui.ListItem(curr_title, "")
                    playlist.add(mix_playlist[shuffle_id][1], listitem, list_index)
                    list_index+=1
                    #workaround to overcome bug issue
                    if (list_index == 1):
                        playlist.add(mix_playlist[shuffle_id][1], listitem, list_index)
                        list_index+=1
                    old_title = curr_title
                else:
                    content = cache(main_url, 0)
                    curr_title = str(content)
                    curr_title = curr_title.replace("\\", " ").replace(",", " ").replace("_", " ")
                    curr_title = ' '.join(curr_title.split())
                xbmc.sleep(5000)

        print "thread done!"
        playlist.clear()

def PlayGalgalatzRadio(type, url, limit):
    url = GLTZ_URLS[int(url)]
    playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    playlist.clear()
    main_url = url
    content = cache(url, 0)
    title = str(content)
    title = title.replace("\\", " ").replace(",", " ").replace("_", " ")
    title = ' '.join(title.split())
    RadioThread = glz_radio(main_url, title, playlist)
    if xbox:
        url = "plugin://video/Youtube Music/?url=" + urllib.quote_plus(title) + "&mode=playYTByTitle&addontype=YTM"
    else:
        url = "plugin://" + addonID + "/?url=" + urllib.quote_plus(title) + "&mode=playYTByTitle&addontype=YTM"
    listitem = xbmcgui.ListItem(title, "")
    dialog = xbmcgui.Dialog()
    i = dialog.yesno(translation(40090),"")
    if i == 0:
        GalgalatzMain()
    else:
        playlist.add(url, listitem)
        xbmc.Player().play(playlist)
        RadioThread.start()



def listGalgalatzPlaylist(type, url, limit):
    url = GLTZ_URLS[int(url)]
    if type == "play" or type == "add":
        musicVideos = []
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
    content = cache(url, 1)
    match = re.compile('<td><span>(.+?)</span>', re.DOTALL).findall(content)
    pos = 1
    artist_list = match[0:len(match):2]
    song_list = match[1:len(match):2]
    for artist, song in zip(artist_list, song_list):
        title = artist + " - " + song
        if type == "browse":
            addYTLink(title, title.replace(" - ", " "), "playYTByTitle", "", song, artist, "", "", "")
        else:
            if xbox:
                url = "plugin://video/Youtube Music/?url=" + urllib.quote_plus(
                    title.replace(" - ", " ")) + "&mode=playYTByTitle&addontype=YTM"
            else:
                url = "plugin://" + addonID + "/?url=" + urllib.quote_plus(
                    title.replace(" - ", " ")) + "&mode=playYTByTitle&addontype=YTM"
            musicVideos.append([title, url, ""])
            if limit and int(limit) == pos:
                break
            pos += 1
    if type == "browse":
        xbmcplugin.endOfDirectory(pluginhandle)
    elif type == "add":
        return musicVideos
    else:
        random.shuffle(musicVideos)
        for title, url, thumb in musicVideos:
            listitem = xbmcgui.ListItem(title, thumbnailImage=thumb)
            playlist.add(url, listitem)
        xbmc.Player().play(playlist)


def listGalgalatzPlaylistMix(type, url, limit):
    musicVideos = listGalgalatzPlaylist("add", "3", "")
    musicVideos += listGalgalatzPlaylist("add", "2", "")
    if type == "play" or type == "add":
        random.shuffle(musicVideos)
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
    for title, url, thumb in musicVideos:
        if type == "browse":
            items = title.split("-")
            artist = items[0]
            songname = items[1]
            addYTLink(title, title.replace(" - ", " "), "playYTByTitle", "", songname, artist, "", "", "")
            # addLink(title, title.replace(" - ", " "), "playYTByTitle", "")
        else:
            listitem = xbmcgui.ListItem(title, thumbnailImage=thumb)
            playlist.add(url, listitem)
    if type == "browse":
        xbmcplugin.endOfDirectory(pluginhandle)
    else:
        xbmc.Player().play(playlist)


def listGalgalatzCharts(type, url, limit):
    url = GLTZ_URLS[int(url)]
    if type == "play":
        musicVideos = []
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
    content = cache(url, 1)
    pos = 1
    song_list = re.compile('<h4>(.+?)</h4>', re.DOTALL).findall(content)
    artist_list = re.compile('spanPerformer">(.+?)</span>', re.DOTALL).findall(content)
    for artist, song in zip(artist_list, song_list):
        title = artist + " - " + song
        if type == "browse":
            addYTLink(title, title.replace(" - ", " "), "playYTByTitle", "", song, artist, "", "", "")
        else:
            if xbox:
                url = "plugin://video/Youtube Music/?url=" + urllib.quote_plus(
                    title.replace(" - ", " ")) + "&mode=playYTByTitle&addontype=YTM"
            else:
                url = "plugin://" + addonID + "/?url=" + urllib.quote_plus(
                    title.replace(" - ", " ")) + "&mode=playYTByTitle&addontype=YTM"
            musicVideos.append([title, url, ""])
            if limit and int(limit) == pos:
                break
            pos += 1
    if type == "browse":
        xbmcplugin.endOfDirectory(pluginhandle)
    else:
        random.shuffle(musicVideos)
        for title, url, thumb in musicVideos:
            listitem = xbmcgui.ListItem(title, thumbnailImage=thumb)
            playlist.add(url, listitem)
        xbmc.Player().play(playlist)


def OneFmMain():
    addAutoPlayDir(translation(400100), "http://www.onefmonline.com", "listOneFmPlaylist",
                   "http://warnerboutique.com/wp-content/uploads/music-dance-hd-wallpaper-50267-hd-wallpapers-background-750x498.jpg",
                   "", "browse")
    addAutoPlayDir(translation(400101), "http://www.onefmonline.com/common/Radio.aspx", "listOneFmLastPlayed",
                   "http://www.desktopaper.com/wp-content/uploads/unusual-abstract-wallpaper-dance-digital-art-music.jpg",
                   "", "browse")
    addAutoPlayDir(translation(400102), "http://www.onefmonline.com/common/Radio.aspx", "PlayOneFmRadio",
                   "http://cdn.superbwallpapers.com/wallpapers/music/microphone-19151-1920x1080.jpg", "", "browse")
    xbmcplugin.endOfDirectory(pluginhandle)


def listOneFmPlaylist(type, url, limit):
    if type == "play":
        musicVideos = []
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
    content = opener.open(url).read()
    content = content[content.find('<div id="listsBg"'):]
    content = content[:content.find('class="listContent ">')]
    match = re.compile("<li title='(.+?)'>", re.DOTALL).findall(content)
    pos = 1
    for title in match:
        if type == "browse":
            artist = title.split(" - ")[0]
            songname = title.split(" - ")[1]
            addYTLink(title, title.replace(" - ", " "), "playYTByTitle", "", songname, artist, "", "", "")
            # addLink(title, title.replace(" - ", " "), "playYTByTitle", "")
        else:
            if xbox:
                url = "plugin://video/Youtube Music/?url=" + urllib.quote_plus(
                    title.replace(" - ", " ")) + "&mode=playYTByTitle&addontype=YTM"
            else:
                url = "plugin://" + addonID + "/?url=" + urllib.quote_plus(
                    title.replace(" - ", " ")) + "&mode=playYTByTitle&addontype=YTM"
            musicVideos.append([title, url, ""])
            if limit and int(limit) == pos:
                break
            pos += 1
    if type == "browse":
        xbmcplugin.endOfDirectory(pluginhandle)
    else:
        random.shuffle(musicVideos)
        for title, url, thumb in musicVideos:
            listitem = xbmcgui.ListItem(title, thumbnailImage=thumb)
            playlist.add(url, listitem)
        xbmc.Player().play(playlist)


def listOneFmLastPlayed(type, url, limit):
    if type == "play":
        musicVideos = []
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
    content = opener.open(url).read()
    content = content[content.find('<h3>Last Played</h3>'):]
    content = content[:content.find('</ul>')]
    match = re.compile('<li title="(.+?)">', re.DOTALL).findall(content)
    pos = 1
    for title in match:
        if type == "browse":
            artist = title.split(" - ")[0]
            songname = title.split(" - ")[1]
            addYTLink(title, title.replace(" - ", " "), "playYTByTitle", "", songname, artist, "", "", "")
            # addLink(title, title.replace(" - ", " "), "playYTByTitle", "")
        else:
            if xbox:
                url = "plugin://video/Youtube Music/?url=" + urllib.quote_plus(
                    title.replace(" - ", " ")) + "&mode=playYTByTitle&addontype=YTM"
            else:
                url = "plugin://" + addonID + "/?url=" + urllib.quote_plus(
                    title.replace(" - ", " ")) + "&mode=playYTByTitle&addontype=YTM"
            musicVideos.append([title, url, ""])
            if limit and int(limit) == pos:
                break
            pos += 1
    if type == "browse":
        xbmcplugin.endOfDirectory(pluginhandle)
    else:
        random.shuffle(musicVideos)
        for title, url, thumb in musicVideos:
            listitem = xbmcgui.ListItem(title, thumbnailImage=thumb)
            playlist.add(url, listitem)
        xbmc.Player().play(playlist)

class onefm_radio(Thread):
    def __init__(self, url,  curr_title, playlist):
        self.url = url
        self.curr_title = curr_title
        self.playlist = playlist
        Thread.__init__(self)

    def run(self):
        self.play(self.url, self.curr_title, self.playlist)

    def play(self, url,  curr_title, playlist):
        main_url = url
        old_title = curr_title
        i = 0
        elapsed_time = 0
        end_thread = False
        list_index = 0
        while not end_thread:
            #handle new title
            if (curr_title != old_title):
                #check for skip items
                if "1Beep1" in curr_title:
                    old_title = curr_title
                    continue
                if xbox:
                    url = "plugin://video/Youtube Music/?url=" + urllib.quote_plus(curr_title) + "&mode=playYTByTitle&addontype=YTM"
                else:
                    url = "plugin://" + addonID + "/?url=" + urllib.quote_plus(curr_title) + "&mode=playYTByTitle&addontype=YTM"
                listitem = xbmcgui.ListItem(curr_title, "")
                playlist.add(url, listitem,list_index)
                list_index+=1
                #workaround to overcome bug issue
                if (list_index == 1):
                    playlist.add(url, listitem,list_index)
                    list_index+=1
                old_title = curr_title
                xbmc.sleep(5000)
            else:
                #some debug info
                try:
                    elapsed_time = int(xbmc.Player().getTime())
                    clip_time =xbmc.Player().getTotalTime()
                    i = 0
                except:
                    xbmc.sleep(5000)
                    i+=1
                    #if not playing for 15 seconds close the thread
                    if (i == 3 ):
                        end_thread = True

                #handle file is alsmost done playing but nothing new come in
                if (playlist.size() == playlist.getposition() and int(clip_time) > 0 and elapsed_time >= int(clip_time) - 10):
                    pass
                else:
                    content = opener.open(main_url).read()
                    content = content[content.find('<h3>Now Playing</h3>'):]
                    content = content[:content.find('</h4>')]
                    match = re.compile('<h4 title="(.+?)" class="recentSong">', re.DOTALL).findall(content)
                    curr_title = match[0]
                xbmc.sleep(5000)

        print "thread done!"
        playlist.clear()


def PlayOneFmRadio(type, url, limit):
    playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    playlist.clear()
    main_url = url
    content = opener.open(url).read()
    content = content[content.find('<h3>Now Playing</h3>'):]
    content = content[:content.find('</h4>')]
    match = re.compile('<h4 title="(.+?)" class="recentSong">', re.DOTALL).findall(content)
    title = match[0]
    RadioThread = onefm_radio(main_url, title, playlist)
    if xbox:
        url = "plugin://video/Youtube Music/?url=" + urllib.quote_plus(
            title.replace(" - ", " ")) + "&mode=playYTByTitle&addontype=YTM"
    else:
        url = "plugin://" + addonID + "/?url=" + urllib.quote_plus(title.replace(" - ", " ")) + "&mode=playYTByTitle&addontype=YTM"
    listitem = xbmcgui.ListItem(title, "")
    dialog = xbmcgui.Dialog()
    i = dialog.yesno(translation(40090),"")
    if i == 0:
        OneFmMain()
    else:
        playlist.add(url, listitem)
        xbmc.Player().play(playlist)
        RadioThread.start()


class fm99_radio_thread(Thread):
    def __init__(self, url,  curr_title, playlist):
        self.url = url
        self.curr_title = curr_title
        self.playlist = playlist
        Thread.__init__(self)

    def run(self):
        self.play(self.url, self.curr_title, self.playlist)

    def play(self, url,  curr_title, playlist):
        main_url = url
        old_title = curr_title
        i = 0
        elapsed_time = 0
        end_thread = False
        list_index = 0
        while not end_thread:
            #handle new title
            if (curr_title != old_title):
                if xbox:
                    url = "plugin://video/Youtube Music/?url=" + urllib.quote_plus(curr_title) + "&mode=playYTByTitle&addontype=YTM"
                else:
                    url = "plugin://" + addonID + "/?url=" + urllib.quote_plus(curr_title) + "&mode=playYTByTitle&addontype=YTM"
                listitem = xbmcgui.ListItem(curr_title, "")
                playlist.add(url, listitem,list_index)
                list_index+=1
                #workaround to overcome bug issue
                if (list_index == 1):
                    playlist.add(url, listitem,list_index)
                    list_index+=1
                old_title = curr_title
                xbmc.sleep(1000)
            else:
                #some debug info
                try:
                    elapsed_time = int(xbmc.Player().getTime())
                    clip_time =xbmc.Player().getTotalTime()
                    i = 0
                except:
                    xbmc.sleep(1000)
                    i+=1
                    #if not playing for 15 seconds close the thread
                    if (i == 3 ):
                        end_thread = True
                else:
                    content = open_url(main_url)
                    song_dict = json.loads(content)
                    artist = song_dict["Artist"].encode('utf-8')
                    try:
                        curr_title = song_dict["Song"].encode('utf-8') + " - " +artist[:artist.index("Feat.")]
                    except:
                        curr_title = song_dict["Song"].encode('utf-8') + " - " +artist
                xbmc.sleep(1000)
        print "thread done!"
        playlist.clear()


def fm99_radio():
    playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    playlist.clear()
    main_url = "http://radiometer.co.il/eco99/feed.php?mode=player"
    content = open_url(main_url)
    song_dict = json.loads(content)
    artist = song_dict["Artist"].encode('utf-8')
    try:
        title = song_dict["Song"].encode('utf-8') + " - " +artist[:artist.index("Feat.")]
    except:
        title = song_dict["Song"].encode('utf-8') + " - " +artist
    RadioThread = fm99_radio_thread(main_url,title , playlist)
    if xbox:
        url = "plugin://video/Youtube Music/?url=" + urllib.quote_plus(
            title.replace(" - ", " ")) + "&mode=playYTByTitle&addontype=YTM"
    else:
        url = "plugin://" + addonID + "/?url=" + urllib.quote_plus(title.replace(" - ", " ")) + "&mode=playYTByTitle&addontype=YTM"
    listitem = xbmcgui.ListItem(title, "")
    dialog = xbmcgui.Dialog()
    i = dialog.yesno(translation(40090),"")
    if i == 0:
        fm99_main()
    else:
        playlist.add(url, listitem)
        xbmc.Player().play(playlist)
        RadioThread.start()

def fm99_top_40_playlist(type, limit):
    if type == "play":
        musicVideos = []
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
    pos = 1
    content = open_url('http://eco99fm.maariv.co.il/include/jw_playlist.aspx?Cid=1&Pid=0&Chart=1')
    tree = ET.fromstring(content)
    for channel in tree:
        for item in channel.findall('item'):
            artist = item.find('title').text
            songname = item.find('description').text
            title = artist.encode('utf-8') + " - " + songname.encode('utf-8')
            if type == "browse":
                addYTLink(title, title.replace(" - ", " "), "playYTByTitle","", songname.encode('utf-8'), artist.encode('utf-8'),"", "", "")
            else:
                if xbox:
                    url = "plugin://video/Youtube Music/?url=" + urllib.quote_plus(
                        title.replace(" - ", " ")) + "&mode=playYTByTitle&addontype=YTM"
                else:
                    url = "plugin://" + addonID + "/?url=" + urllib.quote_plus(
                        title.replace(" - ", " ")) + "&mode=playYTByTitle&addontype=YTM"
                musicVideos.append([title, url, ""])
                if limit and int(limit) == pos:
                    break
                pos += 1
    if type == "browse":
        xbmcplugin.endOfDirectory(pluginhandle)
    else:
        random.shuffle(musicVideos)
        for title, url, thumb in musicVideos:
            listitem = xbmcgui.ListItem(title, thumbnailImage=thumb)
            playlist.add(url, listitem)
        xbmc.Player().play(playlist)


def play_mp3_file(url,name,iconimage):
    liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
    liz.setInfo('music', {'Title':name, 'Artist':""})
    liz.setProperty('mimetype','audio/mpeg')
    liz.setProperty('fanart_image', fanart)
    liz.setProperty('IsPlayable',   'true')
    pl=xbmc.PlayList(xbmc.PLAYLIST_MUSIC)
    pl.clear()
    pl.add(url,liz)
    pl.add(url,liz)
    xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER ).play(pl)

def addMP3Link(set_name, url, mode, iconimage, pl_name):
    liz = xbmcgui.ListItem(set_name, iconImage="DefaultAudio.png", thumbnailImage=iconimage)
    liz.setInfo('music', {'Title':set_name, 'Artist':pl_name})
    liz.setProperty('mimetype','audio/mpeg')
    liz.setProperty('fanart_image', fanart)
    liz.setProperty('IsPlayable',   'true')
    u = sys.argv[0] + "?url=" + urllib.quote(url) + "&mode=" + str(mode)+"&name="+pl_name+"&iconimage="+urllib.quote(iconimage)+"=&addontype=YTM"
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=False)
    return ok

def fm99_sub_dynamic_slider_sets(url):
    content = open_url(RADIO99_URL+"/slider/?Tid="+url)
    sets_data = re.compile('<div class="playSlider"\s*><a href="(.+?)".+?data-src="(.+?)".+?class="SliderText".+?>(.+?)<.+?class="slider_date_txt" id=.+?>(.+?)<', re.DOTALL).findall(content)
    for url, img, title,desc in sets_data:
        content = open_url(RADIO99_URL+urllib.quote(url))
        mp3_url = re.compile('id="FileUrl" name="FileUrl" value="(.+?)"/>', re.DOTALL).findall(content)
        addMP3Link(title, mp3_url[0].replace(" ","%20") , 'play_mp3_file', img, desc)
    if forceView:
        xbmc.executebuiltin('Container.SetViewMode(' + viewIDPlaylists + ')')

def fm99_sub_dynamic_playlists(url):
    content = open_url(RADIO99_URL+"/music_channels/")
    try:
        content = content[content.index('<div id="innerMainTag_'+str(int(url))+'"'):content.index('<div id="innerMainTag_'+str(int(url)+1)+'"')]
    except:
        content = content[content.index('<div id="innerMainTag_'+str(int(url))+'"'):]
    main_data = re.compile('<a href="#InnerTag=(.+?)".+?<image src="(.+?)".+?<td class="MainTag_Name".+?>(.+?)<', re.DOTALL).findall(content)
    for url, img, title in main_data:
        addYTDir(title , url , 'fm99_sub_dynamic_slider_sets', img.replace(" ","%20"), '')
    if forceView:
        xbmc.executebuiltin('Container.SetViewMode(' + viewIDPlaylists + ')')

def fm99_dynamic_playlists():
    content = open_url(RADIO99_URL+"/music_channels/")
    main_data = re.compile('<a href="#MainTag_Id=(.+?)".+?<image src="(.+?)".+?<td class="MainTag_Name".+?>(.+?)<', re.DOTALL).findall(content)
    for url,img, title in main_data:
        addYTDir(title , url , 'fm99_sub_dynamic_playlists', img, '')
    if forceView:
        xbmc.executebuiltin('Container.SetViewMode(' + viewIDPlaylists + ')')

def fm99_sub_playlists(url):
    print RADIO99_URL+url
    content = open_url(RADIO99_URL+url)
    content = content[content.index('id="musicChannels_sets"'):]
    sets_data = re.compile('<a href="(.+?)"\s*style=.+?<div style="BACKGROUND-IMAGE:\s*url\(\'(.+?)\'\).+?<span class=.+?>(.+?)<\/span><\/td>', re.DOTALL).findall(content)
    for set_url, set_img, set_title in sets_data:
        content = open_url(RADIO99_URL+urllib.quote(set_url))
        mp3_url = re.compile('id="FileUrl" name="FileUrl" value="(.+?)"/>', re.DOTALL).findall(content)
        set_desc = re.compile('<meta property="og:description" content="(.+?)">', re.DOTALL).findall(content)
        addMP3Link(set_title, mp3_url[0].replace(" ","%20") , 'play_mp3_file', set_img.replace(" ","%20"), set_desc[0])
        print mp3_url[0].replace(" ","%20")
    if forceView:
        xbmc.executebuiltin('Container.SetViewMode(' + viewIDPlaylists + ')')

def fm99_main_playlists():
    addYTDir("איפה תפסנו אותך?", "url" , 'fm99_dynamic_playlists', "", '')
    content = open_url(RADIO99_URL+"/music_channels/")
    content = content[content.index('id="musicChannels"'):]
    match = re.compile('<a href="(.+?)".+?<div style="BACKGROUND-IMAGE:\s*url\(\'(.+?)\'\).+?<p class="SliderText" dir="rtl">(.+?)</p>.+?<p class="slider_date_txt" dir="rtl">(.+?)</p>', re.DOTALL).findall(content)
    for url, img, title, sub_title in match:
        addYTDir(title + " - " + sub_title, url , 'fm99_sub_playlists', img.replace(" ","%20"), '')
    if forceView:
        xbmc.executebuiltin('Container.SetViewMode(' + viewIDPlaylists + ')')

def fm99_main():
    addYTDir("רשימות השמעה", 'url', 'fm99_main_playlists', '', '')
    addAutoPlayDir("40 הגדולים", 'url', 'fm99_top_40_playlist', '', '', "browse")
    addYTDir("רדיו חי", '2', 'fm99_radio', '', '')



def DisiMain():
    addAutoPlayDir("פלייליסט", "http://www.disi.co.il", "listDisiPlaylist", "", "", "browse")
    addAutoPlayDir("מצעד", "http://www.disi.co.il/best.php", "listDisiChart", "", "", "browse")
    xbmcplugin.endOfDirectory(pluginhandle)


def listDisiPlaylist(type, url, limit):
    if type == "play":
        musicVideos = []
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
    content = cache(url, 1)
    pos = 1
    artist_list = re.compile(" artist: '(.+?)'", re.DOTALL).findall(content)
    song_list = re.compile(" song: '(.+?)'", re.DOTALL).findall(content)
    poster_list = re.compile(" pic: '(.+?)'", re.DOTALL).findall(content)
    for artist, song, poster in zip(artist_list, song_list, poster_list):
        title = artist + " - " + song
        if type == "browse":
            addYTLink(title, title.replace(" - ", " "), "playYTByTitle", "http://www.disi.co.il" + poster, song, artist,
                      "", "", "")
        else:
            if xbox:
                url = "plugin://video/Youtube Music/?url=" + urllib.quote_plus(
                    title.replace(" - ", " ")) + "&mode=playYTByTitle&addontype=YTM"
            else:
                url = "plugin://" + addonID + "/?url=" + urllib.quote_plus(
                    title.replace(" - ", " ")) + "&mode=playYTByTitle&addontype=YTM"
            musicVideos.append([title, url, poster])
            if limit and int(limit) == pos:
                break
            pos += 1
    if type == "browse":
        if forceView:
            xbmc.executebuiltin('Container.SetViewMode(' + viewIDPlaylists + ')')
        xbmcplugin.endOfDirectory(pluginhandle)
    else:
        random.shuffle(musicVideos)
        for title, url, thumb in musicVideos:
            listitem = xbmcgui.ListItem(title, thumbnailImage=thumb)
            playlist.add(url, listitem)
        xbmc.Player().play(playlist)



def listDisiChart(type, url, limit):
    if type == "play":
        musicVideos = []
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
    content = cache(url, 1)
    pos = 1
    artist_list = re.compile('artist:"(.+?)"', re.DOTALL).findall(content)
    song_list = re.compile('song:"(.+?)"', re.DOTALL).findall(content)
    poster_list = re.compile('poster: "(.+?)"', re.DOTALL).findall(content)
    for artist, song, poster in zip(artist_list, song_list, poster_list):
        title = artist + " - " + song
        if type == "browse":
            addYTLink(title, title.replace(" - ", " "), "playYTByTitle", poster, song, artist, "", "", "")
        else:
            if xbox:
                url = "plugin://video/Youtube Music/?url=" + urllib.quote_plus(
                    title.replace(" - ", " ")) + "&mode=playYTByTitle&addontype=YTM"
            else:
                url = "plugin://" + addonID + "/?url=" + urllib.quote_plus(
                    title.replace(" - ", " ")) + "&mode=playYTByTitle&addontype=YTM"
            musicVideos.append([title, url, poster])
            if limit and int(limit) == pos:
                break
            pos += 1

    if type == "browse":
        if forceView:
            xbmc.executebuiltin('Container.SetViewMode(' + viewIDPlaylists + ')')
        xbmcplugin.endOfDirectory(pluginhandle)
    else:
        random.shuffle(musicVideos)
        for title, url, thumb in musicVideos:
            listitem = xbmcgui.ListItem(title, thumbnailImage=thumb)
            playlist.add(url, listitem)
        xbmc.Player().play(playlist)


def youtube_playlist_search():
    searcher = PlayListSearcher()
    output = searcher.start_search()
    data = json.loads(output.decode('utf-8'))
    for playlist in data['playlists']:
        addAutoPlayDirYT(playlist['name'].encode('utf-8'), playlist['url'].encode('utf-8'), "listYoutubePlayList", playlist['img'].encode('utf-8'), "", "browse")
    xbmcplugin.endOfDirectory(pluginhandle)


def listYoutubePlayList(type, url, limit, name="", img=""):
    pos = 1
    playlist_id = url
    if type == "add":
        add_playlist_to_fav_file(url, name, img)
        return
    if type == "remove":
        fh = open(PLAYLIST_FILE, 'r')
        data = json.loads(fh.read().decode('utf-8'))
        for playlist in data['playlists']:
            if playlist.get('url') == playlist_id:
                dialog = xbmcgui.Dialog()
                del data['playlists'][data['playlists'].index(playlist)]
                fh = open(PLAYLIST_FILE, "w")
                fh.write(json.dumps(data))
                fh.close()
                dialog.ok("Youtube Music", "Playlist Removed from Favourites file")
                xbmc.executebuiltin("Container.Refresh")
                break
        return
    if type == "play":
        musicVideos = []
        xbmc_playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        xbmc_playlist.clear()
    data = json.loads(ripYoutubePlaylist(playlist_id))
    for item in data['items']:
        if type == "browse":
            addLinkId(item['title'], item['video_id'], "playYTById", item['img'])
        else:
            if xbox:
                url = "plugin://video/Youtube Music/?videoid=" + item['video_id'] + "&mode=autoPlayYTById&addontype=YTM"
            else:
                url = "plugin://" + addonID + "/?videoid=" + item['video_id'] + "&mode=autoPlayYTById&addontype=YTM"
            musicVideos.append([item['title'], url, item['img']])
            if limit and int(limit) == pos:
                break
            pos += 1
    if type == "browse":
        xbmcplugin.endOfDirectory(pluginhandle)
    else:
        random.shuffle(musicVideos)
        for title, url, thumb in musicVideos:
            listitem = xbmcgui.ListItem(title, thumbnailImage=thumb)
            xbmc_playlist.add(url, listitem)
        xbmc.Player().play(xbmc_playlist)


def YotubeMyPlayListMain():
    fh = open(PLAYLIST_FILE, 'r')
    data = json.loads(fh.read().decode('utf-8'))
    for playlist in data['playlists']:
        addAutoPlayDirYT(playlist['name'], playlist['url'], "listYoutubePlayList", playlist['img'], "", "browse")
    fh.close()
    xbmcplugin.endOfDirectory(pluginhandle)


def ripYoutubePlaylist(playlist_id):
    ripper = PlayListRipper()
    # if not exist in cache than rip & save
    data = ripper.getRipped("youtube_playlist_" + playlist_id, cacheDir, 30)
    if (data is None):
        ripper.rip(playlist_id)
        data = ripper.save("youtube_playlist_" + playlist_id, cacheDir)
    return data


def add_playlist_to_fav_file(playlist_id, title, image):
    img_url = 'https://i.ytimg.com/vi/' + image + '/hqdefault.jpg'
    fh = open(PLAYLIST_FILE, 'a+')
    data = json.loads(fh.read().decode('utf-8'))
    new_entry = {"url": playlist_id, "name": title, "img": img_url}
    dialog = xbmcgui.Dialog()
    if new_entry not in data['playlists']:
        data['playlists'].append(new_entry)
        with open(PLAYLIST_FILE, 'w') as outfile:
            json.dump(data, outfile)
        dialog.ok("Youtube Music", "Playlist added to Favourites file")
    else:
        dialog.ok("Youtube Music", "Playlist Already exists in Favourites file")


def addAutoPlayDirYT(name, url, mode, iconimage="", description="", type="", limit=""):
    suffix = ""
    list = name + "<>"+url + "<>" + iconimage + "<>YTplaylist"
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&type=" + str(type) + "&limit=" + str(
        limit)+"&addontype=YTM"
    ok = True
    img_id = iconimage[iconimage.find("vi/") + 3:iconimage.find("/hq")]
    contextMenuItems=[]
    if not is_favourite(PLAYLIST_FILE, list):
        suffix = ""
        contextMenuItems.append(("[COLOR lime]Add to Favourite YouTube Playlists[/COLOR]",
                                'XBMC.RunPlugin(%s?name=%s&url=%s&mode=add_favourite)' % (
                                                                sys.argv[0], '3', str(list))))
    else:
        heart = u"\u2764"
        suffix = ' [COLOR red][B]' + heart + '[/B][/COLOR]'
        contextMenuItems.append(("[COLOR orange]Remove from Favourite YouTube Playlists[/COLOR]",
                                'XBMC.RunPlugin(%s?name=%s&url=%s&mode=remove_favourite)' % (
                                                                sys.argv[0], '3', str(list))))

    contextMenuItems.append((translation(400200),
                    'RunPlugin(plugin://' + addonID + '/?mode=' + str(mode) + '&url=' + urllib.quote_plus(
                        url) + '&type=play&limit=&addontype=YTM)',))
    contextMenuItems.append((translation(400201),
                    'RunPlugin(plugin://' + addonID + '/?mode=' + str(mode) + '&url=' + urllib.quote_plus(
                        url) + '&type=play&limit=10&addontype=YTM)',))
    contextMenuItems.append((translation(400202),
                    'RunPlugin(plugin://' + addonID + '/?mode=' + str(mode) + '&url=' + urllib.quote_plus(
                        url) + '&type=play&limit=20&addontype=YTM)',))
    contextMenuItems.append((translation(400203),
                    'RunPlugin(plugin://' + addonID + '/?mode=' + str(mode) + '&url=' + urllib.quote_plus(
                        url) + '&type=play&limit=30&addontype=YTM)',))
    contextMenuItems.append((translation(400204),
                    'RunPlugin(plugin://' + addonID + '/?mode=' + str(mode) + '&url=' + urllib.quote_plus(
                        url) + '&type=play&limit=40&addontype=YTM)',))
    contextMenuItems.append((translation(400205),
                    'RunPlugin(plugin://' + addonID + '/?mode=' + str(mode) + '&url=' + urllib.quote_plus(
                        url) + '&type=play&limit=50&addontype=YTM)',))

    liz = xbmcgui.ListItem(name + suffix, iconImage="DefaultAudio.png", thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={"Title": name, "Plot": description})
    liz.addContextMenuItems(contextMenuItems)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
    return ok


def addLinkId(name, videoid, mode, iconimage):
    u = sys.argv[0] + "?videoid=" + videoid + "&mode=" + str(mode)+ '&addontype=YTM'
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultAudio.png", thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={"Title": name})
    liz.setProperty('IsPlayable', 'true')
    entries = []
    entries.append((translation(30004), 'RunPlugin(plugin://' + addonID + '/?mode=queueVideo&url=' + urllib.quote_plus(
        u) + '&videoid=' + videoid + '&addontype=YTM',))
    liz.addContextMenuItems(entries)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz)
    return ok


'''
**********************************************************************************************************************
favourites functions
**********************************************************************************************************************
'''


def clean_favourites_categories():
    addDir(translation(400300), '0', 'clean_favourites', artgenre + 'favouritesongs.jpg', '')
    addDir(translation(400301), '1', 'clean_favourites', artgenre + 'favouritesongs.jpg', '')
    addDir(translation(400302), '2', 'clean_favourites', artgenre + 'favouritesongs.jpg', '')
    addDir(translation(400303), '3', 'clean_favourites', artgenre + 'favouritesongs.jpg', '')

def clean_favourites(dir):
    menu_texts = []
    menu_texts.append(translation(400406))
    dialog = xbmcgui.Dialog()
    if os.path.isfile(dir):
        fh = open(dir, 'r+')
        try:
            file_dict = json.loads(fh.read(), encoding='utf-8')
        except:
            return (None, None)
            dialog.close()
        for category in file_dict:
            menu_texts.append(category)
    else:
        return (None, None)
        dialog.close()

    menu_id = dialog.select(translation(400404), menu_texts)
    if (menu_id < 0):
        return (None, None)
        dialog.close()

    if "song" in dir:
        title = "Song File"
    elif "album" in dir:
        title = "Album File"
    elif "Playlist" in dir:
        title = "Playlist File"
    else:
        title = "Artists File"

    category = menu_texts[menu_id]
    if category == translation(400406):
        file_dict = {}
        fh.seek(0)
        fh.truncate()
        json.dump(file_dict, fh)
        fh.close()
        notification(title, "[COLOR orange]"+translation(400404)+"[/COLOR]", '5000', "")
    else:
        del file_dict[category]
        fh.seek(0)
        fh.truncate()
        json.dump(file_dict, fh)
        fh.close()
        notification(title, "[COLOR orange]" + category.encode('utf-8') + " "+ translation(400401)+"[/COLOR]",
                     '5000', "")


def load_songs_from_heb_album(album_name, url):
    musicVideos = []
    splitdata = url.split('/')
    artist = splitdata[1].replace("+", " ")
    for item in art_dict[artist.decode('utf-8')]["disks"]:
        if item["disk_name"].encode('utf-8') == album_name:
            for track in item["tracks"]:
                songname = track["track_name"].encode('utf-8')
                title = artist + " - " + songname
                if xbox:
                    url = "plugin://video/Youtube Music/?url=" + urllib.quote_plus(
                        title.replace(" - ", " ")) + "&mode=playYTByTitle&addontype=YTM"
                else:
                    url = "plugin://" + addonID + "/?url=" + urllib.quote_plus(
                        title.replace(" - ", " ")) + "&mode=playYTByTitle&addontype=YTM"
                musicVideos.append([title, url, item["disk_img"].encode('utf-8')])

    return musicVideos


def load_songs_from_eng_album(album_name, url, img):
    origurl = url
    musicVideos = []
    std = 'id="(.+?)" itemprop="tracks" itemscope="itemscope" itemtype="http://schema.org/MusicRecording"><td class="song__play_button"><a class="player__play_btn js_play_btn" href="#" rel="(.+?)" title="Play track" /></td><td class="song__name"><div class="title_td_wrap"><meta content="(.+?)" itemprop="url" /><meta content="(.+?)" itemprop="duration"(.+?)<meta content="(.+?)" itemprop="inAlbum" /><meta content="(.+?)" itemprop="byArtist" /><span itemprop="name">(.+?)</span><div class="jp-seek-bar" data-time="(.+?)"><div class="jp-play-bar"></div></div></div></td><td class="(.+?)__service song__service--ringtone'
    alt = std.replace('rel="(.+?)', '')
    match = []
    link = GET_url(url)
    link = link.split('<tr class="song" ')

    for song in link:
        if 'rel=' in song:
            items = re.compile(std).findall(song)
            for item in items:
                match.append(item)
        else:
            items = re.compile(alt).findall(song)
            for item in items:
                item = (item[0], '', item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8])
                match.append(item)

    for track, id, songurl, meta, d1, album, artist, songname, dur, artist1 in match:
        url = 'http://files.musicmp3.ru/lofi/' + id
        songname = songname.replace('&amp;', 'and')
        artist = artist.replace('&amp;', 'and')
        title = artist + " " + songname
        if xbox:
            url = "plugin://video/Youtube Music/?url=" + urllib.quote_plus(
                title.replace(" - ", " ")) + "&mode=playYTByTitle&addontype=YTM"
        else:
            url = "plugin://" + addonID + "/?url=" + urllib.quote_plus(
                title.replace(" - ", " ")) + "&mode=playYTByTitle&addontype=YTM"
        musicVideos.append([title, url, ""])

    return musicVideos

'''
=========play_favourites_songs============
'''
def play_favourites_albums():
    dir = FAV_ALBUM
    musicVideos = []
    playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    playlist.clear()
    menu_texts = []
    menu_texts.append(translation(400406))
    dialog = xbmcgui.Dialog()
    if os.path.isfile(dir):
        fh = open(dir, 'r+')
        try:
            file_dict = json.loads(fh.read(), encoding='utf-8')
        except:
            return (None, None)
            dialog.close()
        for category in file_dict:
            menu_texts.append(category)
    else:
        return (None, None)
        dialog.close()

    menu_id = dialog.select(translation(400404), menu_texts)
    if (menu_id < 0):
        return (None, None)
        dialog.close()

    category = menu_texts[menu_id]
    if category == translation(400406):
        for tag in file_dict:
            cat_list = file_dict.get(tag)
            for item in cat_list:
                if item["type"].encode('utf-8') == "hebalbum":
                    musicVideos += load_songs_from_heb_album(item["album"].encode('utf-8'), item["url"].encode('utf-8'))
                else:
                    musicVideos += load_songs_from_eng_album(item["album"].replace('&amp;', '&').encode('utf-8'),
                                                             item["url"].encode('utf-8'), item["img"].encode('utf-8'))
    else:
        cat_list = file_dict.get(category)
        for item in cat_list:
            if item["type"].encode('utf-8') == "hebalbum":
                musicVideos += load_songs_from_heb_album(item["album"].encode('utf-8'), item["url"].encode('utf-8'))
            else:
                musicVideos += load_songs_from_eng_album(item["album"].replace('&amp;', '&').encode('utf-8'),
                                                         item["url"].encode('utf-8'), item["img"].encode('utf-8'))

    random.shuffle(musicVideos)
    for title, url, thumb in musicVideos:
        listitem = xbmcgui.ListItem(title, thumbnailImage=thumb)
        playlist.add(url, listitem)
    notification("MIX ALBUMS", "[COLOR lime]"+translation(400403)+" " + str(len(musicVideos)) + "[/COLOR]", '5000', "")
    xbmc.Player().play(playlist)

'''
=========play_favourites_songs============
'''
def play_favourites_songs():
    dir = FAV_SONG
    musicVideos = []
    playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    playlist.clear()
    menu_texts = []
    menu_texts.append(translation(400406))
    dialog = xbmcgui.Dialog()
    if os.path.isfile(dir):
        fh = open(dir, 'r+')
        try:
            file_dict = json.loads(fh.read(), encoding='utf-8')
        except:
            return (None, None)
            dialog.close()
        for category in file_dict:
            menu_texts.append(category)
    else:
        return (None, None)
        dialog.close()

    menu_id = dialog.select(translation(400404), menu_texts)
    if (menu_id < 0):
        return (None, None)
        dialog.close()

    category = menu_texts[menu_id]
    if category == translation(400406):
        for tag in file_dict:
            cat_list = file_dict.get(tag)
            for item in cat_list:
                if item["type"] == 'hebrew' or item["type"] == "hebalbum" or item["type"] == "hebartists":
                    img = MAKO_URL + item["img"]
                else:
                    img = item["img"]
                title = item["artist"].encode('utf-8') + " - " + item["song"].encode('utf-8')
                if xbox:
                    url = "plugin://video/Youtube Music/?url=" + urllib.quote_plus(
                        title.replace(" - ", " ")) + "&mode=playYTByTitle&addontype=YTM"
                else:
                    url = "plugin://" + addonID + "/?url=" + urllib.quote_plus(
                        title.replace(" - ", " ")) + "&mode=playYTByTitle&addontype=YTM"
                musicVideos.append([title, url, img])
    else:
        cat_list = file_dict.get(category)
        for item in cat_list:
            if item["type"] == 'hebrew' or item["type"] == "hebalbum" or item["type"] == "hebartists":
                img = MAKO_URL + item["img"]
            else:
                img = item["img"]
            title = item["artist"].encode('utf-8') + " - " + item["song"].encode('utf-8')
            if xbox:
                url = "plugin://video/Youtube Music/?url=" + urllib.quote_plus(
                    title.replace(" - ", " ")) + "&mode=playYTByTitle&addontype=YTM"
            else:
                url = "plugin://" + addonID + "/?url=" + urllib.quote_plus(
                    title.replace(" - ", " ")) + "&mode=playYTByTitle&addontype=YTM"
            musicVideos.append([title, url, img])

    random.shuffle(musicVideos)
    for title, url, thumb in musicVideos:
        listitem = xbmcgui.ListItem(title, thumbnailImage=thumb)
        playlist.add(url, listitem)
    xbmc.Player().play(playlist)


'''
=========show_favourites============
'''
def show_favourites(dir):
    menu_texts = []
    menu_texts.append(translation(400406))
    dialog = xbmcgui.Dialog()
    if os.path.isfile(dir):
        fh = open(dir, 'r+')
        try:
            file_dict = json.loads(fh.read(), encoding='utf-8')
        except:
            return (None, None)
            dialog.close()
        for category in file_dict:
            menu_texts.append(category)
    else:
        return (None, None)
        dialog.close()

    menu_id = dialog.select(translation(400404), menu_texts)
    if (menu_id < 0):
        return (None, None)
        dialog.close()

    category = menu_texts[menu_id]
    if category == translation(400406):
        for tag in file_dict:
            cat_list = file_dict.get(tag)
            for item in cat_list:
                if item["type"] == 'hebrew' or item["type"] == "hebalbum" or item["type"] == "hebartists":
                    img = MAKO_URL + item["img"]
                else:
                    img = item["img"]
                if "song" in dir:
                    if item["album"].encode('utf-8') == "":
                        text = "%s - %s" % (item["artist"].encode('utf-8'), item["song"].encode('utf-8'))
                    else:
                        text = "%s - %s - %s" % (
                            item["artist"].encode('utf-8'), item["song"].encode('utf-8'), item["album"].encode('utf-8'))
                    addYTLink(text, item["url"].encode('utf-8'), 'playYTByTitle', img.encode('utf-8'),
                              item["song"].encode('utf-8'), item["artist"].encode('utf-8'),
                              item["album"].encode('utf-8'), '', item["type"].encode('utf-8'))
                elif "album" in dir:
                    if item["type"].encode('utf-8') == "hebalbum":
                        addDir(item["album"].replace('&amp;', '&').encode('utf-8'), item["url"].encode('utf-8'),
                               'play_israeli_album', img.encode('utf-8'), item["type"].encode('utf-8'), 'browse')
                    else:
                        addDir(item["album"].replace('&amp;', '&').encode('utf-8'), item["url"].encode('utf-8'),
                               'play_album', img.encode('utf-8'), item["type"].encode('utf-8'),'browse')
                elif "playlist" in dir:
                    addAutoPlayDirYT(item["name"], item["url"],"listYoutubePlayList",item["img"], "", "browse" )
                else:
                    if item["type"].encode('utf-8') == "hebartists":
                        url = item["artist"].replace('&amp;', '&').encode('utf-8')
                        addDir(item["artist"].replace('&amp;', '&').encode('utf-8'), url, 'israeli_artists_works',
                               img.encode('utf-8'), item["type"].encode('utf-8'))
                    else:
                        addDir(item["artist"].replace('&amp;', '&').encode('utf-8'), item["url"].encode('utf-8'),
                               'albums', img.encode('utf-8'), item["type"].encode('utf-8'))
    else:
        cat_list = file_dict.get(category)
        for item in cat_list:
            if item["type"] == 'hebrew' or item["type"] == "hebalbum" or item["type"] == "hebartists":
                img = MAKO_URL + item["img"]
            else:
                img = item["img"]
            if "song" in dir:
                if item["album"].encode('utf-8') == "":
                    text = "%s - %s" % (item["artist"].encode('utf-8'), item["song"].encode('utf-8'))
                else:
                    text = "%s - %s - %s" % (
                        item["artist"].encode('utf-8'), item["song"].encode('utf-8'), item["album"].encode('utf-8'))
                addYTLink(text, item["url"].encode('utf-8'), 'playYTByTitle', img.encode('utf-8'),
                          item["song"].encode('utf-8'), item["artist"].encode('utf-8'), item["album"].encode('utf-8'),
                          '', item["type"].encode('utf-8'))
            elif "album" in dir:
                if item["type"].encode('utf-8') == "hebalbum":
                    addDir(item["album"].replace('&amp;', '&').encode('utf-8'), item["url"].encode('utf-8'),
                           'play_israeli_album', img.encode('utf-8'), item["type"].encode('utf-8'),'browse')
                else:
                    addDir(item["album"].replace('&amp;', '&').encode('utf-8'), item["url"].encode('utf-8'),
                           'play_album', img.encode('utf-8'), item["type"].encode('utf-8'),'browse')
            elif "playlist" in dir:
                    addAutoPlayDirYT(item["name"], item["url"],"listYoutubePlayList",item["img"],"", "browse" )
            else:
                if item["type"].encode('utf-8') == "hebartists":
                    url = item["artist"].replace('&amp;', '&').encode('utf-8')
                    addDir(item["artist"].replace('&amp;', '&').encode('utf-8'), url, 'israeli_artists_works',
                           img.encode('utf-8'), item["type"].encode('utf-8'))
                else:
                    addDir(item["artist"].replace('&amp;', '&').encode('utf-8'), item["url"].encode('utf-8'), 'albums',
                           img.encode('utf-8'), item["type"].encode('utf-8'))


'''
=========is_favourite============
'''


def is_favourite(dir, query):
    entry = {}
    if os.path.isfile(dir):
        fh = open(dir, 'r')
        try:
            file_dict = json.loads(fh.read(), encoding='utf-8')
        except:
            return False
    else:
        return False

    splitdata = query.split('<>')
    if "song" in dir:
        entry["artist"] = splitdata[0]
        entry["album"] = splitdata[1]
        entry["song"] = splitdata[2]
        entry["url"] = splitdata[3]
        entry["img"] = splitdata[4]
    elif "album" in dir:
        entry["album"] = splitdata[0]
        entry["url"] = splitdata[1]
        entry["img"] = splitdata[2]
    elif "artist" in dir:
        entry["artist"] = splitdata[0]
        entry["url"] = splitdata[1]
        entry["img"] = splitdata[2]
    if "playlist" in dir:
        entry["name"] = splitdata[0]
        entry["url"] = splitdata[1]
        entry["img"] = splitdata[2]
        entry["type"] = splitdata[3]

    try:
        for category in file_dict:
            cat_list = file_dict.get(category)
            for item in cat_list:
                if "song" in dir:
                    if entry["artist"].lower() == item["artist"].encode('utf-8').lower() and entry["song"].lower() == \
                            item["song"].encode(
                                'utf-8').lower():
                        return True
                elif "album" in dir:
                    if entry["album"].lower() == item["album"].encode('utf-8').lower():
                        return True
                elif "artist" in dir:
                    if entry["artist"].lower() == item["artist"].encode('utf-8').lower() and entry["url"] == item[
                        "url"].encode(
                        'utf-8'):
                        return True
                elif "playlist" in dir:
                    if entry["url"].lower() == item["url"].encode('utf-8').lower():
                        return True
        return False
    except:
        return False


'''
=========add_favourite============
'''


def add_favourite(url, dir, text, source):
    entry = {}
    menu_texts = []
    menu_texts.append(translation(400405))
    dialog = xbmcgui.Dialog()
    if os.path.isfile(dir):
        fh = open(dir, 'r+')
        try:
            file_dict = json.loads(fh.read(), encoding='utf-8')
        except:
            file_dict = {}
        for category in file_dict:
            menu_texts.append(category)
    else:
        fh = open(dir, 'w')
        file_dict = {}

    menu_id = dialog.select(translation(400404), menu_texts)
    if (menu_id < 0):
        return (None, None)
        dialog.close()
    if (menu_id == 0):
        keyboard = xbmc.Keyboard('', translation(400414), False)
        keyboard.doModal()
        if keyboard.isConfirmed():
            query = keyboard.getText()
            if len(query) > 0:
                category = query
    else:
        category = menu_texts[menu_id]

    splitdata = url.split('<>')
    if "song" in dir:
        entry["artist"] = splitdata[0]
        entry["album"] = splitdata[1]
        entry["song"] = splitdata[2]
        entry["url"] = splitdata[3]
        entry["img"] = splitdata[4]
        entry["type"] = splitdata[5]
    elif "album" in dir:
        entry["album"] = splitdata[0]
        entry["url"] = splitdata[1]
        entry["img"] = splitdata[2]
        entry["type"] = splitdata[3]
    elif "artist" in dir:
        entry["artist"] = splitdata[0]
        entry["url"] = splitdata[1]
        entry["img"] = splitdata[2]
        entry["type"] = splitdata[3]
    elif "playlist" in dir:
        entry["name"] = splitdata[0]
        entry["url"] = splitdata[1]
        entry["img"] = splitdata[2]
        entry["type"] = splitdata[3]

    try:
        file_dict.get(category).append(entry)
    except:
        file_dict[category] = []
        file_dict.get(category).append(entry)
    fh.seek(0)
    json.dump(file_dict, fh)
    fh.close()
    if "song" in dir:
        notification(entry["song"], "[COLOR lime]" + text + "[/COLOR]", '5000', entry["img"])
    else:
        notification(splitdata[0], "[COLOR lime]" + text + "[/COLOR]", '5000', entry["img"])
    if source == "":
        xbmc.executebuiltin("Container.Refresh")


'''
=========remove_favourite============
'''


def remove_favourite(dir, query, source):
    entry = {}
    if os.path.isfile(dir):
        fh = open(dir, 'r+')
        try:
            file_dict = json.loads(fh.read(), encoding='utf-8')
        except:
            fh.close()
            return

    splitdata = query.split('<>')
    if "song" in dir:
        entry["artist"] = splitdata[0]
        entry["album"] = splitdata[1]
        entry["song"] = splitdata[2]
        entry["url"] = splitdata[3]
        entry["img"] = splitdata[4]
        entry["type"] = splitdata[5]
    elif "album" in dir:
        entry["album"] = splitdata[0]
        entry["url"] = splitdata[1]
        entry["img"] = splitdata[2]
        entry["type"] = splitdata[3]
    elif "artist" in dir:
        entry["artist"] = splitdata[0]
        entry["url"] = splitdata[1]
        entry["img"] = splitdata[2]
        entry["type"] = splitdata[3]
    if "playlist" in dir:
        entry["name"] = splitdata[0]
        entry["url"] = splitdata[1]
        entry["img"] = splitdata[2]
        entry["type"] = splitdata[3]

    is_found = False

    try:
        for category in file_dict:
            cat_list = file_dict.get(category)
            for item in cat_list:
                if "song" in dir:
                    if entry["artist"].lower() == item["artist"].encode('utf-8').lower() and entry["song"].lower() ==  item["song"].encode('utf-8').lower():
                        cat_list.remove(item)
                        is_found = True
                elif "album" in dir:
                    if entry["album"].lower() == item["album"].encode('utf-8').lower():
                        cat_list.remove(item)
                        is_found = True
                elif "artist" in dir:
                    if entry["artist"].lower() == item["artist"].encode('utf-8').lower() and entry["url"] == item["url"].encode('utf-8'):
                        cat_list.remove(item)
                        is_found = True
                elif "playlist" in dir:
                    if entry["url"].lower() == item["url"].encode('utf-8').lower():
                        cat_list.remove(item)
                        is_found = True

                if is_found:
                    if "song" in dir:
                        notification(entry["song"], "[COLOR orange]"+translation(400401)+"[/COLOR]", '5000', entry["img"])
                    else:
                        notification(splitdata[0], "[COLOR orange]"+translation(400401)+"[/COLOR]", '5000', entry["img"])
                    if not cat_list:
                        del file_dict[category]
                    else:
                        file_dict[category] = cat_list
                    fh.seek(0)
                    fh.truncate()
                    json.dump(file_dict, fh)
                    fh.close()
                    if source == "":
                        xbmc.executebuiltin("Container.Refresh")
                    return
    except:
        fh.close()


def read_from_file(path, silent=False):
    try:
        f = open(path, 'r')
        r = f.read()
        f.close()
        return str(r)
    except:
        if not silent:
            print("Could not read from " + path)
        return None


'''
**********************************************************************************************************************
open connections functions
**********************************************************************************************************************
'''
'''
=========open_url============
'''


def open_url(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent',
                   'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    return link


'''
=========GET_url============
'''


def GET_url(url):
    header_dict = {}
    if 'musicmp3' in url:
        header_dict[
            'Accept'] = 'audio/webm,audio/ogg,udio/wav,audio/*;q=0.9,application/ogg;q=0.7,video/*;q=0.6,*/*;q=0.5'
        header_dict['User-Agent'] = 'AppleWebKit/<WebKit Rev>'
        header_dict['Host'] = 'musicmp3.ru'
        header_dict['Referer'] = 'http://musicmp3.ru/'
        header_dict['Connection'] = 'keep-alive'
    if 'goldenmp3' in url:
        header_dict['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        header_dict['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; rv:35.0) Gecko/20100101 Firefox/35.0'
        header_dict['Host'] = 'www.goldenmp3.ru'
        header_dict['Referer'] = 'http://www.goldenmp3.ru/compilations/events/albums'
        header_dict['Connection'] = 'keep-alive'
    if 'last.fm' in url:
        header_dict['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        header_dict['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; rv:35.0) Gecko/20100101 Firefox/35.0'
        header_dict['Host'] = 'www.last.fm'
        header_dict['Referer'] = 'http://www.last.fm/music/'
        header_dict['Connection'] = 'keep-alive'
    if 'shironet' in url:
        header_dict['Accept'] = 'application/x-javascript'
        header_dict['User-Agent'] = 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'
        header_dict['Host'] = 'shironet.mako.co.il'
        header_dict['Referer'] = 'http://shironet.mako.co.il'
        header_dict['Connection'] = 'keep-alive'
    net.set_cookies(cookie_jar)
    link = net.http_GET(url, headers=header_dict).content.encode("utf-8").rstrip()
    net.save_cookies(cookie_jar)
    return link


'''
**********************************************************************************************************************
links&folders functions
**********************************************************************************************************************
'''


def addAutoPlayDirGlz(name, url, mode, iconimage="", description="", type="", limit=""):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&type=" + str(type) + "&limit=" + str(
        limit) + "&addontype=YTM"
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultMusicVideos.png", thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={"Title": name, "Plot": description})
    liz.setProperty('fanart_image', fanart)
    entries = []
    entries.append(("נגן הכל", 'RunPlugin(plugin://' + addonID + '/?mode=' + str(mode) + '&url=' + urllib.quote_plus(
        url) + '&type=play&addontype=YTM&limit=)',))
    entries.append(("נגן טופ 10", 'RunPlugin(plugin://' + addonID + '/?mode=' + str(mode) + '&url=' + urllib.quote_plus(
        url) + '&type=play&addontype=YTM&limit=10)',))
    entries.append(("נגן טופ 20", 'RunPlugin(plugin://' + addonID + '/?mode=' + str(mode) + '&url=' + urllib.quote_plus(
        url) + '&type=play&addontype=YTM&limit=20)',))
    entries.append(("נגן טופ 30", 'RunPlugin(plugin://' + addonID + '/?mode=' + str(mode) + '&url=' + urllib.quote_plus(
        url) + '&type=play&addontype=YTM&limit=30)',))
    entries.append(("נגן טופ 40", 'RunPlugin(plugin://' + addonID + '/?mode=' + str(mode) + '&url=' + urllib.quote_plus(
        url) + '&type=play&addontype=YTM&limit=40)',))
    entries.append(("נגן טופ 50", 'RunPlugin(plugin://' + addonID + '/?mode=' + str(mode) + '&url=' + urllib.quote_plus(
        url) + '&type=play&addontype=YTM&limit=50)',))
    entries.append(("נגן טופ 100",
                    'RunPlugin(plugin://' + addonID + '/?mode=' + str(mode) + '&url=' + urllib.quote_plus(
                        url) + '&type=play&addontype=YTM&limit=100)',))
    liz.addContextMenuItems(entries)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
    return ok


def addYTDir(name, url, mode, iconimage="", description="", type="", limit=""):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&type=" + str(type) + "&limit=" + str(
        limit) + "&addontype=YTM"
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultMusicVideos.png", thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={"Title": name, "Plot": description})
    liz.setProperty('fanart_image', fanart)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
    return ok


def addAutoPlayDir(name, url, mode, iconimage="", description="", type="", limit=""):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&type=" + str(type) + "&limit=" + str(
        limit) + "&addontype=YTM"
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultMusicVideos.png", thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={"Title": name, "Plot": description})
    liz.setProperty('fanart_image', fanart)
    entries = []
    entries.append((translation(400200),
                    'RunPlugin(plugin://' + addonID + '/?mode=' + str(mode) + '&url=' + urllib.quote_plus(
                        url) + '&type=play&addontype=YTM&limit=)',))
    entries.append((translation(400201),
                    'RunPlugin(plugin://' + addonID + '/?mode=' + str(mode) + '&url=' + urllib.quote_plus(
                        url) + '&type=play&addontype=YTM&limit=10)',))
    entries.append((translation(400202),
                    'RunPlugin(plugin://' + addonID + '/?mode=' + str(mode) + '&url=' + urllib.quote_plus(
                        url) + '&type=play&addontype=YTM&limit=20)',))
    entries.append((translation(400203),
                    'RunPlugin(plugin://' + addonID + '/?mode=' + str(mode) + '&url=' + urllib.quote_plus(
                        url) + '&type=play&addontype=YTM&limit=30)',))
    entries.append((translation(400204),
                    'RunPlugin(plugin://' + addonID + '/?mode=' + str(mode) + '&url=' + urllib.quote_plus(
                        url) + '&type=play&addontype=YTM&limit=40)',))
    entries.append((translation(400205),
                    'RunPlugin(plugin://' + addonID + '/?mode=' + str(mode) + '&url=' + urllib.quote_plus(
                        url) + '&type=play&addontype=YTM&limit=50)',))
    liz.addContextMenuItems(entries)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
    return ok


'''
=========play_album============
'''
def play_album(name, url, iconimage, mix, clear, action):
    if action == "play":
        musicVideos = []
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()

    std = 'id="(.+?)" itemprop="tracks" itemscope="itemscope" itemtype="http://schema.org/MusicRecording"><td class="song__play_button"><a class="player__play_btn js_play_btn" href="#" rel="(.+?)" title="Play track" /></td><td class="song__name"><div class="title_td_wrap"><meta content="(.+?)" itemprop="url" /><meta content="(.+?)" itemprop="duration"(.+?)<meta content="(.+?)" itemprop="inAlbum" /><meta content="(.+?)" itemprop="byArtist" /><span itemprop="name">(.+?)</span><div class="jp-seek-bar" data-time="(.+?)"><div class="jp-play-bar"></div></div></div></td><td class="(.+?)__service song__service--ringtone'
    alt = std.replace('rel="(.+?)', '')
    match = []
    link = GET_url(url)
    link = link.split('<tr class="song" ')

    for song in link:
        if 'rel=' in song:
            items = re.compile(std).findall(song)
            for item in items:
                match.append(item)
        else:
            items = re.compile(alt).findall(song)
            for item in items:
                item = (item[0], '', item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8])
                match.append(item)

    for track, id, songurl, meta, d1, album, artist, songname, dur, artist1 in match:
        trn = track.replace('track', '')
        url = 'http://files.musicmp3.ru/lofi/' + id
        songname = songname.replace('&amp;', 'and')
        artist = artist.replace('&amp;', 'and')
        album = album.replace('&amp;', 'and')
        title = "%s. %s" % (track.replace('track', ''), songname)
        if action == 'browse':
            addYTLink(title, url, 'playYTByTitle', iconimage, songname, artist, album, dur, '')
        else:
            title = artist + " - " + songname
            if xbox:
                url = "plugin://video/Youtube Music/?url=" + urllib.quote_plus(
                    title.replace(" - ", " ")) + "&mode=playYTByTitle&addontype=YTM"
            else:
                url = "plugin://" + addonID + "/?url=" + urllib.quote_plus(
                        title.replace(" - ", " ")) + "&mode=playYTByTitle&addontype=YTM"
            musicVideos.append([title, url, ""])

    if action == "browse":
        xbmcplugin.endOfDirectory(pluginhandle)
    else:
        random.shuffle(musicVideos)
        for title, url, thumb in musicVideos:
            listitem = xbmcgui.ListItem(title, thumbnailImage=thumb)
            playlist.add(url, listitem)
        xbmc.Player().play(playlist)


'''
=========addDir============
'''


def addDir(name, url, mode, iconimage, type, action='', source=''):
    suffix = ""
    if type == "hebartists" or type == "hebalbum":
        list = name + "<>" + url + "<>" + clean_mako_img(iconimage) + "<>" + type
    else:
        list = "%s<>%s<>%s<>%s" % (str(name).lower(), url, str(iconimage), type)
    list = list.replace(',', '')
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(
        name) + "&iconimage=" + urllib.quote_plus(iconimage) + "&list=" + str(list) + "&type=" + str(type)+"&action="+action
    ok = True
    contextMenuItems = []

    if type == "artists" or type == "hebartists":
        if not is_favourite(FAV_ARTIST, list):
            suffix = ""
            contextMenuItems.append(("[COLOR lime]"+translation(400407)+"[/COLOR]",
                                     'XBMC.RunPlugin(%s?name=%s&url=%s&mode=add_favourite&source=%s)' % (
                                         sys.argv[0], '0', str(list), source)))
        else:
            if type == 'hebartists':
                heart = u"\u2764".encode('utf-8')
            else:
                heart = u"\u2764"
            suffix = ' [COLOR red][B]' + heart + '[/B][/COLOR]'
            contextMenuItems.append(("[COLOR orange]"+translation(400408)+"[/COLOR]",
                                     'XBMC.RunPlugin(%s?name=%s&url=%s&mode=remove_favourite&source=%s)' % (
                                         sys.argv[0], '0', str(list), source)))
    if type == 'albums' or type == "hebalbum":
        if type == 'albums':
            contextMenuItems.append(("[COLOR blue]"+translation(400411)+"[/COLOR]",
                                         'XBMC.RunPlugin(%s?name=%s&url=%s&iconimage=%s&action=play&mode=play_album)' % (
                                             sys.argv[0], name, url,iconimage)))
        else:
            contextMenuItems.append(("[COLOR blue]"+translation(400411)+"[/COLOR]",
                                         'XBMC.RunPlugin(%s?&url=%s&action=play&mode=play_israeli_album)' % (
                                             sys.argv[0],url)))
        if not is_favourite(FAV_ALBUM, list):
            suffix = ""
            contextMenuItems.append(("[COLOR lime]"+translation(400409)+"[/COLOR]",
                                     'XBMC.RunPlugin(%s?name=%s&url=%s&mode=add_favourite&source=%s)' % (
                                         sys.argv[0], '1', str(list),source)))
        else:
            if type == 'hebalbum':
                heart = u"\u2764".encode('utf-8')
            else:
                heart = u"\u2764"
            suffix = ' [COLOR red][B]' + heart + '[/B][/COLOR]'
            contextMenuItems.append(("[COLOR orange]"+translation(400410)+"[/COLOR]",
                                     'XBMC.RunPlugin(%s?name=%s&url=%s&mode=remove_favourite&source=%s)' % (
                                         sys.argv[0], '1', str(list), source)))

    liz = xbmcgui.ListItem(name + suffix, iconImage="DefaultAudio.png", thumbnailImage=iconimage)
    liz.addContextMenuItems(contextMenuItems, replaceItems=False)
    liz.setInfo(type="Audio", infoLabels={"Title": name})
    liz.setProperty('fanart_image', fanart)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
    return ok

'''
=========clean_mako_img============
'''


def clean_mako_img(img):
    img = img.replace(MAKO_URL, "")
    try:
        img = img[:img.index('?')]
    except:
        return img
    return img


'''
=========addYTLink============
'''

def addYTLink(name, url, mode, iconimage, songname, artist, album, dur, type, source=''):
    suffix = ""
    if type == 'hebrew':
        list = artist + "<>" + album + "<>" + songname + "<>" + url + "<>" + clean_mako_img(iconimage) + "<>" + type
    else:
        list = "%s<>%s<>%s<>%s<>%s<>%s" % (
            str(artist), str(album), str(songname).lower(), url, str(iconimage), "normal")
    list = list.replace(',', '')
    u = sys.argv[0] + "?url=" + urllib.quote_plus(artist + "+" + songname) + "&mode=" + str(mode)
    contextMenuItems = []
    ok = True
    if not is_favourite(FAV_SONG, list):
        suffix = ""
        contextMenuItems.append(("[COLOR lime]"+translation(400412)+"[/COLOR]",
                                 'XBMC.RunPlugin(%s?name=%s&url=%s&mode=add_favourite&source=%s)' % (
                                     sys.argv[0], '2', str(list), source)))
    else:
        if type == 'hebrew':
            heart = u"\u2764".encode('utf-8')
        else:
            heart = u"\u2764"
        suffix = ' [COLOR red][B]' + heart + '[/B][/COLOR]'
        contextMenuItems.append(("[COLOR orange]"+translation(400413)+"[/COLOR]",
                                 'XBMC.RunPlugin(%s?name=%s&url=%s&mode=remove_favourite&source=%s)' % (
                                     sys.argv[0], '2', str(list), source)))
    liz = xbmcgui.ListItem(name + suffix, iconImage="DefaultAudio.png", thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={"Title": name})
    liz.addContextMenuItems(contextMenuItems, replaceItems=False)
    liz.setProperty('IsPlayable', 'true')
    liz.setProperty('fanart_image', fanart)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz)
    return ok


'''
**********************************************************************************************************************
youtube functions
**********************************************************************************************************************
'''

def queueVideo(url, name):
    playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    listitem = xbmcgui.ListItem(name)
    playlist.add(url, listitem)

def playYTById(youtubeID):
    try:
        if xbox:
            url = "plugin://video/YouTube/?path=/root/video&action=play_video&videoid=" + youtubeID
        else:
            url = "plugin://plugin.video.youtube/play/?video_id=" + youtubeID
        listitem = xbmcgui.ListItem(path=url)
        xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)
    except:
        pass

def autoPlayYTById(youtubeID):
    try:
        if xbox:
            url = "plugin://video/YouTube/?path=/root/video&action=play_video&videoid=" + youtubeID
        else:
            url = "plugin://plugin.video.youtube/play/?video_id=" + youtubeID
        listitem = xbmcgui.ListItem(path=url)
        xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)
        if infoEnabled:
            showInfo()
    except:
        pass
'''
=========playYTByTitle============
'''


def playYTByTitle(title):
    try:
        youtubeID = getYoutubeId(title)
        if xbox:
            url = "plugin://video/YouTube/?path=/root/video&action=play_video&videoid=" + youtubeID
        else:
            url = "plugin://plugin.video.youtube/play/?video_id=" + youtubeID
        listitem = xbmcgui.ListItem(path=url)
        xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)
        if infoEnabled:
            showInfo()
    except:
        pass


'''
=========getYoutubeId============
'''


def getYoutubeId(title):
    link = GET_url("http://www.youtube.com/results?lclk=video&filters=video&search_query=" + urllib.quote_plus(title))
    match = re.compile('class="item-section">.+?data-context-item-id="(.+?)"', re.DOTALL).findall(link)
    return match[0]


'''
**********************************************************************************************************************
general utility functions
**********************************************************************************************************************
'''


def cache(url, duration):
    cacheFile = os.path.join(cacheDir, (''.join(c for c in unicode(url, 'utf-8') if c not in '/\\:?"*|<>')).strip())
    if os.path.exists(cacheFile) and duration != 0 and (
                    time.time() - os.path.getmtime(cacheFile) < 60 * 60 * 24 * duration):
        fh = open(cacheFile, 'r')
        content = fh.read()
        fh.close()
    else:
        content = opener.open(url).read()
        fh = open(cacheFile, 'w')
        fh.write(content)
        fh.close()
    return content


def cleanTitle(title):
    title = title.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&").replace("&#39;", "'").replace(
        "&#039;", "'").replace("&quot;", "\"").replace("&szlig;", "ß").replace("&ndash;", "-")
    title = title.replace("&Auml;", "Ä").replace("&Uuml;", "Ü").replace("&Ouml;", "Ö").replace("&auml;", "ä").replace(
        "&uuml;", "ü").replace("&ouml;", "ö")
    title = title.strip()
    return title


'''
=========translation============
'''


def translation(id):
    return addon.getLocalizedString(id).encode('utf-8')


'''
=========download_img_thread============
'''
class download_img_thread(Thread):
    def __init__(self, artist):
        self.artist = artist
        Thread.__init__(self)

    def run(self):
        self.get_images(self.artist)

    def get_images(self, artist):
        base_url = "http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist="
        end_url = "&api_key=57ee3318536b23ee81d6b27e36997cde&format=json"
        link = open_url(base_url + artist.replace("&amp;", "and").replace(" ", "+") + end_url)
        parsed = json.loads(link)
        try:
            img = parsed.get("artist").get("image")[3]["#text"]
            icon_path = os.path.join(ARTIST_ART, artist + '.txt')
            fh = open(icon_path, "w")
            fh.write(img)
            fh.close()
        except:
            return

'''
=========get_artist_img============
'''
def get_artist_img(name):
    data_path = os.path.join(ARTIST_ART, name + '.txt')
    if not os.path.exists(data_path):
        dlThread = download_img_thread(name)
        dlThread.start()


'''
=========notification============
'''


def notification(title, message, ms, nart):
    xbmc.executebuiltin("XBMC.notification(" + title + "," + message + "," + ms + "," + nart + ")")


'''
=========get_params============
'''


def get_params():
    param = []
    paramstring = sys.argv[2]
    if len(paramstring) >= 2:
        params = sys.argv[2]
        cleanedparams = params.replace('?', '')
        if (params[len(params) - 1] == '/'):
            params = params[0:len(params) - 2]
        pairsofparams = cleanedparams.split('&')
        param = {}
        for i in range(len(pairsofparams)):
            splitparams = {}
            splitparams = pairsofparams[i].split('=')
            if (len(splitparams)) == 2:
                param[splitparams[0]] = splitparams[1]

    return param


'''
=========regex_from_to============
'''


def regex_from_to(text, from_string, to_string, excluding=True):
    if excluding:
        r = re.search("(?i)" + from_string + "([\S\s]+?)" + to_string, text).group(1)
    else:
        r = re.search("(?i)(" + from_string + "[\S\s]+?" + to_string + ")", text).group(1)
    return r


'''
=========regex_get_all============
'''


def regex_get_all(text, start_with, end_with):
    r = re.findall("(?i)(" + start_with + "[\S\s]+?" + end_with + ")", text)
    return r


'''
=========setView============
'''


def setView(content, viewType):
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)


'''
=========showInfo============
'''


def showInfo():
    count = 0
    while not xbmc.Player().isPlaying():
        xbmc.sleep(200)
        if count == 50:
            break
        count += 1
    xbmc.sleep(infoDelay * 1000)
    if infoType == "0":
        xbmc.executebuiltin('XBMC.ActivateWindow(12901)')
        xbmc.sleep(infoDuration * 1000)
        xbmc.executebuiltin('XBMC.ActivateWindow(12005)')
    elif infoType == "1":
        title = 'Now playing:'
        videoTitle = xbmc.getInfoLabel('VideoPlayer.Title').replace(",", " ")
        thumb = xbmc.getInfoImage('VideoPlayer.Cover')
        xbmc.executebuiltin('XBMC.Notification(%s, %s, %s, %s)' % (title, videoTitle, infoDuration * 1000, thumb))


'''
**********************************************************************************************************************
MAIN fuction
**********************************************************************************************************************
'''


def handle_MPS_addon(mode, url, name, iconimage, songname, artist, album, list, dur, type, action, source):
    if mode == None or url == None or len(url) < 1:
        CATEGORIES()
    elif mode == 'play_album':
        play_album(name, url, iconimage, '', True, action)
    elif mode == 'artists':
        artists(url)
    elif mode == 'all_artists':
        all_artists(name, url)
    elif mode == 'sub_dir':
        sub_dir(name, url, iconimage)
    elif mode == 'albums':
        albums(name, url)
    elif mode == 'genres':
        genres(name, url)
    elif mode == 'genre_sub_dir':
        genre_sub_dir(name, url, iconimage)
    elif mode == 'album_list':
        album_list(name, url)
    elif mode == 'eng_search_cat':
        eng_search_cat()
    elif mode == 'eng_search_input':
        eng_search_input(url)
    elif mode == 'compilations_menu':
        compilations_menu()
    elif mode == 'compilations_list':
        compilations_list(name, url, iconimage, type)
    elif mode == 'playYTByTitle':
        playYTByTitle(url)
    elif mode == 'israeli_artists':
        israeli_artists(url)
    elif mode == 'israeli_single_char_artists':
        israeli_single_char_artists(url)
    elif mode == 'israeli_artists_works':
        israeli_artists_works(url)
    elif mode == 'play_israeli_album':
        play_israeli_album(url, action)
    elif mode == 'heb_search_cat':
        heb_search_cat(name)
    elif mode == 'heb_search_input':
        heb_search_input(name)
    elif mode == 'ENGLISH_CATEGORIES':
        ENGLISH_CATEGORIES()
    elif mode == 'FAVOURITE_CATEGORIES':
        FAVOURITE_CATEGORIES()
    elif mode == 'CHARTS_CATEGORIES':
        CHARTS_CATEGORIES()
    elif mode == 'show_favourites':
        show_favourites(favourite_paths[int(url)])
    elif mode == 'add_favourite':
        add_favourite(url, favourite_paths[int(name)], translation(400402), source)
    elif mode == 'remove_favourite':
        remove_favourite(favourite_paths[int(name)], url, source)
    elif mode == 'clean_favourites_categories':
        clean_favourites_categories()
    elif mode == 'clean_favourites':
        clean_favourites(favourite_paths[int(url)])
    elif mode == 'play_favourites_songs':
        play_favourites_songs()
    elif mode == 'play_favourites_albums':
        play_favourites_albums()
    elif mode == 'youtube_playlist_search':
        youtube_playlist_search()

def handle_YTM_addon(mode, url, name, type, limit, chartTitle, iconimage, videoid):
    if mode == 'playYTByTitle':
        playYTByTitle(url)
    elif mode == 'playYTByTitle':
        playYTByTitle(url)
    elif mode == 'spotifyMain':
        spotifyMain()
    elif mode == 'itunesMain':
        itunesMain()
    elif mode == 'billboardMain':
        billboardMain()
    elif mode == 'listBillboardArchiveMain':
        listBillboardArchiveMain()
    elif mode == 'hypemMain':
        hypemMain()
    elif mode == 'listHypem':
        listHypem(type, url, limit)
    elif mode == 'listTimeMachine':
        listTimeMachine()
    elif mode == 'listSpotifyGenres':
        listSpotifyGenres(url)
    elif mode == 'listSpotifyPlaylists':
        listSpotifyPlaylists(url)
    elif mode == 'listSpotifyVideos':
        listSpotifyVideos(type, url, limit)
    elif mode == 'playSpotifyVideos':
        playSpotifyVideos(url)
    elif mode == 'listItunesVideos':
        listItunesVideos(type, url, limit)
    elif mode == 'playItunesVideos':
        playItunesVideos(url)
    elif mode == 'listBillboardCharts':
        listBillboardCharts(type, url, limit)
    elif mode == 'listBillboardArchive':
        listBillboardArchive(url)
    elif mode == 'listBillboardArchiveVideos':
        listBillboardArchiveVideos(type, url, limit)
    elif mode == 'listBillboardChartsNew':
        listBillboardChartsNew(type, url, limit)
    elif mode == 'listBillboardChartsTypes':
        listBillboardChartsTypes(url)
    elif mode == 'queueVideo':
        queueVideo(url, name)
    elif mode == 'GalgalatzMain':
        GalgalatzMain()
    elif mode == 'OneFmMain':
        OneFmMain()
    elif mode == 'DisiMain':
        DisiMain()
    elif mode == 'fm99_main':
        fm99_main()
    elif mode == 'fm99_radio':
        fm99_radio()
    elif mode == 'fm99_top_40_playlist':
        fm99_top_40_playlist(type, limit)
    elif mode == 'fm99_main_playlists':
        fm99_main_playlists()
    elif mode == 'fm99_sub_playlists':
        fm99_sub_playlists(url)
    elif mode == 'fm99_dynamic_playlists':
        fm99_dynamic_playlists()
    elif mode == 'fm99_sub_dynamic_playlists':
        fm99_sub_dynamic_playlists(url)
    elif mode == 'fm99_sub_dynamic_slider_sets':
        fm99_sub_dynamic_slider_sets(url)
    elif mode == 'play_mp3_file':
        play_mp3_file(url,name,iconimage)
    elif mode == 'listYoutubePlayList':
        listYoutubePlayList(type, url, limit, name, iconimage)
    elif mode == 'YotubeMyPlayListMain':
        YotubeMyPlayListMain()
    elif mode == 'playYTById':
        playYTById(videoid)
    elif mode == 'autoPlayYTById':
        autoPlayYTById(videoid)
    elif mode == 'listGalgalatzCharts':
        listGalgalatzCharts(type, url, limit)
    elif mode == 'listGalgalatzPlaylist':
        listGalgalatzPlaylist(type, url, limit)
    elif mode == 'listGalgalatzPlaylistMix':
        listGalgalatzPlaylistMix(type, url, limit)
    elif mode == 'listGalgalatzDecadeChart80':
        listGalgalatzDecadeChart80(type, url, limit)
    elif mode == 'listGalgalatzDecadeChart90':
        listGalgalatzDecadeChart90(type, url, limit)
    elif mode == 'listGalgalatzDecadeChart00':
        listGalgalatzDecadeChart00(type, url, limit)
    elif mode == 'PlayGalgalatzRadio':
        PlayGalgalatzRadio(type, url, limit)
    elif mode == 'listOneFmPlaylist':
        listOneFmPlaylist(type, url, limit)
    elif mode == 'listOneFmLastPlayed':
        listOneFmLastPlayed(type, url, limit)
    elif mode == 'PlayOneFmRadio':
        PlayOneFmRadio(type, url, limit)
    elif mode == 'listDisiChart':
        listDisiChart(type, url, limit)
    elif mode == 'listDisiPlaylist':
        listDisiPlaylist(type, url, limit)


def parameters_string_to_dict(parameters):
    paramDict = {}
    if parameters:
        paramPairs = parameters[1:].split("&")
        for paramsPair in paramPairs:
            paramSplits = paramsPair.split('=')
            if (len(paramSplits)) == 2:
                paramDict[paramSplits[0]] = paramSplits[1]
    return paramDict


url = None
name = None
type = None
mode = None
limit = None
chartTitle = None
addonType = 'MPS'
iconimage = None
songname = None
artist = None
album = None
list = None
dur = None
videoid = None
action=None
source=None
paramsFull = parameters_string_to_dict(sys.argv[2])
try:
    mode = urllib.unquote_plus(paramsFull.get('mode', ''))
except:
    pass
try:
    url = urllib.unquote_plus(paramsFull.get('url', ''))
except:
    pass
try:
    name = urllib.unquote_plus(paramsFull.get('name', ''))
except:
    pass
try:
    type = urllib.unquote_plus(paramsFull.get('type', ''))
except:
    pass
try:
    limit = urllib.unquote_plus(paramsFull.get('limit', ''))
except:
    pass
try:
    chartTitle = urllib.unquote_plus(paramsFull.get('chartTitle', ''))
except:
    pass
try:
    addonType = urllib.unquote_plus(paramsFull.get('addontype', ''))
except:
    pass
try:
    iconimage = urllib.unquote_plus(paramsFull["iconimage"])
except:
    pass
try:
    songname = urllib.unquote_plus(paramsFull["songname"])
except:
    pass
try:
    artist = urllib.unquote_plus(paramsFull["artist"])
except:
    pass
try:
    album = urllib.unquote_plus(paramsFull["album"])
except:
    pass
try:
    videoid = urllib.unquote_plus(paramsFull["videoid"])
except:
    pass
try:
    action = urllib.unquote_plus(paramsFull["action"])
except:
    pass
try:
    list = str(paramsFull["list"])
except:
    pass
try:
    dur = str(paramsFull["dur"])
except:
    pass
try:
    source = str(paramsFull["source"])
except:
    pass

if addonType == 'YTM':
    handle_YTM_addon(mode, url, name, type, limit, chartTitle, iconimage, videoid)
else:
    handle_MPS_addon(mode, url, name, iconimage, songname, artist, album, list, dur, type, action, source)



xbmcplugin.endOfDirectory(int(sys.argv[1]))
