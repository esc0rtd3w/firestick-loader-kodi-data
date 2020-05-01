# coding: utf-8
# Main Addon
__author__ = 'mancuniancol'

from xbmcswift2 import Plugin
from tools2 import *

##INITIALISATION
storage = Storage(settings.storageName, type="dict", eval=True)
plugin = Plugin()


###############################
###  MENU    ##################
###############################
@plugin.route('/')
def index():
    textViewer(settings.string(32000), once=True)
    items = [
        {'label': settings.string(32194),
         'path': plugin.url_for('searchMenu'),
         'thumbnail': dirImages("search.png"),
         'properties': {'fanart_image': settings.fanart}
         }]
    listTypes = ['Movies',
                 'Verified Movies',
                 'TV Shows',
                 'Verified TV Shows',
                 'Animes',
                 'Verified Animes',
                 ]
    listUrl = ['/search?q=movies',
               '/verified?f=movies',
               '/search?q=tv',
               '/verified?f=tv',
               '/search?q=anime',
               '/verified?f=anime',
               ]
    listIcons = [dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("tvShows.png"),
                 dirImages("tvShows.png"),
                 dirImages("animes.png"),
                 dirImages("animes.png"),
                 ]
    listAction = ['readHTML',
                  'readHTML',
                  'readHTML',
                  'readHTML',
                  'readHTML',
                  'readHTML',
                  ]
    for type, url, icon, action in zip(listTypes, listUrl, listIcons, listAction):
        items.append({'label': type,
                      'path': plugin.url_for(action, url=url, showSeasons='True'),
                      'thumbnail': icon,
                      'properties': {'fanart_image': settings.fanart},
                      })
    items.append({'label': settings.string(32016),
                  'path': plugin.url_for('configuration'),
                  'thumbnail': dirImages("settings.png"),
                  'properties': {'fanart_image': settings.fanart}
                  })
    items.append({'label': settings.string(32017),
                  'path': plugin.url_for('help'),
                  'thumbnail': dirImages("help.png"),
                  'properties': {'fanart_image': settings.fanart}
                  })
    return items


# Search Menu
@plugin.route("/searchMenu/")
def searchMenu():
    items = [
        {'label': settings.string(32195),
         'path': plugin.url_for('search'),
         'thumbnail': dirImages("search.png"),
         'properties': {'fanart_image': settings.fanart}
         }]
    items.extend(read())
    return items


# Search
@plugin.route('/search/')
def search():
    query = settings.dialog.input(settings.string(32190))
    url = "/search?q=%s" % query.replace(" ", "%20")
    response = settings.dialog.yesno(settings.name, settings.string(32193))
    if response:
        name = ''
        while name is '':
            name = settings.dialog.input(plugin.get_string(32192)).title()
        storage.database[name] = (url, False)  # url, isSubscribed
        storage.save()
    return readHTML(url, showSeasons='False')


# Settings
@plugin.route('/configuration/')
def configuration():
    settings.settings.openSettings()
    settings.settings = Settings()


####################################################
@plugin.route('/readHTML/<url>/<showSeasons>', name="readHTML")
def readHTML(url="", showSeasons='True'):
    # First Page
    information = plugin.get_storage('information')
    information.clear()
    return nextPage(url=url, showSeasons=showSeasons)


@plugin.route('/nextPage/<url>/<page>/<showSeasons>', name="nextPage")
def nextPage(url="", page="1", showSeasons='True'):
    urlSearch = settings.value["urlAddress"] + url + '&p=%s' % (int(page) - 1)

    # Read
    settings.log(urlSearch)
    response = browser.get(urlSearch, verify=False)
    soup = bs4.BeautifulSoup(response.text)

    # Storage information
    source = plugin.get_storage('source')
    source['url'] = url
    source['page'] = int(page)

    # Titles and Urls
    titles = []
    urlSources = []
    links = soup.select("dt a")
    for a in links:
        titles.append(a.get("title", a.text))
        hash = a["href"].replace("/", "")
        torcache = 'as=http://torcache.net/torrent/%s.torrent' % hash
        trackers = 'tr=udp://open.demonii.com:1337&tr=udp://tracker.coppersurfer.tk:6969&tr=udp://tracker.leechers-paradise.org:6969&tr=udp://tracker.openbittorrent.com:80&tr=udp://exodus.desync.com:6969&tr=udp://tracker.pomf.se&tr=udp://tracker.blackunicorn.xyz:6969&tr=udp://tracker.publicbt.com:80&tr=udp://pow7.com:80/announce'
        magnet = 'magnet:?xt=urn:btih:%s&%s&%s' % (hash, torcache, trackers)
        urlSources.append(magnet)

    # Create Menu
    createMenu(titles, urlSources)
    items = menu1(showSeasons=showSeasons)

    # Next page
    items.append({'label': "[B]" + settings.string(32191) + "[/B]",
                  'path': plugin.url_for('nextPage', url=url, page=int(page) + 1, showSeasons=showSeasons),
                  'thumbnail': dirImages("next11.png"),
                  'info': {'episode': 9999},
                  'properties': {'fanart_image': settings.fanart}
                  })

    if __name__ == '__main__':
        return plugin.finish(items=items, view_mode=settings.value['viewMode'],
                             sort_methods=[24, 'title'])
    else:
        return items


###################################################
############## COMMON NOT TO CHANGE ###############
###################################################
@plugin.route('/play/<url>')
def play(url):
    settings.log(url)
    magnet = url
    uri_string = quote_plus(getPlayableLink(uncodeName(magnet)))
    if settings.value["plugin"] == 'Quasar':
        link = 'plugin://plugin.video.quasar/play?uri=%s' % uri_string
    elif settings.value["plugin"] == 'Pulsar':
        link = 'plugin://plugin.video.pulsar/play?uri=%s' % uri_string
    elif settings.value["plugin"] == 'KmediaTorrent':
        link = 'plugin://plugin.video.kmediatorrent/play/%s' % uri_string
    elif settings.value["plugin"] == "Torrenter":
        link = 'plugin://plugin.video.torrenter/?action=playSTRM&url=' + uri_string + \
               '&not_download_only=True'
    elif settings.value["plugin"] == "YATP":
        link = 'plugin://plugin.video.yatp/?action=play&torrent=' + uri_string
    else:
        link = 'plugin://plugin.video.xbmctorrent/play/%s' % uri_string
    # play media
    settings.debug("PlayMedia(%s)" % link)
    xbmc.executebuiltin("PlayMedia(%s)" % link)
    xbmc.executebuiltin('Dialog.Close(all, true)')


@plugin.route('/help/')
def help():
    textViewer(plugin.get_string(32000), once=False)


@plugin.route('/unsubscribe/<key>')
def unsubscribe(key=""):
    storage.database[key] = (storage.database[key][0], False)
    storage.save()


@plugin.route('/subscribe/<key>/<url>')
def subscribe(key="", url=""):
    storage.add(key, (url, True), safe=False)
    storage.save()
    importAll(url)


@plugin.route('/importOne/<title>')
def importOne(title=""):
    information = plugin.get_storage('information')
    info = information[title][0]
    integration(titles=[title], magnets=[info.fileName], id=[info.id], typeVideo=[info.typeVideo], silence=True)


@plugin.route('/importAll/<url>')
def importAll(url=""):
    items = readHTML(url, showSeasons="False")  # only to create information
    information = plugin.get_storage('information')
    titles = []
    fileNames = []
    typeVideos = []
    ids = []
    for title in information:
        temp, level1 = information[title]
        for season in level1:
            level2 = level1[season]
            for episode in level2:
                temp, level3 = level2[episode]
                for info in level3:
                    ids.append(info.id)
                    titles.append(info.infoTitle["title"])
                    fileNames.append(info.fileName)
                    typeVideos.append(info.typeVideo)
    integration(titles=titles, magnets=fileNames, id=ids, typeVideo=typeVideos, silence=True)


@plugin.route('/rebuilt/<url>')
def rebuilt(url):
    overwrite = settings.value["overwrite"]  # save the user's value
    settings.value["overwrite"] = "true"  # force to overwrite
    importAll(url)
    settings.value["overwrite"] = overwrite  # return the user's value
    settings.log(url + " was rebuilt")


@plugin.route('/remove/<key>')
def remove(key=""):
    if settings.dialog.yesno(settings.cleanName, plugin.get_string(32006) % key):
        storage.remove(key, safe=False)
        storage.save()
        'XBMC.Container.Update(%s)' % plugin.url_for('/search/')


@plugin.route('/modify/<key>')
def modify(key):
    selection = settings.dialog.input(plugin.get_string(32007), storage.database[key][0])
    newKey = ''
    while newKey is '':
        newKey = settings.dialog.input(plugin.get_string(32008), key).title()
    storage.database[newKey] = (selection, storage.database[key][1])
    if newKey != key: storage.remove(key, safe=False)
    storage.save()
    'XBMC.Container.Update(%s)' % plugin.url_for('/search/')


def read():
    # list storage search
    items = []
    for key in sorted(storage.database):  # sort the dictionnary
        (url, isIntegrated) = storage.database[key]
        settings.debug(url)
        settings.debug(isIntegrated)
        if isIntegrated:
            importInfo = (plugin.get_string(32001),
                          'XBMC.Container.Update(%s)' % plugin.url_for('unsubscribe', key=key))
        else:
            importInfo = (plugin.get_string(32002),
                          'XBMC.Container.Update(%s)' % plugin.url_for('subscribe', key=key, url=url))
        items.append({'label': "- " + key,
                      'path': plugin.url_for('readHTML', url=url, showSeasons='True'),
                      'thumbnail': dirImages(key[0] + '.png'),
                      'properties': {'fanart_image': settings.fanart},
                      'context_menu': [importInfo,
                                       (plugin.get_string(32187),
                                        'XBMC.Container.Update(%s)' % plugin.url_for('remove', key=key)),
                                       (plugin.get_string(32188),
                                        'XBMC.Container.Update(%s)' % plugin.url_for('modify', key=key)),
                                       (plugin.get_string(32045),
                                        'XBMC.Container.Update(%s)' % plugin.url_for('rebuilt', url=url))
                                       ]
                      })
    return items


# Create the storage from titles and urls
def createMenu(titles=[], urlSources=[], typeVideo=""):
    information = plugin.get_storage('information')
    page = plugin.get_storage('page')
    page.clear()
    for title, urlSource in zip(titles, urlSources):
        # it gets all the information from the title and url
        info = UnTaggle(title, urlSource, typeVideo=typeVideo)  # Untaggle
        temp, level1 = information.get(info.infoTitle["folder"], ("", {}))  # infoLabels, dictionnary seasons
        level2 = level1.get(str(info.season), {})  # dictionnary episodes
        temp, level3 = level2.get(str(info.episode), ("", []))  # list info for that episode
        level3.append(info)  # add new info video
        level2[str(info.episode)] = (info, level3)
        level1[str(info.season)] = level2
        information[info.infoTitle["folder"]] = (info, level1)
        page[info.infoTitle["folder"]] = (info, level1)


def menu0():  # create the menu for first level
    information = plugin.get_storage('page')
    source = plugin.get_storage('source')

    items = []
    typeVideo = "MOVIE"
    for title in information.keys():
        info, level1 = information.get(title, ("", {}))  # infoLabels, dictionnary seasons
        typeVideo = info.typeVideo
        try:
            settings.log(info.fileName)
            items.append({'label': info.infoTitle["folder"],
                          'path': plugin.url_for('readHTML', url=info.fileName, showSeasons='False'),
                          'thumbnail': info.infoLabels.get('cover_url', settings.icon),
                          'properties': {'fanart_image': info.fanart},
                          'info': info.infoLabels,
                          })
        except:
            pass
    # main
    if __name__ == '__main__':
        plugin.set_content("movies" if typeVideo == "MOVIE" else "tvshows")
    return items


@plugin.route('/menu1')
def menu1(showSeasons='True'):  # create the menu for first level
    information = plugin.get_storage('page')
    source = plugin.get_storage('source')

    items = []
    typeVideo = "MOVIE"
    if len(information.keys()) == 1:
        items = menu2(information.keys()[0], showSeasons=showSeasons)
    else:
        for title in information.keys():
            info, level1 = information.get(title, ("", {}))  # infoLabels, dictionnary seasons
            typeVideo = info.typeVideo
            if typeVideo == 'MOVIE':
                extraInfo = ("Extended Info",
                             'XBMC.RunScript(script.extendedinfo,info=extendedinfo,imdb_id=%s)' % info.imdb_id)
            else:
                extraInfo = ("Extended Info",
                             'XBMC.RunScript(script.extendedinfo,info=extendedtvinfo,imdb_id=%s)' % info.imdb_id)
            try:
                items.append({'label': info.infoTitle["folder"],
                              'path': plugin.url_for('menu2', title=info.infoTitle["folder"]),
                              'thumbnail': info.infoLabels.get('cover_url', settings.icon),
                              'properties': {'fanart_image': info.fanart},
                              'info': info.infoLabels,
                              'context_menu': [extraInfo],
                              })
            except:
                pass
        # main
        if __name__ == '__main__':
            plugin.set_content("movies" if typeVideo == "MOVIE" else "tvshows")
    return items


@plugin.route('/menu2/<title>')
def menu2(title="", showSeasons='True'):  # create the menu for second level
    information = plugin.get_storage('information')
    items = []
    typeVideo = "MOVIE"
    info, level1 = information.get(title, ("", {}))  # infoLabels, dictionnary seasons
    if len(level1) == 1:
        items = menu3(title, level1.keys()[0])
    else:
        for season in level1.keys():
            if showSeasons == 'True':
                typeVideo = info.typeVideo
                if typeVideo == 'MOVIE':
                    extraInfo = ("Extended Info",
                                 'XBMC.RunScript(script.extendedinfo,info=extendedinfo,imdb_id=%s)' % info.imdb_id)
                else:
                    extraInfo = ("Extended Info",
                                 'XBMC.RunScript(script.extendedinfo,info=seasoninfo,tvshow=%s, season=%s)' % (
                                     info.infoTitle['cleanTitle'], season))
                try:
                    items.append({'label': "Season %s" % season,
                                  'path': plugin.url_for('menu3', title=title, season=season),
                                  'thumbnail': info.infoLabels.get('cover_url', settings.icon),
                                  'properties': {'fanart_image': info.fanart},
                                  'info': info.infoLabels,
                                  'context_menu': [extraInfo],
                                  })
                except:
                    pass
            else:
                items.extend(menu3(title=title, season=season))
        # main
        if __name__ == '__main__':
            plugin.set_content("movies" if typeVideo == "MOVIE" else "tvshows")
    return items


@plugin.route('/menu3/<title>/<season>')
def menu3(title="", season=""):  # create the menu for third level
    information = plugin.get_storage('information')
    items = []
    typeVideo = "MOVIE"
    temp, level1 = information.get(title, ("", {}))  # infoLabels, dictionnary seasons
    level2 = level1[season]
    if len(level2) == 1:
        items = menu4(title, season, level2.keys()[0])
    else:
        for episode in level2.keys():
            info, level3 = level2[episode]  # dictionnary episodes
            typeVideo = info.typeVideo
            if typeVideo == 'MOVIE':
                extraInfo = ("Extended Info",
                             'XBMC.RunScript(script.extendedinfo,info=extendedinfo,imdb_id=%s)' % info.imdb_id)
            else:
                extraInfo = ("Extended Info",
                             'XBMC.RunScript(script.extendedinfo,info=extendedepisodeinfo,tvshow=%s, season=%s, episode=%s)' % (
                                 info.infoTitle['cleanTitle'], season, episode))
            try:
                items.append({'label': info.infoTitle["title"] + info.titleEpisode,
                              'path': plugin.url_for('menu4', title=title, season=season, episode=episode),
                              'thumbnail': info.cover,
                              'properties': {'fanart_image': info.fanart},
                              'info': info.info,
                              'context_menu': [extraInfo],
                              })
            except:
                pass
        # main
        if __name__ == '__main__':
            plugin.set_content("movies" if typeVideo == "MOVIE" else "episodes")
    return items


@plugin.route('/menu4/<title>/<season>/<episode>')
def menu4(title="", season="", episode=""):  # create the menu for last level
    information = plugin.get_storage('information')
    items = []
    typeVideo = "MOVIE"
    temp, level1 = information.get(title, ("", {}))  # infoLabels, dictionnary seasons
    level2 = level1[season]
    temp, level3 = level2[episode]
    for info in level3:
        typeVideo = info.typeVideo
        if typeVideo == 'MOVIE':
            extraInfo = ("Extended Info",
                         'XBMC.RunScript(script.extendedinfo,info=extendedinfo,imdb_id=%s)' % info.imdb_id)
        else:
            extraInfo = ("Extended Info",
                         'XBMC.RunScript(script.extendedinfo,info=extendedepisodeinfo,tvshow=%s, season=%s, episode=%s)' % (
                             info.infoTitle['cleanTitle'], season, episode))
        try:
            items.append({'label': info.label,
                          'path': plugin.url_for('play', url=info.fileName),
                          'thumbnail': info.cover,
                          'properties': {'fanart_image': info.fanart},
                          'info': info.info,
                          'stream_info': info.infoStream,
                          'is_playable': play,
                          'context_menu': [
                              (plugin.get_string(32009),
                               'XBMC.RunPlugin(%s)' % plugin.url_for('importOne', title=title)),
                              extraInfo
                          ]
                          })
        except:
            pass
        # main
        if __name__ == '__main__':
            plugin.set_content("movies" if typeVideo == "MOVIE" else "episodes")
    return items


if __name__ == '__main__':
    try:
        plugin.run()
    except:
        pass
