#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
    script.tv.show.next.aired
    TV Show - Next Aired
    main_module.py
    All script methods provided by the addon
'''

import xbmc
import xbmcgui
import xbmcaddon
from thetvdb import TheTvDb
from utils import ADDON_ID, log_msg, KODI_VERSION, log_exception, DATE_FORMAT, NICE_DATE_FORMAT, NICE_DATE_NO_YEAR, NICE_SHORT_DATE
from datetime import datetime, date, timedelta
from time import strftime, strptime, time, mktime, localtime, tzname
import urlparse
import sys


class MainModule:
    '''mainmodule provides the script methods for the nextaired addon'''

    def __init__(self):
        '''Initialization and main code run'''
        self.win = xbmcgui.Window(10000)
        self.addon = xbmcaddon.Addon(ADDON_ID)
        self.thetvdb = TheTvDb()
        self.set_dates()
        action, action_param = self.get_params()
        self.improve_dates = self.addon.getSetting("ImproveDates") == 'true'
        log_msg("MainModule called with action: %s - parameter: %s" % (action, action_param))
        # launch module for action provided by this script
        try:
            getattr(self, action)(action_param)
        except Exception as exc:
            log_exception(__name__, exc)
        finally:
            self.close()

    def close(self):
        '''Cleanup Kodi Cpython instances on exit'''
        del self.win
        del self.addon
        del self.thetvdb
        log_msg("MainModule exited")

    @staticmethod
    def get_params():
        '''extract the action and it's parameter from the called script path'''
        action = "main"
        action_param = ""
        if len(sys.argv) > 1:
            arg = sys.argv[1]
            action = arg.split('=')[0].lower()
            action_param = arg.replace(action + "=", "").lower()
        return action, action_param

    def set_dates(self):
        '''set the date variables'''
        self.now = time()
        self.date = date.today()
        self.datestr = str(self.date)
        self.yesterday = self.date - timedelta(days=1)
        self.yesterstr = str(self.yesterday)
        self.tomorrow = self.date + timedelta(days=1)
        self.weekdays = []
        for j in range(11, 18):
            self.weekdays.append(xbmc.getLocalizedString(j))
        self.wdays = []
        for j in range(41, 48):
            self.wdays.append(xbmc.getLocalizedString(j))
        self.local_months = []
        for j in range(51, 63):
            self.local_months.append(xbmc.getLocalizedString(j))
        self.ampm = xbmc.getCondVisibility('String.Contains(System.Time,Am) | String.Contains(System.Time,Pm)') == 1

    def reset(self, action_param):
        '''reset and force update of all data'''
        if action_param == "true":
            dialog = xbmcgui.Dialog()
            heading = self.addon.getAddonInfo("name").decode("utf-8")
            if dialog.yesno(heading, self.addon.getLocalizedString(32213)):
                dialog = xbmcgui.DialogProgress()
                dialog.create(heading, self.addon.getLocalizedString(32214))
                self.update_data(True)
                dialog.close()
            del dialog

    def update_data(self, ignore_cache=False):
        '''updates all data we need in cache'''
        if self.win.getProperty("nextaired.update_data"):
            log_msg("Update data skipped, another update is in progress")
        else:
            self.win.setProperty("nextaired.update_data", "busy")
            # build details in cache for all continuing series in the kodi db
            log_msg("Updating TheTVDB info for all continuing Kodi tv shows...", xbmc.LOGNOTICE)
            self.thetvdb.ignore_cache = ignore_cache
            continuing_kodi_shows = self.thetvdb.get_kodishows_details(continuing_only=True)
            self.win.setProperty("NextAired.Total", "%s" % len(continuing_kodi_shows))
            # build nextaired episodes listing in cache
            log_msg("Retrieving next airing episodes for all continuing Kodi tv shows...", xbmc.LOGNOTICE)
            want_yesterday = self.addon.getSetting("WantYesterday") == 'true'
            self.thetvdb.get_kodi_unaired_episodes(include_last_episode=want_yesterday)
            # set the window properties for the shows that are airing today
            prev_total = self.win.getProperty("NextAired.TodayTotal")
            prev_total = int(prev_total) if prev_total else 0
            # clear previous properties
            for count in range(prev_total + 1):
                self.clear_properties("%s." % count)
            shows_airing_today = self.thetvdb.get_kodishows_airingtoday()
            all_titles = []
            for count, show_details in enumerate(shows_airing_today):
                self.set_properties(show_details, "%s." % count)
                all_titles.append(show_details["title"])
            self.win.setProperty("NextAired.TodayTotal", "%s" % len(shows_airing_today))
            self.win.setProperty("NextAired.TodayShow", "[CR]".join(all_titles))
            self.thetvdb.ignore_cache = False
            self.win.clearProperty("nextaired.update_data")
            log_msg("Update complete", xbmc.LOGNOTICE)

    def force(self, action_param):
        '''force update of data by script - calls update_data after user confirmation'''
        if action_param == "true":
            dialog = xbmcgui.DialogProgress()
            dialog.create(self.addon.getAddonInfo("name").decode("utf-8"), self.addon.getLocalizedString(32215))
            self.update_data()
            dialog.close()
            del dialog

    def update(self, action_param):
        '''perform update of data in cache - called by the background service'''
        if action_param == "true":
            self.update_data()

    def updateshow(self, showtitle):
        '''force update of single show'''
        if showtitle:
            log_msg("Update show data requested for TV Show: %s" % showtitle)
            self.win.setProperty("nextaired.update_data", "busy")
            self.thetvdb.ignore_cache = True
            self.thetvdb.get_kodishow_details(showtitle)
            self.thetvdb.ignore_cache = False
            self.win.clearProperty("nextaired.update_data")

    def tvshowtitle(self, showtitle, prefix=""):
        '''set details for single show by name'''
        log_msg("Set NextAired properties for TV Show: %s" % showtitle)
        details = self.thetvdb.get_kodishow_details(showtitle)
        if not details or not showtitle:
            self.clear_properties(prefix)
        else:
            self.set_properties(details, prefix)

    def backend(self, action_param):
        '''start monitoring listitem details to set window properties'''
        if not action_param or action_param == "false" or self.win.getProperty("NextAired.backend"):
            log_msg("Start backend aborted, required param missing or backend already running")
            return
        log_msg("Monitoring of listitems started...")
        self.win.setProperty("NextAired.backend", "running")
        try:

            # try parsing the multi-attributes
            li_range_left, li_range_right = self.get_listitem_range(action_param)
            monitor = xbmc.Monitor()
            last_showtitle = ""
            while not monitor.abortRequested() and xbmc.getCondVisibility("Window.IsActive(10025)"):
                showtitle = xbmc.getInfoLabel("ListItem.TvShowTitle").decode("utf-8")
                if showtitle != last_showtitle:
                    last_showtitle = showtitle
                    self.tvshowtitle(showtitle)
                    if li_range_left or li_range_right:
                        # set properties for the given listitem range
                        for count in range(li_range_left, li_range_right):
                            showtitle = xbmc.getInfoLabel("ListItem(%s).TvShowTitle" % count).decode("utf-8")
                            self.tvshowtitle(showtitle, "(%s)" % count)
                monitor.waitForAbort(0.5)
            # clear properties when exiting video library
            if not monitor.abortRequested():
                self.clear_properties()
                if li_range_left or li_range_right:
                    for count in range(li_range_left, li_range_right):
                        self.clear_properties("(%s)" % count)
            del monitor
        except Exception as exc:
            log_exception(__name__, exc)
        finally:
            self.win.clearProperty("NextAired.backend")
        log_msg("Monitoring of listitems ended...")

    @staticmethod
    def get_listitem_range(paramstr):
        '''get the special range params from the parameter string'''
        li_range_left = 0
        li_range_right = 0
        if paramstr != "true":
            try:
                li_range_right = int(paramstr.split(" ")[1])
                li_range_left = int(paramstr.split(" ")[0])
                li_range_right += 1
            except Exception:
                pass
        return li_range_left, li_range_right

    def set_properties(self, details, prefix=""):
        '''set the window properties for the given show'''
        self.win.setProperty("NextAired%s.Label" % prefix, details["title"])
        self.win.setProperty("NextAired%s.Thumb" % prefix, details["art"].get("thumb"))
        self.win.setProperty("NextAired%s.AirTime" % prefix, details["airdaytime"])
        self.win.setProperty("NextAired%s.Path" % prefix, details["file"])
        self.win.setProperty("NextAired%s.Library" % prefix, "videodb://tvshows/titles/%s/" % details["tvshowid"])
        self.win.setProperty("NextAired%s.Status" % prefix, details["status"])
        self.win.setProperty("NextAired%s.Network" % prefix, " / ".join(details["studio"]))
        self.win.setProperty("NextAired%s.Started" % prefix, details["firstaired"])
        self.win.setProperty("NextAired%s.Classification" % prefix, details["classification"])
        self.win.setProperty("NextAired%s.Genre" % prefix, " / ".join(details["genre"]))
        self.win.setProperty("NextAired%s.Premiered" % prefix, str(details["year"]))
        self.win.setProperty("NextAired%s.Runtime" % prefix, str(details["runtime"]))
        self.win.setProperty("NextAired%s.FanArt" % prefix, details["art"]["fanart"])
        if details.get("next_episode"):
            # set next airing episode details if exist
            self.win.setProperty("NextAired%s.NextDate" % prefix, details["next_episode"]["airdate"])
            self.win.setProperty("NextAired%s.NextDay" % prefix, details["next_episode"]["airdate.long"])
            self.win.setProperty("NextAired%s.NextTitle" % prefix, details["next_episode"]["title"])
            nextnumber = "%sx%s" % (details["next_episode"]["season"], details["next_episode"]["episode"])
            self.win.setProperty("NextAired%s.NextNumber" % prefix, nextnumber)
            self.win.setProperty("NextAired%s.NextEpisodeNumber" % prefix, str(details["next_episode"]["episode"]))
            self.win.setProperty("NextAired%s.NextSeasonNumber" % prefix, str(details["next_episode"]["season"]))
        else:
            # clear next episode properties if we don't have that data
            for prop in ["NextDate", "NextDay", "NextTitle", "NextNumber", "NextEpisodeNumber", "NextSeasonNumber"]:
                self.win.clearProperty("NextAired%s.%s" % (prefix, prop))
        if details.get("last_episode"):
            self.win.setProperty("NextAired%s.LatestDate" % prefix, details["last_episode"]["airdate"])
            self.win.setProperty("NextAired%s.LatestDay" % prefix, details["last_episode"]["airdate.long"])
            self.win.setProperty("NextAired%s.LatestTitle" % prefix, details["last_episode"]["title"])
            nextnumber = "%sx%s" % (details["last_episode"]["season"], details["last_episode"]["episode"])
            self.win.setProperty("NextAired%s.LatestNumber" % prefix, nextnumber)
            self.win.setProperty("NextAired%s.LatestEpisodeNumber" % prefix, str(details["last_episode"]["episode"]))
            self.win.setProperty("NextAired%s.LatestSeasonNumber" % prefix, str(details["last_episode"]["season"]))
        else:
            # clear last episode properties if we don't have that data
            for prop in ["LatestDate", "LatestDay", "LatestTitle",
                         "LatestNumber", "LatestEpisodeNumber", "LatestSeasonNumber"]:
                self.win.clearProperty("NextAired%s.%s" % (prefix, prop))
        self.win.setProperty("NextAired%s.Airday" % prefix, details["airday"])
        self.win.setProperty("NextAired%s.ShortTime" % prefix, details["airtime"])
        self.win.setProperty("NextAired%s.Art(poster)" % prefix, details["art"].get("poster"))
        self.win.setProperty("NextAired%s.Art(banner)" % prefix, details["art"].get("banner"))
        self.win.setProperty("NextAired%s.Art(fanart)" % prefix, details["art"].get("fanart"))
        self.win.setProperty("NextAired%s.Art(landscape)" % prefix, details["art"].get("landscape"))
        self.win.setProperty("NextAired%s.Art(clearlogo)" % prefix, details["art"].get("clearlogo"))
        self.win.setProperty("NextAired%s.Art(characterart)" % prefix, details["art"].get("characterart"))

    def clear_properties(self, prefix=""):
        '''clears the nextaired window Properties'''
        props = ["label", "thumb", "airtime", "path", "library", "status", "statusid", "network", "started",
                 "classification", "genre", "premiered", "country", "runtime", "fanart", "airstoday", "nextdate",
                 "nextday", "nexttitle", "nextnumber", "nextepisodenumber", "nextseasonnumber", "latestdate",
                 "latestday", "latesttitle", "latestnumber", "latestepisodenumber", "latestseasonnumber", "airday",
                 "shorttime", "art(poster)", "art(banner)", "art(fanart)", "art(landscape)"]
        for prop in props:
            self.win.clearProperty("NextAired%s.%s" % (prefix, prop))

    def main(self, action_param=None):
        '''show the NextAired dialog'''
        weekday = self.date.weekday()
        self.win.setProperty("NextAired.TodayText", xbmc.getLocalizedString(33006))
        self.win.setProperty("NextAired.TomorrowText", xbmc.getLocalizedString(33007))
        self.win.setProperty("NextAired.YesterdayText", self.addon.getLocalizedString(32018))
        self.win.setProperty("NextAired.TodayDate", self.str_date(self.date, 'DropYear'))
        self.win.setProperty("NextAired.TomorrowDate", self.str_date(self.tomorrow, 'DropThisYear'))
        self.win.setProperty("NextAired.YesterdayDate", self.str_date(self.yesterday, 'DropThisYear'))
        for count in range(0, 7):
            wdate = self.date
            if count != weekday:
                wdate += timedelta(days=(count - weekday + 7) % 7)
            self.win.setProperty("NextAired.%d.Date" % (count + 1), self.str_date(wdate, 'DropThisYear'))
        from next_aired_dialog import NextAiredDialog
        today_style = self.addon.getSetting("TodayStyle") == 'true'
        scan_days = int(self.addon.getSetting("ScanDays2" if today_style else "ScanDays"))
        want_yesterday = self.addon.getSetting("WantYesterday") == 'true'
        eps_list = self.get_nextaired_listing(include_last_episode=want_yesterday)
        xml = "script-NextAired-TVGuide%s.xml" % (2 if today_style else "")
        xml_path = self.addon.getAddonInfo('path').decode('utf-8')
        dialog = NextAiredDialog(
            xml,
            xml_path,
            "Default",
            listing=eps_list,
            nice_date=self.nice_date,
            scan_days=scan_days,
            today_style=today_style,
            want_yesterday=want_yesterday)
        dialog.doModal()
        del dialog

    def get_nextaired_listing(self, include_last_episode=False):
        '''get the listing of all continuing series, include last episode and unaired episodes'''
        eps_list = self.thetvdb.get_kodi_unaired_episodes(
            single_episode_per_show=False, include_last_episode=include_last_episode)
        return eps_list

    def str_date(self, d, style=None):
        '''The style setting only affects "nice" dates, not the historic format.'''
        if d is None:
            return ''
        return self.nice_date(d, style) if self.improve_dates else d.strftime(DATE_FORMAT)

    def nice_date(self, d, style=None):
        '''Specify style DropThisYear, DropYear, or Short (or omit for the full info).'''
        tt = d.timetuple()
        if style == 'Short':
            fmt = NICE_SHORT_DATE
        elif style == 'DropYear' or (style == 'DropThisYear' and tt[0] == self.date.year):
            fmt = NICE_DATE_NO_YEAR
        else:
            fmt = NICE_DATE_FORMAT
        d = fmt % {
            'year': tt[0],
            'mm': tt[1],
            'month': self.local_months[
                tt[1] - 1],
            'day': tt[2],
            'wday': self.wdays[
                tt[6]],
            'unk': '??'}
        return d
