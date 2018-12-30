from dudehere.routines import *
from dudehere.routines import plugin
WATCHLIST_COLOR = 'yellow'
HAS_TRANMOGRIFIED = 'orange'
WATCHLIST_COLOR 	= plugin.get_setting('custom_color_watchlist')
SYNC_COLOR			= plugin.get_setting('custom_color_sync')
DISABLED_COLOR		= plugin.get_setting('custom_color_disabled')
ENABLED_COLOR		= plugin.get_setting('custom_color_enabled')
NEXTPAGE_COLOR		= plugin.get_setting('custom_color_nextpage')
PREVIOUSPAGE_COLOR	= plugin.get_setting('custom_color_previouspage')
UNAIRED_COLOR		= plugin.get_setting('custom_color_unaired')
RESUME_COLOR		= plugin.get_setting('custom_color_resume')

WATCH_PERCENT = 94
RESULT_LIMIT = 500

if plugin.get_setting('enable_default_views') == 'true':
	VIEWS = enum(DEFAULT=plugin.get_setting('default_folder_view'), LIST=50, BIGLIST=51, THUMBNAIL=500, SMALLTHUMBNAIL=522, FANART=508, POSTERWRAP=501, MEDIAINFO=504, MEDIAINFO2=503, MEDIAINFO3=515, WIDE=505, LIST_DEFAULT=plugin.get_setting('default_list_view'), TV_DEFAULT=plugin.get_setting('default_tvshow_view'), MOVIE_DEFAULT=plugin.get_setting('default_movie_view'), SEASON_DEFAULT=plugin.get_setting('default_season_view'), EPISODE_DEFAULT=plugin.get_setting('default_episode_view'))
