import concurrent.futures
from itertools import islice
from xbmcswift2 import xbmc

Executor = concurrent.futures.ThreadPoolExecutor

def execute(f, iterable, stop_flag=None, workers=10):
    with Executor(max_workers=workers) as executor:
        for future in _batched_pool_runner(executor, workers, f, iterable):
            if xbmc.abortRequested:
                break
            if stop_flag and stop_flag.isSet():
                break
            yield future.result()
            

def _batched_pool_runner(pool, batch_size, f, iterable):
    it = iter(iterable)
    
    # Submit the first batch of tasks.
    futures = set(pool.submit(f, x) for x in islice(it, batch_size))
    
    while futures:
        done, futures = concurrent.futures.wait(futures, return_when=concurrent.futures.FIRST_COMPLETED)
        
        # Replenish submitted tasks up to the number that completed.
        futures.update(pool.submit(f, x) for x in islice(it, len(done)))
        
        for d in done:
            yield d
            