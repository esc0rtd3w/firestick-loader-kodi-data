"""
    SALTS XBMC Addon
    Copyright (C) 2015 tknorris

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import xbmcaddon
import strings
import log_utils

def i18n(string_id):
    try:
        return xbmcaddon.Addon().getLocalizedString(strings.STRINGS[string_id]).encode('utf-8', 'ignore')
    except Exception as e:
        log_utils.log('Failed String Lookup: %s (%s)' % (string_id, e))
        return string_id
