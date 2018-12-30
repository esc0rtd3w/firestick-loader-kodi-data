'''
Created on Nov 24, 2011

@author: ajju
'''
from common.DataObjects import ListItem
import xbmcgui  # @UnresolvedImport

def prepareVideoItem(request_obj, response_obj):
    item = ListItem()
    item.add_moving_data('videoUrl', request_obj.get_data()['videoLink'])
    item.set_next_action_name('Play')
    xbmcListItem = xbmcgui.ListItem(label=request_obj.get_data()['videoTitle'])
    if(request_obj.get_data().has_key('videoInfo')):
        meta = request_obj.get_data()['videoInfo']
        xbmcListItem.setIconImage(meta['thumb_url'])
        xbmcListItem.setThumbnailImage(meta['cover_url'])
        xbmcListItem.setInfo('video', meta)
    item.set_xbmc_list_item_obj(xbmcListItem)
    response_obj.addListItem(item)


def preparePlayListItems(request_obj, response_obj):
    if request_obj.get_data().has_key('videoPlayListItems'):
        playList = request_obj.get_data()['videoPlayListItems']
        for videoItem in playList:
            item = ListItem()
            item.add_moving_data('videoUrl', videoItem['videoLink'])
            item.set_next_action_name('Play')
            xbmcListItem = xbmcgui.ListItem(label=videoItem['videoTitle'])
            if(request_obj.get_data().has_key('videoInfo')):
                meta = request_obj.get_data()['videoInfo']
                xbmcListItem.setIconImage(meta['thumb_url'])
                xbmcListItem.setThumbnailImage(meta['cover_url'])
                xbmcListItem.setInfo('video', meta)
            item.set_xbmc_list_item_obj(xbmcListItem)
            response_obj.addListItem(item)
