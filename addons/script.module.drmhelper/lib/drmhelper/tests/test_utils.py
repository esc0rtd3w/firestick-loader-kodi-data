from drmhelper import utils

import fakes

import mock

import testtools

import xbmc


FAKE_ADDON = fakes.FakeAddon()


class UtilsTests(testtools.TestCase):

    @mock.patch('xbmcaddon.Addon', return_value=FAKE_ADDON)
    @mock.patch('xbmc.log')
    def test_log(self, mock_log, mock_addon):
        utils.log('foo')
        mock_log.assert_called_once_with('[Test Add-on v0.0.1] foo',
                                         level=xbmc.LOGNOTICE)

    def test_get_info_label(self):
        with mock.patch('xbmc.getInfoLabel', return_value='foo'):
            utils.get_info_label('test_label')
            self.assertEqual(utils.get_info_label('test_label'), 'foo')

    def test_get_info_label_busy(self):
        with mock.patch('xbmc.getInfoLabel', return_value='Busy'):
            utils.get_info_label('test_label')
            self.assertEqual(utils.get_info_label('test_label'), None)

    def test_get_addon_name(self):
        with mock.patch('xbmcaddon.Addon', return_value=FAKE_ADDON):
            name = utils.get_addon_name()
            self.assertEqual(FAKE_ADDON.name, name)

    def test_get_addon_version(self):
        with mock.patch('xbmcaddon.Addon', return_value=FAKE_ADDON):
            ver = utils.get_addon_version()
            self.assertEqual(FAKE_ADDON.version, ver)

    def test_get_kodi_build(self):
        val = 'foo'
        with mock.patch.object(utils, 'get_info_label', return_value=val):
            result = utils.get_kodi_build()
            self.assertEqual(result, val)

    def test_get_kodi_version(self):
        for b in fakes.KODI_BUILDS:
            with mock.patch.object(utils, 'get_info_label',
                                   return_value=b['build']):
                ver = utils.get_kodi_version()
                self.assertEqual(ver, b['version'])

    def test_get_kodi_major_version(self):
        for b in fakes.KODI_BUILDS:
            with mock.patch.object(utils, 'get_info_label',
                                   return_value=b['build']):
                ver = utils.get_kodi_major_version()
                self.assertEqual(ver, b['major_version'])

    def test_get_kodi_name(self):
        for b in fakes.KODI_BUILDS:
            with mock.patch.object(utils, 'get_kodi_major_version',
                                   return_value=b['major_version']):
                name = utils.get_kodi_name()
                self.assertEqual(name, b['build_name'])

    def test_get_kodi_build_date(self):
        for b in fakes.KODI_BUILDS:
            with mock.patch.object(utils, 'get_kodi_build',
                                   return_value=b['build']):
                date = utils.get_kodi_build_date()
                self.assertEqual(date, b['build_date'])
