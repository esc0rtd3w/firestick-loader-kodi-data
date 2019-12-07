from entertainment.plugnplay.interfaces import WebProxy

class cynberunlocker_com(WebProxy):

    implements = [WebProxy]
    
    name='Cyberunlocker.com'
    display_name='Cyberunlocker.com'
    
    def SetupRequest(self, urllib2, url, data=None):
        
        import urllib
        url = urllib.quote(url)
        if data:
            req = urllib2.Request('http://proxy.cyberunlocker.com/browse.php?u=' + url, data)
        else:
            req = urllib2.Request('http://proxy.cyberunlocker.com/browse.php?u=' + url)
        
        return req
        
    def ResponseReceived(self, response):
    
        import re
        response = re.sub('http://proxy\.cyberunlocker\.com/browse\.php\?u=', '', response)
    
        return response
        