# -*- coding: utf-8 -*-

"""
    views.py --- functions to persist selected content views to database
    Copyright (C) 2017, Jen

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, ordepends
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import xbmc
import xbmcgui
import xbmcaddon
import koding
from koding import route
from language import get_string as _

view_spec = {
    "columns": {
        "skin": "TEXT",
        "content": "TEXT",
        "viewid": "INTEGER"
    },
    "constraints": {
        "unique": "skin, content",
    }
}


@route("get_view_id")
def get_view_id():
    listlabel = xbmc.getInfoLabel("ListItem.Label")
    viewid = ""
    for x in range(50, 5000):
        label = xbmc.getInfoLabel('Control.GetLabel(%s)' % (x))
        if listlabel in label:
            viewid = x
            break
    return viewid


@route("save_view_mode", ["url"])
def save_view_mode(content):
    viewid = get_view_id()
    skin = xbmc.getSkinDir()
    koding.Create_Table("addonviews", view_spec)
    koding.Remove_From_Table(
        "addonviews", {"skin": skin,
                       "content": content})
    koding.Add_To_Table("addonviews", {
        "skin": skin,
        "content": content,
        "viewid": viewid,
    })
    icon = xbmcaddon.Addon().getAddonInfo('icon')
    xbmcgui.Dialog().notification(xbmcaddon.Addon().getAddonInfo('name'),
                                  _("View set for %s") % content,
                                  icon)


def set_list_view_mode(content):
    skin = xbmc.getSkinDir()
    koding.reset_db()
    match = koding.Get_From_Table("addonviews", {
        "skin": skin,
        "content": content
    })
    if match:
        match = match[0]
        xbmc.executebuiltin('Container.SetViewMode(%s)' % str(match["viewid"]))
