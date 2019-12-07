#
#      Copyright (C) 2013 Sean Poyser
#
#  This Program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2, or (at your option)
#  any later version.
#
#  This Program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with XBMC; see the file COPYING.  If not, write to
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
#  http://www.gnu.org/copyleft/gpl.html
#

import xbmc
import xbmcgui
import xbmcaddon
import os
import geturllib
import re
import datetime
import time
import random

URL      = 'http://www.gocomics.com'
ADDONID  = 'plugin.image.comicstrips'
CACHE    = xbmc.translatePath(os.path.join('special://profile', 'addon_data', ADDONID ,'cache'))

geturllib.SetCacheDir(CACHE)

def GetHTML(url, useCache = True, timeout=604800): #1 week
    if useCache:
        html, cached = geturllib.GetURL(url, timeout)
    else:
        html = geturllib.GetURLNoCache(url)

    html  = html.replace('\n', '')
    return html


def GetFullHTML(url, useCache = True, timeout=604800): #1 week
    agent = ' Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
    if useCache:
        html, cached = geturllib.GetURL(url, timeout, agent=agent)
    else:
        html = geturllib.GetURLNoCache(url, agent=agent)

    html  = html.replace('\n', '')
    return html


def GetRandomURL(url):
    year  = GetRandomYear( url)
    month = GetRandomMonth(url, year)
    day   = GetRandomDay(  url, year, month)
    url   = '%s/%s/%d/%d/%d' % (URL, url, year, month, day)

    return url


def GetCurrentURL(url):
    now   = datetime.datetime.today()
    year  = now.year
    month = now.month
    day   = now.day
    url   = '%s/%s/%d/%d/%d' % (URL, url, year, month, day)

    return url


def GetRandomYear(_url):
    now     = datetime.datetime.today()
    current = now.year

    try:
        url  = URL + _url
        html = GetFullHTML(url)
        min  = int(re.compile('minDate: "(.+?)/.+?/.+?"').search(html).groups(1)[0])       

        years = range(min, current+1)
        random.shuffle(years)
 
        months = range(1, 13)
    
        for year in years:
            for month in months:
                url  = '%s/calendar%s/%d/%d' % (URL, _url, year, month)
                html = eval(GetHTML(url))
                if len(html) > 0:
                    return year

    except:
        pass

    return current

def GetRandomMonth(_url, year):
    now     = datetime.datetime.today()
    current = now.month

    try:
        months = range(1, 13)
        random.shuffle(months)
    
        for month in months:
            url  = '%s/calendar%s/%d/%d' % (URL, _url, year, month)
            html = eval(GetHTML(url))
            if len(html) > 0:
                return month
    except:
        pass

    return current


def GetRandomDay(_url, year, month):
    now     = datetime.datetime.today()
    current = now.day

    try:
        url  = '%s/calendar%s/%d/%d' % (URL, _url, year, month)
        html = eval(GetHTML(url))

        if len(html) > 0:
            random.shuffle(html)
            return int(html[0].split('/')[-1])
    except:
        pass
    
    return current


def showText(heading, text, waitForClose=False):
    id = 10147

    xbmc.executebuiltin('ActivateWindow(%d)' % id)
    xbmc.sleep(100)

    win = xbmcgui.Window(id)

    retry = 50
    while (retry > 0):
        try:
            xbmc.sleep(10)
            win.getControl(1).setLabel(heading)
            win.getControl(5).setText(text)
            retry = 0
        except:
            retry -= 1

    if waitForClose:
        while xbmc.getCondVisibility('Window.IsVisible(%d)' % id) == 1:
            xbmc.sleep(50)


def showChangelog(addonID=None):
    try:
        if addonID:
            ADDON = xbmcaddon.Addon(addonID)
        else: 
            ADDON = xbmcaddon.Addon(ADDONID)

        f     = open(ADDON.getAddonInfo('changelog'))
        text  = f.read()
        title = '%s - %s' % (xbmc.getLocalizedString(24054), ADDON.getAddonInfo('name'))

        showText(title, text)

    except Exception, e:
        pass