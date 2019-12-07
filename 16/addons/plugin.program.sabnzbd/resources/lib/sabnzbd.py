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

import sabpostform
import sabutils
import sys
import urllib
import urllib2
import xbmcaddon
from xml.dom.minidom import parseString
if sys.version_info >= (2, 7):
    import json
else:
    try:
        import simplejson as json
    except ImportError:
        import json


class SabnzbdConnection(object):
    __settings__ = xbmcaddon.Addon(id='plugin.program.sabnzbd')
    use_https = __settings__.getSetting("sabnzbd_https").lower() == "true"

    def __init__(self, ip=__settings__.getSetting("sabnzbd_ip"),
                  port=__settings__.getSetting("sabnzbd_port"),
                  apikey=__settings__.getSetting("sabnzbd_key"),
                  username=__settings__.getSetting("sabnzbd_user"),
                  password=__settings__.getSetting("sabnzbd_pass"),
                  category=None, use_https=use_https):
        if not (ip and port and apikey):
            sabutils.notification("SABnzbd API Error", 1000)
            raise RuntimeError("Missing, ip, port or API key")
        self.ip = ip
        self.port = port
        self.apikey = apikey
        if use_https:
            https_string = "https://"
        else:
            https_string = "http://"
        self.baseurl = https_string + self.ip + ":" + self.port + "/api?apikey=" + apikey
        if username and password:
            password_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
            url = https_string + self.ip + ":" + self.port
            password_manager.add_password(None, url, username, password)
            authhandler = urllib2.HTTPBasicAuthHandler(password_manager)
            opener = urllib2.build_opener(authhandler)
            urllib2.install_opener(opener)
        self.category = category
        self.kwargs = dict()


class Sabnzbd(SabnzbdConnection):
    def __init__(self):
        super(Sabnzbd, self).__init__()

    def action(self, **kwargs):
        self.kwargs.update(**kwargs)
        url = "%s&%s" % (self.baseurl, urllib.urlencode(self.kwargs))
        responseMessage = self._sabResponse(url)
        return responseMessage.replace('\n', '')

    def addurl(self, nzb, nzbname, **kwargs):
        category = kwargs.get('category', None)
        priority = kwargs.get('priority', None)
        url = "%s&mode=addurl&name=%s&nzbname=%s" % \
              (self.baseurl, urllib.quote_plus(nzb),urllib.quote_plus(nzbname))
        if priority:
            url = "%s&priority=%s" % (url, priority)
        if category:
            url = "%s&cat=%s" % (url, category)
        elif self.category:
            url = "%s&cat=%s" % (url, self.category)
        responseMessage = self._sabResponse(url)
        return responseMessage

    def add_local(self, path, **kwargs):
        category = kwargs.get('category', None)
        priority = kwargs.get('priority', None)
        url = "%s&mode=addlocalfile&name=%s" % \
              (self.baseurl, urllib.quote_plus(path))
        if priority:
            url = "%s&priority=%s" % (url, priority)
        if category:
            url = "%s&cat=%s" % (url, category)
        elif self.category:
            url = "%s&cat=%s" % (url, self.category)
        responseMessage = self._sabResponse(url)
        return responseMessage
        
    def add_file(self, path, **kwargs):
        url = "%s&mode=addfile" % self.baseurl
        responseMessage = sabpostform.post(path, self.apikey, url, **kwargs)
        return responseMessage

    def max_speed(self, speed):
        self.kwargs['mode'] = 'config'
        self.kwargs['name'] = 'speedlimit'
        self.kwargs['value'] = speed
        return self.action()

    def reset_speed(self):
        return self.max_speed('')

    def pause(self):
        self.kwargs['mode'] = 'pause'
        return self.action()

    def nzo_pause(self, nzo_id):
        self.kwargs['mode'] = 'queue'
        self.kwargs['name'] = 'pause'
        self.kwargs['value'] = nzo_id
        return self.action()

    def resume(self):
        self.kwargs['mode'] = 'resume'
        return self.action()

    def nzo_resume(self, nzo_id):
        self.kwargs['mode'] = 'queue'
        self.kwargs['name'] = 'resume'
        self.kwargs['value'] = nzo_id
        return self.action()

    def nzo_delete(self, nzo_id):
        # will leave data in the incomplete dir
        self.kwargs['mode'] = 'queue'
        self.kwargs['name'] = 'delete'
        self.kwargs['value'] = nzo_id
        return self.action()

    def nzo_delete_files(self, nzo_id):
        self.kwargs['mode'] = 'queue'
        self.kwargs['name'] = 'delete'
        self.kwargs['value'] = nzo_id
        self.kwargs['del_files'] = '1'
        return self.action()

    def nzo_delete_history(self, nzo_id):
        self.kwargs['mode'] = 'history'
        self.kwargs['name'] = 'delete'
        self.kwargs['value'] = nzo_id
        return self.action()

    def nzo_delete_history_files(self, nzo_id):
        self.kwargs['mode'] = 'history'
        self.kwargs['name'] = 'delete'
        self.kwargs['value'] = nzo_id
        self.kwargs['del_files'] = '1'
        return self.action()

    def delete_history_all(self):
        self.kwargs['mode'] = 'history'
        self.kwargs['name'] = 'delete'
        self.kwargs['value'] = 'all'
        return self.action()

    def delete_history_files_all(self):
        self.kwargs['mode'] = 'history'
        self.kwargs['name'] = 'delete'
        self.kwargs['value'] = 'all'
        self.kwargs['del_files'] = '1'
        self.kwargs['failed_only'] = '1'
        return self.action() 

    def nzo_pp(self, nzo_id, value=0):
        self.kwargs['mode'] = 'change_opts'
        self.kwargs['value'] = nzo_id
        self.kwargs['value2'] = value
        return self.action()

    def nzo_change_category(self, nzo_id, category='*'):
        self.kwargs['mode'] = 'change_cat'
        self.kwargs['value'] = nzo_id
        self.kwargs['value2'] = category
        return self.action()

    def nzo_switch(self, nzo_id, value=0):
        self.kwargs['mode'] = 'switch'
        self.kwargs['value'] = nzo_id
        self.kwargs['value2'] = value
        return self.action()

    def nzo_retry(self, nzo_id):
        self.kwargs['mode'] = 'retry'
        self.kwargs['value'] = nzo_id
        return self.action()

    def _sabResponse(self, url):
        responseMessage = _load_url(url)
        sabutils.log("SABnzbd: _sabResponse message: %s" % responseMessage)
        sabutils.log("SABnzbd: _sabResponse from url: %s" % url)
        return responseMessage

    def nzo_id(self, nzbname, nzb = None):
        url = self.baseurl + "&mode=queue&start=0&limit=50&output=xml"
        doc = _load_xml(url)
        nzbname = nzbname.lower().replace('.', ' ').replace('_', ' ')
        if doc:
            if doc.getElementsByTagName("slot"):
                for slot in doc.getElementsByTagName("slot"):
                    status = get_node_value(slot, "status").lower()
                    filename = get_node_value(slot, "filename").lower()
                    if nzb is not None and "grabbing" in status:
                        if nzb.lower() in filename:
                            return get_node_value(slot, "nzo_id")
                    elif not "grabbing" in status:
                        filename = filename.replace('.', ' ').replace('_', ' ')
                        if nzbname == filename:
                            return get_node_value(slot, "nzo_id")
        return None

    def nzf_id(self, sab_nzo_id, name):
        url = self.baseurl + "&mode=get_files&output=xml&value=" + str(sab_nzo_id)
        doc = _load_xml(url)
        sab_nzf_id = None
        if doc:
            if doc.getElementsByTagName("file"):
                for file in doc.getElementsByTagName("file"):
                    filename = get_node_value(file, "filename")
                    status = get_node_value(file, "status")
                    if filename.lower() == name.lower() and status == "active":
                        sab_nzf_id  = get_node_value(file, "nzf_id")
        return sab_nzf_id

    def nzf_id_list(self, sab_nzo_id, file_list):
        url = self.baseurl + "&mode=get_files&output=xml&value=" + str(sab_nzo_id)
        doc = _load_xml(url)
        sab_nzf_id_list = []
        file_nzf = dict()
        if doc:
            if doc.getElementsByTagName("file"):
                for file in doc.getElementsByTagName("file"):
                    filename = get_node_value(file, "filename")
                    status = get_node_value(file, "status")
                    if status == "active":
                        file_nzf[filename] = get_node_value(file, "nzf_id")
        for filename in file_list:
            try:
                sab_nzf_id_list.append(file_nzf[filename])
            except:
                sabutils.log("SABnzbd: nzf_id_list: unable to find sab_nzf_id for: %s" % filename)
        return sab_nzf_id_list

    def nzo_id_history(self, nzbname):
        start = 0
        limit = 20
        noofslots = 21
        nzbname = nzbname.lower().replace('.', ' ').replace('_', ' ')
        while limit <= noofslots:
            url = self.baseurl + "&mode=history&start=" +str(start) + "&limit=" + str(limit) + "&failed_only=1&output=xml"
            doc = _load_xml(url)
            if doc:
                history = doc.getElementsByTagName("history")
                noofslots = int(get_node_value(history[0], "noofslots"))
                if doc.getElementsByTagName("slot"):
                    for slot in doc.getElementsByTagName("slot"):
                        filename = get_node_value(slot, "name").lower().replace('.', ' ').replace('_', ' ')
                        if filename == nzbname:
                            return get_node_value(slot, "nzo_id")
                start = limit + 1
                limit = limit + 20
            else:
                limit = 1
                noofslots = 0
        return None

    def nzo_id_history_list(self, nzbname_list):
        start = 0
        limit = 20
        noofslots = 21
        sab_nzo_id = None
        while limit <= noofslots and not sab_nzo_id:
            url = self.baseurl + "&mode=history&start=" +str(start) + "&limit=" + str(limit) + "&failed_only=1&output=xml"
            doc = _load_xml(url)
            if doc:
                history = doc.getElementsByTagName("history")
                noofslots = int(get_node_value(history[0], "noofslots"))
                if doc.getElementsByTagName("slot"):
                    for slot in doc.getElementsByTagName("slot"):
                        filename = get_node_value(slot, "name").lower().replace('.', ' ').replace('_', ' ')
                        for row in nzbname_list:
                            if filename == row[0].lower().replace('.', ' ').replace('_', ' '):
                                row[1] = get_node_value(slot, "nzo_id")
                start = limit + 1
                limit = limit + 20
            else:
                limit = 1
                noofslots = 0
        return nzbname_list

    def file_list(self, id=''):
        url = self.baseurl + "&mode=get_files&output=xml&value=" + str(id)
        doc = _load_xml(url)
        file_list = []
        if doc:
            if doc.getElementsByTagName("file"):
                for file in doc.getElementsByTagName("file"):
                    status = get_node_value(file, "status")
                    if status == "active":
                        row = []
                        filename = get_node_value(file, "filename")
                        row.append(filename)
                        bytes = get_node_value(file, "bytes")
                        bytes = int(bytes.replace(".00",""))
                        row.append(bytes)
                        file_list.append(row)
        return file_list

    def file_list_position(self, sab_nzo_id, sab_nzf_id, position):
        action = { -1 : 'Delete',
                    0 : 'Top',
                    1 : 'Up',
                    2 : 'Down',
                    3 : 'Bottom'}
        url = "http://" + self.ip + ":" + self.port + "/sabnzbd/nzb/" + sab_nzo_id + "/bulk_operation?session=" \
              + self.apikey + "&action_key=" + action[position]
        for nzf_id in sab_nzf_id:
            url = url + "&" + nzf_id + "=on"
        sabutils.load_url(url, None, "SABnzbd failed moving file to top of queue")
        return

    def category_list(self):
        url = self.baseurl + "&mode=get_cats&output=json"
        doc = _load_json(url)
        if doc:
            return doc["categories"]
        else:
            return ["*"]

    def misc_settings_dict(self):
        url = self.baseurl + "&mode=get_config&section=misc&output=xml"
        doc = _load_xml(url)
        settings_dict = dict()
        if doc:
            if doc.getElementsByTagName("misc"):
                for misc in doc.getElementsByTagName("misc")[0].childNodes:
                    try:
                        settings_dict[misc.tagName] = misc.firstChild.data
                    except:
                        pass
        return settings_dict

    def setup_streaming(self):
        # 1. check allow_streaming
        # 2. set allow streaming if missing
        url = self.baseurl + "&mode=get_config&section=misc&keyword=allow_streaming&output=xml"
        doc = _load_xml(url)
        if doc.getElementsByTagName("result"):
            return "apikey"
        allow_streaming = "0"
        if doc.getElementsByTagName("misc"):
            allow_streaming = get_node_value(doc.getElementsByTagName("misc")[0], "allow_streaming")
        if not allow_streaming == "1":
            url = self.baseurl + "&mode=set_config&section=misc&keyword=allow_streaming&value=1"
            _load_xml(url)
            return "restart"
        return "ok"

    def self_test(self):
        url = self.baseurl + "&mode=version&output=xml"
        if _load_url(url) is None:
            sabutils.log("SABnzbd: setup_streaming: unable to conncet to SABnzbd: %s" % url)
            return "ip"
        url = self.baseurl + "&mode=get_config&section=misc&keyword=allow_streaming&output=xml"
        doc = _load_xml(url)
        if doc.getElementsByTagName("result"):
            return "apikey"
        return "ok"


def get_node_value(parent, name, ns=""):
    if ns:
        return unicode(parent.getElementsByTagNameNS(ns, name)[0].childNodes[0].data.encode('utf-8'), 'utf-8')
    else:
        return unicode(parent.getElementsByTagName(name)[0].childNodes[0].data.encode('utf-8'), 'utf-8')


def _load_url(url):
        sabutils.log("SABnzbd: _load_url: ")
        return sabutils.load_url(url)


def _load_xml(url):
    sabutils.log("SABnzbd: _load_xml: ")
    try:
        out = parseString(_load_url(url))
    except:
        sabutils.log("SABnzbd: _load_xml: malformed xml from url: %s" % url)
        sabutils.notification("SABnzbd malformed xml")
        return None
    return out


def _load_json(url):
    sabutils.log("SABnzbd: _load_json: url: %s" % url)
    try:
        out = json.loads(_load_url(url))
    except:
        sabutils.log("SABnzbd: _load_json: malformed json from url: %s" % url)
        sabutils.notification("SABnzbd malformed json")
        return None
    return out


class Queue(SabnzbdConnection):
    def __init__(self, start=0, limit=50):
        super(Queue, self).__init__()
        self.nzo_list = []
        self.slots = None
        url = "%s&mode=queue&start=%s&limit=%s&output=json" % \
              (self.baseurl, start, limit)
        doc = _load_json(url)
        if doc:
            for key, value in doc["queue"].items():
                setattr(self, key, value)
            if self.slots is not None:
                for slot in self.slots:
                    nzo = NzoListObject(slot)
                    self.nzo_list.append(nzo)

    def nzo(self, nzo_id):
        for m_nzo in self.nzo_list:
            if nzo_id == m_nzo.nzo_id:
                return m_nzo
            else:
                pass
        return None


class NzoListObject:
    def __init__(self, slot):
        for key, value in slot.items():
            setattr(self, key, value)


class History(SabnzbdConnection):
    def __init__(self, start=0, limit=50):
        super(History, self).__init__()
        self.failed_only = 0
        self.nzo_list = []
        self.slots = None
        url = "%s&mode=history&start=%s&limit=%s&failed_only=%s&output=json" % \
              (self.baseurl, start, limit, self.failed_only)
        doc = _load_json(url)
        if doc:
            for key, value in doc["history"].items():
                setattr(self, key, value)
            if self.slots is not None:
                for slot in self.slots:
                    nzo = NzoListObject(slot)
                    self.nzo_list.append(nzo)
        self.len_slots = len(self.nzo_list)

    def nzo(self, nzo_id):
        for m_nzo in self.nzo_list:
            if nzo_id == m_nzo.nzo_id:
                return m_nzo
            else:
                pass
        return None


class Nzo(Queue):
    def __init__(self, nzo_id):
        super(Nzo, self).__init__()
        self.nzo_id = nzo_id
        nzo_list_object = self.nzo(nzo_id)
        if nzo_list_object is None:
            self.is_in_queue = False
        else:
            self.is_in_queue = True
            import inspect
            for n, v in inspect.getmembers(nzo_list_object):
                setattr(self, n, v)

    def _get_nzf_list(self):
        out_list = []
        out_dict = dict()
        url = "%s&mode=get_files&output=json&value=%s" % (self.baseurl, str(self.nzo_id))
        doc = _load_json(url)
        if doc:
            files = doc["files"]
            if files:
                i = 0
                for file in files:
                    nzf = Nzf(**file)
                    out_list.append(nzf)
                    out_dict[file['filename']] = i
                    i+= 1
        return out_list, out_dict

    def nzf_list(self):
        try:
            nzf_list, nzf_dict = self._get_nzf_list()
            return nzf_list
        except:
            return None

    def get_nzf(self, name):
        try:
            nzf_list, nzf_dict = self._get_nzf_list()
            return nzf_list[nzf_dict[name]]
        except:
            return None

    def get_nzf_id(self, nzf_id):
        nzf_list, nzf_dict = self._get_nzf_list()
        out = None
        for nzf in nzf_list:
            if nzf_id == nzf.nzf_id:
                out = nzf
                break
        return out


class Nzf:
    def __init__(self, **kwargs):
        self.status = kwargs.get('status')
        self.mb = kwargs.get('mb', 0)
        self.age = kwargs.get('age')
        self.bytes = kwargs.get('bytes', 0)
        self.filename = kwargs.get('filename')
        self.subject = kwargs.get('subject', self.filename)
        self.mbleft = kwargs.get('mbleft', 0)
        self.nzf_id = kwargs.get('nzf_id', None)
        self.id = kwargs.get('id')

class Warnings(SabnzbdConnection):
    def __init__(self):
        super(Warnings, self).__init__()

    def warnings(self):
        url = "%s&mode=warnings&output=json" % self.baseurl
        doc = _load_json(url)
        if doc:
            out = []
            for i in range(len(doc['warnings'])):
                out.append(doc['warnings'][i].replace('\n', ' '))
                i += 1
            return out
        else:
            return []

    def clear(self):
        url = "http://%s:%s/status/clearwarnings?session=%s" % \
              (self.ip, self.port, self.apikey)
        _load_url(url)
