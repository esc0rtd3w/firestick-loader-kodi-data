'''
    Ice Channel
'''

from entertainment.plugnplay.interfaces import CaptchaHandler
from entertainment.plugnplay import Plugin

class solvemediacom(CaptchaHandler):
    implements = [CaptchaHandler]
    
    name = 'solvemedia'
    
    def CanHandle(self, url, html, params=None):
                
        import re
        
        solvemedia = re.search('<iframe src="(http://api.solvemedia.com.+?)"', html)
        
        if solvemedia:
            return True
        
        return False
        
    def Handle(self, url, html, params=None):
            
        import re
        
        solvemedia = re.search('<iframe src="(http://api.solvemedia.com.+?)"', html)
        
        if solvemedia:
            
            from entertainment.net import Net
            net = Net(cached=False)
            
            html = net.http_GET( solvemedia.group(1) ).content
            
            import re
            hugekey=re.search('id="adcopy_challenge" value="(.+?)">', html).group(1)
            
            solution = self.Solve(net.http_GET("http://api.solvemedia.com%s" % re.search('<img src="(.+?)"', html).group(1)).content)
            
            if solution:
                return {'status':'ok', 'captcha_type':self.name, 'challenge': hugekey, 'captcha':solution, 'adcopy_challenge': hugekey,'adcopy_response': solution}
            else:
                return {'status':'error', 'message':'Image-Text not entered', 'captcha_type':self.name}
        
        return None