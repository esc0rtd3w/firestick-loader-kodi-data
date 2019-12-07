

from resources.lib.modules import control
control.execute('RunPlugin(plugin://%s)' % control.get_plugin_url({'action': 'service'}))
