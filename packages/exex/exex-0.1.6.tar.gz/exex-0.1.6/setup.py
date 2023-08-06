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
    'version': '0.1.6',
    'description': 'Extract data from Excel documents.',
    'long_description': '# exex [![Build Status](https://travis-ci.org/vikpe/exex.svg?branch=master)](https://travis-ci.org/vikpe/exex) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n> Extract data from Excel documents\n\n## Installation\n```sh\npip install exex\n```\n\n## Usage\n\n![Sample Excel file](https://raw.githubusercontent.com/vikpe/exex/master/docs/sample_xlsx.png "Sample Excel file")\n\n**Use `openpyxl` to grab data**\n```python\nfrom openpyxl import load_workbook\nbook = load_workbook("sample.xlsx")\n\n# Sheets\nbook.sheetnames               # (array) sheet names\nbook.sheets[0]                # (sheet) first sheet\nbook.sheets["prices"]         # (sheet) sheet by name\nbook.active                   # (sheet) active sheet\n\n# Grab cells from active sheet\nsheet = book.active\n\nsheet["A1"]                   # (value) single cell by name\nsheet.cell(row=1, column=1)   # (value) single cell by row/column\nsheet["A1":"B2"]              # (array) range of cells\nsheet.values                  # (array) all cells\n\nsheet[5]                      # (array) single row\nsheet[5:10]                   # (array) range of rows\n\nsheet["C"]                    # (array) single column\nsheet["A:C"]                  # (array) range of columns\n```\n\n**Use `exex.parse.values()` to get values**\n```python\nfrom exex import parse\n\nparse.values(sheet["A1"])                   \nparse.values(sheet.cell(row=1, column=1))   \nparse.values(sheet["A1":"B2"])              \nparse.values(sheet.values)                  \nparse.values(sheet[5])                      \nparse.values(sheet[5:10])                   \nparse.values(sheet["C"])                    \nparse.values(sheet["A:C"])                  \n```\n\n## Development\n\n**Tests** (local Python version)\n```sh\npoetry run pytest\n```\n\n**Tests** (all Python versions defined in `tox.ini`)\n```sh\npoetry run tox\n```\n\n**Code formatting** (black)\n```sh\npoetry run black .\n```\n',
    'author': 'Viktor Persson',
    'author_email': None,
    'url': 'https://github.com/vikpe/exex',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
