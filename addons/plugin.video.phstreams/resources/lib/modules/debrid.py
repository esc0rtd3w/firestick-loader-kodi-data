# -*- coding: utf-8 -*-

"""
    Exodus Add-on
    Copyright (C) 2016 Exodus

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

from resources.lib.modules import log_utils

try:
    import urlresolver

    debrid_resolvers = [resolver() for resolver in urlresolver.relevant_resolvers(order_matters=True) if resolver.isUniversal()]
except:
    debrid_resolvers = []


def status():
    return debrid_resolvers != []


def resolver(url, debrid):
    try:
        debrid_resolver = [resolver for resolver in debrid_resolvers if resolver.name == debrid][0]

        debrid_resolver.login()
        _host, _media_id = debrid_resolver.get_host_and_id(url)
        stream_url = debrid_resolver.get_media_url(_host, _media_id)

        return stream_url
    except Exception as e:
        log_utils.log('%s Resolve Failure: %s' % (debrid, e), log_utils.LOGWARNING)
        return None
