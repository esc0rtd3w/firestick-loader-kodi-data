# all code developed by demons_are_real - https://www.reddit.com/user/demons_are_real

import urllib, json

class Feed(object):
    _tvStation = None
    _mediaId = None

    def __init__(self,tvStation,mediaId):
        self._tvStation = tvStation
        self._mediaId = mediaId

    def viewable(self): return True

    @property
    def tvStation(self):
        return self._tvStation
    @property
    def mediaId(self):
        return self._mediaId
    @staticmethod
    def fromContent(content):
        def fromItem(item):
            mediaFeedType = item["mediaFeedType"]
            print "fromContent: " + mediaFeedType
            if mediaFeedType == "HOME":
                return Home(item["callLetters"],item["mediaPlaybackId"])
            elif mediaFeedType == "NATIONAL":
                return National(item["callLetters"],item["mediaPlaybackId"])
            elif mediaFeedType == "AWAY":
                return Away(item["callLetters"],item["mediaPlaybackId"])
            elif mediaFeedType == "FRENCH":
                return French(item["callLetters"],item["mediaPlaybackId"])
            elif mediaFeedType == "COMPOSITE":
                return Composite(item["callLetters"],item["mediaPlaybackId"])
            else:
                return NonViewable(item["callLetters"],item["mediaPlaybackId"])

        if "media" in content:
            return [fromItem(item) 
                for stream in content["media"]["epg"] if stream["title"] == "NHLTV"
                for item in stream["items"]]
        else:
            return []

class Home(Feed):
    def __init__(self,tvStation,mediaId):
        Feed.__init__(self,tvStation,mediaId)
    def __repr__(self):
        return "%s [COLOR blue](Home)[/COLOR]" % (self.tvStation)

class NonViewable(Feed):
    def __init__(self,tvStation,mediaId):
        Feed.__init__(self,tvStation,mediaId)

    def __repr__(self): return "NonViewable"

    def viewable(self): 
        return False

class Away(Feed):
    def __init__(self,tvStation,mediaId):
        Feed.__init__(self,tvStation,mediaId)
    def __repr__(self): return "%s [COLOR red](Away)[/COLOR]" % (self.tvStation)

class National(Feed):
    def __init__(self,tvStation,mediaId):
        Feed.__init__(self,tvStation,mediaId)
    def __repr__(self): return "%s [COLOR blue](National)[/COLOR]" % (self.tvStation)

class French(Feed):
    def __init__(self,tvStation,mediaId):
        Feed.__init__(self,tvStation,mediaId)
    def __repr__(self): return "%s [COLOR teal](French)[/COLOR]" % (self.tvStation)

class Composite(Feed):
    def __init__(self,tvStation,mediaId):
        Feed.__init__(self,tvStation,mediaId)
    def __repr__(self): return "3-Way Camera [COLOR yellow](Composite)[/COLOR]"


class Game:
    _home = None
    _away = None
    _time = None
    _gameState = None
    _timeRemaining = None 
    _awayFull = None 
    _homeFull = None
    _id = None
    _feeds = []

    def __repr__(self):
        print str(self.feeds) + " " + str(len(self.feeds))
        return "Game(%s vs. %s, %s, feeds: %s)" % (self.away,self.home,self.timeRemaining,", ".join(map(lambda f: f.tvStation, self.feeds)))

    def __init__(self,id,away,home,time,gameState,timeRemaining,awayFull,homeFull,feeds = []):
        self._id = id
        self._away = away
        self._home = home
        self._time = time
        self._gameState = gameState
        self._timeRemaining = timeRemaining
        self._awayFull = awayFull
        self._homeFull = homeFull
        if feeds is None:
            self._feeds = []
        else:
            self._feeds = feeds
    @property
    def id(self):
        return self._id
    @property
    def away(self):
        return self._away
    @property
    def home(self):
        return self._home
    @property
    def time(self):
        return self._time
    @property
    def gameState(self):
        return self._gameState
    @property
    def timeRemaining(self):
        return self._timeRemaining
    @property
    def awayFull(self):
        return self._awayFull
    @property
    def homeFull(self):
        return self._homeFull
    @property
    def feeds(self):
        return self._feeds
    
    @staticmethod
    def fromDate(config,date):
        url = config.get("NHLTvSchedule","GameScheduleUrl") % (date,date)
        print "URL -> " + url
        response = urllib.urlopen(config.get("NHLTvSchedule","GameScheduleUrl") % (date,date))
        data = json.loads(response.read())
        if data["totalItems"] <= 0 or len(data["dates"]) == 0:
            return []
        games = data["dates"][0]["games"]
        def asGame(g):
            def remaining(state):
                if "In Progress" in state:
                    return g["linescore"]["currentPeriodOrdinal"] + " - " + g["linescore"]["currentPeriodTimeRemaining"]
                elif state == "Final":
                    return "Final"
                else:
                    return "N/A"
            away = g["teams"]["away"]["team"]
            home = g["teams"]["home"]["team"]
            time = g["gameDate"][11:].replace("Z", "") 
            state = g["status"]["detailedState"]
            return Game(g["gamePk"],
                    away["abbreviation"],
                    home["abbreviation"],
                    "TBD" if time == "04:00:00" else time,
                    state,
                    remaining(state),
                    away["name"],
                    home["name"],
                    Feed.fromContent(g["content"]))
        return map(asGame, games)

