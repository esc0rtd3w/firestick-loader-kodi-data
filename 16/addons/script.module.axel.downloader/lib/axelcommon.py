"""
    axel downloader XBMC Addon
    Copyright (C) 2013 Eldorado

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
"""
#todo remove them from here
import os   
import sys 

addon = None#Addon('script.module.axel.downloader')
profile_path =None# addon.get_profile()

def we_are_frozen():
    # All of the modules are built-in to the interpreter, e.g., by py2exe
    return hasattr(sys, "frozen")

def module_path():
    encoding = sys.getfilesystemencoding()
    if we_are_frozen():
        return os.path.dirname(unicode(sys.executable, encoding))
    return os.path.dirname(unicode(__file__, encoding))

try:
    addon_id = 'script.module.axel.downloader'
    from addon.common.addon import Addon
    addon = Addon('script.module.axel.downloader')
    addon_path = addon.get_path()
    profile_path = addon.get_profile()
    addon_version = addon.get_version()
except:
    profile_path=module_path()

def log(msg,n=0):
    if addon:
        addon.log(msg,n)
        #xbmc.log('%s: %s' % (addon_id, msg), n)
    else:
        print msg
    

#Create queue objects
class _Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(_Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Singleton(_Singleton('SingletonMeta', (object,), {})): pass
