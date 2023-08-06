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
    'version': '0.1.7',
    'description': 'Extract data from Excel documents.',
    'long_description': '# exex [![Build Status](https://travis-ci.org/vikpe/exex.svg?branch=master)](https://travis-ci.org/vikpe/exex) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n> Extract data from Excel documents\n\n## Installation\n```sh\npip install exex\n```\n\n## Usage\n\n![Sample Excel file](https://raw.githubusercontent.com/vikpe/exex/master/docs/sample_xlsx.png "Sample Excel file")\n\n```python\nfrom openpyxl import load_workbook\nfrom exex import parse\n\nbook = load_workbook("sample.xlsx") # load excel file\nsheet = book.active # get active sheet\n\n# single cell by name\nparse.values(sheet["A1"])\n"name"                    \n\n# single cell by row/column number\nparse.values(sheet.cell(row=1, column=1)) \n"name"\n   \n# range of cells\nparse.values(sheet["A1":"B2"])\n[\n  ["name", "abbreviation"],\n  ["alpha", "a"],\n]\n\n# all values              \nparse.values(sheet.values)\n[\n  ["name", "abbreviation", "age"],\n  ["alpha", "a", 1],\n  ["beta", "b", 2],\n  ["gamma", "g", 3],\n]\n\n# row by number                  \nparse.values(sheet[1])\n["alpha", "a", 1]\n           \n# range of rows           \nparse.values(sheet[1:2])\n[\n  ["name", "abbreviation", "age"],\n  ["alpha", "a", 1],\n]\n\n# column by name            \nparse.values(sheet["A"])\n["name", "alpha", "beta", "gamma"]\n\n# column range\nparse.values(sheet["A:B"])\n[\n  ["name", "alpha"],\n  ["abbreviation", "a"],\n]\n```\n\n**Ways to access sheets**\n```python\n# Sheets\nbook.sheets[0]                # (sheet) sheet by index\nbook.sheets["prices"]         # (sheet) sheet by name\nbook.active                   # (sheet) active sheet\n\nbook.sheetnames               # (array) sheet names\n```\n\n## Development\n\n**Tests** (local Python version)\n```sh\npoetry run pytest\n```\n\n**Tests** (all Python versions defined in `tox.ini`)\n```sh\npoetry run tox\n```\n\n**Code formatting** (black)\n```sh\npoetry run black .\n```\n',
    'author': 'Viktor Persson',
    'author_email': None,
    'url': 'https://github.com/vikpe/exex',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
