#!/usr/bin/env python3
"""Set up past time."""
import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()

if sys.argv[-1] == "publish":
    os.system("python3 setup.py sdist upload")
    sys.exit()

setup(
    name="past_time",
    version="0.1.0",
    description="Visualizer for the days of the year",
    long_description=long_description,
    url="https://github.com/fabaff/time-past",
    download_url="https://github.com/fabaff/past-time/releases",
    author="Fabian Affolter",
    author_email="fabian@affolter-engineering.ch",
    license="MIT",
    install_requires=["tqdm", "click"],
    packages=["past_time"],
    zip_safe=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Utilities",
    ],
    entry_points={"console_scripts": ["past-time = past_time.__init__:cli"]},
)
