import os
import os.path
import log_utils
files = os.listdir(os.path.dirname(__file__))
__all__ = [filename[:-3] for filename in files if not filename.startswith('__') and filename.endswith('.py')]

def sources():
    import pkgutil
    import os.path
    __all__ = [x for x in os.walk(os.path.dirname(__file__))][0]
    import kodi
    kodi.notify(msg=str(__all__))
    try:
        sourceDict = []
        for i in __all__:
            log_utils.log('%s' % (i), log_utils.LOGDEBUG)

            for loader, module_name, is_pkg in pkgutil.walk_packages([i]):
                if is_pkg:
                    continue

                try:
                    module = loader.find_module(module_name).load_module(module_name)
                    sourceDict.append((module_name, module.source()))
                except Exception as e:
                    log_utils.log('Could not load "%s": %s' % (module_name, e), log_utils.LOGDEBUG)
        return sourceDict
    except:
        return []