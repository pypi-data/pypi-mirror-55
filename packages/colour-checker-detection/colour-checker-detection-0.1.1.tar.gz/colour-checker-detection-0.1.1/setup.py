# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['colour_checker_detection',
 'colour_checker_detection.detection',
 'colour_checker_detection.detection.tests']

package_data = \
{'': ['*'],
 'colour_checker_detection': ['examples/*',
                              'resources/colour-checker-detection-examples-datasets/*',
                              'resources/colour-checker-detection-tests-datasets/*',
                              'resources/colour-checker-detection-tests-datasets/colour_checker_detection/*']}

install_requires = \
['colour-science>=0.3.14,<0.4.0', 'opencv-python>=4,<5']

extras_require = \
{'development': ['biblib-simple',
                 'coverage',
                 'coveralls',
                 'flake8',
                 'invoke',
                 'jupyter',
                 'matplotlib',
                 'mock',
                 'nose',
                 'pre-commit',
                 'pytest',
                 'restructuredtext-lint',
                 'sphinx',
                 'sphinx_rtd_theme',
                 'sphinxcontrib-bibtex',
                 'toml',
                 'twine',
                 'yapf==0.23'],
 'read-the-docs': ['mock', 'numpy', 'sphinxcontrib-bibtex']}

setup_kwargs = {
    'name': 'colour-checker-detection',
    'version': '0.1.1',
    'description': 'Colour checker detection with Python',
    'long_description': "Colour - Checker Detection\n==========================\n\n.. start-badges\n\n|actions| |coveralls| |codacy| |version|\n\n.. |actions| image:: https://github.com/colour-science/colour-checker-detection/workflows/Continuous%20Integration/badge.svg\n    :target: https://github.com/colour-science/colour-checker-detection/actions\n    :alt: Develop Build Status\n.. |coveralls| image:: http://img.shields.io/coveralls/colour-science/colour-checker-detection/develop.svg?style=flat-square\n    :target: https://coveralls.io/r/colour-science/colour-checker-detection\n    :alt: Coverage Status\n.. |codacy| image:: https://img.shields.io/codacy/grade/984900e3a85e40239a0f8f633dd1ebcb/develop.svg?style=flat-square\n    :target: https://www.codacy.com/app/colour-science/colour-checker-detection\n    :alt: Code Grade\n.. |version| image:: https://img.shields.io/pypi/v/colour-checker-detection.svg?style=flat-square\n    :target: https://pypi.org/project/colour-checker-detection\n    :alt: Package Version\n\n.. end-badges\n\n\nA `Python <https://www.python.org/>`__ package implementing various colour\nchecker detection algorithms and related utilities.\n\nIt is open source and freely available under the\n`New BSD License <https://opensource.org/licenses/BSD-3-Clause>`__ terms.\n\n..  image:: https://raw.githubusercontent.com/colour-science/colour-checker-detection/master/docs/_static/ColourCheckerDetection_001.png\n\n.. contents:: **Table of Contents**\n    :backlinks: none\n    :depth: 3\n\n.. sectnum::\n\nFeatures\n--------\n\nThe following colour checker detection algorithms are implemented:\n\n-   Segmentation\n\nInstallation\n------------\n\nBecause of their size, the resources dependencies needed to run the various\nexamples and unit tests are not provided within the Pypi package. They are\nseparately available as\n`Git Submodules <https://git-scm.com/book/en/v2/Git-Tools-Submodules>`__\nwhen cloning the\n`repository <https://github.com/colour-science/colour-checker-detection>`__.\n\nPrimary Dependencies\n^^^^^^^^^^^^^^^^^^^^\n\n**Colour - Checker Detection** requires various dependencies in order to run:\n\n-  `Python >=3.5 <https://www.python.org/download/releases/>`__\n-  `Colour Science <https://www.colour-science.org>`__\n-  `opencv-python >=4 <https://pypi.org/project/opencv-python/>`__\n\nPypi\n^^^^\n\nOnce the dependencies satisfied, **Colour - Checker Detection** can be installed from\nthe `Python Package Index <http://pypi.python.org/pypi/colour-checker-detection>`__ by\nissuing this command in a shell::\n\n\tpip install colour-checker-detection\n\nThe overall development dependencies are installed as follows::\n\n    pip install 'colour-checker-detection[development]'\n\nUsage\n-----\n\nAPI\n^^^\n\nThe main reference for `Colour - Checker Detection <https://github.com/colour-science/colour-checker-detection>`__\nis the `Colour - Checker Detection Manual <https://colour-checker-detection.readthedocs.io/en/latest/manual.html>`__.\n\nExamples\n^^^^^^^^\n\nVarious usage examples are available from the\n`examples directory <https://github.com/colour-science/colour-checker-detection/tree/master/colour_checker_detection/examples>`__.\n\nContributing\n------------\n\nIf you would like to contribute to `Colour - Checker Detection <https://github.com/colour-science/colour-checker-detection>`__,\nplease refer to the following `Contributing <https://www.colour-science.org/contributing/>`__\nguide for `Colour <https://github.com/colour-science/colour>`__.\n\nBibliography\n------------\n\nThe bibliography is available in the repository in\n`BibTeX <https://github.com/colour-science/colour-checker-detection/blob/develop/BIBLIOGRAPHY.bib>`__\nformat.\n\nCode of Conduct\n---------------\n\nThe *Code of Conduct*, adapted from the `Contributor Covenant 1.4 <https://www.contributor-covenant.org/version/1/4/code-of-conduct.html>`__,\nis available on the `Code of Conduct <https://www.colour-science.org/code-of-conduct/>`__ page.\n\nAbout\n-----\n\n| **Colour - Checker Detection** by Colour Developers\n| Copyright © 2018-2019 – Colour Developers – `colour-science@googlegroups.com <colour-science@googlegroups.com>`__\n| This software is released under terms of New BSD License: https://opensource.org/licenses/BSD-3-Clause\n| `https://github.com/colour-science/colour-checker-detection <https://github.com/colour-science/colour-checker-detection>`__\n",
    'author': 'Colour Developers',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.colour-science.org/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
