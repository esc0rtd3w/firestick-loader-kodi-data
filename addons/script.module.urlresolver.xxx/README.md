# script.module.urlresolver.xxx
Adult Resolver Extension for SMU

1. Import SMU and the XXX SMU Extension to your addon.
2. Call the urlresolver from your addon to resolve the XXX hosts.

    * import urlresolver, xbmcvfs
    * xxx_plugins_path = 'special://home/addons/script.module.urlresolver.xxx/resources/plugins/'
    * if xbmcvfs.exists(xxx_plugins_path): urlresolver.add_plugin_dirs(xbmc.translatePath(xxx_plugins_path))
    * url = urlresolver.resolve(url)
