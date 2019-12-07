# -*- coding: utf-8 -*-

"""
    messages.py ---
    Copyright (C) 2017, Jen

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
import random
from resources.lib.plugin import run_hook


def get_link_message():
    """
    helper function to get a random message when selecting links
    """
    import random
    messages = run_hook("get_link_message")
    if not messages:
        messages = [
            {
                'HD': '',
                'SD': ''
            }
        ]

    if xbmcaddon.Addon().getSetting('disable_messages') == 'true':
        message = {
            'HD': '',
            'SD': ''
        }
    else:
        message = random.choice(messages)
    return message


def get_searching_message(preset):
    """
    helper function to select a message for video items
    Args:
        preset: search quality preset ("HD", "SD" or None)
    Returns:
        random message for video items
    """
    messages = run_hook("get_searching_message", preset)
    if not messages:
        if xbmcaddon.Addon().getSetting('disable_messages') == "true":
            return ' '
        messages = [
            '',
        ]
    return random.choice(messages)
