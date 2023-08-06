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
    'version': '0.1.2',
    'description': 'Extract data from Excel documents.',
    'long_description': '# exex [![Build Status](https://travis-ci.org/vikpe/python-package-starter.svg?branch=master)](https://travis-ci.org/vikpe/python-package-starter) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n> Extract data from Excel documents\n\n## Features\n* Extract data from Excel (xlsx)\n* Format result as JSON, JSONL, XML\n\n## Installation\n```sh\npip install exex\n```\n\n## Usage\n\n![Sample Excel file](https://raw.githubusercontent.com/vikpe/exex/master/docs/sample_xlsx.png "Sample Excel file")\n\n```python\nfrom exex import extract\n\next = extract.Extractor(\'sample.xlsx\')\next.all()\next.range("A1:B2")\next.cell("A1")\next.cells("A1", "B2")\n```\n\n## Development\n\n**Tests** (local Python version)\n```sh\npoetry run pytest\n```\n\n**Tests** (all Python versions defined in `tox.ini`)\n```sh\npoetry run tox\n```\n\n**Code formatting** (black)\n```sh\npoetry run black .\n```\n',
    'author': 'Viktor Persson',
    'author_email': None,
    'url': 'https://github.com/vikpe/exex',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
