# -*- coding: latin-1 -*-

try:
    import StorageServer
except:
    import utils.commonplugincache.storageserverdummy as StorageServer


class CacheManager:
    
    def __init__(self):
        self._cache = StorageServer.StorageServer("Dragon Streams", 1)
        self._initCache()
        self.keys = {}
        self._loadKeys()
    
    def _initCache(self):
        oldKeys = self._cache.get("keys")
        if not oldKeys:
            self._cache.set("keys", repr( {"keys": [] } ) )        
    
    def _loadKeys(self):
        try:
            self.keys = eval(self._cache.get("keys"))
        except:
            self.keys = {}

    
    def setVar(self, name, data):
        self.keys[name] = data
        return self._cache.set(name, data)
    
    def getVar(self, name):
        return self._cache.get(name)
    
    def delVar(self, name):
        if self.keys.has_key(name):
            del self.keys[name]
        return self._cache.delete(name)
    
    def clear(self):
        for k in self.keys:
            self._cache.delete(k)
        self._loadKeys()