# -*- coding: latin-1 -*-

import os
import urllib
import re
from fileUtils import setFileContent, getFileContent
import encodingUtils as enc

from beta.t0mm0.common.net import Net


#------------------------------------------------------------------------------

def get_redirected_url(url):
    head = BaseRequest().getHead(url)
    if head:
        return head.get_url()
    return None

def isOnline(url):
    return BaseRequest().getHead(url) is not None

#------------------------------------------------------------------------------





'''
    REQUEST classes
'''

class BaseRequest(object):
    
    def __init__(self, cookie_file=None):
        self.cookie_file = cookie_file
        self.net = Net()
        if cookie_file:
            self.net.set_cookies(cookie_file)
        self.url = ''
    
    def ErrorDecorator(self, fn):
        '''
            Decorator for web requests
        '''
        def wrap(*args):
            try:
                return fn(*args)
            except ValueError, e:
                print 'Failed to open "%s".' % self.url
                print 'url is invalid'
            
            except IOError, e:
                    #traceback.print_exc(file = sys.stdout)
                    print 'Failed to open "%s".' % self.url
                    if hasattr(e, 'code'):
                        print 'Failed with error code - %s.' % e.code
                    elif hasattr(e, 'reason'):
                        print "The error object has the following 'reason' attribute :", e.reason
                        print "This usually means the server doesn't exist, is down, or we don't have an internet connection."
            return None
        return wrap
    
    def _headRequest(self, url):
        def request():
            return self.net.http_HEAD(url)        
        self.url = url
        decorated = self.ErrorDecorator(request)
        return decorated()
    
    def _getRequest(self, url, form_data, headers):
        def request():
            return self.net._fetch(url, form_data, headers).content
        self.url = url
        decorated = self.ErrorDecorator(request)
        return decorated()
    
    def getHead(self, url):
        self.url = url
        return self._headRequest(url)
    
    def getSource(self, url, form_data, referer):
        url = urllib.unquote_plus(url)
        if not referer:
            referer = url
        headers = {'Referer': referer}
        response  = self._getRequest(url, form_data, headers)
        if response:
            if self.cookie_file:
                self.net.save_cookies(self.cookie_file)
        return response

#------------------------------------------------------------------------------

class DemystifiedWebRequest(BaseRequest):

    def __init__(self, cookiePath):
        super(DemystifiedWebRequest,self).__init__(cookiePath)

    def getSource(self, url, form_data, referer='', demystify=False):
        data = super(DemystifiedWebRequest, self).getSource(url, form_data, referer)
        if not data:
            return None

        if not demystify:
            # remove comments
            r = re.compile('<!--.*?(?!//)-->', re.IGNORECASE + re.DOTALL + re.MULTILINE)
            m = r.findall(data)
            if m:
                for comment in m:
                    data = data.replace(comment,'')
        else:
            import decryptionUtils as crypt
            data = crypt.doDemystify(data)

        return data

#------------------------------------------------------------------------------

class CachedWebRequest(DemystifiedWebRequest):

    def __init__(self, cookiePath, cachePath):
        super(CachedWebRequest,self).__init__(cookiePath)
        self.cachePath = cachePath
        self.cachedSourcePath = os.path.join(self.cachePath, 'page.html')
        self.currentUrlPath = os.path.join(self.cachePath, 'currenturl')
        self.lastUrlPath = os.path.join(self.cachePath, 'lasturl')

    def __setLastUrl(self, url):
        setFileContent(self.lastUrlPath, url)

    def __getCachedSource(self):
        try:
            data = getFileContent(self.cachedSourcePath)
            data = enc.smart_unicode(data)
        except:
            #data = data.decode('utf-8')
            pass
        return data

    def getLastUrl(self):
        url = getFileContent(self.lastUrlPath)
        return url

    def getSource(self, url, form_data, referer='', ignoreCache=False, demystify=False):

        if url == self.getLastUrl() and not ignoreCache:
            data = self.__getCachedSource()
        else:
            data = enc.smart_unicode(super(CachedWebRequest,self).getSource(url, form_data, referer, demystify))
            if data:
                # Cache url
                self.__setLastUrl(url)
                # Cache page
                setFileContent(self.cachedSourcePath, data)
        return data
