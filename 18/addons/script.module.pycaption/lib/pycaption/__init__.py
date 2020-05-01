from __future__ import unicode_literals

from .base import (
    Caption, CaptionConverter, CaptionList, CaptionNode, CaptionSet)
from .dfxp import DFXPReader, DFXPWriter
from .exceptions import (
    CaptionReadError, CaptionReadNoCaptions, CaptionReadSyntaxError
)
from .scc import SCCReader, SCCWriter
from .srt import SRTReader, SRTWriter
from .webvtt import WebVTTReader, WebVTTWriter


__all__ = [
    'CaptionConverter', 'DFXPReader', 'DFXPWriter',
    'SRTReader', 'SRTWriter',
    'SCCReader', 'SCCWriter', 'WebVTTReader', 'WebVTTWriter',
    'CaptionReadError', 'CaptionReadNoCaptions', 'CaptionReadSyntaxError',
    'detect_format', 'CaptionNode', 'Caption', 'CaptionList', 'CaptionSet'
]

SUPPORTED_READERS = (
    DFXPReader, WebVTTReader, SRTReader, SCCReader)

SUPPORTED_WRITERS = (
    DFXPWriter, WebVTTWriter, SRTWriter, SCCWriter)


def detect_format(caps):
    """
    Detect the format of the provided caption string.

    :returns: the reader class for the detected format.
    """
    for reader in SUPPORTED_READERS:
        if reader().detect(caps):
            return reader

    return None
