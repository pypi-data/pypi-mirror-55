import sys
import os
import sys
import setuptools
from setuptools import find_packages
from setuptools.command.test import test as TestCommand
from distutils.version import StrictVersion
from setuptools import __version__ as setuptools_version

if StrictVersion(setuptools_version) < StrictVersion("38.3.0"):
    raise SystemExit(
        "Your `setuptools` version is old. "
        "Please upgrade setuptools by running `pip install -U setuptools` "
        "and try again."
    )


def readme():
    with open("README.md") as f:
        return f.read()


setuptools.setup(
    name="gee2drive",
    version="0.1.0",
    packages=find_packages(),
    url="https://github.com/samapriya/gee2drive",
    install_requires=[
        "earthengine-api>=0.1.191",
        "gitpython>=2.1.11",
        'shapely>=1.6.4;platform_system!="Windows"',
        "pendulum>=2.0.2",
        "Pygments>=2.2.0",
        "prettytable>=0.7.2",
    ],
    license="Apache 2.0",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=(
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: GIS",
    ),
    author="Samapriya Roy",
    author_email="samapriya.roy@gmail.com",
    description="Google Earth Engine to Drive Export Manager",
    entry_points={"console_scripts": ["gee2drive=gee2drive.gee2drive:main"]},
)
