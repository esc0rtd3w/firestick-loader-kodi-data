import os
import zipfile
import contextlib
import urllib2
import base64
import shutil
import io
from urlparse import urlparse, urlunparse
from xbmcswift2 import xbmc

from meta import plugin
from meta.gui import dialogs
from meta.play.players import EXTENSION

from language import get_string as _

data_dir = "special://profile/addon_data/{0}".format(plugin.id)
data_dir = xbmc.translatePath(data_dir)
 
def remove_auth(url):
    parsed = urlparse(url)
    parts = list(parsed)
    parts[1] = parsed.hostname
    return urlunparse(parts)
    
def update_players(path):
    if path.startswith("http://") or path.startswith("https://"):
        return update_players_remote(path)
    
    return update_players_local(path)
    
def update_players_local(zip_path):
    extract_to = os.path.join(data_dir, "players")    
    with contextlib.closing(zipfile.ZipFile(zip_path, "r")) as z:
        members = [x for x in z.namelist() if x.endswith(EXTENSION)]
        flat_extract(z, extract_to, members)
        
    return True

def update_players_remote(url):
    # Get username and password
    parsed = urlparse(url)
    username = parsed.username
    password = parsed.password
    if username is not None:
        if not password:
            password = plugin.keyboard(heading=_('Enter password'), hidden=True)
        if not password:
            return False        
        url = remove_auth(url)
        
    # Try without authentication            
    response = None
    try:
        response = urllib2.urlopen(url)
    except urllib2.HTTPError, e:
        if not username:
            return False
        url = e.geturl()
    
    # Retry with authentication
    if response is None:
        userandpass = base64.b64encode('%s:%s' % (username, password))
        auth = 'Basic %s' % userandpass.decode('ascii')
        request = urllib2.Request(url)
        request.add_header('Authorization', auth)

        try:
            response = urllib2.urlopen(request)
        except:
            return False
    
    extract_to = os.path.join(data_dir, "players")
    
    buffer = io.BytesIO(response.read())
    with contextlib.closing(zipfile.ZipFile(buffer)) as z:
        members = [x for x in z.namelist() if x.endswith(EXTENSION)]
        flat_extract(z, extract_to, members)
         
    return True

def empty_folder(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception, e:
            traceback.print_exc()

def flat_extract(z, extract_to, members=None):
    if members is None:
        members = z.namelist()

    if not os.path.exists(extract_to):
        os.makedirs(extract_to)
    else:
        if xbmc.getInfoLabel('Window(home).Property(running)') == 'totalmetalliq':
            empty_folder(extract_to)
        else:
            if dialogs.yesno(_("Update players"), _("Do you want to remove your existing players first?")):
                empty_folder(extract_to)
        
    for member in members:
        with contextlib.closing(z.open(member)) as source:
            target_path = os.path.join(extract_to, os.path.basename(member))
            with open(target_path, "wb") as target:
                shutil.copyfileobj(source, target)
