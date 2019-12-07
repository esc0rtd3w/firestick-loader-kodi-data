'''
    Ice Channel
    based on plugnplay by https://github.com/daltonmatos
'''

#from glob import glob
import os
from os.path import join, basename
import sys
from entertainment import common
from manager import *

__version__ = "0.1"

__all__ = ['Interface', 'Plugin']


man = Manager()

plugin_dirs = []

'''
  Marker for public interfaces
'''
class Interface(object):

  filecode='_ifc'    
  
  @classmethod
  def implementors(klass):
    return man.implementors(klass)


class PluginMeta(type):
  
  def __new__(metaclass, classname, bases, attrs):
    new_class = super(PluginMeta, metaclass).__new__(metaclass, classname,
        bases, attrs)
    
    new_class_instance = new_class()
    if attrs.has_key('implements'):
      for interface in attrs['implements']:
        man.add_implementor(interface, new_class_instance)
        common.addon.log_debug('registering plugin: %s (%s), as: %s (P=%d)' % \
                       (new_class.name, new_class.__name__, interface.__name__, 
                        new_class_instance.priority))

    return new_class

class Plugin(object):
  __metaclass__ = PluginMeta


def set_plugin_dirs(*dirs):
  for d in dirs:
    common.addon.log_debug('adding plugin dir: %s' % d)
    plugin_dirs.append(d)
    
def load_plugins_new(dirs, plugins):
    sys.path.extend(dirs)
    for plugin in plugins:
        try:
            imported_module = __import__(plugin, globals(), locals())
            sys.modules[plugin] = imported_module
        except:
            pass
  
def load_plugins(plugin_type):
  for d in plugin_dirs:
    
    sys.path.append(d)
    
    py_files = []
    for dirpath, dirnames, files in os.walk(d):
        sys.path.append(dirpath)
        for f in files:             
            if not sys.modules.get(f[:-3], None):
                if isinstance( plugin_type, (str, unicode) ) and plugin_type in f and f.endswith('.py'):
                    py_files.append(os.path.join(dirpath, f))
                elif isinstance( plugin_type, list ) and f.endswith('.py'):
                    for pt in plugin_type:
                        if pt in f: 
                            py_files.append(os.path.join(dirpath, f))
                            break
    #py_files = glob(join(d, '*.py'))
    #Remove ".py" for proper importing
    modules = [basename(f[:-3]) for f in py_files]
    for mod_name in modules:
      imported_module = __import__(mod_name, globals(), locals())
      sys.modules[mod_name] = imported_module
    