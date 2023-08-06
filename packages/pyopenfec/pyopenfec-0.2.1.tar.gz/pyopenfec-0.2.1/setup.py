# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pyopenfec']

package_data = \
{'': ['*']}

install_requires = \
['pytz>=2019.3,<2020.0', 'requests>=2.22,<3.0']

setup_kwargs = {
    'name': 'pyopenfec',
    'version': '0.2.1',
    'description': 'OpenFEC API Client',
    'long_description': None,
    'author': 'Jeremy Bowers',
    'author_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
