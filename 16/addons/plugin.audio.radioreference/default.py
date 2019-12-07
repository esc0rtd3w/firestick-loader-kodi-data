# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Broadcastify
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
#------------------------------------------------------------
import os
import sys
import urlparse
import plugintools

plugintools.module_log_enabled = (plugintools.get_setting("debug")=="true")
expertlist = (plugintools.get_setting("expertlist")=="true")
URL = "http://www.broadcastify.com/listen/"
IMAGES = os.path.join(plugintools.get_runtime_path(),"resources")

# Entry point
def run():
    plugintools.log("broadcastify.run")
    
    # Get params
    params = plugintools.get_params()
    
    if params.get("action") is None:
        main_list(params)
    else:
        action = params.get("action")
        exec action+"(params)"

    plugintools.close_item_list()

# Main menu
def main_list(params):
    plugintools.log("broadcastify.main_list "+repr(params))
    countries(params)

def countries(params):
    plugintools.log("broadcastify.countries "+repr(params))

    # Download home page
    body,response_headers = plugintools.read_body_and_headers(URL)
    body = plugintools.find_single_match(body,"Choose Country.</span[^<]+<select(.*?)</select")

    patron = '<option value="([^"]+)[^>]+>([^<]+)</option>'
    matches = plugintools.find_multiple_matches(body,patron)

    for code,title in matches:
        url="http://www.broadcastify.com/listen/coid/"+code
        plugintools.log("title=["+title+"], url=["+url+"]")

        # Flag images came from http://www.iconarchive.com/show/all-country-flag-icons-by-custom-icon-design.html
        thumbnail = os.path.join(IMAGES,"flags",code+".png")
        plugintools.add_item( action="states", title=title , thumbnail=thumbnail , url=url , folder=True )

    plugintools.set_view(plugintools.THUMBNAIL)

def states(params):
    plugintools.log("broadcastify.states "+repr(params))
    itemlist = []

    # Descarga la home
    body,response_headers = plugintools.read_body_and_headers(params.get("url"))
    
    # Search for states combo
    body2 = plugintools.find_single_match(body,'<form method="GET" action="/listen/"><select size="1" name="stid"(.*?)</selec')
    patron = '<option value="([^"]+)">([^<]+)</option>'
    matches = plugintools.find_multiple_matches(body2,patron)

    for code,title in matches:
        url="http://www.broadcastify.com/listen/stid/"+code
        plugintools.log("title=["+title+"], url=["+url+"]")
        plugintools.add_item( action="feeds", title=title , url=url , folder=True )

    # Search for states urls without repeating
    #<a href="/listen/stid/689">Flevoland</a>
    patron = '<a href="/listen/stid/(\d+)">([^<]+)</a>'
    matches = plugintools.find_multiple_matches(body,patron)

    encontrados = set()

    for code,title in matches:
        if code not in encontrados:    
            url="http://www.broadcastify.com/listen/stid/"+code
            plugintools.log("title=["+title+"], url=["+url+"]")
            plugintools.add_item( action="feeds", title=title , url=url , folder=True )
            encontrados.add(code)

def counties(params):
    plugintools.log("broadcastify.counties "+repr(params))

    # Descarga la home
    body,response_headers = plugintools.read_body_and_headers(params.get("url"))
    at_least_one = parse_counties(body,'<option value="ctid,([^"]+)">([^<]+)</option>',"http://www.broadcastify.com/listen/ctid/")
    if at_least_one:
        return

    at_least_one = parse_counties(body,'<option value="mid,([^"]+)">([^<]+)</option>',"http://www.broadcastify.com/listen/mid/")
    if at_least_one:
        return

    #<a href="/listen/ctid/4899">Central - Capricornia</a></td>
    at_least_one = parse_counties(body,'<a href="/listen/ctid/(\d+)">([^<]+)</a>',"http://www.broadcastify.com/listen/ctid/")
    if at_least_one:
        return

    parse_counties(body,'<a href="/listen/mid/(\d+)">([^<]+)</a>',"http://www.broadcastify.com/listen/mid/")

def parse_counties(body,patron,baseurl):
    
    matches = plugintools.find_multiple_matches(body,patron)
    at_least_one = False

    for code,title in matches:
        at_least_one = True
        url=baseurl+code
        plugintools.log("title=["+title+"], url=["+url+"]")
        plugintools.add_item( action="feeds", title=title , url=url , folder=True )

    return at_least_one

def feeds(params):
    plugintools.log("broadcastify.feeds "+repr(params))

    # Descarga la home
    body,response_headers = plugintools.read_body_and_headers(params.get("url"))
    plugintools.log("body="+body)
    
    # Feed table
    body = plugintools.find_single_match(body,'<h\d+>All Feeds in the State</h\d+[^<]+<table(.*?)</table>')
    
    # Row pattern
    patron  = '<tr[^<]+<td nowrap[^<]+<a href="[^"]+">([^<]+)</a[^<]+</td[^<]+'
    patron += '<td class="w1p"[^<]+.*?<a href="([^"]+)">([^<]+)(</a>.*?)</td[^<]+'
    patron += '<td class="c" nowrap>(.*?)</td[^<]+'
    patron += '<td class="c m">([^<]+)</\'td[^<]+'
    patron += '<td nowrap[^<]+<a href="[^"]+" class="button-info feed-info"></a[^<]+</td[^<]+'
    patron += '<td.+?(Of[^<]+|On[^<]+|Not[^<]+|Act[^<]+).*?</td>'
    matches = plugintools.find_multiple_matches(body,patron)

    at_least_one = False
    for county_name,feed_url,title,alert,feedtype,listeners,status in matches:
        at_least_one = True
        code = plugintools.find_single_match(feed_url,"/listen/feed/(\d+)")
        alert = plugintools.find_single_match(alert,"</a>.*?bold\">(.*?)</font>")
        status = status.strip().lower()
        feedtype = plugintools.find_single_match(feedtype,"([a-zA-Z\ ]+)")
        fulltitle = county_name + ": "+ title.strip() + " (" + feedtype.strip() + ")" + "(" + listeners.strip() + " listeners)" + "(" + status + ")" + alert

        if expertlist:
            fulltitle = "(" + listeners.strip() + ") " + county_name+": "+title.strip() + " (" + feedtype.strip() + ")"+ alert

        if status=="offline":
            fulltitle="[COLOR red]"+ fulltitle + "(" + status + ")" + "[/COLOR]"

        if status=="not active":
            fulltitle="[COLOR brown]"+ fulltitle + "(" + status + ")" + "[/COLOR]"

        if status=="active":
            fulltitle="[COLOR green]"+ fulltitle + "(" + status + ")" + "[/COLOR]"

        if alert:
            fulltitle = "[COLOR yellow]" + fulltitle + " [/COLOR]"

        url="http://www.broadcastify.com/scripts/playlists/ep.php?feedId="+code
        thumbnail = os.path.join(IMAGES,"images","radio-icon.png")
        plugintools.log("title=["+title+"], url=["+url+"]")
        plugintools.add_item( action="play", title=fulltitle , url=url, thumbnail=thumbnail, folder=False, isPlayable=True)

    if not at_least_one:
        thumbnail = os.path.join(IMAGES,"images","Actions-application-exit-icon.png")
        plugintools.add_item( action="play", title="No feeds available for this area" , url="", thumbnail=thumbnail, folder=False, isPlayable=True)

def play(params):
    plugintools.log("broadcastify.play "+repr(params))

    if params.get("url")!="":
        # Descarga la home
        body,response_headers = plugintools.read_body_and_headers(params.get("url"))
        plugintools.log("body="+body)
        location = plugintools.find_single_match(body,"<location>([^<]+)</location>")
        plugintools.play_resolved_url( location )

run()