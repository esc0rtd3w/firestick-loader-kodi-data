import json
from xbmcswift2 import xbmc
from meta import plugin
from meta.utils.properties import get_property, clear_property
from meta.utils.rpc import RPC

class VideoPlayer(xbmc.Player):
    def __init__(self, *args, **kwargs):
        xbmc.Player.__init__(self)
        self.reset()

    def reset(self):
        self.id = None
        self.totalTime = 0
        self.currentTime = 0

    def currently_playing(self):
        video_data = get_property("data")
        if video_data:
            try:
                video_data = json.loads(video_data)
                return self.get_episode_id(video_data.get("dbid"), video_data['tvdb'], video_data['season'], video_data['episode'])
            except KeyError: pass
        return None

    def mark_as_watched(self):
        if not self.id: return
        RPC.video_library.set_episode_details(episodeid = self.id, playcount=1, resume={"position": 0})
        xbmc.executebuiltin('Container.Refresh')

    def get_episode_id(self, dbid, tvdb_id, season, episode):
        filter = {"and": 
            [{"field": "season", "operator": "is", "value": str(season)},
            {"field": "episode", "operator": "is", "value": str(episode)}]}
        result = RPC.video_library.get_episodes(filter=filter, properties=["season", "episode", "file"])
        episodes = result.get('episodes', [])
        if dbid: episodes = [ep for ep in episodes if ep['episodeid']==dbid]
        else: episodes = [ep for ep in episodes if plugin.id in ep['file'] and '/{0}/'.format(tvdb_id) in ep['file'].replace('\\', '/')]
        if episodes: return episodes[0]['episodeid']
        return None

    def onPlayBackStarted(self):
        self.reset()
        if self.isPlayingVideo():
            self.id = self.currently_playing()
            self.totalTime = self.getTotalTime()

    def onPlayBackEnded(self):
        clear_property('script.trakt.ids')
        clear_property('data')
        self.mark_as_watched()
        self.reset()

    def onPlayBackStopped(self):
        clear_property('script.trakt.ids')
        clear_property('data')
        if self.totalTime > 0 and self.currentTime / self.totalTime >= .9: self.mark_as_watched()
        self.reset()
