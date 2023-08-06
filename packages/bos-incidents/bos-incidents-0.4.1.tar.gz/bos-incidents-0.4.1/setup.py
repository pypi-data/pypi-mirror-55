#!/usr/bin/env python

from setuptools import setup
import sys

__VERSION__ = "0.4.1"

assert sys.version_info[0] == 3, "We require Python > 3"

setup(
    name="bos-incidents",
    version=__VERSION__,
    description=("Private module for BOS incident storage"),
    long_description=open("README.md").read(),
    download_url="https://github.com/pbsa/bos-incidents/tarball/" + __VERSION__,
    author='Peerplays Community',
    maintainer='Peerplays Community',
    url='http://pbsa.info',
    keywords=["peerplays", "bos"],
    packages=["bos_incidents"],
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
    ],
    entry_points={"console_scripts": ["bos-incidents = bos_incidents.cli:main"]},
    install_requires=open("requirements.txt").readlines(),
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    include_package_data=True,
)
