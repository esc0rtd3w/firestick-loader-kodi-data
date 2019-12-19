import os
from resources.lib.common import tools
from resources.lib.modules import database

data_path = os.path.join(tools.dataPath, 'providers')
hoster_sources = []
torrent_sources = []

def get_relevant(language):
    provider_packages = [name for name in os.listdir(data_path) if os.path.isdir(os.path.join(data_path, name))]
    # Get relevant and enabled provider entries from the database
    provider_status = [i for i in database.get_providers() if i['country'] == language]
    provider_status = [i for i in provider_status if i['status'] == 'enabled']

    for package in provider_packages:
        try:
            providers_path = 'providers.%s.%s' % (package, language)
            try:
                provider_list = __import__(providers_path, fromlist=[''])
            except:
                continue
            try:
                for i in provider_list.get_hosters():
                    for status in provider_status:
                        if i == status['provider_name']:
                            if package == status['package']:
                                # Add import path and name to hoster_providers
                                hoster_sources.append(('%s.hosters' % providers_path, i, package))
            except:
                pass
            
            try:
                for i in provider_list.get_torrent():
                    for status in provider_status:
                        if i == status['provider_name']:
                            if package == status['package']:
                                # Add import path and name to torrent_providers
                                torrent_sources.append(('%s.torrent' % providers_path, i, package))
            except:
                pass
        except:
            import traceback
            traceback.print_exc()
            continue

    return (torrent_sources, hoster_sources)

def get_all(language):
    provider_packages = [name for name in os.listdir(data_path) if os.path.isdir(os.path.join(data_path, name))]
    for package in provider_packages:
        try:
            providers_path = 'providers.%s.%s' % (package, language)
            try:
                provider_list = __import__(providers_path, fromlist=[''])
            except:
                continue
            try:
                for i in provider_list.get_hosters():
                    hoster_sources.append(('%s.hosters' % providers_path, i, package))
            except:
                pass

            try:
                for i in provider_list.get_torrent():
                    torrent_sources.append(('%s.torrent' % providers_path, i, package))
            except:
                pass

        except:
            import traceback
            traceback.print_exc()
            continue

    return (torrent_sources, hoster_sources)
