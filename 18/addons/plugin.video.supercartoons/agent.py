
#
#      Copyright (C) 2016 Sean Poyser
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


import random


def getUserAgent():
    agents = []

    agents.append('Mozilla/5.0 (Android; Mobile; rv:%d.0) Gecko/%d.0 Firefox/%d.0')
    agents.append('Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.%d (KHTML, like Gecko) Chrome/%d.0.1847.114 Mobile Safari/537.%d')
    agents.append('Mozilla/5.0 (iPad; CPU OS 7_0_4 like Mac OS X) AppleWebKit/5%d.51.1 (KHTML, like Gecko) CriOS/%d.0.1847.%d Mobile/11B554a')
    agents.append('Mozilla/5.0 (iPad; CPU OS 7_0_4 like Mac OS X) AppleWebKit/5%d.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11B5%da Safari/9537.%d')
    agents.append('Mozilla/5.0 (iPhone; CPU OS 7_0_4 like Mac OS X) AppleWebKit/5%d.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11B%d4a Safari/9537.%d')
    agents.append('Mozilla/5.0 (Android; Mobile; rv:%d.0) Gecko/%d.0 Firefox/%d.0')

    agent = random.choice(agents) % (random.randint(10, 40), random.randint(10, 40), random.randint(10, 40))

    return '?|User-Agent=%s' % agent
