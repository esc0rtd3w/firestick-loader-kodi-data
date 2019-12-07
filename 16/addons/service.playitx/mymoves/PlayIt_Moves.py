'''
Created on Dec 27, 2011

@author: ajju
'''
from TurtleContainer import Container
from common import XBMCInterfaceUtils, Logger, HttpUtils, AddonUtils
from common.DataObjects import ListItem
from moves import SnapVideo
import re
import urllib
import urllib2
import xbmcgui  # @UnresolvedImport

def ping(request_obj, response_obj):
    Container().ga_client.reportAction('ping')
    response_obj.addServiceResponseParam("response", "pong")
    response_obj.addServiceResponseParam("message", "Hi there, I am PlayIt")

    item = ListItem()
    item.set_next_action_name('pong')
    response_obj.addListItem(item)
    

def playHostedVideo(request_obj, response_obj):
    pbType = int(Container().getAddonContext().addon.getSetting('playbacktype'))
    
    Container().getAddonContext().addon.setSetting('ga_video_title', 'false')
    
    if pbType == 2 and XBMCInterfaceUtils.isPlaying():
        response_obj.addServiceResponseParam("status", "error")
        response_obj.addServiceResponseParam("title", "XBMC is already playing.")
        response_obj.addServiceResponseParam("message", "Check PlayIt Service add-on settings. Your this request is ignored.")
        item = ListItem()
        item.set_next_action_name('respond')
        response_obj.addListItem(item)
    else:
        if pbType == 0:
            XBMCInterfaceUtils.stopPlayer()
            
        video_url = request_obj.get_data()['videoLink']
        if video_url.startswith('http://goo.gl/'):
            Logger.logDebug('Found google short URL = ' + video_url)
            video_url = HttpUtils.getRedirectedUrl(video_url)
            Logger.logDebug('After finding out redirected URL = ' + video_url)
            request_obj.get_data()['videoLink'] = video_url
        if __is_valid_url(video_url):
            contentType = __check_media_url(video_url)
            if contentType is not None:
                if contentType == 'audio':
                    response_obj.set_redirect_action_name('play_direct_audio')
                    request_obj.get_data()['track_title'] = ''
                    request_obj.get_data()['track_link'] = video_url
                    request_obj.get_data()['track_artwork_url'] = ''
                else:
                    response_obj.set_redirect_action_name('play_direct_video')
            else:
                if XBMCInterfaceUtils.isPlayingAudio():
                    response_obj.addServiceResponseParam("status", "error")
                    response_obj.addServiceResponseParam("title", "Stop active music!")
                    response_obj.addServiceResponseParam("message", "Note: XBMC cannot play video when audio playback is in progress.")
                    item = ListItem()
                    item.set_next_action_name('respond')
                    response_obj.addListItem(item)
                else:
                    video_hosting_info = SnapVideo.findVideoHostingInfo(video_url)
                    if video_hosting_info is None:
                        response_obj.addServiceResponseParam("status", "error")
                        response_obj.addServiceResponseParam("title", "URL not supported")
                        response_obj.addServiceResponseParam("message", "Video URL is currently not supported by PlayIt. Please check if URL selected is correct.")
                        item = ListItem()
                        item.set_next_action_name('respond')
                        response_obj.addListItem(item)
                    else:
                        Container().ga_client.reportContentUsage('hostedvideo', video_hosting_info.get_video_hosting_name())
                        response_obj.addServiceResponseParam("status", "success")
                        if not XBMCInterfaceUtils.isPlaying():
                            XBMCInterfaceUtils.clearPlayList(list_type="video")
                            response_obj.addServiceResponseParam("message", "Enjoy your video!")
                        else:
                            response_obj.addServiceResponseParam("title", "Request Enqueued!")
                            response_obj.addServiceResponseParam("message", "Your request has been added to player queue.")
                        response_obj.set_redirect_action_name('play_it')
                        request_obj.get_data()['videoTitle'] = 'PlayIt Video'
        else:
            Logger.logError('video_url = ' + str(video_url))
            response_obj.addServiceResponseParam("status", "error")
            response_obj.addServiceResponseParam("title", "Invalid URL")
            response_obj.addServiceResponseParam("message", "Video URL is not valid one! Please check and try again.")
            item = ListItem()
            item.set_next_action_name('respond')
            response_obj.addListItem(item)
        
    
def playRawVideo(request_obj, response_obj):
    video_url = request_obj.get_data()['videoLink']
    Container().ga_client.reportAction('video')
    item = ListItem()
    item.get_moving_data()['videoStreamUrl'] = urllib2.unquote(video_url) + '|User-Agent=Apache-HttpClient'
    item.set_next_action_name('Play')
    xbmcListItem = xbmcgui.ListItem(label='Streaming Video')
    item.set_xbmc_list_item_obj(xbmcListItem)
    response_obj.addListItem(item)
    response_obj.addServiceResponseParam("status", "success")
    response_obj.addServiceResponseParam("message", "Enjoy the video!")
    
    
def playHostedAudio(request_obj, response_obj):
    url = 'https://api.soundcloud.com/i1/tracks/%s/streams?client_id=%s&secret_token=%s&soundcloudurl' % (request_obj.get_data()['trackId'], request_obj.get_data()['client_id'], request_obj.get_data()['secret_token'])
    data = {}
    data['videoLink'] = url
    data['videoTitle'] = request_obj.get_data()['track_title']
    
    request_obj.get_data()['track_link'] = 'plugin://plugin.playitx/?data=' + urllib.quote_plus(AddonUtils.encodeData(data))
    response_obj.set_redirect_action_name('play_direct')
    
    
def playRawAudio(request_obj, response_obj):
    pbType = int(Container().getAddonContext().addon.getSetting('playbacktype'))
    Container().ga_client.reportAction('audio')
    if XBMCInterfaceUtils.isPlayingVideo():
        response_obj.addServiceResponseParam("status", "error")
        response_obj.addServiceResponseParam("title", "Stop active video!")
        response_obj.addServiceResponseParam("message", "Note: XBMC cannot play audio when video playback is in progress.")
        item = ListItem()
        item.set_next_action_name('respond')
        response_obj.addListItem(item)
    elif pbType == 2 and XBMCInterfaceUtils.isPlaying():
        response_obj.addServiceResponseParam("status", "error")
        response_obj.addServiceResponseParam("title", "XBMC is already playing.")
        response_obj.addServiceResponseParam("message", "Check PlayIt Service add-on settings. Your this request is ignored.")
        item = ListItem()
        item.set_next_action_name('respond')
        response_obj.addListItem(item)
    else:
        if pbType == 0:
            XBMCInterfaceUtils.stopPlayer()
        if not XBMCInterfaceUtils.isPlaying():
            XBMCInterfaceUtils.clearPlayList(list_type="audio")
            response_obj.addServiceResponseParam("message", "Enjoy your music!")
        else:
            response_obj.addServiceResponseParam("title", "Request Enqueued!")
            response_obj.addServiceResponseParam("message", "Your request has been added to player queue.")
        item = ListItem()
        item.get_moving_data()['audioStreamUrl'] = request_obj.get_data()['track_link']
        item.set_next_action_name('Play')
        xbmcListItem = xbmcgui.ListItem(label=request_obj.get_data()['track_title'], iconImage=request_obj.get_data()['track_artwork_url'], thumbnailImage=request_obj.get_data()['track_artwork_url'])
        xbmcListItem.setInfo('music', {'title':request_obj.get_data()['track_title']})
        item.set_xbmc_list_item_obj(xbmcListItem)
        response_obj.addListItem(item)
        response_obj.addServiceResponseParam("status", "success")
    
    
def playZappyVideo(request_obj, response_obj):
    Logger.logDebug(request_obj.get_data());
    Container().ga_client.reportAction('zappyvideo')
    video_id = request_obj.get_data()['videoId']
    port = request_obj.get_data()['port']
    ipaddress = request_obj.get_data()['client_ip']
    video_url = "http://" + ipaddress + ":" + str(port) + "/?videoId=" + video_id
    item = ListItem()
    item.get_moving_data()['videoStreamUrl'] = video_url
    item.set_next_action_name('Play')
    xbmcListItem = xbmcgui.ListItem(label='Streaming Video')
    item.set_xbmc_list_item_obj(xbmcListItem)
    response_obj.addListItem(item)
    response_obj.addServiceResponseParam("status", "success")
    response_obj.addServiceResponseParam("message", "Enjoy the video!")


APPLICATION_MEDIA_TYPES = ['application/octet-stream', 'application/x-mpegURL', 'application/ogg']
def __check_media_url(video_url):
    try:
        request = urllib2.Request(video_url, headers=HttpUtils.HEADERS)
        request.get_method = lambda : 'HEAD'
        response = urllib2.urlopen(request)
        content_type = response.info().gettype()
        try:
            if(APPLICATION_MEDIA_TYPES.index(content_type) >= 0):
                return 'application'
        except ValueError:
            if re.search('audio/', content_type):
                return 'audio'
            elif re.search('video/', content_type):
                return 'video'
    except urllib2.HTTPError, he:
        Logger.logError(he)

def __is_valid_url(video_url):
    return re.match(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', video_url, re.IGNORECASE)
    
