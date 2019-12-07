# -*- coding: utf-8 -*-


import re
from liveresolver.modules import client

def resolve(url):
        result = client.request(url,referer="http://nbahd.com/2015/11/15/detroit-pistons-los-angeles-lakers-nov-15-2015/", mobile=True)
        print(result)
        return


