# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['teritorio']

package_data = \
{'': ['*'], 'teritorio': ['_data/*']}

setup_kwargs = {
    'name': 'teritorio',
    'version': '1.0.0',
    'description': 'A library for country and currency ISO codes',
    'long_description': '<p align="center">\n<a href="https://github.com/ambv/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>\n<a href="https://travis-ci.com/spapanik/teritorio"><img alt="Build Status" src="https://travis-ci.com/spapanik/teritorio.svg?branch=master"></a>\n</p>\n\n# teritorio: ISO codes for countries and currencies\n\n## Installation and usage\n\n### Installation\n\n_teritorio_ can be installed by running `pip install teritorio`. It requires Python 3.7.0+ to run.\n\n### Usage\n\nThe two main objects are `Countries` and `Currencies`:\n\n#### Countries usage\n\n```python\nfrom teritorio import Countries\n\n# list all countries\nfor country in Countries():\n    print(country)\n\n# get a specific country\ncountries = Countries()\n\n# access the country as an attribute\nprint(countries.DEU)  # Country(english_name=\'Germany\', french_name="Allemagne (l\')", alpha_2_code=\'DE\', alpha_3_code=\'DEU\', numeric_code=276)\n# access the country with square brackets\nprint(countries["DEU"])  # Country(english_name=\'Germany\', french_name="Allemagne (l\')", alpha_2_code=\'DE\', alpha_3_code=\'DEU\', numeric_code=276)\n```\n\n#### Currencies usage\n\n```python\nfrom teritorio import Currencies\n\n# list all currencies\nfor currency in Currencies():\n    print(currency)\n\n# get a specific currency\ncurrencies = Currencies()\n\n# access the currency as an attribute\nprint(currencies.GBP)  # Currency(code=\'GBP\', name=\'Pound Sterling\', entities=[\'GUERNSEY\', \'ISLE OF MAN\', \'JERSEY\', \'UNITED KINGDOM OF GREAT BRITAIN AND NORTHERN IRELAND (THE)\'], numeric_code=826, minor_units=2)\n# access the currency with square brackets\nprint(currencies["GBP"])  # Currency(code=\'GBP\', name=\'Pound Sterling\', entities=[\'GUERNSEY\', \'ISLE OF MAN\', \'JERSEY\', \'UNITED KINGDOM OF GREAT BRITAIN AND NORTHERN IRELAND (THE)\'], numeric_code=826, minor_units=2)\n```\n',
    'author': 'Stephanos Kuma',
    'author_email': 'spapanik21@gmail.com',
    'url': 'https://github.com/spapanik/teritorio',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
