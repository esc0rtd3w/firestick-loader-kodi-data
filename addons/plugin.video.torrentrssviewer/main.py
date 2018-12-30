# coding: utf-8
# Main Addon
__author__ = 'mancuniancol'

from xbmcswift2 import Plugin
from tools2 import *
import feedparser

storage = Storage(settings.storageName, type="dict", eval=True)
plugin = Plugin()


###############################
###  MENU    ##################
###############################

@plugin.route('/')
def index():
    textViewer(plugin.get_string(32000), once=True)
    items = [
        {'label': plugin.get_string(32005),
         'path': plugin.url_for('add'),
         'thumbnail': "DefaultAddSource.png",
         'properties': {'fanart_image': settings.fanart}
         }
    ]
    items.extend(read())
    return items


@plugin.route('/remove/<name>')
def remove(name):
    if settings.dialog.yesno(settings.cleanName, plugin.get_string(32006) % name):
        storage.remove(name)
        storage.save()


@plugin.route('/modify/<name>')
def modify(name):
    selection = settings.dialog.input(plugin.get_string(32007), storage.database[name][0])
    newName = ''
    while newName is '':
        newName = settings.dialog.input(plugin.get_string(32008), name).title()
    storage.database[newName] = (selection, storage.database[name][1])
    if newName != name: storage.remove(name)
    storage.save()


@plugin.route('/add')
def add():
    selection = settings.dialog.input(plugin.get_string(32007))
    name = ''
    while name is '':
        name = settings.dialog.input(plugin.get_string(32008)).title()
    storage.database[name] = (selection, False)
    storage.save()


# read the information from rss url
@plugin.route('/readRss/<url>/')
def readRss(url):
    items = []
    titlesMovie, magnetsMovie, titlesShow, magnetsShow, titlesAnime, magnetsAnime = _readRss(url)
    movies = plugin.get_storage('movies')
    shows = plugin.get_storage('shows')
    animes = plugin.get_storage('animes')
    movies.clear()
    shows.clear()
    animes.clear()

    if len(titlesMovie) > 0:
        movies.update({
            'titles': titlesMovie,
            'magnets': magnetsMovie
        })
        items.append(
            {'label': plugin.get_string(32022),
             'path': plugin.url_for('readList', type="Movie"),
             'thumbnail': dirImages("M.png"),
             'properties': {'fanart_image': settings.fanart}
             }

        )
    if len(titlesShow) > 0:
        shows.update({
            'titles': titlesShow,
            'magnets': magnetsShow
        })
        items.append(
            {'label': plugin.get_string(32023),
             'path': plugin.url_for('readList', type="Show"),
             'thumbnail': dirImages("T.png"),
             'properties': {'fanart_image': settings.fanart}
             }

        )
    if len(titlesAnime) > 0:
        animes.update({
            'titles': titlesAnime,
            'magnets': magnetsAnime,
            'type': "Anime"
        })
        items.append(
            {'label': plugin.get_string(32024),
             'path': plugin.url_for('readList', type="Anime"),
             'thumbnail': dirImages("A.png"),
             'properties': {'fanart_image': settings.fanart}
             }
        )
    return items


### Read the list to get each item and its information
@plugin.route('/readList/<type>')
def readList(type):
    movies = plugin.get_storage('movies')
    shows = plugin.get_storage('shows')
    animes = plugin.get_storage('animes')
    info = {}
    info['titles'] = ""
    info['magnets'] = ""
    if type == "Movie":
        plugin.set_content("movies")
        info = movies
    elif type == "Show":
        plugin.set_content("episodes")
        info = shows
    elif type == "Anime":
        plugin.set_content("episodes")
        info = animes
    items = []
    for (title, magnet) in zip(info['titles'], info['magnets']):
        info = UnTaggle(title)  # it gets all the information from the title and url
        try:
            items.append({'label': info.label,
                          'path': plugin.url_for('play', magnet=normalize(magnet)),
                          'thumbnail': info.cover,
                          'properties': {'fanart_image': info.fanart},
                          'info': info.info,
                          'stream_info': info.infoStream,
                          'context_menu': [
                              (plugin.get_string(32009),
                               'XBMC.RunPlugin(%s)' % plugin.url_for('importOne', title=title,
                                                                     magnet=normalize(magnet)))
                          ]
                          })
        except:
            pass
    return plugin.finish(items=items, view_mode=settings.value['viewMode'])


@plugin.route('/play/<magnet>')
def play(magnet):
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


@plugin.route('/importAll/<name>')
def importAll(name):
    url = storage.database[name][0]
    storage.database[name] = (url, True)
    storage.save()
    titlesMovie, magnetsMovie, titlesShow, magnetsShow, titlesAnime, magnetsAnime = _readRss(url)
    settings.debug("***************************************")
    settings.debug(titlesMovie)
    settings.debug(magnetsMovie)
    settings.debug(titlesShow)
    settings.debug(magnetsShow)
    settings.debug(titlesAnime)
    settings.debug(magnetsAnime)
    settings.debug("***************************************")
    if len(titlesMovie) > 0:
        integration(titles=titlesMovie, magnets=magnetsMovie, typeList='MOVIE',
                    folder=settings.movieFolder, silence=True)
    if len(titlesShow) > 0:
        integration(titles=titlesShow, magnets=magnetsShow, typeList='SHOW',
                    folder=settings.showFolder, silence=True)
    if len(titlesAnime) > 0:
        integration(titles=titlesAnime, magnets=magnetsAnime, typeList='ANIME',
                    folder=settings.animeFolder, silence=True)


@plugin.route('/importOne/<title>/<magnet>')
def importOne(title, magnet):
    info = formatTitle(title)
    if 'MOVIE' in info['type']:
        integration(titles=[title], magnets=[magnet], typeList='MOVIE',
                    folder=settings.movieFolder, silence=True)
    if 'SHOW' in info['type']:
        integration(titles=[title], magnets=[magnet], typeList='SHOW',
                    folder=settings.showFolder, silence=True)
    if 'ANIME' in info['type']:
        integration(titles=[title], magnets=[magnet], typeList='ANIME',
                    folder=settings.animeFolder, silence=True)


@plugin.route('/unsubscribe/<name>')
def unsubscribe(name):
    storage.database[name] = (storage.database[name][0], False)
    storage.save()


@plugin.route('/rebuilt/<name>')
def rebuilt(name):
    url = storage.database[name][0]
    overwrite = settings.value["overwrite"]  # save the user's value
    settings.value["overwrite"] = "true"  # force to overwrite
    titlesMovie, magnetsMovie, titlesShow, magnetsShow, titlesAnime, magnetsAnime = _readRss(url)
    settings.debug(titlesMovie)
    settings.debug(magnetsMovie)
    settings.debug(titlesShow)
    settings.debug(magnetsShow)
    settings.debug(titlesAnime)
    settings.debug(magnetsAnime)
    if len(titlesMovie) > 0:
        integration(titles=titlesMovie, magnets=magnetsMovie, typeList='MOVIE',
                    folder=settings.movieFolder, silence=True)
    if len(titlesShow) > 0:
        integration(titles=titlesShow, magnets=magnetsShow, typeList='SHOW',
                    folder=settings.showFolder, silence=True)
    if len(titlesAnime) > 0:
        integration(titles=titlesAnime, magnets=magnetsAnime, typeList='ANIME',
                    folder=settings.animeFolder, silence=True)
    settings.value["overwrite"] = overwrite  # return the user's value


###############################
###  FONCTIONS    #############
###############################
# read the url list
def read():
    # list of rss available
    items = []
    for name in sorted(storage.database):  # sort the dictionnary
        (RSS, isIntegrated) = storage.database[name]
        settings.debug(RSS)
        settings.debug(isIntegrated)
        if isIntegrated:
            importInfo = (plugin.get_string(32001),
                          'XBMC.Container.Update(%s)' % plugin.url_for('unsubscribe', name=name))
        else:
            importInfo = (plugin.get_string(32002),
                          'XBMC.Container.Update(%s)' % plugin.url_for('importAll', name=name))

        items.append({'label': "- " + name + ": " + RSS if settings.value["viewUrl"] == "true" else "- " + name,
                      'path': plugin.url_for('readRss', url=RSS) if RSS <> "" else plugin.url_for('modify', name=name),
                      'thumbnail': dirImages(name[0] + '.png'),
                      'properties': {'fanart_image': settings.fanart},
                      'context_menu': [
                          (plugin.get_string(32003), 'XBMC.Container.Update(%s)' % plugin.url_for('remove', name=name)),
                          (plugin.get_string(32004), 'XBMC.Container.Update(%s)' % plugin.url_for('modify', name=name)),
                          importInfo,
                          (plugin.get_string(32045), 'XBMC.Container.Update(%s)' % plugin.url_for('rebuilt', name=name))
                      ]
                      })
    return items


def _readRss(url):
    from socket import setdefaulttimeout
    magnetsMovie = []
    titlesMovie = []
    magnetsShow = []
    titlesShow = []
    magnetsAnime = []
    titlesAnime = []
    if url is not '':
        settings.log(url)
        setdefaulttimeout(10)
        feeds = feedparser.parse(url)
        for entry in feeds.entries:
            settings.debug(entry)
            isMagnet = False
            for key in entry.keys():
                if "magnet" in key:
                    isMagnet = True
                    tag = key
                    break
            if isMagnet:
                value = entry[tag]
            else:
                for link in entry.links:
                    value = link.href  # Taking the last link
            entry.title = entry.title.replace('/', '')
            info = formatTitle(entry.title.replace('/', ''))
            if 'MOVIE' in info['type']:
                titlesMovie.append(entry.title)
                magnetsMovie.append(value)
            if 'SHOW' in info['type']:
                titlesShow.append(entry.title)
                magnetsShow.append(value)
            if 'ANIME' in info['type']:
                titlesAnime.append(entry.title)
                magnetsAnime.append(value)
    return titlesMovie, magnetsMovie, titlesShow, magnetsShow, titlesAnime, magnetsAnime


if __name__ == '__main__':
    plugin.run()
