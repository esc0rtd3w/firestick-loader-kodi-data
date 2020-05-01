from dudehere.routines import *
from dudehere.routines.i18nlib import i18n
class STRINGS():
	def map(self, key):
		table = {
			'tv_menu': 				30000,
			'movie_menu': 			30001,
			'settings_menu': 		30002,
			'show_about':			30003,
			'authorize_trakt': 		30004,
			'calendar': 			30005,
			'genres':		 		30006,
			'tv_watchlist': 		30007,
			'custom_lists': 		30008,
			'tv_trending': 			30009,
			'tv_popular': 			30010,
			'tv_recommended': 		30011,
			'search': 				30012,
			'movie_watchlist':		30013,
			'movie_trending':		30014,
			'movie_popular':		30015,
			'movie_recommended':	30016,
			'movie_discover':		30017,
			'scraper_list':			30018,
			'scraper_accounts':		30019,
			'manage_transmogrifier':30020,
			'enable_advanced_mode':	30021,
			'enable_basic_mode':	30022,
			'reset_trw':			30023,
			'tv_anticipated':		30024,
			'settings_transmogrifier':	30025,
			'settings_urlresolver':	30026,
			'settings_theroyalwe':	30027,
			'calendar_browser':		30028,
			'manage_hosts':			30029,
			'my_collection':		30030,
			'my_favorites':			30031,
			'movie_tmdb':			30032,
			'scraper_settings':		30033,
			'manage_walter':		30034,
			'ondeck':				30036,
			'clear_cache':			30037,
		}
		if key in table.keys():
			return i18n(table[key])
		else:
			return False