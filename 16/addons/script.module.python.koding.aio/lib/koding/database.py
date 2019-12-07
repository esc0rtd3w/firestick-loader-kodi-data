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
try: from sqlite3 import dbapi2 as database
except: from pysqlite2 import dbapi2 as database

import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs
from __init__ import Caller
from filetools import Physical_Path

# Put this in a try statement, when called from a service it will throw an error otherwise
try:
    try:
        ADDON_ID = xbmcaddon.Addon().getAddonInfo('id')
    except:
        ADDON_ID = Caller()

    AddonVersion     = xbmcaddon.Addon(id=ADDON_ID).getAddonInfo('version')
    profile_path     = xbmcaddon.Addon(id=ADDON_ID).getAddonInfo('profile')
    addon_db_path    = Physical_Path(os.path.join(profile_path,'database.db'))
except:
    pass

dbcur, dbcon     = None, None
dialog = xbmcgui.Dialog()
#----------------------------------------------------------------
def _connect_to_db():
    """ internal command ~"""
    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    xbmcvfs.mkdirs(profile_path)
    db_location = os.path.join(profile_path.decode('utf-8'),'database.db')
    db_location = Physical_Path(db_location)
    dbcon = database.connect(db_location)
    dbcon.row_factory = dict_factory
    dbcur = dbcon.cursor()
    return (dbcur, dbcon)
#----------------------------------------------------------------
def _execute_db_string(sql_string, commit = True):
    """ internal command ~"""
    global dbcur, dbcon
    if dbcur is None or dbcon is None:
        dbcur, dbcon = _connect_to_db()
    dbcur.execute(sql_string)
    if commit:
        dbcon.commit()
    results = []
    for result in dbcur:
        results.append(result)
    return results
#----------------------------------------------------------------
# TUTORIAL #
def Add_To_Table(table, spec, abort_on_error=False):
    """
Add a row to the table in /userdata/addon_data/<your_addon_id>/database.db

CODE:  Add_To_Table(table, spec)

AVAILABLE PARAMS:

    (*) table  -  The table name you want to query

    (*) spec   -  Sent through as a dictionary this is the colums and constraints.

    abort_on_error  -  Default is set to False but set to True if you want to abort
    the process when it hits an error.
    
EXAMPLE CODE:
create_specs = {"columns":{"name":"TEXT", "id":"TEXT"}}
koding.Create_Table("test_table", create_specs)
add_specs1 = {"name":"YouTube", "id":"plugin.video.youtube"}
add_specs2 = {"name":"vimeo","id":"plugin.video.vimeo"}
koding.Add_To_Table("test_table", add_specs1)
koding.Add_To_Table("test_table", add_specs2)
results = koding.Get_All_From_Table("test_table")
final_results = ''
for item in results:
    final_results += 'ID: %s | Name: %s\n'%(item["id"], item["name"])
koding.Text_Box('DB RESULTS', final_results)
koding.Remove_Table('test_table')
~"""
    global dbcon
    sql_string = "INSERT INTO %s (" % table
    keys = []
    values = []
    if type(spec) != list:
        spec = [spec]
    for item in spec:
        for key in item.keys():
            keys.append(key)
            values.append(item[key])
        for key in keys:
            sql_string += "%s, " % key
        sql_string = sql_string[:-2]
        sql_string += ") Values ("
        for value in values:
            sql_string += "\"%s\", " % value
        sql_string = sql_string[:-2]
        sql_string += ")"
        try:
            _execute_db_string(sql_string, commit=False)
        except:
            if abort_on_error:
                dbcon.rollback()
                raise Exception()
            continue
    dbcon.commit()
#----------------------------------------------------------------
# TUTORIAL #
def Add_Multiple_To_Table(table, keys=[], values=[]):
    """
This will allow you to add multiple rows to a table in one big (fast) bulk command
The db file is: /userdata/addon_data/<your_addon_id>/database.db

CODE:  Add_To_Table(table, spec)

AVAILABLE PARAMS:

    (*) table  -  The table name you want to query

    (*) keys   -  Send through a list of keys you want to add to

    (*) values -  A list of values you want to add, this needs to be
    a list of lists (see example below)

EXAMPLE CODE:
create_specs = {"columns":{"name":"TEXT", "id":"TEXT"}}
koding.Create_Table("test_table", create_specs)
dialog.ok('ADD TO TABLE','Lets add the details of 3 add-ons to "test_table" in our database.')
mykeys = ["name","id"]
myvalues = [("YouTube","plugin.video.youtube"), ("vimeo","plugin.video.vimeo"), ("test2","plugin.video.test2")]
koding.Add_Multiple_To_Table(table="test_table", keys=mykeys, values=myvalues)
results = koding.Get_All_From_Table("test_table")
final_results = ''
for item in results:
    final_results += 'ID: %s | Name: %s\n'%(item["id"], item["name"])
koding.Text_Box('DB RESULTS', 'Below are details of the items pulled from our db:\n\n%s'%final_results)
koding.Remove_Table('test_table')
~"""
    dbcur, dbcon = _connect_to_db()
    sql_string = "INSERT INTO %s (" % table
    sql_2  = ''
    if type(keys) != list:
        keys = [keys]
    if type(values) != list:
        values = [values]
    for item in keys:
        if not item.startswith('`'):
            item = r'`'+item
        if not item.endswith('`'):
            item = item+r'`'
        xbmc.log('ITEM: %s'%item,2)
        sql_string += "%s, " % item
        sql_2 += "?,"
    sql_string = "%s) VALUES (%s)"%(sql_string[:-2], sql_2[:-1])
    dbcur.executemany(sql_string, values)
    dbcon.commit()
#----------------------------------------------------------------
# TUTORIAL #
def Create_Table(table, spec):
    """
Create a new table in the database at /userdata/addon_data/<your_addon_id>/database.db

CODE:  Create_Table(table, spec)

AVAILABLE PARAMS:

    (*) table  -  The table name you want to query

    (*) spec   -  Sent through as a dictionary this is the colums and constraints.

EXAMPLE CODE:
create_specs = { "columns":{"name":"TEXT", "id":"TEXT"}, "constraints":{"unique":"id"} }
koding.Create_Table("test_table", create_specs)
dialog.ok('TABLE CREATED','A new table has been created in your database and the id column has been set as UNIQUE.')
my_specs = {"name":"YouTube", "id":"plugin.video.youtube"}
try:
    koding.Add_To_Table("test_table", my_specs)
    koding.Add_To_Table("test_table", my_specs)
except:
    dialog.ok('FAILED TO ADD','Could not add duplicate items because the the column "id" is set to be UNIQUE')
results = koding.Get_All_From_Table("test_table")
final_results = ''
for item in results:
    final_results += 'ID: %s | Name: %s\n'%(item["id"], item["name"])
koding.Text_Box('DB RESULTS', final_results)
koding.Remove_Table('test_table')
~"""
    sql_string = "CREATE TABLE IF NOT EXISTS %s (" % table
    columns = spec.get("columns", {})
    constraints = spec.get("constraints", {})
    for key in columns.keys():
        if not columns[key]:
            columns[key] = "TEXT"
        sql_string += "%s %s, " % (key, columns[key])

    for key in constraints.keys():
        sql_string += "%s(%s), " % (key, constraints[key])
    sql_string = sql_string[:-2]
    sql_string += ");"
    _execute_db_string(sql_string)
#----------------------------------------------------------------
# TUTORIAL #
def DB_Query(db_path, query, values=''):
    """
Open a database and either return an array of results with the SELECT SQL command or perform an action such as INSERT, UPDATE, CREATE.

CODE:  DB_Query(db_path, query, [values])

AVAILABLE PARAMS:

    (*) db_path -  the full path to the database file you want to access.
    
    (*) query   -  this is the actual db query you want to process, use question marks for values

    values  -  a list of values, even if there's only one value it must be sent through as a list item.

IMPORTANT: Directly accessing databases which are outside of your add-ons domain is very much frowned
upon. If you need to access a built-in kodi database (as shown in example below) you should always use
the JSON-RPC commands where possible. 

EXAMPLE CODE:
import filetools
dbpath = filetools.DB_Path_Check('addons')
db_table = 'addon'
kodi_version = int(float(xbmc.getInfoLabel("System.BuildVersion")[:2]))
if kodi_version >= 17:
    db_table = 'addons'
db_query = koding.DB_Query(db_path=dbpath, query='SELECT * FROM %s WHERE addonID LIKE ? AND addonID NOT LIKE ?'%db_table, values=['%youtube%','%script.module%'])
koding.Text_Box('DB SEARCH RESULTS',str(db_query))
~"""
    db_dict = []
    db_path = Physical_Path(db_path)
    con = database.connect(db_path)
    cur = con.cursor()
    
    if query.upper().startswith('SELECT'):
        if values == '':
            cur.execute(query)
        else:
            cur.execute(query, values)

        names = list(map(lambda x: x[0], cur.description))

        for rows in iter(cur.fetchmany, []):
            for row in rows:
                temp_dict = {}
                for idx, col in enumerate(cur.description):
                    temp_dict[col[0]] = row[idx]
                db_dict.append(temp_dict)
        return db_dict

    elif query.upper().startswith('CREATE'):
        cur.execute(query)
        con.commit()

# ANY NON SELECT QUERY (UPDATE, INSERT ETC.)
    else:
        try:
            if values == '':
                cur.executemany(query)
                con.commit()
            else:
                cur.executemany(query, values)
                con.commit()
        except:
            if values == '':
                cur.execute(query)
                con.commit()
            else:
                cur.execute(query, values)
                con.commit()

    cur.close()
#----------------------------------------------------------------
# TUTORIAL #
def Get_All_From_Table(table):
    """
Return a list of all entries from a specific table in /userdata/addon_data/<your_addon_id>/database.db

CODE:  Get_All_From_Table(table)

AVAILABLE PARAMS:

    (*) table  -  The table name you want to query

EXAMPLE CODE:
create_specs = {"columns":{"name":"TEXT", "id":"TEXT"}}
koding.Create_Table("test_table", create_specs)
add_specs1 = {"name":"YouTube", "id":"plugin.video.youtube"}
add_specs2 = {"name":"vimeo","id":"plugin.video.vimeo"}
koding.Add_To_Table("test_table", add_specs1)
koding.Add_To_Table("test_table", add_specs2)
results = koding.Get_All_From_Table("test_table")
final_results = ''
for item in results:
    final_results += 'ID: %s | Name: %s\n'%(item["id"], item["name"])
koding.Text_Box('DB RESULTS', final_results)
koding.Remove_Table('test_table')
~"""
    try:
        return _execute_db_string("SELECT * FROM %s" % table)
    except:
        return []
#----------------------------------------------------------------
# TUTORIAL #
def Get_From_Table(table, spec=None, default_compare_operator="="):
    """
Return a list of all entries matching a specific criteria from the
database stored at: /userdata/addon_data/<your_addon_id>/database.db

CODE:  Get_From_Table(table, spec, compare_operator)

AVAILABLE PARAMS:

    (*) table  -  The table name you want to query

    spec  -  This is the query value, sent through as a dictionary.

    default_compare_operator  -  By default this is set to '=' but could be any
    other SQL query string such as 'LIKE', 'NOT LIKE', '!=' etc.

EXAMPLE CODE:
create_specs = {"columns":{"name":"TEXT", "id":"TEXT"}}
koding.Create_Table("test_table", create_specs)
add_specs1 = {"name":"YouTube", "id":"plugin.video.youtube"}
add_specs2 = {"name":"vimeo","id":"plugin.video.vimeo"}
koding.Add_To_Table("test_table", add_specs1)
koding.Add_To_Table("test_table", add_specs2)
results = koding.Get_From_Table(table="test_table", spec={"name":"%vim%"}, default_compare_operator="LIKE")
final_results = ''
for item in results:
    final_results += 'ID: %s | Name: %s\n'%(item["id"], item["name"])
koding.Text_Box('DB CONTENTS', final_results)
koding.Remove_Table('test_table')
~"""
    if spec == None:
        return Get_All_From_Table()
    sql_string = "SELECT * FROM %s WHERE " % table
    for key in spec.keys():
        if type(spec[key]) == dict:
            value = spec[key]["value"]
            column_compare_operator = spec[key].get("compare_operator", default_compare_operator)
        else:
            value = spec[key]
            column_compare_operator = default_compare_operator
        sql_string += "%s %s \"%s\" AND " % (key, column_compare_operator, value)
    sql_string = sql_string[:-5]
    try:
        return _execute_db_string(sql_string, commit=False)
    except:
        return []
#----------------------------------------------------------------
# TUTORIAL #
def Remove_From_Table(table, spec, default_compare_operator="=", abort_on_error=False):
    """
Remove entries in the db table at /userdata/addon_data/<your_addon_id>/database.db

CODE:  Remove_From_Table(table, spec, [compare_operator])

AVAILABLE PARAMS:

    (*) table  -  The table name you want to query

    spec  -  This is the query value, sent through as a dictionary.

    default_compare_operator  -  By default this is set to '=' but could be any
    other SQL query string such as 'LIKE', 'NOT LIKE', '!=' etc.

EXAMPLE CODE:
create_specs = {"columns":{"name":"TEXT", "id":"TEXT"}}
koding.Create_Table(table="test_table", spec=create_specs)
add_specs1 = {"name":"YouTube", "id":"plugin.video.youtube"}
add_specs2 = {"name":"vimeo","id":"plugin.video.vimeo"}
koding.Add_To_Table(table="test_table", spec=add_specs1)
koding.Add_To_Table(table="test_table", spec=add_specs2)
results = koding.Get_All_From_Table(table="test_table")
final_results = ''
for item in results:
    final_results += 'ID: %s | Name: %s\n'%(item["id"], item["name"])
koding.Text_Box('DB CONTENTS', final_results)
dialog.ok('REMOVE ITEM','We will now remove vimeo from the table, lets see if it worked...')
koding.Remove_From_Table(table="test_table", spec={"name":"vimeo"})
results = koding.Get_All_From_Table(table="test_table")
final_results = ''
for item in results:
    final_results += 'ID: %s | Name: %s\n'%(item["id"], item["name"])
koding.Text_Box('NEW DB CONTENTS', final_results)
koding.Remove_Table('test_table')
~"""
    global dbcon
    sql_string = "DELETE FROM %s WHERE " % table
    if type(spec) != list:
        spec = [spec]
    for item in spec:
        for key in item.keys():
            if type(item[key]) == dict:
                value = item[key]["value"]
                column_compare_operator = item[key].get("compare_operator", default_compare_operator)
            else:
                value = item[key]
                column_compare_operator = default_compare_operator
            sql_string += "%s %s \"%s\" AND " % (key, column_compare_operator, value)
        sql_string = sql_string[:-4]
        try:
            _execute_db_string(sql_string, commit=False)
        except:
            if abort_on_error:
                dbcon.rollback()
                raise Exception()
            continue
    dbcon.commit()
#----------------------------------------------------------------
# TUTORIAL #
def Remove_Table(table):
    """
Use with caution, this will completely remove a database table and
all of it's contents. The only database you can access with this command
is your add-ons own db file called database.db

CODE:  Remove_Table(table)

AVAILABLE PARAMS:

    (*) table  -  This is the name of the table you want to permanently delete.

EXAMPLE CODE:
dialog.ok('REMOVE TABLE','It\'s a bit pointless doing this as you can\'t physically see what\'s happening so you\'ll just have to take our word it works!')
koding.Remove_Table('test_table')
~"""
    sql_string = "DROP TABLE IF EXISTS %s;" % table
    _execute_db_string(sql_string)
#----------------------------------------------------------------
def reset_db():
    global dbcon, dbcur
    dbcur, dbcon     = None, None