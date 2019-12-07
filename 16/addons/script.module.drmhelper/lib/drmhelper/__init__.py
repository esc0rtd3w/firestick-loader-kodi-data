"""
This contains the legacy entrypoints for DRM Helper
"""
from drmhelper import helper


def check_inputstream(drm=True):
    dh = helper.DRMHelper()
    return dh.check_inputstream(drm=drm)


def get_addon(drm=True):
    dh = helper.DRMHelper()
    return dh.get_addon(drm=drm)


def get_widevinecdm(cdm_path=None):
    dh = helper.DRMHelper()
    return dh._get_wvcdm(cdm_path=cdm_path)


def get_ssd_wv(cdm_path=None):
    dh = helper.DRMHelper()
    return dh._get_ssd_wv(cdm_path=cdm_path)


def get_ia_direct(update=False, drm=True):
    dh = helper.DRMHelper()
    return dh._get_ia_direct(update=update, drm=drm)
