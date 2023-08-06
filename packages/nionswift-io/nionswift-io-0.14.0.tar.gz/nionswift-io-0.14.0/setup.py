# -*- coding: utf-8 -*-

"""
To upload to PyPI, PyPI test, or a local server:
python setup.py bdist_wheel upload -r <server_identifier>
"""

import setuptools
import os

setuptools.setup(
    name="nionswift-io",
    version="0.14.0",
    author="Nion Software",
    author_email="swift@nion.com",
    description="IO handlers for NionSwift.",
    long_description=open("README.rst").read(),
    url="https://github.com/nion-software/nionswift-io",
    packages=["nionswift_plugin.DM_IO", "nionswift_plugin.DM_IO.test", "nionswift_plugin.TIFF_IO", "nionswift_plugin.TIFF_IO.test"],
    install_requires=["niondata>=0.13.1"],
    tests_require=["h5py"],
    license='Apache 2.0',
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3.6",
    ],
    include_package_data=True,
    python_requires='~=3.6',
)
