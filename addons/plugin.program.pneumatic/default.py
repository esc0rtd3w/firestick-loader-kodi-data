"""
 Copyright (c) 2010, 2011, 2012 Popeye

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

import sys
import os
import time

import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin

from threading import Thread

from sabnzbd import Sabnzbd
from sabnzbd import Nzo
from utils import log
import utils
import nfo
import xbmcplayer
import nfo2home
import strm2lib
import nzb as m_nzb

__settings__ = xbmcaddon.Addon(id='plugin.program.pneumatic')
__language__ = __settings__.getLocalizedString

sabnzbd = Sabnzbd()
INCOMPLETE_FOLDER = unicode(__settings__.getSetting("sabnzbd_incomplete"), 'utf-8')

NZB_FOLDER = __settings__.getSetting("nzb_folder")
SAVE_NZB = (__settings__.getSetting("save_nzb").lower() == "true")
NZB_CACHE = __settings__.getSetting("nzb_cache")

AUTO_PLAY = (__settings__.getSetting("auto_play").lower() == "true")

MODE_PLAY = "play"
MODE_DOWNLOAD = "download"
MODE_LIST_PLAY = "list_play"
MODE_AUTO_PLAY = "auto_play"
MODE_DELETE = "delete"
MODE_REPAIR = "repair"
MODE_INCOMPLETE = "incomplete"
MODE_INCOMPLETE_LIST = "incomplete_list"
MODE_STRM = "strm"
MODE_SAVE_STRM = "save_strm"
MODE_LOCAL = "local"
MODE_LOCAL_LIST_TOP = "local_list_top"
MODE_LOCAL_LIST = "local_list"
MODE_ADD_LOCAL = "add_local"
MODE_DEL_LOCAL = "del_local"
MODE_LOCAL_FILE = "local_file"
MODE_LOCAL_FILE_IN_DIR = "local_file_in_dir"
MODE_DEL_LOCAL_FILE = "del_local_file"
MODE_DEL_LOCAL_FILE_IN_DIR = "del_local_file_in_dir"

def add_posts(info_labels, url, mode, thumb='', fanart='', folder=True):
    log("add_posts: info_labels: %s url: %s mode: %s" % (info_labels, url, mode))
    listitem=xbmcgui.ListItem(info_labels['title'], iconImage="DefaultVideo.png", thumbnailImage=thumb)
    listitem.setInfo(type="Video", infoLabels=info_labels)
    listitem.setProperty("Fanart_Image", fanart)
    cm = []
    if mode == MODE_INCOMPLETE_LIST:
        cm_url_delete = sys.argv[0] + '?' + "mode=delete&incomplete=True" + url
        cm.append(("Delete" , "XBMC.RunPlugin(%s)" % (cm_url_delete)))
        cm_url_delete_all = sys.argv[0] + '?' + "mode=delete&delete_all=True&incomplete=True" + url
        cm.append(("Delete all inactive" , "XBMC.RunPlugin(%s)" % (cm_url_delete_all)))
    if mode == MODE_LOCAL_LIST_TOP:
        cm_url_add_local = sys.argv[0] + '?' + "mode=add_local"
        cm.append(("Add folder" , "XBMC.RunPlugin(%s)" % (cm_url_add_local)))
        cm_url_delete_local = sys.argv[0] + '?' + "mode=del_local" + url
        cm.append(("Remove folder" , "XBMC.RunPlugin(%s)" % (cm_url_delete_local)))
    if mode == MODE_LOCAL_FILE:
        mode = MODE_PLAY
        cm.append(("Remove nzb" , "XBMC.RunPlugin(%s?mode=%s%s)" % (sys.argv[0], MODE_DEL_LOCAL_FILE, url)))
    if mode == MODE_LOCAL_FILE_IN_DIR:
        mode = MODE_PLAY
        cm.append(("Remove nzb" , "XBMC.RunPlugin(%s?mode=%s%s)" % (sys.argv[0], MODE_DEL_LOCAL_FILE_IN_DIR, url)))
    if len(cm) > 0:
        listitem.addContextMenuItems(cm, replaceItems=True)
    xurl = "%s?mode=%s" % (sys.argv[0],mode)
    xurl = xurl + url
    listitem.setPath(xurl)
    return xbmcplugin.addDirectoryItem(handle=HANDLE, url=xurl, listitem=listitem, isFolder=folder)
    
def is_nzb_home(params):
    log("is_nzb_home: params: %s" % params)
    get = params.get
    nzb = utils.unquote_plus(get("nzb"))
    nzbname = m_nzb.Nzbname(utils.unquote_plus(get("nzbname"))).final_name
    folder = utils.join(INCOMPLETE_FOLDER, os.path.join(nzbname, ''))
    iscanceled = False
    type = get('type', 'addurl')
    sab_nzo_id = sabnzbd.nzo_id(nzbname, nzb)
    log("is_nzb_home: folder: %s sab_nzo_id: %s" %(folder, sab_nzo_id))
    if sab_nzo_id is None:
        nzo_id = sabnzbd.nzo_id_history(nzbname)
    else:
        nzo_id = sab_nzo_id
    log("is_nzb_home: nzo_id: %s" % nzo_id)
    if not utils.dir_exists(folder, nzo_id):
        progressDialog = xbmcgui.DialogProgress()
        progressDialog.create('Pneumatic', 'Sending request to SABnzbd')
        category = get_category()
        # correct wrong type mode
        if nzb.startswith('http'):
            type = "addurl"
            log("is_nzb_home: type changed to addurl")
        elif type == 'addurl':
            type = 'add_file'
            log("is_nzb_home: type changed to add_file")
        if type == 'addurl':
            type, nzb = nzb_cache(type, nzb, nzbname)
        # SABnzbd and URI should be latin-1 encoded
        if type == 'addurl':
            response = sabnzbd.addurl(nzb.encode('latin-1'), nzbname, category=category)
        # add_local will not work on remote shares, thus add_file
        elif type == 'add_file' or type == 'add_local':
            response = sabnzbd.add_file(nzb.encode('latin-1'), category=category)
        log("is_nzb_home: type: %s response: %s" %(type, response))
        if "ok" in response:
            progressDialog.update(0, 'Request to SABnzbd succeeded', 'waiting for nzb download')
            seconds = 0
            timer = 0
            #SABnzbd uses nzb url as name until it has downloaded the nzb file
            sab_nzo_id_init = sabnzbd.nzo_id(nzbname, nzb)
            log("is_nzb_home: sab_nzo_id_init: %s" % sab_nzo_id_init)
            while not (sab_nzo_id and utils.exists_incomplete(folder)):
                # Ask user what incomplete dir is right every 10s
                if timer > 9:
                    timer = 0
                    folder, nzbname = find_incomplete(folder, nzbname)
                sab_nzo_id = sabnzbd.nzo_id(nzbname)
                label = str(seconds) + " seconds"
                log("is_nzb_home: waiting for nzb: sab_nzo_id: %s for: %s" % (sab_nzo_id, label))
                progressDialog.update(0, 'Request to SABnzbd succeeded', 'waiting for nzb download', label)
                if progressDialog.iscanceled():
                    progressDialog.close()
                    log("is_nzb_home: waiting for nzb: canceled")
                    # Fix for hang when playing .strm
                    time.sleep(1)
                    xbmc.Player().stop()
                    if sab_nzo_id is None and sab_nzo_id_init is not None:
                        sab_nzo_id = sab_nzo_id_init
                    #Trying to delete both the queue and history
                    if sab_nzo_id is not None:
                        pause = sabnzbd.nzo_pause(sab_nzo_id)
                        log("is_nzb_home: pause: sab_nzo_id: %s msg: %s" % (sab_nzo_id, pause))
                        time.sleep(3)
                        delete_msg = sabnzbd.nzo_delete_files(sab_nzo_id)
                        log("is_nzb_home: delete_queue: sab_nzo_id: %s nzbname: %s msg: %s" % (sab_nzo_id, nzbname, delete_msg))
                        if not "ok" in delete_msg:
                            delete_msg = sabnzbd.nzo_delete_history_files(sab_nzo_id)
                            log("is_nzb_home: delete_history: sab_nzo_id: %s nzbname: %s msg: %s" % (sab_nzo_id, nzbname, delete_msg))
                    else:
                        log("is_nzb_home: failed removing %s from the queue" % nzbname)
                    iscanceled = True
                    break
                time.sleep(1)
                seconds += 1
                timer += 1
            if not iscanceled:
                switch = sabnzbd.nzo_switch(sab_nzo_id, 0).replace('\n', '')
                log("is_nzb_home: switch: sab_nzo_id: %s msg: %s" % (sab_nzo_id, switch))
                if not "0" in switch:
                    progressDialog.update(0, 'Failed to prioritize the nzb!')
                    time.sleep(1)
                # Dont add meta data for local nzb's
                if type == 'addurl':
                    t = Thread(target=save_nfo, args=(folder,))
                    t.start()
                progressDialog.close()
                return True, sab_nzo_id
            else:
                progressDialog.close()
                return False, sab_nzo_id
        else:
            progressDialog.close()
            log("is_nzb_home: failed adding nzb to SAB")
            # Fix for hang when playing .strm
            xbmc.Player().stop()            
            utils.notification("Request to SABnzbd failed!")
            return False, sab_nzo_id
    else:
        switch = sabnzbd.nzo_switch(sab_nzo_id, 0).replace('\n', '')
        log("is_nzb_home: switch: sab_nzo_id: %s msg: %s" % (sab_nzo_id, switch))
        if not "0" in switch:
            utils.notification("Failed to prioritize the nzb!")
        # TODO make sure there is also a NZB in the queue
        return True, sab_nzo_id

def nzb_cache(type, nzb, nzbname):
    nzb_path = os.path.join(NZB_CACHE, '%s%s' % (nzbname, '.nzb'))
    if utils.exists(nzb_path):
        nzb = nzb_path
        type = 'add_file'
        log("nzb_cache: nzb_path: %s" % nzb)
    return type, nzb

def find_incomplete(folder, nzbname):
    log("find_incomplete: folder: %s nzbname: %s" % (folder, nzbname))
    active_nzbname_list, nzbname_list = nzbname_lists()
    ui_list = []
    incomplete_list = []
    for row in active_nzbname_list:
        incomplete_list.append(row)
        ui_list.append(os.path.basename(row[0]))
    for row in nzbname_list:
        if row[1] is not None:
            incomplete_list.append(row)
            ui_list.append(os.path.basename(row[0]))
    dialog = xbmcgui.Dialog()
    if len(ui_list) > 0:
        ret = dialog.select('Select download directory', ui_list)
        log("find_incomplete: ret: %s ui_list: %s" %(ret, ui_list))
        if ret <= 0:
            return folder, nzbname
        else:
            index = ret + 1
        # folder, nzbname
        return ui_list[index][0], ui_list[index][0]
    else:
        ret = dialog.ok('Pneumatic', \
                  'Can\'t find any incomplete directory for', \
                  '%s' % nzbname, \
                  'please wait or cancel the streaming')
        log("find_incomplete: no incomplete dir found ret: %s" % ret)
        return folder, nzbname

def save_nfo(folder):
    log("save_nfo: folder: %s" % folder)
    nfo2home.save_nfo(__settings__, folder)
    return

def pre_play(nzbname, **kwargs):
    log("pre_play: nzbname: %s kwargs: %s" % (nzbname, kwargs))
    mode = kwargs.get('mode', None)
    sab_nzo_id = kwargs.get('nzo', None)
    iscanceled = False
    folder = utils.join(INCOMPLETE_FOLDER, os.path.join(nzbname, ''))
    folder_one = folder + '.1'
    if utils.exists(os.path.join(folder_one, '')):
        folder = folder_one
    if sab_nzo_id is None:
        sab_nzo_id_history = sabnzbd.nzo_id_history(nzbname)
        nzf_list = utils.dir_to_nzf_list(folder)
    else:
        nzo = Nzo(sab_nzo_id)
        nzf_list = nzo.nzf_list()
        sab_nzo_id_history = None
    sorted_rar_nzf_list = utils.sorted_rar_nzf_file_list(nzf_list)
    # TODO
    # If we cant find any rars in the queue, we have to wait for SAB
    # and then guess the names...
    # if len(nzf_list) == 0:
        # iscanceled = get_nzf(folder, sab_nzo_id, None)
    is_movie_in_rar = True
    if len(sorted_rar_nzf_list) == 0:
        # look for other playable files
        multi_nzf_list = sorted_nzf_list = utils.sorted_movie_nzf_file_list(nzf_list)
        if len(multi_nzf_list) > 0:
            is_movie_in_rar = False
    else:
        multi_nzf_list = utils.sorted_multi_arch_nzf_list(sorted_rar_nzf_list)
        sorted_nzf_list = sorted_rar_nzf_list
        clean_sorted_nzf_list = utils.nzf_diff_list(sorted_nzf_list, multi_nzf_list)
    if len(multi_nzf_list) > 0:
        # Loop though all multi archives and add file to the 
        play_list = []
        for nzf in multi_nzf_list:
            if sab_nzo_id is not None:
                response = set_streaming(sab_nzo_id)
                log("pre_play: set_streaming: %s" % response)
                t = Thread(target=nzf_to_bottom, args=(sab_nzo_id, nzf_list, sorted_nzf_list,))
                t.start()
                iscanceled = get_nzf(folder, sab_nzo_id, nzf)
            if iscanceled:
                break
            else:
                if is_movie_in_rar:
                    # RAR ANALYSYS #
                    in_rar_file_list = utils.rar_filenames(folder, nzf.filename)
                    movie_list = utils.sort_filename(in_rar_file_list)
                    log("pre_play: folder: %s nzf.filename: %s in_rar_file_list: %s" % (folder, nzf.filename, in_rar_file_list))
                else:
                    movie_list = [os.path.join(folder, nzf.filename)]
                # Make sure we have a movie
                if not (len(movie_list) >= 1):
                    utils.notification("Not a movie!")
                    log("pre_play: no movie in movie_list")
                    break
                # Who needs sample?
                movie_no_sample_list = utils.no_sample_list(movie_list)
                # If auto play is enabled we skip samples in the play_list
                if AUTO_PLAY and mode is not MODE_INCOMPLETE_LIST:
                    for movie_file in movie_no_sample_list:
                        play_list.append(nzf.filename)
                        play_list.append(movie_file)
                else:
                    for movie_file in movie_list:
                        play_list.append(nzf.filename)
                        play_list.append(movie_file)
                # If the movie is a .mkv or .mp4 we need the last rar
                if utils.is_movie_mkv(movie_list) and sab_nzo_id and is_movie_in_rar:
                    # If we have a sample or other file, the second rar is also needed..
                    if len(in_rar_file_list) > 1:
                        second_nzf = clean_sorted_nzf_list[1]
                        iscanceled = get_nzf(folder, sab_nzo_id, second_nzf)
                    last_nzf = clean_sorted_nzf_list[-1]
                    iscanceled =  get_nzf(folder, sab_nzo_id, last_nzf)
                    if iscanceled: 
                        break 
        if iscanceled:
            log("pre_play: get_nzf: canceled")
            return
        else:
            rar_file_list = [x.filename for x in sorted_nzf_list]
            if (len(rar_file_list) >= 1) or (not is_movie_in_rar and len(movie_list) >= 1):
                if AUTO_PLAY and ( mode is None or mode is MODE_STRM):
                    video_params = dict()
                    if not mode:
                        video_params['mode'] = MODE_AUTO_PLAY
                    else:
                        video_params['mode'] = MODE_STRM
                    video_params['play_list'] = utils.quote_plus(';'.join(play_list))
                    video_params['file_list'] = utils.quote_plus(';'.join(rar_file_list))
                    video_params['folder'] = utils.quote_plus(folder)
                    video_params['nzoid'] = sab_nzo_id
                    video_params['nzoidhistory'] = sab_nzo_id_history
                    return play_video(video_params)   
                else:
                    return playlist_item(play_list, rar_file_list, folder, sab_nzo_id, sab_nzo_id_history)
            else:
                utils.notification("No rar\'s in the NZB!")
                log("pre_play: no rar\'s in the NZB")
                return
    else:
        utils.notification("No playable files found!")
        log("pre_play: no playable files found")
        return

def set_streaming(sab_nzo_id):
    # Set the post process to 0 = skip will cause SABnzbd to fail the job. requires streaming_allowed = 1 in sabnzbd.ini (6.x)
    setstreaming = "ok"
    pp_message = sabnzbd.nzo_pp(sab_nzo_id, 0)
    switch_message = sabnzbd.nzo_switch(sab_nzo_id, 0)
    log("set_streaming: sab_nzo_id: %s pp_message %s switch_message %s" % (sab_nzo_id, pp_message, switch_message))
    if (not "ok" in pp_message) and (not "0" in switch_message):
        utils.notification('Post process request to SABnzbd failed!')
        time.sleep(1)
        setstreaming = "notOk"
    return setstreaming

def playlist_item(play_list, rar_file_list, folder, sab_nzo_id, sab_nzo_id_history):
    log("playlist_item: play_list: %s rar_file_list: %s folder: %s sab_nzo_id: %s sab_nzo_id_history: %s" %\
       (play_list, rar_file_list, folder, sab_nzo_id, sab_nzo_id_history))
    new_play_list = play_list[:]
    for arch_rar, movie_file in zip(play_list[0::2], play_list[1::2]):
        info = nfo.ReadNfoLabels(folder)
        xurl = "%s?mode=%s" % (sys.argv[0],MODE_LIST_PLAY)
        url = (xurl + "&nzoid=" + str(sab_nzo_id) + "&nzoidhistory=" + str(sab_nzo_id_history)) +\
              "&play_list=" + utils.quote_plus(';'.join(new_play_list)) + "&folder=" + utils.quote_plus(folder) +\
              "&file_list=" + utils.quote_plus(';'.join(rar_file_list))
        new_play_list.remove(arch_rar)
        new_play_list.remove(movie_file)
        item = xbmcgui.ListItem(movie_file, iconImage='DefaultVideo.png', thumbnailImage=info.thumbnail)
        item.setInfo(type="Video", infoLabels=info.info_labels)
        item.setProperty("Fanart_Image", info.fanart)
        item.setPath(url)
        isfolder = False
        # item.setProperty("IsPlayable", "true")
        cm = []
        if sab_nzo_id_history:
            cm_url_repair = sys.argv[0] + '?' + "mode=repair" + "&nzoidhistory=" + str(sab_nzo_id_history) + "&folder=" + utils.quote_plus(folder)
            cm.append(("Repair" , "XBMC.RunPlugin(%s)" % (cm_url_repair)))
        cm_url_delete = sys.argv[0] + '?' + "mode=delete" + "&nzoid=" + str(sab_nzo_id) + "&nzoidhistory=" + str(sab_nzo_id_history) + "&folder=" + utils.quote_plus(folder)
        cm.append(("Delete" , "XBMC.RunPlugin(%s)" % (cm_url_delete)))
        item.addContextMenuItems(cm, replaceItems=True)
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=item, isFolder=isfolder)
    xbmcplugin.setContent(HANDLE, 'movies')
    xbmcplugin.endOfDirectory(HANDLE, succeeded=True, cacheToDisc=True)
    return

def get_nzf(folder, sab_nzo_id, nzf):
    log("get_nzf: folder: %s sab_nzo_id: %s nzf.filename: %s" % (folder, sab_nzo_id, nzf.filename))
    if sab_nzo_id is not None:
        if nzf.status.lower() == 'active':
            sabnzbd.file_list_position(sab_nzo_id, [nzf.nzf_id], 0)
        return wait_for_nzf(folder, sab_nzo_id, nzf)
    else:
        return False

def wait_for_nzf(folder, sab_nzo_id, nzf):
    log("wait_for_nzf: folder: %s sab_nzo_id: %s nzf.filename: %s" % (folder, sab_nzo_id, nzf.filename))
    iscanceled = False
    is_rar_found = False
    # If rar exist we skip dialogs
    some_rar = os.path.join(folder, nzf.filename)
    if utils.exists(some_rar):
        is_rar_found = True
    if not is_rar_found:
        progressDialog = xbmcgui.DialogProgress()
        progressDialog.create('Pneumatic', 'Request to SABnzbd succeeded, waiting for ', utils.short_string(nzf.filename))
        time_now = time.time()
        while not is_rar_found:
            time.sleep(1)
            if utils.exists(some_rar):
                # TODO Look for optimization
                # Wait until the file is written to disk before proceeding
                size_now = float(nzf.bytes)
                size_later = 0
                while (size_now != size_later) or (size_now == 0) or (size_later == 0):
                    size_now = utils.size(some_rar)
                    if size_now != size_later:
                        time.sleep(0.5)
                        size_later = utils.size(some_rar)
                is_rar_found = True
                break
            nzo = Nzo(sab_nzo_id)
            m_nzf = nzo.get_nzf_id(nzf.nzf_id)
            percent, label = utils.wait_for_rar_label(nzo, m_nzf, time_now)
            progressDialog.update(percent, 'Request to SABnzbd succeeded, waiting for', utils.short_string(nzf.filename), label)
            if progressDialog.iscanceled():
                progressDialog.close()
                dialog = xbmcgui.Dialog()
                ret = dialog.select('What do you want to do?', ['Delete job', 'Just download'])
                # Fix for hang when playing .strm
                xbmc.Player().stop()
                xbmc.executebuiltin('Dialog.Close(all, true)')
                if ret == 0:
                    sabnzbd.nzo_pause(sab_nzo_id)
                    time.sleep(3)
                    delete_ = sabnzbd.nzo_delete_files(sab_nzo_id)
                    if not "ok" in delete_:
                        xbmc.log(delete_)
                        utils.notification("Deleting failed")
                    else:
                        utils.notification("Deleting succeeded") 
                elif ret == 1:
                    # allow the previous select dialog to close
                    time.sleep(1)
                    just_download({'nzoid': sab_nzo_id})
                return True
        progressDialog.close()
    return iscanceled

def nzf_to_bottom(sab_nzo_id, nzf_list, sorted_nzf_list):
    log("nzf_to_bottom: sab_nzo_id: %s" % sab_nzo_id)
    diff_list = list(set([nzf.nzf_id for nzf in nzf_list if nzf.nzf_id is not None])-
                     set([nzf.nzf_id for nzf in sorted_nzf_list if nzf.nzf_id is not None]))
    sabnzbd.file_list_position(sab_nzo_id, diff_list, 3)
    return

def list_movie(params):
    log("list_movie: params: %s" % params) 
    get = params.get
    mode = get("mode")
    file_list = utils.unquote_plus(get("file_list")).split(";")
    play_list = utils.unquote_plus(get("play_list")).split(";")
    folder = get("folder")
    folder = utils.unquote_plus(folder)
    sab_nzo_id = get("nzoid")
    sab_nzo_id_history = get("nzoidhistory")
    return playlist_item(play_list, file_list, folder, sab_nzo_id, sab_nzo_id_history)

def list_incomplete(params):
    log("list_incomplete: params: %s" % params)
    nzbname = utils.unquote_plus(params.get("nzbname"))
    sab_nzo_id = params.get("nzoid")
    pre_play(nzbname, mode=MODE_INCOMPLETE_LIST, nzo=sab_nzo_id)

def play_video(params):
    log("play_video: params: %s" % params)
    get = params.get
    mode = get("mode")
    file_list = get("file_list")
    file_list = utils.unquote_plus(file_list).split(";")
    play_list = get("play_list")
    play_list = utils.unquote_plus(play_list).split(";")
    folder = get("folder")
    folder = utils.unquote_plus(folder)
    # We might have deleted the path
    if utils.exists_incomplete(folder):
        if len(file_list) > 0 and not play_list[1].endswith(play_list[0]):
            # we trick xbmc to play avi by creating empty rars if the download is only partial
            utils.write_fake(file_list, folder)
            # Prepare potential file stacking
            if (len(play_list) > 2):
                rar = []
                for arch_rar, movie_file in zip(play_list[0::2], play_list[1::2]):
                    raruri = "rar://" + utils.rarpath_fixer(folder, arch_rar) + "/" + movie_file
                    rar.append(raruri)
                    raruri = 'stack://' + ' , '.join(rar)
            else:
                raruri = "rar://" + utils.rarpath_fixer(folder, play_list[0]) + "/" + play_list[1]
            uri = raruri
        else:
            # we have a plain file
            if (len(play_list) > 2):
                uri = "stack://%s" % ' , '.join(play_list[1::2])
            else:
                uri = play_list[1]
        log("play_video: uri: %s" % uri)
        info = nfo.NfoLabels()
        item = xbmcgui.ListItem(info.info_labels['title'], iconImage='DefaultVideo.png', thumbnailImage=info.thumbnail)
        item.setInfo(type="Video", infoLabels=info.info_labels)
        item.setPath(uri)
        item.setProperty("IsPlayable", "true")
        xbmcplugin.setContent(HANDLE, 'movies')
        wait = 0
        player = xbmcplayer.XBMCPlayer(xbmc.PLAYER_CORE_AUTO)
        player.sleep(1000)
        if mode == MODE_AUTO_PLAY or mode == MODE_LIST_PLAY:
            player.play( uri, item )
            log("play_video: player.play uri: %s" % uri)
        else:
            xbmcplugin.setResolvedUrl(handle=HANDLE, succeeded=True, listitem=item)
            log("play_video: setResolvedUrl uri: %s" % uri)
        removed_fake = False
        while player.is_active:
            player.sleep(500)
            wait+= 1
            if player.is_playing and not removed_fake:
                utils.remove_fake(file_list, folder)
                removed_fake = True
            if player.is_stopped:
                the_end(folder, player.is_stopped, params.get("nzoid"), params.get("nzoidhistory"))
                player.is_active = False
            elif player.is_ended:
                the_end(folder, False, params.get("nzoid"), params.get("nzoidhistory"))
                player.is_active = False
            elif wait >= 6000 and not player.isPlayingVideo():
                utils.notification("Error playing file!")
                break
        if not removed_fake:
            utils.remove_fake(file_list, folder)
    else:
        utils.notification("File deleted")
        time.sleep(1)
        xbmc.executebuiltin("Action(ParentDir)")
    return

def the_end(folder, is_stopped=False, sab_nzo_id=None, sab_nzo_id_history=None):
    log("the_end: folder: %s is_stopped: %s" % (folder, is_stopped))
    dummy, nzbname = os.path.split(os.path.dirname(folder))
    if sab_nzo_id_history or sab_nzo_id is None:
        if sab_nzo_id_history is None:
            sab_nzo_id_history = sabnzbd.nzo_id_history(nzbname)
        if sab_nzo_id is None:
            sab_nzo_id = sabnzbd.nzo_id(nzbname)
    params = dict()
    params['nzbname'] = nzbname
    params['nzoidhistory'] = sab_nzo_id_history
    params['nzoid'] = sab_nzo_id
    params['incomplete'] = True
    params['folder'] = folder
    params['end'] = True
    if sab_nzo_id_history is None:
        the_end_dialog(params,progressing=True, is_stopped=is_stopped)
    elif is_stopped:
        the_end_dialog(params)
    elif (__settings__.getSetting("post_process").lower() == "repair"):
        repair(params)
    elif (__settings__.getSetting("post_process").lower() == "delete"):
        delete(params)
    elif (__settings__.getSetting("post_process").lower() == "ask"):
        the_end_dialog(params)
    return

def the_end_dialog(params, **kwargs):
    log("the_end_dialog: params: %s kwargs: %s" %(params, kwargs))
    dialog = xbmcgui.Dialog()
    if 'is_stopped' in kwargs:
        is_stopped = kwargs['is_stopped']
    else:
        is_stopped = False
    if 'progressing' in kwargs:
        progressing = kwargs['progressing']
    else:
        progressing = False
    if progressing:
        options = ['Delete', 'Just download']
        if is_stopped:
            heading = 'Downloading, what do you want to do?'
        else:
            heading = 'Still downloading, what do you want to do?'
    else:
        heading = 'Download finished, what do you want to do?'
        options = ['Delete', 'Repair']
    ret = dialog.select(heading, options)
    if ret == 0:
        delete(params)
    if ret == 1 and progressing:
        just_download(params)
    elif ret == 1 and not progressing:
        repair(params)
    return

def delete(params):
    log("delete: params: %s" % params)
    get = params.get
    sab_nzo_id = get("nzoid")
    sab_nzo_id_history = get("nzoidhistory")
    sab_nzo_id_history_list = get("nzoidhistory_list")
    if sab_nzo_id_history_list:
        sab_nzo_id_history_list = utils.unquote_plus(sab_nzo_id_history_list).split(";")
    folder = get("folder")
    folder = utils.unquote_plus(folder)
    incomplete = get("incomplete")
    end = get("end")
    delete_all = get("delete_all")
    if delete_all:
        utils.notification("Deleting all incomplete")
    else:
        utils.notification("Deleting %s" % xbmc.translatePath(folder))
    if sab_nzo_id or sab_nzo_id_history:
        delete_ = "ok"
        if sab_nzo_id:
            if not "None" in sab_nzo_id and not delete_all:
                pause = sabnzbd.nzo_pause(sab_nzo_id)
                log("delete: pause: %s" % pause)
                time.sleep(3)
                if "ok" in pause:
                    delete_ = sabnzbd.nzo_delete_files(sab_nzo_id)
                    log("delete: delete_: %s" % delete_)
                else:
                    delete_ = "failed"
        if sab_nzo_id_history:
            if not "None" in sab_nzo_id_history and not delete_all:
                delete_ = sabnzbd.nzo_delete_history_files(sab_nzo_id_history)
        if delete_all and sab_nzo_id_history_list:
            for sab_nzo_id_history_item in sab_nzo_id_history_list:
                delete_state = sabnzbd.nzo_delete_history_files(sab_nzo_id_history_item)
                if delete_state is not delete_:
                    delete_state = "failed"
            delete_ = delete_state
        if not "ok" in delete_:
            utils.notification("Deleting failed")
    else:
        utils.notification("Deleting failed")
        log("delete: deleting failed")
    if end:
        return
    elif incomplete:
        time.sleep(2)
        xbmc.executebuiltin("Container.Refresh")
    else:
        xbmc.executebuiltin("Action(ParentDir)")
    return

def download(params):
    log("download: params: %s" % params)
    get = params.get
    nzb = utils.unquote_plus(get("nzb"))
    nzbname = utils.unquote_plus(get("nzbname"))
    category = get_category(ask = True)
    addurl = sabnzbd.addurl(nzb, nzbname, category=category)
    log("download: addurl: %s" % addurl)
    progressDialog = xbmcgui.DialogProgress()
    progressDialog.create('Pneumatic', 'Sending request to SABnzbd')
    if "ok" in addurl:
        progressDialog.update(100, 'Request to SABnzbd succeeded')
        time.sleep(1)
    else:
        progressDialog.update(0, 'Request to SABnzbd failed!')
        time.sleep(1)
    progressDialog.close()
    return

def just_download(params):
    log("just_download: params: %s" % params)
    get = params.get
    sab_nzo_id = get("nzoid")
    category = get_category()
    set_category = sabnzbd.nzo_change_category(sab_nzo_id, category)
    log("just_download: set_category: %s" % set_category)
    if "ok" in set_category:
        utils.notification("Downloading")
    else:
        utils.notification("Manual repair required")

def get_category(ask = False):
    log("get_category: ask: %s" % ask)
    if __settings__.getSetting("sabnzbd_cat_ask").lower() == "true":
        ask = True
    if ask:
        dialog = xbmcgui.Dialog()
        category_list = sabnzbd.category_list()
        log("get_category: category_list: %s" % category_list)
        category_list.remove('*')
        category_list.insert(0, 'Default')
        ret = dialog.select('Select SABnzbd category', category_list)
        if ret == 0:
            category = None
        else:
            category = category_list[ret]
        log("get_category: category: %s" % category)
        return category
    else:
        return None

def repair(params):
    log("repair: params: %s" % params)
    get = params.get
    sab_nzo_id_history = get("nzoidhistory")
    end = get("end")
    repair_ = sabnzbd.nzo_retry(sab_nzo_id_history)
    log("repair: repair_: %s" % repair_)
    if "ok" in repair_:
        utils.notification("Repair succeeded")
    else:
        utils.notification("Repair failed")
    if not end:
        xbmc.executebuiltin("Action(ParentDir)")
    return

def incomplete():
    log("incomplete:")
    active_nzbname_list, nzbname_list = nzbname_lists()
    nzoid_history_list = [x[1] for x in nzbname_list if x[1] is not None]
    for row in active_nzbname_list:
        url = "&nzoid=" + str(row[1]) + "&nzbname=" + utils.quote_plus(row[0]) +\
              "&nzoidhistory_list=" + utils.quote_plus(';'.join(nzoid_history_list)) +\
              "&folder=" + utils.quote_plus(row[0])
        info = nfo.ReadNfoLabels(utils.join(INCOMPLETE_FOLDER, row[0]))
        info.info_labels['title'] = "Active - " + info.info_labels['title']
        add_posts(info.info_labels, url, MODE_INCOMPLETE_LIST, info.thumbnail, info.fanart)
    for row in nzbname_list:
        if row[1]:
            url = "&nzoidhistory=" + str(row[1]) + "&nzbname=" + utils.quote_plus(row[0]) +\
                  "&nzoidhistory_list=" + utils.quote_plus(';'.join(nzoid_history_list)) +\
                  "&folder=" + utils.quote_plus(row[0])
            info = nfo.ReadNfoLabels(utils.join(INCOMPLETE_FOLDER, row[0]))
            add_posts(info.info_labels, url, MODE_INCOMPLETE_LIST, info.thumbnail, info.fanart)
        else:
            # Clean out a failed SABnzbd folder removal
            utils.dir_exists(utils.join(INCOMPLETE_FOLDER, row[0]), None)
    xbmcplugin.setContent(HANDLE, 'movies')
    xbmcplugin.endOfDirectory(HANDLE, succeeded=True, cacheToDisc=True)
    return

def nzbname_lists():
    log("nzbname_lists:")
    active_nzbname_list = []
    m_nzbname_list = []
    m_row = []
    for folder in utils.listdir_dirs(INCOMPLETE_FOLDER):
        sab_nzo_id = sabnzbd.nzo_id(folder)
        if not sab_nzo_id:
            m_row.append(folder)
            m_row.append(None)
            m_nzbname_list.append(m_row)
            log("incomplete: m_nzbname_list.append: %s" % m_row)
            m_row = []
        else:
            m_row.append(folder)
            m_row.append(sab_nzo_id)
            active_nzbname_list.append(m_row)
            log("incomplete: active_nzbname_list: %s" % m_row)
            m_row = []
    nzbname_list = sabnzbd.nzo_id_history_list(m_nzbname_list)
    return active_nzbname_list, nzbname_list

def local():
    log("local:")
    type = 'add_file'
    folder_list = __settings__.getSetting('nzb_folder_list').split(';')
    if len(folder_list) == 1 and len(folder_list[0]) == 0:
        add_posts({'title':'Add folder'}, '', MODE_ADD_LOCAL, '', '', False)
    else:
        for folder in folder_list:
            folder_path = unicode(folder, 'utf-8')
            folder_name = os.path.split(os.path.dirname(folder_path))[1]
            if len(folder_path) > 1:
                url = "&type=" + type + "&folder=" + utils.quote_plus(folder_path)
                add_posts({'title':folder_name}, url, MODE_LOCAL_LIST_TOP, '', '')
    xbmcplugin.setContent(HANDLE, 'movies')
    xbmcplugin.endOfDirectory(HANDLE, succeeded=True, cacheToDisc=True)

def list_local(params):
    log("list_local: params: %s" % params)
    top_folder = utils.unquote_plus(params.get("folder"))
    type = utils.unquote_plus(params.get("type"))
    for folder in utils.listdir_dirs(top_folder):
        folder_path = utils.join(top_folder, folder)
        # Check if the folder contains a single nzb and no folders
        nzb_list = []
        folder_list = []
        for file in utils.listdir_files(folder_path):
            file_path = utils.join(folder_path, file)
            ext = os.path.splitext(file_path)[1]
            if  ext == '.nzb' or ext == '.gz' or ext == '.zip':
                nzb_list.append(file_path)
        for sub_folder in utils.listdir_dirs(folder_path):
                folder_list.append(sub_folder)
        # If single nzb allow the folder to be playable and show info
        if len(nzb_list) == 1 and len(folder_list) == 0:
            # Fixing the naming of nzb according to SAB rules
            nzb_name = m_nzb.Nzbname(os.path.basename(nzb_list[0])).final_name
            if folder.lower() == nzb_name.lower():
                info = nfo.ReadNfoLabels(folder_path)
                info.info_labels['title'] = info.info_labels['title']
                url = "&nzbname=" + utils.quote_plus(nzb_name) +\
                      "&nzb=" + utils.quote_plus(nzb_list[0]) + "&type=" + type
                add_posts(info.info_labels, url, MODE_LOCAL_FILE_IN_DIR, info.thumbnail, info.fanart, False)
            else:
                url = "&type=" + type + "&folder=" + utils.quote_plus(folder_path)
                add_posts({'title':folder}, url, MODE_LOCAL_LIST, '', '')
        else:
            url = "&type=" + type + "&folder=" + utils.quote_plus(folder_path)
            add_posts({'title':folder}, url, MODE_LOCAL_LIST, '', '')
    for file in utils.listdir_files(top_folder):
        ext = os.path.splitext(file)[1]
        if  ext == '.nzb' or ext == '.gz' or ext == '.zip':
            file_path = utils.join(top_folder, file)
            url = "&nzbname=" + utils.quote_plus(m_nzb.Nzbname(file).final_name) +\
                  "&nzb=" + utils.quote_plus(file_path) + "&type=" + type
            add_posts({'title':file}, url, MODE_LOCAL_FILE, '', '', False)
    xbmcplugin.setContent(HANDLE, 'movies')
    xbmcplugin.endOfDirectory(HANDLE, succeeded=True, cacheToDisc=True)
    return

def add_local():
    log("add_local:")
    dialog = xbmcgui.Dialog()
    nzb_file = dialog.browse(0, 'Pick a folder', 'video')
    # XBMC outputs utf-8
    path = unicode(nzb_file, 'utf-8')
    log("add_local: path: %s" % path)
    if not utils.isdir(path):
        return None
    else:
        folder_list = __settings__.getSetting("nzb_folder_list").split(';')
        folder_list.append(nzb_file)
        new_folder_list = ';'.join(folder_list)
        log("add_local: new_folder_list: %s" % new_folder_list)
        __settings__.setSetting("nzb_folder_list", new_folder_list)
        xbmc.executebuiltin("Container.Refresh")

def del_local(params):
    log("del_local: params: %s" % params)
    folder = utils.unquote_plus(params.get("folder"))
    folder_path = folder.encode('utf-8')
    folder_list = __settings__.getSetting("nzb_folder_list").split(';')
    folder_list.remove(folder_path)
    new_folder_list = ';'.join(folder_list)
    log("del_local: new_folder_list: %s" % new_folder_list)
    __settings__.setSetting("nzb_folder_list", new_folder_list)
    xbmc.executebuiltin("Container.Refresh")

def del_local_file(params):
    log("del_local_file: params: %s" % params)
    local_file = utils.unquote_plus(params.get("nzb"))
    if xbmcgui.Dialog().yesno("Pneumatic", "Delete:", "%s" % local_file):
        log("del_local_file: delete: %s" % local_file)
        utils.delete(local_file)
        xbmc.executebuiltin("Container.Refresh")
    
def del_local_file_in_dir(params):
    log("del_local_file_in_dir: params: %s" % params)
    local_file = utils.unquote_plus(params.get("nzb"))
    local_path = os.path.dirname(local_file)
    if xbmcgui.Dialog().yesno("Pneumatic", "Delete:", "%s" % local_path):
        for file in utils.listdir_files(local_path):
            local_file_path = utils.join(local_path, file)
            log("del_local_file_in_dir: delete: %s" % local_file_path)
            utils.delete(local_file_path)
        log("del_local_file_in_dir: rmdir: %s" % local_path)
        utils.rmdir(local_path)
        xbmc.executebuiltin("Container.Refresh")

def save_strm(nzbname, url):
    log("save_strm: nzbname: %s url: %s" % (nzbname, url))
    strm2lib.save_strm(__settings__, nzbname, url)
    if SAVE_NZB and utils.exists(NZB_CACHE):
        nzb_path = utils.join(NZB_CACHE, '%s%s' % (nzbname, '.nzb'))
        log("save_strm: nzb_path: %s" % nzb_path)
        m_nzb.save(url, nzb_path)

def strm_init(params):
    log("strm_init: params: %s" % params)
    strm_path = unicode(xbmc.getInfoLabel("ListItem.FileNameAndPath"), 'utf-8')
    log("strm_init: strm_path: %s" % strm_path)
    strm_base = os.path.dirname(strm_path)
    nzbname = params['nzbname']
    extensions = ['nzb', 'nzb.zip', 'nzb.gz']
    for ext in extensions:
        nzbname_ext = "%s.%s" % (utils.join(strm_base, nzbname), ext)
        if utils.exists(nzbname_ext):
            log("strm_init: exists: %s" % nzbname_ext)
            params['nzb'] = nzbname_ext
            params['type'] = 'add_file'
    return params

if (__name__ == "__main__" ):
    log('v%s started' % __settings__.getAddonInfo("version"), xbmc.LOGNOTICE)
    HANDLE = int(sys.argv[1])
    if not (__settings__.getSetting("firstrun")):
        __settings__.openSettings()
        #TODO fix this
        if utils.pass_setup_test(sabnzbd.self_test(), __settings__.getSetting("sabnzbd_incomplete")):
            __settings__.setSetting("firstrun", '1')
    else:
        if (not sys.argv[2]):
            add_posts({'title':'Incomplete'}, '', MODE_INCOMPLETE)
            add_posts({'title':'Browse local NZB\'s'}, '', MODE_LOCAL, '', '')
            xbmcplugin.setContent(HANDLE, 'movies')
            xbmcplugin.endOfDirectory(HANDLE, succeeded=True, cacheToDisc=True)
        else:
            params = utils.get_parameters(sys.argv[2])
            get = params.get
            if get("mode")== MODE_PLAY:
                is_home, sab_nzo_id = is_nzb_home(params)
                if is_home:
                    nzbname = utils.unquote_plus(get("nzbname"))
                    pre_play(nzbname, nzo=sab_nzo_id)
            if get("mode")== MODE_LIST_PLAY or get("mode")== MODE_AUTO_PLAY:
                play_video(params)
            if get("mode")== MODE_DELETE:
                delete(params)
            if get("mode")== MODE_DOWNLOAD:
                download(params)
            if get("mode")== MODE_REPAIR:
                repair(params)
            if get("mode")== MODE_INCOMPLETE:
                incomplete()
            if get("mode")== MODE_INCOMPLETE_LIST:
                list_incomplete(params)
            if get("mode")== MODE_STRM:
                xbmc.executebuiltin('Dialog.Close(all, true)')
                time.sleep(2)
                params = strm_init(params)
                is_home, sab_nzo_id = is_nzb_home(params)
                if is_home:
                    nzbname = utils.unquote_plus(get("nzbname"))
                    pre_play(nzbname, mode=MODE_STRM, nzo=sab_nzo_id)
            if get("mode")== MODE_SAVE_STRM:
                nzbname = utils.unquote_plus(get("nzbname"))
                nzb = utils.unquote_plus(get("nzb"))
                t = Thread(target=save_strm, args=(nzbname, nzb,))
                t.start()
            if get("mode")== MODE_LOCAL:
                local()
            if get("mode")== MODE_LOCAL_LIST or get("mode")== MODE_LOCAL_LIST_TOP:
                list_local(params)
            if get("mode")== MODE_ADD_LOCAL:
                add_local()
            if get("mode")== MODE_DEL_LOCAL:
                del_local(params)
            if get("mode")== MODE_DEL_LOCAL_FILE:
                del_local_file(params)
            if get("mode")== MODE_DEL_LOCAL_FILE_IN_DIR:
                del_local_file_in_dir(params)                
