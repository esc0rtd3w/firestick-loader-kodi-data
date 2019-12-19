import xbmc
import abc


abstractstaticmethod = abc.abstractmethod


class abstractclassmethod(classmethod):
    __isabstractmethod__ = True

    def __init__(self, callable):
        callable.__isabstractmethod__ = True
        super(abstractclassmethod, self).__init__(callable)


class Plugin():
    __metaclass__ = abc.ABCMeta
    name = "Plugin"
    priority = 100

    def get_xml(self, url):
        pass

    def get_xml_uncached(self, url):
        pass

    def get_link_message(self):
        pass

    def get_searching_message(self, preset):
        pass

    def process_item(self, item_xml):
        pass

    def get_theme_list(self):
        pass

    def replace_url(self, url):
        pass

    def get_sources(self, item):
        pass

    def get_info(self, items, dialog):
        pass

    def do_search(self, search_term):
        pass

    def display_list(self, items, content_type, pins):
        pass

    def first_run_wizard(self):
        pass

    def clear_cache(self):
        pass

    def get_context_items(self, item, context):
        pass


plugin_cache = {}


def get_plugins():
    import resources.lib.plugins
    klasses = Plugin.__class__.__subclasses__(Plugin)
    plugins = []
    for klass in klasses:
        if klass in plugin_cache:
            plugins.append(plugin_cache[klass])
        else:
            plugin_cache[klass] = klass()
            plugins.append(plugin_cache[klass])
    return plugins


def run_hook(*args):
    plugins = get_plugins()
    function_name = args[0]
    other_args = args[1:]
    plugins = sorted(plugins, key=lambda plugin: plugin.priority, reverse=True)
    for plugin in plugins:
        result = getattr(plugin, function_name)(*other_args)
        if result:
            return result
    return False
