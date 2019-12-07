# -*- coding: utf-8 -*-
#
#  Cipher/PKCS1-v1_5.py : PKCS#1 v1.5
#
# ===================================================================
# The contents of this file are dedicated to the public domain.  To
# the extent that dedication to the public domain is not available,
# everyone is granted a worldwide, perpetual, royalty-free,
# non-exclusive license to exercise all rights associated with the
# contents of this file for any purpose whatsoever.
# No rights are reserved.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ===================================================================

"""RSA encryption protocol according to PKCS#1 v1.5

See RFC3447__ or the `original RSA Labs specification`__ .

This scheme is more properly called ``RSAES-PKCS1-v1_5``.

**If you are designing a new protocol, consider using the more robust PKCS#1 OAEP.**

As an example, a sender may encrypt a message in this way:

        >>> from Crypto.Cipher import PKCS1_v1_5
        >>> from Crypto.PublicKey import RSA
        >>> from Crypto.Hash import SHA
        >>>
        >>> message = b'To be encrypted'
        >>> h = SHA.new(message)
        >>>
        >>> key = RSA.importKey(open('pubkey.der').read())
        >>> cipher = PKCS1_v1_5.new(key)
        >>> ciphertext = cipher.encrypt(message+h.digest())

At the receiver side, decryption can be done using the private part of
the RSA key:

        >>> From Crypto.Hash import SHA
        >>> from Crypto import Random
        >>>
        >>> key = RSA.importKey(open('privkey.der').read())
        >>>
        >>> dsize = SHA.digest_size
        >>> sentinel = Random.new().read(15+dsize)      # Let's assume that average data length is 15
        >>>
        >>> cipher = PKCS1_v1_5.new(key)
        >>> message = cipher.decrypt(ciphertext, sentinel)
        >>>
        >>> digest = SHA.new(message[:-dsize]).digest()
        >>> if digest==message[-dsize:]:                # Note how we DO NOT look for the sentinel
        >>>     print "Encryption was correct."
        >>> else:
        >>>     print "Encryption was not correct."

:undocumented: __revision__, __package__

.. __: http://www.ietf.org/rfc/rfc3447.txt
.. __: http://www.rsa.com/rsalabs/node.asp?id=2125.
"""
from os import urandom

import rsa

__all__ = ['new', 'PKCS115_Cipher']

from Crypto.Util.number import ceil_div, bytes_to_long, long_to_bytes
from Crypto.Util.py3compat import *
import Crypto.Util.number


class PKCS115_Cipher:
    """This cipher can perform PKCS#1 v1.5 RSA encryption or decryption."""

    def __init__(self, key, randfunc):
        """Initialize this PKCS#1 v1.5 cipher object.

        :Parameters:
         key : an RSA key object
          If a private half is given, both encryption and decryption are possible.
          If a public half is given, only encryption is possible.
         randfunc : callable
          Function that returns random bytes.
        """

        self._key = key
        self._randfunc = randfunc

    def can_encrypt(self):
        """Return True if this cipher object can be used for encryption."""
        return self._key.can_encrypt()

    def can_decrypt(self):
        """Return True if this cipher object can be used for decryption."""
        return self._key.can_decrypt()

    def encrypt(self, message):
        return rsa.encrypt(message, self._key)

    def decrypt(self, ct, sentinel):
        return rsa.decrypt(ct, self._key)


def new(key, randfunc=None):
    """Return a cipher object `PKCS115_Cipher` that can be used to perform PKCS#1 v1.5 encryption or decryption.

    :Parameters:
     key : RSA key object
      The key to use to encrypt or decrypt the message. This is a `Crypto.PublicKey.RSA` object.
      Decryption is only possible if *key* is a private RSA key.
     randfunc : callable
      Function that return random bytes.
      The default is `Crypto.Random.get_random_bytes`.
    """
    return PKCS115_Cipher(key, randfunc or urandom)
