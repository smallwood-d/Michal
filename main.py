from openpyxl import load_workbook

from os import path
from table import Table

import logging
logging.basicConfig(format=logging.BASIC_FORMAT)
logger = logging.getLogger('main')

import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-c', '--compound', type=str, nargs='+',
                    help='an integer for the accumulator')
parser.add_argument('--workbook', action='store_const', type=str,
                    help='xlsx workbook path')
parser.add_argument('-o', '--out', action='store_const', type=str,
                    help='xlsx workbook output path')

args = parser.parse_args()
print(args)

wb = load_workbook(filename = path.join('.','resources', 'example.xlsx'))
print(wb.sheetnames)
ws = wb['מרוכז חדש']

c = ws.cell(12,2)

print(c.value)
print(ws.max_column)
for t in Table.find_compound_cells(ws):
    t.fill_table()
    break

# wb.save(path.join('.','resources', 'example1.xlsx'))



# Save the file
#wb.save("sample.xlsx")



# print(getRealNamePubChem('Bicyclo[2.2.1]heptane, 7,7-dimethyl-2-methylene-'))