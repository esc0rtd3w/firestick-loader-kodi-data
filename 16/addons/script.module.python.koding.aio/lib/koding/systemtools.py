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

import datetime
import os
import sys
import shutil
import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs
try:
    from vartools import Data_Type
except:
    pass
#----------------------------------------------------------------
# TUTORIAL #
def Cleanup_Textures(frequency=14,use_count=10):
    """
This will check for any cached artwork and wipe if it's not been accessed more than 10 times in the past x amount of days.

CODE: Cleanup_Textures([frequency, use_count])

AVAILABLE PARAMS:
    
    frequency  -  This is an optional integer, be default it checks for any
    images not accessed in 14 days but you can use any amount of days here.

    use_count   -  This is an optional integer, be default it checks for any
    images not accessed more than 10 times. If you want to be more ruthless
    and remove all images not accessed in the past x amount of days then set this very high.

EXAMPLE CODE:
dialog.ok('Clean Textures','We are going to clear any old cached images not accessed at least 10 times in the past 5 days')
koding.Cleanup_Textures(frequency=5)
~"""
    try: from sqlite3 import dbapi2 as database
    except: from pysqlite2 import dbapi2 as database
    from filetools import DB_Path_Check

    db   = DB_Path_Check('Textures')
    xbmc.log('### DB_PATH: %s' % db)
    conn = database.connect(db, timeout = 10, detect_types=database.PARSE_DECLTYPES, check_same_thread = False)
    conn.row_factory = database.Row
    c = conn.cursor()

    # Set paramaters to check in db, cull = the datetime (we've set it to 14 days) and useCount is the amount of times the file has been accessed
    cull     = datetime.datetime.today() - datetime.timedelta(days = frequency)

    # Create an array to store paths for images and ids for database
    ids    = []
    images = []

    c.execute("SELECT idtexture FROM sizes WHERE usecount < ? AND lastusetime < ?", (use_count, str(cull)))

    for row in c:
        ids.append(row["idtexture"])

    for id in ids:
        c.execute("SELECT cachedurl FROM texture WHERE id = ?", (id,))
        for row in c:
            images.append(row["cachedurl"])


# Clean up database
    for id in ids:       
        c.execute("DELETE FROM sizes   WHERE idtexture = ?", (id,))
        c.execute("DELETE FROM texture WHERE id        = ?", (id,))

    c.execute("VACUUM")
    conn.commit()
    c.close()

    xbmc.log("### Automatic Cache Removal: %d Old Textures removed" % len(images))

# Delete files
    thumbfolder = 'special://home/userdata/Thumbnails'
    for image in images:
        path = os.path.join(thumbfolder, image)
        try:
            xbmcvfs.delete(path)
        except:
            xbmc.log(Last_Error())
#----------------------------------------------------------------
# TUTORIAL #
def Current_Profile():
    """
This will return the current running profile, it's only one line of code but this is for my benefit as much as
anyone else's. I use this function quite a lot and keep forgetting the code so figured it would be easier to
just write a simple function for it :)

CODE:  Current_Profile()

EXAMPLE CODE:
profile = koding.Current_Profile()
dialog.ok('CURRENT PROFILE','Your current running profile is:','[COLOR=dodgerblue]%s[/COLOR]' % profile)
~"""

    return xbmc.getInfoLabel('System.ProfileName')
#----------------------------------------------------------------
# TUTORIAL #
def Force_Close():
    """
Force close Kodi, should only be used in extreme circumstances.

CODE: Force_Close()

EXAMPLE CODE:
if dialog.yesno('FORCE CLOSE','Are you sure you want to forcably close Kodi? This could potentially cause corruption if system tasks are taking place in background.'):
    koding.Force_Close()
~"""
    os._exit(1)
#----------------------------------------------------------------
# TUTORIAL #
def Get_ID(setid=False):
    """
A simple function to set user id and group id to the current running App
for system commands. For example if you're using the subprocess command
you could send through the preexec_fn paramater as koding.Get_ID(setid=True).
This function will also return the uid and gid in form of a dictionary.

CODE: Get_ID([setid])

AVAILABLE PARAMS:
    
    (*) setid  -  By default this is set to False but if set to True it
    will set the ids (to be used for subprocess commands)

EXAMPLE CODE:
ids = Get_ID(setid=False)
if ids:
    uid = ids['uid']
    gid = ids['gid']
    dialog.ok('USER & GROUP ID','User ID: %s'%uid, 'Group ID: %s'%gid)
else:
    dialog.ok('USER & GROUP ID','This function is not applicable to your system. We\'ve been sent back a return of False to indicate this function does not exist on your os.')
~"""
    try:
        uid = os.getuid()
        gid = os.getgid()
        if setid:
            os.setgid(uid)
            os.setuid(gid)
        if not setid:
            return {"uid":uid,"gid":gid}
    except:
        return False
#----------------------------------------------------------------
def Get_Mac(protocol = 'eth'):
    cont      = False
    vpn_check = False
    counter   = 0
    mac       = ''
    while len(mac)!=17 and counter < 5:
        if sys.platform == 'win32':
            for line in os.popen("ipconfig /all"):
                if protocol == 'wifi':
                    if line.startswith('Wireless LAN adapter Wi'):
                        cont = True
                    if line.lstrip().startswith('Physical Address') and cont:
                        mac = line.split(':')[1].strip().replace('-',':').replace(' ','')
                        break
                else:
                    if line.lstrip().startswith('Description'):
                        if not 'VPN' in line:
                            vpn_check = True
                    if line.lstrip().startswith('Physical Address') and vpn_check:
                        mac = line.split(':')[1].strip().replace('-',':').replace(' ','')
                        vpn_check = False
                        break

        elif sys.platform == 'darwin': 
            if protocol == 'wifi':
                for line in os.popen("ifconfig en0 | grep ether"):
                    if line.lstrip().startswith('ether'):
                        mac = line.split('ether')[1].strip().replace('-',':').replace(' ','')
                        break
            else:
                for line in os.popen("ifconfig en1 | grep ether"):
                    if line.lstrip().startswith('ether'):
                        mac = line.split('ether')[1].strip().replace('-',':').replace(' ','')
                        break

        elif xbmc.getCondVisibility('System.Platform.Android'):
            try:
                if protocol == 'wifi':
                    readfile = open('/sys/class/net/wlan0/address', mode='r')
                if protocol != 'wifi':
                    readfile = open('/sys/class/net/eth0/address', mode='r')
                mac = readfile.read()
                readfile.close()
                mac = mac.strip()
                mac = mac.replace(' ','')
                mac = mac[:17]
            except:
                mac = ''

        else:
            mac = ''
            if protocol == 'wifi':
                for line in os.popen("/sbin/ifconfig"):
                    if line.find('wlan0') > -1: 
                        mac = line.split()[4].strip()
                        break
                    elif line.startswith('en'):
                        if 'Ethernet'in line and 'HWaddr' in line:
                            mac = line.split('HWaddr')[1].strip()
                            break
            else:
               for line in os.popen("/sbin/ifconfig"): 
                    if line.find('eth0') > -1: 
                        mac = line.split()[4].strip()
                        break
                    elif line.startswith('wl'):
                        if 'Ethernet'in line and 'HWaddr' in line:
                            mac = line.split('HWaddr')[1].strip()
                            break
        counter += 1
        xbmc.log('attempt no.%s %s mac: %s'%(counter,protocol,mac),2)
    if len(mac) != 17:
        counter = 0
        while counter < 5 and len(mac) != 17:
            mac = xbmc.getInfoLabel('Network.MacAddress')
            xbmc.log('MAC (backup): %s'%mac,2)
            xbmc.sleep(100)
            counter += 1
    if len(mac) != 17:
        return 'Unknown'
    else:
        return mac
#-----------------------------------------------------------------------------
# TUTORIAL #
def Grab_Log(log_type = 'std', formatting = 'original', sort_order = 'reverse'):
    """
This will grab the log file contents, works on all systems even forked kodi.

CODE:  Grab_Log([log_type, formatting, sort_order])

AVAILABLE PARAMS:
    
    log_type    -  This is optional, if not set you will get the current log.
    If you would prefer the old log set this to 'old'

    formatting  -  By default you'll just get a default log but you can set
    this to 'warnings', 'notices', 'errors' to filter by only those error types.
    Notices will return in blue, warnings in gold and errors in red.
    You can use as many of the formatting values as you want, just separate by an
    underscore such as 'warnings_errors'. If using anything other than the
    default in here your log will returned in order of newest log activity first
    (reversed order). You can also use 'clean' as an option and that will just
    return the full log but with clean text formatting and in reverse order.

    sort_order   -  This will only work if you've sent through an argument other
    than 'original' for the formatting. By default the log will be shown in
    'reverse' order but you can set this to 'original' if you prefer ascending
    timestamp ordering like a normal log.

EXAMPLE CODE:
my_log = koding.Grab_Log()
dialog.ok('KODI LOG LOOP','Press OK to see various logging options, every 5 seconds it will show a new log style.')
koding.Text_Box('CURRENT LOG FILE (ORIGINAL)',my_log)
xbmc.sleep(5000)
my_log = koding.Grab_Log(formatting='clean', sort_order='reverse')
koding.Text_Box('CURRENT LOG FILE (clean in reverse order)',my_log)
xbmc.sleep(5000)
my_log = koding.Grab_Log(formatting='errors_warnings', sort_order='reverse')
koding.Text_Box('CURRENT LOG FILE (erros & warnings only - reversed)',my_log)
xbmc.sleep(5000)
old_log = koding.Grab_Log(log_type='old')
koding.Text_Box('OLD LOG FILE',old_log)
~"""
    from filetools import Physical_Path, Text_File
    log_path    = Physical_Path('special://logpath/')
    logfilepath = os.listdir(log_path)
    finalfile   = 0
    for item in logfilepath:
        cont = False
        if item.endswith('.log') and not item.endswith('.old.log') and log_type == 'std':
            mylog        = os.path.join(log_path,item)
            cont = True
        elif item.endswith('.old.log') and log_type == 'old':
            mylog        = os.path.join(log_path,item)
            cont = True
        if cont:
            lastmodified = xbmcvfs.Stat(mylog).st_mtime()
            if lastmodified>finalfile:
                finalfile = lastmodified
                logfile   = mylog
    
    logtext = Text_File(logfile, 'r')

    if formatting != 'original':
        logtext_final = ''

        with open(logfile) as f:
            log_array = f.readlines()
        log_array = [line.strip() for line in log_array]
        
        if sort_order == 'reverse':
            log_array = reversed(log_array)

        for line in log_array:
            if ('warnings' in formatting or 'clean' in formatting) and 'WARNING:' in line:
                logtext_final += line.replace('WARNING:', '[COLOR=gold]WARNING:[/COLOR]')+'\n'
            if ('errors' in formatting or 'clean' in formatting) and 'ERROR:' in line:
                logtext_final += line.replace('ERROR:', '[COLOR=red]ERROR:[/COLOR]')+'\n'
            if ('notices' in formatting or 'clean' in formatting) and 'NOTICE:' in line:
                logtext_final += line.replace('NOTICE:', '[COLOR=dodgerblue]NOTICE:[/COLOR]')+'\n'

        logtext = logtext_final

    return logtext
#----------------------------------------------------------------
# TUTORIAL #
def Last_Error():
    """
Return details of the last error produced, perfect for try/except statements

CODE: Last_Error()

EXAMPLE CODE:
try:
    xbmc.log(this_should_error)
except:
    koding.Text_Box('ERROR MESSAGE',Last_Error())
~"""

    import traceback
    error = traceback.format_exc()
    return error
#----------------------------------------------------------------
# TUTORIAL #
def Network_Settings():
    """
Attempt to open the WiFi/network settings for the current running operating system.

I have no access to any iOS based systems so if anybody wants to add support for
that and you know the working code please contact me at info@totalrevolution.tv
The Linux one is also currently untested and of course there are many different
distros so if you know of any improved code please do pass on. Thank you.

CODE: Network_Settings()

EXAMPLE CODE:
koding.Network_Settings()
~"""
    content = Grab_Log()
    if xbmc.getCondVisibility('System.Platform.Android'):
        xbmc.executebuiltin('StartAndroidActivity(,android.settings.WIFI_SETTINGS)')
    
    elif xbmc.getCondVisibility('System.Platform.OSX'):
        os.system('open /System/Library/PreferencePanes/Network.prefPane/')

    elif xbmc.getCondVisibility('System.Platform.Windows'):
        os.system('ncpa.cpl')

    elif 'Running on OpenELEC' in content or 'Running on LibreELEC' in content:

        if xbmc.getCondVisibility("System.HasAddon(service.openelec.settings)") or xbmc.getCondVisibility("System.HasAddon(service.libreelec.settings)"):
            if xbmc.getCondVisibility("System.HasAddon(service.openelec.settings)"): 
                xbmcaddon.Addon(id='service.openelec.settings').getAddonInfo('name')
                xbmc.executebuiltin('RunAddon(service.openelec.settings)')
            elif xbmc.getCondVisibility("System.HasAddon(service.libreelec.settings)"):
                xbmcaddon.Addon(id='service.libreelec.settings').getAddonInfo('name')
                xbmc.executebuiltin('RunAddon(service.libreelec.settings)')
            xbmc.sleep(1500)
            xbmc.executebuiltin('Control.SetFocus(1000,2)')
            xbmc.sleep(500)
            xbmc.executebuiltin('Control.SetFocus(1200,0)')

    elif xbmc.getCondVisibility('System.Platform.Linux'):
        os.system('nm-connection-editor')
#----------------------------------------------------------------
# TUTORIAL #
def Python_Version():
    """
Return the current version of Python as a string. Very useful if you need
to find out whether or not to return https links (Python 2.6 is not SSL friendly).

CODE: Python_Version()

EXAMPLE CODE:
py_version = koding.Python_Version()
dialog.ok('PYTHON VERSION','You are currently running:','Python v.%s'%py_version)
~"""
    py_version = '%s.%s'%(sys.version_info[0],sys.version_info[1])
    return py_version
#----------------------------------------------------------------
# TUTORIAL #
def Refresh(r_mode=['addons', 'repos'], profile_name='default'):
    """
Refresh a number of items in kodi, choose the order they are
executed in by putting first in your r_mode. For example if you
want to refresh addons then repo and then the profile you would
send through a list in the order you want them to be executed.

CODE: Refresh(r_mode, [profile])

AVAILABLE PARAMS:

    r_mode  -  This is the types of "refresh you want to perform",
    you can send through just one item or a list of items from the
    list below. If you want a sleep between each action just put a
    '~' followed by amount of milliseconds after the r_mode. For example
    r_mode=['addons~3000', 'repos~2000', 'profile']. This would refresh
    the addons, wait 2 seconds then refresh the repos, wait 3 seconds then
    reload the profile. The default is set to do a force refresh on
    addons and repositories - ['addons', 'repos'].
      
       'addons': This will perform the 'UpdateLocalAddons' command.

       'container': This will refresh the contents of the page.

       'profile': This will refresh the current profile or if
       the profile_name param is set it will load that.

       'repos': This will perform the 'UpdateAddonRepos' command.

       'skin': This will perform the 'ReloadSkin' command.

    profile_name -  If you're sending through the option to refresh
    a profile it will reload the current running profile by default
    but you can pass through a profile name here.

EXAMPLE CODE:
dialog.ok('RELOAD SKIN','We will now attempt to update the addons, pause 3s, update repos and pause 2s then reload the skin. Press OK to continue.')
koding.Refresh(r_mode=['addons~3000', 'repos~2000', 'skin'])
xbmc.sleep(2000)
dialog.ok('COMPLETE','Ok that wasn\'t the best test to perform as you can\'t physically see any visible changes other than the skin refreshing so you\'ll just have to trust us that it worked!')
~"""
    from vartools import Data_Type
    if profile_name == 'default':
        profile_name = Current_Profile()

    data_type = Data_Type(r_mode)
    if data_type == 'str':
        r_mode = [r_mode]

    for item in r_mode:
        sleeper = 0
        if '~' in item:
            item, sleeper = item.split('~')
            sleeper = int(sleeper)
        if item =='addons':
            xbmc.executebuiltin('UpdateLocalAddons')
        if item =='repos':
            xbmc.executebuiltin('UpdateAddonRepos')
        if item =='container':
            xbmc.executebuiltin('Container.Refresh')
        if item =='skin':
            xbmc.executebuiltin('ReloadSkin')
        if item =='profile':
            xbmc.executebuiltin('LoadProfile(%s)' % profile_name)
        if sleeper:
            xbmc.sleep(sleeper)
#----------------------------------------------------------------
# TUTORIAL #
def Requirements(dependency):
    """
Return the min and max versions of built-in kodi dependencies required by
the running version of Kodi (xbmc.gui, xbmc.python etc.), The return will
be a dictionary with the keys 'min' and 'max'.

CODE: Requirements(dependency)

AVAILABLE PARAMS:

    (*) dependency  -  This is the dependency you want to check.
    You can check any built-in dependency which has backwards-compatibility
    but the most commonly used are xbmc.gui and xbmc.python.

EXAMPLE CODE:
xbmc_gui = Requirements('xbmc.gui')
xbmc_python = Requirements('xbmc.python')
dialog.ok('DEPENDENCIES','[COLOR=dodgerblue]xbmc.gui[/COLOR]  Min: %s  Max: %s'%(xbmc_gui['min'],xbmc_gui['max']),'[COLOR=dodgerblue]xbmc.python[/COLOR]  Min: %s  Max: %s'%(xbmc_python['min'],xbmc_python['max']))
~"""
    from filetools import Physical_Path,Text_File
    from vartools  import Find_In_Text
    kodi_ver = xbmc.getInfoLabel("System.BuildVersion")[:2]
# Dictionary used for fallback if local file not accessible (AFTV for example)
    defaults = {'15':{'xbmc.gui':['5.3.0','5.9.0'], 'xbmc.python':['2.1.0','2.20.0']}, '16':{'xbmc.gui':['5.10.0','5.10.0'], 'xbmc.python':['2.1.0','2.24.0']}, '17':{'xbmc.gui':['5.12.0','5.12.0'], 'xbmc.python':['2.1.0','2.25.0']}}
    root     = 'special://xbmc/addons'
    dep_path = os.path.join(root,dependency,'addon.xml')
    content  = Text_File(dep_path,'r')
    try:
        max_ver  = Find_In_Text(content=content,start='version="',end='"')[1]
        min_ver  = Find_In_Text(content=content,start='abi="',end='"')[0]
    except:
        xbmc.log(repr(defaults[kodi_ver]),2)
        try:
            max_ver = defaults[kodi_ver][dependency][1]
            min_ver = defaults[kodi_ver][dependency][0]
        except:
            max_ver = 'unknown'
            min_ver = 'unknown'
    xbmc.log('%s min: %s'%(dependency,min_ver),2)
    xbmc.log('%s max: %s'%(dependency,max_ver),2)
    return {'min':min_ver,"max":max_ver}
#----------------------------------------------------------------
# TUTORIAL #
def Running_App():
    """
Return the Kodi app name you're running, useful for fork compatibility

CODE: Running_App()

EXAMPLE CODE:
my_kodi = koding.Running_App()
kodi_ver = xbmc.getInfoLabel("System.BuildVersion")
dialog.ok('KODI VERSION','You are running:','[COLOR=dodgerblue]%s[/COLOR] - v.%s' % (my_kodi, kodi_ver))
~"""
    root_folder = xbmc.translatePath('special://xbmc')
    xbmc.log(root_folder)
    if '/cache' in root_folder:
        root_folder = root_folder.split('/cache')[0]
    root_folder = root_folder.split('/')
    if root_folder[len(root_folder)-1] == '':
        root_folder.pop()
    finalitem   = len(root_folder)-1
    running     = root_folder[finalitem]
    return running
#----------------------------------------------------------------
# TUTORIAL #
def Set_Setting(setting, setting_type='kodi_setting', value = 'true'):
    """
Use this to set built-in kodi settings via JSON or set skin settings.

CODE: Set_Setting(setting, [setting_type, value])

AVAILABLE PARAMS:
    
    setting_type - The type of setting type you want to change. By default
    it's set to 'kodi_setting', see below for more info.

    AVAILALE VALUES:

        'string' : sets a skin string, requires a value.

        'bool_true' :  sets a skin boolean to true, no value required.

        'bool_false' sets a skin boolean to false, no value required.
        
        'kodi_setting' : sets values found in guisettings.xml. Requires
        a string of 'true' or 'false' for the value paramater.
        
        'addon_enable' : enables/disables an addon. Requires a string of
        'true' (enable) or 'false' (disable) as the value. You will get a
        return of True/False on whether successul. Depending on your requirements
        you may prefer to use the Toggle_Addons function.

        'json' : WIP - setitng = method, value = params, see documentation on
        JSON-RPC API here: http://kodi.wiki/view/JSON-RPC_API)

    setting - This is the name of the setting you want to change, it could be a
    setting from the kodi settings or a skin based setting. If you're wanting
    to enable/disable an add-on this is set as the add-on id.

    value: This is the value you want to change the setting to. By default this
    is set to 'true'.


EXAMPLE CODE:
if dialog.yesno('RSS FEEDS','Would you like to enable or disable your RSS feeds?',yeslabel='ENABLE',nolabel='DISABLE'):
    koding.Set_Setting(setting_type='kodi_setting', setting='lookandfeel.enablerssfeeds', value='true')
else:
    koding.Set_Setting(setting_type='kodi_setting', setting='lookandfeel.enablerssfeeds', value='false')
~"""
    try:    import simplejson as json
    except: import json

    try:

# If the setting_type is kodi_setting we run the command to set the relevant values in guisettings.xml
        if setting_type == 'kodi_setting':
            setting = '"%s"' % setting
            value = '"%s"' % value

            query = '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue","params":{"setting":%s,"value":%s}, "id":1}' % (setting, value)
            response = xbmc.executeJSONRPC(query)

            if 'error' in str(response):
                query = '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue","params":{"setting":%s,"value":%s}, "id":1}' % (setting, value.replace('"',''))
                response = xbmc.executeJSONRPC(query)
                if 'error' in str(response):
                    xbmc.log('### Error With Setting: %s' % response, 2)
                    return False
                else:
                    return True
            else:
                return True

# Set a skin string to <value>
        elif setting_type == 'string':
            xbmc.executebuiltin('Skin.SetString(%s,%s)' % (setting, value))

# Set a skin setting to true
        elif setting_type == 'bool_true':
            xbmc.executebuiltin('Skin.SetBool(%s)' % setting)

# Set a skin setting to false
        elif setting_type == 'bool_false':
            xbmc.executebuiltin('Skin.Reset(%s)' % setting)

# If we're enabling/disabling an addon        
        elif setting_type == 'addon_enable':
            if setting != '':
                query = '{"jsonrpc":"2.0", "method":"Addons.SetAddonEnabled","params":{"addonid":"%s", "enabled":%s}, "id":1}' % (setting, value)
                response = xbmc.executeJSONRPC(query)
                if 'error' in str(response):
                    xbmc.log('### Error in json: %s'%query,2)
                    xbmc.log('^ %s' % response, 2)
                    return False
                else:
                    return True

# If it's none of the above then it must be a json command so we use the setting_type as the method in json
        elif setting_type == 'json':
            query = '{"jsonrpc":"2.0", "method":"%s","params":{%s}, "id":1}' % (setting, value)
            response = xbmc.executeJSONRPC(query)
            if 'error' in str(response):
                xbmc.log('### Error With Setting: %s' % response,2)
                return False
            else:
                return True

    except:
        xbmc.log(Last_Error())
#----------------------------------------------------------------    
# TUTORIAL #
def Sleep_If_Function_Active(function, args=[], kill_time=30, show_busy=True):
    """
This will allow you to pause code while a specific function is
running in the background.

CODE: Sleep_If_Function_Active(function, args, kill_time, show_busy)

AVAILABLE PARAMS:

    function  -  This is the function you want to run. This does
    not require brackets, you only need the function name.

    args  -  These are the arguments you want to send through to
    the function, these need to be sent through as a list.

    kill_time - By default this is set to 30. This is the maximum
    time in seconds you want to wait for a response. If the max.
    time is reached before the function completes you will get
    a response of False.

    show_busy - By default this is set to True so you'll get a busy
    working dialog appear while the function is running. Set to
    false if you'd rather not have this.

EXAMPLE CODE:
def Open_Test_URL(url):
    koding.Open_URL(url)

dialog.ok('SLEEP IF FUNCTION ACTIVE','We will now attempt to read a 20MB zip and then give up after 10 seconds.','Press OK to continue.')
koding.Sleep_If_Function_Active(function=Open_Test_URL, args=['http://download.thinkbroadband.com/20MB.zip'], kill_time=10, show_busy=True)
dialog.ok('FUNCTION COMPLETE','Of course we cannot read that file in just 10 seconds so we\'ve given up!')
~"""
    from guitools import Show_Busy
    import threading
    if show_busy:
        Show_Busy(True)
    my_thread = threading.Thread(target=function, args=args)
    my_thread.start()
    thread_alive = True
    counter = 0
    while thread_alive and counter <= kill_time:
        xbmc.sleep(1000)
        thread_alive = my_thread.isAlive()
        counter += 1
    if show_busy:
        Show_Busy(False)
    return thread_alive
#----------------------------------------------------------------    
# TUTORIAL #
def Sleep_If_Window_Active(window_type=10147):
    """
This will allow you to pause code while a specific window is open.

CODE: Sleep_If_Window_Active(window_type)

AVAILABLE PARAMS:

    window_type  -  This is the window xml name you want to check for, if it's
    active then the code will sleep until it becomes inactive. By default this
    is set to the custom text box (10147). You can find a list of window ID's
    here: http://kodi.wiki/view/Window_IDs

EXAMPLE CODE:
koding.Text_Box('EXAMPLE TEXT','This is just an example, normally a text box would not pause code and the next command would automatically run immediately over the top of this.')
koding.Sleep_If_Window_Active(10147) # This is the window id for the text box
dialog.ok('WINDOW CLOSED','The window has now been closed so this dialog code has now been initiated')
~"""
    from __init__ import dolog
    windowactive = False
    counter      = 0

    if window_type == 'yesnodialog' or window_type == 10100:
        count = 30
    else:
        count = 10
    
    okwindow = False

# Do not get stuck in an infinite loop. Check x amount of times and if condition isn't met after x amount it quits
    while not okwindow and counter < count:
        xbmc.sleep(100)
        okwindow = xbmc.getCondVisibility('Window.IsActive(%s)' % window_type)
        counter += 1

# Window is active
    while okwindow:
        okwindow = xbmc.getCondVisibility('Window.IsActive(%s)' % window_type)
        xbmc.sleep(250)

    return okwindow
#----------------------------------------------------------------
# TUTORIAL #
def System(command, function=''):
    """
This is just a simplified method of grabbing certain Kodi infolabels, paths
and booleans as well as performing some basic built in kodi functions.
We have a number of regularly used functions added to a dictionary which can
quickly be called via this function or you can use this function to easily
run a command not currently in the dictionary. Just use one of the
many infolabels, builtin commands or conditional visibilities available:

info: http://kodi.wiki/view/InfoLabels
bool: http://kodi.wiki/view/List_of_boolean_conditions

CODE: System(command, [function])

AVAILABLE PARAMS:
    
    (*) command  -  This is the command you want to perform, below is a list
    of all the default commands you can choose from, however you can of course
    send through your own custom command if using the function option (details
    at bottom of page)

    AVAILABLE VALUES:

        'addonid'       : Returns the FOLDER id of the current add-on. Please note could differ from real add-on id.
        'addonname'     : Returns the current name of the add-on
        'builddate'     : Return the build date for the current running version of Kodi
        'cpu'           : Returns the CPU usage as a percentage
        'cputemp'       : Returns the CPU temperature in farenheit or celcius depending on system settings
        'currentlabel'  : Returns the current label of the item in focus
        'currenticon'   : Returns the name of the current icon
        'currentpos'    : Returns the current list position of focused item
        'currentpath'   : Returns the url called by Kodi for the focused item
        'currentrepo'   : Returns the repo of the current focused item
        'currentskin'   : Returns the FOLDER id of the skin. Please note could differ from actual add-on id
        'date'          : Returns the date (Tuesday, April 11, 2017)
        'debug'         : Toggles debug mode on/off
        'freeram'       : Returns the amount of free memory available (in MB)
        'freespace'     : Returns amount of free space on storage in this format: 10848 MB Free
        'hibernate'     : Hibernate system, please note not all systems are capable of waking from hibernation
        'internetstate' : Returns True or False on whether device is connected to internet
        'ip'            : Return the current LOCAL IP address (not your public IP)
        'kernel'        : Return details of the system kernel
        'language'      : Return the language currently in use
        'mac'           : Return the mac address, will only return the mac currently in use (Wi-Fi OR ethernet, not both)
        'numitems'      : Return the total amount of list items curently in focus
        'profile'       : Return the currently running profile name
        'quit'          : Quit Kodi
        'reboot'        : Reboot the system
        'restart'       : Restart Kodi (Windows/Linux only)
        'shutdown'      : Shutdown the system
        'sortmethod'    : Return the current list sort method
        'sortorder'     : Return the current list sort order
        'systemname'    : Return a clean friendly name for the system
        'time'          : Return the current time in this format: 2:05 PM
        'usedspace'     : Return the amount of used space on the storage in this format: 74982 MB Used
        'version'       : Return the current version of Kodi, this may need cleaning up as it contains full file details
        'viewmode'      : Return the current list viewmode
        'weatheraddon'  : Return the current plugin being used for weather


    function  -  This is optional and default is set to a blank string which will
    allow you to use the commands listed above but if set you can use your own
    custom commands by setting this to one of the values below.

    AVAILABLE VALUES:

        'bool' : This will allow you to send through a xbmc.getCondVisibility() command
        'info' : This will allow you to send through a xbmc.getInfoLabel() command
        'exec' : This will allow you to send through a xbmc.executebuiltin() command

EXAMPLE CODE:
current_time = koding.System(command='time')
current_label = koding.System(command='currentlabel')
is_folder = koding.System(command='ListItem.IsFolder', function='bool')
dialog.ok('PULLED DETAILS','The current time is %s' % current_time, 'Folder status of list item [COLOR=dodgerblue]%s[/COLOR]: %s' % (current_label, is_folder),'^ A zero means False, as in it\'s not a folder.')
~"""
    params = {
    'addonid'       :'xbmc.getInfoLabel("Container.PluginName")',
    'addonname'     :'xbmc.getInfoLabel("Container.FolderName")',
    'builddate'     :'xbmc.getInfoLabel("System.BuildDate")',
    'cpu'           :'xbmc.getInfoLabel("System.CpuUsage")',
    'cputemp'       :'xbmc.getInfoLabel("System.CPUTemperature")',
    'currentlabel'  :'xbmc.getInfoLabel("System.CurrentControl")',
    'currenticon'   :'xbmc.getInfoLabel("ListItem.Icon")',
    'currentpos'    :'xbmc.getInfoLabel("Container.CurrentItem")',
    'currentpath'   :'xbmc.getInfoLabel("Container.FolderPath")',
    'currentrepo'   :'xbmc.getInfoLabel("Container.Property(reponame)")',
    'currentskin'   :'xbmc.getSkinDir()',
    'date'          :'xbmc.getInfoLabel("System.Date")',
    'debug'         :'xbmc.executebuiltin("ToggleDebug")',
    'freeram'       :'xbmc.getFreeMem()',
    'freespace'     :'xbmc.getInfoLabel("System.FreeSpace")',
    'hibernate'     :'xbmc.executebuiltin("Hibernate")',
    'internetstate' :'xbmc.getInfoLabel("System.InternetState")',
    'ip'            :'xbmc.getIPAddress()',
    'kernel'        :'xbmc.getInfoLabel("System.KernelVersion")',
    'language'      :'xbmc.getInfoLabel("System.Language")',
    'mac'           :'xbmc.getInfoLabel("Network.MacAddress")',
    'numitems'      :'xbmc.getInfoLabel("Container.NumItems")',
    'profile'       :'xbmc.getInfoLabel("System.ProfileName")',
    'quit'          :'xbmc.executebuiltin("Quit")',
    'reboot'        :'xbmc.executebuiltin("Reboot")',
    'restart'       :'xbmc.restart()', # Windows/Linux only
    'shutdown'      :'xbmc.shutdown()',
    'sortmethod'    :'xbmc.getInfoLabel("Container.SortMethod")',
    'sortorder'     :'xbmc.getInfoLabel("Container.SortOrder")',
    'systemname'    :'xbmc.getInfoLabel("System.FriendlyName")',
    'time'          :'xbmc.getInfoLabel("System.Time")',
    'usedspace'     :'xbmc.getInfoLabel("System.UsedSpace")',
    'version'       :'xbmc.getInfoLabel("System.BuildVersion")',
    'viewmode'      :'xbmc.getInfoLabel("Container.Viewmode")',
    'weatheraddon'  :'xbmc.getInfoLabel("Weather.plugin")',
    }

    if function == '': newcommand = params[command]
    elif function == 'info': newcommand = 'xbmc.getInfoLabel("%s")' % command
    elif function == 'bool': newcommand = 'xbmc.getCondVisibility("%s")' % command
    elif function == 'exec': newcommand = 'xbmc.getCondVisibility("%s")' % command
    else:
        dialog.ok('INCORRECT PARAMS','The following command has been called:','koding.System(%s,[COLOR=dodgerblue]%s[/COLOR])'%(command, function),'^ The wrong function has been sent through, please double check the section highlighted in blue.')

    try:
        return eval(newcommand)
    except:
        return 'error'
#----------------------------------------------------------------
# TUTORIAL #
def Timestamp(mode = 'integer'):
    """
This will return the timestamp in various formats. By default it returns as "integer" mode but other options are listed below:

CODE: Timestamp(mode)
mode is optional, by default it's set as integer

AVAILABLE VALUES:

    'integer' -  An integer which is nice and easy to work with in Python (especially for
    finding out human readable diffs). The format returned is [year][month][day][hour][minutes][seconds]. 
    
    'epoch'   -  Unix Epoch format (calculated in seconds passed since 12:00 1st Jan 1970).

    'clean'   -  A clean user friendly time format: Tue Jan 13 10:17:09 2009

    'date_time' -  A clean interger style date with time at end: 2017-04-07 10:17:09

EXAMPLE CODE:
integer_time = koding.Timestamp('integer')
epoch_time = koding.Timestamp('epoch')
clean_time = koding.Timestamp('clean')
date_time = koding.Timestamp('date_time')
import datetime
installedtime = str(datetime.datetime.now())[:-7]
dialog.ok('CURRENT TIME','Integer: %s' % integer_time, 'Epoch: %s' % epoch_time, 'Clean: %s' % clean_time)
~"""
    import time
    import datetime

    now = time.time()
    try:
        localtime = time.localtime(now)
    except:
        localtime = str(datetime.datetime.now())[:-7]
        localtime = localtime.replace('-','').replace(':','')
    if mode == 'date_time':
        return time.strftime('%Y-%m-%d %H:%M:%S', localtime)
    if mode == 'integer':
        return time.strftime('%Y%m%d%H%M%S', localtime)

    if mode == 'clean':
        return time.asctime(localtime)

    if mode == 'epoch':
        return now
#----------------------------------------------------------------