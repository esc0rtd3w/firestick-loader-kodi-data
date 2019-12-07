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

from filetools import Physical_Path

HOME = Physical_Path('special://home')
#----------------------------------------------------------------
# TUTORIAL #
def ASCII_Check(sourcefile=HOME, dp=False):
    """
Return a list of files found containing non ASCII characters in the filename.

CODE: ASCII_Check([sourcefile, dp])

AVAILABLE PARAMS:
    
    sourcefile  -  The folder you want to scan, by default it's set to the
    Kodi home folder.
        
    dp  -  Optional DialogProgress, by default this is False. If you want
    to show a dp make sure you initiate an instance of xbmcgui.DialogProgress()
    and send through as the param.
        
EXAMPLE CODE:
home = koding.Physical_Path('special://home')
progress = xbmcgui.DialogProgress()
progress.create('ASCII CHECK')
my_return = ASCII_Check(sourcefile=home, dp=progress)
if len(my_return) > 0:
    dialog.select('NON ASCII FILES', my_return)
else:
    dialog.ok('ASCII CHECK CLEAN','Congratulations!','There weren\'t any non-ASCII files found on this system.')
~"""
    rootlen      = len(sourcefile)
    for_progress = []
    final_array  = []
    ITEM         = []

    for base, dirs, files in os.walk(sourcefile):
        for file in files:
            ITEM.append(file)   
    N_ITEM =len(ITEM)
    
    for base, dirs, files in os.walk(sourcefile):
        dirs[:] = [d for d in dirs]
        files[:] = [f for f in files]
        
        for file in files:
            for_progress.append(file) 
            progress = len(for_progress) / float(N_ITEM) * 100
            if dp:
                dp.update(0,"Checking for non ASCII files",'[COLOR yellow]%s[/COLOR]'%d, 'Please Wait')
            
            try:
                file.encode('ascii')

            except UnicodeDecodeError:
                badfile = (str(base)+'/'+str(file)).replace('\\','/').replace(':/',':\\')
                final_array.append(badfile)
    return final_array
#----------------------------------------------------------------
# TUTORIAL #
def Cleanup_String(my_string):
    """
Clean a string, removes whitespaces and common buggy formatting when pulling from websites

CODE: Cleanup_String(my_string)

AVAILABLE PARAMS:
    
    (*) my_string   -  This is the main text you want cleaned up.
        
EXAMPLE CODE:
current_text = '" This is a string of text which should be cleaned up   /'
dialog.ok('ORIGINAL STRING', '[COLOR dodgerblue]%s[/COLOR]\n\nPress OK to view the cleaned up version.'%current_text)
clean_text = koding.Cleanup_String(current_text)
dialog.ok('CLEAN STRING', '[COLOR dodgerblue]%s[/COLOR]'%clean_text)
~"""
    import urllib
    bad_chars = ['/','\\',':',';','"',"'"]

    try:
        my_string = my_string.encode('utf8')
    except:
        pass
    
    my_string = urllib.unquote_plus(my_string)
    my_string = my_string.replace('<br>','').replace('<br />','').replace('<br/>','')
    my_string = my_string.replace('</p>','').replace('</div>','').replace('</class>','')
    my_string = my_string.replace('&amp;','&')
    if len(my_string) > 4:
        if my_string[-4] == '.':
            my_string = my_string[:-4]
    
    my_string = my_string.strip()

    while my_string[0] in bad_chars or my_string[-1] in bad_chars:
        if my_string[-1] in bad_chars:
            my_string = my_string[:-1]
        if my_string[0] in bad_chars:
            my_string = my_string[1:]
        my_string = my_string.strip()

    return my_string
#----------------------------------------------------------------
# TUTORIAL #
def Colour_Text(text, colour1='dodgerblue',colour2='white'):
    """
Capitalize a string and make the first colour of each string blue and the rest of text white
That's the default colours but you can change to whatever colours you want.

CODE: Colour_Text(text, [color1, color2])

AVAILABLE PARAMS:
    
    (*) text   -  This is the main text you want to change

    colour1 -  This is optional and is set as dodgerblue by default.
    This is the first letter of each word in the string

    colour2 -  This is optional and is set as white by default. 
    This is the colour of the text

IMPORTANT: I use the Queens English so please note the word "colour" has a 'u' in it!

EXAMPLE CODE:
current_text = 'This is a string of text which should be changed to dodgerblue and white with every first letter capitalised'
mytext = koding.Colour_Text(text=current_text, colour1='dodgerblue', colour2='white')
xbmc.log(current_text)
xbmc.log(mytext)
dialog.ok('CURRENT TEXT', current_text)
dialog.ok('NEW TEXT', mytext)
~"""
    if text.startswith('[COLOR') and text.endswith('/COLOR]'):
        return text

    colour_clean = 0

    if ' ' in text:
        newname = ''
        text = text.split(' ')
        for item in text:
            if len(item)==1 and item == '&':
                newname += ' &'
            if '[/COLOR]' in item:
                newname += ' '+item
            elif not item.startswith('[COLOR=') and not colour_clean:
                if item.startswith('(') or item.startswith('['):
                    newname += '[COLOR=yellow] '+item
                    colour_clean = 1
                else:
                    if item.isupper():
                        newname += '[COLOR=%s] %s[/COLOR]' % (colour1, item)
                    else:
                        try:
                            newname += '[COLOR=%s] %s[/COLOR][COLOR=%s]%s[/COLOR]' % (colour1, item[0].upper(), colour2, item[1:])
                        except:
                            try:
                                newname += '[COLOR=%s] %s[/COLOR][COLOR=%s][/COLOR]' % (colour1, item[0], colour2, item[1:])
                            except:
                                pass
            

            elif item.endswith(')') or item.endswith(']'):
                newname += ' '+item+'[/COLOR]'
                colour_clean = 0

            else:
                newname += ' '+item

    else:
        if text[0] == '(':
            newname = '[COLOR=%s]%s[/COLOR][COLOR=%s]%s[/COLOR][COLOR=%s]%s[/COLOR]' % (colour2, text[0], colour1, text[1].upper(), colour2, text[2:])
        else:
            newname = '[COLOR=%s]%s[/COLOR][COLOR=%s]%s[/COLOR]' % (colour1, text[0], colour2, text[1:])

    success = 0
    while success != 1:
        if newname.startswith(' '):
            newname = newname[1:]
        success = 1
    if newname.startswith('[COLOR=%s] ' % colour1):
        newname = '[COLOR=%s]%s' % (colour1, newname[19:])

    return newname
#----------------------------------------------------------------
# TUTORIAL #
def Convert_Special(filepath=HOME, string=False, quoted=True):
    """
Convert physcial paths stored in text files to their special:// equivalent or
replace instances of physical paths to special in a string sent through.

CODE: Convert_Special([filepath, string])

AVAILABLE PARAMS:

    filepath  -  This is the path you want to scan, by default it's set to the Kodi HOME directory.
    
    string  -  By default this is set to False which means it will convert all instances found of
    the physical paths to their special equivalent. The scan will convert all instances in all filenames
    ending in ini, xml, hash, properties. If you set this value to True you will get a return of your
    'filepath' string and no files will be altered.

    quoted  -  By default this is set to true, this means the return you get will be converted
    with urllib.quote_plus(). This is ideal if you need to get a string you can send
    through as a path for routing.

EXAMPLE CODE:
path = koding.Physical_Path('special://profile')
dialog.ok('ORIGINAL PATH','Let\'s convert this path to it\'s special equivalent:\n[COLOR dodgerblue]%s[/COLOR]'%path)
path = Convert_Special(filepath=path,string=True,quoted=False)
dialog.ok('CONVERTED PATH','This is the converted path:\n[COLOR dodgerblue]%s[/COLOR]'%path)
if dialog.yesno('CONVERT PHYSICAL PATHS','We will now run through your Kodi folder converting all physical paths to their special:// equivalent in xml/hash/properties/ini files.\nDo you want to continue?'):
    koding.Convert_Special()
    dialog.ok('SUCCESS','Congratulations, all references to your physical paths have been converted to special:// paths.')
~"""
    import urllib
    from filetools import Text_File
    if not string:
        for root, dirs, files in os.walk(filepath):
            for file in files:
                if file.endswith(".xml") or file.endswith(".hash") or file.endswith("properies") or file.endswith(".ini"):
                    contents     = Text_File(os.path.join(root,file), 'r')
                    encodedpath  = urllib.quote(HOME)
                    encodedpath2 = encodedpath.replace('%3A','%3a').replace('%5C','%5c')
                    newfile = contents.replace(HOME, 'special://home/').replace(encodedpath, 'special://home/').replace(encodedpath2, 'special://home/')
                    Text_File(os.path.join(root, file), 'w', newfile)
    else:
        encodedpath  = urllib.quote(HOME)
        encodedpath2 = encodedpath.replace('%3A','%3a').replace('%5C','%5c')
        newstring = filepath.replace(HOME, 'special://home/').replace(encodedpath, 'special://home/').replace(encodedpath2, 'special://home/')
        if quoted:
            newstring = urllib.quote_plus(newstring)
        return newstring
#----------------------------------------------------------------    
# TUTORIAL #
def Data_Type(data):
    """
This will return whether the item received is a dictionary, list, string, integer etc.

CODE:  Data_Type(data)

AVAILABLE PARAMS:
    
    (*) data  -  This is the variable you want to check.

RETURN VALUES:
    list, dict, str, int, float, bool

EXAMPLE CODE:
test1 = ['this','is','a','list']
test2 = {"a" : "1", "b" : "2", "c" : 3}
test3 = 'this is a test string'
test4 = 12
test5 = 4.3
test6 = True

my_return = '[COLOR dodgerblue]%s[/COLOR] : %s\n' % (test1, koding.Data_Type(test1))
my_return += '[COLOR dodgerblue]%s[/COLOR] : %s\n' % (test2, koding.Data_Type(test2))
my_return += '[COLOR dodgerblue]%s[/COLOR] : %s\n' % (test3, koding.Data_Type(test3))
my_return += '[COLOR dodgerblue]%s[/COLOR] : %s\n' % (test4, koding.Data_Type(test4))
my_return += '[COLOR dodgerblue]%s[/COLOR] : %s\n' % (test5, koding.Data_Type(test5))
my_return += '[COLOR dodgerblue]%s[/COLOR] : %s\n' % (test6, koding.Data_Type(test6))

koding.Text_Box('TEST RESULTS', my_return)
~"""
    data_type = type(data).__name__
    return data_type
#----------------------------------------------------------------
# TUTORIAL #
def Decode_String(string):
    """
This will allow you to send a string which contains a variety of special characters (including
non ascii, unicode etc.) and it will convert into a nice clean string which plays nicely
with Python and Kodi.

CODE: Decode_String(string)

AVAILABLE PARAMS:
    
    (*) string - This is the string you want to convert

EXAMPLE CODE:
my_string = 'symbols like [COLOR dodgerblue]¥¨˚∆ƒπø“¬∂≈óõřĖė[/COLOR] can cause errors \nnormal chars like [COLOR dodgerblue]asfasdf[/COLOR] are fine'
dialog.ok('ORIGINAL TEXT',my_string)
my_string = koding.Decode_String(my_string)
dialog.ok('DECODED/STRIPPED',my_string)
~"""
    try:
        string = string.encode('ascii', 'ignore')
    except:
        string = string.decode('utf-8').encode('ascii', 'ignore')
    return string
#----------------------------------------------------------------
# TUTORIAL #
def Find_In_Text(content, start, end, show_errors = False):
    """
Regex through some text and return a list of matches.
Please note this will return a LIST so even if only one item is found
you will still need to access it as a list, see example below.

CODE: Find_In_Text(content, start, end, [show_errors])

AVAILABLE PARAMS:
    
    (*) content  -  This is the string to search

    (*) start    -  The start search string

    (*) end      -  The end search string

    show_errors  -  Default is False, if set to True the code will show help
    dialogs for bad code.

EXAMPLE CODE:
textsearch = 'This is some text so lets have a look and see if we can find the words "lets have a look"'
dialog.ok('ORIGINAL TEXT','Below is the text we\'re going to use for our search:','[COLOR dodgerblue]%s[/COLOR]'%textsearch)
search_result = koding.Find_In_Text(textsearch, 'text so ', ' and see')
dialog.ok('SEARCH RESULT','You searched for the start string of "text so " and the end string of " and see".','','Your result is: [COLOR dodgerblue]%s[/COLOR]' % search_result[0])

# Please note: we know for a fact there is only one result which is why we're only accessing list item zero.
# If we were expecting more than one return we would probably do something more useful and loop through in a for loop.
~"""
    import re
    if content == None or content == False:
        if show_errors:
            dialog.ok('ERROR WITH REGEX','No content sent through - there\'s nothing to scrape. Please check the website address is still active (details at bottom of log).')
            xbmc.log(content)
        return
    if end != '':
        links = re.findall('%s([\s\S]*?)%s' % (start, end), content)
    if len(links)>0:
        return links
    else:
        if show_errors:
            xbmc.log(content)
            dialog.ok('ERROR WITH REGEX','Please check your regex, there was content sent through to search but there are no matches for the regex supplied. The raw content has now been printed to the log')
        return None
#----------------------------------------------------------------
# TUTORIAL #
def Fuzzy_Search(search_string, search_list, replace_strings=[]):
    """
Send through a list of items and try to match against the search string.
This will match where the search_string exists in the list or an item in
the list exists in the search_string.

CODE: Fuzzy_Search(search_string, search_list, [strip])

AVAILABLE PARAMS:
    
    (*) search_string  -  This is the string to search for

    (*) search_list    -  The list of items to search through

    replace_strings  -  Optionally send through a list of strings you want to
    replace. For example you may want to search for "West Ham United" but in
    the list you've sent through they've abbreviated it to "West Ham Utd FC". In
    this case we might want to send through a replace_strings list of:

    (["united","utd"], ["fc",""])

    This will remove any instances of "FC" from the search and it will replace
    instances of "united" to "utd". The code will convert everythig to lowercase
    so it doesn't matter what case you use in these searches.

EXAMPLE CODE:
my_search = 'west ham utd'
my_list = ['west ham united', 'west ham utd', 'rangers fc', 'Man City', 'West Ham United FC', 'Fulham FC', 'West Ham f.c']
my_replace = (["united","utd"], ["fc",""], ["f.c",""])
dialog.ok('FUZZY SEARCH','Let\'s search for matches similar to "west ham utd" in the list:\n\n%s'%my_list)
search_result = koding.Fuzzy_Search(my_search, my_list, my_replace)
good = ', '.join(search_result)
bad = ''
for item in my_list:
    if item not in search_result:
        bad += item+', '
dialog.ok('RESULTS FOUND','[COLOR=dodgerblue]SEARCH:[/COLOR] %s\n[COLOR=lime]GOOD:[/COLOR] %s\n[COLOR=cyan]BAD:[/COLOR] %s'%(my_search,good,bad))
~"""
    final_array = []
    newsearch = search_string.lower().strip().replace(' ','')
    for item in replace_strings:
        newsearch = newsearch.replace(item[0],item[1])
    xbmc.log('newsearch: %s'%newsearch,2)
    for item in search_list:
        newitem = item.lower().strip().replace(' ','')
        for rep in replace_strings:
            newitem = newitem.replace(rep[0],rep[1])
        xbmc.log('list_item: %s'%newitem,2)
        if (newsearch in newitem) or (newitem in newsearch):
            final_array.append(item)
    if len(final_array)>0:
        return final_array
    else:
        return False
#----------------------------------------------------------------
# TUTORIAL #
def Highest_Version(content=[],start_point='',end_point=''):
    """
Send through a list of strings which all have a common naming structure,
the one with the highest version number will be returned.

CODE: Highest_Version(content,[start_point,end_point])

AVAILABLE PARAMS:

    (*) content  -  This is the list of filenames you want to check.

    start_point  -  If your filenames have a common character/string immediately
    before the version number enter that here. For example if you're looking at
    online repository/add-on files you would use '-' as the start_point. The version
    numbers always appear after the final '-' with add-ons residing on repo's.

    end_point  -  If your version number is followed by a common string (e.g. '.zip')
    then enter it in here.

EXAMPLE CODE:
mylist = ['plugin.test-1.0.zip','plugin.test-0.7.zip','plugin.test-1.1.zip','plugin.test-0.9.zip']
dialog.ok('OUR LIST OF FILES', '[COLOR=dodgerblue]%s[/COLOR]\n[COLOR=powderblue]%s[/COLOR]\n[COLOR=dodgerblue]%s[/COLOR]\n[COLOR=powderblue]%s[/COLOR]'%(mylist[0],mylist[1],mylist[2],mylist[3]))

highest = Highest_Version(content=mylist,start_point='-',end_point='.zip')
dialog.ok('HIGHEST VERSION', 'The highest version number of your files is:','[COLOR=dodgerblue]%s[/COLOR]'%highest)
~"""
    highest      = 0
    highest_ver  = ''
    for item in content:
        version = item.replace(end_point,'')
        version = version.split(start_point)
        version = version[len(version)-1]
        if version > highest:
            highest      = version
            highest_ver  = item
    return highest_ver
#----------------------------------------------------------------
# TUTORIAL #
def ID_Generator(size=15):
    """
This will generate a random string made up of uppercase & lowercase ASCII
characters and digits - it does not contain special characters.

CODE:  ID_Generator([size])
size is an optional paramater.

AVAILABLE PARAMS:

    size - just send through an integer, this is the length of the string you'll get returned.
    So if you want a password generated that's 20 characters long just use ID_Generator(20). The default is 15.

EXAMPLE CODE:
my_password = koding.ID_Generator(20)
dialog.ok('ID GENERATOR','Password generated:', '', '[COLOR=dodgerblue]%s[/COLOR]' % my_password)
~"""
    import string
    import random

    chars=string.ascii_uppercase + string.digits + string.ascii_lowercase
    return ''.join(random.choice(chars) for _ in range(size))
#---------------------------------------------------------------------------------------------------
# TUTORIAL #
def List_From_Dict(mydict={},use_key=True):
    """
Send through a dictionary and return a list of either the keys or values.
Please note: The returned list will be sorted in alphabetical order.

CODE: List_From_Dict(mydict,[use_key])

AVAILABLE PARAMS:

    (*) mydict  -  This is the dictionary (original data) you want to traverse through.

    use_key  -  By default this is set to True and a list of all your dictionary keys
    will be returned. Set to False if you'd prefer to have a list of the values returned.

EXAMPLE CODE:
raw_data = {'test1':'one','test2':'two','test3':'three','test4':'four','test5':'five'}
mylist1 = koding.List_From_Dict(mydict=raw_data)
mylist2 = koding.List_From_Dict(mydict=raw_data,use_key=False)
koding.Text_Box('LIST_FROM_DICT','Original dictionary: [COLOR dodgerblue]%s[/COLOR][CR][CR]Returned List (use_key=True): [COLOR dodgerblue]%s[/COLOR][CR]Returned List (use_key=False): [COLOR dodgerblue]%s[/COLOR]'%(raw_data,mylist1,mylist2))
~"""
    pos = 1
    if use_key:
        pos = 0
    final_list = []
    for item in mydict.items():
        if item[0]!='' and item[1]!='':
            final_list.append(item[pos])
    return sorted(final_list)
#---------------------------------------------------------------------------------------------------
# TUTORIAL #
def md5_check(src,string=False):
    """
Return the md5 value of string/file/directory, this will return just one unique value.

CODE: md5_check(src,[string])

AVAILABLE PARAMS:

    (*) src  -  This is the source you want the md5 value of.
    This can be a string, path of a file or path to a folder.

    string  -  By default this is set to False but if you want to send
    through a string rather than a path set this to True.

EXAMPLE CODE:
home = koding.Physical_Path('special://home')
home_md5 = koding.md5_check(home)
dialog.ok('md5 Check', 'The md5 of your home folder is:', '[COLOR=dodgerblue]%s[/COLOR]'%home_md5)

guisettings = xbmc.translatePath('special://profile/guisettings.xml')
guisettings_md5 = koding.md5_check(guisettings)
dialog.ok('md5 Check', 'The md5 of your guisettings.xml:', '[COLOR=dodgerblue]%s[/COLOR]'%guisettings_md5)

mystring = 'This is just a random text string we\'ll get the md5 value of'
myvalue = koding.md5_check(src=mystring,string=True)
dialog.ok('md5 String Check', 'String to get md5 value of:', '[COLOR=dodgerblue]%s[/COLOR]'%mystring)
dialog.ok('md5 String Check', 'The md5 value of your string:', '[COLOR=dodgerblue]%s[/COLOR]'%myvalue)
~"""
    import hashlib
    import os

    SHAhash = hashlib.md5()
    if not os.path.exists(src) and not string:
        return -1

# If source is a file
    if string:
        return hashlib.md5(src).hexdigest()
# If source is a file
    elif not os.path.isdir(src):
        return hashlib.md5(open(src,'rb').read()).hexdigest()

# If source is a directory
    else:
        try:
            for root, dirs, files in os.walk(src):
              for names in files:
                filepath = os.path.join(root,names)
                try:
                  f1 = open(filepath, 'rb')
                except:
                  f1.close()
                  continue

            while 1:
# Read file in as little chunks
              buf = f1.read(4096)
              if not buf : break
              SHAhash.update(hashlib.md5(buf).hexdigest())
            f1.close()
        except:
            return -2

        return SHAhash.hexdigest()
#----------------------------------------------------------------
# TUTORIAL #
def Merge_Dicts(*dict_args):
    """
Send through any number of dictionaries and get a return of one merged dictionary.
Please note: If you have duplicate keys the value will be overwritten by the final
dictionary to be checked. So if you send through dicts a-f and the same key exists
in dicts a,e,f the final value for that key would be whatever is set in 'f'.

CODE: Merge_Dicts(*dict_args)

AVAILABLE PARAMS:

    (*) *dict_args  -  Enter as many dictionaries as you want, these will be merged
    into one final dictionary. Please send each dictionary through as a new paramater.

EXAMPLE CODE:
dict1 = {'1':'one','2':'two'}
dict2 = {'3':'three','4':'four','5':'five'}
dict3 = {'6':'six','7':'seven'}
dict4 = {'1':'three','8':'eight'}

mytext = 'Original Dicts:\ndict1 = %s\ndict2 = %s\ndict3 = %s\ndict4 = %s\n\n'%(repr(dict1),repr(dict2),repr(dict3),repr(dict4))
mytext += 'Merged dictionaries (1-3): %s\n\n'%repr(koding.Merge_Dicts(dict1,dict2,dict3))
mytext += 'Merged dictionaries (1-4): %s\n\n'%repr(koding.Merge_Dicts(dict1,dict2,dict3,dict4))
mytext += "[COLOR = gold]IMPORTANT:[/COLOR]\nNotice how on the last run the key '1'now has a value of three.\nThis is because dict4 also contains that same key."
Text_Box('Merge_Dicts',mytext)
~"""
    result = {}
    for dictionary in dict_args:
        if Data_Type(dictionary)=='dict':
            result.update(dictionary)
    return result
#----------------------------------------------------------------
# TUTORIAL #
def Parse_XML(source, block, tags):
    """
Send through the contents of an XML file and pull out a list of matching
items in the form of dictionaries. When checking your results you should
allow for lists to be returned, by default each tag found in the xml will
be returned as a string but if multiple entries of the same tag exists your
dictionary item will be a list. Although this can be used for many uses this
was predominantly added for support of XML's which contain multiple links to video
files using things like <sublink>. When checking to see if a string or list has been
returned you can use the Data_Type function from Koding which will return 'str' or 'list'.

CODE: Parse_XML(source, block, tags)

AVAILABLE PARAMS:

    source  -  This is the original source file, this must already be read into
    memory as a string so made sure you've either used Open_URL or Text_File to
    read the contents before sending through.

    block -  This is the master tag you want to use for creating a dictionary of items.
    For example if you have an xml which contains multiple tags called <item> and you wanted
    to create a dictionary of sub items found in each of these you would just use 'item'.

    tags - This is a list of tags you want to return in your dictionary, so lets say each <item>
    section contains <link>, <title> and <thumb> tags you can return a dictionary of all those
    items by sending through ['link','title','thumb']

EXAMPLE CODE:
dialog.ok('DICTIONARY OF ITEMS','We will now attempt to return a list of the source details pulled from the official Kodi repository addon.xml')
xml_file = koding.Physical_Path('special://xbmc/addons/repository.xbmc.org/addon.xml')
xml_file = koding.Text_File(xml_file,'r')
xbmc.log(xml_file,2)
repo_details = koding.Parse_XML(source=xml_file, block='extension', tags=['info','checksum','datadir'])
counter = 0
for item in repo_details:
    dialog.ok( 'REPO %s'%(counter+1),'info path: [COLOR dodgerblue]%s[/COLOR]\nchecksum path: [COLOR dodgerblue]%s[/COLOR]\ndatadir: [COLOR dodgerblue]%s[/COLOR]' % (repo_details[counter]['info'],repo_details[counter]['checksum'],repo_details[counter]['datadir']) )
    counter += 1
~"""
    from BeautifulSoup import BeautifulSoup
    soup = BeautifulSoup(source)
    my_return = []

# Grab all the blocks of xml to search
    for myblock in soup.findAll(block):
        if myblock:
            my_dict = {}
            for tag in tags:
                newsoup = BeautifulSoup(str(myblock))
                newtag  = newsoup.findAll(tag)
                if newtag:
                    xbmc.log(repr(newtag),2)

                # If only one instance is found we add to dict as a plain string
                    if len(newtag)==1:
                        newtag  = str(newtag).split(r'>')[1]
                        newtag  = newtag.split(r'<')[0]
                
                # Otherwise we add to dict as a list
                    else:
                        tag_array = []
                        for item in newtag:
                            mynewtag  = str(item).split(r'>')[1]
                            mynewtag  = mynewtag.split(r'<')[0]
                            tag_array.append(mynewtag)
                        newtag = tag_array
                    my_dict[tag] = newtag
            my_return.append(my_dict)
    return my_return
#----------------------------------------------------------------
# TUTORIAL #
def Table_Convert(url, contents={}, table=0):
    """
Open a web page which a table and pull out the contents of that table
into a list of dictionaries with your own custom keys.

CODE:   Table_Convert(url, contents, table)

AVAILABLE PARAMS:

    url  -  The url you want to open and pull data from

    contents  -  Send through a dictionary of the keys you want to assign to
    each of the cells. The format would be: {my_key : position}
    You can pull out as many cells as you want, so if your table has 10 columns
    but you only wanted to pull data for cells 2,4,5,6,8 then you could do so
    by setting contents to the following params:
    contents = {"name 1":2, "name 2":4, "name 3":5, "name 4":6, "name 5":8}

    table  -  By default this is set to zero, this is to be used if there's
    multiple tables on the page you're accessing. Remeber to start at zero,
    so if you want to access the 2nd table on the page it will be table=1.

EXAMPLE CODE:
dialog.ok('TABLE DATA','Let\'s pull some details from the proxy list table found at:\nhttps://free-proxy-list.net.')
proxies = koding.Table_Convert(url='https://free-proxy-list.net', contents={"ip":0,"port":1}, table=0)
mytext = '[COLOR dodgerblue]Here are some proxies:[/COLOR]\n'
for item in proxies:
    mytext += '\nIP: %s\nPort: %s\n[COLOR steelblue]----------------[/COLOR]'%(item['ip'],item['port'])
koding.Text_Box('MASTER PROXY LIST',mytext)
~"""
    from web import Open_URL
    from BeautifulSoup import BeautifulSoup
    table_list=[]
    content = Open_URL(url)
    if content:
        rawdata = Parse_XML(content,'table',['td'])

    # Work out the amount of columns in the table
        soup = BeautifulSoup(content)
        my_return = []
        mytable = soup.findAll('table')[table]
        if mytable:
            newsoup = BeautifulSoup(str(mytable))
            newtag  = str( newsoup.find('tr') )
            if '<th' in newtag:
                count_tag = '<th'
            else:
                count_tag = '<td'
            cells = newtag.count(count_tag)

        rows = [rawdata[table]['td'][x:x+cells] for x in range(0, len(rawdata[0]['td']), cells)]
        for row in rows:
            my_dict = {}
            for cell_name in contents:
                my_dict[cell_name] = row[contents[cell_name]]
            table_list.append(my_dict)
        return table_list
    else:
        return {}
#----------------------------------------------------------------
# TUTORIAL #
def Split_Lines(raw_string, size):
    """
Splits up a piece of text into a list of lines x amount of chars in length.

CODE: koding.Split_Lines(raw_string, size)

AVAILABLE PARAMS:

    (*) raw_string  -  This is the text you want split up into lines

    (*) size        -  This is the maximum size you want the line length to be (in characters)

EXAMPLE CODE:
raw_string = 'This is some test code, let\'s take a look and see what happens if we split this up into lines of 20 chars per line'
dialog.ok('ORIGINAL TEXT',raw_string)
my_list = koding.Split_Lines(raw_string,20)
koding.Text_Box('List of lines',str(my_list))
~"""    
    final_list=[""]
    for i in raw_string:
        length = len(final_list)-1
        if len(final_list[length]) < size:
            final_list[length]+=i
        else:
            final_list += [i]
    return final_list
#----------------------------------------------------------------
# TUTORIAL #
def Split_List(source, split_point, include='all'):
    """
Send through a list and split it up into multiple lists. You can choose to create
lists of every x amount of items or you can split at every nth item and only include
specific items in your new list.

CODE: Split_List(source, split_point, include)

AVAILABLE PARAMS:

    source  -  This is the original list you want split

    split_point -  This is the postition you want to split your list at. For example:
    original list: [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    Lets say we want to split it at every 5 items the split point would be 5

    include - You have 3 options here:

        'all' - This will add all items to your lists, so in the example above you will
        get a return of ([1,2,3,4,5],[6,7,8,9,10],[11,12,13,14,15])

        [] - Send through a list of positions you want to include, based on the example
        above and using include=[0,1,3] you will get a return of ([1,2,4],[6,7,9],[11,12,14])

        int - Send through an integer and it will return everything up to that position,
        based on the example above and using include=3 you will get a return of
        ([1,2,3],[6,7,8],[11,12,13])


EXAMPLE CODE:
my_list = ['one','two','three','four','five','six','seven','eight','nine','ten','eleven','twelve','thirteen','fourteen','fifteen']
dialog.ok('SPLIT LIST 1','We will now attempt to split the following list into blocks of 5:\n%s'%my_list)
newlist = koding.Split_List(source=my_list, split_point=5)
dialog.ok('RESULTS','Our returned var:\n%s'%newlist)
dialog.ok('SPLIT LIST 2','We will now attempt to split the same list at every 5th item position and only show items [0,1,3]')
newlist = koding.Split_List(source=my_list, split_point=5, include=[0,1,3])
dialog.ok('RESULTS','Our returned var:\n%s'%newlist)
dialog.ok('SPLIT LIST 3','We will now attempt to split the same list at every 5th item position and only show the first 3 items.')
newlist = koding.Split_List(source=my_list, split_point=5, include=3)
dialog.ok('RESULTS','Our returned var:\n%s'%newlist)
~"""
    if include == 'all':
        return [source[x:x+split_point] for x in range(0, len(source), split_point)]
    elif Data_Type(include) == 'list':
        mylists = [source[x:x+split_point] for x in range(0, len(source), split_point)]
        return_list = []
        for item in mylists:
            mylist = []
            for keep in include:
                mylist.append(item[keep])
            return_list.append(mylist)
        return return_list
    elif Data_Type(include) == 'int':
        return [source[x:x+include] for x in range(0, len(source), split_point)]
#----------------------------------------------------------------
# TUTORIAL #
def String(code='', source=''):
    """
This will return the relevant language skin as set in the
resources/language folder for your add-on. By default you'll get
the language string returned from your current running add-on
but if you send through another add-on id you can grab from
any add-on or even the built-in kodi language strings.

CODE: String(code, [source])

AVAILABLE PARAMS:

    (*) code  -  This is the language string code set in your strings.po file.

    source  -  By default this is set to a blank string and will
    use your current add-on id. However if you want to pull the string
    from another add-on just enter the add-on id in here. If you'd prefer
    to pull from the built-in kodi resources files just set as 'system'.

EXAMPLE CODE:
kodi_string = koding.String(code=10140, source='system')
koding_string = koding.String(code=30825, source='script.module.python.koding.aio')
dialog.ok('SYSTEM STRING','The string [COLOR=dodgerblue]10140[/COLOR] pulled from the default system language resources is:','[COLOR=gold]%s[/COLOR]' % kodi_string)
dialog.ok('PYTHON KODING STRING','The string [COLOR=dodgerblue]30825[/COLOR] pulled from the Python Koding language resources is:','[COLOR=gold]%s[/COLOR]' % koding_string)
~"""
    import xbmcaddon
    from addons import Caller
    if source == '':
        source = Caller()
    if source != 'system':
        addon_id = xbmcaddon.Addon(id=source)
        mystring = addon_id.getLocalizedString(code)
    else:
        mystring = xbmc.getLocalizedString(code)
    return mystring
#----------------------------------------------------------------
# TUTORIAL #
def Remove_Formatting(string, color=True, bold=True, italic=True, spaces=True, dots=True, dashes=True):
    """
This will cleanup a Kodi string, it can remove color, bold and italic tags as well as
preceding spaces, dots and dashes. Particularly useful if you want to show the names of
add-ons in alphabetical order where add-on names have deliberately had certain formatting
added to them to get them to always show at the top of lists.

CODE: Remove_Formatting(string, [color, bold, italic, spaces, dots, dashes])

AVAILABLE PARAMS:

    (*) string  -  This is string you want to remove formatting from.

    color  -  By default this is set to true and all references to the color tag
    will be removed, set this to false if you don't want color formatting removed.

    bold  -  By default this is set to true and all references to the bold tag
    will be removed, set this to false if you don't want bold formatting removed.

    italic  -  By default this is set to true and all references to the italic tag
    will be removed, set this to false if you don't want italic formatting removed.

    spaces  -  By default this is set to true and any spaces at the start of the text
    will be removed, set this to false if you don't want the spaces removed.

    dots  -  By default this is set to true and any dots (.) at the start of the text
    will be removed, set this to false if you don't want the dots removed.

    dashes  -  By default this is set to true and any dashes (-) at the start of the text
    will be removed, set this to false if you don't want the dashes removed.

EXAMPLE CODE:
mystring = '...-- [I]This[/I]  is the [COLOR dodgerblue]ORIGINAL[/COLOR] [B][COLOR cyan]TEXT[/COLOR][/B]'
dialog.ok('ORIGINAL TEXT','Below is the original text we\'re going to try and clean up:[CR]%s'%mystring)
dialog.ok('DOTS REMOVED','[COLOR gold]Original:[/COLOR][CR]%s[CR][COLOR gold]This is with only dots set to True:[/COLOR][CR]%s'%(mystring,koding.Remove_Formatting(mystring, color=False, bold=False, italic=False, spaces=False, dots=True, dashes=False)))
dialog.ok('DOTS & DASHES REMOVED','[COLOR gold]Original:[/COLOR][CR]%s[CR][COLOR gold]This is with dots & dashes set to True:[/COLOR][CR]%s'%(mystring,koding.Remove_Formatting(mystring, color=False, bold=False, italic=False, spaces=False, dots=True, dashes=True)))
dialog.ok('DOTS, DASHES & SPACES REMOVED','[COLOR gold]Original:[/COLOR][CR]%s[CR][COLOR gold]This is with dots, dashes & spaces set to True:[/COLOR][CR]%s'%(mystring,koding.Remove_Formatting(mystring, color=False, bold=False, italic=False, spaces=True, dots=True, dashes=True)))
dialog.ok('ALL FORMATTING REMOVED','[COLOR gold]Original:[/COLOR][CR]%s[CR][COLOR gold]This is with all options set to True:[/COLOR][CR]%s'%(mystring,koding.Remove_Formatting(mystring)))
~"""
    import re
    if color:
        if '[COLOR' in string:
            string = string.replace('[/COLOR]','')
            colorlist = re.compile(r'\[COLOR(.+?)\]').findall(string)
            for colors in colorlist:
                string = string.replace('[COLOR%s]'%colors,'')
    if spaces:
        string = string.strip()
    if bold:
        string = string.replace('[B]','').replace('[/B]','')
    if spaces:
        string = string.strip()
    if italic:
        string = string.replace('[I]','').replace('[/I]','')
    if spaces:
        string = string.strip()
    if dots:
        while string.startswith('.'):
            string = string[1:]
    if spaces:
        string = string.strip()
    if dashes:
        while string.startswith('-'):
            string = string[1:]
    if spaces:
        string = string.strip()
    if spaces:
        string = string.strip()

    return string
