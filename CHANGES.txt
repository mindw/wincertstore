Changelog
=========

wincertstore 0.2
----------------

*Release date: 26-Feb-2013*

- By default CertSystemStore.itercerts() is now limited to return only
  certs that are suitable for SERVER_AUTH -- that is to validate a TLS/SSL's
  server cert from the perspective of a client.

- Add CERT_CONTEXT.get_name() to get a human readable name of a certificate.

- Add CERT_CONTEXT.enhanced_keyusage() to get enhanced key usage and trust
  settings from registry. The method returns either ``True`` or a frozenset
  of OIDs. True means that the certificate is valid for any purpose.

- CERT_CONTEXT.enhanced_keyusage_names() maps OIDs to human readable names.

- Add commin OIDs for enhanced key usages like SERVER_AUTH and CLIENT_AUTH.

- Add support for universal wheels.

- Add tox for testing Python 2.6 to 3.3. Python 2.4 and 2.5 are tested
  manually.

- Use pypi.python.org:443 for TLS tests.


wincertstore 0.1
----------------

*Release date: 22-Mar-2013*

- Initial release
