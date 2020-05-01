'''
    common XBMC Module
    Copyright (C) 2011 t0mm0

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
from entertainment import cookielib

import gzip
import re
import StringIO
import urllib
import urllib2
import socket

import socks
from dns.resolver import Resolver
from httplib import HTTPConnection

#Set Global timeout - Useful for slow connections.
socket.setdefaulttimeout(60)

class DNSHTTPConnection(HTTPConnection):
    _dnsproxy = []
    def connect(self):
        resolver = Resolver()
        resolver.nameservers = self._dnsproxy
        answer = resolver.query(self.host, 'A')
        self.host = answer.rrset.items[0].address
        self.sock = socket.create_connection((self.host, self.port))

class DNSHTTPHandler(urllib2.HTTPHandler):
    _dnsproxy = []
    def http_open(self, req):
        DNSHTTPConnection._dnsproxy = self._dnsproxy 
        return self.do_open(DNSHTTPConnection, req)

class SocksiPyConnection(HTTPConnection):
    def __init__(self, proxytype, proxyaddr, proxyport = None, rdns = True, username = None, password = None, *args, **kwargs):
        self.proxyargs = (proxytype, proxyaddr, proxyport, rdns, username, password)
        HTTPConnection.__init__(self, *args, **kwargs)
 
    def connect(self):
        self.sock = socks.socksocket()
        self.sock.setproxy(*self.proxyargs)
        if isinstance(self.timeout, float):
            self.sock.settimeout(self.timeout)
        self.sock.connect((self.host, self.port))
            
class SocksiPyHandler(urllib2.HTTPHandler):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kw = kwargs
        urllib2.HTTPHandler.__init__(self)
 
    def http_open(self, req):
        def build(host, port=None, strict=None, timeout=0):    
            conn = SocksiPyConnection(*self.args, host = host, port = port, strict = strict, timeout = timeout, **self.kw)
            return conn
        return self.do_open(build, req)

from entertainment import common

HELPER = 'netcache'

Cache_Interval = int(common.addon.get_setting('cache_retention'))

#Cache Actions
Cache_None = 'none'
Cache_Insert = 'insert'
Cache_Update = 'update'

class HeadRequest(urllib2.Request):
    '''A Request class that sends HEAD requests'''
    def get_method(self):
        return 'HEAD'

class Net:
    '''
    This class wraps :mod:`urllib2` and provides an easy way to make http
    requests while taking care of cookies, proxies, gzip compression and 
    character encoding.
    
    Example::
    
        from addon.common.net import Net
        net = Net()
        response = net.http_GET('http://xbmc.org')
        print response.content
    '''
    
    _cj = cookielib.LWPCookieJar()
    _proxy = None
    _user_agent = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.1 ' + \
                  '(KHTML, like Gecko) Chrome/13.0.782.99 Safari/535.1'
    _http_debug = False
    
    _socket_class = None
    
    _web_proxy = None
    
    
    def __init__(self, cookie_file='', proxy='', user_agent='', 
                 http_debug=False, cached=True, do_not_cache_if_any=[]):
        '''
        Kwargs:
            cookie_file (str): Full path to a file to be used to load and save
            cookies to.
            
            proxy (str): Proxy setting (eg. 
            ``'http://user:pass@example.com:1234'``)
            
            user_agent (str): String to use as the User Agent header. If not 
            supplied the class will use a default user agent (chrome)
            
            http_debug (bool): Set ``True`` to have HTTP header info written to
            the XBMC log for all requests.
        '''
        
        # setup net cache if cached == True
        self._cached = cached
        self._do_not_cache_if_any = do_not_cache_if_any
        if self._cached == True:
            self._local_cache_db = 'netcache.db'            
            try:
                #raise Exception('Remote Net Cache Disabled...')
                if  common.addon.get_setting('use_remote_db')=='true' and   \
                    common.addon.get_setting('db_address') is not None and  \
                    common.addon.get_setting('db_user') is not None and     \
                    common.addon.get_setting('db_pass') is not None and     \
                    common.addon.get_setting('db_name') is not None:
                    import mysql.connector as database
                    common.addon.log('-' + HELPER + '- -' +'Loading MySQLdb as DB engine', 2)
                    self._DB = 'mysql'
                else:
                    raise ValueError('MySQL not enabled or not setup correctly')
            except:
                try: 
                    import sqlite3
                    from sqlite3 import dbapi2 as database
                    common.addon.log('-' + HELPER + '- -' +'Loading sqlite3 as DB engine version: %s' % database.sqlite_version, 2)
                except Exception, e:
                    from pysqlite2 import dbapi2 as database
                    common.addon.log('-' + HELPER + '- -' +'pysqlite2 as DB engine', 2)
                self._DB = 'sqlite'
                
            import os
            import xbmc
                
            db_path = common.addon.get_setting('local_db_location')
            if db_path:
                self.path = xbmc.translatePath(db_path)
            else:
                self.path = xbmc.translatePath('special://profile/addon_data/script.icechannel/databases')            
            self.path = common.make_dir(self.path, '')            
            self.db = os.path.join(self.path, self._local_cache_db)
            
            # connect to db at class init and use it globally
            if self._DB == 'mysql':
                class MySQLCursorDict(database.cursor.MySQLCursor):
                    def _row_to_python(self, rowdata, desc=None):
                        row = super(MySQLCursorDict, self)._row_to_python(rowdata, desc)
                        if row:
                            return dict(zip(self.column_names, row))
                        return None
                self.dbcon = database.connect(database=common.addon.get_setting('db_name'), user=common.addon.get_setting('db_user'), 
                    password=common.addon.get_setting('db_pass'), host=common.addon.get_setting('db_address'), buffered=True, charset='utf8')                
                self.dbcur = self.dbcon.cursor(cursor_class=MySQLCursorDict, buffered=True)
            else:
                self.dbcon = database.connect(self.db)
                self.dbcon.row_factory = database.Row # return results indexed by field names and not numbers so we can convert to dict
                self.dbcon.text_factory = str
                self.dbcur = self.dbcon.cursor()
                    
            self._create_net_cache_tables()
        
        if cookie_file:
            self.set_cookies(cookie_file)
        if proxy:
            self.set_proxy(proxy)
        if user_agent:
            self.set_user_agent(user_agent)
        self._http_debug = http_debug
    
    def __del__(self):
        if self._cached == True:
            ''' Cleanup db when object destroyed '''
            try:
                self.dbcur.close()
                self.dbcon.close()
            except: pass
            
    def _prepare_dns_proxy(self, dnsproxy):
        print 'Using DNS Proxy: ' + ','.join(dnsproxy)
        DNSHTTPHandler._dnsproxy = dnsproxy
        opener = urllib2.build_opener(DNSHTTPHandler, urllib2.HTTPCookieProcessor(self._cj))
        return opener
        
    def _prepare_proxy(self, ip, port, username='', password='', socks5=True):
        if (socks5==True):
            if ((password is not '') and (username is not '')):
                print 'Using socks5 authenticated proxy: ' + ip + ':' + port
                opener = urllib2.build_opener(SocksiPyHandler(socks.PROXY_TYPE_SOCKS5, ip, int(port), True, username, password))
            else:
                print 'Using socks5 proxy: ' + ip + ':' + port
                opener = urllib2.build_opener(SocksiPyHandler(socks.PROXY_TYPE_SOCKS5, ip, int(port)))
        elif (socks5==False):
            us_proxy = 'http://' + ip + ':' + port
            proxy_handler = urllib2.ProxyHandler({'http' : us_proxy})
            if ((password is not '') and (username is not '')):
                print 'Using authenticated proxy: ' + us_proxy
                password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
                password_mgr.add_password(None, us_proxy, username, password)
                proxy_auth_handler = urllib2.ProxyBasicAuthHandler(password_mgr)
                opener = urllib2.build_opener(proxy_handler, proxy_auth_handler, urllib2.HTTPCookieProcessor(self._cj))
            else:
                print 'Using proxy: ' + us_proxy
                opener = urllib2.build_opener(proxy_handler, urllib2.HTTPCookieProcessor(self._cj))
        return opener
    
    def _update_opener(self, url):
        '''
        Builds and installs a new opener to be used by all future calls to 
        :func:`urllib2.urlopen`.
        '''
        
        opener=None
        
        if self._http_debug:
            http = urllib2.HTTPHandler(debuglevel=1)
        else:
            http = urllib2.HTTPHandler()
            
        if self._socket_class or self._proxy:
            if self._socket_class:
                urllib2.socket.socket = self._socket_class        
        
            if self._proxy:
                opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self._cj),
                                              urllib2.ProxyHandler({'http': 
                                                                    self._proxy}), 
                                              urllib2.HTTPBasicAuthHandler(),
                                              http)
            
        else:            
            
            from entertainment.plugnplay.interfaces import ProxySupport
            #common.loadplugins([ProxySupport])
            internetConnectionSettings = common.GetiStreamSettings(common.settings_Internet_Connection)
            # lets check if the url is from a proxy support extension
            supported=None
            for item in ProxySupport.implementors():
                for domain in item.domains:
                    if url.lower().startswith(domain.lower()):                        
                        supported=item
                        break
                if supported:
                    break
            
            if supported:                            
                #lets check if proxy defined
                proxy_index_on_item = int(internetConnectionSettings.Settings().get_setting(supported.name))
                if proxy_index_on_item > 0:
                    lp_item = 'lp_%s' % str(proxy_index_on_item)
                    lp_enabled = internetConnectionSettings.Settings().get_setting(lp_item)
                    if lp_enabled and lp_enabled == 'true':
                        lp_ct = int (internetConnectionSettings.Settings().get_setting(lp_item + '_connection_type'))
                        if lp_ct == 0:
                            lp_ct_p_ip = internetConnectionSettings.Settings().get_setting(lp_item + '_ct_p_ip')
                            lp_ct_p_port = internetConnectionSettings.Settings().get_setting(lp_item + '_ct_p_port')
                            lp_ct_p_username = internetConnectionSettings.Settings().get_setting(lp_item + '_ct_p_username')
                            lp_ct_p_password = internetConnectionSettings.Settings().get_setting(lp_item + '_ct_p_password')
                            lp_ct_p_socks5 = internetConnectionSettings.Settings().get_setting(lp_item + '_ct_p_socks5')
                            opener = self._prepare_proxy(lp_ct_p_ip,lp_ct_p_port,lp_ct_p_username,lp_ct_p_password,lp_ct_p_socks5=='true')
                        elif lp_ct == 1:
                            dnsproxy = []
                            lp_ct_dp_ip1 = internetConnectionSettings.Settings().get_setting(lp_item + '_ct_dp_ip1')
                            lp_ct_dp_ip2 = internetConnectionSettings.Settings().get_setting(lp_item + '_ct_dp_ip2')
                            lp_ct_dp_ip3 = internetConnectionSettings.Settings().get_setting(lp_item + '_ct_dp_ip3')
                            if lp_ct_dp_ip1: dnsproxy.append(lp_ct_dp_ip1)
                            if lp_ct_dp_ip2: dnsproxy.append(lp_ct_dp_ip2)
                            if lp_ct_dp_ip3: dnsproxy.append(lp_ct_dp_ip3)
                            opener = self._prepare_dns_proxy(dnsproxy)
                        elif lp_ct == 2:
                            selected_wp = internetConnectionSettings.Settings().get_setting(lp_item + '_ct_wp')                            
                            from entertainment.plugnplay.interfaces import WebProxy
                            common.loadplugins([WebProxy])
                            for wp in WebProxy.implementors():
                                if wp.name == selected_wp:
                                    self._web_proxy = wp
                                    break
                
            if not opener and not self._web_proxy: # local proxy not available lets check global proxy
                gp_enabled = internetConnectionSettings.Settings().get_setting('global_proxy')
                if gp_enabled and gp_enabled == 'true':
                    gp_item='gp'
                    gp_ct = int(internetConnectionSettings.Settings().get_setting(gp_item + '_connection_type'))
                    if gp_ct == 0:
                        gp_ct_p_ip = internetConnectionSettings.Settings().get_setting(gp_item + '_ct_p_ip')
                        gp_ct_p_port = internetConnectionSettings.Settings().get_setting(gp_item + '_ct_p_port')
                        gp_ct_p_username = internetConnectionSettings.Settings().get_setting(gp_item + '_ct_p_username')
                        gp_ct_p_password = internetConnectionSettings.Settings().get_setting(gp_item + '_ct_p_password')
                        gp_ct_p_socks5 = internetConnectionSettings.Settings().get_setting(gp_item + '_ct_p_socks5')
                        opener = self._prepare_proxy(gp_ct_p_ip,gp_ct_p_port,gp_ct_p_username,gp_ct_p_password,gp_ct_p_socks5=='true')
                    elif gp_ct == 1:
                        dnsproxy = []
                        gp_ct_dp_ip1 = internetConnectionSettings.Settings().get_setting(gp_item + '_ct_dp_ip1')
                        gp_ct_dp_ip2 = internetConnectionSettings.Settings().get_setting(gp_item + '_ct_dp_ip2')
                        gp_ct_dp_ip3 = internetConnectionSettings.Settings().get_setting(gp_item + '_ct_dp_ip3')
                        if gp_ct_dp_ip1: dnsproxy.append(gp_ct_dp_ip1)
                        if gp_ct_dp_ip2: dnsproxy.append(gp_ct_dp_ip2)
                        if gp_ct_dp_ip3: dnsproxy.append(gp_ct_dp_ip3)
                        opener = self._prepare_dns_proxy(dnsproxy)
                    elif gp_ct == 2:
                        selected_wp = internetConnectionSettings.Settings().get_setting(gp_item + '_ct_wp')
                        from entertainment.plugnplay.interfaces import WebProxy
                        common.loadplugins([WebProxy])
                        for wp in WebProxy.implementors():
                            if wp.name == selected_wp:
                                self._web_proxy = wp
                                break
                    
                    
        if not opener:        
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self._cj),
                                          urllib2.HTTPBasicAuthHandler(),
                                          http)
                                              
        urllib2.install_opener(opener)
        

            
    def _create_net_cache_tables(self):
    
        sql_create = "CREATE TABLE IF NOT EXISTS netcache ("\
                            "id TEXT,"\
                            "request_url TEXT,"\
                            "response_url TEXT,"\
                            "headers TEXT,"\
                            "content TEXT,"\
                            "cached TIMESTAMP,"\
                            "UNIQUE(id)"\
                            ");"
        if self._DB == 'mysql':
            sql_create = sql_create.replace("id TEXT", "id VARCHAR(32)")
            sql_create = sql_create.replace("content TEXT", "content MEDIUMTEXT")
            self.dbcur.execute(sql_create)
            try: self.dbcur.execute('CREATE INDEX ncindex on netcache (id);')
            except: pass
            try: self.dbcur.execute('CREATE INDEX nctmindex on netcache (cached);')
            except: pass
        else:
            self.dbcur.execute(sql_create)
            self.dbcur.execute('CREATE INDEX IF NOT EXISTS ncindex on netcache (id);')
            self.dbcur.execute('CREATE INDEX IF NOT EXISTS nctmindex on netcache (cached);')
            
        common.addon.log('-' + HELPER + '- -' +'Table netcache initialized', 0)
        
    def _update_cache(self, url, form_data={}, http_response = None):
        if self._cached == False or not http_response:
            return
        
        request_url = url
        if form_data:
            from entertainment import odict
            ordered_form_data = odict.odict(form_data)
            ordered_form_data.sort(key=lambda x: x[0].lower())
            request_url = request_url + '?' + urllib.urlencode(ordered_form_data)
        
        import hashlib
        id = hashlib.md5(request_url).hexdigest()
        
        sql_update = ''
        
        if self._DB == 'mysql':
            sql_update = "UPDATE netcache SET response_url = %s, headers = %s, content = %s, cached = %s WHERE id = %s"
        else:
            sql_update = "UPDATE netcache SET response_url = ?, headers = ?, content = ?, cached = ? WHERE id = ?"
        
        import datetime
        cache_tm = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        
        common.addon.log('-' + HELPER + '- -' +'%s: %s, %s' % (sql_update, cache_tm, id), 2)
            
        try:
            self.dbcur.execute(sql_update, (http_response.get_url(), common.ConvertListToString(http_response.get_headers()), http_response.content, cache_tm, id) )
            self.dbcon.commit()
            #common.addon.log('-' + HELPER + '- - success')
        except Exception, e:
            common.addon.log('-' + HELPER + '- - failure: %s' % e )
            pass

    def _insert_cache(self, url, form_data={}, http_response=None):
        if self._cached == False or not http_response:
            return
        request_url = url
        if form_data:
            from entertainment import odict
            ordered_form_data = odict.odict(form_data)
            ordered_form_data.sort(key=lambda x: x[0].lower())
            request_url = request_url + '?' + urllib.urlencode(ordered_form_data)
        
        import hashlib
        id = hashlib.md5(request_url).hexdigest()
        
        sql_insert = ''
        
        if self._DB == 'mysql':
            sql_insert = "INSERT INTO netcache( id, request_url, response_url, headers, content, cached ) VALUES(%s, %s, %s, %s, %s, %s)"
        else:
            sql_insert = "INSERT INTO netcache( id, request_url, response_url, headers, content, cached ) VALUES(?, ?, ?, ?, ?, ?)"            
        
        import datetime
        cache_tm = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        
        common.addon.log('-' + HELPER + '- -' +'%s: %s, %s' % (sql_insert, id, cache_tm), 2)
                    
        try:
            self.dbcur.execute(sql_insert, (id, request_url, http_response.get_url(), common.ConvertListToString(http_response.get_headers()), http_response.content, cache_tm) )
            self.dbcon.commit()
            #common.addon.log('-' + HELPER + '- - success')
        except Exception, e:
            common.addon.log('-' + HELPER + '- - failure: %s' % e )
            pass
    
    def _get_from_cache(self, url, form_data={}):
    
        if self._cached == False:
            return (Cache_None, False, None)
        
        request_url = url
        if form_data:
            from entertainment import odict
            ordered_form_data = odict.odict(form_data)
            ordered_form_data.sort(key=lambda x: x[0].lower())
            request_url = request_url + '?' + urllib.urlencode(ordered_form_data)
        
        import hashlib
        id = hashlib.md5(request_url).hexdigest()
        
        cache_action = Cache_Insert
        cache_found = False
        cache_content = None
            
        try:
            sql_select = ''
            if self._DB == 'mysql':
                sql_select = "SELECT response_url, headers, content, cached FROM netcache WHERE id = %s " 
            else:
                sql_select = "SELECT response_url, headers, content, cached FROM netcache WHERE id = ? " 
                
            self.dbcur.execute(sql_select, (id, ) )    
            matchedrow = self.dbcur.fetchall()[0]
            
            #common.addon.log('Cache - Item Found')
            
            match = dict(matchedrow)
            import datetime
            
            try:                
                cached_tm = datetime.datetime.strptime(str(match['cached']), "%Y-%m-%d %H:%M:%S")
            except:
                import time
                cached_tm = datetime.datetime(*(time.strptime(str(match['cached']), "%Y-%m-%d %H:%M:%S")[0:6]))
                
            curr_dt = datetime.datetime.today()
            time_diff = curr_dt - cached_tm
            interval = datetime.timedelta ( hours = Cache_Interval )
            
            if time_diff < interval:
                #common.addon.log('Cache - Item Found - Valid')
                cache_action = Cache_None
                cache_found = True
                cache_content = HttpResponseCached(match['response_url'], common.ConvertStringToList(match['headers']), match['content'])
            else:
                #common.addon.log('Cache - Item Found - Invalid')
                cache_action = Cache_Update
                cache_found = True
                cache_content = None
            
        except: 
            common.addon.log('Cache - Item Not Found')
            cache_action = Cache_Insert
            cache_found = False
            cache_content = None
            pass
            
        return (cache_action, cache_found, cache_content)
    
    def clear_cache(self):
   
        sql_delete = 'DELETE FROM netcache'
        success = False
        try:
            common.addon.log('-' + HELPER + '- -' + sql_delete, 2)
            self.dbcur.execute( sql_delete )
            self.dbcon.commit()
            success = True
        except Exception, e:
            common.addon.log('-' + HELPER + '- - failure: %s' % e )
            pass         
        finally:
            return success
    
    def cleanup_cache(self):
        
        import datetime
        cutoff_date = str(datetime.date.today() - datetime.timedelta(hours=Cache_Interval))
        
        sql_delete = ''
        sql_delete = "DELETE FROM netcache WHERE cached < '%s'" % cutoff_date            
        
        try:
            common.addon.log('-' + HELPER + '- -' +sql_delete,2)
            self.dbcur.execute(sql_delete)
            self.dbcon.commit()
        except Exception, e:
            common.addon.log('-' + HELPER + '- - failure: %s' % e )
            pass
    
    def set_socket_class(self, socket_class):
        self._socket_class = socket_class
    
    def set_cookies(self, cookie_file, force=True):
        '''
        Set the cookie file and try to load cookies from it if it exists.
        
        Args:
            cookie_file (str): Full path to a file to be used to load and save
            cookies to.
        '''
        import os
        cookie_valid = False
        if os.path.exists(cookie_file):
            try:
                # open cookie file
                cookie = open(cookie_file).read()
                
                # get cookie expired time
                expire = re.search('expires="(.*?)"',cookie, re.I)    
                if expire:
                    expire = str(expire.group(1))
                    import time
                    if time.time() > time.mktime(time.strptime(expire, '%Y-%m-%d %H:%M:%SZ')):
                        # cookie expired
                        cookie_valid = False
                    else:
                        self._cj.load(cookie_file, ignore_discard=True)
                        cookie_valid = True
                else:
                    self._cj.load(cookie_file, ignore_discard=True)
                    cookie_valid = True
                
            except:
                cookie_valid = False
                
        return cookie_valid
        
    
    def get_cookies(self):
        '''Returns A dictionary containing all cookie information by domain.'''
        return self._cj._cookies


    def save_cookies(self, cookie_file):
        '''
        Saves cookies to a file.
        
        Args:
            cookie_file (str): Full path to a file to save cookies to.
        '''
        self._cj.save(cookie_file, ignore_discard=True)        

        
    def set_proxy(self, proxy):
        '''
        Args:
            proxy (str): Proxy setting (eg. 
            ``'http://user:pass@example.com:1234'``)
        '''
        self._proxy = proxy

        
    def get_proxy(self):
        '''Returns string containing proxy details.'''
        return self._proxy
        
        
    def set_user_agent(self, user_agent):
        '''
        Args:
            user_agent (str): String to use as the User Agent header.
        '''
        self._user_agent = user_agent

        
    def get_user_agent(self):
        '''Returns user agent string.'''
        return self._user_agent
    
    def http_GET(self, url, headers={}, compression=True,auto_read_response=True, url_for_cache=None):
        '''
        Perform an HTTP GET request.
        
        Args:
            url (str): The URL to GET.
            
        Kwargs:
            headers (dict): A dictionary describing any headers you would like
            to add to the request. (eg. ``{'X-Test': 'testing'}``)

            compression (bool): If ``True`` (default), try to use gzip 
            compression.
            
        Returns:
            An :class:`HttpResponse` object containing headers and other 
            meta-information about the page and the page content.
        '''
        return self._fetch(url, headers=headers, compression=compression,auto_read_response=auto_read_response, url_for_cache=url_for_cache)
        

    def http_POST(self, url, form_data, headers={}, compression=True, auto_read_response=True, url_for_cache=None, form_data_for_cache=None):
        '''
        Perform an HTTP POST request.
        
        Args:
            url (str): The URL to POST.
            
            form_data (dict): A dictionary of form data to POST.
            
        Kwargs:
            headers (dict): A dictionary describing any headers you would like
            to add to the request. (eg. ``{'X-Test': 'testing'}``)

            compression (bool): If ``True`` (default), try to use gzip 
            compression.

        Returns:
            An :class:`HttpResponse` object containing headers and other 
            meta-information about the page and the page content.
        '''
        return self._fetch(url, form_data, headers=headers, 
            compression=compression,auto_read_response=auto_read_response, url_for_cache=url_for_cache, form_data_for_cache=form_data_for_cache)

    
    def http_HEAD(self, url, headers={}, auto_read_response=True):
        '''
        Perform an HTTP HEAD request.
        
        Args:
            url (str): The URL to GET.
        
        Kwargs:
            headers (dict): A dictionary describing any headers you would like
            to add to the request. (eg. ``{'X-Test': 'testing'}``)
        
        Returns:
            An :class:`HttpResponse` object containing headers and other 
            meta-information about the page.
        '''
        
        # custom socket
        if self._socket_class:
            urllib2.socket.socket = self._socket_class
        
        req = HeadRequest(url)
        req.add_header('User-Agent', self._user_agent)
        for k, v in headers.items():
            req.add_header(k, v)
        response = urllib2.urlopen(req, timeout=3)
        return HttpResponse(response, auto_read_response=auto_read_response)


    def _fetch(self, url, form_data={}, headers={}, compression=True, auto_read_response=True, url_for_cache=None, form_data_for_cache=None):
        '''
        Perform an HTTP GET or POST request.
        
        Args:
            url (str): The URL to GET or POST.
            
            form_data (dict): A dictionary of form data to POST. If empty, the 
            request will be a GET, if it contains form data it will be a POST.
            
        Kwargs:
            headers (dict): A dictionary describing any headers you would like
            to add to the request. (eg. ``{'X-Test': 'testing'}``)

            compression (bool): If ``True`` (default), try to use gzip 
            compression.

        Returns:
            An :class:`HttpResponse` object containing headers and other 
            meta-information about the page and the page content.            
        '''
        
        cache_action = Cache_None
        cache_found = True
        cache_content = None
        
        if self._cached == True:
            if not url_for_cache:
                url_for_cache = url
            if not form_data_for_cache:
                form_data_for_cache = form_data
                
            (cache_action, cache_found, cache_content) = self._get_from_cache(url_for_cache, form_data_for_cache)

            if cache_action == Cache_None and cache_found == True and cache_content:
                return cache_content
        
        old_opener = urllib2._opener
        self._web_proxy=None
        self._update_opener(url)
        
        encoding = ''
        
        if form_data:
            if isinstance(form_data, dict):
                form_data = urllib.urlencode(form_data)
                
        req = urllib2.Request(url)
        if form_data:
            req = urllib2.Request(url, form_data)
            
        if self._web_proxy:
            req = self._web_proxy.SetupRequest(urllib2, url, form_data)
            
        req.add_header('User-Agent', self._user_agent)
        for k, v in headers.items():
            req.add_header(k, v)
        if compression:
            req.add_header('Accept-Encoding', 'gzip')
        response = urllib2.urlopen(req, timeout=3)
                
        http_response = HttpResponse( response, auto_read_response=auto_read_response, net=self, 
            cache_action = Cache_None if auto_read_response == True else ( Cache_Update if cache_action == Cache_Insert else cache_action ), 
            url_for_cache=url_for_cache, form_data_for_cache=form_data_for_cache,
            do_not_cache_if_any=self._do_not_cache_if_any, web_proxy=self._web_proxy )
        
        urllib2.install_opener(old_opener)
            
        if cache_action == Cache_Insert or cache_action == Cache_Update:
            if self._do_not_cache_if_any and len(self._do_not_cache_if_any) > 0:
                for item in self._do_not_cache_if_any:
                    if item in http_response.content:
                        cache_action = Cache_None
                        break
        
        if cache_action == Cache_Insert:
            self._insert_cache(url_for_cache, form_data_for_cache, http_response)
        elif cache_action == Cache_Update:
            self._update_cache(url_for_cache, form_data_for_cache, http_response) 
        
        return http_response
        
    def http_POST_BINARY(self, site, path, data, headers={}, compression=True, auto_read_response=True ):
        
        if site.startswith("http://"):
            site = site[7:]
        
        headers.update( { 'User-Agent' : self._user_agent } )
        
        if compression:
            headers.update( {'Accept-Encoding' : 'gzip'} )
            
        import httplib
        
        conn = httplib.HTTPConnection(site)
        conn.request("POST", path, data, headers)
        response = conn.getresponse()
        
        http_response = HttpResponse( response, auto_read_response=auto_read_response)
        
        return http_response

class HttpResponseCached:
    
    content = ''
    
    def __init__(self, response_url, response_headers, response_content):
        self._response_url = response_url
        self._response_headers = response_headers
        
        encoding = None
        response_headers = str(response_headers)
        if 'charset=' in response_headers:
            import re
            encoding = re.search('charset=([0-9a-zA-Z\_\-]+?)', response_headers)
            if encoding:
                encoding = encoding.group(1)

        r = re.search('<meta\s+http-equiv="Content-Type"\s+content="(?:.+?);' +
                      '\s+charset=(.+?)"', response_content, re.IGNORECASE)
        if r:
            encoding = r.group(1) 
        
        if encoding:
            self.content = unicode(response_content, encoding)
        else:
            self.content = unicode(response_content, 'UTF-8')
        
    def get_headers(self):
        return self._response_headers
        
    def get_url(self):
        return self._response_url
       
    def read_response(self):        
        return self.content

class HttpResponse:
    '''
    This class represents a resoponse from an HTTP request.
    
    The content is examined and every attempt is made to properly encode it to
    Unicode.
    
    .. seealso::
        :meth:`Net.http_GET`, :meth:`Net.http_HEAD` and :meth:`Net.http_POST` 
    '''
    
    content = ''
    '''Unicode encoded string containing the body of the reposne.'''
    
    
    def __init__( self, response, auto_read_response=True, net=None, cache_action=Cache_None, 
                    url_for_cache='', form_data_for_cache={}, do_not_cache_if_any=[], web_proxy=None ):
        '''
        Args:
            response (:class:`mimetools.Message`): The object returned by a call
            to :func:`urllib2.urlopen`.
            
            auto_read_response: (:bool:): Whether the reda the response or not.
            If True: response is read right-away
            If False: response is not read right-away, 
                call read_response() to fetch and return the response later.
        '''
        self._response = response
        self._net = net
        self._auto_read_response = auto_read_response
        self._cache_action = cache_action
        self._url_for_cache = url_for_cache
        self._form_data_for_cache = form_data_for_cache
        self._do_not_cache_if_any = do_not_cache_if_any
        self._web_proxy = web_proxy
        
        if self._auto_read_response == True:
            self.read_response()
    
    def get_headers(self):
        '''Returns a List of headers returned by the server.'''
        return self._response.info().headers
    
        
    def get_url(self):
        '''
        Return the URL of the resource retrieved, commonly used to determine if 
        a redirect was followed.
        '''
        return self._response.geturl()
        
    def read_response(self):
    
        if self.content == '':
            html = self._response.read()

            try:
                try:
                    content_encoding = self._response.headers['content-encoding'].lower()
                except:
                    content_encoding = self._response.getheader(u'content-encoding', u'').lower()
                if content_encoding in ('gzip', u'gzip'):
                    html = gzip.GzipFile(fileobj=StringIO.StringIO(html)).read()
            except:
                pass
            
            encoding = None
            try:
                try:
                    content_type = self._response.headers['content-type']
                except:
                    content_type = self._response.getheader(u'content-type', u'')
                if 'charset=' in content_type:
                    encoding = content_type.split('charset=')[-1]
            except:
                pass
            
            r = re.search('<meta\s+http-equiv="Content-Type"\s+content="(?:.+?);' +
                          '\s+charset=(.+?)"', html, re.IGNORECASE)
            if r:
                encoding = r.group(1) 

            try:
                if encoding:
                    html = unicode(html, encoding)
            except:
                pass
            
            if self._web_proxy:
                html = self._web_proxy.ResponseReceived(html)

            self.content = html
            
            if not self._auto_read_response:
                if self._cache_action == Cache_Insert or self._cache_action == Cache_Update:
                    if self._do_not_cache_if_any and len(self._do_not_cache_if_any) > 0:
                        for item in self._do_not_cache_if_any:
                            if item in self.content:
                                self._cache_action = Cache_None
                                break
                                
                if self._cache_action == Cache_Insert:                
                    self._net._insert_cache(self._url_for_cache, self._form_data_for_cache, self)
                elif self._cache_action == Cache_Update:
                    self._net._update_cache(self._url_for_cache, self._form_data_for_cache, self) 

        return self.content
            
