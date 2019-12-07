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
import shutil
import os
import sys
import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs

from systemtools    import Last_Error
from xml.etree      import ElementTree

dp       = xbmcgui.DialogProgress()
dialog   = xbmcgui.Dialog()
HOME     = 'special://home'
PROFILE  = 'special://profile'
DATABASE = os.path.join(PROFILE,'Database')

#----------------------------------------------------------------    
# TUTORIAL #
class xml(object):
    """
SETTINGS - CREATE CUSTOM ADD-ON SETTINGS:
All credit goes to OptimusGREEN for this module.

This will create a new settings file for your add-on which you can read and write to. This is separate
to the standard settings.xml and you can call the file whatever you want, however you would presumably
call it something other than settings.xml as that is already used by Kodi add-ons.

CODE:  XML(path)

AVAILABLE CLASSES:

ParseValue  -  This class will allow you to get the value of an item in these custom settings.

SetValue  -  This class allows you to set a value to the custom settings. If the settings.xml doesn't exist it will be automatically created so long as the path given in XML is writeable.


EXAMPLE CODE:
myXmlFile = "special://userdata/addon_data/script.module.python.koding.aio/timefile.xml"
timefile = koding.xml(myXmlFile)
getSetting = timefile.ParseValue
setSetting = timefile.SetValue
dialog.ok('CHECK SETTINGS','If you take a look in the addon_data folder for python koding a new file called timefile.xml will be created when you click OK.')
setSetting("autorun", "true")
autoRun = getSetting("autorun")
dialog.ok('AUTORUN VALUE','The value of autorun in these new settings is [COLOR dodgerblue]%s[/COLOR].[CR][CR]Press OK to delete this file.'%autoRun)
os.remove(koding.Physical_Path(myXmlFile))
~"""

    def __init__(self, xmlFile, masterTag="settings", childTag="setting"):
        self.xmlFile = xmlFile
        self.masterTag = masterTag
        self.childTag = childTag
        self.xmlFile = Physical_Path(self.xmlFile)

    def ParseValue(self, settingID, settingIDTag="id", settingValueTag="value", addChild=False, formatXML=True):
        if not os.path.exists(self.xmlFile):
            return
        tree = ElementTree.parse(self.xmlFile)
        root = tree.getroot()
        for child in root:
            if child.attrib[settingIDTag] == settingID:
                return child.attrib.get(settingValueTag)

    def SetValue(self, settingID, newValue, settingIDTag="id", settingValueTag="value", addChild=False, asString=False, formatXML=True):
        if not os.path.exists(self.xmlFile):
            self.CreateXML(settingIDTag=settingIDTag, settingValueTag=settingValueTag, addChild=addChild, formatXML=formatXML)
        tree = ElementTree.parse(self.xmlFile)
        root = tree.getroot()
        targetChild = None
        for child in root:
            if child.attrib[settingIDTag] == settingID:
                targetChild = child
        if targetChild is None:
            self.AppendChild(root, settingID=settingID, newValue=newValue, settingIDTag=settingIDTag, settingValueTag=settingValueTag)
        else:
            for child in root:
                if child.attrib[settingIDTag] == settingID:
                    child.attrib['%s' % (settingValueTag)] = '%s' % (newValue)
        tree.write(self.xmlFile)
        if asString:
            readfile = open(self.xmlFile, 'r')
            content = readfile.read()
            readfile.close()
            pretty = self.Prettify(content, asString=True)
        else:
            pretty = self.Prettify(self.xmlFile)
        f = open(self.xmlFile, "w")
        f.write(pretty)
        f.close()

    def CreateXML(self, settingIDTag="id", settingValueTag="value", addChild=False, formatXML=True):
        root = ElementTree.Element("%s" % self.masterTag)
        if addChild:
            sub = ElementTree.SubElement(root, "%s" % self.childTag)
            sub.set(settingIDTag, "")
            sub.set(settingValueTag, "")

        tree = ElementTree.ElementTree(root)
        tree.write(self.xmlFile)
        if formatXML:
            pretty = self.Prettify(self.xmlFile)
            f = open(self.xmlFile, "w")
            f.write(pretty)
            f.close()

    def AppendChild(self, root, settingID, newValue, settingIDTag="id", settingValueTag="value"):
        ElementTree.SubElement(root, self.childTag, attrib={settingIDTag: settingID, settingValueTag: newValue})
        return root

    def Prettify(self, elem, asString=False):
        import xml.dom.minidom
        if asString:
            xml = xml.dom.minidom.parseString(elem)
            pretty_xml_as_string = '\n'.join([line for line in xml.toprettyxml(indent=' ' * 2).split('\n') if line.strip()])
        else:
            pretty_xml_as_string = '\n'.join([line for line in xml.dom.minidom.parse(open(elem)).toprettyxml(indent=' ' * 2).split('\n') if line.strip()])
        return pretty_xml_as_string
#----------------------------------------------------------------    
# Legacy code, now use new function Compress
def Archive_Tree(sourcefile, destfile, exclude_dirs=['temp'], exclude_files=['kodi.log','kodi.old.log','xbmc.log','xbmc.old.log','spmc.log','spmc.old.log'], message_header = 'ARCHIVING', message = 'Creating archive'):
    Compress(src=sourcefile, dst=destfile, exclude_dirs=exclude_dirs, exclude_files=exclude_files)
#----------------------------------------------------------------    
# TUTORIAL #
def Compress(src,dst,compression='zip',parent=False, exclude_dirs=['temp'], exclude_files=['kodi.log','kodi.old.log','xbmc.log','xbmc.old.log','spmc.log','spmc.old.log'], message_header = 'ARCHIVING', message = 'Creating archive'):
    """
Compress files in either zip or tar format. This will most likely be replacing
Archive_Tree longer term as this has better functionality but it's currently
missing the custom message and exclude files options.

IMPORTANT: There was a known bug where some certain compressed tar.gz files can cause the system to hang
and a bad zipfile will continue to be made until it runs out of space on your storage device. In the unlikely
event you encounter this issue just add the problematic file(s) to your exclude list. I think this has since
been fixed since a complete re-code to this function, or at least I've been unable to recreate it. If you
find this problem is still occuring please let me know on the forum at http://totalrevolution.tv/forum
(user: trevdev), thankyou.

CODE: Compress(src,dst,[compression,parent])

AVAILABLE PARAMS:

    (*) src  -  This is the source folder you want to compress

    (*) dst  -  This is the destination file you want to create

    compression  -  By default this is set to 'zip' but you can also use 'tar'

    parent  -  By default this is set to False which means it will compress
    everything inside the path given. If set to True it will do the same but
    it will include the parent folder name - ideal if you want to zip up
    an add-on folder and be able to install via Kodi Settings.

    exclude_dirs   - This is optional, if you have folder names you want to exclude just
    add them here as a list item. By default the folder 'temp' is added to this list so
    if you need to include folders called temp make sure you send through a list, even
    if it's an empty one. The reason for leaving temp out is that's where Kodi logfiles
    and crashlogs are stored on a lot of devices and these are generally not needed in
    backup zips.

    exclude_files  - This is optional, if you have specific file names you want to
    exclude just add them here as a list item. By default the list consists of:
    'kodi.log','kodi.old.log','xbmc.log','xbmc.old.log','spmc.log','spmc.old.log'

EXAMPLE CODE:
koding_path = koding.Physical_Path('special://home/addons/script.module.python.koding.aio')
zip_dest = koding.Physical_Path('special://home/test_addon.zip')
zip_dest2 = koding.Physical_Path('special://home/test_addon2.zip')
tar_dest = koding.Physical_Path('special://home/test_addon.tar')
tar_dest2 = koding.Physical_Path('special://home/test_addon2.tar')
koding.Compress(src=koding_path,dst=zip_dest,compression='zip',parent=True)
koding.Compress(src=koding_path,dst=zip_dest2,compression='zip',parent=False)
koding.Compress(src=koding_path,dst=tar_dest,compression='tar',parent=True)
koding.Compress(src=koding_path,dst=tar_dest2,compression='tar',parent=False)
koding.Text_Box('CHECK HOME FOLDER','If you check your Kodi home folder you should now have 4 different compressed versions of the Python Koding add-on.\n\ntest_addon.zip: This has been zipped up with parent set to True\n\ntest_addon2.zip: This has been zipped up with parent set to False.\n\ntest_addon.tar: This has been compressed using tar format and parent set to True\n\ntest_addon2.tar: This has been compressed using tar format and parent set to False.\n\nFeel free to manually delete these.')
~"""
    import zipfile
    import tarfile
    directory = os.path.dirname(dst)
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except:
            dialog.ok('ERROR','The destination directory you gave does not exist and it wasn\'t possible to create it.')
            return
    if compression == 'zip':
        zip = zipfile.ZipFile(dst, 'w', compression=zipfile.ZIP_DEFLATED)
    elif compression == 'tar':
        zip = tarfile.open(dst, mode='w')
    module_id        =  'script.module.python.koding.aio'
    this_module      =  xbmcaddon.Addon(id=module_id)
    folder_size      =  Folder_Size(src,'mb')
    available_space  =  Free_Space(HOME,'mb')
    if os.path.exists(src):
        choice = True
        if float(available_space) < float(folder_size):
            choice = dialog.yesno(this_module.getLocalizedString(30809), this_module.getLocalizedString(30810), this_module.getLocalizedString(30811) % folder_size, this_module.getLocalizedString(30812) % available_space, yeslabel = this_module.getLocalizedString(30813), nolabel = this_module.getLocalizedString(30814))
        if choice:
            root_len = len(os.path.dirname(os.path.abspath(src)))
            for base, dirs, files in os.walk(src):
                dirs[:]  = [d for d in dirs if d not in exclude_dirs]
                files[:] = [f for f in files if f not in exclude_files and not 'crashlog' in f and not 'stacktrace' in f]
                archive_root = os.path.abspath(base)[root_len:]

                for f in files:
                    fullpath = os.path.join(base, f)
                    if parent:
                        archive_name = os.path.join(archive_root, f)
                        if compression == 'zip':
                            zip.write(fullpath, archive_name, zipfile.ZIP_DEFLATED)
                        elif compression == 'tar':
                            zip.add(fullpath, archive_name)
                    else:
                        newpath = fullpath.split(src)[1]
                        if compression == 'zip':
                            zip.write(fullpath, newpath, zipfile.ZIP_DEFLATED)
                        elif compression == 'tar':
                            zip.add(fullpath, newpath)
            zip.close()
#----------------------------------------------------------------    
# TUTORIAL #
def Create_Paths(path=''):
    """
Send through a path to a file, if the directories required do not exist this will create them.

CODE: Create_Paths(path)

AVAILABLE PARAMS:

    (*) path  -  This is the full path including the filename. The path
    sent through will be split up at every instance of '/'

EXAMPLE CODE:
my_path = xbmc.translatePath('special://home/test/testing/readme.txt')
koding.Create_Paths(path=my_path)
dialog.ok('PATH CREATED','Check in your Kodi home folder and you should now have sub-folders of /test/testing/.','[COLOR=gold]Press ok to remove these folders.[/COLOR]')
shutil.rmtree(xbmc.translatePath('special://home/test'))
~"""
    home_path = Physical_Path('special://home')
    path = path.replace(home_path,'')
    newpath = os.path.join('special://home',path)
    if path != '' and not os.path.exists(Physical_Path(newpath)):
        root_path = path.split(os.sep)
        if root_path[-1] == '':
            root_path.pop()
        root_path.pop()
        final_path = ''
        for item in root_path:
            final_path = os.path.join(final_path,item)
        final_path = os.path.join('special://home',final_path)
        xbmcvfs.mkdirs(final_path)
#----------------------------------------------------------------    
# TUTORIAL #
def DB_Path_Check(db_path):
    """
If you need to find out the current "real" database in use then this is the function for you.
It will scan for a specific database type (e.g. addons) and return the path to the one which was last updated.
This is particularly useful if the system has previously updated to a newer version rather than a fresh install
or if they've installed a "build" which contained old databases.

CODE: DB_Path_Check(db_path)

AVAILABLE VALUES:

    (*) db_path  -  This is the string the database starts with.
    If you want to find the path for the addons*.db you would use "addons"
    as the value, if you wanted to find the path of the MyVideos*.db you would use
    "myvideos" etc. - it is not case sensitive.

EXAMPLE CODE:
dbpath = koding.DB_Path_Check(db_path='addons')
dialog.ok('ADDONS DB','The path to the current addons database is:',dbpath)
~"""
    finalfile = 0
    dirs,databasepath = xbmcvfs.listdir(DATABASE)
    for item in databasepath:
        if item.lower().endswith('.db') and item.lower().startswith(db_path.lower()):
            mydb         = os.path.join(DATABASE,item)
            lastmodified = xbmcvfs.Stat(mydb).st_mtime()
            if lastmodified>finalfile:
                finalfile = lastmodified
                gooddb   = mydb
    return Physical_Path(gooddb)
#---------------------------------------------------------------------------------------------------
# TUTORIAL #
def Delete_Crashlogs(extra_paths=[]):
    """
Delete all kodi crashlogs. This function will retun the amount of successfully removed crashlogs.

CODE: Delete_Crashlogs([extra_paths])

AVAILABLE PARAMS:
    extra_paths  -  By default this will search for crashlogs for xbmc,
    kodi and spmc. If you want to add compatibility for other forks of
    Kodi please send through a list of the files you want deleted. The
    format to use needs to be like example shown below.

EXAMPLE CODE:
# Lets setup some extra crashlog types for tvmc and ftmc kodi forks
log_path =  xbmc.translatePath('special://logpath/')
tvmc_path = os.path.join(log_path,'tvmc_crashlog*.*')
ftmc_path = os.path.join(log_path,'ftmc_crashlog*.*')


deleted_files = koding.Delete_Crashlogs(extra_paths=[tvmc_path, ftmc_path])
if deleted_files > 0:
    dialog.ok('CRASHLOGS DELETED','Congratulations, a total of %s crashlogs have been deleted.')
else:
    dialog.ok('NO CRASHLOGS','No crashlogs could be found on the system.')
~"""
    import glob
    log_path =  'special://logpath/'
    xbmc_path = (os.path.join(log_path, 'xbmc_crashlog*.*'))
    kodi_path = (os.path.join(log_path, 'kodi_crashlog*.*'))
    spmc_path = (os.path.join(log_path, 'spmc_crashlog*.*'))
    paths = [xbmc_path, kodi_path, spmc_path]
    total = 0
    for items in paths:
        for file in glob.glob(items):
            try:
                 xbmcvfs.delete(file)
                 total+=1
            except:
                pass
    return total
#----------------------------------------------------------------
# TUTORIAL #
def Delete_Files(filepath = HOME, filetype = '*.txt', subdirectories=False):
    """
Delete all specific filetypes in a path (including sub-directories)

CODE: Delete_Files([filepath, filetype, subdirectories])

AVAILABLE PARAMS:
    
    (*) filepath  -  By default this points to the Kodi HOME folder (special://home).
    The path you send through must be a physical path and not special://

    (*) filetype  -  The type of files you want to delete, by default it's set to *.txt

    subdirectories  -  By default it will only search the folder given, if set to True
    all filetypes listed above will be deleted in the sub-directories too.

WARNING: This is an extremely powerful and dangerous tool! If you wipe your whole system
by putting in the wrong path then it's your own stupid fault!

EXAMPLE CODE:
delete_path = 'special://profile/addon_data/test'
xbmcvfs.mkdirs(delete_path)
test1 = os.path.join(delete_path,'test1.txt')
test2 = os.path.join(delete_path,'test2.txt')
koding.Text_File(test1,'w','testing1')
koding.Text_File(test2,'w','testing2')
dialog.ok('DELETE FILES','All *.txt files will be deleted from:', '', '/userdata/addon_data/test/')
koding.Delete_Files(filepath=delete_path, filetype='.txt', subdirectories=True)
~"""
    filepath = Physical_Path(filepath)
    if filepath == '/' or filepath == '.' or filepath == '' or (filepath[1]==':' and len(filepath)<4):
        dialog.ok('IDTenT ERROR!!!','You are trying to wipe your whole system!!!','Be more careful in future, not everyone puts checks like this in their code!')
        return

    if os.path.exists(filepath):
        filetype = filetype.replace('*','')

        if subdirectories:
            for parent, dirnames, filenames in os.walk(filepath):
                for fn in filenames:
                    if fn.lower().endswith(filetype):
                        xbmcvfs.delete(os.path.join(parent, fn))

        else:
            for delete_file in xbmcvfs.listdir(filepath):
                delete_path = os.path.join(filepath,delete_file)
                if delete_path.endswith(filetype):
                    try:
                        xbmcvfs.delete(delete_path)
                    except:
                        xbmc.log(Last_Error(),2)
    else:
        xbmc.log('### Cannot delete files as directory does not exist: %s' % filepath,2)
#----------------------------------------------------------------
# TUTORIAL #
def Delete_Folders(filepath='', ignore=[]):
    """
Completely delete a folder and all it's sub-folders. With the ability to add
an ignore list for any folders/files you don't want removed.

CODE: Delete_Folders(filepath, [ignore])

AVAILABLE PARAMS:
    
    (*) filepath  -  Use the physical path you want to remove, this must be converted
    to the physical path and will not work with special://

    ignore  -  A list of paths you want to ignore. These need to be sent
    through as physical paths so just use koding.Physical_Path() when creating
    your list and these can be folder paths or filepaths.

WARNING: This is an extremely powerful and dangerous tool! If you wipe important
system files from your system by putting in the wrong path then I'm afraid that's
your own stupid fault! A check has been put in place so you can't accidentally
wipe the whole root.

EXAMPLE CODE:
delete_path = koding.Physical_Path('special://profile/py_koding_test')

# Create new test directory to remove
if not os.path.exists(delete_path):
    os.makedirs(delete_path)

# Fill it with some dummy files
file1 = os.path.join(delete_path,'file1.txt')
file2 = os.path.join(delete_path,'file2.txt')
file3 = os.path.join(delete_path,'file3.txt')
koding.Dummy_File(dst=file1, size=10, size_format='kb')
koding.Dummy_File(dst=file2, size=10, size_format='kb')
koding.Dummy_File(dst=file3, size=10, size_format='kb')

dialog.ok('TEST FILE CREATED','If you look in your userdata folder you should now see a new test folder containing 3 dummy files. The folder name is \'py_koding_test\'.')
if dialog.yesno('[COLOR gold]DELETE FOLDER[/COLOR]','Everything except file1.txt will now be removed from:', '/userdata/py_koding_test/','Do you want to continue?'):
    koding.Delete_Folders(filepath=delete_path, ignore=[file1])
    dialog.ok('DELETE LEFTOVERS','When you press OK we will delete the whole temporary folder we created including it\'s contents')
    koding.Delete_Folders(filepath=delete_path)
~"""
    exclude_list = ['','/','\\','C:/','storage']

# Check you're not trying to wipe root!
    if filepath in exclude_list:
        dialog.ok('FILEPATH REQUIRED','You\'ve attempted to remove files but forgot to pass through a valid filepath. Luckily this failsafe check is in place or you could have wiped your whole system!')

# If there's some ignore files we run through deleting everything but those files
    elif len(ignore) > 0:
        for root, dirs, files in os.walk(filepath, topdown=False):
            cont = True
            if not root in ignore:
                for item in ignore:
                    if item in root:
                        cont=False
                        break
                if cont:
                    for file in files:
                        file_path = os.path.join(root,file)
                        if file_path not in ignore:
                            try:
                                xbmcvfs.delete(file_path)
                            except:
                                xbmc.log('Failed to delete: %s'%file_path,2)
                    if len(os.listdir(root)) == 0:
                        try:
                            xbmcvfs.rmdir(root)
                        except:
                            pass

# If a simple complete wipe of a directory and all sub-directories is required we use this
    elif os.path.exists(filepath):
        shutil.rmtree(filepath, ignore_errors=True)
        # xbmc.executebuiltin('Container.Refresh')
#----------------------------------------------------------------
# TUTORIAL #
def Dummy_File(dst= 'special://home/dummy.txt', size='10', size_format='mb'):
    """
Create a dummy file in whatever location you want and with the size you want.
Use very carefully, this is designed for testing purposes only. Accidental
useage can result in the devices storage becoming completely full in just a
few seconds. If using a cheap poor quality device (like many android units)
then you could even end up killing the device as some of them are made
with very poor components which are liable to irreversable corruption.

CODE: koding.Dummy_File(dest, [size, size_format])

AVAILABLE PARAMS:

    dst          - This is the destination folder. This needs to be a FULL path including
    the file extension. By default this is set to special://home/dummy.txt

    size         -  This is an optional integer, by default a file of 10 MB will be created.

    size_format  -  By default this is set to 'mb' (megabytes) but you can change this to
    'b' (bytes), 'kb' (kilobytes), 'gb' (gigabytes)

EXAMPLE CODE:
dummy = 'special://home/test_dummy.txt'
koding.Dummy_File(dst=dummy, size=100, size_format='b')
dialog.ok('DUMMY FILE CREATED','Check your Kodi home folder and you should see a 100 byte test_dummy.txt file.','[COLOR=gold]Press OK to delete this file.[/COLOR]')
xbmcvfs.delete(dummy)
~"""
    dst = Physical_Path(dst)
    xbmc.log('dst: %s'%dst,2)
    if size_format == 'kb':
        size = float(size*1024)
    elif size_format == 'mb':
        size = float(size*1024) * 1024
    elif size_format == 'gb':
        size = float(size*1024) * 1024 * 1024

    xbmc.log('format: %s  size: %s'%(size_format, size), 2)

    f = open(dst,"wb")
    f.seek(size-1)
    f.write("\0")
    f.close()
#----------------------------------------------------------------
# TUTORIAL #
def End_Path(path):
    """
Split the path at every '/' and return the final file/folder name.
If your path uses backslashes rather than forward slashes it will use
that as the separator.

CODE:  End_Path(path)

AVAILABLE PARAMS:

    path  -  This is the path where you want to grab the end item name.

EXAMPLE CODE:
addons_path = 'special://home/addons'
file_name = koding.End_Path(path=addons_path)
dialog.ok('ADDONS FOLDER','Path checked:',addons_path,'Folder Name: [COLOR=dodgerblue]%s[/COLOR]'%file_name)
file_path = 'special://home/addons/script.module.python.koding.aio/addon.xml'
file_name = koding.End_Path(path=file_path)
dialog.ok('FILE NAME','Path checked:',file_path,'File Name: [COLOR=dodgerblue]%s[/COLOR]'%file_name)
~"""
    if '/' in path:
        path_array = path.split('/')
        if path_array[-1] == '':
            path_array.pop()
    elif '\\' in path:
        path_array = path.split('\\')
        if path_array[-1] == '':
            path_array.pop()
    else:
        return path
    return path_array[-1]
#----------------------------------------------------------------
# TUTORIAL #
def Extract(_in, _out, dp=None, show_error=False):
    """
This function will extract a zip or tar file and return true or false so unlike the
builtin xbmc function "Extract" this one will pause code until it's completed the action.

CODE: koding.Extract(src,dst,[dp])
dp is optional, by default it is set to false

AVAILABLE PARAMS:

    (*) src    - This is the source file, the actual zip/tar. Make sure this is a full path to
    your zip file and also make sure you're not using "special://". This extract function
    is only compatible with .zip/.tar/.tar.gz files

    (*) dst    - This is the destination folder, make sure it's a physical path and not
    "special://...". This needs to be a FULL path, if you want it to extract to the same
    location as where the zip is located you still have to enter the full path.

    dp - This is optional, if you pass through the dp function as a DialogProgress()
    then you'll get to see the status of the extraction process. If you choose not to add
    this paramater then you'll just get a busy spinning circle icon until it's completed.
    See the example below for a dp example.

    show_error - By default this is set to False, if set to True an error dialog 
    will appear showing details of the file which failed to extract.

EXAMPLE CODE:
koding_path = koding.Physical_Path('special://home/addons/script.module.python.koding.aio')
zip_dest = koding.Physical_Path('special://home/test_addon.zip')
extract_dest = koding.Physical_Path('special://home/TEST')
koding.Compress(src=koding_path,dst=zip_dest,compression='zip',parent=True)
dp = xbmcgui.DialogProgress()
dp.create('Extracting Zip','Please Wait')
if koding.Extract(_in=zip_dest,_out=extract_dest,dp=dp,show_error=True):
    dialog.ok('YAY IT WORKED!','We just zipped up your python koding add-on then extracted it to a new folder in your Kodi root directory called TEST. Press OK to delete these files.')
    xbmcvfs.delete(zip_dest)
    shutil.rmtree(extract_dest)
else:
    dialog.ok('BAD NEWS!','UH OH SOMETHING WENT HORRIBLY WRONG')
~"""
    import tarfile
    import xbmcaddon
    import zipfile

    module_id   = 'script.module.python.koding.aio'
    this_module = xbmcaddon.Addon(id=module_id)
    nFiles      = 0
    count       = 0

    if xbmcvfs.exists(_in):
        if zipfile.is_zipfile(_in):
            zin      = zipfile.ZipFile(_in,  'r')
            nFiles   = float(len(zin.infolist()))
            contents = zin.infolist()

        elif tarfile.is_tarfile(_in):
            zin      = tarfile.open(_in)
            contents = [tarinfo for tarinfo in zin.getmembers()]
            nFiles   = float(len(contents))
       
        if nFiles > 0:
            if dp:
                try:
                    for item in contents:
                        count += 1
                        update = count / nFiles * 100
                        dp.update(int(update))
                        zin.extract(item, _out)
                    zin.close()
                    return True

                except:
                    xbmc.log(Last_Error(),2)
                    return False
            else:
                try:
                    zin.extractall(_out)
                    return True
                except:
                    xbmc.log(Last_Error(),2)
                    return False
        
        else:
            xbmc.log('NOT A VALID ZIP OR TAR FILE: %s' % _in,2)
    else:
        if show_error:
            dialog.ok(this_module.getLocalizedString(30965),this_module.getLocalizedString(30815) % _in)
#----------------------------------------------------------------
# TUTORIAL #
def Free_Space(dirname = HOME, filesize = 'b'):
    """
Show the amount of available free space in a path, this can be returned in a number of different formats.

CODE: Free_Space([dirname, filesize])

AVAILABLE PARAMS:

    dirname  - This optional, by default it will tell you how much space is available in your special://home
    folder. If you require information for another path (such as a different partition or storage device)
    then enter the physical path. This currently only works for local paths and not networked drives.

    filesize - By default you'll get a return of total bytes, however you can get the value as bytes,
    kilobytes, megabytes, gigabytes and terabytes..

        VALUES:
        'b'  = bytes (integer)
        'kb' = kilobytes (float to 1 decimal place)
        'mb' = kilobytes (float to 2 decimal places)
        'gb' = kilobytes (float to 3 decimal places)
        'tb' = terabytes (float to 4 decimal places)

EXAMPLE CODE:
HOME = Physical_Path('special://home')
my_space = koding.Free_Space(HOME, 'gb')
dialog.ok('Free Space','Available space in HOME: %s GB' % my_space)
~"""
    import ctypes
    dirname = Physical_Path(dirname)
    filesize = filesize.lower()
    if xbmc.getCondVisibility('system.platform.windows'):
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(dirname), None, None, ctypes.pointer(free_bytes))
        finalsize = free_bytes.value
    else:
        st = os.statvfs(dirname)
        finalsize =  st.f_bavail * st.f_frsize
    if filesize == 'b':
        return finalsize
    elif filesize == 'kb':
        return "%.1f" % (float(finalsize / 1024))
    elif filesize == 'mb':
        return "%.2f" % (float(finalsize / 1024) / 1024)
    elif filesize == 'gb':
        return "%.3f" % (float(finalsize / 1024) / 1024 / 1024)
    elif filesize == 'tb':
        return "%.4f" % (float(finalsize / 1024) / 1024 / 1024 / 1024)
#----------------------------------------------------------------
# TUTORIAL #
def Folder_Size(dirname = HOME, filesize = 'b'):
    """
Return the size of a folder path including sub-directories,
this can be returned in a number of different formats.

CODE: koding.Folder_Size([dirname, filesize])

AVAILABLE PARAMS:

    dirname  - This optional, by default it will tell you how much space is available in your
    special://home folder. If you require information for another path (such as a different
    partition or storage device) then enter the physical path. This currently only works for
    local paths and not networked drives.

    filesize - By default you'll get a return of total bytes, however you can get the value as
    bytes, kilobytes, megabytes, gigabytes and terabytes..

        VALUES:
        'b'  = bytes (integer)
        'kb' = kilobytes (float to 1 decimal place)
        'mb' = kilobytes (float to 2 decimal places)
        'gb' = kilobytes (float to 3 decimal places)
        'tb' = terabytes (float to 4 decimal places)

EXAMPLE CODE:
HOME = Physical_Path('special://home')
home_size = Folder_Size(HOME, 'mb')
dialog.ok('Folder Size','KODI HOME: %s MB' % home_size)
~"""
    finalsize = 0
    for dirpath, dirnames, filenames in os.walk(dirname):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            finalsize += os.path.getsize(fp)
    if filesize == 'b':
        return finalsize
    elif filesize == 'kb':
        return "%.1f" % (float(finalsize / 1024))
    elif filesize == 'mb':
        return "%.2f" % (float(finalsize / 1024) / 1024)
    elif filesize == 'gb':
        return "%.3f" % (float(finalsize / 1024) / 1024 / 1024)
    elif filesize == 'tb':
        return "%.4f" % (float(finalsize / 1024) / 1024 / 1024 / 1024)
#----------------------------------------------------------------
# TUTORIAL #
def Fresh_Install(keep_addons=[],ignore=[],keepdb=True):
    """
Attempt to completely wipe your install. You can send through a list
of addons or paths you want to ignore (leave in the setup) or you can
leave blank. If left blank and the platform is OpenELEC or LibreELEC
it will perform a hard reset command followed by a reboot.

CODE:  Fresh_Install([keep_addons, ignore, keepdb)

AVAILABLE PARAMS:

    keep_addons  -  This is optional, if you have specific add-ons you want to omit
    from the wipe (leave intact) then just enter a list of add-on id's here. The code
    will determine from the addon.xml file which dependencies and sub-dependencies are
    required for that add-on so there's no need to create a huge list, you only need to
    list the master add-on id's. For example if you want to keep the current skin and
    your add-on you would use: keep_addons=['plugin.program.myaddon',System('currentskin')]
    and all addons/dependencies associated with those two add-ons will be added to the ignore
    list.

    ignore  -  This is optional, you can send through a list of paths you want to omit from
    the wipe. You can use folder paths to skip the whole folder or you can use individual
    file paths. Please make sure you use the physical path and not special://
    So before creating your list make sure you use xbmc.translatePath()

    keepdb  -  By default this is set to True which means the code will keep all the Kodi databases
    intact and perform a profile reload once wipe is complete. This will mean addons, video, music,
    epg, ADSP and viewtypes databases will remain completely untouched and Kodi should be fine to use
    without the need for a restart. If you set keepdb to False nothing will happen once the wipe has
    completed and it's up to you to choose what to do in your main code. I would highly recommend an
    ok dialog followed by xbmc.executebuiltin('Quit'). This will force Kodi to recreate all the relevant
    databases when they re-open. If you try and continue using Kodi without restarting the databases
    will not be recreated and you risk corruption.

EXAMPLE CODE:
if dialog.yesno('[COLOR gold]TOTAL WIPEOUT![/COLOR]','This will attempt give you a totally fresh install of Kodi.','Are you sure you want to continue?'):
    if dialog.yesno('[COLOR gold]FINAL CHANCE!!![/COLOR]','If you click Yes this WILL attempt to wipe your install', '[COLOR=dodgerblue]ARE YOU 100% CERTAIN YOU WANT TO WIPE?[/COLOR]'):
        clean_state = koding.Fresh_Install()
~"""
# If it's LE/OE and there are no files to ignore we do a hard reset
    from systemtools import Cleanup_Textures
    if ( len(ignore)==0 ) and ( len(keep_addons)==0 ) and ( xbmc.getCondVisibility("System.HasAddon(service.libreelec.settings)") or xbmc.getCondVisibility("System.HasAddon(service.openelec.settings)") ):
        xbmc.log('OE DETECTED',2)
        resetpath='storage/.cache/reset_oe'
        Text_File(resetpath,'w')
        xbmc.executebuiltin('reboot')
    else:
        from addons import Dependency_Check
        xbmc.log('DOING MAIN WIPE',2)
        skip_array = []
        addonsdb = DB_Path_Check('addons')
        textures = DB_Path_Check('Textures')
        Cleanup_Textures(frequency=1,use_count=999999)
        if len(keep_addons) > 0:
            ignorelist = Dependency_Check(addon_id = keep_addons, recursive = True)
            for item in ignorelist:
                skip_array.append(xbmcaddon.Addon(id=item).getAddonInfo('path'))
        skip_array.append(addonsdb)
        skip_array.append(textures)
        if keepdb:
            try:
                skip_array.append( DB_Path_Check('Epg') )
            except:
                xbmc.log('No EPG DB Found, skipping',2)
            try:
                skip_array.append( DB_Path_Check('MyVideos') )
            except:
                xbmc.log('No MyVideos DB Found, skipping',2)
            try:
                skip_array.append( DB_Path_Check('MyMusic') )
            except:
                xbmc.log('No MyMusic DB Found, skipping',2)
            try:
                skip_array.append( DB_Path_Check('TV') )
            except:
                xbmc.log('No TV DB Found, skipping',2)
            try:
                skip_array.append( DB_Path_Check('ViewModes') )
            except:
                xbmc.log('No ViewModes DB Found, skipping',2)
            try:
                skip_array.append( DB_Path_Check('ADSP') )
            except:
                xbmc.log('No ADSP DB Found, skipping',2)
        for item in ignore:
            skip_array.append(item)
        Delete_Folders(filepath=HOME, ignore=skip_array)
        Refresh()
        if keepdb:
            Refresh('profile')

# Good option for wiping android data but not so good if using the app as a launcher!
    # elif xbmc.getCondVisibility('System.Platform.Android'):
    #     import subprocess
    #     running   = Running_App()
    #     cleanwipe = subprocess.Popen(['exec ''pm clear '+str(running)+''], executable='/system/bin/sh', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, preexec_fn=Get_ID(setid=True)).communicate()[0]
#----------------------------------------------------------------
# TUTORIAL #
def Get_Contents(path,folders=True,subfolders=False,exclude_list=[],full_path=True,filter=''):
    """
Return a list of either files or folders in a given path.

CODE:  Get_Contents(path, [folders, subfolders, exclude_list, full_path, filter])

AVAILABLE PARAMS:
    
    (*) path  -  This is the path you want to search, no sub-directories are scanned.
    
    folders  -  By default this is set to True and the returned list will only
    show folders. If set to False the returned list will show files only.

    exclude_list  -  Optionally you can add a list of items you don't want returned

    full_path  -  By default the entries in the returned list will contain the full
    path to the folder/file. If you only want the file/folder name set this to False.

    subfolders  -  By default this is set to False but if set to true it will check
    all sub-directories and not just the directory sent through.

    filter  -  If you want to only return files ending in a specific string you
    can add details here. For example to only show '.xml' files you would send
    through filter='.xml'.

EXAMPLE CODE:
ADDONS = Physical_Path('special://home/addons')
addon_folders = koding.Get_Contents(path=ADDONS, folders=True, exclude_list=['packages','temp'], full_path=False)
results = ''
for item in addon_folders:
    results += 'FOLDER: [COLOR=dodgerblue]%s[/COLOR]\n'%item
koding.Text_Box('ADDON FOLDERS','Below is a list of folders found in the addons folder (excluding packages and temp):\n\n%s'%results)
~"""
    final_list = []
    path = Physical_Path(path)
# Check all items in the given path
    if not subfolders:
        dirs,files = xbmcvfs.listdir(path)
        if folders:
            active_list = dirs
        else:
            active_list = files
        for item in active_list:
            if item not in exclude_list:
                if full_path:
                    final_list.append(os.path.join(path,item))
                else:
                    final_list.append(item)

# Traverse through all subfolders
    else:
        path = Physical_Path(path)
        for root, dirnames, filenames in os.walk(path):
            if not folders:
                for filename in filenames:
                    file_path = os.path.join(root, filename)
                    if filter=='':
                        if full_path:
                            final_list.append(file_path)
                        else:
                            final_list.append(filename)

                    elif file_path.endswith(filter):
                        if full_path:
                            final_list.append(file_path)
                        else:
                            final_list.append(filename)
            else:
                for dirname in dirnames:
                    if full_path:
                        final_list.append(os.path.join(root, dirname))
                    else:
                        final_list.append(dirname)
    return final_list
#----------------------------------------------------------------
# TUTORIAL #
def Move_Tree(src, dst, dp=None):
    """
Move a directory including all sub-directories to a new location.
This will automatically create the new location if it doesn't already
exist and it wierwrite any existing entries if they exist.

CODE: koding.Move_Tree(src, dst)

AVAILABLE PARAMS:

    (*) src  -  This is source directory that you want to copy

    (*) dst  -  This is the destination location you want to copy a directory to.

    dp - This is optional, if you pass through the dp function as a DialogProgress()
    then you'll get to see the status of the move process. See the example below for a dp example.

EXAMPLE CODE:
dp = xbmcgui.DialogProgress()
source = koding.Physical_Path('special://profile/move_test')

# Lets create a 500MB dummy file so we can move and see dialog progress
dummy = os.path.join(source,'dummy')
if not os.path.exists(source):
    os.makedirs(source)
koding.Dummy_File(dst=dummy+'1.txt', size=10, size_format='mb')
koding.Dummy_File(dst=dummy+'2.txt', size=10, size_format='mb')
koding.Dummy_File(dst=dummy+'3.txt', size=10, size_format='mb')
koding.Dummy_File(dst=dummy+'4.txt', size=10, size_format='mb')
koding.Dummy_File(dst=dummy+'5.txt', size=10, size_format='mb')
koding.Dummy_File(dst=dummy+'6.txt', size=10, size_format='mb')
dialog.ok('DUMMY FILE CREATED','If you want to check in your userdata folder you should have a new folder called "move_test" which has 6x 10MB dummy files.')

# This is optional but if you want to see a dialog progress then you'll need this
dp.create('MOVING FILES','Please Wait')

destination = koding.Physical_Path('special://home/My MOVED Dummy File')
koding.Move_Tree(source, destination, dp)
dialog.ok('CHECK YOUR KODI HOME FOLDER','Please check your Kodi home folder, the dummy file should now have moved in there. When you press OK it will be removed')
shutil.rmtree(destination)
~"""
    src = Physical_Path(src)
    dst = Physical_Path(dst)
    if dp:
        totalfiles = 0
        for root, dirs, files in os.walk(src):
            totalfiles += len(files)
        count = 0

    for src_dir, dirs, files in os.walk(src):
        dst_dir = src_dir.replace(src, dst, 1)
        if os.path.exists(dst_dir) and not os.path.isdir(dst_dir):
            try:
                os.remove(dst_dir)
            except:
                xbmc.log('File with same name as folder exists, need to manually delete:',2)
                xbmc.log(dst_dir,2)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        for file_ in files:
            src_file = os.path.join(src_dir, file_)
            dst_file = os.path.join(dst_dir, file_)
            if os.path.exists(dst_file) and dst_file != dst:
                os.remove(dst_file)
            try:
                os.rename(src_file,dst_file)
            except:
                shutil.move(src_file, dst_dir)
            if dp:
                try:
                    count += 1
                    update = count / totalfiles * 100
                    dp.update(int(update))
                except:
                    pass
    try:
        shutil.rmtree(src)
    except:
        pass

    if dp:
        dp.close()
#----------------------------------------------------------------
# TUTORIAL #
def Physical_Path(path='special://home'):
    """
Send through a special:// path and get the real physical path returned.
This has been written due to the problem where if you're running the Windows Store
version of Kodi the built-in xbmc.translatePath() function is returning bogus results
making it impossible to access databases.

CODE: koding.Physical_Path([path])

AVAILABLE PARAMS:
    
    path  -  This is the path to the folder/file you want returned. This is optional,
    if you leave this out it will just return the path to the root directory (special://home)

EXAMPLE CODE:
location = 'special://home/addons/script.module.python.koding.aio'
real_location = koding.Physical_Path(location)
xbmc.log(real_location,2)
dialog.ok('PHYSICAL PATH','The real path of special://home/addons/script.module.python.koding.aio is:','[COLOR=dodgerblue]%s[/COLOR]'%real_location)
~"""
    xbmc_install = xbmc.translatePath('special://xbmc')
    if not "WindowsApps" in xbmc_install:
        clean = xbmc.translatePath(path)
        if sys.platform == 'win32':
            clean = clean.replace('\/','\\')
    else:
        clean = xbmc.translatePath(path)
        if clean.startswith(xbmc_install):
            if sys.platform == 'win32':
                clean = clean.replace('\/','\\')
        else:
            return clean.replace('AppData\\Roaming\\','AppData\\Local\\Packages\\XBMCFoundation.Kodi_4n2hpmxwrvr6p\\LocalCache\\Roaming\\')
            if sys.platform == 'win32':
                clean = clean.replace('\/','\\')
    return clean
#----------------------------------------------------------------
# TUTORIAL #
def Text_File(path, mode, text = ''):
    """
Open/create a text file and read/write to it.

CODE: koding.Text_File(path, mode, [text])

AVAILABLE PARAMS:
    
    (*) path  -  This is the path to the text file

    (*) mode  -  This can be 'r' (for reading) or 'w' (for writing)

    text  -  This is only required if you're writing to a file, this
    is the text you want to enter. This will completely overwrite any
    text already in the file.

EXAMPLE CODE:
HOME = koding.Physical_Path('special://home')
koding_test = os.path.join(HOME, 'koding_test.txt')
koding.Text_File(path=koding_test, mode='w', text='Well done, you\'ve created a text file containing this text!')
dialog.ok('CREATE TEXT FILE','If you check your home Kodi folder and you should now have a new koding_test.txt file in there.','[COLOR=gold]DO NOT DELETE IT YET![/COLOR]')
mytext = koding.Text_File(path=koding_test, mode='r')
dialog.ok('TEXT FILE CONTENTS','The text in the file created is:','[COLOR=dodgerblue]%s[/COLOR]'%mytext,'[COLOR=gold]CLICK OK TO DELETE THE FILE[/COLOR]')
try:
    os.remove(koding_test)
except:
    dialog.ok('FAILED TO REMOVE','Could not remove the file, looks like you might have it open in a text editor. Please manually remove yourself')
~"""
    try:
        textfile = xbmcvfs.File(path, mode)

        if mode == 'r':
            content = textfile.read()
            textfile.close()
            return content

        if mode == 'w':
            textfile.write(text)
            textfile.close()
            return True

    except:
        xbmc.log(Last_Error(),2)
        return False
#----------------------------------------------------------------