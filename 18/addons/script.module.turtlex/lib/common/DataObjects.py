'''
Created on Oct 30, 2011

@author: ajju
'''

from common import HttpUtils, AddonUtils, Logger

class Request(object):
    '''
    classdocs
    '''

    def __init__(self, params=None):
        Logger.logDebug(params)
        self.set_action_id('__start__')
        if params is None:
            self.set_params({})
        elif type(params) is str:
            self.set_params(HttpUtils.getUrlParams(params))
        elif type(params) is dict:
            self.set_params(params)
        if self.get_params().has_key('actionId') and self.get_params()['actionId'] != '':
            self.set_action_id(self.get_params()['actionId'])
        if self.get_params().has_key('data') and self.get_params()['data'] != '':
            self.set_data(AddonUtils.decodeData(self.get_params()['data']))


    def get_data(self):
        return self.__data


    def set_data(self, value):
        self.__data = value


    def del_data(self):
        del self.__data


    def get_action_id(self):
        return self.__actionId


    def get_params(self):
        return self.__params


    def set_action_id(self, value):
        self.__actionId = value


    def set_params(self, value):
        self.__params = value


    def del_action_id(self):
        del self.__actionId


    def del_params(self):
        del self.__params

    actionId = property(get_action_id, set_action_id, del_action_id, "actionId's docstring")
    params = property(get_params, set_params, del_params, "params's docstring")
    data = property(get_data, set_data, del_data, "data's docstring")
        
        
class Response(object):
    '''
    classdocs
    '''

    def get_service_response_obj(self):
        return self.__service_response_obj


    def set_service_response_obj(self, value):
        self.__service_response_obj = value


    def del_service_response_obj(self):
        del self.__service_response_obj


    def __init__(self):
        self.__item_list = []
        self.__redirect_action_name = None
        self.__xbmc_sort_method = None
        self.__xbmc_content_type = None
        self.__service_response_obj = {}

    def get_xbmc_sort_method(self):
        return self.__xbmc_sort_method


    '''
    xbmcplugin has following SORT methods:
        SORT_METHOD_NONE, SORT_METHOD_UNSORTED, SORT_METHOD_VIDEO_TITLE,
        SORT_METHOD_TRACKNUM, SORT_METHOD_FILE, SORT_METHOD_TITLE
        SORT_METHOD_TITLE_IGNORE_THE, SORT_METHOD_LABEL
        SORT_METHOD_LABEL_IGNORE_THE
    '''
    def set_xbmc_sort_method(self, value):
        self.__xbmc_sort_method = value


    def del_xbmc_sort_method(self):
        del self.__xbmc_sort_method

    def get_xbmc_content_type(self):
        return self.__xbmc_content_type

    '''
    xbmcplugin has following content types:
    files, songs, artists, albums, movies, tvshows, episodes, musicvideos
    '''
    def set_xbmc_content_type(self, value):
        self.__xbmc_content_type = value


    def del_xbmc_content_type(self):
        del self.__xbmc_content_type


    def get_redirect_action_name(self):
        return self.__redirect_action_name


    def set_redirect_action_name(self, value):
        self.__redirect_action_name = value


    def del_redirect_action_name(self):
        del self.__redirect_action_name


    def get_item_list(self):
        return self.__item_list


    def set_item_list(self, value):
        self.__item_list = value


    def del_item_list(self):
        del self.__item_list
        
    def extendItemList(self, items):
        self.__item_list.extend(items)

    def addListItem(self, list_item):
        if type(list_item) == ListItem:
            self.__item_list.append(list_item)
    
    def reset_item_list(self):
        self.__item_list = []
            
    def addServiceResponseParam(self, param_name, param_value):
        self.__service_response_obj[param_name] = param_value
        
    item_list = property(get_item_list, set_item_list, del_item_list, "item_list's docstring")
    redirect_action_name = property(get_redirect_action_name, set_redirect_action_name, del_redirect_action_name, "redirect_action_name's docstring")
    xbmc_sort_method = property(get_xbmc_sort_method, set_xbmc_sort_method, del_xbmc_sort_method, "xbmc_sort_method's docstring")
    xbmc_content_type = property(get_xbmc_content_type, set_xbmc_content_type, del_xbmc_content_type, "xbmc_content_type's docstring")
    service_response_obj = property(get_service_response_obj, set_service_response_obj, del_service_response_obj, "service_response_obj's docstring")
    
        

class ListItem(object):
    
    def __init__(self):
        '''
        Constructor
        '''
        self.__request_data = {}
        self.__moving_data = {}
        self.__next_action_name = None

    def get_moving_data(self):
        return self.__moving_data


    def set_moving_data(self, value):
        self.__moving_data = value


    def del_moving_data(self):
        del self.__moving_data

    def add_moving_data(self, key, value):
        self.__moving_data[key] = value

    def get_next_action_name(self):
        return self.__next_action_name


    def set_next_action_name(self, value):
        self.__next_action_name = value


    def del_next_action_name(self):
        del self.__next_action_name
        

    def get_xbmc_list_item_obj(self):
        return self.__xbmc_list_item_obj


    def set_xbmc_list_item_obj(self, value):
        self.__xbmc_list_item_obj = value


    def del_xbmc_list_item_obj(self):
        del self.__xbmc_list_item_obj


    def get_request_data(self):
        return self.__request_data


    def set_request_data(self, value):
        self.__request_data = value
        
        
    def add_request_data(self, param, value):
        self.__request_data[param] = value


    def del_request_data(self):
        del self.__request_data

    request_data = property(get_request_data, set_request_data, del_request_data, "request_data's docstring")
    xbmc_list_item_obj = property(get_xbmc_list_item_obj, set_xbmc_list_item_obj, del_xbmc_list_item_obj, "xbmc_list_item_obj's docstring")
    next_action_name = property(get_next_action_name, set_next_action_name, del_next_action_name, "next_action_name's docstring")
    moving_data = property(get_moving_data, set_moving_data, del_moving_data, "moving_data's docstring")
    
        
VIDEO_QUAL_LOW = 'LOW'
VIDEO_QUAL_SD = 'STANDARD'
VIDEO_QUAL_HD_720 = '720p'
VIDEO_QUAL_HD_1080 = '1080p'
XBMC_EXECUTE_PLUGIN = 'execute_plugin'

class VideoInfo(object):
    def __init__(self):
        self.__video_links = {}
        self.__video_stopped = True
        self.__video_name = ''
        self.__video_image = ''

    def is_video_stopped(self):
        return self.__video_stopped


    def set_video_stopped(self, value):
        self.__video_stopped = value


    def del_video_stopped(self):
        del self.__video_stopped


    def get_video_image(self):
        return self.__video_image


    def get_video_id(self):
        return self.__video_id


    def get_video_hosting_info(self):
        return self.__video_hosting_info


    def get_video_name(self):
        return self.__video_name


    def set_video_image(self, value):
        self.__video_image = value


    def set_video_id(self, value):
        self.__video_id = value


    def set_video_hosting_info(self, value):
        self.__video_hosting_info = value


    def set_video_name(self, value):
        self.__video_name = value


    def del_video_image(self):
        del self.__video_image


    def del_video_id(self):
        del self.__video_id


    def del_video_hosting_info(self):
        del self.__video_hosting_info


    def del_video_name(self):
        del self.__video_name


    def get_video_links(self):
        return self.__video_links


    def set_video_links(self, value):
        self.__video_links = value


    def del_video_links(self):
        del self.__video_links

    def get_video_link(self, video_qual):
        if self.__video_links.has_key(video_qual):
            return self.__video_links[video_qual]
        else:
            return None

    def add_video_link(self, video_qual, video_link, addUserAgent=True, addReferer=False, refererUrl=None):
        if addUserAgent:
            video_link = video_link.replace(' ', '%20') + '|' + HttpUtils.getUserAgentForXBMCPlay()
            if addReferer and refererUrl is not None:
                video_link = video_link + '&Referer=' + refererUrl
        self.__video_links[video_qual] = video_link
    
    video_image = property(get_video_image, set_video_image, del_video_image, "video_image's docstring")
    video_id = property(get_video_id, set_video_id, del_video_id, "video_id's docstring")
    video_hosting_info = property(get_video_hosting_info, set_video_hosting_info, del_video_hosting_info, "video_hosting_info's docstring")
    video_name = property(get_video_name, set_video_name, del_video_name, "video_name's docstring")
    video_stopped = property(is_video_stopped, set_video_stopped, del_video_stopped, "video_stopped's docstring")
    video_links = property(get_video_links, set_video_links, del_video_links, "video_links's docstring")


class VideoHostingInfo(object):

    def get_video_hosting_image(self):
        return self.__video_hosting_image


    def get_video_hosting_name(self):
        return self.__video_hosting_name


    def set_video_hosting_image(self, value):
        self.__video_hosting_image = value


    def set_video_hosting_name(self, value):
        self.__video_hosting_name = value


    def del_video_hosting_image(self):
        del self.__video_hosting_image


    def del_video_hosting_name(self):
        del self.__video_hosting_name


    video_hosting_image = property(get_video_hosting_image, set_video_hosting_image, del_video_hosting_image, "video_hosting_image's docstring")
    video_hosting_name = property(get_video_hosting_name, set_video_hosting_name, del_video_hosting_name, "video_hosting_name's docstring")

    
