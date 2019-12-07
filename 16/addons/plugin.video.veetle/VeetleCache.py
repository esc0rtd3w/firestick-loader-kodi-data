import datetime
import time
import Logger

try:
    import StorageServer
except:
    import StorageServerDummy as StorageServer

VALIDITY_DATETIME_KEY = "_validity"
VALIDITY_DATETIME_PATTERN = "%Y-%m-%dT%H:%M:%S"

log = Logger.Logger("VeetleCache")

# This class wraps the common plugin cache and adds a validity date to each cached object key
# so that objects are only cached for a certain amount of time
class VeetleCache:

    def __init__(self, minutes):
        self.cache = StorageServer.StorageServer("plugin.video.veetle", 1)
        self.minutes = minutes

    def get(self, key):

        validityDateTimeString = self.cache.get(key + VALIDITY_DATETIME_KEY)

        # If there is no validity date yet, then return None
        if validityDateTimeString is None or len(str(validityDateTimeString)) == 0:
            log.debug("Validity date is None or empty")
            return None

        # Try parse validity date
        try:
            try:
                validityDateTime = datetime.datetime.strptime(validityDateTimeString, VALIDITY_DATETIME_PATTERN)
            except TypeError:
                validityDateTime = datetime.datetime(*(time.strptime(validityDateTimeString, VALIDITY_DATETIME_PATTERN)[0:6]))

        except Exception, e:
            log.warn("Error parsing validity date: " + repr(e))
            return None

        # If validity date is smaller than current date then return None
        if validityDateTime < datetime.datetime.now():
            log.debug("Validity date is smaller than now()")
            return None

        # Otherwise return cached value
        log.debug("Using cached value")

        return self.cache.get(key)


    def set(self, key, value):

        # Set validity date for this key
        validityDateTime = datetime.datetime.now() + datetime.timedelta(minutes = self.minutes)

        self.cache.set(key + VALIDITY_DATETIME_KEY, validityDateTime.strftime(VALIDITY_DATETIME_PATTERN))

        log.debug("Set validity date to '%s' for key '%s'" % (repr(validityDateTime), key))

        # Set value for key
        self.cache.set(key, value)

        log.debug("Set value for key '%s' to '%s'" % (key, repr(value)))

