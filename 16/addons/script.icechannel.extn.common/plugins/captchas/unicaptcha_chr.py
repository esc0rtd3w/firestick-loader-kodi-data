'''
    Ice Channel
'''

from entertainment.plugnplay.interfaces import CaptchaHandler
from entertainment.plugnplay import Plugin

class unicaptcha(CaptchaHandler):
    implements = [CaptchaHandler]
    
    name = 'unicaptcha'
    
    def CanHandle(self, url, html, params=None):
        
        import re
        
        unicaptcha = re.search('padding-left:\d+px;padding-top:\d+px\;\'\>.*?\<\/span\>', html)
        
        if unicaptcha:
            return True
        
        return False
        
    def Handle(self, url, html, params=None):
        
        import re
        
        unicaptcha = re.findall(r'padding-left:(\d+)px;padding-top:\d+px\;\'\>(.*?)\<\/span\>', html, re.I)
        
        if unicaptcha:
            
            from entertainment import htmlcleaner
            codeD = {}
            code = ''

            for key, value in unicaptcha:
                value2 = htmlcleaner.unescape(value)
                codeD.update({int(key): str(value2)})

            for key in sorted(codeD.iterkeys()):
                code = code+codeD[key]

            if code:
                return {'status':'ok', 'captcha_type':self.name, 'captcha':str(code) }
            else:
                return {'status':'error', 'message':'Captcha failure', 'captcha_type':self.name}
        
        return None