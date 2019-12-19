#
#       Copyright (C) 2014-
#       Sean Poyser (seanpoyser@gmail.com)
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

import sfile


def getParams(file):
    params = {}

    try:
        config = []
        config = sfile.readlines(file)
    except Exception, e:
        return None

    for line in config:
        items = line.split('=', 1)
        try:    params[items[0]] = items[1]
        except: pass

    return params


def getParam(param, cfg):
    if isinstance(cfg, dict):
        try:    return cfg[param]
        except: return None
        
    try:
        config = []
        config = sfile.readlines(cfg)
    except Exception, e:
        return None

    param  += '='
    for line in config:
        if line.startswith(param):
            return line.split(param, 1)[-1].strip()
    return None


def clearParam(param, file):
    setParam(param, '', file)


def setParam(param, value, file):
    config = []
    try:
        param  = param.upper() + '='
        config = sfile.readlines(file)
    except:
        pass

    value = str(value)
        
    copy = []
    for line in config:
        line = line.strip()
        if (len(line) > 0) and (not line.startswith(param)):
            copy.append(line)

    if len(value) > 0:
        copy.append(param + value)

    f = sfile.file(file, 'w')

    for line in copy:
        f.write(line)
        f.write('\n')
    f.close()
