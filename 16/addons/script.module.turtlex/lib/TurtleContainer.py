'''
Created on Oct 17, 2011
Modified on Apr 11, 2013 :: Added cache support
'''

from common import DataObjects, XBMCInterfaceUtils, AddonUtils, Logger
from common.GoogleAnalytics import GAClient
from common.Singleton import SingletonClass
from common.XBMCInterfaceUtils import ProgressDisplayer
from definition.Turtle import Action, Move, Service
import sys
import xbmcaddon  # @UnresolvedImport
try:
    import StorageServer  # @UnresolvedImport
except:
    import common.storageserverdummy as StorageServer
    
__author__ = "ajju"



class AddonContext(SingletonClass):
    '''
    AddonContext will provide a way for container to access the route
    '''
    def __initialize__(self, addon_id, addon_ver=None, turtle_id='script.module.turtlex'):
        
        # Addon information
        self.addon = xbmcaddon.Addon(id=addon_id)
        self.addon_id = addon_id
        self.addon_ver = self.addon.getAddonInfo('version')
        self.addonPath = self.addon.getAddonInfo('path')
        self.addonProfile = self.addon.getAddonInfo('profile')
        
        self.turtle_addon = xbmcaddon.Addon(id=turtle_id)
        self.turtle_id = turtle_id
        self.turtle_ver = self.turtle_addon.getAddonInfo('version')
        self.turtle_addonPath = self.turtle_addon.getAddonInfo('path')
        self.turtle_addonProfile = self.turtle_addon.getAddonInfo('profile')
        
        self.cache = StorageServer.StorageServer(addon_id, 2)
        self.turtle_map = self.cache.cacheFunction(self.loadTurtleMap)
        
    
    def loadTurtleMap(self):
        turtle_filepath = AddonUtils.getCompleteFilePath(self.addonPath, 'config', 'turtle.xml')
        if not AddonUtils.doesFileExist(turtle_filepath):
            turtle_filepath = AddonUtils.getCompleteFilePath(self.turtle_addonPath, 'lib/config', 'turtle.xml')
        return AddonUtils.getBeautifulSoupObj(turtle_filepath)
    
    
    def getTurtleRoute(self, actionId):
        actionTag = self.turtle_map.find(name='action', attrs={'id':actionId})
        actionObj = Action(actionTag['id'])
        if actionTag.has_key('pmessage'):
            ProgressDisplayer().displayMessage(5, pmessage=actionTag['pmessage'])
        
        for moveTag in actionTag.findAll('move'):
            modulePath = moveTag['module']
            functionName = moveTag['function']
            pmessage = None
            if moveTag.has_key('pmessage'):
                pmessage = moveTag['pmessage']
            actionObj.addMove(Move(modulePath, functionName, pmessage))
            
        for nextActionTag in actionTag.findAll('next-action'):
            actionName = nextActionTag['name']
            actionId = nextActionTag['id']
            actionObj.addNextAction(actionName, actionId)
            
        for redirectActionTag in actionTag.findAll('redirect-action'):
            actionName = redirectActionTag['name']
            actionId = redirectActionTag['id']
            actionObj.addRedirectAction(actionName, actionId)
            
        return actionObj
    
    
    def isNextActionFolder(self, actionId, nextActionName):
        actionTag = self.turtle_map.find(name='action', attrs={'id':actionId})
        nextActionTag = actionTag.find(name='next-action', attrs={'name':nextActionName})
        return (nextActionTag['isfolder'] == 'true')
    
    def getDownloadActionIfDownloadable(self, actionId, nextActionName):
        actionTag = self.turtle_map.find(name='action', attrs={'id':actionId})
        nextActionTag = actionTag.find(name='next-action', attrs={'name':nextActionName})
        if (nextActionTag.has_key('downloadable') and nextActionTag['downloadable'] == 'true'):
            return nextActionTag['download-action-id']
        else:
            None
        
    def getTurtleServices(self):
        services = []
        serviceTags = self.turtle_map.findAll(name='service')
        for serviceTag in serviceTags:
            services.append(Service(serviceTag['name'], serviceTag['action-id']))
        return services
    
    def cleanUp(self):
        del self.addon
        del self.addonPath
        del self.addonProfile
        
        del self.cache
        
        del self.turtle_addon
        del self.turtle_addonPath
        del self.turtle_addonProfile
        del self.turtle_map
    
        
'''CONTAINER FUNCTIONS START FROM HERE'''
# INITIALIZE CONTAINER
class Container(SingletonClass):
    
    def __initialize__(self, addon_id, addon_ver=None):
        self.addon_context = AddonContext(addon_id=addon_id, addon_ver=addon_ver)
        self.ga_client = GAClient(addon_context=self.addon_context)
        self.ga_client.reportAppLaunch()
        
    def getAddonContext(self):
        return self.addon_context
        
    def getTurtleRequest(self):
        params = None
        if len(sys.argv) >= 3:
            params = str(sys.argv[2])
        self.request_obj = DataObjects.Request(params=params)
        self.response_obj = DataObjects.Response()
        return self.request_obj
    
    def getTurtleResponse(self):
        return self.response_obj
        
    def reloadTurtleRequest(self, params):
        self.request_obj = DataObjects.Request(params=params)
        self.response_obj = DataObjects.Response()
        
    def getTurtleRoute(self, actionId):
        return self.addon_context.getTurtleRoute(actionId)
        
    def moveTurtle(self, moveObj):
        if moveObj.get_pmessage() is not None:
            ProgressDisplayer().displayMessage(50, pmessage=moveObj.get_pmessage())
        components = moveObj.module_path.split('.')
        module = __import__(moveObj.module_path)
        if components is not None and isinstance(components, list):
            for index in range(1, len(components)):
                module = getattr(module, components[index])
        function = getattr(module, moveObj.function_name)
        function(self.request_obj, self.response_obj)
        
        
    def judgeTurtleNextAction(self, actionObj):
        ProgressDisplayer().displayMessage(80, line1='Preparing items for display or play', line2='Total items: ' + str(len(self.response_obj.get_item_list())))
        if self.response_obj.get_redirect_action_name() is None:
            isAnyPlayableItem = False
            isItemsList = False
            playlist_type = None
            for item in self.response_obj.get_item_list():
                nextActionId = actionObj.get_next_action_map()[item.get_next_action_name()]
                if nextActionId == '__play__':
                    if item.get_moving_data().has_key('pluginUrl'):
                        XBMCInterfaceUtils.executePlugin(item.get_moving_data()['pluginUrl'])
                    else:
                        if not isAnyPlayableItem and not XBMCInterfaceUtils.isPlaying():
                            XBMCInterfaceUtils.clearPlayList()  # Clear playlist item only when at least one video item is found.
                        playlist_type = XBMCInterfaceUtils.addPlayListItem(item)
                        isAnyPlayableItem = True
                elif nextActionId == '__service_response__':
                    # Do Nothing , get response object from container for parameters to be returned
                    pass
                elif nextActionId == '__download__':
                    downloadPath = self.addon_context.addon.getSetting('downloadPath')
                    if downloadPath is None or downloadPath == '':
                        XBMCInterfaceUtils.displayDialogMessage("Download path not provided", "Please provide download path in add-on settings.", "The download path should be a local directory.")
                        self.addon_context.addon.openSettings(sys.argv[ 0 ])
                        downloadPath = self.addon_context.addon.getSetting('downloadPath')
                    if downloadPath is not None and downloadPath != '':
                        XBMCInterfaceUtils.downloadVideo(item, downloadPath)
                elif nextActionId == '__resolved__':
                    XBMCInterfaceUtils.setResolvedMediaUrl(item)
                else:
                    isItemsList = True
                    is_Folder = self.addon_context.isNextActionFolder(actionObj.get_action_id(), item.get_next_action_name())
                    downloadAction = self.addon_context.getDownloadActionIfDownloadable(actionObj.get_action_id(), item.get_next_action_name())
                    if(downloadAction is not None):
                        XBMCInterfaceUtils.addContextMenuItem(item, 'Download Video', downloadAction)
                    XBMCInterfaceUtils.addFolderItem(item, nextActionId, is_Folder)
                del item  # deletes item
            if isAnyPlayableItem == True:
                ProgressDisplayer().end()
                try:
                    if playlist_type is not None:
                        XBMCInterfaceUtils.play(list_type=playlist_type)
                    else:
                        XBMCInterfaceUtils.play()
                except Exception, e:
                    Logger.logFatal(e)
            elif isItemsList:
                if self.response_obj.get_xbmc_sort_method() is not None:
                    XBMCInterfaceUtils.sortMethod(self.response_obj.get_xbmc_sort_method())
                if self.response_obj.get_xbmc_content_type() is not None:
                    XBMCInterfaceUtils.setContentType(self.response_obj.get_xbmc_content_type())
                XBMCInterfaceUtils.setSortMethods()

        else:
            redirectActionId = actionObj.get_redirect_action_map()[self.response_obj.get_redirect_action_name()]
            self.response_obj.set_redirect_action_name(None)
            return redirectActionId


    def performAction(self, actionId):
        ProgressDisplayer().start('Processing request...')
        while actionId is not None:
            Logger.logInfo('Action to be performed ::' + actionId)
            turtle_route = self.getTurtleRoute(actionId)
            for move in turtle_route.moves:
                self.moveTurtle(move)
            actionId = self.judgeTurtleNextAction(turtle_route)
            
        ProgressDisplayer().end()
        
    def cleanRequest(self):
        del self.response_obj
        del self.request_obj
        
    def cleanUpForService(self):
        self.addon_context.cleanUp()
        del self.addon_context
        
    def cleanUp(self):
        self.addon_context.cleanUp()
        del self.addon_context
        
        del self.response_obj
        del self.request_obj
