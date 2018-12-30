#!/usr/bin/python 
import xbmcaddon
import xbmcgui
import xbmc
import urllib, os, re, urllib2
import sys
import time
addon       = xbmcaddon.Addon()
addonname   = addon.getAddonInfo('name')


videoDir = addon.getSetting("videoDir")


line99 = "Please set Download Directory in Settings"
line100 = "Read Description"
line101 = "Download folder set to " + (videoDir)       
xbmcgui.Dialog().ok(addonname, line99, line100, line101)
xbmcaddon.Addon(id='plugin.program.pythonzipdownloader').openSettings()
           
line1 = "Please set Download URL."
line2 = "Google, GitHub, DropBox(public or private)...etc."
line3 = "USE AT OWN RISK...ENJOY!!"

xbmcgui.Dialog().ok(addonname, line1, line2, line3)


keyboard    = xbmc.Keyboard()
#keyboard.setHiddenInput(hidden)
keyboard.setHeading('ENTER URL')
keyboard.doModal()
       
if keyboard.isConfirmed():
    result = keyboard.getText()
    
line4 = "URL set..DOWNLOAD what we want here. Zip's and more.."
line5 = "**** ENTER WHAT YOU WANT THE FILE NAME and EXTENSION TO BE ****"
line6 = "EXAMPLE:   myzipfile.zip"

xbmcgui.Dialog().ok(addonname, line4, line5, line6)
keyboard2    = xbmc.Keyboard()
keyboard2.setHeading('SAVE FILE AS')
keyboard2.doModal()
if keyboard2.isConfirmed():
    result2 = keyboard2.getText()
    
    
dest = videoDir + result2
url = result
percent = 0
def DownloaderClass(url,dest):
    dp = xbmcgui.DialogProgress()
    dp.create("PYTHON ZIP DOWNLOADER","Downloading File",url)
    urllib.urlretrieve(url,dest,lambda nb, bs, fs, url=url: _pbhook(nb,bs,fs,url,dp))
 
def _pbhook(numblocks, blocksize, filesize, url=None,dp=None):
    try:
        percent = min((numblocks*blocksize*100)/filesize, 100)
        dp.update(percent)
    except: 
        percent = 100
        dp.update(percent)
        time.sleep(20)
        dp.close()
    if dp.iscanceled(): 
        dp.close()
        
DownloaderClass(url,dest)




line7 = "File DOWNLOADED....."
line8 = "Saved as " + (result2)

xbmcgui.Dialog().ok(addonname, line7, line8)



