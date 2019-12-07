'''
    Ice Channel
'''

from entertainment.plugnplay.interfaces import CaptchaHandler
from entertainment.plugnplay import Plugin

class googlerecaptcha(CaptchaHandler):
    implements = [CaptchaHandler]
    
    name = 'googlerecaptcha'
    
    def CanHandle(self, url, html, params=None):
            
        import re
        
        recaptcha = re.search('<script type=[\'"]{1}text/javascript[\'"]{1} src=[\'"]{1}http://www.google.com/recaptcha/api/.+?[\'"]{1}', html)
        
        if recaptcha:
            return True
        
        return False
        
    def Handle(self, url, html, params=None):
            
        import re
        
        recaptcha = re.search('<script type=[\'"]{1}text/javascript[\'"]{1} src=[\'"]{1}(http://www.google.com/recaptcha/api/.+?)[\'"]{1}', html)
        
        if recaptcha:
            
            recaptcha = recaptcha.group(1)
            
            from entertainment.net import Net
            net = Net(cached=False)
                        
            if 'recaptcha_ajax' in recaptcha:
                import random
                recaptcha = 'http://www.google.com/recaptcha/api/challenge?k=%s&ajax=1&cachestop=%s' % ( params['site'], str(random.random()) )
            
            html = net.http_GET( recaptcha ).content
            
            import re
            hugekey=re.search('challenge \: [\'"]{1}(.+?)[\'"]{1}', html).group(1)
            
            solution = self.Solve(net.http_GET("http://www.google.com/recaptcha/api/image?c=%s" % hugekey ).content)
            
            if solution:
                return {'status':'ok', 'captcha_type':self.name, 'challenge':hugekey, 'captcha':solution, 'recaptcha_challenge_field': hugekey,'recaptcha_response_field': solution}
            else:
                return {'status':'error', 'message':'Image-Text not entered', 'captcha_type':self.name}
        
        return None