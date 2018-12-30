

class ScraperVideo:
    def __init__(self, video_type, title, year, trakt_id, season='', episode='', ep_title='', ep_airdate=''):
        self.video_type = video_type
        if isinstance(title, unicode):
            self.title = title.encode('utf-8')
        else:
            self.title = title
        self.year = str(year)
        self.season = season
        self.episode = episode
        if isinstance(ep_title, unicode):
            self.ep_title = ep_title.encode('utf-8')
        else:
            self.ep_title = ep_title
        self.trakt_id = trakt_id
        self.ep_airdate = None

    def __str__(self):
        return '|%s|%s|%s|%s|%s|%s|%s|' % (
        self.video_type, self.title, self.year, self.season, self.episode, self.ep_title, self.ep_airdate)
