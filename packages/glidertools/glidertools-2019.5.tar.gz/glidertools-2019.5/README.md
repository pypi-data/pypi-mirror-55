Glider Tools
============

[![](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) [![](https://badgen.net/pypi/v/glidertools)](https://pypi.org/project/glidertools/) [![](https://img.shields.io/badge/DOI-10.6084%2Fm9.figshare.9724586.v1-blue)](https://doi.org/10.6084/m9.figshare.9724586.v1) [![](https://readthedocs.org/projects/glidertools/badge/?version=latest)](https://glidertools.readthedocs.io/en/latest/)


Glider tools is a Python 3.6+ package designed to process data from the first level of processing to a science ready dataset. The package is designed to easily import data to a standard column format (numpy.ndarray or pandas.DataFrame). Cleaning and smoothing functions are flexible and can be applied as required by the user. We provide examples and demonstrate best practices as developed by the [SOCCO Group](http://socco.org.za/).

Please cite the original publication of this package and the version that you've used: (in review). Until published, please cite as recomended by the DIO:
*Gregor, Luke; Ryan-Keogh, Thomas; Nicholson, Sarah-Anne; du Plessis, Marcel; Giddy, Isabelle; Swart, Sebastiaan (2019): GliderTools: A Python toolbox for processing underwater glider data. figshare. Software. DOI: https://doi.org/10.6084/m9.figshare.9724586.v1*

Installation
------------

##### PyPI
To install the core package run: `pip install glidertools`.

##### GitLab (for latest version)
1. Clone glidertools to your local machine: `git clone --depth 1 https://gitlab.com/socco/GliderTools` (--depth 1 reduces the download size)
2. Change to the parent directory of GliderTools
3. Install glidertools with `pip install -e ./GliderTools`. This will allow changes you make locally, to be reflected when you import the package in Python

##### Recommended, but optional packages
There are some packages that are not installed by default, as these are large packages or can result in installation errors, resulting in failure to install GliderTools. These should install automatically with `pip install <package_name>`:

- `gsw`: accurate density calculation (may fail in some cases)
- `pykrige`: variogram plotting (installation generally works, except when bundled)
- `plotly`: interactive 3D plots (large package)


How you can contribute
-----
- Error reporting with using GitLab (https://gitlab.com/socco/GliderTools/issues/new). Please copy the entire error message (even if it's long).
- Detailed error reporting so users know where the fault lies.
- Oxygen processing is rudimentary as we do not have the expertise in our group to address this

Acknowledgements
----------------
- We rely heavily on `ion_functions.data.flo_functions` which was written by Christopher Wingard, Craig Risien, Russell Desiderio
- This work was initially funded by Pedro M Scheel Monteiro at the Council for Scientific and Industrial Research (where Luke was working at the time of writing the code).
- Testers for their feedback: SOCCO team at the CSIR and ...
