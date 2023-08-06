#!/usr/bin/env python
from __future__ import (print_function as _pf,
                        unicode_literals as _ul,
                        absolute_import as _ai)
from glidertools import __version__
from setuptools import setup, find_packages
import os


long_description = """
Glider Tools
============

Glider tools is a Python 3.6+ package designed to process data from the first level of processing to a science ready dataset. The package is designed to easily import data to a standard column format (numpy.ndarray or pandas.DataFrame). Cleaning and smoothing functions are flexible and can be applied as required by the user. We provide examples and demonstrate best practices as developed by the SOCCO Group (http://socco.org.za/).

Please cite the original publication of this package and the version that you've used: Reference here with <#link_to_the_paper>

Installation
------------

PyPI
....
To install the core package run: ``pip install glidertools``.

GitLab
......
1. Clone glidertools to your local machine: `git clone --depth 1 https://gitlab.com/socco/GliderTools` (--depth 1 reduces the download size)
2. Change to the parent directory of GliderTools
3. Install glidertools with `pip install -e ./GliderTools`. This will allow changes you make locally, to be reflected when you import the package in Python

Recommended, but optional packages
..................................
There are some packages that are not installed by default, as these are large packages or can result in installation errors, resulting in failure to install GliderTools. These should install automatically with ``pip install package_name``:

* ``gsw``: accurate density calculation (may fail in some cases)
* ``pykrige``: variogram plotting (installation generally works, except when bundled)
* ``plotly``: interactive 3D plots (large package)


How you can contribute
----------------------
- Error reporting with using GitLab (https://gitlab.com/socco/GliderTools/issues/new). Please copy the entire error message (even if it's long).
- Detailed error reporting so users know where the fault lies.
- Oxygen processing is rudimentary as we do not have the expertise in our group to address this

Acknowledgements
----------------
- We rely heavily on ``ion_functions.data.flo_functions`` which was written by Christopher Wingard, Craig Risien, Russell Desiderio
- This work was initially funded by Pedro M Scheel Monteiro at the Council for Scientific and Industrial Research (where Luke was working at the time of writing the code).
- Testers for their feedback: SOCCO team at the CSIR and ...

"""


def walker(base, *paths):
    file_list = set([])
    cur_dir = os.path.abspath(os.curdir)

    os.chdir(base)
    try:
        for path in paths:
            for dname, _, files in os.walk(path):
                for f in files:
                    file_list.add(os.path.join(dname, f))
    finally:
        os.chdir(cur_dir)

    return list(file_list)


setup(
    # Application name:
    name="glidertools",

    # Version number (initial):
    version=__version__,

    # Application author details:
    author="Luke Gregor",
    author_email="luke.gregor@usys.ethz.ch",

    # Packages
    packages=find_packages(),

    # Include additional files into the package
    include_package_data=True,

    # Details
    url="https://gitlab.com/socco/GliderTools",

    license="GPLv3 License",
    description='Tools and utilities for buoyancy glider data processing. ',

    long_description=long_description,

    # Dependent packages (distributions)
    install_requires=[
        "matplotlib",
        "seawater",
        "tqdm",
        "scipy",
        "scikit-learn",
        "numpy",
        "xarray",
        "pandas",
        "astral",
        "netCDF4",
        "numexpr",
        # "pykrige",
        "m2r",
    ],
)
