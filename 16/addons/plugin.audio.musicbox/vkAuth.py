#!/usr/bin/env python
# -*- coding: UTF-8 -*-

##############LIBRARIES TO IMPORT AND SETTINGS####################

import os,urllib,urllib2
import cookielib
from urlparse import urlparse
from HTMLParser import HTMLParser
import os, xbmc, xbmcgui

addon_id = 'plugin.audio.musicbox'
datapath = xbmc.translatePath('special://profile/addon_data/%s' % addon_id ).decode("utf-8")

VKCookie = os.path.join(datapath,'cookies.txt')

VK_useragent = "Mozilla/5.0 (Windows NT 6.1; rv:51.0) Gecko/20100101 Firefox/51.0"

###################################################################################
#Form Parser

class FormParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.url = None
        self.params = {}
        self.in_form = False
        self.form_parsed = False
        self.method = "GET"

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        if tag == "form":
            if self.form_parsed:
                raise RuntimeError("Second form on page")
            if self.in_form:
                raise RuntimeError("Already in form")
            self.in_form = True
        if not self.in_form:
            return
        attrs = dict((name.lower(), value) for name, value in attrs)
        if tag == "form":
            self.url = attrs["action"]
            if "method" in attrs:
                self.method = attrs["method"].upper()
        elif tag == "input" and "type" in attrs and "name" in attrs:
            if attrs["type"] in ["hidden", "text", "password"]:
                self.params[attrs["name"]] = attrs["value"] if "value" in attrs else ""

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag == "form":
            if not self.in_form:
                raise RuntimeError("Unexpected end of <form>")
            self.in_form = False
            self.form_parsed = True

###################################################################################
#Login to vk.com

def auth(email, password):

    # Authorization form
    def auth_user(email, password, opener):
        response = opener.open("https://m.vk.com")
        doc = response.read()
        parser = FormParser()
        parser.feed(doc)
        parser.close()
        if not parser.form_parsed or parser.url is None or "pass" not in parser.params or \
          "email" not in parser.params:
              raise RuntimeError("Something wrong")
        parser.params["email"] = email
        parser.params["pass"] = password
        if parser.method == "POST":
            response = opener.open(parser.url, urllib.urlencode(parser.params))
        else:
            raise NotImplementedError("Method '%s'" % parser.method)
        return response.read(), response.geturl()

    #2nd step of authentification
    def sms_code(doc, opener):
        parser = FormParser()
        parser.feed(doc)
        parser.close()
        auth_code = xbmcgui.Dialog().numeric(0,'Auth code:')
        auth_code = int(auth_code)
        parser.params["code"] = auth_code
        if parser.method == "POST":
            response = opener.open("https://m.vk.com" + parser.url, urllib.urlencode(parser.params))
        else:
            raise NotImplementedError("Method '%s'" % parser.method)
        return response.read(), response.geturl()

    cj = cookielib.LWPCookieJar()
    opener = urllib2.build_opener(
        urllib2.HTTPCookieProcessor(cj),
        urllib2.HTTPRedirectHandler())
    doc, url = auth_user(email, password, opener)
    #Check login success
    if "Login failed" in doc: return False
    #Check 2-Step Auth
    if "/login" in urlparse(url).path: 
        doc, url = sms_code(doc, opener)
    else: cj.save(VKCookie)
    return True

###################################################################################
#Check if the vk.com cookie is valid

def isCookieValid(cookie):
    cj = cookielib.LWPCookieJar()
    cj.load(cookie)
    #check vk.com audio page
    req = urllib2.Request('https://m.vk.com/audio')
    req.add_header('User-Agent', VK_useragent)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    response = opener.open(req)
    doc = response.read()
    url = response.geturl()
    if not "/audio" in urlparse(url).path: return False
    #aditional check for expired cookies
    post = {'_ajax':'1'}
    data = urllib.urlencode(post)
    req = urllib2.Request('https://m.vk.com/audio?act=search&q=eminem&offset=0',data)
    req.add_header('Content-Type', 'application/x-www-form-urlencoded')
    req.add_header('X-Requested-With', 'XMLHttpRequest')
    req.add_header('User-Agent', VK_useragent)
    response = opener.open(req)
    doc = response.read()
    if ".mp3" in doc: return True
    else: return False