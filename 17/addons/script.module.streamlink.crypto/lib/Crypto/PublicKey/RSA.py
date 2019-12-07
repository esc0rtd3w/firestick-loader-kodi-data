#!/usr/bin/env python
from __future__ import absolute_import
import binascii
import struct
from rsa import PublicKey, PrivateKey
from Crypto.Math.Numbers import Integer


def import_key(extern_key, passphrase=None):
    """Import an RSA key (public or private half), encoded in standard
    form.

    :Parameter extern_key:
        The RSA key to import, encoded as a byte string.

        An RSA public key can be in any of the following formats:

        - X.509 certificate (binary or PEM format)
        - X.509 ``subjectPublicKeyInfo`` DER SEQUENCE (binary or PEM
          encoding)
        - `PKCS#1`_ ``RSAPublicKey`` DER SEQUENCE (binary or PEM encoding)
        - OpenSSH (textual public key only)

        An RSA private key can be in any of the following formats:

        - PKCS#1 ``RSAPrivateKey`` DER SEQUENCE (binary or PEM encoding)
        - `PKCS#8`_ ``PrivateKeyInfo`` or ``EncryptedPrivateKeyInfo``
          DER SEQUENCE (binary or PEM encoding)
        - OpenSSH (textual public key only)

        For details about the PEM encoding, see `RFC1421`_/`RFC1423`_.

        The private key may be encrypted by means of a certain pass phrase
        either at the PEM level or at the PKCS#8 level.
    :Type extern_key: string

    :Parameter passphrase:
        In case of an encrypted private key, this is the pass phrase from
        which the decryption key is derived.
    :Type passphrase: string

    :Return: An RSA key object (`RsaKey`).

    :Raise ValueError/IndexError/TypeError:
        When the given key cannot be parsed (possibly because the pass
        phrase is wrong).

    .. _RFC1421: http://www.ietf.org/rfc/rfc1421.txt
    .. _RFC1423: http://www.ietf.org/rfc/rfc1423.txt
    .. _`PKCS#1`: http://www.ietf.org/rfc/rfc3447.txt
    .. _`PKCS#8`: http://www.ietf.org/rfc/rfc5208.txt
    """
    if passphrase is not None:
        raise ValueError("RSA key passphrase is not supported")
    if extern_key.startswith('ssh-rsa '):
        # This is probably an OpenSSH key
        keystring = binascii.a2b_base64(extern_key.split(' ')[1])
        keyparts = []
        while len(keystring) > 4:
            l = struct.unpack(">I", keystring[:4])[0]
            keyparts.append(keystring[4:4 + l])
            keystring = keystring[4 + l:]
        e = Integer.from_bytes(keyparts[1])
        n = Integer.from_bytes(keyparts[2])
        return PublicKey(n._value, e._value)

    for fmt in ("PEM", "DER"):
        try:
            return PrivateKey.load_pkcs1(extern_key, fmt)
        except:
            try:
                return PublicKey.load_pkcs1(extern_key, fmt)
            except:
                pass

    raise ValueError("RSA key format is not supported")

# Backward compatibility
importKey = import_key
