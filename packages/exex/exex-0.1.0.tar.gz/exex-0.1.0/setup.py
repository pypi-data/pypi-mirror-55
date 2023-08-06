# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['exex']

package_data = \
{'': ['*']}

install_requires = \
['openpyxl>=3.0,<4.0']

setup_kwargs = {
    'name': 'exex',
    'version': '0.1.0',
    'description': 'Excel extractor written in Python.',
    'long_description': None,
    'author': 'Viktor Persson',
    'author_email': 'viktor.persson@arcsin.se',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
