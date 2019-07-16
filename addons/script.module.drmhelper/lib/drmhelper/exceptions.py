class DRMHelperException(Exception):
    """DRM Helper Exception

    Custom exception for handling DRM helper exceptions
    """
    def __init__(self, message):
        super(DRMHelperException, self).__init__(message)


class WidevinePlatformNotSupported(DRMHelperException):
    """Widevine Platform Not Supported

    This platform is not supported by Widevine
    """
    pass
