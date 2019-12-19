from time import mktime
from datetime import date, timedelta, datetime
import xbmc
import xbmcgui
import xbmcaddon
import time
from utils import ADDON_ID, log_msg, KODI_VERSION, log_exception


class NextAiredDialog(xbmcgui.WindowXML):

    def __init__(self, *args, **kwargs):
        xbmcgui.WindowXML.__init__(self)
        self.win = xbmcgui.Window(10000)
        self.addon = xbmcaddon.Addon(ADDON_ID)
        self.eps_list = kwargs['listing']
        self.nice_date = kwargs['nice_date']
        self.scan_days = kwargs['scan_days']
        self.today_style = kwargs['today_style']
        self.want_yesterday = kwargs['want_yesterday']
        self.today_str = str(date.today())
        # We allow today + 2 weeks worth of "upcoming" days.
        if self.scan_days > 15:
            self.scan_days = 15
        if self.today_style:
            if self.want_yesterday:
                self.scan_days += 1
            self.cntr_cnt = self.scan_days
        else:
            self.cntr_cnt = 7
            self.want_yesterday = False

    def onInit(self):
        self.settings_open = False
        self.start_day = date.today()

        if not self.today_style:
            self.first_num = 200
            shift_cnt = self.start_day.weekday()
        elif self.want_yesterday:
            self.first_num = 200
            shift_cnt = 0
            self.start_day -= timedelta(days=1)  # start with yesterday
        else:
            self.first_num = 201
            shift_cnt = 0

        self.cntr_nums = range(self.first_num, self.first_num + self.cntr_cnt)
        for j in range(shift_cnt):
            self.cntr_nums.append(self.cntr_nums.pop(0))

        self.set_properties()
        self.fill_containers()
        self.set_focus()

    def close_dialog(self):
        '''when we should close our dialog'''
        del self.win
        del self.addon
        self.close()

    def set_properties(self):
        self.listitems = []
        ndx = 0
        for c in self.cntr_nums:
            self.listitems.append([])
            cntr_day = self.start_day + timedelta(days=ndx)
            wday = xbmc.getLocalizedString(cntr_day.weekday() + 41)
            weekday = xbmc.getLocalizedString(cntr_day.weekday() + 11)
            nice_date = self.nice_date(cntr_day, 'Short')
            self.win.setProperty('NextAired.%d.Wday' % c, wday)
            self.win.setProperty('NextAired.%d.Date' % c, nice_date)
            self.win.setProperty('NextAired.%d.Weekday' % c, weekday)
            ndx += 1
        for c in range(200, 216):
            if c not in self.cntr_nums:
                self.win.clearProperty('NextAired.%d.Wday' % c)
                self.win.clearProperty('NextAired.%d.Date' % c)
                self.win.clearProperty('NextAired.%d.Weekday' % c)
        min_day = str(self.start_day)
        mid_day = str(self.start_day + timedelta(days=6))
        max_day = str(self.start_day + timedelta(days=self.scan_days - 1))
        episodes = []
        for eps in self.eps_list:
            aired = eps['firstaired']
            if (aired < min_day) or (aired > max_day):
                continue
            episodes.append((aired, eps))
        episodes.sort(key=lambda x: x[0])

        for aired, eps in episodes:
            listitem = self.create_listitem(eps)
            if self.today_style:
                try:
                    aired = datetime.strptime(aired, '%Y-%m-%d').date()
                except TypeError:
                    aired = datetime(*(time.strptime(aired, '%Y-%m-%d')[0:6])).date()
                ndx = (aired - self.start_day).days
            else:
                ndx = eps['airday.int'] - 1
                second_week = 1 if aired > mid_day else 0
                listitem.setProperty('SecondWeek', str(second_week))
            self.listitems[ndx].append(listitem)

    def fill_containers(self):
        if self.today_style and self.want_yesterday:
            self.cntr_nums.append(self.cntr_nums.pop(0))
        for c in self.cntr_nums:
            self.getControl(c).reset()
            self.getControl(c).addItems(self.listitems[c - self.first_num])

    def set_focus(self):
        focus_to = 8
        for c in self.cntr_nums:
            if self.listitems[c - self.first_num]:
                focus_to = c
                break
        self.setFocus(self.getControl(focus_to))

    def onClick(self, controlID):
        if controlID == 8:
            self.settings_open = True
            self.addon.openSettings()
            self.close()
        elif controlID in self.cntr_nums:
            listitem = self.getControl(controlID).getSelectedItem()
            filename = 'ActivateWindow(Videos,%s,return)' % listitem.getProperty('Path')
            log_msg(filename)
            xbmc.executebuiltin(filename)

    def onFocus(self, controlID):
        pass

    def onAction(self, action):
        if self.settings_open and action.getId() in (7, 10, 92, ):
            self.settings_open = False
        if action.getId() in (9, 10, 92, 216, 247, 257, 275, 61467, 61448, ):
            self.close_dialog()

    def create_listitem(self, item):
        '''create a listitem from the episode details'''
        label = item["tvshowtitle"]
        liz = xbmcgui.ListItem(label, item.get("file", ""))
        is_today = 'True' if item['firstaired'] == self.today_str else 'False'
        genres = " / ".join(item.get("genre", []))
        studio = " / ".join(item.get("studio", []))
        infolabels = {
            "title": item["title"],
            "genre": genres,
            "rating": item.get("rating", ""),
            "director": " / ".join(item.get("director", [])),
            "plot": item["plot"],
            "duration": item.get("runtime"),
            "studio": studio,
            "writer": " / ".join(item.get("writer")),
            "tvshowtitle": item["tvshowtitle"],
            "status": item["tvshow.status"],
            "code": item.get("imdbnumber"),
            "imdbnumber": item.get("imdbnumber"),
            "aired": item["firstaired"],
            "season": item['season'],
            "episode": item['episode'],
            "mediatype": "episode"
        }
        liz.setInfo(type="Video", infoLabels=infolabels)
        art = {}
        for key, value in item["art"].items():
            if not isinstance(value, list):
                art[key] = value
                key = key.replace("tvshow.", "")
                liz.setProperty("Art(%s)" % key, value)
                liz.setProperty(key, value)
        liz.setArt(art)
        liz.setProperty("Label", label)
        liz.setProperty("Thumb", item["art"].get("thumb"))
        liz.setProperty("AirTime", item["airdatetime"])
        liz.setProperty("NextDate", item["airdate"])
        liz.setProperty("NextDay", item["airdate.long"])
        liz.setProperty("NextTitle", item["title"])
        liz.setProperty("NextNumber", "%sx%s" %(item["season"], item["episode"]))
        liz.setProperty("NextEpisodeNumber", str(item["episode"]))
        liz.setProperty("NextSeasonNumber", str(item["season"]))
        liz.setProperty("Path", item["file"])
        liz.setProperty("Library", item.get("library",""))
        liz.setProperty("Status", item["tvshow.status"])
        liz.setProperty("Network", studio)
        liz.setProperty("Started", item["tvshow.firstaired"])
        liz.setProperty("Classification", item.get("classification",""))
        liz.setProperty("Genre", genres)
        liz.setProperty("Premiered", str(item.get("year","")))
        liz.setProperty("Started", item["tvshow.firstaired"])
        liz.setProperty("Runtime", str(item.get("runtime", 0)))
        liz.setProperty("AirsToday", is_today)
        liz.setProperty("AirDay", item["airday"])
        liz.setProperty("ShortTime", item["airtime"])
        return liz
