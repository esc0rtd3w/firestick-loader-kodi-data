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

import xbmc
import subprocess
#----------------------------------------------------------------
# TUTORIAL #
def App_Settings(apk_id):
    """
Open up the settings for an installed Android app.

CODE: App_Settings(apk_id)

AVAILABLE PARAMS:

    (*) apk_id  -  The id of the app you want to open the settings for.

EXAMPLE CODE:
my_apps = koding.My_Apps()
choice = dialog.select('CHOOSE AN APK', my_apps)
koding.App_Settings(apk_id=my_apps[choice])
~"""
    xbmc.executebuiltin('StartAndroidActivity("","android.settings.APPLICATION_DETAILS_SETTINGS","","package:%s")' % apk_id)
#----------------------------------------------------------------
# TUTORIAL #
def My_Apps():
    """
Return a list of apk id's installed on system

CODE: My_Apps()

EXAMPLE CODE:
my_apps = koding.My_Apps()
choice = dialog.select('CHOOSE AN APK', my_apps)
if choice >= 0:
    koding.App_Settings(apk_id=my_apps[choice])
~"""
    Installed_APK = []
    if xbmc.getCondVisibility('system.platform.android'):
        try:
            Installed_APK = subprocess.Popen(['exec ''/system/bin/pm list packages -3'''], executable='/system/bin/sh', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].rstrip('\n').splitlines()
        except Exception as e:
            xbmc.log('Failed to grab installed app details: %s' % e)
            Installed_APK = []

        for i in range(len(Installed_APK)):
            Installed_APK[i] = Installed_APK[i].partition(':')[2]

    return Installed_APK
#----------------------------------------------------------------
# TUTORIAL #
def Start_App(apk_id):
    """
Open an Android application

CODE: Start_App(apk_id)

AVAILABLE PARAMS:

    (*) apk_id  -  The id of the app you want to open.

EXAMPLE CODE:
dialog.ok('OPEN FACEBOOK','Presuming you have Facebook installed and this is an Android system we will now open that apk')
koding.Start_App(apk_id='com.facebook.katana')
~"""
    xbmc.executebuiltin('StartAndroidActivity(%s)' % apk_id)
#----------------------------------------------------------------
# TUTORIAL #
def Uninstall_APK(apk_id):
    """
Uninstall and Android app

CODE: Uninstall_APK(apk_id)

EXAMPLE CODE:
if dialog.yesno('UNINSTALL FACEBOOK','Would you like to uninstall the Facebook app from your system?'):
    koding.Uninstall_APK(apk_id='com.facebook.katana')
~"""
    xbmc.executebuiltin('StartAndroidActivity("","android.intent.action.DELETE","","package:%s")' % apk_id)
#----------------------------------------------------------------