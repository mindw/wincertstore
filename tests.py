#!/usr/bin/env python
#
# Copyright (c) 2013 by Christian Heimes <christian@python.org>
# Licensed to PSF under a Contributor Agreement.
# See http://www.python.org/psf/license for licensing details.
#
import os
import pprint
import socket
import sys
import unittest

try:
    import ssl
except ImportError:
    ssl = None

import wincertstore

if sys.version_info[0] == 3:
    def b(s):
        return s.encode("ascii")
else:
    def b(s):
        return s


class TestWinCertStore(unittest.TestCase):
    def test_wincertstore(self):
        store = wincertstore.CertSystemStore("ROOT")
        try:
            for cert in store.itercerts():
                pem = cert.get_pem()
                enc = cert.get_encoded()
                name = cert.get_name()
                trust = cert.enhanced_keyusage_names()
                if ssl is not None:
                    self.assertEqual(ssl.DER_cert_to_PEM_cert(enc), pem)
                    self.assertEqual(ssl.PEM_cert_to_DER_cert(pem), enc)
            for crl in store.itercrls():
                pem = cert.get_pem()
        finally:
            store.close()

    def create_certfile(self):
        certfile = wincertstore.CertFile()
        store = wincertstore.CertSystemStore("ROOT")
        try:
            certfile.addstore(store)
        finally:
            store.close()
        certfile.addstore("CA")
        return certfile

    def test_certfile(self):
        certfile = self.create_certfile()
        pemfile = certfile.name
        try:
            self.assertTrue(os.path.isfile(pemfile))
            self.assertTrue(pemfile.endswith("ca.pem"), pemfile)
            self.assertEqual(certfile.read(), certfile.read())
        finally:
            certfile.close()
        self.assertFalse(os.path.isfile(pemfile))

    def test_certfile_ssl(self):
        if ssl is None:
            return

        certfile = self.create_certfile()
        try:
            # based on example from SSL module docs
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(("pypi.python.org", 443))
            ssl_sock = ssl.wrap_socket(sock,
                                       ssl_version=ssl.PROTOCOL_SSLv3,
                                       ca_certs=certfile.name,
                                       cert_reqs=ssl.CERT_REQUIRED)
            if 0:
                print(repr(ssl_sock.getpeername()))
                print(ssl_sock.cipher())
                print(pprint.pformat(ssl_sock.getpeercert()))

            ssl_sock.write(b("GET / HTTP/1.1\r\n"
                             "Host: www.google.com\r\n\r\n"))
            data = ssl_sock.read()
            ssl_sock.close()
        finally:
            certfile.close()

def test_main():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestWinCertStore))
    return suite

if __name__ == "__main__":
    suite = test_main()
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    sys.exit(not result.wasSuccessful())
