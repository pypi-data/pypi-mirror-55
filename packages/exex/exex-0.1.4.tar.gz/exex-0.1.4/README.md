# exex [![Build Status](https://travis-ci.org/vikpe/python-package-starter.svg?branch=master)](https://travis-ci.org/vikpe/python-package-starter) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
> Extract data from Excel documents

## Features
* Extract data from Excel (xlsx)
* Format result as JSON, JSONL, XML

## Installation
```sh
pip install exex
```

## Usage

![Sample Excel file](https://raw.githubusercontent.com/vikpe/exex/master/docs/sample_xlsx.png "Sample Excel file")

```python
from exex import extract

ext = extract.Extractor('sample.xlsx')

# Sheets
ext.sheetnames               # (array) sheet names
ext.sheets.active            # (sheet) active sheet
ext.sheets[0]                # (sheet) first sheet
ext.sheets["prices"]         # (sheet) sheet by name

# Cells
sheet["A1"]                  # (value) single cell by name
sheet.cell(row=1, column=1)  # (value) single cell by row/column
sheet["A1":"B2"]             # (array) range of cells

sheet.all()                  # (array) all cells
sheet.cells(["A1", "B2"])    # (array) multiple cells by name

# Rows
sheet[5]                     # (array) single row
sheet[5:10]                  # (array) range of rows

# Columns
sheet["C"]                   # (array) single column
sheet["A:C"]                 # (array) range of columns
```

## Development

**Tests** (local Python version)
```sh
poetry run pytest
```

**Tests** (all Python versions defined in `tox.ini`)
```sh
poetry run tox
```

**Code formatting** (black)
```sh
poetry run black .
```
