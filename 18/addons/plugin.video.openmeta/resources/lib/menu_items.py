from resources.lib import lists
from resources.lib import nav_movies
from resources.lib import nav_tvshows
from resources.lib.xswift2 import plugin

@plugin.route('/')
def root():
	items = [
	{
		'label': 'Movies',
		'path': plugin.url_for('movies'),
		'thumbnail': plugin.get_media_icon('movies'),
		'fanart': plugin.get_addon_fanart()
	},
	{
		'label': 'TV Shows',
		'path': plugin.url_for('tv'),
		'thumbnail': plugin.get_media_icon('tv'),
		'fanart': plugin.get_addon_fanart()
	},
	{
		'label': 'My Trakt',
		'path': plugin.url_for('my_trakt'),
		'thumbnail': plugin.get_media_icon('trakt'),
		'fanart': plugin.get_addon_fanart()
	},
	{
		'label': 'Search...',
		'path': plugin.url_for('search_term'),
		'thumbnail': plugin.get_media_icon('search'),
		'fanart': plugin.get_addon_fanart()
	},
	{
		'label': 'Settings',
		'path': plugin.url_for('open_settings'),
		'thumbnail': plugin.get_media_icon('settings'),
		'fanart': plugin.get_addon_fanart()
	}]
	return items

@plugin.route('/movies')
def movies():
	items = [
	{
		'label': 'Blockbusters (TMDB)',
		'path': plugin.url_for('tmdb_movies_blockbusters', page=1),
		'thumbnail': plugin.get_media_icon('most_voted'),
		'fanart': plugin.get_addon_fanart(),
		'context_menu': [
			('Play (random)', 'RunPlugin(%s)' % plugin.url_for('tmdb_movies_play_random_blockbuster'))]
	},
	{
		'label': 'In theatres (TMDB)',
		'path': plugin.url_for('tmdb_movies_now_playing', page=1),
		'thumbnail': plugin.get_media_icon('intheatres'),
		'fanart': plugin.get_addon_fanart(),
		'context_menu': [
			('Play (random)', 'RunPlugin(%s)' % plugin.url_for('tmdb_movies_play_random_now_playing'))]
	},
	{
		'label': 'Popular (TMDB)',
		'path': plugin.url_for('tmdb_movies_popular', page=1),
		'thumbnail': plugin.get_media_icon('popular'),
		'fanart': plugin.get_addon_fanart(),
		'context_menu': [
			('Play (random)', 'RunPlugin(%s)' % plugin.url_for('tmdb_movies_play_random_popular'))]
	},
	{
		'label': 'Top rated (TMDB)',
		'path': plugin.url_for('tmdb_movies_top_rated', page=1),
		'thumbnail': plugin.get_media_icon('top_rated'),
		'fanart': plugin.get_addon_fanart(),
		'context_menu': [
			('Play (random)', 'RunPlugin(%s)' % plugin.url_for('tmdb_movies_play_random_top_rated'))]
	},
	{
		'label': 'Most watched (Trakt)',
		'path': plugin.url_for('trakt_movies_watched', page=1),
		'thumbnail': plugin.get_media_icon('traktwatchlist'),
		'fanart': plugin.get_addon_fanart(),
		'context_menu': [
			('Play (random)', 'RunPlugin(%s)' % plugin.url_for('trakt_movies_play_random_watched'))]
	},
	{
		'label': 'Most collected (Trakt)',
		'path': plugin.url_for('trakt_movies_collected', page=1),
		'thumbnail': plugin.get_media_icon('traktcollection'),
		'fanart': plugin.get_addon_fanart(),
		'context_menu': [
			('Play (random)', 'RunPlugin(%s)' % plugin.url_for('trakt_movies_play_random_collected'))]
	},
	{
		'label': 'Popular (Trakt)',
		'path': plugin.url_for('trakt_movies_popular', page=1),
		'thumbnail': plugin.get_media_icon('traktrecommendations'),
		'fanart': plugin.get_addon_fanart(),
		'context_menu': [
			('Play (random)', 'RunPlugin(%s)' % plugin.url_for('trakt_movies_play_random_popular'))]
	},
	{
		'label': 'Trending (Trakt)',
		'path': plugin.url_for('trakt_movies_trending', page=1),
		'thumbnail': plugin.get_media_icon('trending'),
		'fanart': plugin.get_addon_fanart(),
		'context_menu': [
			('Play (random)', 'RunPlugin(%s)' % plugin.url_for('trakt_movies_play_random_trending'))]
	},
	{
		'label': 'Latest releases (Trakt)',
		'path': plugin.url_for('trakt_movies_latest_releases'),
		'thumbnail': plugin.get_media_icon('traktcalendar'),
		'fanart': plugin.get_addon_fanart(),
		'context_menu': [
			('Play (random)', 'RunPlugin(%s)' % plugin.url_for('trakt_movies_play_random_latest_releases'))]
	},
	{
		'label': 'Top 250 (IMDB)',
		'path': plugin.url_for('trakt_movies_imdb_top_rated', page=1),
		'thumbnail': plugin.get_media_icon('imdb'),
		'fanart': plugin.get_addon_fanart(),
		'context_menu': [
			('Play (random)', 'RunPlugin(%s)' % plugin.url_for('trakt_movies_play_random_imdb_top_rated'))]
	},
	{
		'label': 'Genres',
		'path': plugin.url_for('tmdb_movies_genres'),
		'thumbnail': plugin.get_media_icon('genres'),
		'fanart': plugin.get_addon_fanart()
	}]
	return items

@plugin.route('/tv')
def tv():
	items = [
	{
		'label': 'Currently Airing (TMDB)',
		'path': plugin.url_for('tmdb_tv_on_the_air', page=1),
		'thumbnail': plugin.get_media_icon('ontheair'),
		'fanart': plugin.get_addon_fanart()
	},
	{
		'label': 'Popular (TMDB)',
		'path': plugin.url_for('tmdb_tv_most_popular', page=1),
		'thumbnail': plugin.get_media_icon('popular'),
		'fanart': plugin.get_addon_fanart()
	},
	{
		'label': 'Most Watched (Trakt)',
		'path': plugin.url_for('trakt_tv_watched', page=1),
		'thumbnail': plugin.get_media_icon('traktwatchlist'),
		'fanart': plugin.get_addon_fanart()
	},
	{
		'label': 'Most Collected (Trakt)',
		'path': plugin.url_for('trakt_tv_collected', page=1),
		'thumbnail': plugin.get_media_icon('traktcollection'),
		'fanart': plugin.get_addon_fanart()
	},
	{
		'label': 'Most Collected Netflix (Trakt)',
		'path': plugin.url_for('trakt_netflix_tv_collected', page=1),
		'thumbnail': plugin.get_media_icon('traktcollection'),
		'fanart': plugin.get_addon_fanart()
	},
	{
		'label': 'Most Popular (Trakt)',
		'path': plugin.url_for('tv_trakt_popular', page=1),
		'thumbnail': plugin.get_media_icon('traktrecommendations'),
		'fanart': plugin.get_addon_fanart()
	},
	{
		'label': 'Trending (Trakt)',
		'path': plugin.url_for('trakt_tv_trending', page=1),
		'thumbnail': plugin.get_media_icon('trending'),
		'fanart': plugin.get_addon_fanart()
	},
	{
		'label': 'Genres',
		'path': plugin.url_for('tmdb_tv_genres'),
		'thumbnail': plugin.get_media_icon('genres'),
		'fanart': plugin.get_addon_fanart()
	}]
	return items

@plugin.route('/my_trakt')
def my_trakt():
	items = [
	{
		'label': 'Movies',
		'path': plugin.url_for('movie_lists'),
		'thumbnail': plugin.get_media_icon('movies'),
		'fanart': plugin.get_addon_fanart()
	},
	{
		'label': 'TV Shows',
		'path': plugin.url_for('tv_lists'),
		'thumbnail': plugin.get_media_icon('tv'),
		'fanart': plugin.get_addon_fanart()
	},
	{
		'label': 'Lists (Movies & TV Shows)',
		'path': plugin.url_for('lists'),
		'thumbnail': plugin.get_media_icon('traktmylists'),
		'fanart': plugin.get_addon_fanart()
	}]
	return items

@plugin.route('/my_trakt/movie_lists')
def movie_lists():
	items = [
	{
		'label': 'Collection',
		'path': plugin.url_for('lists_trakt_movies_collection'),
		'thumbnail': plugin.get_media_icon('traktcollection'),
		'fanart': plugin.get_addon_fanart(),
		'context_menu': [
			('Play (random)', 'RunPlugin(%s)' % plugin.url_for('lists_trakt_movies_play_random_collection')),
			('Add to library', 'RunPlugin(%s)' % plugin.url_for('lists_trakt_movies_collection_to_library'))]
	},
	{
		'label': 'Recommendations',
		'path': plugin.url_for('trakt_movies_recommendations'),
		'thumbnail': plugin.get_media_icon('traktrecommendations'),
		'fanart': plugin.get_addon_fanart()
	},
	{
		'label': 'Watchlist',
		'path': plugin.url_for('trakt_movies_watchlist'),
		'thumbnail': plugin.get_media_icon('traktwatchlist'),
		'fanart': plugin.get_addon_fanart(),
		'context_menu': [
				('Play (random)', 'RunPlugin(%s)' % plugin.url_for('trakt_movies_play_random_watchlist'))]
	},
	{
		'label': 'My Lists',
		'path': plugin.url_for('lists_trakt_my_movie_lists'),
		'thumbnail': plugin.get_media_icon('traktmylists'),
		'fanart': plugin.get_addon_fanart()
	},
	{
		'label': 'Liked Lists',
		'path': plugin.url_for('lists_trakt_liked_movie_lists', page=1),
		'thumbnail': plugin.get_media_icon('traktlikedlists'),
		'fanart': plugin.get_addon_fanart()
	}]
	return items

@plugin.route('/my_trakt/tv_lists')
def tv_lists():
	items = [
	{
		'label': 'Collection',
		'path': plugin.url_for('lists_trakt_tv_collection'),
		'thumbnail': plugin.get_media_icon('traktcollection'),
		'fanart': plugin.get_addon_fanart(),
		'context_menu': [
			('Add to library', 'RunPlugin(%s)' % plugin.url_for('lists_trakt_tv_collection_to_library'))]
	},
	{
		'label': 'Recommendations',
		'path': plugin.url_for('trakt_tv_recommendations'),
		'thumbnail': plugin.get_media_icon('traktrecommendations'),
		'fanart': plugin.get_addon_fanart()
	},
	{
		'label': 'Watchlist',
		'path': plugin.url_for('trakt_tv_watchlist', page = 1),
		'thumbnail': plugin.get_media_icon('traktwatchlist'),
		'fanart': plugin.get_addon_fanart()
	},
	{
		'label': 'My Lists',
		'path': plugin.url_for('lists_trakt_my_tv_lists'),
		'thumbnail': plugin.get_media_icon('traktmylists'),
		'fanart': plugin.get_addon_fanart()
	},
	{
		'label': 'Liked Lists',
		'path': plugin.url_for('lists_trakt_liked_tv_lists', page=1),
		'thumbnail': plugin.get_media_icon('traktlikedlists'),
		'fanart': plugin.get_addon_fanart()
	},
	{
		'label': 'Next Episodes',
		'path': plugin.url_for('trakt_tv_next_episodes'),
		'thumbnail': plugin.get_media_icon('traktnextepisodes'),
		'fanart': plugin.get_addon_fanart()
	},
	{
		'label': 'Upcoming Episodes',
		'path': plugin.url_for('trakt_tv_upcoming_episodes'),
		'thumbnail': plugin.get_media_icon('traktcalendar'),
		'fanart': plugin.get_addon_fanart()
	}]
	return items

@plugin.route('/my_trakt/lists')
def lists():
	items = [
	{
		'label': 'My Lists',
		'path': plugin.url_for('lists_trakt_my_lists'),
		'thumbnail': plugin.get_media_icon('traktmylists'),
		'fanart': plugin.get_addon_fanart()
	},
	{
		'label': 'Liked Lists',
		'path': plugin.url_for('lists_trakt_liked_lists', page=1),
		'thumbnail': plugin.get_media_icon('traktlikedlists'),
		'fanart': plugin.get_addon_fanart()
	}]
	return items

@plugin.route('/search')
def search_term():
	term = plugin.keyboard(heading='Enter search string')
	if term != None and term != '':
		return search(term)
	else:
		return

@plugin.route('/search/edit/<term>')
def search_edit(term):
	if term == ' ' or term == None or term == '':
		term = plugin.keyboard(heading='Enter search string')
	else:
		term = plugin.keyboard(default=term, heading='Enter search string')
	if term != None and term != '':
		return search(term)
	else:
		return

@plugin.route('/search/<term>', options = {'term': 'None'})
def search(term):
	items = [
	{
		'label': 'Movies (TMDB) search - ' + term,
		'path': plugin.url_for('tmdb_movies_search_term', term=term, page=1),
		'thumbnail': plugin.get_media_icon('search'),
		'fanart': plugin.get_addon_fanart()
	},
	{
		'label': 'Movies (Trakt) search - ' + term, 
		'path': plugin.url_for('trakt_movies_search_term', term=term, page=1),
		'thumbnail': plugin.get_media_icon('search'),
		'fanart': plugin.get_addon_fanart()
	},
	{
		'label': 'TV shows (TVDB) search - ' + term,
		'path': plugin.url_for('tvdb_tv_search_term', term=term, page=1),
		'thumbnail': plugin.get_media_icon('search'),
		'fanart': plugin.get_addon_fanart()
	},
	{
		'label': 'TV shows (Trakt) search - ' + term,
		'path': plugin.url_for('trakt_tv_search_term', term=term, page=1),
		'thumbnail': plugin.get_media_icon('search'),
		'fanart': plugin.get_addon_fanart()
	},
	{
		'label': 'Lists (Trakt) search - ' + term,
		'path': plugin.url_for('lists_search_for_lists_term', term=term, page=1),
		'thumbnail': plugin.get_media_icon('search'),
		'fanart': plugin.get_addon_fanart(),
	},
	{
		'label': 'Edit search string',
		'path': plugin.url_for('search_edit', term=term),
		'thumbnail': plugin.get_media_icon('search'),
		'fanart': plugin.get_addon_fanart()
	}]
	return items