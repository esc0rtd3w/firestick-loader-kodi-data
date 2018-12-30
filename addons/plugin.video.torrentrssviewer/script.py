# coding: utf-8
# Main Script
__author__ = 'mancuniancol'

from tools import *
import feedparser

storage = Storage(settings.storageName, type="dict", eval=True)

# this read the settings
list_url_search = []
rep = 0

while rep < 7:
    rep = settings.dialog.select(settings.string(32010),
                                 [settings.string(32005),
                                  settings.string(32011),
                                  settings.string(32012),
                                  settings.string(32013),
                                  settings.string(32014),
                                  settings.string(32015),
                                  settings.string(32016),
                                  settings.string(32017),
                                  settings.string(32018)
                                  ])
    if rep == 0:  # Add a New RSS
        selection = settings.dialog.input(settings.string(32007))
        name = ''
        while name is '':
            name = settings.dialog.input(settings.string(32008)).title()
        storage.database[name] = (selection, True)

    if rep == 1:  # Modify RSS list
        List = [name + ": " + RSS for (name, (RSS, isIntegrated)) in
                zip(storage.database.keys(), storage.database.values())]
        list_rep = settings.dialog.select(settings.string(32010), List + [settings.string(32019)])
        if list_rep < len(List):
            name = storage.database.keys()[list_rep]
            storage.database[name] = (settings.dialog.input(settings.string(32007), storage.database[name][0]), True)

    if rep == 2 and len(storage.database.keys()) > 0:  # Remove a RSS
        List = [name + ": " + RSS for (name, (RSS, isIntegrated)) in
                zip(storage.database.keys(), storage.database.values())]
        list_rep = settings.dialog.select(settings.string(32020), List + [settings.string(32019)])
        if list_rep < len(List):
            if settings.dialog.yesno('', settings.string(32006) % List[list_rep]):
                storage.remove(storage.database.keys()[list_rep])

    if rep == 3:  # View Saved RSS list
        List = [name + ": " + RSS + ' : %s' % isIntegrated for (name, (RSS, isIntegrated)) in
                zip(storage.database.keys(), storage.database.values())]
        settings.dialog.select(settings.string(32007), List)

    if rep == 4:  # Read RSS list and create .strm Files
        list_url = storage.database.values()
        # Begin reading
        magnetsMovie = []
        titlesMovie = []
        magnetsShow = []
        titlesShow = []
        magnetsAnime = []
        titlesAnime = []
        for (url_search, isIntegrated) in list_url:
            if url_search is not '' and isIntegrated:
                settings.notification(settings.string(32021) % url_search)
                settings.log(url_search)
                response = feedparser.parse(url_search)
                for entry in response.entries:
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
                    info = formatTitle(entry.title)
                    if 'MOVIE' in info['type']:
                        titlesMovie.append(entry.title)
                        magnetsMovie.append(value)
                    if 'SHOW' in info['type']:
                        titlesShow.append(entry.title)
                        magnetsShow.append(value)
                    if 'ANIME' in info['type']:
                        titlesAnime.append(entry.title)
                        magnetsAnime.append(value)
        if len(titlesMovie) > 0:
            integration(titles=titlesMovie, magnets=magnetsMovie, typeList='MOVIE',
                        folder=settings.movieFolder, silence=True)
        if len(titlesShow) > 0:
            integration(titles=titlesShow, magnets=magnetsShow, typeList='SHOW',
                        folder=settings.showFolder, silence=True)
        if len(titlesAnime) > 0:
            integration(titles=titlesAnime, magnets=magnetsAnime, typeList='ANIME',
                        folder=settings.animeFolder, silence=True)

    if rep == 5:  # Erase Folders
        selectionRemove = settings.dialog.select(settings.string(32010),
                                                 [settings.string(32022), settings.string(32023),
                                                  settings.string(32024)])
        if selectionRemove == 0:
            removeDirectory(settings.movieFolder)
        elif selectionRemove == 1:
            removeDirectory(settings.showFolder)
        else:
            removeDirectory(settings.animeFolder)

    if rep == 6:  # Settings
        settings.settings.openSettings()
        del settings
        settings = Settings()

    if rep == 7:  # Help
        settings.dialog.ok(settings.string(32017),
                           settings.string(32025))
    # save the dictionary
    storage.save()

del settings
del storage
del browser
