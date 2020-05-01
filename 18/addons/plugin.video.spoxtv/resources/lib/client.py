# -*- coding: utf-8 -*-

import simple_requests as requests

class Client(object):

    def __init__(self):
        self.headers = {'User-Agent':'iPhone',
                        'Host':'fta.performfeeds.com',
                        'Origin':'http://player.performgroup.com',
                        'Referer':'http://player.performgroup.com/fta/fta.html',
                        }

        self.params = {'_fmt':'json',
                        '_rt':'c',
                        }

        self.live_feeds = ['5w44is9j2kg1exsezt1prbln',      # la liga
                            '15mr4d7sk5ozr19pg3wukpy6xy',   # serie a
                            '6hb4vxgg0v5h1wmeszxg6tj5d',    # ligue 1
                            '1kg3w2dghuz811gi8ievfcehbg',   # capital one cup
                            '17f2wdxjk7d3k1h5tzqxarsshg',   # nfl
                            '1afp49nwvibsa1odik6302ensg',   # nba
                            '1qc5gbmew6d0f1le90szgf6nmz',   # south america wcq
                            '14ycunmhmyaly1ditl2qp9d3ll',   # championship
                            'h74jgqrq4v531ja61e1ekl5ld',    # copa del rey
                            '1qy6syz7xrs5v12i7m6e3xxksn',   # jupiler pro league
                            '11so6ig8yk0hu1u7k0jxew9zpd',   # rugby six nations
                            '1ces60xgq8i8i1i6yr6etdpfus',   # primera division
                            '10amwadygsuaa1dqgibu4p66sb',   # temporary
                            ]

                            #'16pwtsmir4rip18i4x3jbtfrx4',    unknown

    def get_categories(self):
        result = {}
        try:
            url = 'http://xml.eplayer.performgroup.com/eplayer/structure/1q76ar0oz29chzaqk5mxmxt7o'
            data = requests.get(url, headers=self.headers, params=self.params).json()
            if not 'errorCode' in data:
                return data
        except:
            pass
        return result
        
    def get_videos(self, id, offset, total):
        result = {}
        try:
            url = 'http://xml.eplayer.performgroup.com/eplayer/mrss/1q76ar0oz29chzaqk5mxmxt7o/%s/%s-%s' % (id,offset,total)
            data = requests.get(url, headers=self.headers, params=self.params).json()
            if not 'errorCode' in data:
                return data
        except:
            pass
        return result
        
    def get_live_videos(self, id):
        result = {}
        try:
            url = 'http://fta.performfeeds.com/ftalivestream/3y0k606h5xy31p08hi6ldmirf/%s/' % id
            data = requests.get(url, headers=self.headers, params=self.params).json()
            if not 'errorCode' in data:
                return data
        except:
            pass
        return result
        
    def get_all_live_videos(self):
        result = []
        for id in self.live_feeds:
            data = self.get_live_videos(id)
            if 'streams' in data:
                result.append(data)
        return result
        
    def get_live_stream(self, id):
        result = {}
        try:
            url = 'http://fta.performfeeds.com/livestreamlaunch/3y0k606h5xy31p08hi6ldmirf/%s/' % id
            data = requests.get(url, headers=self.headers, params=self.params).json()
            if not 'errorCode' in data:
                return data
        except:
            pass
        return result
        
    def get_data(self, url):
        result = ''
        try:
            r = requests.get(url)
            if r.status_code == 200:
                return r.text
        except:
            pass
        return result