'''
Created on Oct 28, 2011

@author: singleton recipe
'''
# import thread
from common import Logger

class SingletonClass(object):
    '''Implement Pattern: SINGLETON'''

    # Disabled lock mechanism as we don't start multiple threads in this add-on
    # __lockObj = thread.allocate_lock()  # lock object
    __instance = None  # the unique instance
    __initialized = False  # the initialization status
    
    def __new__(cls, *args, **kargs):
        return cls.getInstance(cls, *args, **kargs)

    def getInstance(cls, *args, **kargs):
        '''Static method to have a reference to **THE UNIQUE** instance'''
        
        if cls.__instance is None:
            
            # Critical section start
            # cls.__lockObj.acquire()
            try:
                if cls.__instance is None:
                    cls.__instance = object.__new__(cls)
            except Exception, e:
                Logger.logFatal('Error occurred while creating singleton obj')
                Logger.logFatal(e)
                raise
#            finally:
#                #  Exit from critical section whatever happens
#                #cls.__lockObj.release()
#                # Critical section end
#                pass
            
            # Initialize **the unique** instance
            try:
                if cls.__instance is not None:
                    cls.__instance.__initialize__(**kargs)
            except Exception, e:
                Logger.logFatal('Error occurred while initialization of singleton obj')
                Logger.logFatal(e)
                raise
            cls.__initialized = True
#        else:
#            #Wait for initialization :: Initialization might be completed with errors.
#            while not cls.__initialized:
#                print 'Waiting for initialization :: ' + str(cls)
#                pass

        return cls.__instance
    getInstance = classmethod(getInstance)
