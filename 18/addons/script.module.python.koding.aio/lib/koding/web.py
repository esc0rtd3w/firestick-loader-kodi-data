# -*- coding: utf-8 -*-

# script.module.python.koding.aio
# Python Koding AIO (c) by TOTALREVOLUTION LTD (support@trmc.freshdesk.com)

# Python Koding AIO is licensed under a
# Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License.

# You should have received a copy of the license along with this
# work. If not, see http://creativecommons.org/licenses/by-nc-nd/4.0.

# Please make sure you've read and understood the license, this code can NOT be used commercially
# and it can NOT be modified and redistributed. If you're found to be in breach of this license
# then any affected add-ons will be blacklisted and will not be able to work on the same system
# as any other add-ons which use this code. Thank you for your cooperation.

import os
import time
import urllib
import xbmc
import xbmcgui
import xbmcvfs
from systemtools import Python_Version
#----------------------------------------------------------------    
# TUTORIAL #
def Cleanup_URL(url):
    """
Clean a url, removes whitespaces and common buggy formatting when pulling from websites

CODE: Cleanup_URL(url)

AVAILABLE PARAMS:
        
    (*) url   -  This is the main url you want cleaned up.

EXAMPLE CODE:
raw_url = '" http://test.com/video/"/'
clean_url = koding.Cleanup_URL(raw_url)
dialog.ok('CLEANUP URL', 'Orig: %s'%raw_url,'Clean: %s'%clean_url)
~"""
    from HTMLParser import HTMLParser

    bad_chars = ['/','\\',':',';','"',"'"]
    url = url.strip()

    while url[0] in bad_chars or url[-1] in bad_chars:
        if url[-1] in bad_chars:
            url = url[:-1]
        if url[0] in bad_chars:
            url = url[1:]
        url = url.strip()
    return HTMLParser().unescape(url)
#----------------------------------------------------------------    
# TUTORIAL #
def Delete_Cookies(filename='cookiejar'):
    """
This will delete your cookies file.

CODE: Delete_Cookies([filename])

AVAILABLE PARAMS:

    filename - By default this is set to the filename 'cookiejar'.
    This is the default cookie filename which is created by the Open_URL
    function but you can use any name you want and this function will
    return True or False on whether or not it's successfully been removed.

EXAMPLE CODE:
Open_URL(url='http://google.com',cookiejar='google')
dialog.ok('GOOGLE COOKIES CREATED','We have just opened a page to google.com, if you check your addon_data folder for your add-on you should see a cookies folder and in there should be a cookie called "google". When you press OK this will be removed.')
koding.Delete_Cookies(filename='google')
~"""
    from addons     import Addon_Info
    Addon_Version = Addon_Info(id='version')
    Addon_Profile = Addon_Info(id='profile')
    Cookie_File   = os.path.join(Addon_Profile,'cookies',filename)
    if xbmcvfs.delete(Cookie_File):
        return True
    else:
        return False
#----------------------------------------------------------------    
# TUTORIAL #
def Download(url, dest, dp=None, timeout=5):
    """
This will download a file, currently this has to be a standard download link which doesn't require cookies/login.

CODE: Download(src,dst,[dp])
dp is optional, by default it is set to false

AVAILABLE PARAMS:

    (*) src  - This is the source file, the URL to your download. If you attempted to download an item but it's not behaving the way you think it should (e.g. a zip file not unzipping) then change the extension of the downloaded file to .txt and open up in a text editor. You'll most likely find it's just a piece of text that was returned from the URL you gave and it should have details explaining why it failed. Could be that's the wrong URL, it requires some kind of login, it only accepts certain user-agents etc.

    (*) dst  - This is the destination file, make sure it's a physical path and not "special://...". Also remember you need to add the actual filename to the end of the path, so if we were downloading something to the "downloads" folder and we wanted the file to be called "test.txt" we would use this path: dst = "downloads/test.txt". Of course the downloads folder would actually need to exist otherwise it would fail and based on this poor example the downloads folder would be at root level of your device as we've not specified a path prior to that so it just uses the first level that's accessible.

    dp - This is optional, if you pass through the dp function as a DialogProgress() then you'll get to see the progress of the download. If you choose not to add this paramater then you'll just get a busy spinning circle icon until it's completed. See the example below for a dp example.

    timeout - By default this is set to 5. This is the max. amount of time you want to allow for checking whether or
    not the url is a valid link and can be accessed via the system.

EXAMPLE CODE:
src = 'http://noobsandnerds.com/portal/Bits%20and%20bobs/Documents/user%20guide%20of%20the%20gyro%20remote.pdf'
dst = 'special://home/remote.pdf'
dp = xbmcgui.DialogProgress()
dp.create('Downloading File','Please Wait')
koding.Download(src,dst,dp)
dialog.ok('DOWNLOAD COMPLETE','Your download is complete, please check your home Kodi folder. There should be a new file called remote.pdf.')
dialog.ok('DELETE FILE','Click OK to delete the downloaded file.')
xbmcvfs.delete(dst)
~"""
    from filetools import Physical_Path
    dest = Physical_Path(dest)
    status = Validate_Link(url,timeout)
    if status >= 200 and status < 400:
        if Python_Version() < 2.7 and url.startswith('https'):
            url = url.replace('https','http')
        start_time=time.time()
        urllib.urlretrieve(url, dest, lambda nb, bs, fs: Download_Progress(nb, bs, fs, dp, start_time))
        return True
    else:
        return False
#----------------------------------------------------------------    
def Download_Progress(numblocks, blocksize, filesize, dp, start_time):
    """ internal command ~"""

    try: 
        percent = min(numblocks * blocksize * 100 / filesize, 100) 
        currently_downloaded = float(numblocks) * blocksize / (1024 * 1024) 
        kbps_speed = numblocks * blocksize / (time.time() - start_time) 
        if kbps_speed > 0: 
            eta = (filesize - numblocks * blocksize) / kbps_speed 
        else: 
            eta = 0 
        kbps_speed = kbps_speed / 1024 
        total = float(filesize) / (1024 * 1024) 
        mbs = '%.02f MB of %.02f MB' % (currently_downloaded, total) 
        e = 'Speed: %.02f Kb/s ' % kbps_speed 
        e += 'ETA: %02d:%02d' % divmod(eta, 60) 
        if dp:
            dp.update(percent, mbs, e)
        if dp.iscanceled(): 
            dp.close()
    except: 
        percent = 100
        if dp:
            dp.update(percent) 
    if dp:
        if dp.iscanceled(): 
            dp.close()
        dp.close()
#----------------------------------------------------------------    
# TUTORIAL #
def Get_Extension(url):
    """
Return the extension of a url

CODE:   Get_Extension(url)

AVAILABLE PARAMS:

    (*) url  -  This is the url you want to grab the extension from

EXAMPLE CODE:
dialog.ok('ONLINE FILE','We will now try and get the extension of the file found at this URL:','','[COLOR=dodgerblue]http://www.sample-videos.com/video/mp4/720/big_buck_bunny_720p_1mb.mp4[/COLOR]')
url_extension = koding.Get_Extension('http://www.sample-videos.com/video/mp4/720/big_buck_bunny_720p_1mb.mp4')
dialog.ok('FILE EXTENSION','The file extension of this Big Buck Bunny sample is:','','[COLOR=dodgerblue]%s[/COLOR]'%url_extension)
~"""
    
    import os
    import urlparse

    parsed = urlparse.urlparse(url)
    root, ext = os.path.splitext(parsed.path)
    return ext
#----------------------------------------------------------------
# TUTORIAL #
def Open_URL(url='',post_type='get',payload={},headers={'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'},cookies=True,auth=None,timeout=None,cookiejar=None,proxies={}):
    """
If you need to pull the contents of a webpage it's very simple to do so by using this function.
This uses the Python Requests module, for more detailed info on how the params work
please look at the following link: http://docs.python-requests.org/en/master/user/advanced/

IMPORTANT: This function will attempt to convert a url with a query string into the
correct params for a post or get command but I highly recommend sending through your
query string as a dictionary using the payload params. It's much cleaner and is a
safer way of doing things, if you send through your url with a query string attached
then I take no responsibility if it doesn't work!

CODE:   Open_URL(url,[post_type,payload,headers,cookies,auth,timeout,cookiejar])

AVAILABLE PARAMS:

    url  -  This is the main url you want to send through. Send it through
    as a query string format even if it's a post.

    post_type  -  By default this is set to 'get' but this can be set to 'post',
    if set to post the query string will be split up into a post format automatically.
    
    payload - By default this is not used but if you just want a standard
    basic Open_URL function you can add a dictionary of params here. If you
    don't enter anything in here the function will just split up your url
    accordingly. Make sure you read the important information at the top
    of this tutorial text.

    headers -  Optionally send through headers in form of a dictionary.

    cookies  -  If set to true your request will send through and store cookies.

    auth  -  User/pass details

    timeout  -  Optionally set a timeout for the request.

    cookiejar  -  An name for the location to store cookies. By default it's
    set to addon_data/<addon_id>/cookies/cookiejar but if you have multiple
    websites you access then you may want to use a separate filename for each site.

    proxies - Use a proxy for accessing the link, see requests documentation for full
    information but essentially you would send through a dictionary like this:
    proxies = {"http":"http://10.10.1.10:3128","htts":"https://10.10.1.10:3128"}

EXAMPLE CODE:
dialog.ok('OPEN FORUM PAGE','We will attempt to open the noobsandnerds forum page and return the contents. You will now be asked for your forum credentials.')
myurl = 'http://noobsandnerds.com/support/index.php'
username = koding.Keyboard('ENTER USERNAME')
password = koding.Keyboard('ENTER PASSWORD')
params = {"username":username,"password":password}
xbmc.log(repr(params),2)
url_contents = koding.Open_URL(url=myurl, payload=params, post_type='get')
koding.Text_Box('CONTENTS OF WEB PAGE',url_contents)
~"""
    import os
    import pickle
    import requests
    import sys
    import xbmc
    import xbmcaddon

    from __init__   import converthex, dolog, ADDON_ID, KODI_VER
    from addons     import Addon_Info
    from filetools  import Text_File

    Addon_Version = Addon_Info(id='version')
    Addon_Profile = Addon_Info(id='profile')
    Cookie_Folder = os.path.join(Addon_Profile,'cookies')
    xbmc.log(Cookie_Folder,2)
    if not xbmcvfs.exists(Cookie_Folder):
        xbmcvfs.mkdirs(Cookie_Folder)

    if cookiejar == None:
        Cookie_Jar = os.path.join(Cookie_Folder,'cookiejar')
    else:
        Cookie_Jar = os.path.join(Cookie_Folder,cookiejar)
    
    my_cookies = None
    if cookies:
        if xbmcvfs.exists(Cookie_Jar):
            try:
                openfile = xbmcvfs.File(Cookie_Jar)
                f = openfile.read()
                openfile.close()
                my_cookies = pickle.load(f)
            except:
                my_cookies = None

# If the payload is empty we split the params
    if len(payload) == 0:

        if '?' in url:
            url, args = url.split('?')
            args = args.split('&')
            for item in args:
                var, data = item.split('=')
                payload[var] = data

    dolog('PAYLOAD: %s'%payload)

    try:
        if Python_Version() < 2.7 and url.startswith('https'):
            url = url.replace('https','http')

        if post_type == 'post':
            r = requests.post(url, payload, headers=headers, cookies=my_cookies, auth=auth, timeout=timeout, proxies=proxies)
        else:
            r = requests.get(url, payload, headers=headers, cookies=my_cookies, auth=auth, timeout=timeout, proxies=proxies)
    except:
        dolog('Failed to pull content for %s'%url)
        return False
    dolog('### CODE: %s   |   REASON: %s' % (r.status_code, r.reason))
    if r.status_code >= 200 and r.status_code < 400:
        content = r.text.encode('utf-8')
        dolog('content: %s'%content)
        if cookies:
            openfile = xbmcvfs.File(Cookie_Jar,'wb')
            pickle.dump(r.cookies, openfile)
            openfile.close()
        return content
    else:
        dolog('Failed to pull content for %s'%url)
        return False
#----------------------------------------------------------------
# TUTORIAL #
def Validate_Link(url='',timeout=30):
    """
Returns the code for a particular link, so for example 200 is a good link and 404 is a URL not found

CODE:   Validate_Link(url,[timeout])

AVAILABLE PARAMS:

    (*) url  -  This is url you want to check the header code for

    timeout  -  An optional timeout integer for checking url (default is 30 seconds)

EXAMPLE CODE:
url_code = koding.Validate_Link('http://totalrevolution.tv')
if url_code == 200:
    dialog.ok('WEBSITE STATUS','The website [COLOR=dodgerblue]totalrevolution.tv[/COLOR] is [COLOR=lime]ONLINE[/COLOR]')
else:
    dialog.ok('WEBSITE STATUS','The website [COLOR=dodgerblue]totalrevolution.tv[/COLOR] is [COLOR=red]OFFLINE[/COLOR]')
~"""
    import requests
    import xbmc

    if Python_Version() < 2.7 and url.startswith('https'):
        url = url.replace('https','http')

    try:
        r = requests.get(url,timeout=timeout)
        return r.status_code
    except:
        return 400
#----------------------------------------------------------------