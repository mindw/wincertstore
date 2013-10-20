============
wincertstore
============

Example
=======

::

    import wincertstore
    for storename in ("CA", "ROOT"):
        with wincertstore.CertSystemStore(storename) as store:
            for cert in store.itercerts():
                print(cert.get_pem().decode("ascii"))
                print(cert.get_name())
                print(cert.enhanced_keyusage_names())


For Python versions with with statement::

    for storename in ("CA", "ROOT"):
        store = wincertstore.CertSystemStore(storename)
        try:
            for cert in store.itercerts():
                print(cert.get_pem().decode("ascii")
        finally:
            store.close()

See `CertOpenSystemStore`_

::

    import wincertstore
    import atexit
    import ssl

    certfile = wincertstore.CertFile()
    certfile.addstore("CA")
    certfile.addstore("ROOT")
    atexit.register(certfile.close) # cleanup and remove files on shutdown)

    ssl_sock = ssl.wrap_socket(sock,
                               ca_certs=certfile.name,
                               cert_reqs=ssl.CERT_REQUIRED)


Requirements
============

- Python 2.3 to 3.3

- Windows XP, Windows Server 2003 or newer

- ctypes 1.0.2 (Python 2.3 and 2.4)
  from http://sourceforge.net/projects/ctypes/

  
License
=======

Copyright (c) 2013 by Christian Heimes <christian@python.org>

Licensed to PSF under a Contributor Agreement.

See http://www.python.org/psf/license for licensing details.


Acknowledgements
================

http://fixunix.com/openssl/254866-re-can-openssl-use-windows-certificate-store.html

http://bugs.python.org/issue17134


References
==========

.. _CertOpenSystemStore: http://msdn.microsoft.com/en-us/library/windows/desktop/aa376560%28v=vs.85%29.aspx
