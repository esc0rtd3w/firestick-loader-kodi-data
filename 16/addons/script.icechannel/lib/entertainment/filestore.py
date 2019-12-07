#    Ice Channel

HELPER = 'filestore'

import os    
import datetime
import xbmc
import re
import sys

from entertainment import common

try:
    if  common.addon.get_setting('use_remote_db')=='true' and   \
        common.addon.get_setting('db_address') is not None and  \
        common.addon.get_setting('db_user') is not None and     \
        common.addon.get_setting('db_pass') is not None and     \
        common.addon.get_setting('db_name') is not None:
        import mysql.connector as database
        common.addon.log('-' + HELPER + '- -' +'Loading MySQLdb as DB engine', 2)
        DB = 'mysql'
    else:
        raise ValueError('MySQL not enabled or not setup correctly')
except:
    try: 
        import sqlite3
        from sqlite3 import dbapi2 as database
        common.addon.log('-' + HELPER + '- -' +'Loading sqlite3 as DB engine version: %s' % database.sqlite_version, 2)
    except Exception, e:
        from pysqlite2 import dbapi2 as database
        common.addon.log('-' + HELPER + '- -' +'pysqlite2 as DB engine', 2)
    DB = 'sqlite'
    
class FileStore:

    local_db_name = 'filestore.db'    
    
    def __init__(self):
        
        #Check if a path has been set in the addon settings
        db_path = common.addon.get_setting('local_db_location')
        if db_path:
            self.path = xbmc.translatePath(db_path)
        else:
            self.path = xbmc.translatePath('special://profile/addon_data/script.icechannel/databases')
        
        self.path = common.make_dir(self.path, '')
        
        self.db = os.path.join(self.path, self.local_db_name)
        
        # connect to db at class init and use it globally
        if DB == 'mysql':
            class MySQLCursorDict(database.cursor.MySQLCursor):
                def _row_to_python(self, rowdata, desc=None):
                    row = super(MySQLCursorDict, self)._row_to_python(rowdata, desc)
                    if row:
                        return dict(zip(self.column_names, row))
                    return None
            self.dbcon = database.connect(database=common.addon.get_setting('db_name'), user=common.addon.get_setting('db_user'), 
                password=common.addon.get_setting('db_pass'), host=common.addon.get_setting('db_address'), buffered=True, charset='utf8')                
            self.dbcur = self.dbcon.cursor(cursor_class=MySQLCursorDict, buffered=True)
        else:
            self.dbcon = database.connect(self.db)
            self.dbcon.row_factory = database.Row # return results indexed by field names and not numbers so we can convert to dict
            self.dbcon.text_factory = str
            self.dbcur = self.dbcon.cursor()
                
        self._create_filestore_tables()
        
    def __del__(self):
        ''' Cleanup db when object destroyed '''
        try:
            self.dbcur.close()
            self.dbcon.close()
        except: pass
        
    def _create_filestore_tables(self):
        
        sql_create = "CREATE TABLE IF NOT EXISTS filestore ("\
                            "id TEXT,"\
                            "title TEXT,"\
                            "img TEXT,"\
                            "fanart TEXT,"\
                            "type TEXT,"\
                            "fmt_name TEXT,"\
                            "fmt_display_name TEXT,"\
                            "path TEXT,"\
                            "tmstmp TIMESTAMP,"\
                            "UNIQUE(id)"\
                            ");"
        if DB == 'mysql':
            sql_create = sql_create.replace("id TEXT"  ,"id VARCHAR(32)")
            sql_create = sql_create.replace("title TEXT", "title VARCHAR(50)")
            sql_create = sql_create.replace("type TEXT", "type VARCHAR(50)")
            sql_create = sql_create.replace("fmt_name TEXT", "fmt_name VARCHAR(50)")
            sql_create = sql_create.replace("fmt_display_name TEXT"  ,"fmt_display_name VARCHAR(255)")
            self.dbcur.execute(sql_create)
            try: self.dbcur.execute('CREATE INDEX fsindex on filestore (id);')                
            except: pass
        else:
            self.dbcur.execute(sql_create)
            self.dbcur.execute('CREATE INDEX IF NOT EXISTS fsindex on filestore (id);')
        
        common.addon.log('-' + HELPER + '- -' +'Table filestore initialized', 0)
                        
    def add_file_store(self, title, img, fanart, type, fmt_name, fmt_display_name, path ):
    
        import hashlib
        id = hashlib.md5(path.lower()).hexdigest()
        
        import datetime
        tmstmp = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')

        sql_insert = ''
    
        if DB == 'mysql':
            sql_insert = "INSERT INTO filestore( id, title, img, fanart, type, fmt_name, fmt_display_name, path, tmstmp ) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        else:
            sql_insert = "INSERT INTO filestore( id, title, img, fanart, type, fmt_name, fmt_display_name, path, tmstmp ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)"            
        
        common.addon.log('-' + HELPER + '- -' +'%s: %s, %s, %s, %s, %s, %s, %s, %s, %s' % (sql_insert, id, title, img, fanart, type, fmt_name, fmt_display_name, path, tmstmp), 2)
                    
        try:
            self.dbcur.execute(sql_insert, (id, title, img, fanart, type, fmt_name, fmt_display_name, path, tmstmp) )
            self.dbcon.commit()
        except Exception, e:
            common.addon.log('-' + HELPER + '- - failure: %s' % e )
            pass
            
    def remove_file_store(self, path ):
    
        import hashlib
        id = hashlib.md5(path.lower()).hexdigest()

        sql_delete = ''
    
        if DB == 'mysql':
            sql_delete = "DELETE FROM filestore WHERE id = %s "
        else:
            sql_delete = "DELETE FROM filestore WHERE id = ? "            
        
        common.addon.log('-' + HELPER + '- -' +'%s: %s' % (sql_delete, id), 2)
                    
        try:
            self.dbcur.execute(sql_delete, (id, ) )
            self.dbcon.commit()
        except Exception, e:
            common.addon.log('-' + HELPER + '- - failure: %s' % e )
            pass
            
    def rename_file_store(self, path, title ):
    
        import hashlib
        id = hashlib.md5(path.lower()).hexdigest()

        sql_update = ''
    
        if DB == 'mysql':
            sql_update = "UPDATE filestore SET title = %s WHERE id = %s "
        else:
            sql_update = "UPDATE filestore SET title = ? WHERE id = ? "            
        
        common.addon.log('-' + HELPER + '- -' +'%s: %s, %s' % (sql_update, title, id), 2)
                    
        try:
            self.dbcur.execute(sql_update, (title, id) )
            self.dbcon.commit()
        except Exception, e:
            common.addon.log('-' + HELPER + '- - failure: %s' % e )
            pass
            
    def check_file_store(self, path):
    
        import hashlib
        id = hashlib.md5(path.lower()).hexdigest()
        
        sql_select = ''
        
        if DB == 'mysql':
            sql_select = "SELECT * FROM filestore WHERE id = %s "
        else:
            sql_select = "SELECT * FROM filestore WHERE id = ? "
            
        common.addon.log('-' + HELPER + '- -' +'%s: %s' % (sql_select, id), 2)
        
        store_exists = False
        
        try:
            self.dbcur.execute(sql_select, (id, ) )
            matchedrow = self.dbcur.fetchall()[0]
            store_exists = True
        except Exception, e:
            store_exists = False
            common.addon.log('-' + HELPER + '- - failure: %s' % e )
            pass
        
        return store_exists
        
    def check_file_store_title(self, title):
    
        sql_select = ''
        
        if DB == 'mysql':
            sql_select = "SELECT * FROM filestore WHERE LOWER(title) = LOWER(%s) "
        else:
            sql_select = "SELECT * FROM filestore WHERE LOWER(title) = LOWER(?) "
            
        common.addon.log('-' + HELPER + '- -' +'%s: %s' % (sql_select, title), 2)
        
        store_exists = False
        
        try:
            self.dbcur.execute(sql_select, (title, ) )
            matchedrow = self.dbcur.fetchall()[0]
            store_exists = True
        except Exception, e:
            store_exists = False
            common.addon.log('-' + HELPER + '- - failure: %s' % e )
            pass
        
        return store_exists
            
    def get_filestores(self):
        
        stores = []
        
        sql_select = "SELECT id, title, img, fanart, type, fmt_name, fmt_display_name, path FROM filestore ORDER BY tmstmp DESC "
            
        common.addon.log('-' + HELPER + '- -' +'%s' % sql_select, 2)
        
        try:
            self.dbcur.execute(sql_select)
            for matchedrow in self.dbcur.fetchall():
                data = dict(matchedrow)
                stores.append(data)
        except Exception, e:
            common.addon.log('-' + HELPER + '- - failure: %s' % e )
            pass
            
        return stores
        
    def get_file_id(self, path):
        import hashlib
        return hashlib.md5(path.lower()).hexdigest()
        
    def get_files(self):

        file_titles = ''
        file_ids = ''
        
        from glob import glob
        files = glob( os.path.join( os.path.dirname(common.addon_path), common.addon_id + '.extn.store.*', 'plugins', 'files', '*.py' ) )
        
        import re

        for file in files:
            
            f = open(file, 'r')
            data = f.read()
            f.close()
            
            id = re.search('\#\#--id=(.*)', data)
            if id:
                file_ids += id.group(1) + '|'
                
            title = re.search('\#\#--title=(.*)', data)
            if title:
                file_titles += title.group(1) + '|'
                
        return (file_ids, file_titles)
        
    def get_files_with_details(self):
        
        file_details = []
        
        from glob import glob
        files = glob( os.path.join( os.path.dirname(common.addon_path), common.addon_id + '.extn.store.*', 'plugins', 'files', '*.py' ) )
        
        import re
        
        for file in files:

            f = open(file, 'r')
            data = f.read()
            f.close()
            
            id = re.search('\#\#--id=(.*)', data)
            if id:
                id = id.group(1)
                
            title = re.search('\#\#--title=(.*)', data)
            if title:
                title = title.group(1)
                
            format = re.search('\#\#--format=(.*)', data)
            if format:
                format = format.group(1)
                
            url = re.search('\#\#--url=(.*)', data)
            if url:
                url = url.group(1)
                
            img = re.search('\#\#--img=(.*)', data)
            if img:
                img = img.group(1)
                
            fanart = re.search('\#\#--fanart=(.*)', data)
            if fanart:
                fanart = fanart.group(1)
            
            parents = re.search('\#\#--parents=(.*)', data)
            if parents:
                parents = parents.group(1)
                
            type = re.search('\#\#--type=(.*)', data)
            if type:
                type = type.group(1)
                
            file_details.append( { 'id':id, 'title':title, 'name':title, 'format':format, 'url':url, 'path':url, 'img':img, 
                'fanart':fanart, 'parents':parents, 'type':type } )
                
        return file_details
        
    def check_file(self, path):
        
        (file_ids, file_titles) = self.get_files()
        
        if self.get_file_id() in file_ids:
            return True
            
        return False
        
    def check_file_title(self, title):
        
        (file_ids, file_titles) = self.get_files()
        
        if title in file_titles:
            return True
            
        return False

    def update_files(self):
        
        from entertainment import istream as entertainment
        entertainment.loadiStreamPlugins(load_fileformats=True)
        
        ff_objs = {}
        
        file_details = self.get_files_with_details()
        
        for file_detail in file_details:
            ff_obj = ff_objs.get(file_detail['format'], None)
            if not ff_obj:
                ff_obj = entertainment.GetFileFormatObj(file_detail['format'])
                
            if not ff_obj: continue
            
            ff_obj.AddItem(file_detail, file_detail['title'], file_detail['name'], file_detail['parents'])
                
