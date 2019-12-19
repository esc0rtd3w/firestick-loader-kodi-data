#
#       Copyright (C) 2014-2015
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


import inspect
FILENAME = inspect.getfile(inspect.currentframe())


def _select(index):
    import utils
    if index < 0:
        return

    import xbmc
    import utils 

    view  = 0
    count = 50
    while view < 1 and count > 0:
        count -= 1
        view   = utils.getViewType()
        xbmc.sleep(50)

    if view < 1:
        return

    import xbmcgui

    win   = None
    count = 10
    while not win and count > 0:
        count -= 1
        try:    win = xbmcgui.Window(utils.getCurrentWindowId())
        except: xbmc.sleep(50)

    if not win:
        return

    list  = None
    count = 10
    while not list and count > 0:
        try:    list = win.getControl(view)
        except: xbmc.sleep(50)

    if not list:
        return

    xbmc.sleep(50)

    try:    
        nItem = int(xbmcgui.Window(10000).getProperty('SF_NMR_ITEMS'))
        if index >= nItem:           
            index = nItem-1
    except:
        pass

    list.selectItem(index)


def select(index):
    import utils
    import xbmc
    import os  

    HOME = utils.HOME

    name      = 'select'
    script    = FILENAME
    args      = '%d' % index
    cmd       = 'AlarmClock(%s,RunScript(%s,%s),%d,True)' % (name, script, args, 0)

    xbmc.executebuiltin('CancelAlarm(%s,True)' % name)  
    xbmc.executebuiltin(cmd) 
    utils.log(cmd, True)


if __name__ == '__main__':
    if FILENAME.endswith(sys.argv[0]):
        try:    _select(int(sys.argv[1]))
        except: pass