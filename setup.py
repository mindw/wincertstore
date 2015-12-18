#!/usr/bin/env python

from setuptools import setup


def _read(fname):
    with open(fname) as f:
        return f.read()

long_description = [_read("README.txt"), _read("CHANGES.txt")]

setup(
    name="wincertstore",
    version="0.2",
    setup_requires=['pytest-runner'],
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
    description="Python module to extract CA and CRL certs from Windows' cert store (ctypes based).",
    long_description="\n".join(long_description),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Python Software Foundation License",
        "Natural Language :: English",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.3",
        "Programming Language :: Python :: 2.4",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
    ],
)
