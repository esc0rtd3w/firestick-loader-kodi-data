import urllib
import os
import time
import xbmcgui
import xbmc
import xbmcaddon
    
packages_path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
addons_path = xbmc.translatePath('special://home/addons')

filesize_of_file_being_downloaded = 0

def handleRemoveReadonly(func, path, exc_info):
    import stat
    if not os.access(path, os.W_OK):
        # Is the error an access error ?
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise

def calculate_progress_precent(step, total_steps):
    return (100/total_steps) * step
    
def download(url, dest, dp, percent, pline1="", pline2=""):

    global filesize_of_file_being_downloaded
    filesize_of_file_being_downloaded = 0
    
    start_time=time.time()
    urllib.urlretrieve(url, dest, lambda nb, bs, fs: _pbhook(nb, bs, fs, dp, start_time, percent, pline1, pline2))
     
def _pbhook(numblocks, blocksize, filesize, dp, start_time, percent, pline1, pline2):
    
    global filesize_of_file_being_downloaded
    filesize_of_file_being_downloaded = filesize
    
    try: 
        #percent = min(numblocks * blocksize * 100 / filesize, 100) 
        currently_downloaded_bytes = float(numblocks) * blocksize
        currently_downloaded_kbs = currently_downloaded_bytes / 1024 
        currently_downloaded = currently_downloaded_bytes / (1024 * 1024) 
        Bps_speed = currently_downloaded_bytes / (time.time() - start_time) 
        if Bps_speed > 0:                                                 
            eta = (filesize - numblocks * blocksize) / Bps_speed 
            if Bps_speed > max_Bps: max_Bps = Bps_speed
        else: 
            eta = 0 
        
        kbps_speed = Bps_speed * 8 / 1024 
        mbps_speed = kbps_speed / 1024 
        
        total_kbs = float(filesize) / 1024 
        total = float(filesize) / (1024 * 1024) 
        currently_downloaded = currently_downloaded_bytes / (1024 * 1024) 
        
        Bps_speed = currently_downloaded_bytes / (time.time() - start_time) 
        if Bps_speed > 0:                                                 
            eta = (filesize - numblocks * blocksize) / Bps_speed         
        speedstr = 'Speed: %.02f Mb/s ' % mbps_speed 
        etastr = 'ETA: %02d:%02d' % divmod(eta, 60) 
        mbs = '[I][COLOR gray]%.02f MB of %.02f MB - %s[/COLOR][/I]' % (currently_downloaded, total, etastr) 
        dp.update(percent, pline1, pline2, mbs)
    except: 
        #percent = 100 
        dp.update(percent) 

def UnInstall(extn):
    # Uninstall Steps
    extn_id = extn['extn_id']
    extn_version = extn['extn_version']
    extn_name = extn['extn_name']
    extn_provider = extn['extn_provider']
    extn_zip = extn['extn_zip']
    extn_icon = extn['extn_icon']
    extn_fanart = extn['extn_fanart']
    extn_summary = extn['extn_summary']
    extn_desc = extn['extn_desc']
    extn_repo_id = extn['extn_repo_id']
    extn_repo_version = extn['extn_repo_version']
    extn_repo_zip = extn['extn_repo_zip']
    
    pline1 = "[B]Uninstall: [COLOR gold]%s[/COLOR][/B]" % extn_name
    pline2 = ""
    pline3 = " "
    
    pDialog = xbmcgui.DialogProgress()
    ret = pDialog.create("iStream Extension Store", pline1, pline2, pline3 )
    
    # get window progress
    WINDOW_PROGRESS = xbmcgui.Window( 10101 )
    # give window time to initialize
    xbmc.sleep( 100 )
    
    try:
        # get our cancel button
        CANCEL_BUTTON = WINDOW_PROGRESS.getControl( 10 )
        # desable button (bool - True=enabled / False=disabled.)
        CANCEL_BUTTON.setEnabled( False )
    except:
        pass
    
    current_step=-1
    total_steps=4
    
    #STEP: Check if extn repo is already installed
    current_step+=1
    percent = calculate_progress_precent(current_step, total_steps)
    pline2 = "Uninstalling..."
    pDialog.update(percent, pline1, pline2, pline3)
    
    install_loc = os.path.join(addons_path, extn_id)        
    if os.path.exists(install_loc):
        try:            
            import shutil    
            shutil.rmtree(install_loc, onerror=handleRemoveReadonly)
            current_step+=1
            percent = calculate_progress_precent(current_step, total_steps)
            pDialog.update(percent, pline1, pline2, pline3)
        except Exception, e:
            pline3 = "[I][COLOR red]ERROR: Uninstallation failed, check logs.[/COLOR][/I]"
            pDialog.update(100, pline1, pline2, pline3)
            xbmc.sleep(2000)
            CANCEL_BUTTON.setEnabled( True )
            pDialog.close()
            xbmc.log(msg=str(e), level=xbmc.LOGERROR)
            return
            
    xbmc.executebuiltin('UpdateLocalAddons')
    uninstall_validated=False
    while uninstall_validated == False:
        try:
            xbmcaddon.Addon(extn_id)
            uninstall_validated=False
            if not os.path.exists(install_loc):
                uninstall_validated=True
        except:
            uninstall_validated=True
        xbmc.sleep(250)
        
    pline2 = "[COLOR green]Extension uninstalled successfully.[/COLOR]"
    pline3 = " "
    percent = 100
    pDialog.update(percent, pline1, pline2, pline3)
    
    xbmc.sleep(2000)
    
    try:
        # enable button
        CANCEL_BUTTON.setEnabled( True )
    except:
        pass
    
    pDialog.close()
        
def Install(extn):
    # Installation Steps
    extn_id = extn['extn_id']
    extn_version = extn['extn_version']
    extn_name = extn['extn_name']
    extn_provider = extn['extn_provider']
    extn_zip = extn['extn_zip']
    extn_icon = extn['extn_icon']
    extn_fanart = extn['extn_fanart']
    extn_summary = extn['extn_summary']
    extn_desc = extn['extn_desc']
    extn_repo_id = extn['extn_repo_id']
    extn_repo_version = extn['extn_repo_version']
    extn_repo_zip = extn['extn_repo_zip']
    
    pline1 = "[B]Install: [COLOR gold]%s[/COLOR][/B]" % extn_name
    pline2 = ""
    pline3 = " "
    
    pDialog = xbmcgui.DialogProgress()
    ret = pDialog.create("iStream Extension Store", pline1, pline2, pline3 )
    
    # get window progress
    WINDOW_PROGRESS = xbmcgui.Window( 10101 )
    # give window time to initialize
    xbmc.sleep( 100 )
    try:
        # get our cancel button    
        CANCEL_BUTTON = WINDOW_PROGRESS.getControl( 10 )
        # desable button (bool - True=enabled / False=disabled.)
        CANCEL_BUTTON.setEnabled( False )
    except:
        pass
    
    current_step=-1
    total_steps=23
    
    #STEP: Check if extn repo is already installed
    current_step+=1
    percent = calculate_progress_precent(current_step, total_steps)
    pline2 = "Verifying repository..."
    pDialog.update(percent, pline1, pline2, pline3)
    try:
        xbmcaddon.Addon(extn_repo_id)
        pline3 = "[I][COLOR gray]Repository exists[/COLOR][/I]"
        repo_exists = True
        current_step+=10
    except:        
        pline3 = "[I][COLOR gray]Repository does not exist[/COLOR][/I]"
        repo_exists = False
        current_step+=1
                
    percent = calculate_progress_precent(current_step, total_steps)
    pDialog.update(percent, pline1, pline2, pline3)
    
    if repo_exists == False:
        current_step+=1
        pline2="Downloading repository..."
        pline3=""
        pDialog.update(percent, pline1, pline2, pline3)
        
        extn_repo_download_dest=os.path.join(packages_path, '%s-%s.zip'%(extn_repo_id, extn_repo_version))
        try:
           os.remove(extn_repo_download_dest)
        except:
           pass
        
        download(extn_repo_zip, extn_repo_download_dest, pDialog, percent, pline1, pline2)
        
        try:
            downloaded_filesize = os.path.getsize(extn_repo_download_dest)
        except:
            downloaded_filesize = 0
        
        if filesize_of_file_being_downloaded != downloaded_filesize:
            pline3 = "[I][COLOR red]ERROR: Repository download corrupt/failed, try again later.[/COLOR][/I]"
            pDialog.update(100, pline1, pline2, pline3)
            xbmc.sleep(2000)
            CANCEL_BUTTON.setEnabled( True )
            pDialog.close()
            return
        
        pline3 = "[I][COLOR gray]Repository download complete[/COLOR][/I]"
        current_step+=1
        percent = calculate_progress_precent(current_step, total_steps)
        pDialog.update(percent, pline1, pline2, pline3)
        
        pline2 = "Installing repository..."
        pline3 = " "
        current_step+=1
        percent = calculate_progress_precent(current_step, total_steps)
        pDialog.update(percent, pline1, pline2, pline3)
        
        install_loc = os.path.join(addons_path, extn_repo_id)        
        if os.path.exists(install_loc):
            try:            
                import shutil    
                shutil.rmtree(install_loc, onerror=handleRemoveReadonly)
                current_step+=1
                percent = calculate_progress_precent(current_step, total_steps)
                pDialog.update(percent, pline1, pline2, pline3)
            except Exception, e:
                pline3 = "[I][COLOR red]ERROR: Repository installation failed, check logs.[/COLOR][/I]"
                pDialog.update(100, pline1, pline2, pline3)
                xbmc.sleep(2000)
                CANCEL_BUTTON.setEnabled( True )
                pDialog.close()
                xbmc.log(msg=str(e), level=xbmc.LOGERROR)
                return
            
        import zipfile
        zin = zipfile.ZipFile(extn_repo_download_dest,  'r')
        nFiles = float(len(zin.infolist()))
        count  = 0
        try:
            zip_step=0
            for item in zin.infolist():
                count += 1
                update = count / nFiles * 100
                if update>=20 and zip_step==0: 
                    current_step+=1
                    percent = calculate_progress_precent(current_step, total_steps)
                    pDialog.update(percent, pline1, pline2, pline3)
                    zip_step=1
                elif update>=40 and zip_step==1: 
                    current_step+=1
                    percent = calculate_progress_precent(current_step, total_steps)
                    pDialog.update(percent, pline1, pline2, pline3)
                    zip_step=2
                elif update>=60 and zip_step==2: 
                    current_step+=1
                    percent = calculate_progress_precent(current_step, total_steps)
                    pDialog.update(percent, pline1, pline2, pline3)
                    zip_step=3
                elif update>=80 and zip_step==3: 
                    current_step+=1
                    percent = calculate_progress_precent(current_step, total_steps)
                    pDialog.update(percent, pline1, pline2, pline3)
                    zip_step=4
                
                zin.extract(item, addons_path)
                
            current_step+=1
            percent = calculate_progress_precent(current_step, total_steps)
            pline3 = "[I][COLOR gray]Repository install complete[/COLOR][/I]"
            pDialog.update(percent, pline1, pline2, pline3)
        except Exception, e:
            pline3 = "[I][COLOR red]ERROR: Repository installation failed, check logs.[/COLOR][/I]"
            pDialog.update(100, pline1, pline2, pline3)
            xbmc.sleep(2000)
            CANCEL_BUTTON.setEnabled( True )
            pDialog.close()
            xbmc.log(msg=str(e), level=xbmc.LOGERROR)
            return

        pline2 = "Validating repository..."
        pline3 = " "
        current_step+=1
        percent = calculate_progress_precent(current_step, total_steps)
        pDialog.update(percent, pline1, pline2, pline3)
        
        xbmc.executebuiltin('UpdateLocalAddons')
        install_validated=False
        while install_validated == False:
            try:
                xbmcaddon.Addon(extn_repo_id)
                install_validated=True
            except:
                install_validated=False        
            xbmc.sleep(250)
            
        pline2 = "[COLOR green]Repository installed and validated.[/COLOR]"
        pline3 = " "
        current_step+=1
        percent = calculate_progress_precent(current_step, total_steps)
        pDialog.update(percent, pline1, pline2, pline3)
        
    pline2 = "Downloading..."
    pline3 = " "
    current_step+=1
    percent = calculate_progress_precent(current_step, total_steps)
    pDialog.update(percent, pline1, pline2, pline3)
    
    extn_download_dest=os.path.join(packages_path, '%s-%s.zip'%(extn_id, extn_version))
    try:
       os.remove(extn_download_dest)
    except:
       pass
    
    download(extn_zip, extn_download_dest, pDialog, percent, pline1, pline2)
    
    try:
        downloaded_filesize = os.path.getsize(extn_download_dest)
    except:
        downloaded_filesize = 0
    
    if filesize_of_file_being_downloaded != downloaded_filesize:
        # enable button
        pline3 = "[I][COLOR red]ERROR: Download corrupt/failed, try again later.[/COLOR][/I]"
        pDialog.update(100, pline1, pline2, pline3)
        xbmc.sleep(2000)
        CANCEL_BUTTON.setEnabled( True )
        pDialog.close()
        return
    
    pline3 = "[I][COLOR gray]Download complete[/COLOR][/I]"
    current_step+=1
    percent = calculate_progress_precent(current_step, total_steps)
    pDialog.update(percent, pline1, pline2, pline3)
    
    pline2 = "Installing..."
    pline3 = " "
    current_step+=1
    percent = calculate_progress_precent(current_step, total_steps)
    pDialog.update(percent, pline1, pline2, pline3)
    
    install_loc = os.path.join(addons_path, extn_id)        
    if os.path.exists(install_loc):
        try:            
            import shutil    
            shutil.rmtree(install_loc, onerror=handleRemoveReadonly)
            current_step+=1
            percent = calculate_progress_precent(current_step, total_steps)
            pDialog.update(percent, pline1, pline2, pline3)
        except Exception, e:
            pline3 = "[I][COLOR red]ERROR: Installation failed, check logs.[/COLOR][/I]"
            pDialog.update(100, pline1, pline2, pline3)
            xbmc.sleep(2000)
            CANCEL_BUTTON.setEnabled( True )
            pDialog.close()
            xbmc.log(msg=str(e), level=xbmc.LOGERROR)
            return
        
    import zipfile
    zin = zipfile.ZipFile(extn_download_dest,  'r')
    nFiles = float(len(zin.infolist()))
    count  = 0
    try:
        zip_step=0
        for item in zin.infolist():
            count += 1
            update = count / nFiles * 100
            if update>=20 and zip_step==0: 
                current_step+=1
                percent = calculate_progress_precent(current_step, total_steps)
                pDialog.update(percent, pline1, pline2, pline3)
                zip_step=1
            elif update>=40 and zip_step==1: 
                current_step+=1
                percent = calculate_progress_precent(current_step, total_steps)
                pDialog.update(percent, pline1, pline2, pline3)
                zip_step=2
            elif update>=60 and zip_step==2: 
                current_step+=1
                percent = calculate_progress_precent(current_step, total_steps)
                pDialog.update(percent, pline1, pline2, pline3)
                zip_step=3
            elif update>=80 and zip_step==3: 
                current_step+=1
                percent = calculate_progress_precent(current_step, total_steps)
                pDialog.update(percent, pline1, pline2, pline3)
                zip_step=4
            
            zin.extract(item, addons_path)
            
        current_step+=1
        percent = calculate_progress_precent(current_step, total_steps)
        pline3 = "[I][COLOR gray]Install complete[/COLOR][/I]"
        pDialog.update(percent, pline1, pline2, pline3)
    except Exception, e:
        pline3 = "[I][COLOR red]ERROR: Installation failed, check logs.[/COLOR][/I]"
        pDialog.update(100, pline1, pline2, pline3)
        xbmc.sleep(2000)
        CANCEL_BUTTON.setEnabled( True )
        pDialog.close()
        xbmc.log(msg=str(e), level=xbmc.LOGERROR)
        return

    pline2 = "Validating..."
    pline3 = " "
    current_step+=1
    percent = calculate_progress_precent(current_step, total_steps)
    pDialog.update(percent, pline1, pline2, pline3)
    
    xbmc.executebuiltin('UpdateLocalAddons')
    install_validated=False
    while install_validated == False:
        try:
            xbmcaddon.Addon(extn_id)
            install_validated=True
        except:
            install_validated=False        
        xbmc.sleep(250)
        
    pline2 = "[COLOR green]Extension installed and validated successfully.[/COLOR]"
    pline3 = " "
    percent = 100
    pDialog.update(percent, pline1, pline2, pline3)
    
    xbmc.sleep(2000)
    
    try:
        # enable button
        CANCEL_BUTTON.setEnabled( True )
    except:
        pass
    
    pDialog.close()
    print 'Update Repo'
    xbmc.executebuiltin("UpdateAddonRepos")
    from addon import Addon

    addon_id = 'script.icechannel'

    try:
        addon = Addon(addon_id, sys.argv)
    except:
        addon = Addon(addon_id)

    addon_path = addon.get_path()
    lib_path = os.path.join(addon_path, 'lib', 'entertainment')
    plugins_path = os.path.join(lib_path, 'plugins')
    settings_file = os.path.join(addon_path, 'resources', 'settings.xml')
        
    plugin_dirs = [plugins_path]
    from glob import glob
    plugin_dirs.extend( glob( os.path.join( os.path.dirname(addon_path), addon_id + '.extn.*', 'plugins' ) ) )
    

    
    
    plugins_dict = {}
    plugin_dirs_dict = {}
    
    filecodes = ['_xstrc','_xstrs','_tls','_prx','_wpx','_hrv','_prv','_chr','_lrv','_ffm','_cst','_ist','_lsi','_mvi','_tvi','_ltvi','_lspi','_mvs','_tvs','_ltvs','_lsps']
    
    i = 1
    found = 0
    for plugin_dir in plugin_dirs:
        for dirpath, dirnames, files in os.walk(plugin_dir):
            for f in files:
                if f.endswith('.py'):
                    for filecode in filecodes:
                        if filecode in f: 
                            found+=1
                            dirlist = plugin_dirs_dict.get(filecode, None)
                            if dirlist:
                                dirlist.append(dirpath)
                            else:
                                newdirlist = []
                                newdirlist.append(dirpath)
                                plugin_dirs_dict.update( { filecode:newdirlist } )
                                
                            plgnlist = plugins_dict.get(filecode, None)
                            if plgnlist:
                                plgnlist.append(f[:-3])
                            else:
                                newplgnlist = []
                                newplgnlist.append(f[:-3])
                                plugins_dict.update( { filecode:newplgnlist } )

    addon.set_setting( "plugins_dirs", ','.join(plugin_dirs) )
    
    for k, v in plugin_dirs_dict.iteritems():
        addon.set_setting( "plugins_dirs"+k, ','.join(v) )
        
    for k, v in plugins_dict.iteritems():
        addon.set_setting( "plugins"+k, ','.join(v) )
         
    if xbmc.getCondVisibility('system.platform.linux'):
        if not xbmc.getInfoLabel("Skin.HasSetting(extInstaller)"):
            xbmc.executebuiltin('Skin.SetBool(extInstaller)')
            dialog = xbmcgui.Dialog()
            dialog.ok('iStream Extension Installer', "Your System Will Now Reboot To Take Effect", "")
            os.system('reboot')
