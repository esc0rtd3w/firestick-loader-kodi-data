# -*- coding: utf-8 -*-
"""
openload.io urlresolver plugin
Copyright (C) 2015 tknorris

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""
import re
import base64
import json
from urlresolver9 import common
from urlresolver9.resolver import UrlResolver, ResolverError
from urlresolver9.common import i18n

import js2py
import os

API_BASE_URL = 'https://api.openload.co/1'
INFO_URL = API_BASE_URL + '/streaming/info'
GET_URL = API_BASE_URL + '/streaming/get?file={media_id}'
FILE_URL = API_BASE_URL + '/file/info?file={media_id}'

try:
    compat_chr = unichr  # Python 2
except NameError:
    compat_chr = chr
#urllib2.urlopen("https://your-test-server.local", context=ctx)

class OpenLoadResolver(UrlResolver):
    name = "openload"
    domains = ["openload.io", "openload.co"]
    #pattern = '(?://|\.)(openload\.(?:io|co))/(?:embed|f)/([0-9a-zA-Z\-_]+)'
    pattern = '(?://|\.)(openload\.(?:io|co))/(?:embed|f)/([0-9a-zA-Z-_]+)'

    def __init__(self):
        self.net = common.Net()

    def get_media_url(self, host, media_id):
        try:

            myurl = 'http://openload.co/embed/%s' % media_id
            HTTP_HEADER = {'User-Agent': common.FF_USER_AGENT,'Referer': myurl}  # 'Connection': 'keep-alive'

            response = self.net.http_GET(myurl, headers=HTTP_HEADER)
            html = response.content
            common.log_utils.log_notice('%s; DIRECTORY' % os.getcwd())

            videoUrl = media_id


            if not self.__file_exists(media_id):
                raise ResolverError('File Not Available')

            try:
                ol_id = re.findall(r'''<span[^>]+id=(["'])[^"']+\1[^>]*>(?P<id>[0-9A-Za-z]+)</span>''',html)
                video_url = 'https://openload.co/stream/%s?mime=true'
                decoded = self._eval_id_decoding(html, ol_id[0][-1])
                video_url = video_url % decoded
                #video_url = self.mytest(ol_id[0][-1])
                return video_url
            except Exception as e:
                common.log_utils.log_notice('%s; falling back to method with pairing, error: %s' % (media_id,e))

                video_url = self.__check_auth(media_id)
                if not video_url:
                    video_url = self.__auth_ip(media_id)


            if video_url:
                return video_url
            else:
                raise ResolverError(i18n('no_ol_auth'))

            #return videoUrl + helpers.append_headers({'User-Agent': common.FF_USER_AGENT})
            return videoUrl
            # video_url = 'https://openload.co/stream/%s?mime=true' % myvidurl


        except Exception as e:
            common.log_utils.log_notice('Exception during openload resolve parse: %s' % e)
            print("Error", e)
            raise

    def get_url(self, host, media_id):
        return 'http://openload.io/embed/%s' % media_id

    def mytest(self,ol_id):
        #ol_id = self._search_regex(
        #    '<span[^>]+id="[^"]+"[^>]*>([0-9A-Za-z]+)</span>',
        #    webpage, 'openload ID')

        decoded = ''
        a = ol_id[0:24]
        b = []
        for i in range(0, len(a), 8):
            b.append(int(a[i:i + 8] or '0', 16))
        ol_id = ol_id[24:]
        j = 0
        k = 0
        while j < len(ol_id):
            c = 128
            d = 0
            e = 0
            f = 0
            _more = True
            while _more:
                if j + 1 >= len(ol_id):
                    c = 143
                f = int(ol_id[j:j + 2] or '0', 16)
                j += 2
                d += (f & 127) << e
                e += 7
                _more = f >= c
            g = d ^ b[k % 3]
            for i in range(4):
                char_dec = (g >> 8 * i) & (c + 127)
                char = compat_chr(char_dec)
                if char != '#':
                    decoded += char
            k += 1

        video_url = 'https://openload.co/stream/%s?mime=true'
        video_url = video_url % decoded
        return video_url

    def __file_exists(self, media_id):
        js_data = self.__get_json(FILE_URL.format(media_id=media_id))
        return js_data.get('result', {}).get(media_id, {}).get('status') == 200

    def __auth_ip(self, media_id):
        js_data = self.__get_json(INFO_URL)
        pair_url = js_data.get('result', {}).get('auth_url', '')
        if pair_url:
            pair_url = pair_url.replace('\/', '/')
            header = i18n('ol_auth_header')
            line1 = i18n('auth_required')
            line2 = i18n('visit_link')
            line3 = i18n('click_pair') % (pair_url)
            with common.kodi.CountdownDialog(header, line1, line2, line3) as cd:
                return cd.start(self.__check_auth, [media_id])

    def __check_auth(self, media_id):
        try:
            js_data = self.__get_json(GET_URL.format(media_id=media_id))
        except ResolverError as e:
            status, msg = e
            if status == 403:
                return
            else:
                raise ResolverError(msg)

        return js_data.get('result', {}).get('url')

    def __get_json(self, url):
        result = self.net.http_GET(url).content
        common.log_utils.log(result)
        js_result = json.loads(result)
        if js_result['status'] != 200:
            raise ResolverError(js_result['status'], js_result['msg'])
        return js_result

    def _eval_id_decoding(self, webpage, ol_id):
        try:
            # raise # uncomment to test method with pairing
            #js_code = re.findall(
            #    ur"(ﾟωﾟﾉ=.*?\('_'\);.*?)ﾟωﾟﾉ= /｀ｍ´）ﾉ ~┻━┻   //\*´∇｀\*/ \['_'\];"
            #,webpage, re.DOTALL)[0]
            js_code = re.findall(
                #ur"(ﾟωﾟﾉ=.*?\('_'\);.*?)ﾟωﾟﾉ= /｀ｍ´）ﾉ ~┻━┻   //\*´∇｀\*/ \['_'\];",
                ur"(ﾟωﾟﾉ=.*?\('_'\);.*?)ﾟωﾟﾉ= /｀ｍ´）ﾉ",
                webpage,re.S)

            #common.log_utils.log_notice('js_code: %s' % js_code)
            js_code = re.sub('''if\s*\([^\}]+?typeof[^\}]+?\}''', '', js_code)
            js_code = re.sub('''if\s*\([^\}]+?document[^\}]+?\}''', '', js_code)
        except Exception as e:
            print 'Could not find JavaScript %s' % e
            raise ResolverError('Could not find JavaScript %s' % e)
        print("AAA1", ol_id, js_code)
        #js_code = base64.b64decode('''ICAgICAgICAgICAgICAgICAgICB2YXIgaWQgPSAiJXMiDQogICAgICAgICAgICAgICAgICAgICAgLCBkZWNvZGVkDQogICAgICAgICAgICAgICAgICAgICAgLCBkb2N1bWVudCA9IHt9DQogICAgICAgICAgICAgICAgICAgICAgLCB3aW5kb3cgPSB0aGlzDQogICAgICAgICAgICAgICAgICAgICAgLCAkID0gZnVuY3Rpb24oKXsNCiAgICAgICAgICAgICAgICAgICAgICAgICAgcmV0dXJuIHsNCiAgICAgICAgICAgICAgICAgICAgICAgICAgICB0ZXh0OiBmdW5jdGlvbihhKXsNCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGlmKGEpDQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGRlY29kZWQgPSBhOw0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgZWxzZQ0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICByZXR1cm4gaWQ7DQogICAgICAgICAgICAgICAgICAgICAgICAgICAgfSwNCiAgICAgICAgICAgICAgICAgICAgICAgICAgICByZWFkeTogZnVuY3Rpb24oYSl7DQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICBhKCkNCiAgICAgICAgICAgICAgICAgICAgICAgICAgICB9DQogICAgICAgICAgICAgICAgICAgICAgICAgIH0NCiAgICAgICAgICAgICAgICAgICAgICAgIH07DQogICAgICAgICAgICAgICAgICAgIChmdW5jdGlvbihkLCB3KXsNCiAgICAgICAgICAgICAgICAgICAgICB2YXIgZiA9IGZ1bmN0aW9uKCl7fTsNCiAgICAgICAgICAgICAgICAgICAgICB2YXIgcyA9ICcnOw0KICAgICAgICAgICAgICAgICAgICAgIHZhciBvID0gbnVsbDsNCiAgICAgICAgICAgICAgICAgICAgICB2YXIgYiA9IGZhbHNlOw0KICAgICAgICAgICAgICAgICAgICAgIHZhciBuID0gMDsNCiAgICAgICAgICAgICAgICAgICAgICB2YXIgZGYgPSBbJ2Nsb3NlJywnY3JlYXRlQXR0cmlidXRlJywnY3JlYXRlRG9jdW1lbnRGcmFnbWVudCcsJ2NyZWF0ZUVsZW1lbnQnLCdjcmVhdGVFbGVtZW50TlMnLCdjcmVhdGVFdmVudCcsJ2NyZWF0ZU5TUmVzb2x2ZXInLCdjcmVhdGVSYW5nZScsJ2NyZWF0ZVRleHROb2RlJywnY3JlYXRlVHJlZVdhbGtlcicsJ2V2YWx1YXRlJywnZXhlY0NvbW1hbmQnLCdnZXRFbGVtZW50QnlJZCcsJ2dldEVsZW1lbnRzQnlOYW1lJywnZ2V0RWxlbWVudHNCeVRhZ05hbWUnLCdpbXBvcnROb2RlJywnb3BlbicsJ3F1ZXJ5Q29tbWFuZEVuYWJsZWQnLCdxdWVyeUNvbW1hbmRJbmRldGVybScsJ3F1ZXJ5Q29tbWFuZFN0YXRlJywncXVlcnlDb21tYW5kVmFsdWUnLCd3cml0ZScsJ3dyaXRlbG4nXTsNCiAgICAgICAgICAgICAgICAgICAgICBkZi5mb3JFYWNoKGZ1bmN0aW9uKGUpe2RbZV09Zjt9KTsNCiAgICAgICAgICAgICAgICAgICAgICB2YXIgZG9fID0gWydhbmNob3JzJywnYXBwbGV0cycsJ2JvZHknLCdkZWZhdWx0VmlldycsJ2RvY3R5cGUnLCdkb2N1bWVudEVsZW1lbnQnLCdlbWJlZHMnLCdmaXJzdENoaWxkJywnZm9ybXMnLCdpbWFnZXMnLCdpbXBsZW1lbnRhdGlvbicsJ2xpbmtzJywnbG9jYXRpb24nLCdwbHVnaW5zJywnc3R5bGVTaGVldHMnXTsNCiAgICAgICAgICAgICAgICAgICAgICBkb18uZm9yRWFjaChmdW5jdGlvbihlKXtkW2VdPW87fSk7DQogICAgICAgICAgICAgICAgICAgICAgdmFyIGRzID0gWydVUkwnLCdjaGFyYWN0ZXJTZXQnLCdjb21wYXRNb2RlJywnY29udGVudFR5cGUnLCdjb29raWUnLCdkZXNpZ25Nb2RlJywnZG9tYWluJywnbGFzdE1vZGlmaWVkJywncmVmZXJyZXInLCd0aXRsZSddOw0KICAgICAgICAgICAgICAgICAgICAgIGRzLmZvckVhY2goZnVuY3Rpb24oZSl7ZFtlXT1zO30pOw0KICAgICAgICAgICAgICAgICAgICAgIHZhciB3YiA9IFsnY2xvc2VkJywnaXNTZWN1cmVDb250ZXh0J107DQogICAgICAgICAgICAgICAgICAgICAgd2IuZm9yRWFjaChmdW5jdGlvbihlKXt3W2VdPWI7fSk7DQogICAgICAgICAgICAgICAgICAgICAgdmFyIHdmID0gWydhZGRFdmVudExpc3RlbmVyJywnYWxlcnQnLCdhdG9iJywnYmx1cicsJ2J0b2EnLCdjYW5jZWxBbmltYXRpb25GcmFtZScsJ2NhcHR1cmVFdmVudHMnLCdjbGVhckludGVydmFsJywnY2xlYXJUaW1lb3V0JywnY2xvc2UnLCdjb25maXJtJywnY3JlYXRlSW1hZ2VCaXRtYXAnLCdkaXNwYXRjaEV2ZW50JywnZmV0Y2gnLCdmaW5kJywnZm9jdXMnLCdnZXRDb21wdXRlZFN0eWxlJywnZ2V0U2VsZWN0aW9uJywnbWF0Y2hNZWRpYScsJ21vdmVCeScsJ21vdmVUbycsJ29wZW4nLCdwb3N0TWVzc2FnZScsJ3Byb21wdCcsJ3JlbGVhc2VFdmVudHMnLCdyZW1vdmVFdmVudExpc3RlbmVyJywncmVxdWVzdEFuaW1hdGlvbkZyYW1lJywncmVzaXplQnknLCdyZXNpemVUbycsJ3Njcm9sbCcsJ3Njcm9sbEJ5Jywnc2Nyb2xsVG8nLCdzZXRJbnRlcnZhbCcsJ3NldFRpbWVvdXQnLCdzdG9wJ107DQogICAgICAgICAgICAgICAgICAgICAgd2YuZm9yRWFjaChmdW5jdGlvbihlKXt3W2VdPWY7fSk7DQogICAgICAgICAgICAgICAgICAgICAgdmFyIHduID0gWydkZXZpY2VQaXhlbFJhdGlvJywnaW5uZXJIZWlnaHQnLCdpbm5lcldpZHRoJywnbGVuZ3RoJywnb3V0ZXJIZWlnaHQnLCdvdXRlcldpZHRoJywncGFnZVhPZmZzZXQnLCdwYWdlWU9mZnNldCcsJ3NjcmVlblgnLCdzY3JlZW5ZJywnc2Nyb2xsWCcsJ3Njcm9sbFknXTsNCiAgICAgICAgICAgICAgICAgICAgICB3bi5mb3JFYWNoKGZ1bmN0aW9uKGUpe3dbZV09bjt9KTsNCiAgICAgICAgICAgICAgICAgICAgICB2YXIgd28gPSBbJ2FwcGxpY2F0aW9uQ2FjaGUnLCdjYWNoZXMnLCdjcnlwdG8nLCdleHRlcm5hbCcsJ2ZyYW1lRWxlbWVudCcsJ2ZyYW1lcycsJ2hpc3RvcnknLCdpbmRleGVkREInLCdsb2NhbFN0b3JhZ2UnLCdsb2NhdGlvbicsJ2xvY2F0aW9uYmFyJywnbWVudWJhcicsJ25hdmlnYXRvcicsJ29uYWJvcnQnLCdvbmFuaW1hdGlvbmVuZCcsJ29uYW5pbWF0aW9uaXRlcmF0aW9uJywnb25hbmltYXRpb25zdGFydCcsJ29uYmVmb3JldW5sb2FkJywnb25ibHVyJywnb25jYW5wbGF5Jywnb25jYW5wbGF5dGhyb3VnaCcsJ29uY2hhbmdlJywnb25jbGljaycsJ29uY29udGV4dG1lbnUnLCdvbmRibGNsaWNrJywnb25kZXZpY2Vtb3Rpb24nLCdvbmRldmljZW9yaWVudGF0aW9uJywnb25kcmFnJywnb25kcmFnZW5kJywnb25kcmFnZW50ZXInLCdvbmRyYWdsZWF2ZScsJ29uZHJhZ292ZXInLCdvbmRyYWdzdGFydCcsJ29uZHJvcCcsJ29uZHVyYXRpb25jaGFuZ2UnLCdvbmVtcHRpZWQnLCdvbmVuZGVkJywnb25lcnJvcicsJ29uZm9jdXMnLCdvbmhhc2hjaGFuZ2UnLCdvbmlucHV0Jywnb25pbnZhbGlkJywnb25rZXlkb3duJywnb25rZXlwcmVzcycsJ29ua2V5dXAnLCdvbmxhbmd1YWdlY2hhbmdlJywnb25sb2FkJywnb25sb2FkZWRkYXRhJywnb25sb2FkZWRtZXRhZGF0YScsJ29ubG9hZHN0YXJ0Jywnb25tZXNzYWdlJywnb25tb3VzZWRvd24nLCdvbm1vdXNlZW50ZXInLCdvbm1vdXNlbGVhdmUnLCdvbm1vdXNlbW92ZScsJ29ubW91c2VvdXQnLCdvbm1vdXNlb3ZlcicsJ29ubW91c2V1cCcsJ29ub2ZmbGluZScsJ29ub25saW5lJywnb25wYWdlaGlkZScsJ29ucGFnZXNob3cnLCdvbnBhdXNlJywnb25wbGF5Jywnb25wbGF5aW5nJywnb25wb3BzdGF0ZScsJ29ucHJvZ3Jlc3MnLCdvbnJhdGVjaGFuZ2UnLCdvbnJlc2V0Jywnb25yZXNpemUnLCdvbnNjcm9sbCcsJ29uc2Vla2VkJywnb25zZWVraW5nJywnb25zZWxlY3QnLCdvbnNob3cnLCdvbnN0YWxsZWQnLCdvbnN0b3JhZ2UnLCdvbnN1Ym1pdCcsJ29uc3VzcGVuZCcsJ29udGltZXVwZGF0ZScsJ29udG9nZ2xlJywnb250cmFuc2l0aW9uZW5kJywnb251bmxvYWQnLCdvbnZvbHVtZWNoYW5nZScsJ29ud2FpdGluZycsJ29ud2Via2l0YW5pbWF0aW9uZW5kJywnb253ZWJraXRhbmltYXRpb25pdGVyYXRpb24nLCdvbndlYmtpdGFuaW1hdGlvbnN0YXJ0Jywnb253ZWJraXR0cmFuc2l0aW9uZW5kJywnb253aGVlbCcsJ29wZW5lcicsJ3BhcmVudCcsJ3BlcmZvcm1hbmNlJywncGVyc29uYWxiYXInLCdzY3JlZW4nLCdzY3JvbGxiYXJzJywnc2VsZicsJ3Nlc3Npb25TdG9yYWdlJywnc3BlZWNoU3ludGhlc2lzJywnc3RhdHVzYmFyJywndG9vbGJhcicsJ3RvcCddOw0KICAgICAgICAgICAgICAgICAgICAgIHdvLmZvckVhY2goZnVuY3Rpb24oZSl7d1tlXT1vO30pOw0KICAgICAgICAgICAgICAgICAgICAgIHZhciB3cyA9IFsnbmFtZSddOw0KICAgICAgICAgICAgICAgICAgICAgIHdzLmZvckVhY2goZnVuY3Rpb24oZSl7d1tlXT1zO30pOw0KICAgICAgICAgICAgICAgICAgICB9KShkb2N1bWVudCwgd2luZG93KTsNCiAgICAgICAgICAgICAgICAgICAgJXM7DQogICAgICAgICAgICAgICAgICAgIHByaW50KGRlY29kZWQpOw==''') % (ol_id, js_code)
        #print("AAA2", ol_id, js_code)
        js_code = '''
            var id = "%s"
              , decoded
              , document = {}
              , window = this
              , $ = function(){
                  return {
                    text: function(a){
                      if(a)
                        decoded = a;
                      else
                        return id;
                    },
                    ready: function(a){
                      a()
                    }
                  }
                };
            (function(d){
              var f = function(){};
              var s = '';
              var o = null;
              ['close','createAttribute','createDocumentFragment','createElement','createElementNS','createEvent','createNSResolver','createRange','createTextNode','createTreeWalker','evaluate','execCommand','getElementById','getElementsByName','getElementsByTagName','importNode','open','queryCommandEnabled','queryCommandIndeterm','queryCommandState','queryCommandValue','write','writeln'].forEach(function(e){d[e]=f;});
              ['anchors','applets','body','defaultView','doctype','documentElement','embeds','firstChild','forms','images','implementation','links','location','plugins','styleSheets'].forEach(function(e){d[e]=o;});
              ['URL','characterSet','compatMode','contentType','cookie','designMode','domain','lastModified','referrer','title'].forEach(function(e){d[e]=s;});
            })(document);
            %s;
            decoded;''' % (ol_id, js_code)


        try:
            decoded = js2py.eval_js(js_code)
            if ' ' in decoded or decoded == '':
                raise
            return decoded
        except Exception as e:
            raise ResolverError('Could not eval ID decoding %s' %e)