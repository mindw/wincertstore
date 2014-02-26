#!/usr/bin/env python
import sys
import os
try:
    from setuptools.core import setup
except ImportError:
    from distutils.core import setup
from distutils.core import Command
try:
    import subprocess
except ImportError:
    subprocess = None


class PyTest(Command):
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        if subprocess is None:
            exe = sys.executable
            errno = os.spawnl(os.P_WAIT, exe, os.path.basename(exe),
                              "tests.py")
        else:
            errno = subprocess.call([sys.executable, "tests.py"])
        raise SystemExit(errno)


def _read(fname):
    f = open(fname)
    try:
        return f.read()
    finally:
        f.close()

long_description = [_read("README.txt"), _read("CHANGES.txt")]

setup(
    name="wincertstore",
    version="0.2",
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
