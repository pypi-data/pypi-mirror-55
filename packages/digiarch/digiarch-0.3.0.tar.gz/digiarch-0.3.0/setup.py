# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['digiarch', 'digiarch.identify', 'digiarch.utils']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0',
 'dacite>=1.0,<2.0',
 'pandas>=0.25.1,<0.26.0',
 'tqdm>=4.36,<5.0']

entry_points = \
{'console_scripts': ['digiarch = digiarch.digiarch:cli']}

setup_kwargs = {
    'name': 'digiarch',
    'version': '0.3.0',
    'description': 'Tools for the Digital Archive Project at Aarhus Stadsarkiv',
    'long_description': '![Aarhus Stadsarkiv](Stadsarkiv.png)\n# Digital Archive [![CircleCI](https://circleci.com/gh/aarhusstadsarkiv/digital-archive/tree/master.svg?style=shield)](https://circleci.com/gh/aarhusstadsarkiv/digital-archive/tree/master) [![codecov](https://codecov.io/gh/aarhusstadsarkiv/digital-archive/branch/master/graph/badge.svg)](https://codecov.io/gh/aarhusstadsarkiv/digital-archive) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/74e85419f1334761ae22b447468835db)](https://www.codacy.com/manual/jnik-aarhus/digital-archive?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=aarhusstadsarkiv/digital-archive&amp;utm_campaign=Badge_Grade)\nThis repository contains code pertaining to the Digital Archive Project at Aarhus Stadsarkiv.\n',
    'author': 'Nina Jensen',
    'author_email': 'jnik@aarhus.dk',
    'url': 'https://stadsarkiv.aarhus.dk/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
