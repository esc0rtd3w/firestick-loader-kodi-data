import xbmc
import xbmcgui
import koding
import sys
import xbmcplugin


class JenPlayer(xbmc.Player):
    tablespec = {
        "columns": {
            "identifier": "TEXT",
            "season": "TEXT",
            "episode": "TEXT",
            "watched": "TEXT",
            "currentTime": "TEXT",
        },
        "constraints": {
            "unique": "identifier, season, episode"
        }
    }

    def __init__(self, resume=False):
        xbmc.Player.__init__(self)
        self.resume = resume
        self.currentTime = 0

    def setItem(self, item):
        self.identifier = item.get("imdb", "0")
        self.season = item.get("season", "0")
        self.episode = item.get("episode", "0")

    def play(self, url, item):
        if type(url) == list:
            playlist = xbmc.PlayList()
            for vid in url:
                playlist.add(vid, item)
            xbmc.Player().play(playlist, item)
        else:
            xbmc.Player().play(url, item)
        self.item = item

    def onPlayBackStarted(self):
        koding.dolog("playback started")
        xbmc.executebuiltin('Dialog.Close(all,true)')
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, self.item)

    def keep_alive(self):
        koding.dolog("staying alive")
        # keep connection alive
        self.totalTime = 0
        self.currentTime = 0

        if self.resume:
            koding.Create_Table("watched", self.tablespec)
            match = koding.Get_From_Table("watched", {
                "identifier": self.identifier,
                "season": self.season,
                "episode": self.episode
            })
            if match:
                match = match[0]
                if match["currentTime"]:
                        seconds = float(match["currentTime"])
                        xbmc.Player().seekTime(seconds)

        for i in range(0, 240):
            if self.isPlaying():
                break
            xbmc.sleep(1000)
        while self.isPlaying():
            try:
                self.totalTime = self.getTotalTime()
                self.currentTime = self.getTime()
            except:
                pass
            xbmc.sleep(2000)
        xbmc.sleep(5000)

    def onPlayBackEnded(self):
        koding.dolog("playback ended")
        if self.identifier == "0":
            return
        koding.Create_Table("watched", self.tablespec)
        try:
            koding.Remove_From_Table("watched", {
                "identifier": self.identifier,
                "season": self.season,
                "episode": self.episode
            })
        except:
            pass
        koding.Add_To_Table("watched", {
            "identifier": self.identifier,
            "season": self.season,
            "episode": self.episode,
            "watched": "1",
            "currentTime": "0"
        })
        return True

    def onPlayBackStopped(self):
        koding.dolog("playback stopped")
        if self.identifier == "0":
            return
        if not self.currentTime > 1:
            return
        koding.Create_Table("watched", self.tablespec)
        try:
            koding.Remove_From_Table("watched", {
                "identifier": self.identifier,
                "season": self.season,
                "episode": self.episode
            })
        except:
            pass
        koding.Add_To_Table("watched", {
            "identifier": self.identifier,
            "season": self.season,
            "episode": self.episode,
            "watched": "0",
            "currentTime": self.currentTime
        })
        return True
