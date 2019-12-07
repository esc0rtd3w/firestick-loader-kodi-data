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
import re
import sys
import urllib
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
import xbmcvfs

from directory      import Add_Dir
from filetools      import Text_File
from vartools       import Find_In_Text
from guitools       import Text_Box, Show_Busy, Keyboard
from systemtools    import Sleep_If_Window_Active
from video          import Play_Video
from web            import Open_URL

dialog     = xbmcgui.Dialog()
py_path    = 'special://home/addons/script.module.python.koding.aio/lib/koding'
video_base = 'http://totalrevolution.tv/videos/python_koding/'
#----------------------------------------------------------------
def Grab_Tutorials():
    """ internal command ~"""
    import re
    full_array = []
    dirs,files = xbmcvfs.listdir(py_path)
# Check all the modules for functions with tutorial info
    for file in files:
        file_path = os.path.join(py_path,file)
        if file.endswith('.py') and file != 'tutorials.py':
            content = Text_File(file_path,'r').replace('\r','')
            # content_array = re.compile('# TUTORIAL #\ndef (.+?)\(').findall(content)
            content_array = Find_In_Text(content=content, start='# TUTORIAL #\ndef ', end='\(', show_errors=False)
            if content_array:
                for item in content_array:
                    item = item.strip()
                    full_array.append('%s~%s'%(item,file_path))
            content_array = Find_In_Text(content=content, start='# TUTORIAL #\nclass ', end='\(', show_errors=False)
            if content_array:
                for item in content_array:
                    item = item.strip()
                    full_array.append('%s~%s'%(item,file_path))

# Return a list of tutorials
    Add_Dir('[COLOR=gold]CREATE YOUR FIRST ADD-ON[/COLOR]',video_base+'Create_Addon.mov','play_video', folder=False, icon='', fanart='', description='How to create your own add-on using the Python Koding framework.')

    for item in sorted(full_array,key=str.lower):
        name, filepath = item.split('~')
        filepath = urllib.quote(filepath)
        Add_Dir(name=name.upper().replace('_',' '), url='%s~%s'%(name,filepath), mode='show_tutorial', folder=False, icon='', fanart='', description='Instructions for how to use the %s function.'%name)
#----------------------------------------------------------------
def Show_Tutorial(url):
    """ internal command ~"""
    name, filepath = url.split('~')
    filepath = urllib.unquote(filepath)
    readfile = Text_File(filepath,'r').replace('\r','')
    try:
        raw_find = Find_In_Text(content=readfile, start='# TUTORIAL #\ndef %s' % name,end='~"""')[0]
    except:
        raw_find = Find_In_Text(content=readfile, start='# TUTORIAL #\nclass %s' % name,end='~"""')[0]
# Check if an example code segment exists in the comments    
    if 'EXAMPLE CODE:' in raw_find:
        code = re.findall(r'(?<=EXAMPLE CODE:)(?s)(.*$)', raw_find)[0]
        code = code.replace('script.module.python.koding.aio','temp_replace_string')
        code = code.replace('koding.','').strip()
        code = code.replace('temp_replace_string','script.module.python.koding.aio')

    else:
        code = None

# Check if a video exists in the comments
    internetstate = xbmc.getInfoLabel('System.InternetState')
    if internetstate:
        video_page = Open_URL(video_base)
        extension = Find_In_Text(video_page, name, '"', False)
        if extension != '' and extension != None:
            video = video_base+name+extension[0]
        else:
            video = None
    else:
        video = None

    counter  = 0
    removal_string = ''
    final_header   = ''
    newline        = ''
    temp_raw = raw_find.splitlines()
    for line in temp_raw:
        if counter == 0:
            removal_string += line
            if '[' in line:
                replace_file = Find_In_Text(content=line,start='\[',end='\]')
                for item in replace_file:
                    line = line.replace(item,'')
            if ',' in line:
                header_extension = line.split(',')
                for item in header_extension:
                    if '=' in item:
                        item = item.split('=')[0]
                    final_header += item+','
                final_header = 'koding.'+name+final_header[:-2]+')'
            else:
                final_header = 'koding.'+name+line[:-1]
        else:
            removal_string += '\n'+line
        counter += 1
        if counter == 2:
            break
    if final_header.endswith('))'):
        final_header = final_header[:-1]
    if final_header.startswith('koding.User_Info'):
        final_header = 'koding.User_Info()'
    full_text = raw_find.replace(removal_string,'').strip()

# Initialise the dialog select
    dialog_array = ['Documentation']
    if code:
        dialog_array.append('Run Example Code')
    if video:
        dialog_array.append('Watch Video')
    
# If there's more than one item we show a dialog select otherwise we just load up the text window
    if len(dialog_array) > 1:
        choice = dialog.select(name, dialog_array)
        if choice >= 0:
            choice = dialog_array[choice]
        if choice == 'Documentation':
            Text_Box(final_header,full_text
                .replace('AVAILABLE PARAMS:','[COLOR=dodgerblue]AVAILABLE PARAMS:[/COLOR]')
                .replace('EXAMPLE CODE:','[COLOR=dodgerblue]EXAMPLE CODE:[/COLOR]')
                .replace('IMPORTANT:','[COLOR=gold]IMPORTANT:[/COLOR]')
                .replace('CODE:','[COLOR=dodgerblue]CODE:[/COLOR]')
                .replace('AVAILABLE VALUES:','[COLOR=dodgerblue]AVAILABLE VALUES:[/COLOR]')
                .replace('WARNING:','[COLOR=red]WARNING:[/COLOR]'))
        elif choice == 'Run Example Code':
            codefile = filepath.split(os.sep)
            codefile = codefile[len(codefile)-1].replace('.py','')
            exec('from %s import *' % codefile)
            # exec('from %s import %s' % (codefile, params["name"]))
            exec(code)
        elif choice == 'Watch Video':
            Play_Video(video)
        if choice < 0:
            return
    else:
        Text_Box(final_header,full_text
            .replace('AVAILABLE PARAMS:','[COLOR=dodgerblue]AVAILABLE PARAMS:[/COLOR]')
            .replace('EXAMPLE CODE:','[COLOR=dodgerblue]EXAMPLE CODE:[/COLOR]')
            .replace('IMPORTANT:','[COLOR=gold]IMPORTANT:[/COLOR]')
            .replace('CODE:','[COLOR=dodgerblue]CODE:[/COLOR]')
            .replace('AVAILABLE VALUES:','[COLOR=dodgerblue]AVAILABLE VALUES:[/COLOR]')
            .replace('WARNING:','[COLOR=red]WARNING:[/COLOR]'))
