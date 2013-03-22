#!/usr/bin/env python
#
# Copyright (c) 2013 by Christian Heimes <christian@python.org>
# Licensed to PSF under a Contributor Agreement.
# See http://www.python.org/psf/license for licensing details.
#
import os
import sys
import unittest

import wincertstore


class TestWinCertStore(unittest.TestCase):
    def test_wincertstore(self):
        store = wincertstore.CertSystemStore("CA")
        try:
            store.itercerts()
            store.itercrls()
        finally:
            store.close()


def test_main():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestWinCertStore))
    return suite

if __name__ == "__main__":
    suite = test_main()
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    sys.exit(not result.wasSuccessful())
