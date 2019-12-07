import nanscrapers
import xbmcgui
import os
import xbmc
import xbmcaddon
import random
import sys
import urlparse
import xbmcvfs
from nanscrapers.common import clean_title
from BeautifulSoup import BeautifulStoneSoup

params = dict(urlparse.parse_qsl(sys.argv[2].replace('?', '')))
mode = params.get('mode')
if mode == "DisableAll":
    scrapers = sorted(
        nanscrapers.relevant_scrapers(include_disabled=True), key=lambda x: x.name.lower())
    for scraper in scrapers:
        key = "%s_enabled" % scraper.name
        xbmcaddon.Addon('script.module.nanscrapers').setSetting(key, "false")
    sys.exit()
elif mode == "EnableAll":
    scrapers = sorted(
        nanscrapers.relevant_scrapers(include_disabled=True), key=lambda x: x.name.lower())
    for scraper in scrapers:
        key = "%s_enabled" % scraper.name
        xbmcaddon.Addon('script.module.nanscrapers').setSetting(key, "true")
    sys.exit()


try:
    from sqlite3 import dbapi2 as database
except:
    from pysqlite2 import dbapi2 as database

movies = [
    {
        'title': 'Deadpool',
        'year': '2016',
        'imdb': 'tt1431045'
    },
    {
        'title': 'Silence',
        'year': '2016',
        'imdb': 'tt0490215'
    },
    {
        'title': 'Resident Evil: The Final Chapter',
        'year': '2016',
        'imdb': 'tt2592614'
    },
    {
        'title': 'The Great Wall',
        'year': '2016',
        'imdb': 'tt2034800'
    },
    {
        'title': 'Why Him?',
        'year': '2016',
        'imdb': 'tt4501244'
    },
    {
        'title': 'Patriots Day',
        'year': '2016',
        'imdb': 'tt4572514'
    },
    {
        'title': 'Moana',
        'year': '2016',
        'imdb': 'tt3521164'
    },
    {
        'title': 'Sing',
        'year': '2016',
        'imdb': 'tt3470600'
    },
    {
        'title': 'Sonic The Hedgehog: The Movie',
        'year': '1996',
        'imdb': 'tt0237765'
    },
    {
        'title': 'Surf\'s Up',
        'year': '2007',
        'imdb': 'tt0423294'
    },
    {
        'title': 'Kim Possible A Sitch in Time',
        'year': '2004',
        'imdb': 'tt0389074'
    },
    {
        'title': 'Izzies Way Home',
        'year': '2016',
        'imdb': 'tt5667482'
    },
    {
        'title': 'A Turtle\'s Tale: Sammy\'s Adventures',
        'year': '2010',
        'imdb': 'tt1230204'
    },
]

shows = [
    {
        'title': "The Flash",
        'show_year': "2014",
        'year': "2014",
        'season': '1',
        'episode': '1',
        'imdb': 'tt3107288',
    },
    {
        'title': "The Flash",
        'show_year': "2014",
        'year': "2016",
        'season': '3',
        'episode': '8',
        'imdb': 'tt3107288',
    },
    {
        'title': "Breaking Bad",
        'show_year': "2008",
        'year': "2008",
        'season': '1',
        'episode': '1',
        'imdb': 'tt0903747',
    },
    {
        'title': "Breaking Bad",
        'show_year': "2008",
        'year': "2011",
        'season': '4',
        'episode': '6',
        'imdb': 'tt0903747',
    },
    {
        'title': "Game of Thrones",
        'show_year': "2011",
        'year': "2011",
        'season': '1',
        'episode': '1',
        'imdb': 'tt0944947',
    },
    {
        'title': "Game of Thrones",
        'show_year': "2011",
        'year': "2016",
        'season': '6',
        'episode': '5',
        'imdb': 'tt0944947',
    },
    {
        'title': "House M.D.",
        'show_year': "2004",
        'year': "2004",
        'season': '1',
        'episode': '1',
        'imdb': 'tt0412142',
    },

]


def main():
    test_type = xbmcgui.Dialog().select("Choose type of test", ["Test List", "Profile List", "Profile Scrapers"])
    basepath = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo("profile"))
    if test_type == 0:
        test()
    elif test_type == 1:
        import cProfile
        cProfile.run('test()',
                     os.path.join(basepath, 'profile_list.profile'))
    elif test_type == 2:
        import cProfile
        cProfile.run('profile_scrapers("movie")',
                     os.path.join(basepath, 'profile_scrapers_movies.profile'))
        cProfile.run('profile_scrapers("episode")',
                     os.path.join(basepath, 'profile_scrapers_episodes.profile'))


def test():
    global movies, shows
    try:
        test_movies = []
        test_episodes = []
        profile_path = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo('profile')).decode('utf-8')
        test_file = xbmcvfs.File(os.path.join(profile_path, "testings.xml"))
        xml = BeautifulStoneSoup(test_file.read())
        test_file.close()
        items = xml.findAll("item")
        for item in items:
            try:
                content = item.find("content")
                if content:
                    if "movie" in content.text:
                        meta = item.find("meta")
                        test_movies.append({
                            'title': meta.find("title").text,
                            'imdb': meta.find("imdb").text,
                            'year': meta.find("year").text,
                        })
                    elif "episode" in content.text:
                        meta = item.find("meta")
                        test_episodes.append({
                            'title': meta.find("tvshowtitle").text,
                            'show_year': int(meta.find("premiered").text[0:4]),
                            'year': meta.find("year").text,
                            'season': meta.find("season").text,
                            'episode': meta.find("season").text,
                            'imdb': meta.find("imdb").text,
                        })
            except:
                pass

            movies = test_movies
            shows = test_episodes
    except:
        pass

    dialog = xbmcgui.Dialog()
    pDialog = xbmcgui.DialogProgress()
    if dialog.yesno("NaNscrapers Testing Mode", 'Clear cache?'):
        nanscrapers.clear_cache()
    try:
        dbcon = database.connect(os.path.join(
            xbmc.translatePath(xbmcaddon.Addon("script.module.nanscrapers").getAddonInfo('profile')).decode('utf-8'),
            'url_cache.db'))
        dbcur = dbcon.cursor()
    except:
        dialog.ok("NaNscrapers Testing Mode", 'Error connecting to db')
        sys.exit()

    num_movies = len(movies)
    if num_movies > 0:
        pDialog.create('NaNscrapers Testing mode active', 'please wait')
        index = 0
        for movie in movies:
            index += 1
            title = movie['title']
            year = movie['year']
            imdb = movie['imdb']
            if pDialog.iscanceled():
                pDialog.close()
                break
            pDialog.update((index / num_movies) * 100, "Scraping movie {} of {}".format(index, num_movies), title)
            links_scraper = nanscrapers.scrape_movie(title, year, imdb)
            links_scraper = links_scraper()
            for scraper_links in links_scraper:
                if pDialog.iscanceled():
                    break
                if scraper_links:
                    random.shuffle(scraper_links)

        pDialog.close()
        dbcur.execute("SELECT COUNT(DISTINCT(scraper)) FROM rel_src where episode = ''")
        match = dbcur.fetchone()
        num_movie_scrapers = match[0]

        dbcur.execute("SELECT scraper, count(distinct(urls)) FROM rel_src where episode = '' group by scraper")
        matches = dbcur.fetchall()
        failed = []
        for match in matches:
            if int(match[1]) <= 1:
                failed.append(match[0])

        if len(failed) > 0:
            failedstring = "Failed: {}".format(len(failed))
            for fail in failed:
                failedstring += "\n        - {}".format(str(fail))
        else:
            failedstring = ""

        dbcur.execute("SELECT title, count(distinct(urls)) FROM rel_src where episode = '' group by title")
        matches = dbcur.fetchall()
        failed_movies = []
        for match in matches:
            if int(match[1]) <= 1:
                if int(match[1]) == 1:
                    dbcur.execute(
                        "SELECT scraper, urls FROM rel_src where episode == '' and title == '{}' group by scraper".format(
                            match[0]))
                    new_matches = dbcur.fetchall()
                    found = False
                    for new_match in new_matches:
                        if new_match[1] == "[]":
                            continue
                        else:
                            found = True
                    if not found:
                        failed_movies.append(match[0])
                else:
                    failed_movies.append(match[0])

        if len(failed_movies) > 0:
            failed_movie_string = "Failed movies: {}".format(len(failed_movies))
            for fail in failed_movies:
                for movie in movies:
                    if clean_title(movie['title']).upper() == str(fail):
                        failed_movie_string += "\n        - {}".format(movie["title"])

        else:
            failed_movie_string = ""

    num_shows = len(shows)
    if num_shows > 0:
        pDialog.create('NaNscrapers Testing mode active', 'please wait')
        index = 0
        for show in shows:
            index += 1
            title = show['title']
            show_year = show['show_year']
            year = show['year']
            season = show['season']
            episode = show['episode']
            imdb = show['imdb']
            tvdb = show.get('tvdb', '')

            if pDialog.iscanceled():
                pDialog.close()
                break
            pDialog.update((index / num_shows) * 100, "Scraping show {} of {}".format(index, num_shows), title)
            links_scraper = nanscrapers.scrape_episode(title, show_year, year, season, episode, imdb, tvdb)
            links_scraper = links_scraper()
            for scraper_links in links_scraper:
                if pDialog.iscanceled():
                    break
                if scraper_links:
                    random.shuffle(scraper_links)

        pDialog.close()
        dbcur.execute("SELECT COUNT(DISTINCT(scraper)) FROM rel_src where episode != ''")
        match = dbcur.fetchone()
        num_show_scrapers = match[0]

        dbcur.execute("SELECT scraper, count(distinct(urls)) FROM rel_src where episode != '' group by scraper")
        matches = dbcur.fetchall()
        failed = []
        for match in matches:
            if int(match[1]) <= 1:
                if int(match[1]) == 1:
                    dbcur.execute(
                        "SELECT scraper, urls FROM rel_src where episode != '' and scraper == '{}' group by scraper".format(
                            match[0]))
                    match = dbcur.fetchone()
                    if match[1] == "[]":
                        failed.append(match[0])
                else:
                    failed.append(match[0])

        if len(failed) > 0:
            show_scraper_failedstring = "Failed: {}".format(len(failed))
            for fail in failed:
                show_scraper_failedstring += "\n        - {}".format(str(fail))
        else:
            show_scraper_failedstring = ""

        dbcur.execute("SELECT title, count(distinct(urls)) FROM rel_src where episode != '' group by title")
        matches = dbcur.fetchall()
        failed_shows = []
        for match in matches:
            if int(match[1]) <= 1:
                if int(match[1]) == 1:
                    dbcur.execute(
                        "SELECT scraper, urls FROM rel_src where episode != '' and title == '{}' group by scraper".format(
                            match[0]))
                    new_matches = dbcur.fetchall()
                    found = False
                    for new_match in new_matches:
                        if new_match[1] == "[]":
                            continue
                        else:
                            found = True
                    if not found:
                        failed_shows.append(match[0])
                else:
                    failed_shows.append(match[0])

        if len(failed_shows) > 0:
            failed_show_string = "Failed shows: {}".format(len(failed_shows))
            for fail in failed_shows:
                for show in shows:
                    if clean_title(show['title']).upper() == str(fail):
                        failed_show_string += "\n        - {} S{}-E{}".format(show["title"], show["season"],
                                                                              show["episode"])

        else:
            failed_show_string = ""

    resultstring = 'Results:\n'
    if num_movies > 0:
        resultstring = resultstring + \
                       '    Movie Scrapers: {}\n' \
                       '    {}\n' \
                       '    {}\n'.format(num_movie_scrapers, failedstring, failed_movie_string)
    if num_shows > 0:
        resultstring = resultstring + \
                       '    Episode Scrapers: {}\n' \
                       '    {}\n' \
                       '    {}\n'.format(num_show_scrapers, show_scraper_failedstring, failed_show_string)

    dialog.textviewer("NaNscrapers Testing Mode", resultstring)


def profile_scrapers(profile_type):
    global movies, shows
    from nanscrapers.hl import HostedLink
    import random
    if profile_type == "movie":
        movieindex = 1
        num_movies = len(movies)
        pDialog = xbmcgui.DialogProgress()
        pDialog.create('NaNscrapers Testing mode active', 'please wait')
        for movie in movies:
            if pDialog.iscanceled():
                pDialog.close()
                break
            title = movie['title']
            year = movie["year"]
            imdb = movie["imdb"]
            hl = HostedLink(title, year, imdb, None)
            scrapers = hl.get_scrapers()
            num_scrapers = len(scrapers)
            index = 1
            for scraper in scrapers:
                if pDialog.iscanceled():
                    pDialog.close()
                    break
                pDialog.update((index / num_scrapers) * 100,
                               "Scraping movie {} of {} with scraper {} of {}".format(movieindex, num_movies, index,
                                                                                      num_scrapers),
                               "current scraper: {}".format(scraper.name))
                scraper.scrape_movie(title, year, imdb)
                index += 1
            movieindex += 1
        pDialog.close()
    elif profile_type == "episode":
        episodeindex = 1
        num_episodes = len(movies)
        pDialog = xbmcgui.DialogProgress()
        pDialog.create('NaNscrapers Testing mode active', 'please wait')
        for show in shows:
            if pDialog.iscanceled():
                pDialog.close()
                break
            title = show['title']
            year = show["year"]
            imdb = show["imdb"]
            show_year = show["show_year"]
            season = show["season"]
            episode = show["episode"]
            hl = HostedLink(title, year, imdb, None)
            scrapers = hl.get_scrapers()
            num_scrapers = len(scrapers)
            index = 0
            for scraper in scrapers:
                if pDialog.iscanceled():
                    pDialog.close()
                    break
                pDialog.update((index / num_scrapers) * 100,
                               "Scraping episode {} of {} with scraper {} of {}".format(episodeindex, num_episodes,
                                                                                        index, num_scrapers),
                               "current scraper: {}".format(scraper.name))
                scraper.scrape_episode(title, show_year, year, season, episode, imdb, None)
                index += 1
            episodeindex +=1
        pDialog.close()


if __name__ == '__main__':
    main()
