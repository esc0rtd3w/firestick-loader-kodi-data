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
import sys
import xbmc
import xbmcgui
import xbmcvfs
from systemtools import Last_Error
from filetools import Physical_Path
dialog      = xbmcgui.Dialog()
koding_path = Physical_Path("special://home/addons/script.module.python.koding.aio")
#----------------------------------------------------------------    
# TUTORIAL #
def Browse_To_Folder(header='Select the folder you want to use', path = 'special://home'):
    """
As the title suggests this will bring up a dialog that allows the user to browse to a folder
and the path is then returned.

IMPORTANT: Do not confuse this with the Browse_To_File function

CODE: Browse_To_Folder(header, path)

AVAILABLE PARAMS:
header  -  As the name suggests this is a string to be used for the header/title
of the window. The default is "Select the folder you want to use".

path    -  Optionally you can add a default path for the browse start folder.
The default start position is the Kodi HOME folder.

EXAMPLE CODE:
folder = koding.Browse_To_Folder(header='Choose a folder you want to use', path='special://home/userdata')
dialog.ok('FOLDER DETAILS','Folder path: [COLOR=dodgerblue]%s[/COLOR]'%folder)
~"""    
    text = dialog.browse(type=3, heading=header, shares='files', useThumbs=False, treatAsFolder=False, defaultt=path)
    return text
#----------------------------------------------------------------    
# TUTORIAL #
def Browse_To_File(header='Select the file you want to use', path='special://home/addons/', extension='', browse_in_archives=False):
    """
This will allow the user to browse to a specific file and return the path.

IMPORTANT: Do not confuse this with the Browse_To_Folder function

CODE: koding.Browse_To_File([header, path, extension, browse_in_archives])

AVAILABLE PARAMS:

    header    -  As the name suggests this is a string to be used for the header/title
    of the window. The default is "Select the file you want to use".

    path      -  Optionally you can add a default path for the browse start folder.
    The default start position is the Kodi HOME folder.

    extension -  Optionally set extensions to filter by, let's say you only wanted
    zip and txt files to show you would send through '.zip|.txt'

    browse_in_archives -  Set to true if you want to be able to browse inside zips and
    other archive files. By default this is set to False.

EXAMPLE CODE:
dialog.ok('BROWSE TO FILE 1','We will now browse to your addons folder with browse_in_archives set to [COLOR dodgerblue]False[/COLOR]. Try clicking on a zip file if you can find one (check packages folder).')
folder = koding.Browse_To_File(header='Choose a file you want to use', path='special://home/addons')
dialog.ok('FOLDER DETAILS','File path: [COLOR=dodgerblue]%s[/COLOR]'%folder)
dialog.ok('BROWSE TO FILE 2','We will now browse to your addons folder with browse_in_archives set to [COLOR dodgerblue]True[/COLOR]. Try clicking on a zip file if you can find one (check packages folder).')
folder = koding.Browse_To_File(header='Choose a file you want to use', path='special://home/addons', browse_in_archives=True)
dialog.ok('FOLDER DETAILS','File path: [COLOR=dodgerblue]%s[/COLOR]'%folder)
~"""
    if not path.endswith(os.sep):
        path += os.sep
    try:
        text = dialog.browse(type=1, heading=header, shares='myprograms', mask=extension, useThumbs=False, treatAsFolder=browse_in_archives, defaultt=path)
    except:
        text = dialog.browse(type=1, heading=header, s_shares='myprograms', mask=extension, useThumbs=False,
                             treatAsFolder=browse_in_archives, defaultt=path)
    return text
#----------------------------------------------------------------    
# TUTORIAL #
def Countdown(title='COUNTDOWN STARTED', message='A quick simple countdown example.', update_msg='Please wait, %s seconds remaining.', wait_time=10, allow_cancel=True, cancel_msg='[COLOR=gold]Sorry, this process cannot be cancelled[/COLOR]'):
    """
Bring up a countdown timer and return true if waited or false if cancelled.

CODE: Countdown(title, message, update_msg, wait_time, allow_cancel, cancel_msg):

AVAILABLE PARAMS:

    title  -  The header string in the dialog window, the default is:
    'COUNTDOWN STARTED'

    message   -  A short line of info which will show on the first line
    of the dialog window just below the title. Default is:
    'A quick simple countdown example.'

    update_msg  - The message you want to update during the countdown.
    This must contain a %s which will be replaced by the current amount
    of seconds that have passed. The default is:
    'Please wait, %s seconds remaining.'

    wait_time  -  This is the amount of seconds you want the countdown to
    run for. The default is 10.

    allow_cancel  -  By default this is set to true and the user can cancel
    which will result in False being returned. If this is set to True
    they will be unable to cancel.

    cancel_msg  -  If allow_cancel is set to False you can add a custom
    message when the user tries to cancel. The default string is:
    '[COLOR=gold]Sorry, this process cannot be cancelled[/COLOR]'

EXAMPLE CODE:
dialog.ok('COUNTDOWN EXAMPLE', 'Press OK to bring up a countdown timer', '', 'Try cancelling the process.')
my_return = koding.Countdown(title='COUNTDOWN EXAMPLE', message='Quick simple countdown message (cancel enabled).', update_msg='%s seconds remaining', wait_time=5)
if my_return:
    dialog.ok('SUCCESS!','Congratulations you actually waited through the countdown timer without cancelling!')
else:
    dialog.ok('BORED MUCH?','What happened, did you get bored waiting?', '', '[COLOR=dodgerblue]Let\'s set off another countdown you CANNOT cancel...[/COLOR]')
    koding.Countdown(title='COUNTDOWN EXAMPLE', message='Quick simple countdown message (cancel disabled).', update_msg='%s seconds remaining', wait_time=5, allow_cancel=False, cancel_msg='[COLOR=gold]Sorry, this process cannot be cancelled[/COLOR]')
~"""
    dp        = xbmcgui.DialogProgress()
    current   = 0
    increment = 100 / wait_time
    cancelled = False

    dp.create(title)
    while current <= wait_time:
        if (dp.iscanceled()):
            if allow_cancel:
                cancelled = True
                break
            else:
                dp.create(title,cancel_msg)

        if current != 0: 
            xbmc.sleep(1000)

        remaining = wait_time - current
        if remaining == 0: 
            percent = 100
        else: 
            percent = increment * current
        
        remaining_display = update_msg % remaining
        dp.update(percent, message, remaining_display)

        current += 1

    if cancelled == True:     
        return False
    else:
        return True        
#----------------------------------------------------------------    
# TUTORIAL #
def Custom_Dialog(pos='center', dialog='Text', size='700x500', button_width=200, icon='', fanart='',\
    header='Disclaimer', main_content='Add some text here', buttons=['Decline','Agree'],\
    header_color='gold', text_color='white', background='000000', transparency=100,\
    highlight_color='gold', button_color_focused='4e91cf', button_trans_focused=100,\
    button_color_nonfocused='586381', button_trans_nonfocused=50):
    """
A fully customisable dialog where you can have as many buttons as you want.
Similar behaviour to the standard Kodi yesno dialog but this allows as many buttons
as you want, as much text as you want (with a slider) as well as fully configurable
sizing and positioning.

CODE: Custom_Dialog([pos, dialog, size, button_width, header, main_content, buttons,\
    header_color, text_color, background, transparency, highlight_color, button_color_focused,\
    button_trans_focused, button_color_nonfocused, button_trans_nonfocused])

AVAILABLE PARAMS:

    pos  -  This is the co-ordinates of where on the screen you want the
    dialog to appear. This needs to be sent through as a string so for
    example if you want the dialog top left corner to be 20px in and
    10px down you would use pos='20x10'. By default this is set to 'center'
    which will center the dialog on the screen.

    dialog   -  By default this is set to 'Text'. Currently that is the
    only custom dialog available but there are plans to improve upon this
    and allow for image and even video dialogs.

    size  - Sent through as a string this is the dimensions you want the
    dialog to be, by default it's set to '700x500' but you can set to any
    size you want using that same format. Setting to 'fullscreen' will
    use 1280x720 (fullscreen).

    button_width  -  This is sent through as an integer and is the width you
    want your buttons to be. By default this is set to 200 which is quite large
    but looks quite nice if using only 2 or 3 buttons.

    icon  -  If sent through this will be shown in the top right corner of your dialog,
    make sure your first few lines of text aren't too long or they will overlap on top
    of the image which is 150x150 pixels.
    
    fanart  -  If sent through this will be the background image of your custom dialog.
    Ideal if you want to only show an image, any text sent through will be overlayed
    on top of this fanart.

    header  -  Sent through as a string this is the header shown in the dialog.
    The default is 'Disclaimer'.

    header_color  -  Set the text colour, by default it's 'gold'

    text_color  -  Set the text colour, by default it's 'white'

    main_content  -  This is sent through as a string and is the main message text
    you want to show in your dialog. When the ability to add videos, images etc.
    is added there may well be new options added to this param but it will remain
    backwards compatible.

    buttons  -  Sent through as a list (tuple) this is a list of all your buttons.
    Make sure you do not duplicate any names otherwise it will throw off the
    formatting of the dialog and you'll get false positives with the results.

    background  -  Optionally set the background colour (hex colour codes required).
    The default is '000000' (black).

    transparency  -  Set the percentage of transparency as an integer. By default
    it's set to 100 which is a solid colour.

    highlight_color  -  Set the highlighted text colour, by default it's 'gold'

    button_color_focused - Using the same format as background you can set the
    colour to use for a button when it's focused.

    button_trans_focused - Using the same format as transparency you can set the
    transparency amount to use on the button when in focus.

    button_color_nonfocused - Using the same format as background you can set the
    colour to use for buttons when they are not in focus.

    button_trans_nonfocused - Using the same format as transparency you can set the
    transparency amount to use on the buttons when not in focus.

EXAMPLE CODE:
main_text = 'This is my main text.\n\nYou can add anything you want in here and the slider will allow you to see all the contents.\n\nThis example shows using a blue background colour and a transparency of 90%.\n\nWe have also changed the highlighted_color to yellow.'
my_buttons = ['button 1', 'button 2', 'button 3']
my_choice = koding.Custom_Dialog(main_content=main_text,pos='center',buttons=my_buttons,background='213749',transparency=90,highlight_color='yellow')
dialog.ok('CUSTOM DIALOG 1','You selected option %s'%my_choice,'The value of this is: [COLOR=dodgerblue]%s[/COLOR]'%my_buttons[my_choice])

main_text = 'This is example 2 with no fancy colours, just a fullscreen and a working scrollbar.\n\nYou\'ll notice there are also a few more buttons on this one.\n\nline 1\nline 2\nline 3\nline 4\nline 5\nline 6\nline 7\nline 8\nline 9\nline 10\nline 11\nline 12\nline 13\nline 14\nline 15\nline 16\nline 17\nline 18\nline 19\nline 20\n\nYou get the idea we\'ll stop there!'
my_buttons = ['button 1', 'button 2', 'button 3','button 4', 'button 5', 'button 6','button 7', 'button 8', 'button 9','button 10', 'button 11', 'button 12', 'button 13','button 14', 'button 15', 'button 16','button 17', 'button 18', 'button 19','button 20']
my_choice = koding.Custom_Dialog(main_content=main_text,pos='center',size='fullscreen',buttons=my_buttons)
dialog.ok('CUSTOM DIALOG 2','You selected option %s'%my_choice,'The value of this is: [COLOR=dodgerblue]%s[/COLOR]'%my_buttons[my_choice])
~"""
    skin_path   = os.path.join(koding_path,"resources","skins","Default","720p")
    ACTION      = -1
    # Convert the transparency percentage to hex
    transparency = float(transparency) / 100 * 255
    transparency = hex(int(transparency)).split('x')[1]
    button_trans_focused = float(button_trans_focused) / 100 * 255
    button_trans_focused = hex(int(button_trans_focused)).split('x')[1]
    button_trans_nonfocused = float(button_trans_nonfocused) / 100 * 255
    button_trans_nonfocused = hex(int(button_trans_nonfocused)).split('x')[1]

    # Work out the dialog dimensions
    if size == 'fullscreen':
        dialog_width = '1280'
        dialog_height = '720'
    else:
        dialog_width, dialog_height = size.split('x')  

    # Set the background to black image if not set otherwise remove background/transparency
    if fanart != '' and xbmcvfs.exists(fanart):
        background = ''
        transparency = ''
    else:
        fanart = 'DialogBack.png'

    button_count    = len(buttons)
    buttons_per_row = (int(dialog_width)-25) / (button_width+25)
    if buttons_per_row > button_count:
        buttons_per_row = button_count

    # work out the number of rows, round up if a float
    button_rows     = int(button_count/buttons_per_row) + (button_count % buttons_per_row > 0)

    # Work out the positioning of the dialog
    if pos == 'center':
        posx = str( (1280 - int(dialog_width)) / 2)
        posy = str( (720 - int(dialog_height)) / 2)
    else:
        posx, posy = pos.split(',')

# Work out the text area size
    text_width  = str( int(dialog_width)-80 )
    text_height = str( (int(dialog_height)-(50*(button_rows+1)))-70 )
    scroll_pos  = str( int(text_width)+32 )
    button_max  = int(dialog_height)-30
    iconx       = str(int(text_width)-150)

    # Work out the button positions
    if dialog == 'Text':
        button_spacing  = ( int(dialog_width)-(buttons_per_row*button_width) ) / (buttons_per_row+1)
        buttons_dict    = {}
        counter         = 1
        row             = 1
        # Create a dictionary of button positioning
        for button in buttons:
            if counter > buttons_per_row:
                counter = 1
                row += 1
            # If starting a new line reset the values
            if counter > buttons_per_row or counter == 1:
                current_pos = button_spacing
                counter += 1
            else:
                current_pos = current_pos+button_width+button_spacing
                counter += 1

            buttons_dict[button] = [str(current_pos),row]

    # Set the dialog template name and new temporary "live" XML
    dialog_type = dialog.capitalize()+'.xml'
    dialog_new  = 'temp.xml'
    dialog_path = os.path.join(skin_path,dialog_type)
    temp_path   = os.path.join(skin_path,dialog_new)

    button_num   = 100
    counter      = 1
    buttons_code = ''
    for button in buttons:
        if buttons_dict[button][1] == 1:
            onup = 99
        else:
            onup = button_num-buttons_per_row

        # If button is on the last row we set down to scrollbar
        if buttons_dict[button][1] == button_rows:
            ondown = 99
        # Otherwise set down to the item on row below
        elif buttons_dict[button][1] != button_rows:
            ondown = button_num+buttons_per_row

        # Set the vertical position (y) of the buttons
        button_y = str( int(text_height)+(buttons_dict[button][1]*50)+40 )
        if ( int(text_height) < 200 ) or ( int(button_y) > button_max ):
            if size != 'fullscreen':
                xbmcgui.Dialog().ok('WE NEED A BIGGER WINDOW!','The amount of buttons sent through do not fit in this window. Either make the button width smaller or make a bigger window')
            else:
                xbmcgui.Dialog().ok('SMALLER BUTTONS NEEDED!','The amount of buttons sent through do not fit in this window. Either send through less buttons or decrease their width using the button_width param.')
            return
        button_x = str( buttons_dict[button][0] )

        buttons_code += '\
           <control type="button" id="%s">\n\
                <posx>%s</posx>\n\
                <posy>%s</posy>\n\
                <width>%s</width>\n\
                <height>40</height>\n\
                <label>%s</label>\n\
                <texturefocus colordiffuse="%s%s">DialogBack.png</texturefocus>\n\
                <texturenofocus colordiffuse="%s%s">DialogBack.png</texturenofocus>\n\
                <font>font12_title</font>\n\
                <textcolor>%s</textcolor>\n\
                <focusedcolor>%s</focusedcolor>\n\
                <align>center</align>\n\
                <onleft>%s</onleft>\n\
                <onright>%s</onright>\n\
                <onup>%s</onup>\n\
                <ondown>%s</ondown>\n\
            </control>\n' % (button_num, button_x, button_y, button_width, buttons[counter-1],\
                            button_trans_focused, button_color_focused, button_trans_nonfocused,\
                            button_color_nonfocused, text_color, highlight_color, button_num-1,\
                            button_num+1, onup, ondown)
        button_num += 1
        counter    += 1

    # Grab contents of the template and replace with our new values
    with open(dialog_path, 'r') as content_file:
        content = content_file.read()
        content = content.replace('dialog_width',dialog_width)\
            .replace('dialog_height',dialog_height)\
            .replace('text_width',text_width)\
            .replace('text_height',text_height)\
            .replace('pos_x',posx)\
            .replace('pos_y',posy)\
            .replace('PK_Icon',icon)\
            .replace('PK_I_X',iconx)\
            .replace('PK_Fanart',fanart)\
            .replace('PK_Transparency',transparency)\
            .replace('PK_Color',background)\
            .replace('PK_Text_Color',text_color)\
            .replace('PK_Header_Color',header_color)\
            .replace('<!-- buttons -->',buttons_code)
    # Create the new temp "live" XML
    myfile = open(temp_path,'w')
    myfile.write(content)
    myfile.close()

    d=MyDisclaimer(dialog_new,koding_path,header=header,main_content=main_content)
    d.doModal()
    ACTION = d.ACTION
    del d
    return ACTION

class MyDisclaimer(xbmcgui.WindowXMLDialog):
    def __init__(self,*args,**kwargs):
        self.header=kwargs['header']
        self.main_content=kwargs['main_content']
        self.WINDOW=xbmcgui.Window( 10000 )
        self.WINDOW.setProperty( 'PK_Header' , self.header )
        self.WINDOW.setProperty( 'PK_Main_Text' , self.main_content )
        self.ACTION=-1
    def onClick( self, controlID ):
        if controlID>=100:
            self.ACTION=(controlID-100)
            self.close()
        elif controlID==12:
            self.close()
    def onAction( self, action ):
        if action in [ 5, 6, 7, 9, 10, 92, 117 ] or action.getButtonCode() in [275,257,261]:
            self.close()
#----------------------------------------------------------------    
# TUTORIAL #
def Keyboard(heading='',default='',hidden=False,return_false=False,autoclose=False,kb_type='alphanum'):
    """
Show an on-screen keyboard and return the string

CODE: koding.Keyboard([default, heading, hidden, return_false, autoclose, kb_type])

AVAILABLE PARAMS:

    heading  -  Optionally enter a heading for the text box.

    default  -  This is optional, if set this will act as the default text shown in the text box

    hidden   -  Boolean, if set to True the text will appear as hidden (starred out)

    return_false - By default this is set to False and when escaping out of the keyboard
    the default text is returned (or an empty string if not set). If set to True then
    you'll receive a return of False.

    autoclose - By default this is set to False but if you want the keyboard to auto-close
    after a period of time you can send through an integer. The value sent through needs to
    be milliseconds, so for example if you want it to close after 3 seconds you'd send through
    3000. The autoclose function only works with standard alphanumeric keyboard types.

    kb_type  -  This is the type of keyboard you want to show, by default it's set to alphanum.
    A list of available values are listed below:

        'alphanum'  - A standard on-screen keyboard containing alphanumeric characters.
        'numeric'   - An on-screen numerical pad.
        'date'      - An on-screen numerical pad formatted only for a date.
        'time'      - An on-screen numerical pad formatted only for a time.
        'ipaddress' - An on-screen numerical pad formatted only for an IP Address.
        'password'  - A standard keyboard but returns value as md5 hash. When typing
        the text is starred out, once you've entered the password you'll get another
        keyboard pop up asking you to verify. If the 2 match then your md5 has is returned.


EXAMPLE CODE:
mytext = koding.Keyboard(heading='Type in the text you want returned',default='test text')
dialog.ok('TEXT RETURNED','You typed in:', '', '[COLOR=dodgerblue]%s[/COLOR]'%mytext)
dialog.ok('AUTOCLOSE ENABLED','This following example we\'ve set the autoclose to 3000. That\'s milliseconds which converts to 3 seconds.')
mytext = koding.Keyboard(heading='Type in the text you want returned',default='this will close in 3s',autoclose=3000)
dialog.ok('TEXT RETURNED','You typed in:', '', '[COLOR=dodgerblue]%s[/COLOR]'%mytext)
mytext = koding.Keyboard(heading='Enter a number',kb_type='numeric')
dialog.ok('NUMBER RETURNED','You typed in:', '', '[COLOR=dodgerblue]%s[/COLOR]'%mytext)
dialog.ok('RETURN FALSE ENABLED','All of the following examples have "return_false" enabled. This means if you escape out of the keyboard the return will be False.')
mytext = koding.Keyboard(heading='Enter a date',return_false=True,kb_type='date')
dialog.ok('DATE RETURNED','You typed in:', '', '[COLOR=dodgerblue]%s[/COLOR]'%mytext)
mytext = koding.Keyboard(heading='Enter a time',return_false=True,kb_type='time')
dialog.ok('TIME RETURNED','You typed in:', '', '[COLOR=dodgerblue]%s[/COLOR]'%mytext)
mytext = koding.Keyboard(heading='IP Address',return_false=True,kb_type='ipaddress',autoclose=5)
dialog.ok('IP RETURNED','You typed in:', '', '[COLOR=dodgerblue]%s[/COLOR]'%mytext)
mytext = koding.Keyboard(heading='Password',kb_type='password')
dialog.ok('MD5 RETURN','The md5 for this password is:', '', '[COLOR=dodgerblue]%s[/COLOR]'%mytext)
~"""
    from vartools import Decode_String
    kb_type = eval( 'xbmcgui.INPUT_%s'%kb_type.upper() )
    if hidden:
        hidden = eval( 'xbmcgui.%s_HIDE_INPUT'%kb_type.upper() )
    keyboard = dialog.input(heading,default,kb_type,hidden,autoclose)

    if keyboard != '':
        return keyboard
    
    elif not return_false:
        return Decode_String(default)
    
    else:
        return False
#----------------------------------------------------------------    
# TUTORIAL #
def Notify(title, message, duration=2000, icon='special://home/addons/script.module.python.koding.aio/resources/update.png'):
    """
Show a short notification for x amount of seconds

CODE: koding.Notify(title, message, [duration, icon])

AVAILABLE PARAMS:

    (*) title    -  A short title to show on top line of notification

    (*) message  -  A short message to show on the bottom line of notification

    duration  -  An integer in milliseconds, the default to show the notification for is 2000

    icon      -  The icon to show in notification bar, default is the update icon from this module. 

EXAMPLE CODE:
koding.Notify(title='TEST NOTIFICATION', message='This is a quick 5 second test', duration=5000)
~"""
    xbmc.executebuiltin('XBMC.Notification(%s, %s, %s, %s)' % (title , message , duration, icon))
#----------------------------------------------------------------
# TUTORIAL #
def OK_Dialog(title,message):
    """
This will bring up a short text message in a dialog.ok window.

CODE: OK_Dialog(title,message)

AVAILABLE PARAMS:

    (*) title  -  This is title which appears in the header of the window.

    (*) message  -  This is the main text you want to appear.

EXAMPLE CODE:
koding.OK_Dialog(title='TEST DIALOG',message='This is a test dialog ok box. Click OK to quit.')
~"""
    dialog.ok(title,message)
#----------------------------------------------------------------
# TUTORIAL #
def Select_Dialog(title,options,key=True):
    """
This will bring up a selection of options to choose from. The options are
sent through as a list and only one can be selected - this is not a multi-select dialog.

CODE: Select_Dialog(title,options,[key])

AVAILABLE PARAMS:

    (*) title  -  This is title which appears in the header of the window.

    (*) options  -  This is a list of the options you want the user to be able to choose from.

    key  -  By default this is set to True so you'll get a return of the item number. For example
    if the user picks "option 2" and that is the second item in the list you'll receive a return of
    1 (0 would be the first item in list and 1 is the second). If set to False you'll recieve a return
    of the actual string associated with that key, in this example the return would be "option 2".

EXAMPLE CODE:
my_options = ['Option 1','Option 2','Option 3','Option 4','Option 5']
mychoice = koding.Select_Dialog(title='TEST DIALOG',options=my_options,key=False)
koding.OK_Dialog(title='SELECTED ITEM',message='You selected: [COLOR=dodgerblue]%s[/COLOR]\nNow let\'s try again - this time we will return a key...'%mychoice)
mychoice = koding.Select_Dialog(title='TEST DIALOG',options=my_options,key=True)
koding.OK_Dialog(title='SELECTED ITEM',message='The item you selected was position number [COLOR=dodgerblue]%s[/COLOR] in the list'%mychoice)
~"""
    mychoice = dialog.select(title,options)
    if key:
        return mychoice
    else:
        return options[mychoice]
#----------------------------------------------------------------
# TUTORIAL #
def Show_Busy(status=True, sleep=0):
    """
This will show/hide a "working" symbol.

CODE: Show_Busy([status, sleep])

AVAILABLE PARAMS:

    status - This optional, by default it's True which means the "working"
    symbol appears. False will disable.

    sleep  -  If set the busy symbol will appear for <sleep> amount of
    milliseconds and then disappear.

EXAMPLE CODE:
dialog.ok('BUSY SYMBOL','Press OK to show a busy dialog which restricts any user interaction. We have added a sleep of 5 seconds at which point it will disable.')
koding.Show_Busy(sleep=5000)
dialog.ok('BUSY SYMBOL','We will now do the same but with slightly different code')
koding.Show_Busy(status=True)
xbmc.sleep(5000)
koding.Show_Busy(status=False)
~"""
    if status:
        xbmc.executebuiltin("ActivateWindow(busydialog)")
        if sleep:
            xbmc.sleep(sleep)
            xbmc.executebuiltin("Dialog.Close(busydialog)")
    else:
        xbmc.executebuiltin("Dialog.Close(busydialog)")
#----------------------------------------------------------------    
# TUTORIAL #
def Text_Box(header, message):
    """
This will allow you to open a blank window and fill it with some text.

CODE: koding.Text_Box(header, message)

AVAILABLE PARAMS:

    (*) header  -  As the name suggests this is a string to be used for the header/title of the window

    (*) message -  Yes you've probably already gussed it, this is the main message text


EXAMPLE CODE:
koding.Text_Box('TEST HEADER','Just some random text... Use kodi tags for new lines, colours etc.')
~"""
    xbmc.executebuiltin("ActivateWindow(10147)")
    controller = xbmcgui.Window(10147)
    xbmc.sleep(500)
    controller.getControl(1).setLabel(header)
    controller.getControl(5).setText(message)
#----------------------------------------------------------------
# TUTORIAL #
def Reset_Percent(property='update_percent_',window_id=10000):
    """
If using the Update_Progress function for setting percentages in skinning then this
will allow you to reset all the percent properties (1-100)

CODE: Reset_Percent([property,window_id])

AVAILABLE PARAMS:

    property  -  the property name you want reset, this will reset all properties starting
    with this string from 1-100. For example if you use the default 'update_percent_' this
    will loop through and reset update_percent_1, update_percent_2 etc. all the way through
    to update_percent_100.

    window_id -  By default this is set to 10000 but you can send any id through you want.

    kwargs  -  Send through any other params and the respective property will be set.colours etc.')
~"""
    counter = 0
    while counter <= 100:
        xbmcgui.Window(10000).clearProperty('update_percent_%s'%counter)
        counter +=1
#----------------------------------------------------------------
# TUTORIAL #
def Update_Progress(total_items,current_item,**kwargs):
    """
This function is designed for skinners but can be used for general Python too. It will
work out the current percentage of items that have been processed and update the
"update_percent" property accordingly (1-100). You can also send through any properties
you want updated and it will loop through updating them with the relevant values.

To send through properties just send through the property name as the param and assign to a value.
Example: Update_Progress( total_items=100,current_item=56, {"myproperty1":"test1","myproperty2":"test2"} )


CODE: Update_Progress(total_items,current_item,[kwargs])

AVAILABLE PARAMS:

    (*) total_items  -  Total amount of items in your list you're processing

    (*) current_item -  Current item number that's been processed.

    kwargs  -  Send through any other params and the respective property will be set.colours etc.
~"""
    Reset_Percent()
    for item in kwargs:
        if item.endswith('color'):
            value = '0xFF'+kwargs[item]
        else:
            value = kwargs[item]
        if value == 'false' or value == '' and not item.endswith('color'):
            xbmcgui.Window(10000).clearProperty(item)
        elif value:
            xbmcgui.Window(10000).setProperty(item, value)
    percent = 100*(current_item/(total_items*1.0))
    newpercent=int(percent)
    if (newpercent % 1 == 0) and (newpercent <=100):
        xbmcgui.Window(10000).setProperty('update_percent',str(newpercent))
        xbmcgui.Window(10000).setProperty('update_percent_%s'%newpercent,'true')
    if newpercent == 100:
        xbmc.executebuiltin('Action(firstpage)')
#-----------------------------------------------------------------------------
# TUTORIAL #
def Update_Screen(disable_quit=False, auto_close=True):
    """
This will create a full screen overlay showing progress of updates. You'll need to
use this in conjunction with the Update_Progress function.

CODE: Update_Screen([disable_quit, auto_close))

AVAILABLE PARAMS:

    disable_quit  -  By default this is set to False and pressing the parent directory
    button (generally esc) will allow you to close the window. Setting this to True
    will mean it's not possible to close the window manually.

    auto_close  -  By default this is set to true and when the percentage hits 100
    the window will close. If you intend on then sending through some more commands
    you might want to consider leaving this window open in which case you'd set this
    to false. Bare in mind if you go this route the window will stay active until
    you send through the kill command which is: xbmc.executebuiltin('Action(firstpage)')

EXAMPLE CODE:
mykwargs = {
    "update_header"    : "Downloading latest updates",\
    "update_main_text" : "Your device is now downloading all the latest updates.\nThis shouldn\'t take too long, "\
                         "depending on your internet speed this could take anything from 2 to 10 minutes.\n\n"\
                         "Once downloaded the system will start to install the updates.",\
    "update_bar_color" : "4e91cf",\
    "update_icon"      : "special://home/addons/script.module.python.koding.aio/resources/skins/Default/media/update.png",\
    "update_spinner"   : "true"}
Update_Screen()
counter = 1
while counter <= 60:
    xbmc.sleep(300)
    Update_Progress(total_items=60,current_item=counter,**mykwargs)
    if counter == 30:
        mykwargs = {
            "update_header"        : "Halfway there!",\
            "update_main_text"     : "We just updated the properties to show how you can change things on the fly "\
                                     "simply by sending through some different properties. Both the icon and the "\
                                     "background images you see here are being pulled from online.",\
            "update_header_color"  : "4e91cf",\
            "update_percent_color" : "4e91cf",\
            "update_bar_color"     : "4e91cf",\
            "update_background"    : "http://www.planwallpaper.com/static/images/518164-backgrounds.jpg",\
            "update_icon"          : "http://totalrevolution.tv/img/tr_small_black_bg.jpg",\
            "update_spinner"       : "false"}
    counter += 1
~"""
    import threading
    update_screen_thread = threading.Thread(target=Show_Update_Screen, args=[disable_quit, auto_close])
    update_screen_thread.start()
    xbmc.sleep(2000)

def Show_Update_Screen(disable_quit=False,auto_close=True):
    xbmcgui.Window(10000).clearProperty('update_icon')
    xbmcgui.Window(10000).clearProperty('update_percent')
    xbmcgui.Window(10000).clearProperty('update_spinner')
    xbmcgui.Window(10000).clearProperty('update_header')
    xbmcgui.Window(10000).clearProperty('update_main_text')
    xbmcgui.Window(10000).setProperty('update_background','whitebg.jpg')
    xbmcgui.Window(10000).setProperty('update_percent_color','0xFF000000')
    xbmcgui.Window(10000).setProperty('update_bar_color','0xFF000000')
    xbmcgui.Window(10000).setProperty('update_main_color','0xFF000000')
    xbmcgui.Window(10000).setProperty('update_header_color','0xFF000000')
# Set a property so we can determine if update screen is active
    xbmcgui.Window(10000).setProperty('update_screen','active')
    d=MyUpdateScreen('Loading.xml',koding_path,disable_quit=disable_quit,auto_close=auto_close)
    d.doModal()
    del d
    xbmcgui.Window(10000).clearProperty('update_screen')

class MyUpdateScreen(xbmcgui.WindowXMLDialog):
    def __init__(self,*args,**kwargs):
        self.disable_quit=kwargs['disable_quit']
        self.auto_close=kwargs['auto_close']
        self.WINDOW=xbmcgui.Window( 10000 )
    def onAction( self, action ):
        if action in [10,7]:
            if self.disable_quit:
                xbmc.log("ESC and HOME Disabled",2)
            else:
                self.close()
        if action==159 and self.auto_close:
            self.close()
#----------------------------------------------------------------    
# TUTORIAL #
def YesNo_Dialog(title,message,yes=None,no=None):
    """
This will bring up a short text message in a dialog.yesno window. This will
return True or False

CODE: YesNo_Dialog(title,message,[yeslabel,nolabel])

AVAILABLE PARAMS:

    (*) title  -  This is title which appears in the header of the window.

    (*) message  -  This is the main text you want to appear.

    yes  -  Optionally change the default "YES" to a custom string

    no  -  Optionally change the default "NO" to a custom string

EXAMPLE CODE:
mychoice = koding.YesNo_Dialog(title='TEST DIALOG',message='This is a yes/no dialog with custom labels.\nDo you want to see an example of a standard yes/no.',yes='Go on then',no='Nooooo!')
if mychoice:
    koding.YesNo_Dialog(title='STANDARD DIALOG',message='This is an example of a standard one without sending custom yes/no params through.')
~"""
    choice = dialog.yesno(title,message,yeslabel=yes,nolabel=no)
    return choice
#----------------------------------------------------------------
