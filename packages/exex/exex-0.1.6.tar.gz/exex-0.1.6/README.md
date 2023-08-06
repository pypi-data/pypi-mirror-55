# exex [![Build Status](https://travis-ci.org/vikpe/exex.svg?branch=master)](https://travis-ci.org/vikpe/exex) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
> Extract data from Excel documents

## Installation
```sh
pip install exex
```

## Usage

![Sample Excel file](https://raw.githubusercontent.com/vikpe/exex/master/docs/sample_xlsx.png "Sample Excel file")

**Use `openpyxl` to grab data**
```python
from openpyxl import load_workbook
book = load_workbook("sample.xlsx")

# Sheets
book.sheetnames               # (array) sheet names
book.sheets[0]                # (sheet) first sheet
book.sheets["prices"]         # (sheet) sheet by name
book.active                   # (sheet) active sheet

# Grab cells from active sheet
sheet = book.active

sheet["A1"]                   # (value) single cell by name
sheet.cell(row=1, column=1)   # (value) single cell by row/column
sheet["A1":"B2"]              # (array) range of cells
sheet.values                  # (array) all cells

sheet[5]                      # (array) single row
sheet[5:10]                   # (array) range of rows

sheet["C"]                    # (array) single column
sheet["A:C"]                  # (array) range of columns
```

**Use `exex.parse.values()` to get values**
```python
from exex import parse

parse.values(sheet["A1"])                   
parse.values(sheet.cell(row=1, column=1))   
parse.values(sheet["A1":"B2"])              
parse.values(sheet.values)                  
parse.values(sheet[5])                      
parse.values(sheet[5:10])                   
parse.values(sheet["C"])                    
parse.values(sheet["A:C"])                  
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
