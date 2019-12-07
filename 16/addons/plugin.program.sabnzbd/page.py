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

import builder
from resources.lib import sabutils
from resources.lib.sabnzbd import Queue, Nzo, History, Warnings
import time
import xbmcgui


class Page:
    def __init__(self, **kwargs):
        sabutils.log("Page: kwargs: %s" % kwargs)
        for key, value in kwargs.items():
            setattr(self, key, value)

    def page_main(self):
        page = builder.PageBuilder()
        queue = Queue()
        # Status
        status = "SABnzbd %s" % queue.version
        if queue.status.lower() == "paused":
            status = "%s - Paused" % status
        elif queue.status.lower() == "idle":
            status = "%s - Idle" % status
        else:
            status = "%s - %sB/s  - %s%% - %s" % (status, queue.speed, \
                                           self._quote(queue.mb, queue.mbleft), \
                                           queue.timeleft)
        page.add(info_labels={'title':status,}, \
                 path='&mode=page_refresh', \
                 cm=self._cm_status(queue),)
        # List nzo
        for nzo in queue.nzo_list:
            title = "%s %s%% %s - %s" % (nzo.status, nzo.percentage, nzo.size, nzo.filename)
            path = "&mode=dialog_queue_details&nzo_id=%s" % nzo.nzo_id
            size = int(round(float(nzo.mb) * 1024))
            page.add(info_labels={'title':title,'size': size,}, \
                     path=path, \
                     cm=self._cm_nzo(nzo))
        # History
        page.add(info_labels={'title':'History',}, path='&mode=page_history&start=0&limit=100')
        if queue.have_warnings != "0":
            page.add(info_labels={'title':'Warnings',}, path='&mode=page_warnings')
        page.show()

    def page_refresh(self):
        sabutils.container_refresh()

    def page_parent_dir(self):
        sabutils.parent_dir()

    def _cm_status(self, queue):
        if queue.status.lower() == "paused":
            pause_resume = ("Resume", "&mode=sab_resume")
        else:
            pause_resume = ("Pause", "&mode=sab_pause")
        if queue.speedlimit != "":
            speedlimit = ("Reset speed limit", "&mode=sab_reset_speed")
        else:
            speedlimit = ("Max speed", "&mode=sab_max_speed")
        cm_nzf_details = [("Add nzb", "&mode=sab_add_nzb"),
                          speedlimit,
                          pause_resume,
                          ("Restart", "&mode=sab_restart"),
                          ("Shutdown", "&mode=sab_shutdown")
                         ]
        cm = builder.CmBuilder()
        cm.add_list(cm_nzf_details)
        return cm.list
        pass

    def _cm_nzo(self, nzo):
        if nzo.status.lower() == "paused":
            pause_resume = ("Resume", "&mode=nzo_resume&nzo_id=%s" % nzo.nzo_id)
        else:
            pause_resume = ("Pause", "&mode=nzo_pause&nzo_id=%s" % nzo.nzo_id)
        cm_nzo_details = [pause_resume,
                          ("Move up", "&mode=nzo_up&nzo_id=%s&index=%s" % (nzo.nzo_id, nzo.index)),
                          ("Move down", "&mode=nzo_down&nzo_id=%s&index=%s" % (nzo.nzo_id, nzo.index)),
                          ("Category", "&mode=nzo_change_category&nzo_id=%s" % nzo.nzo_id),
                          ("Post process", "&mode=nzo_pp&nzo_id=%s" % nzo.nzo_id),
                          ("Delete", "&mode=nzo_delete_files&nzo_id=%s" % nzo.nzo_id)
                         ]
                         # priority
        cm = builder.CmBuilder()
        cm.add_list(cm_nzo_details)
        cm.insert_cu(0, "Manage files", "&mode=page_nzo_details&nzo_id=%s" % nzo.nzo_id)
        return cm.list

    def page_nzo_details(self):
        page = builder.PageBuilder()
        nzo = Nzo(self.nzo_id)
        active = [nzf for nzf in nzo.nzf_list() if nzf.status.lower() == "active"]
        for nzf in active:
            title = "%s%% - %s" % (self._quote(nzf.mb, nzf.mbleft), nzf.filename)
            path = "&mode=page_nzf_details&nzo_id=%s&nzf_id=%s" % (nzo.nzo_id, nzf.nzf_id)
            cm = self._cm_nzf(nzo, nzf)
            page.add(info_labels={'title':title, \
                                   'size': int(nzf.bytes.replace('.00', '')),}, \
                     path=path, \
                     cm=cm, \
                     is_folder=False)
        page.show()

    def _cm_nzf(self, nzo, nzf):
        cm_nzf_details = [("Delete", "&mode=nzf_delete&nzo_id=%s&nzf_id=%s" % (nzo.nzo_id, nzf.nzf_id)),
                          ("Top", "&mode=nzf_top&nzo_id=%s&nzf_id=%s" % (nzo.nzo_id, nzf.nzf_id)),
                          ("Up", "&mode=nzf_up&nzo_id=%s&nzf_id=%s" % (nzo.nzo_id, nzf.nzf_id)),
                          ("Down", "&mode=nzf_down&nzo_id=%s&nzf_id=%s" % (nzo.nzo_id, nzf.nzf_id)),
                          ("Bottom", "&mode=nzf_bottom&nzo_id=%s&nzf_id=%s" % (nzo.nzo_id, nzf.nzf_id))
                         ]
        cm = builder.CmBuilder()
        cm.add_list(cm_nzf_details)
        return cm.list

    def page_nzf_details(self):
        sabutils.container_refresh()

    def page_history(self):
        page = builder.PageBuilder()
        queue = History(int(self.start), int(self.limit))
        for nzo in queue.nzo_list:
            if nzo.status.lower() == "failed":
                title = "* Failed - %s" % (nzo.name)
            else:
                title = "%s" % (nzo.name)
            path = "&mode=dialog_history_details&nzo_id=%s&start=%s&limit=%s" % (nzo.nzo_id, self.start, self.limit)
            page.add(info_labels={'title':title, \
                                  'size': nzo.bytes, \
                                  'date': time.strftime('%d.%m.%Y', time.localtime(nzo.completed))}, \
                     path=path, \
                     cm=self._cm_history(nzo), \
                     is_folder=False)
        if queue.len_slots == 100:
            start = int(self.start) + int(self.limit)
            limit = start + int(self.limit)
            path = "&mode=page_history&start=%s&limit=%s" % \
                   (start, limit)
            page.add(info_labels={'title':'Next...', }, path=path)
        page.show()

    def _cm_history(self, nzo):
        cm_history_details = [("Remove", "&mode=nzo_delete_history&nzo_id=%s" % nzo.nzo_id)]
        if nzo.status.lower() == "failed":
            cm_history_details.insert(0, ("Retry", "&mode=nzo_retry&nzo_id=%s" % nzo.nzo_id))
            cm_history_details.append(("Remove + delete", "&mode=nzo_delete_history_files&nzo_id=%s" % nzo.nzo_id))
            cm_history_details.append(("Remove all failed + delete files", "&mode=sab_delete_history_files_all"))
        else:
            cm_history_details.append(("Remove all", "&mode=sab_delete_history_all"))
        cm = builder.CmBuilder()
        cm.add_list(cm_history_details)
        return cm.list

    def page_warnings(self):
        page = builder.PageBuilder()
        warnings = Warnings().warnings()
        for warning in warnings:
            title = "%s" % warning
            path = "&mode=page_parent_dir"
            cm = self._cm_warnings()
            page.add(info_labels={'title':title,}, \
                     path=path, \
                     cm=cm, \
                     is_folder=False)
        page.show()

    def _cm_warnings(self):
        cm_warnings = [("Clear warnings", "&mode=sab_clear_warnings")]
        cm = builder.CmBuilder()
        cm.add_list(cm_warnings)
        return cm.list

    def _quote(self, mb, mbleft):
        quote = 0
        mb = float(mb)
        mbleft = float(mbleft)
        if mb > 0.00:
            quote = int(round(100*(mb-mbleft)/mb))
        return str(quote)


class Dialog:
    def __init__ (self, **kwargs):
        sabutils.log("Dialog: kwargs: %s" % kwargs)
        for key, value in kwargs.items():
            setattr(self, key, value)

    def dialog_queue_details(self):
        queue = Queue()
        nzo = queue.nzo(self.nzo_id)
        dialog = xbmcgui.Dialog()
        heading = nzo.filename
        line1 = "Status: %s - Completed: %s%% - Size: %s" % (nzo.status, nzo.percentage,  nzo.size)
        line2 = "Category: %s - Priority: %s - Time left: %s" % (nzo.cat, nzo.priority, nzo.timeleft)
        line3 = "Age: %s - Eta: %s" % (nzo.avg_age, nzo.eta)
        ret = dialog.ok(heading, line1, line2, line3)

    def dialog_history_details(self):
        history = History(int(self.start), int(self.limit))
        nzo = history.nzo(self.nzo_id)
        dialog = xbmcgui.Dialog()
        heading = nzo.name
        line1 = "%s: %s - %s" % (nzo.status, time.ctime(nzo.completed), nzo.size)
        if nzo.fail_message != "":
            line2 = "%s" % nzo.fail_message
            line3 = ""
        else:
            line2 = "Category: %s - Post Process: %s" % (nzo.category, nzo.pp)
            line3 = "%s" % nzo.stage_log[0]['actions'][0].replace(' minutes ', 'm').\
                                                          replace(' minute ', 'm').\
                                                          replace(' hours ', 'h').\
                                                          replace(' hour ', 'h').\
                                                          replace(' seconds', 's').\
                                                          replace(' second', 's')
        ret = dialog.ok(heading, line1, line2, line3)
