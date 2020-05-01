'''
    Ice Channel
'''

from entertainment.plugnplay.interfaces import iStreamSettings
from entertainment.plugnplay.interfaces import ProxySupport
from entertainment.plugnplay import Plugin
from entertainment import common

class InternetConnection(iStreamSettings):
    implements = [iStreamSettings]
    
    priority = 120
        
    def Initialize(self):
        
        xml = '<settings>\n'
                
        xml += '<category label="Global Proxy">\n'
        xml += '<setting type="sep"/>\n'
        xml += '<setting id="global_proxy" type="bool" label="Global Proxy" default="false"/>\n'
        
        from entertainment.plugnplay.interfaces import WebProxy
        webproxy_count = len(WebProxy.implementors())
        if webproxy_count > 0:
            ct_enum = 'Proxy|DNS Proxy|Web Proxy'
        else:
            ct_enum = 'Proxy|DNS Proxy'        
        xml += '<setting id="gp_connection_type" type="enum" values="%s" label="     Connection Type" default="0" visible="eq(-1,true)"/>\n' % ct_enum
        xml += '<setting id="gp_ct_p_ip" type="ipaddress" label="     Proxy IP" default="" visible="eq(-2,true) + eq(-1,0)"/>\n'
        xml += '<setting id="gp_ct_p_port" type="number" label="     Port" default="" visible="eq(-3,true) + eq(-2,0)"/>\n'
        xml += '<setting id="gp_ct_p_username" type="text" label="     Username" default="" visible="eq(-4,true) + eq(-3,0)"/>\n'
        xml += '<setting id="gp_ct_p_password" type="text" label="     Password" default="" visible="eq(-5,true) + eq(-4,0)"/>\n'
        xml += '<setting id="gp_ct_dp_ip1" type="ipaddress" label="     Primary DNS" default="" visible="eq(-6,true) + eq(-5,1)"/>\n'
        xml += '<setting id="gp_ct_dp_ip2" type="ipaddress" label="     Secondary DNS" default="" visible="eq(-7,true) + eq(-6,1)"/>\n'
        xml += '<setting id="gp_ct_dp_ip3" type="ipaddress" label="     Tertiary DNS" default="" visible="eq(-8,true) + eq(-7,1)"/>\n'
        xml += '<setting id="gp_ct_p_socks5" type="bool" label="     Socks 5" default="false" visible="eq(-9,true) + eq(-8,0)"/>\n'
        
        if webproxy_count > 0:
            wp_enum = ''
            wp_enum_f = True
            for wp in WebProxy.implementors():
                if wp_enum_f == True:
                    wp_enum_f = False
                else:
                    wp_enum += '|'
                wp_enum += wp.name
            xml += '<setting id="gp_ct_wp" type="labelenum" values="%s" label="     Web Proxy Provider" default="0" visible="eq(-10,true) + eq(-9,2)"/>\n' % wp_enum
                
            
        
        xml += '<setting type="sep"/>\n'
        xml += '</category>\n' 
        
        proxy_selection = "Global Proxy"
        
        xml += '<category label="More Proxies">\n'
        xml += '<setting type="sep"/>\n'
        for x in range(0, 8):
            i = str(x+1)
            proxy_selection += '|' + 'Proxy %s' % i
            xml += '<setting id="lp_%s" type="bool" label="Proxy %s" default="false"/>\n' % (i, i)
            xml += '<setting id="lp_%s_connection_type" type="enum" values="%s" label="     Connection Type" default="0" visible="eq(-1,true)"/>\n' % (i, ct_enum)
            xml += '<setting id="lp_%s_ct_p_ip" type="ipaddress" label="     Proxy IP" default="" visible="eq(-2,true) + eq(-1,0)"/>\n' % i
            xml += '<setting id="lp_%s_ct_p_port" type="number" label="     Port" default="" visible="eq(-3,true) + eq(-2,0)"/>\n' % i
            xml += '<setting id="lp_%s_ct_p_username" type="text" label="     Username" default="" visible="eq(-4,true) + eq(-3,0)"/>\n' % i
            xml += '<setting id="lp_%s_ct_p_password" type="text" label="     Password" default="" visible="eq(-5,true) + eq(-4,0)"/>\n' % i
            xml += '<setting id="lp_%s_ct_dp_ip1" type="ipaddress" label="     Primary DNS" default="" visible="eq(-6,true) + eq(-5,1)"/>\n' % i
            xml += '<setting id="lp_%s_ct_dp_ip2" type="ipaddress" label="     Secondary DNS" default="" visible="eq(-7,true) + eq(-6,1)"/>\n' % i
            xml += '<setting id="lp_%s_ct_dp_ip3" type="ipaddress" label="     Tertiary DNS" default="" visible="eq(-8,true) + eq(-7,1)"/>\n' % i
            xml += '<setting id="lp_%s_ct_p_socks5" type="bool" label="     Socks 5" default="false" visible="eq(-9,true) + eq(-8,0)"/>\n' % i
            if webproxy_count > 0:
                xml += '<setting id="lp_%s_ct_wp" type="labelenum" values="%s" label="     Web Proxy Provider" default="0" visible="eq(-10,true) + eq(-9,2)"/>\n' % (i, wp_enum)
            xml += '<setting type="sep"/>\n'        
        xml += '</category>\n' 
                
        xml += '<category label="Proxy Assignments">\n'
        xml += '<setting type="sep"/>\n'
        i=0
        for item in ProxySupport.implementors():
            i += 1
            xml += '<setting id="%s" type="enum" label="%s" values="%s" default="0"/>\n' % (item.name, item.display_name, proxy_selection)        
            #xml += '<setting id="domain_%s" type="text" label="Domain %s" default="%s" visible="false"/>\n' % (str(i), str(i), ','+','.join(item.domains)+',__psid__'+item.name)
        #xml += '<setting id="domain_count" type="number" label="Domain Counte" default="%s" visible="false"/>\n' % i
        xml += '<setting type="sep"/>\n'
        xml += '</category>\n' 
        xml += '</settings>\n'
        
        self.CreateSettings('Internet Connection', common.settings_Internet_Connection, xml)
