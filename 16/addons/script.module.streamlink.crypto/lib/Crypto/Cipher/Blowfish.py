from Crypto.Cipher.blockcipher import *
from pyblowfish import Blowfish as pBlowfish


def new(key, mode=MODE_ECB, IV=None, counter=None, segment_size=None):
    return Blowfish(key, mode, IV, counter, segment_size)


class Blowfish(BlockCipher):
    key_error_message = "Key should be between 8 and 56 bytes (64 <-> 448 bits)"

    def __init__(self, key, mode, IV, counter, segment_size):
        self.blocksize = 8
        BlockCipher.__init__(self, key, mode, IV, counter, pBlowfish, segment_size)

    def keylen_valid(self, key):
        return 8 <= len(key) <= 56
