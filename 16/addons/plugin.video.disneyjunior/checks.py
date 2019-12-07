import xbmc,os,shutil


xunityrepo = xbmc.translatePath(os.path.join('special://home/addons', 'repository.xunitytalk'))

theone = xbmc.translatePath(os.path.join('special://home/addons', 'repository.the-one'))

mikey1234 = xbmc.translatePath(os.path.join('special://home/addons', 'repository.mikey1234'))

def deleteold(name): 
        addonfolder = xbmc.translatePath(os.path.join('special://home/addons', ''))
        path=os.path.join(addonfolder, name)
        for root, dirs, files in os.walk(path):
           for f in files:
                os.unlink(os.path.join(root, f))
           for d in dirs:
                shutil.rmtree(os.path.join(root, d))
        try:
            os.rmdir(path)
        except:
            pass



if os.path.exists(xunityrepo) == True:
    
    if os.path.exists(theone) == True:

        deleteold('repository.the-one')
        
    if os.path.exists(mikey1234) == True:
        
        deleteold('repository.mikey1234')


