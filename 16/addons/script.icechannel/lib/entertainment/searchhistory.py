#    Ice Channel

HELPER = 'searchhistory'

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
    
class SearchHistory:

    local_db_name = 'searchhistory.db'    
    
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
                
        self._create_subscription_tables()
        
    def __del__(self):
        ''' Cleanup db when object destroyed '''
        try:
            self.dbcur.close()
            self.dbcon.close()
        except: pass
        
    def _create_subscription_tables(self):
        
        sql_create = "CREATE TABLE IF NOT EXISTS searchhistory ("\
                            "id TEXT,"\
                            "indexer_type TEXT,"\
                            "search_term TEXT,"\
                            "tmstmp TIMESTAMP,"\
                            "UNIQUE(id)"\
                            ");"
        if DB == 'mysql':
            sql_create = sql_create.replace("id TEXT"  ,"id VARCHAR(32)")
            sql_create = sql_create.replace("indexer_type TEXT", "indexer_type VARCHAR(50)")
            sql_create = sql_create.replace("search_term TEXT"  ,"search_term VARCHAR(255)")
            self.dbcur.execute(sql_create)
            try: self.dbcur.execute('CREATE INDEX shindex on searchhistory (id);')                
            except: pass
            try: self.dbcur.execute('CREATE INDEX shtmindex on searchhistory (tmstmp);')                
            except: pass
        else:
            self.dbcur.execute(sql_create)
            self.dbcur.execute('CREATE INDEX IF NOT EXISTS shindex on searchhistory (id);')
            self.dbcur.execute('CREATE INDEX IF NOT EXISTS shtmindex on searchhistory (tmstmp);')
        
        common.addon.log('-' + HELPER + '- -' +'Table searchhistory initialized', 0)
                        
    def get_searchhistory(self, indexer_type ):
        
        search_terms = []
        
        sql_select = ''
        
        if DB == 'mysql':
            sql_select = "SELECT search_term FROM searchhistory WHERE indexer_type = %s ORDER BY tmstmp DESC "
        else:
            sql_select = "SELECT search_term FROM searchhistory WHERE indexer_type = ? ORDER BY tmstmp DESC "
            
        common.addon.log('-' + HELPER + '- -' +'%s: %s' % (sql_select, indexer_type), 2)
        
        try:
            self.dbcur.execute(sql_select, (indexer_type, ) )
            for matchedrow in self.dbcur.fetchall():
                data = dict(matchedrow)
                search_terms.append(data['search_term'])
        except Exception, e:
            common.addon.log('-' + HELPER + '- - failure: %s' % e )
            pass
        return search_terms            
    
    def clear_search_history(self):
   
        sql_delete = 'DELETE FROM searchhistory'
        success = False
        
        try:
            common.addon.log('-' + HELPER + '- -' + sql_delete, 2)
            self.dbcur.execute( sql_delete )
            self.dbcon.commit()
            success = True
        except Exception, e:
            common.addon.log('-' + HELPER + '- - failure: %s' % e )
            pass            
        finally:
            return success
    
    def cleanup_search_history(self):
        sql_select_distinct_search_types = 'SELECT DISTINCT indexer_type FROM searchhistory'
        
        items_to_keep_in_search_history = '20'
        sql_delete = ''
        if DB == 'mysql':
            sql_delete = "DELETE FROM searchhistory WHERE indexer_type = %s AND id NOT IN (SELECT id FROM searchhistory WHERE indexer_type = %s ORDER BY tmstmp DESC LIMIT %s)" 
        else:
            sql_delete = "DELETE FROM searchhistory WHERE indexer_type = ? AND id NOT IN (SELECT id FROM searchhistory WHERE indexer_type = ? ORDER BY tmstmp DESC LIMIT ?)"
        
        try:
            common.addon.log('-' + HELPER + '- -' + '%s' % sql_select_distinct_search_types, 2)
            self.dbcur.execute(sql_select_distinct_search_types)
            matchedrows = self.dbcur.fetchall()
            for matchedrow in matchedrows:
                data = dict(matchedrow)
                try:
                    common.addon.log('-' + HELPER + '- -' + sql_delete, 2)
                    self.dbcur.execute(sql_delete, ( data['indexer_type'], data['indexer_type'], items_to_keep_in_search_history ) )
                    self.dbcon.commit()
                except Exception, e:
                    common.addon.log('-' + HELPER + '- - failure: %s' % e )
                    pass            
        except Exception, e:
            common.addon.log('-' + HELPER + '- - failure: %s' % e )
            pass
    
    def add_search_term(self, indexer_type, search_term ):
    
        import hashlib
        id = hashlib.md5(indexer_type + ' - ' + search_term).hexdigest()
        
        import datetime
        tmstmp = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        
        try:
            sql_select = ''
            if DB == 'mysql':
                sql_select = "SELECT * FROM searchhistory WHERE id = %s " 
            else:
                sql_select = "SELECT * FROM searchhistory WHERE id = ? " 
            self.dbcur.execute(sql_select, (id, ) )    
            
            matchedrow = self.dbcur.fetchall()[0]
            
            sql_update = ''
        
            if DB == 'mysql':
                sql_update = "UPDATE searchhistory SET tmstmp = %s WHERE id = %s "
            else:
                sql_update = "UPDATE searchhistory SET tmstmp = ? WHERE id = ? "
                        
            common.addon.log('-' + HELPER + '- -' +'%s: %s, %s' % (sql_update, tmstmp, id), 2)
                
            try:
                self.dbcur.execute(sql_update, (tmstmp, id) )
                self.dbcon.commit()
            except Exception, e:
                common.addon.log('-' + HELPER + '- - failure: %s' % e )
                pass
            
        except:
        
            sql_insert = ''
        
            if DB == 'mysql':
                sql_insert = "INSERT INTO searchhistory( id, indexer_type, search_term, tmstmp ) VALUES(%s, %s, %s, %s)"
            else:
                sql_insert = "INSERT INTO searchhistory( id, indexer_type, search_term, tmstmp ) VALUES(?, ?, ?, ?)"            
            
            common.addon.log('-' + HELPER + '- -' +'%s: %s, %s, %s, %s' % (sql_insert, id, indexer_type, search_term, tmstmp), 2)
                        
            try:
                self.dbcur.execute(sql_insert, (id, indexer_type, search_term, tmstmp) )
                self.dbcon.commit()
            except Exception, e:
                common.addon.log('-' + HELPER + '- - failure: %s' % e )
                pass
                
            pass
            