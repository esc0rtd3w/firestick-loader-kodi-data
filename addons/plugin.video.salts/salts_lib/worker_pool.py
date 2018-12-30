"""
    SALTS XBMC Addon
    Copyright (C) 2016 tknorris

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import Queue
import threading
import log_utils

logger = log_utils.Logger.get_logger(__name__)
logger.disable()

Empty = Queue.Empty

class WorkerPool(object):
    def __init__(self, max_workers=None):
        self.max_workers = max_workers
        self.workers = []
        self.out_q = Queue.Queue()
        self.in_q = Queue.Queue()
        self.new_job = threading.Event()
        self.manager = None
        self.closing = False
        self.__start_manager()
    
    def request(self, func, args=None, kwargs=None):
        if args is None: args = []
        if kwargs is None: kwargs = {}
        self.in_q.put({'func': func, 'args': args, 'kwargs': kwargs})
        self.new_job.set()
    
    def receive(self, timeout):
        return self.out_q.get(True, timeout)
    
    def close(self):
        self.closing = True
        self.new_job.set()

        # tell all consumers to die
        self.in_q.put(None)
        if self.manager is not None:
            self.manager.join()
            
        return reap_workers(self.workers)

    def __start_manager(self):
        self.manager = threading.Thread(target=self.__manage_consumers)
        self.manager.daemon = True
        self.manager.start()
        logger.log('Pool Manager(%s): started.' % (self), log_utils.LOGDEBUG)
        
    def __manage_consumers(self):
        while not self.closing:
            self.new_job.wait()
            self.new_job.clear()
            if self.closing:
                break
            
            new_workers = self.in_q.qsize()  # create a worker for each job waiting (up to max_workers)
            if new_workers > 0:
                if self.max_workers is None:
                    max_new = new_workers
                else:
                    max_new = self.max_workers - len(self.workers)
                    
                if max_new > 0:
                    logger.log('Pool Manager: Requested: %s Allowed: %s - Pool Size: (%s / %s)' % (new_workers, max_new, len(self.workers), self.max_workers), log_utils.LOGDEBUG)
                    if new_workers > max_new:
                        new_workers = max_new
                        
                    for _ in xrange(new_workers):
                        try:
                            worker = threading.Thread(target=self.consumer)
                            worker.daemon = True
                            worker.start()
                            self.workers.append(worker)
                            logger.log('Pool Manager: %s thrown in Pool: (%s/%s)' % (worker.name, len(self.workers), self.max_workers), log_utils.LOGDEBUG)
                        except RuntimeError as e:
                            try: logger.log('Pool Manager: %s missed Pool: %s - (%s/%s)' % (worker.name, e, len(self.workers), self.max_workers), log_utils.LOGWARNING)
                            except UnboundLocalError: pass  # worker may not have gotten assigned
                        
        logger.log('Pool Manager(%s): quitting.' % (self), log_utils.LOGDEBUG)
            
    def consumer(self):
        me = threading.current_thread()
        while True:
            job = self.in_q.get()
            if job is None:
                logger.log('Worker: %s committing suicide.' % (me.name), log_utils.LOGDEBUG)
                self.in_q.put(job)
                break
            
            # logger.log('Worker: %s handling job: |%s| with args: |%s| and kwargs: |%s|' % (me.name, job['func'], job['args'], job['kwargs']), log_utils.LOGDEBUG)
            result = job['func'](*job['args'], **job['kwargs'])
            self.out_q.put(result)
    
def reap_workers(workers, timeout=0):
    """
    Reap thread/process workers; don't block by default; return un-reaped workers
    """
    logger.log('In Reap: Total Workers: %s' % (len(workers)), log_utils.LOGDEBUG)
    living_workers = []
    for worker in workers:
        if worker:
            logger.log('Reaping: %s' % (worker.name), log_utils.LOGDEBUG)
            worker.join(timeout)
            if worker.is_alive():
                logger.log('Worker %s still running' % (worker.name), log_utils.LOGDEBUG)
                living_workers.append(worker)
    return living_workers
