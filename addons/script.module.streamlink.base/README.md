# script.module.streamlink.base

_Streamlink library packed for Kodi: [Upstream link](https://github.com/streamlink/streamlink)

You can install it from [repository.twilight0.libs](https://github.com/Twilight0/repo.twilight0.libs)

Add this to your repository xml in order to pull updates:

    <dir>
        <info compressed="false">http://raw.githubusercontent.com/Twilight0/repo.twilight0.libs/master/_zips/addons.xml</info>
        <checksum>http://raw.githubusercontent.com/Twilight0/repo.twilight0.libs/master/_zips/addons.xml.md5</checksum>
        <datadir zip="true">http://raw.githubusercontent.com/Twilight0/repo.twilight0.libs/master/_zips/</datadir>
    </dir>

## Extracting streams
### The simplest use of the Streamlink API looks like this:

    import streamlink
    streams = streamlink.streams("https://www.youtube.com/watch?v=XIMLoLxmTDw")
    url = streams.['best'].to_url()

Where url can be passed into the player:

    xbmc.Player().play(url)


If no plugin for the URL is found, a **NoPluginError** will be raised.

If an error occurs while fetching streams, a **PluginError** will be raised.

### Session based usage, which allows plugin options to be passed

    import streamlink.session

    def resolve(url, quality='best'):

        try:

            session = streamlink.session.Streamlink()
            plugin = session.resolve_url(url)
            streams = plugin.get_streams()
            playable_link = streams.[quality].to_url()

            return playable_link

        except:

            pass
