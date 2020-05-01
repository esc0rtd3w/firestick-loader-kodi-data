#    Ice Channel

HELPER = 'subscriptions'

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
    
class Subscriptions:

    local_db_name = 'subscriptions.db'    
    
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
        
        sql_create = "CREATE TABLE IF NOT EXISTS subscriptions ("\
                            "indexer_type TEXT,"\
                            "indexer_id TEXT,"\
                            "type TEXT,"\
                            "video_type TEXT,"\
                            "title TEXT,"\
                            "name TEXT,"\
                            "year TEXT,"\
                            "imdb_id TEXT,"\
                            "url TEXT,"\
                            "UNIQUE(indexer_type, indexer_id, type, video_type, name, year)"\
                            ");"
        if DB == 'mysql':
            sql_create = sql_create.replace("indexer_type TEXT", "indexer_type VARCHAR(25)")
            sql_create = sql_create.replace("indexer_id TEXT"  ,"indexer_id VARCHAR(25)")
            sql_create = sql_create.replace(",type TEXT"  ,",type VARCHAR(20)")
            sql_create = sql_create.replace("video_type TEXT"  ,"video_type VARCHAR(20)")
            sql_create = sql_create.replace("name TEXT"  ,"name VARCHAR(200)")
            sql_create = sql_create.replace("year TEXT"  ,"year VARCHAR(10)")
            sql_create = sql_create.replace("imdb_id TEXT"  ,"imdb_id VARCHAR(20)")
            self.dbcur.execute(sql_create)
            try: self.dbcur.execute('CREATE INDEX subsindex on subscriptions (indexer_type, indexer_id, type, video_type, name, year);')                
            except: pass
        else:
            self.dbcur.execute(sql_create)
            self.dbcur.execute('CREATE INDEX IF NOT EXISTS subsindex on subscriptions (indexer_type, indexer_id, type, video_type, name, year);')
        
        common.addon.log('-' + HELPER + '- -' +'Table subscriptions initialized', 0)
        
    def is_subscribed(self, indexer_type, indexer_id, type, video_type, name, year, url, title='', imdb_id=''):
        
        if self.is_indexer_subscribed(indexer_type, indexer_id, type, video_type, name, year) == True:
            return True
            
        if self.is_item_subscribed(indexer_type, type, video_type, name, year) == True:
            return not self.add_subscription(indexer_type, indexer_id, type, video_type, name, year, url, title, imdb_id)
            
        return False
            
        
    
    def is_item_subscribed(self, indexer_type, type, video_type, name, year):
    
        subscribed = True
        
        try:
            sql_select = ''
            if DB == 'mysql':
                sql_select = "SELECT url FROM subscriptions WHERE indexer_type = %s AND type = %s AND video_type = %s AND name = %s AND year = %s " 
            else:
                sql_select = "SELECT url FROM subscriptions WHERE indexer_type = ? AND type = ? AND video_type = ? AND name = ? AND year = ? " 
            self.dbcur.execute(sql_select, (indexer_type, type, video_type, name, year) )    
            matchedrow = self.dbcur.fetchall()[0]
        except:
            subscribed = False
            
        return subscribed
        
    def is_indexer_subscribed(self, indexer_type, indexer_id, type, video_type, name, year):
    
        indexer_subscribed = True
        
        try:
            sql_select = ''
            if DB == 'mysql':
                sql_select = "SELECT url FROM subscriptions WHERE indexer_type = %s AND indexer_id = %s AND type = %s AND video_type = %s AND name = %s AND year = %s " 
            else:
                sql_select = "SELECT url FROM subscriptions WHERE indexer_type = ? AND indexer_id = ? AND type = ? AND video_type = ? AND name = ? AND year = ? " 
            self.dbcur.execute(sql_select, (indexer_type, indexer_id, type, video_type, name, year) )    
            matchedrow = self.dbcur.fetchall()[0]
        except:
            indexer_subscribed = False
            
        return indexer_subscribed
        
    def add_subscription(self, indexer_type, indexer_id, type, video_type, name, year, url, title='', imdb_id=''):
        
        error = False
        
        if title == '' or not title:
            title = name
            if year and year != '0':
                title = title + ' (' + year + ')'
                
        sql_insert = ''
        
        if DB == 'mysql':
            sql_insert = "INSERT INTO subscriptions( indexer_type, indexer_id, type, video_type, name, year, url, title, imdb_id ) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        else:
            sql_insert = "INSERT INTO subscriptions( indexer_type, indexer_id, type, video_type, name, year, url, title, imdb_id ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)"            
                            
        common.addon.log('-' + HELPER + '- -' +'%s: %s, %s, %s, %s, %s, %s, %s, %s, %s' % (sql_insert, indexer_type, indexer_id, type, video_type, name, year, url, title, imdb_id), 2)
        
        try:
            self.dbcur.execute(sql_insert, (indexer_type, indexer_id, type, video_type, name, year, url, title, imdb_id) )
            self.dbcon.commit()
            common.addon.log('-' + HELPER + '- - success')
        except Exception, e:
            common.addon.log('-' + HELPER + '- - failure: %s' % e )
            error = True
            pass
            
        return error
                
         
                
    def cancel_subscription(self, indexer_type, type, video_type, name, year):
        
        error = False
        
        sql_delete = ''
        if self.is_item_subscribed(indexer_type, type, video_type, name, year) == True:
            if DB == 'mysql':
                sql_delete = "DELETE FROM subscriptions WHERE indexer_type = %s AND type = %s AND video_type = %s AND name = %s AND year = %s "
            else:
                sql_delete = "DELETE FROM subscriptions WHERE indexer_type = ? AND type = ? AND video_type = ? AND name = ? AND year = ? "            
                                
            common.addon.log('-' + HELPER + '- -' +'%s: %s, %s, %s, %s, %s' % (sql_delete, indexer_type, type, video_type, name, year), 2)
            
            try:
                self.dbcur.execute(sql_delete, (indexer_type, type, video_type, name, year ) )
                self.dbcon.commit()
                common.addon.log('-' + HELPER + '- - success')
            except Exception, e:
                common.addon.log('-' + HELPER + '- - failure: %s' % e )
                error = True
                pass
                
        return error
                
    def get_subscriptions(self, indexer_type, type, video_type ):
        
        subs = []
        
        sql_select = ''
        
        if DB == 'mysql':
            sql_select = "SELECT indexer_id, title, name, year, imdb_id, url FROM subscriptions WHERE indexer_type = %s AND type = %s AND video_type = %s ORDER BY name, year, indexer_id DESC "
        else:
            sql_select = "SELECT indexer_id, title, name, year, imdb_id, url FROM subscriptions WHERE indexer_type = ? AND type = ? AND video_type = ? ORDER BY name, year, indexer_id DESC "
            
        common.addon.log('-' + HELPER + '- -' +'%s: %s, %s, %s' % (sql_select, indexer_type, type, video_type), 2)
        
        try:
            self.dbcur.execute(sql_select, (indexer_type, type, video_type ) )
            for matchedrow in self.dbcur.fetchall():
                data = dict(matchedrow)                
                subs.append(data)
            common.addon.log('-' + HELPER + '- - success')
        except Exception, e:
            common.addon.log('-' + HELPER + '- - failure: %s' % e )
            pass
        return subs            