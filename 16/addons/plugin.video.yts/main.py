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
def quality(keyword="0", isSearch="False"):
    textViewer(settings.string(32000), once=True)
    items = []
    if isSearch == 'False':
        items = [
            {'label': settings.string(32194),
             'path': plugin.url_for('searchMenu'),
             'thumbnail': dirImages("search.png"),
             'properties': {'fanart_image': settings.fanart}
             }]
    listTypes = ['All',
                 '720p',
                 '1080p',
                 '3D',
                 ]
    listUrl = ['all',
               '720p',
               '1080p',
               '3d',
               ]
    listIcons = [dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 ]
    listAction = ['genre',
                  'genre',
                  'genre',
                  'genre',
                  ]
    for type, url, icon, action in zip(listTypes, listUrl, listIcons, listAction):
        items.append({'label': type,
                      'path': plugin.url_for(action, keyword=keyword, quality=url, isSearch=isSearch),
                      'thumbnail': icon,
                      'properties': {'fanart_image': settings.fanart},
                      })
    if isSearch == 'False':
        items.append({'label': "[B]Help[/B]",
                      'path': plugin.url_for('help'),
                      'thumbnail': dirImages("help.png"),
                      'properties': {'fanart_image': settings.fanart}
                      })
    return items


@plugin.route('/genre/<keyword>/<quality>/<isSearch>')
def genre(keyword="0", quality="all", isSearch="False"):
    list = ["all", "action", "adventure", "animation", "biography",
            "comedy", "crime", "documentary", "drama", "family",
            "fantasy", "film-noir", "game-show", "history", "horror",
            "music", "musical", "mystery", "news", "reality-tv", "romance",
            "sci-fi", "sport", "talk-show", "thriller", "war", "western",
            ]
    items = []
    for item in list:
        items.append(
                {'label': item.title(),
                 'path': plugin.url_for('rating', keyword=keyword, quality=quality, genre=item, isSearch=isSearch),
                 'thumbnail': dirImages("movies.png"),
                 'properties': {'fanart_image': settings.fanart}
                 })
    return items


@plugin.route('/rating/<keyword>/<quality>/<genre>/<isSearch>')
def rating(keyword="0", quality="all", genre="all", isSearch="False"):
    list = ["all", "9", "8", "7", "6", "5", "4", "3", "2", "1",
            ]
    items = []
    for item in list:
        items.append(
                {'label': (item + '+').replace('all+', 'All'),
                 'path': plugin.url_for('orderBy', keyword=keyword, quality=quality, genre=genre, rating=item,
                                        isSearch=isSearch),
                 'thumbnail': dirImages("movies.png"),
                 'properties': {'fanart_image': settings.fanart}
                 })
    return items


@plugin.route('/orderBy/<keyword>/<quality>/<genre>/<rating>/<isSearch>')
def orderBy(keyword="0", quality="all", genre="all", rating="all", isSearch="False"):
    list = ["latest", "oldest", "seeds", "peers", "year", "rating", "likes", "alphabetical", "downloads",
            ]
    items = []
    for item in list:
        items.append(
                {'label': item.title(),
                 'path': plugin.url_for('readHTML', keyword=keyword, quality=quality, genre=genre, rating=rating,
                                        order_by=item, isSearch=isSearch),
                 'thumbnail': dirImages("movies.png"),
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
    if query == "":
        query = "0"
    return quality(keyword=query, isSearch="True")


####################################################
@plugin.route('/readHTML/<keyword>/<quality>/<genre>/<rating>/<order_by>/<isSearch>', name="readHTML")
def readHTML(keyword="0", quality="all", genre="all", rating="0", order_by="latest", isSearch="False"):
    # First Page
    information = plugin.get_storage('information')
    information.clear()
    return nextPage(keyword=keyword, quality=quality, genre=genre, rating=rating, order_by=order_by, isSearch=isSearch)


@plugin.route('/nextPage/<keyword>/<quality>/<genre>/<rating>/<order_by>/<page>/<isSearch>', name="nextPage")
def nextPage(keyword="0", quality="all", genre="all", rating="0", order_by="latest", page="1", isSearch="False",
             showSeasons='True'):
    urlSearch = settings.value['urlAddress']
    rating = rating.replace("all", "0")

    # Reading the _token
    response = ""
    if page == "1":
        response = browser.get(urlSearch)
        soup = bs4.BeautifulSoup(response.text)
        itemToken = soup.select("div#mobile-search-input input")
        token = itemToken[0]["value"]  # hidden token

        # Read
        settings.log(urlSearch)
        payload = {
            "keyword": keyword if keyword != "0" else "",
            "_token": token,
            "quality": quality,
            "genre": genre,
            "rating": rating,
            "order_by": order_by,
        }
        settings.log(payload)
        response = browser.post(urlSearch + "/search-movies", data=payload)
    else:
        # read the result
        urlSearch = settings.value['urlAddress'] + "/browse-movies/%s/%s/%s/%s/%s?page=%s" % (
            keyword, quality, genre, rating, order_by, page)
        urlSearch = urlSearch.replace("?page=1", "")
        settings.log(urlSearch)
        response = browser.get(urlSearch)
    soup = bs4.BeautifulSoup(response.text)

    # Save search
    if (isSearch == "True" and page == "1"):
        response = settings.dialog.yesno(settings.name, settings.string(32193))
        if response:
            name = ''
            while name is '':
                name = settings.dialog.input(plugin.get_string(32192)).title()
            storage.database[name] = {
                "keyword": keyword, "quality": quality, "genre": genre, "rating": rating, "order_by": order_by,
                "isIntegrated": "False"}  # parameters
            storage.save()

    # Titles and Urls
    titles = []
    urlSources = []
    links = soup.select("div.browse-movie-bottom")
    for div in links:
        baseTitle = div.a.text  # title
        aList = div.select("div a")
        for a in aList:
            titles.append(baseTitle + ' ' + a.text)
            urlSources.append(a["href"])

    # Create Menu
    createMenu(titles, urlSources)
    items = menu1(showSeasons=showSeasons)

    # Next page
    items.append({'label': "[B]" + settings.string(32191) + "[/B]",
                  'path': plugin.url_for('nextPage', keyword=keyword, quality=quality, genre=genre, rating=rating,
                                         order_by=order_by, page=int(page) + 1, isSearch=isSearch),
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
    # magnet = getPlayableLink(url)
    magnet = url
    # Set-up the plugin
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


@plugin.route('/subscribe/<key>/<keyword>/<quality>/<genre>/<rating>/<order_by>')
def subscribe(key="", keyword="0", quality="all", genre="all", rating="0", order_by="latest", isIntegrated="True"):
    parameters = {"keyword": keyword, "quality": quality, "genre": genre, "rating": rating, "order_by": order_by,
                  "isIntegrated": isIntegrated}
    storage.add(key, parameters, safe=False)
    storage.save()
    importAll(keyword=keyword, quality=quality, genre=genre, rating=rating, order_by=order_by)


@plugin.route('/importOne/<title>')
def importOne(title=""):
    information = plugin.get_storage('information')
    info = information[title][0]
    integration(titles=[title], magnets=[info.fileName], id=[info.id], typeVideo=[info.typeVideo], silence=True)


@plugin.route('/importAll/<keyword>/<quality>/<genre>/<rating>/<order_by>')
def importAll(keyword="0", quality="all", genre="all", rating="0", order_by="latest"):
    items = readHTML(keyword=keyword, quality=quality, genre=genre, rating=rating, order_by=order_by,
                     showSeasons="False")  # only to create information
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


@plugin.route('/rebuilt/<keyword>/<quality>/<genre>/<rating>/<order_by>')
def rebuilt(keyword="0", quality="all", genre="all", rating="0", order_by="latest"):
    overwrite = settings.value["overwrite"]  # save the user's value
    settings.value["overwrite"] = "True"  # force to overwrite
    importAll(keyword=keyword, quality=quality, genre=genre, rating=rating, order_by=order_by)
    settings.value["overwrite"] = overwrite  # return the user's value
    settings.log(keyword + " was rebuilt")


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
        parameters = storage.database[key]
        settings.debug(parameters)
        if parameters["isIntegrated"] == "True":
            importInfo = (plugin.get_string(32001),
                          'XBMC.Container.Update(%s)' % plugin.url_for('unsubscribe', key=key))
        else:
            importInfo = (plugin.get_string(32002),
                          'XBMC.Container.Update(%s)' % plugin.url_for('subscribe', key=key,
                                                                       keyword=parameters["keyword"],
                                                                       quality=parameters["quality"],
                                                                       genre=parameters["genre"],
                                                                       rating=parameters["rating"],
                                                                       order_by=parameters["order_by"]))
        items.append({'label': "- " + key,
                      'path': plugin.url_for('readHTML', keyword=parameters["keyword"], quality=parameters["quality"],
                                             genre=parameters["genre"], rating=parameters["rating"],
                                             order_by=parameters["order_by"], isSearch="False"),
                      'thumbnail': dirImages(key[0] + '.png'),
                      'properties': {'fanart_image': settings.fanart},
                      'context_menu': [importInfo,
                                       (plugin.get_string(32187),
                                        'XBMC.Container.Update(%s)' % plugin.url_for('remove', key=key)),
                                       (plugin.get_string(32188),
                                        'XBMC.Container.Update(%s)' % plugin.url_for('modify', key=key)),
                                       (plugin.get_string(32045),
                                        'XBMC.Container.Update(%s)' % plugin.url_for('rebuilt',
                                                                                     keyword=parameters["keyword"],
                                                                                     quality=parameters["quality"],
                                                                                     genre=parameters["genre"],
                                                                                     rating=parameters["rating"],
                                                                                     order_by=parameters["order_by"]))
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
