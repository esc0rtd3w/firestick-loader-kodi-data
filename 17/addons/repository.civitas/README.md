```
#:'######::'####:'##::::'##:'####:'########::::'###:::::'######::
#'##... ##:. ##:: ##:::: ##:. ##::... ##..::::'## ##:::'##... ##:
# ##:::..::: ##:: ##:::: ##:: ##::::: ##:::::'##:. ##:: ##:::..::
# ##:::::::: ##:: ##:::: ##:: ##::::: ##::::'##:::. ##:. ######::
# ##:::::::: ##::. ##:: ##::: ##::::: ##:::: #########::..... ##:
# ##::: ##:: ##:::. ## ##:::: ##::::: ##:::: ##.... ##:'##::: ##:
#. ######::'####:::. ###::::'####:::: ##:::: ##:::: ##:. ######::
#:......:::....:::::...:::::....:::::..:::::..:::::..:::......:::
```

Welcome to CIVITAS,

In the history of Rome, the Latin term civitas, according to Cicero in the time of the late Roman Republic, was the social body of the cives, or citizens, united by law. It is the law that binds them together, giving them responsibilities on the one hand and rights of citizenship on the other. The agreement has a life of its own, creating a res publica or "public entity", into which individuals are born or accepted, and from which they die or are ejected. The civitas is not just the collective body of all the citizens, it is the contract binding them all together, because each of them is a civis.

# Civitas Scrapers Repo

You can add the source directory to your own repository for convenience and updates
```
<dir>
    <info compressed="false">https://raw.githubusercontent.com/civitasadmin/_scrapers/master/addons.xml</info>
    <checksum>https://raw.githubusercontent.com/civitasadmin/_scrapers/master/addons.xml.md5</checksum>
    <datadir zip="true">https://raw.githubusercontent.com/civitasadmin/_scrapers/master/</datadir>
</dir>
```
# How to Import Civitas Scrapers Into Any Addon

Any multi-source Kodi addon can be altered to use these new scrapers instead of its own, you can follow the instructions below to get things updated. The below is an example using 13clowns. When appling to a different addon, change "13clowns" with the name of the addon.

i.e. /plugin.video.name_of_addon/

Open the addons/plugin.video.13clowns/addon.xml.

Add the following line to the addon.xml file:

    <import addon=”script.module.civitasscrapers”/>

Open addons/script.module.13clowns/lib/resources/lib/modules/sources.py

Add the following line to the sources.py file:

    import civitasscrapers

Add it right after the line that says:

    from resources.lib.modules import thexem

You will also need to change a few lines in the def getConstants(self) function in sources.py file:

Find the line that says:

    from resources.lib.sources import sources

Comment out that line by adding a pound/hashtag at the beginning like this:

    #from resources.lib.sources import sources

add the following:

    from civitasscrapers import sources
