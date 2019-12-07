import drmhelper

import testtools


class DRMHelperTests(testtools.TestCase):

    def test_check_inputstream(self):
        drmhelper.check_inputstream()
