#!/usr/bin/env python
from __future__ import absolute_import
import sys
from distutils.core import setup, Command
import subprocess

class PyTest(Command):
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        errno = subprocess.call([sys.executable, "tests.py"])
        raise SystemExit(errno)


long_description = []
with open("README.txt") as f:
    long_description.append(f.read())
with open("CHANGES.txt") as f:
    long_description.append(f.read())

setup(
    name="wincertstore",
    version="0.1",
    cmdclass={"test": PyTest},
    py_modules=["wincertstore"],
    author="Christian Heimes",
    author_email="christian@python.org",
    maintainer="Christian Heimes",
    maintainer_email="christian@python.org",
    url="https://bitbucket.org/tiran/wincertstore",
    download_url="http://pypi.python.org/pypi/wincertstore",
    keywords="windows cert ssl ca crl",
    platforms="Windows",
    license="PSFL",
    description="Python module to extract CA and CRL certs from Window's cert store (ctypes based).",
    long_description="\n".join(long_description),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Python Software Foundation License",
        "Natural Language :: English",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
    ],
)
