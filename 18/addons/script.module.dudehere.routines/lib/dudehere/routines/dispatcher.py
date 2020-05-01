from dudehere.routines import *
from dudehere.routines.plugin import log
class FunctionDispatcher():
	__functions = {}
	__args = {}
	__kwargs = {}

	def register(self, mode, args=[], kwargs={}):
		def decorator(target):
			for foo in args:
				args[args.index(foo)] = self.__coerce(foo)
			for foo in kwargs.keys():
				kwargs[foo] = self.__coerce(kwargs[foo])
			if isinstance(mode, list):
				for foo in mode:
					self.__functions[foo] = target
					self.__args[foo] = args
					self.__kwargs[foo] = kwargs
			else:
				self.__functions[mode] = target
				self.__args[mode] = args
				self.__kwargs[mode] = kwargs
			return target
		return decorator
	
	def __coerce(self, v):
		test = v.lower()
		if test == 'none': return None
		if test == 'false': return False
		if test == "true": return True
		return v
	
	def error(self):
		pass
	
	def run(self, mode='default'):
		if mode is None or mode == '' or mode is False:
			mode = 'default'
		if mode in self.__functions:
			args = self.__args[mode]
			kwargs = self.__kwargs[mode]
			try:
				self.__functions[mode](*args, **kwargs)
			except Exception, e:
				log( "Dispatcher Error in mode %s:  %s" % (mode, e))
				self.error()
		else:
			log( "Illegal mode: %s" % mode)
			self.error()
dispatcher = FunctionDispatcher()