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

import sys
import urllib
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin

dialog = xbmcgui.Dialog()
mode   = ''
#----------------------------------------------------------------
# TUTORIAL #
def Add_Dir(name, url='', mode='', folder=False, icon='', fanart='', description='', info_labels={}, set_art={}, set_property={}, content_type='', context_items=None, context_override=False, playable=False):
    """
This allows you to create a list item/folder inside your add-on.
Please take a look at your addon default.py comments for more information
(presuming you created one at http://totalrevolution.tv)

TOP TIP: If you want to send multiple variables through to a function just
send through as a dictionary encapsulated in quotation marks. In the function
you can then use the following code to access them:

params = eval(url)
^ That will then give you a dictionary where you can just pull each variable and value from.

CODE: Add_Dir(name, url, mode, [folder, icon, fanart, description, info_labels, content_type, context_items, context_override, playable])

AVAILABLE PARAMS:

    (*) name  -  This is the name you want to show for the list item

    url   -  If the route (mode) you're calling requires extra paramaters
    to be sent through then this is where you add them. If the function is
    only expecting one item then you can send through as a simple string.
    Unlike many other Add_Dir functions Python Koding does allow for multiple
    params to be sent through in the form of a dictionary so let's say your
    function is expecting the 2 params my_time & my_date. You would send this info
    through as a dictionary like this:
    url={'my_time':'10:00', 'my_date':'01.01.1970'}
    
    If you send through a url starting with plugin:// the item will open up into
    that plugin path so for example:
    url='plugin://plugin.video.youtube/play/?video_id=FTI16i7APhU'

    mode  -  The mode you want to open when this item is clicked, this is set
    in your master_modes dictionary (see template add-on linked above)

    folder       -  This is an optional boolean, by default it's set to False.
    True will open into a folder rather than an executable command

    icon         -  The path to the thumbnail you want to use for this list item

    fanart       -  The path to the fanart you want to use for this list item

    description  - A description of your list item, it's skin dependant but this
    usually appears below the thumbnail

    info_labels  - You can send through any number of info_labels via this option.
    For full details on the infolabels available please check the pydocs here:
    http://mirrors.kodi.tv/docs/python-docs/16.x-jarvis/xbmcgui.html#ListItem-setInfo

    When passing through infolabels you need to use a dictionary in this format:
    {"genre":"comedy", "title":"test video"}
    
    set_art  -  Using the same format as info_labels you can set your artwork via
    a dictionary here. Full details can be found here:
    http://mirrors.kodi.tv/docs/python-docs/16.x-jarvis/xbmcgui.html#ListItem-setArt

    set_property  -  Using the same format as info_labels you can set your artwork via
    a dictionary here. Full details can be found here:
    http://kodi.wiki/view/InfoLabels#ListItem

    content_type - By default this will set the content_type for kodi to a blank string
    which is what Kodi expects for generic category listings. There are plenty of different
    types though and when set Kodi will perform different actions (such as access the
    database looking for season/episode information for the list item).

    WARNING: Setting the wrong content type for your listing can cause the system to
    log thousands of error reports in your log, cause the system to lag and make
    thousands of unnecessary db calls - sometimes resulting in a crash. You can find
    details on the content_types available here: http://forum.kodi.tv/showthread.php?tid=299107

    context_items - Add context items to your directory. The params you need to send through
    need to be in a list format of [(label, action,),] look at the example code below for
    more details.

    context_override - By default your context items will be added to the global context
    menu items but you can override this by setting this to True and then only your
    context menu items will show.

    playable  -  By default this is set to False but if set to True kodi will just try
    and play this item natively with no extra fancy functions.

EXAMPLE:
my_context = [('Music','xbmc.executebuiltin("ActivateWindow(music)")'),('Programs','xbmc.executebuiltin("ActivateWindow(programs)")')]
# ^ This is our two basic context menu items (music and programs)

Add_Dir(name='TEST DIRECTORY', url='', mode='test_directory', folder=True, context_items=my_context, context_override=True)
# ^ This will add a folder AND a context menu item for when bring up the menu (when focused on this directory).
# ^^ The context_override is set to True which means it will override the default Kodi context menu items.

Add_Dir(name='TEST ITEM', url='', mode='test_item', folder=False, context_items=my_context, context_override=False)
# ^ This will add an item to the list AND a context menu item for when bring up the menu (when focused on this item).
# ^^ The context_override is set to False which means the new items will appear alongside the default Kodi context menu items.
~"""
    from vartools       import Convert_Special, Data_Type

    module_id   =  'script.module.python.koding.aio'
    this_module =  xbmcaddon.Addon(id=module_id)

    addon_handle = int(sys.argv[1])
# Check we're in an appropriate section for the content type set
    song_only_modes  = ['songs','artist','album','song','music']
    video_only_modes = ['sets','tvshows','seasons','actors','directors','unknown','video','set','movie','tvshow','season','episode']
    if xbmc.getInfoLabel('Window.Property(xmlfile)') == 'MyVideoNav.xml' and content_type in song_only_modes:
        content_type = ''
    if xbmc.getInfoLabel('Window.Property(xmlfile)') == 'MyMusicNav.xml' and content_type in video_only_modes:
        content_type = ''

    if description == '':
        description = this_module.getLocalizedString(30837)

    if Data_Type(url) == 'dict':
        url = repr(url)

    if Data_Type(info_labels) != 'dict':
        dialog.ok('WRONG INFO LABELS', 'Please check documentation, these should be sent through as a dictionary.')

    if Data_Type(set_art) != 'dict':
        dialog.ok('WRONG SET_ART', 'Please check documentation, these should be sent through as a dictionary.')

    if Data_Type(set_property) != 'dict':
        dialog.ok('WRONG SET_PROPERTY', 'Please check documentation, these should be sent through as a dictionary.')
     
# Set the default title, filename and plot if not sent through already via info_labels
    try:
        title = info_labels["Title"]
        if title == '':
            info_labels["Title"] = name
    except:
        info_labels["Title"] = name

    try:
        filename = info_labels["FileName"]
        # if filename == '':
        #     info_labels["FileName"] = name
    except:
        info_labels["FileName"] = name

    try:
        plot = info_labels["plot"]
        if plot == '':
            info_labels["plot"] = description
    except:
        info_labels["plot"] = description
# Set default thumbnail image used for listing (if not sent through via set_art)
    try:
        set_art["icon"]
    except:
        set_art["icon"] = icon

# Set default Fanart if not already sent through via set_property
    try:
        set_property["Fanart_Image"] = fanart
    except:
        set_property["Fanart_Image"]

# Set the main listitem properties
    liz = xbmcgui.ListItem(label=str(name), iconImage=str(icon), thumbnailImage=str(icon))

# Set the infolabels
    liz.setInfo(type=content_type, infoLabels=info_labels)

# Set the artwork
    liz.setArt(set_art)

# Loop through the set_property list and set each item in there
    for item in set_property.items():
        liz.setProperty(item[0], item[1])

# Add a context item (if details for context items are sent through)
    if context_items:
        liz.addContextMenuItems(context_items, context_override)

    u   = sys.argv[0]
    u += "?mode="           +str(mode)
    u += "&url="            +Convert_Special(url,string=True)
    u += "&name="           +urllib.quote_plus(name)
    u += "&iconimage="      +urllib.quote_plus(icon)
    u += "&fanart="         +urllib.quote_plus(fanart)
    u += "&description="    +urllib.quote_plus(description)
    
    if url.startswith('plugin://'):
        xbmcplugin.addDirectoryItem(handle=addon_handle,url=url,listitem=liz,isFolder=True) 

    elif folder:
        xbmcplugin.addDirectoryItem(handle=addon_handle,url=u,listitem=liz,isFolder=True)

    elif playable:
        liz.setProperty('IsPlayable', 'true')
        xbmcplugin.addDirectoryItem(handle=addon_handle,url=url,listitem=liz,isFolder=False) 

    else:
        xbmcplugin.addDirectoryItem(handle=addon_handle,url=u,listitem=liz,isFolder=False) 
#----------------------------------------------------------------
def Default_Mode():
    """ internal command ~"""
    dialog = xbmcgui.Dialog()
    dialog.ok('MODE ERROR','You\'ve tried to call Add_Dir() without a valid mode, check you\'ve added the mode into the master_modes dictionary')
#---------------------------------------------------------------- 