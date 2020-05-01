# -*- coding: latin-1 -*-

import os
import urllib
from urlparse import urlparse

import utils.regexUtils as rU
import utils.scrapingUtils as sU
import utils.fileUtils as fU
import utils.githubUtils as github
from utils.githubUtils import GitHubAPI


# enums
class SyncSourceType:
    CATCHERS = 1
    MODULES = 2


# entities

class SyncManager:
    def __init__(self):
        self.sources = []
        self.__githubAPI = None
    
    def __getSourceByName__(self, name):
        found = filter(lambda x : x.name == name, self.sources)
        if found and len(found) > 0:
            return found[0]
        return None
    
    def addSource(self, name, sourceType, url):
        if not self.__getSourceByName__(name):
            hostName = sU.getHostName(url)
            if hostName == 'github.com':
                if not self.__githubAPI:
                    self.__githubAPI = GitHubAPI()
                self.sources.append(GitHubSource(name, sourceType, url, self.__githubAPI))
    
    def removeSource(self, name):
        source = self.__getSourceByName__(name)
        if source:
            self.sources.remove(source)
    
    def setSourceEnabledState(self, name, enabled):
        source = self.__getSourceByName__(name)
        if source:
            source.enabled = enabled
    
    def getSources(self):
        if len(self.sources) > 0:
            return map(lambda x : x.name, self.sources)
        else:
            return None
    
    
    def getUpdates(self, sourceType, localCachePath):
        updates = {}
        
        def battleSyncObjects(source, target):
            if source.checksum != target.checksum:
                return source
            else:
                return target
        
        def battleUpdates(uSource, uTarget):
            winner = battleSyncObjects(uSource.source, uTarget.source)
            if winner == uSource.source:
                return uSource
            else:
                return uTarget
            
        def addToUpdates(update):
            if not updates.has_key(update.name):
                updates[update.name] = update
            else:
                updates[update.name] = battleUpdates(update, updates[update.name])
        
        if len(self.sources) == 0:
            return None
                
        local = self.__getLocalFiles__(localCachePath)
        
        for source in self.sources:
            if source.enabled and source.type == sourceType:
                syncObjects = source.getFiles()
                if not syncObjects:
                    continue
                for obj in syncObjects:
                    name = obj.name
                    found = filter(lambda x : x.name == name, local)
                    if found and len(found) > 0:
                        old = found[0]
                        winner = battleSyncObjects(obj, old)
                        if winner == obj:
                            addToUpdates(Update(name, obj, old))
                    else:
                        s = SyncObject()
                        s.name = name
                        s.file = os.path.join(localCachePath, name)
                        s.created = obj.created
                        s.checksum = obj.checksum
                        addToUpdates(Update(name, obj, s))
                            
        return updates
    
    
    def __getLocalFiles__(self, folder):            
        if folder:
            syncObjects = []
            for root, _, files in os.walk(folder, topdown = False):
                relpath = root.replace(folder, '').replace('\\','/').strip('/')
                for name in files:
                    path = os.path.join(root, name)
                    obj = SyncObject()
                    obj.name = relpath
                    if obj.name != '':
                        obj.name += '/' + name
                    else:
                        obj.name = name
                    obj.file = path
                    obj.created = fU.lastModifiedAt(path)
                    obj.checksum = github.getGithash(path)
                    syncObjects.append(obj)
            return syncObjects
        
        return None
        
    
class SyncObject:
    def __init__(self):
        self.name = None
        self.file = None
        self.created = None
        self.checksum = None    


class Update:
    def __init__(self, name, source, target):
        self.name = name
        self.source = source
        self.target = target
    
    def do(self):
        if self.source and self.target:
            response = None
            try:
                f = urllib.urlopen(self.source.file)
                response = f.read()
                f.close()
            except:
                return False
                        
            fU.setFileContent(self.target.file, response, True)
            return True
        
        return False
    
    

class SyncSourceBase(object):
    
    def __init__(self, name, sourceType, url):
        self.name = name
        self._url = url
        self.type = sourceType
        self.enabled = True
    
    def getFiles(self):
        syncObjects = self.getFilesAPI()         
        return syncObjects
    
    def getFilesAPI(self):
        pass
    
    def getFilesScrape(self):
        pass
        

class GitHubSource(SyncSourceBase):
    
    def __init__(self, name, sourceType, url, api = None):
        SyncSourceBase.__init__(self, name, sourceType, url)
        self.__api = api
        
    def getFilesAPI(self):
        if not self.__api:
            return None
        
        url = self._url
        parts = urlparse(url)
        cleanPath = parts.path[1:]
        parts = cleanPath.split('/', 4)
        userName = parts[0]
        repoName = parts[1]
        branchName = parts[3]
        
        folderName = None
        if len(parts) > 4:
            folderName = parts[4]
        
        entries = self.__api.getEntries(userName, repoName, branchName, folderName)
        if not entries:
            return None
        
        # file = blob, directory = tree
        files = filter(lambda x: x.type == 'blob', entries)
        
        syncObjects = []
        for f in files:
            obj = SyncObject()
            relpath = f.path
            if folderName:
                relpath = relpath.replace(folderName + '/', '')
            obj.name = relpath
            obj.file =  "https://github.com/%s/%s/raw/%s/" % (userName, repoName, branchName)
            if folderName:
                obj.file += folderName + "/" 
            obj.file += obj.name
            obj.created = None # would be another request to github api
            obj.checksum = f.sha
            syncObjects.append(obj)
                
        return syncObjects