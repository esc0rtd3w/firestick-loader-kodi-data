"""
 Copyright (c) 2013 Popeye

 Permission is hereby granted, free of charge, to any person
 obtaining a copy of this software and associated documentation
 files (the "Software"), to deal in the Software without
 restriction, including without limitation the rights to use,
 copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the
 Software is furnished to do so, subject to the following
 conditions:

 The above copyright notice and this permission notice shall be
 included in all copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
 OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
 HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
 WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
 OTHER DEALINGS IN THE SOFTWARE.
"""

from resources.lib import sabutils
from resources.lib.sabnzbd import Sabnzbd
from resources.lib.sabnzbd import Warnings
import xbmcgui

sabnzbd = Sabnzbd()
warnings = Warnings()


class NzoAction:
    def __init__ (self, **kwargs):
        sabutils.log("NzoAction: kwargs: %s" % kwargs)
        for key, value in kwargs.items():
            setattr(self, key, value)

    def nzo_pause(self):
        message = sabnzbd.nzo_pause(self.nzo_id)
        sabutils.container_refresh()
        sabutils.notification("Jobb paused: %s" % message)

    def nzo_resume(self):
        message = sabnzbd.nzo_resume(self.nzo_id)
        sabutils.container_refresh()
        sabutils.notification("Jobb resumed: %s" % message)

    def nzo_delete(self):
        message = sabnzbd.nzo_delete(self.nzo_id)
        sabutils.container_refresh()
        sabutils.notification("Delete: %s" % message)

    def nzo_delete_files(self):
        message = sabnzbd.nzo_delete_files(self.nzo_id)
        sabutils.container_refresh()
        sabutils.notification("Delete: %s" % message)

    def nzo_delete_history(self):
        message = sabnzbd.nzo_delete_history(self.nzo_id)
        sabutils.container_refresh()
        sabutils.notification("Remove: %s" % message)

    def nzo_delete_history_files(self):
        message = sabnzbd.nzo_delete_history_files(self.nzo_id)
        sabutils.container_refresh()
        sabutils.notification("Remove: %s" % message)

    def nzo_up(self):
        self._switch(-1)

    def nzo_down(self):
        self._switch(1)

    def _switch(self, value):
        message = sabnzbd.nzo_switch(self.nzo_id, (int(self.index) + value))
        sabutils.container_refresh()

    def nzo_change_category(self):
        dialog = xbmcgui.Dialog()
        category_list = sabnzbd.category_list()
        sabutils.log("nzo_change_category: category_list: %s" % category_list)
        category_list.remove('*')
        category_list.insert(0, 'Default')
        ret = dialog.select('Select sabnzbd category', category_list)
        category_list.remove('Default')
        category_list.insert(0, '*')
        if ret == -1:
            return
        else:
            category = category_list[ret]
            sabutils.log("nzo_change_category: category: %s" % category)
            message = sabnzbd.nzo_change_category(self.nzo_id, category)
            sabutils.container_refresh()

    def nzo_pp(self):
        dialog = xbmcgui.Dialog()
        pp_list = ['Download', '+Repair', '+Unpack', '+Delete']
        ret = dialog.select('sabnzbd Post process', pp_list)
        sabutils.log("nzo_pp: pp: %s" % ret)
        if ret == -1:
            return
        else:
            message = sabnzbd.nzo_pp(self.nzo_id, ret)
            sabutils.container_refresh()

    def nzo_retry(self):
        # TODO
        # dialog = xbmcgui.Dialog()
        # ret = dialog.yesno('sabnzbd Retry', 'Add optional supplemental NZB?', '# TODO')
        # if ret:
            # dialog = xbmcgui.Dialog()
            # nzb_file = dialog.browse(0, 'Pick a folder', 'files')
            # # XBMC outputs utf-8
            # path = unicode(nzb_file, 'utf-8')
        # else:
        message = sabnzbd.nzo_retry(self.nzo_id)
        sabutils.container_refresh()
        sabutils.notification("Retry: %s" % message)


class NzfAction:
    def __init__ (self, **kwargs):
        sabutils.log("NzfAction: kwargs: %s" % kwargs)
        for key, value in kwargs.items():
            setattr(self, key, value)

    def nzf_delete(self):
        self._file_list_position(-1)

    def nzf_top(self):
        self._file_list_position(0)

    def nzf_up(self):
        self._file_list_position(1)

    def nzf_down(self):
        self._file_list_position(2)

    def nzf_bottom(self):
        self._file_list_position(3)

    def _file_list_position(self, pos):
        sabnzbd.file_list_position(self.nzo_id, [self.nzf_id], pos)
        sabutils.container_refresh()


class SabAction:
    def __init__ (self, **kwargs):
        sabutils.log("SabAction: kwargs: %s" % kwargs)
        self.sab_kwargs = dict()
        for key, value in kwargs.items():
            if key.startswith('sab_'):
                key = key.replace('sab_', '')
                self.sab_kwargs[key] = value
            else:
                setattr(self, key, value)

    def sab_add_nzb(self):
        dialog = xbmcgui.Dialog()
        nzb_file = dialog.browse(1, 'Add a nzb', 'files', '.nzb|.zip|.gz|.rar')
        path = nzb_file
        if sabutils.exists(path):
            sabnzbd.add_file(path)
            sabutils.notification("SAB File added")
            sabutils.container_refresh()

    def sab_max_speed(self):
        dialog = xbmcgui.Dialog()
        ret = dialog.numeric(0, 'sabnzbd Max speed  in KB/s')
        if ret is not "":
            sabnzbd.max_speed(int(ret))
            sabutils.container_refresh()

    def sab_reset_speed(self):
        sabnzbd.reset_speed()
        sabutils.container_refresh()

    def sab_pause(self):
        message = sabnzbd.pause()
        sabutils.container_refresh()
        sabutils.notification("SAB paused: %s" % message)

    def sab_resume(self):
        message = sabnzbd.resume()
        sabutils.container_refresh()
        sabutils.notification("Queue resumed: %s" % message)

    def sab_delete_history_all(self):
        dialog = xbmcgui.Dialog()
        ret = dialog.yesno('sabnzbd History', 'Remove whole history', 'Are you sure?')
        if ret:
            message = sabnzbd.delete_history_all()
            sabutils.container_refresh()
            sabutils.notification("Remove: %s" % message)

    def sab_delete_history_files_all(self):
        dialog = xbmcgui.Dialog()
        ret = dialog.yesno('sabnzbd History', 'Remove all failed + delete files', 'Are you sure?')
        if ret:
            message = sabnzbd.delete_history_files_all()
            sabutils.container_refresh()
            sabutils.notification("Remove: %s" % message)

    def sab_restart(self):
        self.sab_kwargs['mode'] = 'restart'
        message = self.sab_action()
        sabutils.parent_dir()

    def sab_shutdown(self):
        self.sab_kwargs['mode'] = 'shutdown'
        message = self.sab_action()
        sabutils.parent_dir()

    def sab_action(self):
        return sabnzbd.action(**self.sab_kwargs)

    def sab_clear_warnings(self):
        warnings.clear()
        sabutils.parent_dir()
