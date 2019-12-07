# -*- coding: utf-8 -*-

'''
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
'''


import pkgutil


def sources():
    try:
        sourceDict = []
        for pkg, name, is_pkg in pkgutil.walk_packages(__path__): sourceDict.append((name, is_pkg))
        sourceDict = [i[0] for i in sourceDict if i[1] == False]
        sourceDict = [(i, __import__(i, globals(), locals(), [], -1).source()) for i in sourceDict]
        return sourceDict
    except:
        return []


