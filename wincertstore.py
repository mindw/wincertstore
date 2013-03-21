#!/usr/bin/env python
#
# Copyright (c) 2013 by Christian Heimes <christian@python.org>
# Licensed to PSF under a Contributor Agreement.
# See http://www.python.org/psf/license for licensing details.
#
"""ctypes interface to Window's certificate store

Requirements:
  Windows XP, Windows Server 2003 or newer
  Python 2.6+
  Python 3.2+
"""
from ctypes import WinDLL, FormatError, get_last_error, string_at
from ctypes import Structure, POINTER, c_void_p
from ctypes.wintypes import LPCWSTR, DWORD, BOOL, BYTE
from base64 import b64encode

__all__ = ("CertSystemStore",)

HCERTSTORE = c_void_p
PCCERT_INFO = c_void_p
PCCRL_INFO = c_void_p
LPTCSTR = LPCWSTR

PKCS_7_ASN_ENCODING = 0x00010000

def isPKCS7(value):
    return (value & PKCS_7_ASN_ENCODING) == PKCS_7_ASN_ENCODING


class ContextStruct(Structure):
    cert_type = None

    def get_encoded(self):
        """Get encoded cert as byte string
        """
        pass

    @property
    def encoding_type(self):
        """Get encoding type for PEM
        """
        if isPKCS7(self.dwCertEncodingType):
            return b"PKCS7"
        else:
            return self.cert_type

    def get_pem(self):
        """Get PEM encoded cert
        """
        encoding_type = self.encoding_type
        b64data = b64encode(self.get_encoded())
        lines = [b"-----BEGIN " + encoding_type + b"-----"]
        # split up in lines of 64 chars each
        quotient, remainder = divmod(len(b64data), 64)
        linecount = quotient + bool(remainder)
        lines.extend(b64data[i*64:(i+1)*64] for i in range(linecount))
        lines.append(b"-----END " + encoding_type + b"-----")
        return b"\n".join(lines)


class CERT_CONTEXT(ContextStruct):
    """Cert context
    """
    cert_type = b"CERTIFICATE"
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
    cert_type = b"X509 CRL"
    _fields_ = [
        ("dwCertEncodingType", DWORD),
        ("pbCrlEncoded", POINTER(BYTE)),
        ("cbCrlEncoded", DWORD),
        ("pCrlInfo", PCCRL_INFO),
        ("hCertStore", HCERTSTORE),
        ]

    def get_encoded(self):
        return string_at(self.pbCrlEncoded, self.cbCrlEncoded)


crypt32 = WinDLL("crypt32.dll", use_last_error=True)

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

    def __init__(self, storename):
        self._storename = storename
        self._hStore = None

    @property
    def storename(self):
        """Get store name
        """
        return self._storename

    def __enter__(self):
        self._hStore = CertOpenSystemStore(None, self.storename)
        if not self._hStore:
            self._hStore = None
            errmsg = FormatError(get_last_error())
            raise OSError(errmsg)
        return self

    def __exit__(self, exc, value, tb):
        CertCloseStore(self._hStore, 0)
        self._hStore = None

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
        with CertSystemStore(storename) as store:
            for cert in store.itercerts():
                print(cert.get_pem().decode("ascii"))
