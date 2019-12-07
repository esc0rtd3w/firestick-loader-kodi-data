
#       Copyright (C) 2013-
#       Sean Poyser (seanpoyser@gmail.com)
#
#  This Program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2, or (at your option)
#  any later version.
#
#  This Progr`am is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with XBMC; see the file COPYING.  If not, write to
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
#  http://www.gnu.org/copyleft/gpl.html
#
# Script inspired and heavily based on original script.favourites from Ronie and Black at XBMC.org
#
# See Readme for more information on how to use this script



import xbmc
import xbmcgui
import os
import urllib

import utils
import parameters
import favourite
import sfile

ADDON       = utils.ADDON
HOME        = utils.HOME
PROFILE     = utils.PROFILE
FILENAME    = utils.FILENAME
FOLDERCFG   = utils.FOLDERCFG
ADDONID     = utils.ADDONID
ICON        = utils.ICON
DISPLAYNAME = utils.DISPLAYNAME

INHERIT          = utils.INHERIT
ALPHA_SORT       = utils.ALPHA_SORT
LABEL_NUMERIC    = utils.LABEL_NUMERIC
LABEL_NUMERIC_QL = utils.LABEL_NUMERIC_QL
SHOWXBMC         = utils.SHOWXBMC

GETTEXT   = ADDON.getLocalizedString


def getFolderThumb(path):
    cfg   = os.path.join(path, FOLDERCFG)
    thumb = parameters.getParam('ICON', cfg)

    if thumb:
        return thumb

    if not INHERIT:
        return ICON

    faves = favourite.getFavourites(os.path.join(path, FILENAME), 1, chooser=True)   

    if len(faves) < 1:
        return ICON

    thumb = faves[0][1]

    if len(thumb) > 0:
        return thumb

    return ICON


def GetFave(property, path='', changeTitle=False, includePlay=True):
    xbmc.executebuiltin('Skin.Reset(%s)' % '%s.%s' % (property, 'Path'))
    xbmc.executebuiltin('Skin.Reset(%s)' % '%s.%s' % (property, 'Label'))
    xbmc.executebuiltin('Skin.Reset(%s)' % '%s.%s' % (property, 'Icon'))
    xbmc.executebuiltin('Skin.Reset(%s)' % '%s.%s' % (property, 'IsFolder'))

    Main(property, path, changeTitle, includePlay)

    while xbmcgui.Window(10000).getProperty('Super_Favourites_Chooser') == 'true':
        xbmc.sleep(100)

    xbmc.sleep(500)

    return len(xbmc.getInfoLabel('Skin.String(%s.Path)' % property)) > 0


class Main:
    def __init__(self, property=None, path='', changeTitle=False, includePlay=False):
        xbmcgui.Window(10000).setProperty('Super_Favourites_Chooser', 'true')
        if property:
            self.init(property, path, changeTitle, includePlay)
        else:
            self._parse_argv()

        faves = self.getFaves()
        MyDialog(faves, self.PROPERTY, self.CHANGETITLE, self.PATH, self.MODE, self.INCLUDEPLAY)
        
    
    def _parse_argv(self):
        try:           
            params = dict(arg.split('=') for arg in sys.argv[1].split('&'))          
        except:
            params = {}
                    
        path        = params.get('path',     '')               
        property    = params.get('property', '')
        changeTitle = params.get('changetitle',   '').lower() == 'true'
        includePlay = params.get('includePlay',   '').lower() == 'true'

        path = path.replace('SF_AMP_SF', '&')

        self.init(property, path, changeTitle, includePlay)


    def init(self, property, path, changeTitle, includePlay): 
        self.PATH        = path
        self.PROPERTY    = property
        self.CHANGETITLE = changeTitle
        self.INCLUDEPLAY = includePlay

        self.MODE = 'folder' if len(self.PATH) > 0 else 'root'

        if self.PATH == 'special://profile/':
            self.MODE = 'xbmc'
            self.FULLPATH = self.PATH
        else:                
            self.FULLPATH = os.path.join(utils.PROFILE, self.PATH)

        self.FULLPATH = urllib.unquote_plus(self.FULLPATH)

                
    def getFaves(self):
        file  = os.path.join(self.FULLPATH, FILENAME).decode('utf-8')        
        faves = []        

        index = 0

        label_numeric = LABEL_NUMERIC 
        if self.MODE == 'folder':    
            folderCfg = os.path.join(self.FULLPATH, FOLDERCFG)
            numeric = parameters.getParam('NUMERICAL', folderCfg)
            if numeric:
                label_numeric = numeric.lower() == 'true'

        if label_numeric:
            label_numeric = LABEL_NUMERIC_QL

        if self.MODE != 'xbmc':        
            try:    
                current, dirs, files = sfile.walk(self.FULLPATH)

                dirs = sorted(dirs, key=str.lower)

                for dir in dirs:
                    path = os.path.join(self.FULLPATH, dir)
                                   
                    folderCfg = os.path.join(path, FOLDERCFG)
                    folderCfg = parameters.getParams(folderCfg)
                    lock      = parameters.getParam('LOCK',   folderCfg)
                    if lock:
                        continue
                    colour    = parameters.getParam('COLOUR', folderCfg)
                    thumb     = getFolderThumb(path)               

                    label = dir
                
                    if colour and colour.lower() <> 'none':
                        label = '[COLOR %s]%s[/COLOR]' % (colour, label)
              
                    label, index = utils.addPrefixToLabel(index, label, label_numeric)
                
                    fave = [label, thumb, os.path.join(self.PATH, dir),  True]
                    faves.append(fave)
                
            except Exception, e:
                pass
            
        items = favourite.getFavourites(file, chooser=True)

        sortorder = 0

        if self.MODE == 'folder':    
            folderCfg = os.path.join(self.FULLPATH, FOLDERCFG)

            try:    sortorder = int(parameters.getParam('SORT', folderCfg))
            except: sortorder = 0

        if sortorder == 0:
            sortorder = 1 if ALPHA_SORT else 2
     
        if sortorder == 1: #ALPHA_SORT:
            items = sorted(items, key=lambda x: utils.CleanForSort(x))

        if not label_numeric:
            faves.extend(items)
        else:
            for fave in items:
                label  = fave[0]
                thumb  = fave[1]
                cmd    = fave[2]

                label, index = utils.addPrefixToLabel(index, label, label_numeric)

                faves.append([label, thumb, cmd])

        return faves
            
            
class MainGui(xbmcgui.WindowXMLDialog):
    def __init__(self, *args, **kwargs):
        xbmcgui.WindowXMLDialog.__init__( self )
        self.faves       = kwargs.get('faves')
        self.property    = kwargs.get('property')
        self.changeTitle = kwargs.get('changeTitle')
        self.path        = kwargs.get('path')
        self.mode        = kwargs.get('mode')
        self.includePlay = kwargs.get('includePlay')
        
        
    def onInit(self):
        try:
            self.favList = self.getControl(6)
            self.getControl(3).setVisible(False)
        except:
            self.favList = self.getControl(3)

        self.getControl(5).setVisible(False)
        #self.getControl(1).setVisible(False) #necessary due to a bug in Kodi
        #self.getControl(1).setLabel(GETTEXT(30000))
        self.getControl(1).setLabel(self.path)

        try:    self.getControl(7).setLabel(xbmc.getLocalizedString(222))
        except: pass

        self.getControl(5).setVisible(False) 

        #the remove item 
        #self.favList.addItem(xbmcgui.ListItem(GETTEXT(30100), iconImage='DefaultAddonNone.png'))

        if self.mode != 'xbmc':
            self.addFolderItem()

        if self.mode == 'root':
            self.addXBMCFavouritesItem()

        for fave in self.faves:            
            listitem = xbmcgui.ListItem(fave[0])

            icon = fave[1]
            if not icon:
                icon = ICON 
            
            listitem.setIconImage(icon)
            listitem.setProperty('Icon', fave[1])

            cmd = fave[2]
            if cmd.lower().startswith('activatewindow'):
                cmd = cmd.replace('")', '",return)')

            fanart = favourite.getFanart(cmd) 
            desc   = favourite.getOption(cmd, 'desc')
            mode   = favourite.getOption(cmd, 'mode')

            cmd = favourite.removeSFOptions(cmd)

            listitem.setProperty('Path',   cmd)
            listitem.setProperty('Fanart', fanart)
            listitem.setProperty('Desc',   desc)
            listitem.setProperty('Mode',   mode)
            
            if len(fave) > 3 and fave[3]:
                listitem.setProperty('IsFolder', 'true')
            
            self.favList.addItem(listitem)
            
        # add a dummy item with no action assigned
        #listitem = xbmcgui.ListItem(GETTEXT(30101))
        #listitem.setProperty('Path', 'noop')
        #self.favList.addItem(listitem)
        self.setFocus(self.favList)


    def addXBMCFavouritesItem(self):
        if not SHOWXBMC:
            return

        try:
            fullpath = 'special://profile/'

            thumb = parameters.getParam('ICON', os.path.join(PROFILE, FOLDERCFG))
            if not thumb:
                thumb = os.path.join(HOME, 'resources', 'media', 'icon_favourites.png')

            label    = GETTEXT(30106) % DISPLAYNAME
            listitem = xbmcgui.ListItem(label) 

            listitem.setIconImage(thumb)
            listitem.setProperty('Icon',     thumb)
            listitem.setProperty('Path',     fullpath)
            listitem.setProperty('IsFolder', 'true')

            self.favList.addItem(listitem)


        except Exception, e:
            pass


    def addFolderItem(self):
        path = ''

        if len(self.path) == 0:
            path = GETTEXT(30000)
        else:
            path = self.path.replace(os.sep, '/').rsplit('/', 1)[-1]

        try:
            fullpath = os.path.join(utils.PROFILE, self.path)
            thumb    = getFolderThumb(fullpath) if self.mode != 'root' else ICON

            #open folder
            listitem = xbmcgui.ListItem(path + GETTEXT(30102))                     
            listitem.setIconImage(thumb)
            listitem.setProperty('Icon',     thumb)
            listitem.setProperty('Path',     self.path)
            listitem.setProperty('IsFolder', 'open')
            self.favList.addItem(listitem)

            #play folder
            if self.includePlay:
                listitem = xbmcgui.ListItem(path + GETTEXT(30236))                     
                listitem.setIconImage(thumb)
                listitem.setProperty('Icon',     thumb)
                listitem.setProperty('Path',     self.path)
                listitem.setProperty('IsFolder', 'play')
                self.favList.addItem(listitem)

        except Exception, e:
            pass


    def closeDialog(self):
        xbmcgui.Window(10000).setProperty('Super_Favourites_Chooser', 'false')               
        self.close()

        
    def onAction(self, action):
        actionID = action.getId()

        if actionID in [10]: #'x' button
            return self.closeDialog()

        if actionID in [9, 92, 216, 247, 257, 275, 61467, 61448]:
            if len(self.path) == 0: 
                return self.closeDialog()

            if self.mode == 'xbmc':
                self.changeFolder('')
                return

            path = '/' + self.path.replace(os.sep, '/')
            path = path.rsplit('/', 1)[0]
            path = path[1:]
            self.changeFolder(path)

            
    def onClick(self, controlID):
        if controlID in [7, 99]: #cancel buttons Krypton(7) / Pre-Krypton(99)
            return self.closeDialog()
            
        if controlID == 6 or controlID == 3:
            num = self.favList.getSelectedPosition()

            if num >= 0:
                favPath  = self.favList.getSelectedItem().getProperty('Path')
                favLabel = self.favList.getSelectedItem().getLabel()
                favIcon  = self.favList.getSelectedItem().getProperty('Icon')
                isFolder = self.favList.getSelectedItem().getProperty('IsFolder')

                if not isFolder:
                    fanart = self.favList.getSelectedItem().getProperty('Fanart')
                    desc   = self.favList.getSelectedItem().getProperty('Desc')
                    mode   = self.favList.getSelectedItem().getProperty('Mode')

                    favPath = favourite.updateSFOption(favPath, 'fanart', fanart)
                    favPath = favourite.updateSFOption(favPath, 'desc',   desc)
                    favPath = favourite.updateSFOption(favPath, 'mode',   mode)

                favLabel = utils.fix(favLabel)
                if favLabel.endswith(GETTEXT(30102)):
                    favLabel = favLabel.replace(GETTEXT(30102), '')
                if favLabel.endswith(GETTEXT(30236)):
                    favLabel = favLabel.replace(GETTEXT(30236), '')

                if isFolder:
                    if isFolder.lower() == 'true':
                        self.changeFolder(favPath)
                        return
                    if isFolder.lower() == 'open':
                        cmd  = 'ActivateWindow(10025,"plugin://'
                        cmd += utils.ADDONID + '/?'
                        cmd += 'label=%s&' % urllib.quote_plus(favLabel)
                        cmd += 'folder=%s' % urllib.quote_plus(favPath)
                        cmd += '",return)'
                        favPath = cmd
                    if isFolder.lower() == 'play':
                        cmd  = 'PlayMedia("plugin://'
                        cmd += utils.ADDONID + '/?'
                        cmd += 'label=%s&' % urllib.quote_plus(favLabel)
                        cmd += 'mode=%s&'  % urllib.quote_plus('5400')
                        cmd += 'folder=%s' % urllib.quote_plus(favPath)
                        cmd += '")'
                        favPath = cmd                        
                
                if self.changeTitle:
                    keyboard = xbmc.Keyboard(favLabel, xbmc.getLocalizedString(528), False)
                    keyboard.doModal()
                    if (keyboard.isConfirmed()):
                        favLabel = keyboard.getText()

                if favPath.lower().startswith('activatewindow') and '?' in favPath:
                    text    = '?content_type=%s&' % urllib.quote_plus('Chooser')
                    favPath = favPath.replace('?', text)
                        
                xbmc.executebuiltin('Skin.SetString(%s,%s)' % ( '%s.%s' % ( self.property, 'Path'),   favPath.decode('string-escape')))
                xbmc.executebuiltin('Skin.SetString(%s,%s)' % ( '%s.%s' % ( self.property, 'Label'), favLabel))
               
                if favIcon:
                    xbmc.executebuiltin('Skin.SetString(%s,%s)' % ('%s.%s' % (self.property, 'Icon'), favIcon))
                    
                if isFolder:
                    xbmc.executebuiltin('Skin.SetString(%s,%s)' % ('%s.%s' % (self.property, 'IsFolder'), 'true'))
                else:
                    xbmc.executebuiltin('Skin.SetString(%s,%s)' % ('%s.%s' % (self.property, 'IsFolder'), 'false'))
                    
            else:
                xbmc.executebuiltin('Skin.Reset(%s)' % '%s.%s' % ( self.property, 'Path'))
                xbmc.executebuiltin('Skin.Reset(%s)' % '%s.%s' % ( self.property, 'Label'))
                xbmc.executebuiltin('Skin.Reset(%s)' % '%s.%s' % ( self.property, 'Icon'))
                xbmc.executebuiltin('Skin.Reset(%s)' % '%s.%s' % ( self.property, 'IsFolder'))

            try:    count = int(xbmcgui.Window(10000).getProperty('Super_Favourites_Count'))
            except: count = 0    
            xbmcgui.Window(10000).setProperty('Super_Favourites_Count', str(count+1))
            xbmcgui.Window(10000).setProperty('Super_Favourites_Chooser', 'false')
                
            xbmc.sleep(300)
            self.close()

                
    def onFocus(self, controlID):
        pass


    def changeFolder(self, path):
        path = path.replace('&', 'SF_AMP_SF')
        cmd = 'RunScript(special://home/addons/%s/chooser.py,property=%s&path=%s&changetitle=%s&includePlay=%s)' % (ADDONID, self.property, path, self.changeTitle, self.includePlay)
        self.close()    
        xbmc.executebuiltin(cmd)

        
def MyDialog(faves, property, changeTitle, path, mode, includePlay):
    w = MainGui('DialogSelect.xml', HOME, faves=faves, property=property, changeTitle=changeTitle, path=urllib.unquote_plus(path), mode=mode, includePlay=includePlay)
    w.doModal()
    del w

    
if __name__ == '__main__':
    Main()