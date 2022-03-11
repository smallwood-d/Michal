from inspect import _void
import requests
from bs4 import BeautifulSoup
from pubchempy import get_compounds
from openpyxl import Workbook, load_workbook

from os import path
from table import Table

import logging
logging.basicConfig(format=logging.BASIC_FORMAT)
logger = logging.getLogger('main')


wb = load_workbook(filename = path.join('.','resources', 'example.xlsx'))
print(wb.sheetnames)
ws = wb['מרוכז חדש']

c = ws.cell(12,2)

print(c.value)
print(ws.max_column)
for t in Table.find_compound_cells(ws):
    t.fill_table()
    break

wb.save(path.join('.','resources', 'example1.xlsx'))



# Save the file
#wb.save("sample.xlsx")



# print(getRealNamePubChem('Bicyclo[2.2.1]heptane, 7,7-dimethyl-2-methylene-'))