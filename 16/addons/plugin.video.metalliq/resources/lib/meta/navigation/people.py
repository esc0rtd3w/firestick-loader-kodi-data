import meta.navigation.movies
import meta.navigation.tvshows
from meta import plugin, import_tmdb
from trakt import trakt
from xbmcswift2 import xbmcgui
from meta.utils.text import to_utf8
from language import get_string as _

import_tmdb()


@plugin.route('/people/list/show/<id>/<source>/<fanart>')
def people_list_show_people(id, source, fanart):
    items = []
    try:
        if source == "imdb":
            people = trakt.get_show_people(id)
        else:
            xbmcgui.Dialog().ok("Error", "No cast info found")
            return plugin.finish(items=[])
    except:
        xbmcgui.Dialog().ok("Error", "No cast info found")
        return plugin.finish(items=[])
    if "cast" in people:
        for actor in people["cast"]:
            context_menu = [
                (
                    "Convert to bob_xml",
                    "RunPlugin({0})".format(
                        plugin.url_for("bob_convert_person_to_xml", trakt_id=actor["person"]["ids"]["trakt"]))
                )
            ]
            image = get_person_artwork(actor)
            label = "{0} ({1})".format(to_utf8(actor["person"]["name"]), to_utf8(actor["character"]))
            info = actor["person"]["biography"]
            items.append({'label': label,
                          'path': plugin.url_for("people_list_person_select", id=actor["person"]["ids"]["trakt"],
                                                 name=to_utf8(actor["person"]["name"])),
                          'info': info,
                          'thumbnail': image,
                          'poster': image,
                          'context_menu': context_menu,
                          'icon': "DefaultVideo.png",
                          'properties': {'fanart_image': fanart},
                          })
        return plugin.finish(items=items)


@plugin.route('/people/list/movie/<id>/<source>/<fanart>')
def people_list_movie_people(id, source, fanart):
    items = []
    try:
        if source == "imdb":
            people = trakt.get_movie_people(id)
        elif source == "tmdb":
            ids = trakt.find_trakt_ids("tmdb", id)
            if ids:
                people = trakt.get_movie_people(ids["imdb"])
            else:
                xbmcgui.Dialog().ok("Error", "No cast info found")
                return plugin.finish(items=[])
        else:
            xbmcgui.Dialog().ok("Error", "No cast info found")
            return plugin.finish(items=[])
    except:
        xbmcgui.Dialog().ok("Error", "No cast info found")
        return plugin.finish(items=[])
    if "cast" in people:
        for actor in people["cast"]:
            context_menu = [
                (
                    "Convert to bob_xml",
                    "RunPlugin({0})".format(
                        plugin.url_for("bob_convert_person_to_xml", trakt_id=actor["person"]["ids"]["trakt"]))
                )
            ]
            image = get_person_artwork(actor)
            label = "{0} ({1})".format(to_utf8(actor["person"]["name"]), to_utf8(actor["character"]))
            info = actor["person"]["biography"]
            items.append({'label': label,
                          'path': plugin.url_for("people_list_person_select", id=actor["person"]["ids"]["trakt"],
                                                 name=to_utf8(actor["person"]["name"])),
                          'info': info,
                          'thumbnail': image,
                          'poster': image,
                          'context_menu': context_menu,
                          'icon': "DefaultVideo.png",
                          'properties': {'fanart_image': fanart},
                          })
        return plugin.finish(items=items)
    else:
        xbmcgui.Dialog().ok("Error", "No cast info found")


@plugin.route('/people/<id>/<name>/select')
def people_list_person_select(id, name):
    selection = xbmcgui.Dialog().select("show {0}'s:".format(name), ["movies", "shows"])
    if selection == 0:
        people_list_person_movies(id)
    elif selection == 1:
        people_list_person_shows(id)


@plugin.route('/people/<id>/shows')
def people_list_person_shows(id):
    shows = trakt.get_person_shows(id)
    if shows["cast"]:
        meta.navigation.tvshows.list_trakt_items(shows["cast"], 1, 1)
    else:
        xbmcgui.Dialog().ok("Error", "No shows found")


@plugin.route('/people/<id>/movies')
def people_list_person_movies(id):
    movies = trakt.get_person_movies(id)
    if movies["cast"]:
        meta.navigation.movies.list_trakt_movies_plain(movies["cast"])
    else:
        xbmcgui.Dialog().ok("Error", "No movies found")


def get_person_artwork(item):
    person_id = item['person']['ids']['trakt']
    person_tmdb_id = item['person']['ids']['tmdb']
    try:
        person_images = tmdb.People(person_tmdb_id).images()['profiles']
        return 'https://image.tmdb.org/t/p/w640' + person_images[0]['file_path']
    except:
        return 'https://raw.githubusercontent.com/OpenELEQ/Style/master/MetalliQ/default/unavailable_movieposter.png'
