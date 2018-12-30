import os
import xbmc
from strings import ADDON


def reset_playing():
    path = xbmc.translatePath(ADDON.getAddonInfo('profile'))
    if not os.path.exists(path):
        os.mkdir(path)
    proc_file = os.path.join(path, 'proc')
    f = open(proc_file, 'w')
    f.write('')
    f.close()
