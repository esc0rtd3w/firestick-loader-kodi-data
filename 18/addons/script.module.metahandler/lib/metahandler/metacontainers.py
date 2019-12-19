'''
create/install metadata containers,
v1.0
'''

# NOTE: these are imported later on in the create container function:
# from cleaners import *
# import clean_dirs

import os,sys
import shutil
import xbmcvfs
import common
from lib.modules import db_utils
from lib.modules import log_utils

logger = log_utils.Logger.get_logger()

#append lib directory
sys.path.append((os.path.split(common.addon_path))[0])

class MetaContainer:

    def __init__(self):

        self.path = xbmc.translatePath('special://profile/addon_data/script.module.metahandler')

        self.work_path = os.path.join(self.path, 'work', '')
        self.cache_path = os.path.join(self.path,  'meta_cache')
        self.videocache = os.path.join(self.cache_path, 'video_cache.db')
        self.work_videocache = os.path.join(self.work_path, 'video_cache.db')
        self.movie_images = os.path.join(self.cache_path, 'movie')
        self.tv_images = os.path.join(self.cache_path, 'tvshow')        
        
        self.table_list = ['movie_meta', 'tvshow_meta', 'season_meta', 'episode_meta']
     
        logger.log('---------------------------------------------------------------------------------------')
        #delete and re-create work_path to ensure no previous files are left over
        self._del_path(self.work_path)
        
        #Re-Create work folder
        self.make_dir(self.work_path)

               
    def get_workpath(self):
        return self.work_path


    def get_cachepath(self):
        return self.cache_path
            

    def make_dir(self, mypath):
        ''' Creates sub-directories if they are not found. '''
        try:
            if not xbmcvfs.exists(mypath): xbmcvfs.mkdirs(mypath)
        except:
            if not os.path.exists(mypath): os.makedirs(mypath)  


    def _del_path(self, path):

        logger.log('Attempting to remove folder: %s' % path)
        if xbmcvfs.exists(path):
            try:
                logger.log('Removing folder: %s' % path)
                try:
                    dirs, files = xbmcvfs.listdir(path)
                    for file in files:
                        xbmcvfs.delete(os.path.join(path, file))
                    success = xbmcvfs.rmdir(path)
                    if success == 0:
                        raise Exception
                except Exception, e:
                    try:
                        logger.log_error('Failed to delete path using xbmcvfs: %s' % e)
                        logger.log('Attempting to remove with shutil: %s' % path)
                        shutil.rmtree(path)
                    except:
                        raise
            except Exception, e:
                logger.log_error('Failed to delete path: %s' % e)
                return False
        else:
            logger.log('Folder does not exist: %s' % path)


    def _extract_zip(self, src, dest):
            try:
                logger.log('Extracting '+str(src)+' to '+str(dest))
                #make sure there are no double slashes in paths
                src=os.path.normpath(src)
                dest=os.path.normpath(dest) 

                #Unzip - Only if file size is > 1KB
                if os.path.getsize(src) > 10000:
                    xbmc.executebuiltin("XBMC.Extract("+src+","+dest+")")
                else:
                    logger.log_error('************* Error: File size is too small')
                    return False

            except:
                logger.log_error('Extraction failed!')
                return False
            else:                
                logger.log('Extraction success!')
                return True


    def _insert_metadata(self, table):
        '''
        Batch insert records into existing cache DB

        Used to add extra meta packs to existing DB
        Duplicate key errors are ignored
        
        Args:
            table (str): table name to select from/insert into
        '''

        logger.log('Inserting records into table: %s' % table)
        # try:
        if DB == 'mysql':
            try: 	from sqlite3  import dbapi2 as sqlite
            except: from pysqlite2 import dbapi2 as sqlite

            db_address = common.addon.get_setting('db_address')
            db_port = common.addon.get_setting('db_port')
            if db_port: db_address = '%s:%s' %(db_address,db_port)
            db_user = common.addon.get_setting('db_user')
            db_pass = common.addon.get_setting('db_pass')
            db_name = common.addon.get_setting('db_name')

            db = database.connect(db_name, db_user, db_pass, db_address, buffered=True)
            mysql_cur = db.cursor()
            work_db = sqlite.connect(self.work_videocache);
            rows = work_db.execute('SELECT * FROM %s' %table).fetchall()

            cur = work_db.cursor()
            rows = cur.execute('SELECT * FROM %s' %table).fetchall()
            if rows:
                cols = ','.join([c[0] for c in cur.description])
                num_args = len(rows[0])
                args = ','.join(['%s']*num_args)
                sql_insert = 'INSERT IGNORE INTO %s (%s) VALUES(%s)'%(table, cols, args)
                mysql_cur.executemany(sql_insert, rows)
            work_db.close()

        else:
            sql_insert = 'INSERT OR IGNORE INTO %s SELECT * FROM work_db.%s' % (table, table)        
            logger.log('SQL Insert: %s' % sql_insert)
            logger.log(self.work_videocache)
            db = database.connect(self.videocache)
            db.execute('ATTACH DATABASE "%s" as work_db' % self.work_videocache)
            db.execute(sql_insert)
        # except Exception, e:
            # logger.log_error('************* Error attempting to insert into table: %s with error: %s' % (table, e))
            # pass
            # return False
        db.commit()
        db.close()
        return True

         
    def install_metadata_container(self, containerpath, installtype):

        logger.log('Attempting to install type: %s  path: %s' % (installtype, containerpath))

        if installtype=='database':
            extract = self._extract_zip(containerpath, self.work_path)
            #Sleep for 5 seconds to ensure DB is unzipped - else insert will fail
            xbmc.sleep(5000)
            for table in self.table_list:
                install = self._insert_metadata(table)
            
            if extract and install:
                return True
                
        elif installtype=='movie_images':
            return self._extract_zip(containerpath, self.movie_images)

        elif installtype=='tv_images':
            return self._extract_zip(containerpath, self.tv_images)

        else:
            logger.log('********* Not a valid installtype: %s' % installtype, 3)
            return False
