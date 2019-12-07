#    Ice Channel

HELPER = 'mystream'

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
    
class MyStream:

    local_db_name = 'mystream.db'    
    
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
                
        self._create_mystream_tables()
        
    def __del__(self):
        ''' Cleanup db when object destroyed '''
        try:
            self.dbcur.close()
            self.dbcon.close()
        except: pass
        
    def _create_mystream_tables(self):
        
        sql_create = "CREATE TABLE IF NOT EXISTS mystream ("\
                            "id TEXT,"\
                            "title TEXT,"\
                            "display_title TEXT,"\
                            "img TEXT,"\
                            "fanart TEXT,"\
                            "path TEXT,"\
                            "UNIQUE(id)"\
                            ");"
        if DB == 'mysql':
            sql_create = sql_create.replace("id TEXT"  ,"id VARCHAR(32)")
            self.dbcur.execute(sql_create)
            try: self.dbcur.execute('CREATE INDEX mystreamindex on mystream (id);')                
            except: pass
        else:
            self.dbcur.execute(sql_create)
            self.dbcur.execute('CREATE INDEX IF NOT EXISTS mystreamindex on mystream (id);')
        
        common.addon.log('-' + HELPER + '- -' +'Table mystream initialized', 0)
                        
    def add_mystream_item(self, title, img, fanart, path ):
        
        import re
        regex = re.compile('\[/?(?:color|b|i)[^\]]*\]', re.I)
        clean_title = regex.sub('', title)
        
        import hashlib
        id = hashlib.md5(clean_title.lower()).hexdigest()
        
        success = True
        
        sql_insert = ''
    
        if DB == 'mysql':
            sql_insert = "INSERT INTO mystream( id, title, display_title, img, fanart, path ) VALUES(%s, %s, %s, %s, %s, %s)"
        else:
            sql_insert = "INSERT INTO mystream( id, title, display_title, img, fanart, path ) VALUES(?, ?, ?, ?, ?, ?)"            
        
        common.addon.log('-' + HELPER + '- -' +'%s: %s, %s, %s, %s, %s, %s' % (sql_insert, id, clean_title, title, img, fanart, path), 2)
                    
        try:
            self.dbcur.execute(sql_insert, (id, clean_title, title, img, fanart, path) )
            self.dbcon.commit()
        except Exception, e:
            common.addon.log('-' + HELPER + '- - failure: %s' % e )
            success = False
            pass
            
        return success
            
    def remove_mystream_item(self, title ):
    
        import re
        regex = re.compile('\[/?(?:color|b|i)[^\]]*\]', re.I)
        clean_title = regex.sub('', title)
    
        import hashlib
        id = hashlib.md5(clean_title.lower()).hexdigest()
        
        success = True

        sql_delete = ''
    
        if DB == 'mysql':
            sql_delete = "DELETE FROM mystream WHERE id = %s "
        else:
            sql_delete = "DELETE FROM mystream WHERE id = ? "            
        
        common.addon.log('-' + HELPER + '- -' +'%s: %s' % (sql_delete, id), 2)
                    
        try:
            self.dbcur.execute(sql_delete, (id, ) )
            self.dbcon.commit()
        except Exception, e:
            common.addon.log('-' + HELPER + '- - failure: %s' % e )
            success = False
            pass
            
        return success
            
    def check_mystream(self, title):
    
        import re
        regex = re.compile('\[/?(?:color|b|i)[^\]]*\]', re.I)
        clean_title = regex.sub('', title)
    
        import hashlib
        id = hashlib.md5(clean_title.lower()).hexdigest()
        
        sql_select = ''
        
        if DB == 'mysql':
            sql_select = "SELECT * FROM mystream WHERE id = %s "
        else:
            sql_select = "SELECT * FROM mystream WHERE id = ? "
            
        common.addon.log('-' + HELPER + '- -' +'%s: %s' % (sql_select, id), 2)
        
        item_exists = False
        
        try:
            self.dbcur.execute(sql_select, (id, ) )
            matchedrow = self.dbcur.fetchall()[0]
            item_exists = True
        except Exception, e:
            item_exists = False
            common.addon.log('-' + HELPER + '- - failure: %s' % e )
            pass
        
        return item_exists
        
    def get_mystream_items(self):
        
        items = []
        
        sql_select = "SELECT id, title, display_title, img, fanart, path FROM mystream ORDER BY title ASC "
            
        common.addon.log('-' + HELPER + '- -' +'%s' % sql_select, 2)
        
        try:
            self.dbcur.execute(sql_select)
            for matchedrow in self.dbcur.fetchall():
                data = dict(matchedrow)
                items.append(data)
        except Exception, e:
            common.addon.log('-' + HELPER + '- - failure: %s' % e )
            pass
            
        return items
        
    def rename_mystream_item(self, title, new_display_title):
        
        import re
        regex = re.compile('\[/?(?:color|b|i)[^\]]*\]', re.I)
        clean_title = regex.sub('', title)
        
        import hashlib
        id = hashlib.md5(clean_title.lower()).hexdigest()
        
        success = True

        sql_update = ''
    
        if DB == 'mysql':
            sql_update = "UPDATE mystream SET display_title = %s where id = %s"
        else:
            sql_update = "UPDATE mystream SET display_title = ? where id = ?"
        
        common.addon.log('-' + HELPER + '- -' +'%s: %s, %s' % (sql_update, new_display_title, id), 2)
                    
        try:
            self.dbcur.execute(sql_update, (new_display_title, id ) )
            self.dbcon.commit()
        except Exception, e:
            common.addon.log('-' + HELPER + '- - failure: %s' % e )
            success = False
            pass
            
        return success
