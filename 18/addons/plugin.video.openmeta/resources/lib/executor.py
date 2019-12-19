from itertools import islice
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED
import xbmc

def execute(f, iterable, stop_flag=None, workers=10):
	Executor = ThreadPoolExecutor
	with Executor(max_workers=workers) as executor:
		for future in _batched_pool_runner(executor, workers, f, iterable):
			if xbmc.Monitor().abortRequested():
				break
			if stop_flag and stop_flag.isSet():
				break
			yield future.result()

def _batched_pool_runner(pool, batch_size, f, iterable):
	it = iter(iterable)
	futures = set(pool.submit(f, x) for x in islice(it, batch_size))
	while futures:
		done, futures = wait(futures, return_when=FIRST_COMPLETED)
		futures.update(pool.submit(f, x) for x in islice(it, len(done)))
		for d in done:
			yield d