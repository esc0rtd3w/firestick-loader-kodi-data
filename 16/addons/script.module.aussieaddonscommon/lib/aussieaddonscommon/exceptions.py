class AussieAddonsException(Exception):
    """Aussie Add-ons custom exception

    This exception can be thrown with the reportable arg set which can
    determine whether or not it is allowed to be sent as an automatic
    error report
    """
    def __init__(self, message, reportable=False):
        super(AussieAddonsException, self).__init__(message)
        self.reportable = False

    def is_reportable(self):
        return self.reportable
