#! /usr/bin/env python
""" cryptopy.cipher.test_all_ciphers

    All unit tests in the cipher package

    Copyright (c) 2002 by Paul A. Lambert
    Read LICENSE.txt for license information.
"""
import unittest
import cryptopy.cipher.aes_cbc_test
import cryptopy.cipher.aes_test
import cryptopy.cipher.arc4_test
import cryptopy.cipher.cbc_test
import cryptopy.cipher.ccm_test
import cryptopy.cipher.icedoll_test
import cryptopy.cipher.rijndael_test
import cryptopy.cipher.tkip_encr_test
import cryptopy.cipher.tkip_fake_crc_test
import cryptopy.cipher.wep_test

# Make this test module runnable from the command prompt
if __name__ == "__main__":
    unittest.main()



