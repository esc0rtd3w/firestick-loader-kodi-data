'''
    Ice Channel
    based on plugnplay by https://github.com/daltonmatos    
'''

'''
  The main plugin Manager class.
  Stores all implementors of all public interfaces
'''

class Manager(object):

  def __init__(self):
    self.iface_implementors = {}


  def add_implementor(self, interface, implementor_instance):
    self.iface_implementors.setdefault(interface, [])
    for index, item in enumerate(self.iface_implementors[interface]):
        if implementor_instance.priority <= item.priority:
            self.iface_implementors[interface].insert(index, 
                                                      implementor_instance)
            return
    self.iface_implementors[interface].append(implementor_instance)

  def implementors(self, interface):
    return self.iface_implementors.get(interface, [])
