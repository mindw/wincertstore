#!/usr/bin/env python
#
# Copyright (c) 2013 by Christian Heimes <christian@python.org>
# Licensed to PSF under a Contributor Agreement.
# See http://www.python.org/psf/license for licensing details.
#
"""ctypes interface to Window's certificate store

Requirements:
  Windows XP, Windows Server 2003 or newer
  Python 2.3+
  Python 3.2+

Python 2.3 and 2.4 need ctypes 1.0.2 from
http://sourceforge.net/projects/ctypes/
"""
__all__ = ("CertSystemStore",)

import sys
from ctypes import WinDLL, FormatError, string_at
from ctypes import Structure, POINTER, c_void_p
from ctypes.wintypes import LPCWSTR, DWORD, BOOL, BYTE

try:
    from ctypes import get_last_error
except ImportError:
    from ctypes import GetLastError as get_last_error
    USE_LAST_ERROR = False
else:
    USE_LAST_ERROR = True

try:
    from base64 import b64encode
except ImportError:
    # Python 2.3
    from binascii import b2a_base64
    def b64encode(s):
        return bb2a_base64(s)[:-1]


if sys.version_info[0] == 3:
    def b(s):
        return s.encode("ascii")
else:
    def b(s):
        return s


HCERTSTORE = c_void_p
PCCERT_INFO = c_void_p
PCCRL_INFO = c_void_p
LPTCSTR = LPCWSTR

PKCS_7_ASN_ENCODING = 0x00010000

def isPKCS7(value):
    """PKCS#7 check
    """
    return (value & PKCS_7_ASN_ENCODING) == PKCS_7_ASN_ENCODING


class ContextStruct(Structure):
    cert_type = None
    __slots__ = ()
    _fields_ = []

    def get_encoded(self):
        """Get encoded cert as byte string
        """
        pass

    def encoding_type(self):
        """Get encoding type for PEM
        """
        if isPKCS7(self.dwCertEncodingType):
            return "PKCS7"
        else:
            return self.cert_type

    encoding_type = property(encoding_type)

    def get_pem(self):
        """Get PEM encoded cert
        """
        encoding_type = self.encoding_type
        b64data = b64encode(self.get_encoded())
        lines = [b("-----BEGIN %s-----" % encoding_type)]
        # split up in lines of 64 chars each
        quotient, remainder = divmod(len(b64data), 64)
        linecount = quotient + bool(remainder)
        for i in range(linecount):
            lines.append(b64data[i * 64:(i + 1) * 64])
        lines.append(b("-----END %s-----" % encoding_type))
        return b("\n").join(lines)


class CERT_CONTEXT(ContextStruct):
    """Cert context
    """
    cert_type = "CERTIFICATE"
    __slots__ = ()
    _fields_ = [
        ("dwCertEncodingType", DWORD),
        ("pbCertEncoded", POINTER(BYTE)),
        ("cbCertEncoded", DWORD),
        ("pCertInfo", PCCERT_INFO),
        ("hCertStore", HCERTSTORE),
        ]

    def get_encoded(self):
        return string_at(self.pbCertEncoded, self.cbCertEncoded)


class CRL_CONTEXT(ContextStruct):
    """Cert revocation list context
    """
    cert_type = "X509 CRL"
    __slots__ = ()
    _fields_ = [
        ("dwCertEncodingType", DWORD),
        ("pbCrlEncoded", POINTER(BYTE)),
        ("cbCrlEncoded", DWORD),
        ("pCrlInfo", PCCRL_INFO),
        ("hCertStore", HCERTSTORE),
        ]

    def get_encoded(self):
        return string_at(self.pbCrlEncoded, self.cbCrlEncoded)


if USE_LAST_ERROR:
    crypt32 = WinDLL("crypt32.dll", use_last_error=True)
else:
    crypt32 = WinDLL("crypt32.dll")


CertOpenSystemStore = crypt32.CertOpenSystemStoreW
CertOpenSystemStore.argtypes = [c_void_p, LPTCSTR]
CertOpenSystemStore.restype = HCERTSTORE

CertCloseStore = crypt32.CertCloseStore
CertCloseStore.argtypes = [HCERTSTORE, DWORD]
CertCloseStore.restype = BOOL

PCCERT_CONTEXT = POINTER(CERT_CONTEXT)
CertEnumCertificatesInStore = crypt32.CertEnumCertificatesInStore
CertEnumCertificatesInStore.argtypes = [HCERTSTORE, PCCERT_CONTEXT]
CertEnumCertificatesInStore.restype = PCCERT_CONTEXT

PCCRL_CONTEXT = POINTER(CRL_CONTEXT)
CertEnumCRLsInStore = crypt32.CertEnumCRLsInStore
CertEnumCRLsInStore.argtypes = [HCERTSTORE, PCCRL_CONTEXT]
CertEnumCRLsInStore.restype = PCCRL_CONTEXT


class CertSystemStore(object):
    """Wrapper for Window's cert system store

    http://msdn.microsoft.com/en-us/library/windows/desktop/aa376560%28v=vs.85%29.aspx

    store names
    -----------
    CA:
      Certification authority certificates
    MY:
      Certs with private keys
    ROOT:
      Root certificates
    SPC:
      Software Publisher Certificate
    """
    __slots__ = ("_storename", "_hStore")

    def __init__(self, storename):
        self._storename = storename
        self._hStore = CertOpenSystemStore(None, self.storename)
        if not self._hStore: # NULL ptr
            self._hStore = None
            errmsg = FormatError(get_last_error())
            raise OSError(errmsg)

    def storename(self):
        """Get store name
        """
        return self._storename

    storename = property(storename)

    def close(self):
        CertCloseStore(self._hStore, 0)
        self._hStore = None

    def __enter__(self):
        return self

    def __exit__(self, exc, value, tb):
        self.close()

    def itercerts(self):
        """Iterate over certificates
        """
        pCertCtx = CertEnumCertificatesInStore(self._hStore, None)
        while pCertCtx:
            certCtx = pCertCtx[0]
            yield certCtx
            pCertCtx = CertEnumCertificatesInStore(self._hStore, pCertCtx)

    def itercrls(self):
        """Iterate over cert revocation lists
        """
        pCrlCtx = CertEnumCRLsInStore(self._hStore, None)
        while pCrlCtx:
            crlCtx = pCrlCtx[0]
            yield crlCtx
            pCrlCtx = CertEnumCRLsInStore(self._hStore, pCrlCtx)

    def __iter__(self):
        for cert in self.itercerts():
            yield cert
        for crl in self.itercrls():
            yield crl


if __name__ == "__main__":
    for storename in ("CA", "ROOT"):
        store = CertSystemStore(storename)
        try:
            for cert in store.itercerts():
                print(cert.get_pem().decode("ascii"))
        finally:
            store.close()
