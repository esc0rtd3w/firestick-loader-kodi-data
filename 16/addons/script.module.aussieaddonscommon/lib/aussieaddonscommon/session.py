import requests
import ssl
import utils

from exceptions import AussieAddonsException

from requests.adapters import HTTPAdapter
from requests.exceptions import SSLError
from requests.packages.urllib3.poolmanager import PoolManager
from requests.packages.urllib3.util import Retry

# Ignore all warnings
requests.packages.urllib3.disable_warnings()


class TLSv1Adapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=ssl.PROTOCOL_TLSv1)


class Session(requests.Session):
    """Class to encapsulate the rest api endpoint with a requests session."""
    def __init__(self, force_tlsv1=False, max_retries=3, *args, **kwargs):
        requests.Session.__init__(self, *args, **kwargs)

        retry = Retry(total=max_retries,
                      backoff_factor=0.2,
                      status_forcelist=[500, 502, 503, 504])

        # Always allow retries on server failures
        http_adapter = HTTPAdapter(max_retries=retry)

        if force_tlsv1:
            https_adapter = TLSv1Adapter(max_retries=retry)
        else:
            https_adapter = HTTPAdapter(max_retries=retry)

        self.mount('http://', http_adapter)
        self.mount('https://', https_adapter)

        # Always ignore SSL validation errors
        self.verify = False

    def request(self, method, url, *args, **kwargs):
        """Send the request after generating the complete URL."""
        utils.log("Performing {0} for {1}".format(method, url))
        try:
            req = super(Session, self).request(method, url, *args, **kwargs)
            req.raise_for_status()
        except SSLError as e:
            msg = ('SSL Error: {0}. This is usually due to an old version of '
                   'Kodi. Please upgrade to Kodi v17 or later.'.format(e))
            raise AussieAddonsException(msg)
        except requests.exceptions.HTTPError as e:
            raise e
        except Exception as e:
            raise AussieAddonsException('Error: {0}'.format(e))

        return req
