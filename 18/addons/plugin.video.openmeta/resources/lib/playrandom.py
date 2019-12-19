import random
from resources.lib.play_movies import play_movie

def trakt_play_random(list_items):
	random.seed()
	index = random.randint(0, len(list_items) - 1)
	list_item = list_items[index]
	if list_item['type'] == 'movie':
		id = list_item['movie']['ids']['tmdb']
		play_movie(id)

def tmdb_play_random(list_items):
	random.seed()
	index = random.randint(0, len(list_items) - 1)
	list_item = list_items[index]
	if list_item['type'] == 'movie':
		id = list_item['id']
		play_movie(id)