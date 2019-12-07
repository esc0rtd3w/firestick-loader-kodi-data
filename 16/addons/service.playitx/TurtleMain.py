'''
Created on Dec 27, 2011

@author: ajju
'''
try:
    import TurtleService
except:
    import xbmcgui  # @UnresolvedImport
    dialog = xbmcgui.Dialog()
    dialog.ok('[B][COLOR red]ALERT: [/COLOR][/B] RESTART XBMC', 'A new update has recently installed or add-on reconfigured.', 'Please restart XBMC to reflect the changes.', 'You will not be able to access until restart.')


TurtleService.start('service.playitx', 'PlayIt', '/PlayIt', 8181, [8100, 8199])
