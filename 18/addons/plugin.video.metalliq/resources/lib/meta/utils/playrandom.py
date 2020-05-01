from trakt import trakt
from meta.play.tvshows import play_episode
from meta.play.movies import play_movie
def trakt_play_random(list_items):
    import random
    random.seed()
    index = random.randint(0, len(list_items) - 1)
    list_item = list_items[index]
    if list_item['type'] == "show":
        id = list_item["show"]["ids"]["tvdb"]
        show_slug = list_item["show"]["ids"]["slug"]
        show_episodes = trakt.get_all_episodes(show_slug)
        season = show_episodes[random.randint(0, len(show_episodes) - 1)]
        episode = season["episodes"][random.randint(0, len(season) - 1)]
        season_number = episode["season"]
        episode_number = episode["number"]
        play_episode(id, season_number, episode_number, "default")
    elif list_item['type'] == "season":
        id = list_item["show"]["ids"]["tvdb"]
        show_slug = list_item["show"]["ids"]["slug"]
        season_number = list_item["season"]["number"]
        season_episodes = trakt.get_season_episodes(show_slug, season_number)
        episode = season_episodes[random.randint(0, len(season_episodes) - 1)]
        episode_number = episode["number"]
        play_episode(id, season_number, episode_number, "default")
    elif list_item['type'] == "episode":
        id = list_item["show"]["ids"]["tvdb"]
        season_number = list_item["season"]
        episode_number = list_item["number"]
        play_episode(id, season_number, episode_number, "default")
    elif list_item['type'] == "movie":
        id = list_item["movie"]["ids"]["tmdb"]
        play_movie(id, "default")


def tmdb_play_random(list_items):
    import random
    random.seed()
    index = random.randint(0, len(list_items) - 1)
    list_item = list_items[index]
    if list_item['type'] == "movie":
        id = list_item["id"]
        play_movie(id, "default")
