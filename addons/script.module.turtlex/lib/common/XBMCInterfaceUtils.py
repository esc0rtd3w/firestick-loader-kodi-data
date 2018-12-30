'''
Created on Nov 12, 2011

@author: ajju
'''
import xbmcgui, xbmcplugin, xbmc  # @UnresolvedImport
import urllib
from common.Singleton import SingletonClass
from common import AddonUtils, ExceptionHandler, Logger
import sys

SUPPRESS_DIALOG_MSG = False

def setSuppressDialogMsg(suppressMsg=False):
    global SUPPRESS_DIALOG_MSG
    if suppressMsg:
        SUPPRESS_DIALOG_MSG = True
    else:
        SUPPRESS_DIALOG_MSG = False


def updateListItem_With_VideoHostingInfo(video_hosting_info, xbmc_list_item):
    new_label = xbmc_list_item.getLabel()
    if new_label is None or new_label == '':
        new_label = video_hosting_info.get_video_hosting_name()
    xbmc_list_item.setLabel(new_label)
    if video_hosting_info.get_video_hosting_image() is not None:
        xbmc_list_item.setThumbnailImage(video_hosting_info.get_video_hosting_image())


def updateListItem_With_VideoInfo(video_info, xbmc_list_item):
    new_label = video_info.get_video_name()
    if new_label is None or new_label == '':
        new_label = video_info.get_video_hosting_info().get_video_hosting_name()
    xbmc_list_item.setLabel(new_label)
    if video_info.get_video_image() is not None:
        xbmc_list_item.setThumbnailImage(video_info.get_video_image())
    
    
def callBackDialogProgressBar(function_obj, function_args, heading, failure_message=None, line1='Please wait...', line2='Retrieved $current_index of $total_it items', line3='To go back, press the Cancel button'):
    total_iteration = len(function_args)
    current_index = 0
    ProgressDisplayer().end()
    pDialog = None
    if not SUPPRESS_DIALOG_MSG:
        pDialog = xbmcgui.DialogProgress()
        pDialog.create(heading, line1, line2.replace('$total_it', str(total_iteration)).replace('$current_index', str(current_index)), line3)
        pDialog.update(1)
    Logger.logDebug('Total Iterations = ' + str(total_iteration))
    function_returns = []
    isCanceled = False
    for arg in function_args:
        try:
            returnedObj = function_obj(arg)
            if returnedObj is not None and type(returnedObj) is list:
                function_returns.extend(returnedObj)
            elif returnedObj is not None:
                function_returns.append(returnedObj)
            if not SUPPRESS_DIALOG_MSG and pDialog is not None:
                current_index = current_index + 1
                percent = (current_index * 100) / total_iteration
                pDialog.update(percent, line1, line2.replace('$total_it', str(total_iteration)).replace('$current_index', str(current_index)), line3)
                if (pDialog.iscanceled()):
                    isCanceled = True
                    break
        except Exception, e:
            if not SUPPRESS_DIALOG_MSG and pDialog is not None and failure_message is not None:
                pDialog.close()
                dialog = xbmcgui.Dialog()
                dialog.ok('[B][COLOR red]FAILED: [/COLOR][/B]Info Retrieval Process', failure_message, 'You may like to try again later or use other source if available')
            Logger.logFatal(e)
            raise Exception(ExceptionHandler.DONOT_DISPLAY_ERROR, '')
        if isCanceled:
            raise Exception(ExceptionHandler.PROCESS_STOPPED, 'It looks like you don\'t want wait more|Process was stopped in between')
    return function_returns
    
def sortMethod(xbmc_sort_method):
    xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmc_sort_method)
    
def setContentType(content_type):
    xbmcplugin.setContent(handle=int(sys.argv[1]), content=content_type)

def addFolderItem(item, item_next_action_id, is_folder=True):
    u = sys.argv[0] + '?actionId=' + urllib.quote_plus(item_next_action_id) + '&data=' + urllib.quote_plus(AddonUtils.encodeData(item.get_request_data()))
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=item.get_xbmc_list_item_obj(), isFolder=is_folder)
    
def addContextMenuItem(item, label, action_id, data=None):
    if data is None:
        data = item.get_request_data()
    contextMenuItems = []
    data = '?actionId=' + urllib.quote_plus(action_id) + '&data=' + urllib.quote_plus(AddonUtils.encodeData(item.get_request_data()))
    contextMenuItems.append((label, 'XBMC.RunPlugin(%s?%s)' % (sys.argv[0], data)))
    item.get_xbmc_list_item_obj().addContextMenuItems(contextMenuItems, replaceItems=False)

def executePlugin(pluginPath):
    xbmc.executebuiltin('RunPlugin(%s)' % pluginPath)

def addPlayListItem(item):
    if item.get_moving_data().has_key('videoStreamUrl'):
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.add(url=item.get_moving_data()['videoStreamUrl'], listitem=item.get_xbmc_list_item_obj())
        return "video"
    elif item.get_moving_data().has_key('audioStreamUrl'):
        playlist = xbmc.PlayList(xbmc.PLAYLIST_MUSIC)
        playlist.add(url=item.get_moving_data()['audioStreamUrl'], listitem=item.get_xbmc_list_item_obj())
        return "audio"

def setResolvedMediaUrl(item):
    new_item = None
    if item.get_moving_data().has_key('videoStreamUrl'):
        new_item = xbmcgui.ListItem(path=item.get_moving_data()['videoStreamUrl'])
    elif item.get_moving_data().has_key('audioStreamUrl'):
        new_item = xbmcgui.ListItem(path=item.get_moving_data()['audioStreamUrl'])
    xbmcplugin.setResolvedUrl(int(sys.argv[ 1 ]), True, new_item)
        
def downloadVideo(item, downloadPath):
    if item.get_moving_data().has_key('videoStreamUrl'):
        import SimpleDownloader as downloader  # @UnresolvedImport
        downloader = downloader.SimpleDownloader()
        videoUrl = item.get_moving_data()['videoStreamUrl'].partition('|')[0]
        params = { "url": videoUrl, "download_path": downloadPath}
        downloader.download(item.get_xbmc_list_item_obj().getLabel(), params)
    else:
        displayDialogMessage("Download failure!", "Unable to resolve video URL.", "Please try again with different source.")
    
def clearPlayList(list_type="video"):
    if list_type == "video":
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
    elif list_type == "audio":
        playlist = xbmc.PlayList(xbmc.PLAYLIST_MUSIC)
        playlist.clear()
    
def play(videoSrc=None, list_type="video"):
    if isPlaying():
        return
    if videoSrc == None:
        if list_type == "video":
            videoSrc = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        elif list_type == "audio":
            videoSrc = xbmc.PlayList(xbmc.PLAYLIST_MUSIC)
    xbmcPlayer = xbmc.Player()
    xbmcPlayer.play(videoSrc)
    
def isPlayingVideo():
    return xbmc.Player().isPlayingVideo() 

def isPlayingAudio():
    return xbmc.Player().isPlayingAudio() 

def isPlaying():
    return xbmc.Player().isPlaying() 

def stopPlayer():
    if isPlaying():
        xbmc.Player().stop()       

class ProgressDisplayer(SingletonClass):
    
    def __initialize__(self):
#        self.pDialog = xbmcgui.DialogProgress()
        pass
        
        
    def start(self, heading='', line1='', line2='', line3=''):
#        self.pDialog.create(heading, line1, line2, line3)
#        self.pDialog.update(1)
        pass
        
        
    def displayMessage(self, percent=1, line1='', line2='', line3='', pmessage=None):
#        if pmessage is not None:
#            lines = pmessage.split('|')
#            if len(lines) == 3:
#                line1 = lines[0]
#                line2 = lines[1]
#                line3 = lines[2]
#            elif len(lines) == 2:
#                line1 = lines[0]
#                line2 = lines[1]
#            elif len(lines) == 1:
#                line1 = lines[0]
#        self.pDialog.update(percent, line1, line2, line3)
        pass

    
    def end(self):
#        self.pDialog.close()
        pass

def displayDialogMessage(heading='', line1='', line2='', line3='', dmessage=None, msgType='[B][COLOR red]FAILURE: [/COLOR][/B]'):
    ProgressDisplayer().end()
    if dmessage is not None:
        lines = dmessage.split('|')
        if len(lines) == 3:
            line1 = lines[0]
            line2 = lines[1]
            line3 = lines[2]
        elif len(lines) == 2:
            line1 = lines[0]
            line2 = lines[1]
        elif len(lines) == 1:
            line1 = lines[0]
    if not SUPPRESS_DIALOG_MSG:
        dialog = xbmcgui.Dialog()
        dialog.ok(msgType + heading, line1, line2, line3)

def getUserInput(heading='Input', isPassword=False):
    keyb = xbmc.Keyboard()
    if isPassword:
        keyb.setDefault('password')
        keyb.setHiddenInput(True)
    keyb.setHeading(heading)
    keyb.doModal()
    text = None
    if (keyb.isConfirmed()):
        text = urllib.quote_plus(keyb.getText())
    return text

def displayNotification(header, message='', time='3000', iconimage=''):
    notification = "XBMC.Notification(%s,%s,%s,%s)" % (header, message, time, iconimage)
    xbmc.executebuiltin(notification)
    
def setSortMethods():
    
    # set sort methods - probably we don't need all of them
    xbmcplugin.addSortMethod(handle=int(sys.argv[ 1 ]), sortMethod=xbmcplugin.SORT_METHOD_UNSORTED)
    xbmcplugin.addSortMethod(handle=int(sys.argv[ 1 ]), sortMethod=xbmcplugin.SORT_METHOD_LABEL)
    xbmcplugin.addSortMethod(handle=int(sys.argv[ 1 ]), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RATING)
    xbmcplugin.addSortMethod(handle=int(sys.argv[ 1 ]), sortMethod=xbmcplugin.SORT_METHOD_DATE)
    xbmcplugin.addSortMethod(handle=int(sys.argv[ 1 ]), sortMethod=xbmcplugin.SORT_METHOD_PROGRAM_COUNT)
    xbmcplugin.addSortMethod(handle=int(sys.argv[ 1 ]), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RUNTIME)
    xbmcplugin.addSortMethod(handle=int(sys.argv[ 1 ]), sortMethod=xbmcplugin.SORT_METHOD_GENRE)
