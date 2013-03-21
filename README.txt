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
                print(cert.get_pem().decode("ascii")

See `CertOpenSystemStore`_


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
