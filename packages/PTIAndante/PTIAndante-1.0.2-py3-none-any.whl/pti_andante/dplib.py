"""
dplib.py

Demand planner library
"""

import csv
import datetime
from dateutil.relativedelta import *
from loguru import logger

MTH_SHORT = {
             'JAN': 1, 'FEB': 2, 'MAR': 3, 'APR': 4,
             'MEI': 5, 'JUN': 6, 'JUL': 7, 'AGT': 8,
             'SEP': 9, 'OKT': 10, 'NOV': 11, 'DEC': 12,
             'DES': 12,
            }

def write_csv_dict(rows, fields, file_name):
    with open(file_name, 'wt') as f:
        writer = csv.DictWriter(f, fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

def pivot_sheet(sheet):
    """
    Create pivot from sheet.

    :param sheet: The sheet to pivot
    :type sheet: XLRD Sheet object
    :returns: Pivot data
    :rtype: list
    """
    # Find table header row
    header_row = -1
    for row in range(sheet.nrows):
        cells = sheet.row_values(row)
        col = 0
        for cell in cells:
            if cell == '1BASELINE':
                header_row = row
                break
            col += 1
        if header_row != -1:
            break

    if header_row == -1:
        raise Exception('Could not find header signature: 1BASELINE')

    logger.info('Header found at row {}'.format(header_row))

    # Find columns
    columns = {
            'BRAND': -1,
            'NO': -1,
            'KOITEM': -1,
            'PERSENTASE': -1,
            '1BASELINE': -1,
            '1UPLIFT': -1,
            '1NPD': -1,
            '1Uplift NOO': -1,
    }
    header_cells = sheet.row_values(header_row)
    col = 0
    for cell in header_cells:
        if cell in columns:
            columns[cell] = col
        col += 1

    for col_key in columns:
        if columns[col_key] == -1:
            raise Exception('Column not found: {}'.format(col_key))

    # Find first month
    month_info = header_cells[columns['PERSENTASE']+1].split("'")
    date_str = '20{}-{}-1'.format(month_info[1], MTH_SHORT[month_info[0]])
    logger.info('Start date detected: {}'.format(date_str))
    date_start = datetime.datetime.strptime(date_str, '%Y-%m-%d')

    # Now read data
    result = []
    for row in range(header_row+1, sheet.nrows):
        cells = sheet.row_values(row)
        for serie in range(18):
            ddate = date_start + relativedelta(months = serie)
            result.append({
                    '_s': serie,
                    'ID': '{}{}{}'.format(
                                          cells[columns['BRAND']],
                                          cells[columns['KOITEM']],
                                          ddate.strftime('%Y%m')
                                         ),
                    'BRAND': cells[columns['BRAND']],
                    'NO': cells[columns['NO']],
                    'KOITEM': cells[columns['KOITEM']],
                    'DATE': ddate.strftime('%b-%y'),
                    'Rev Baseline': cells[columns['1BASELINE'] + serie],
                    'Rev Uplift': cells[columns['1UPLIFT'] + serie],
                    'Rev Uplift NPD': cells[columns['1NPD'] + serie],
                    'Rev Uplift NOO': cells[columns['1Uplift NOO'] + serie]
            })

    brand_order = {
                   'WARDAH': 1,
                   'WARDAH MALAYSIA': 2,
                   'MAKE OVER': 3,
                   'EMINA': 4,
                   'PUTRI': 5,
                   'CHIC': 6,
                   'X': 7
                  }
    return sorted(result, key=lambda x: (x['_s'], brand_order[x['BRAND']], x['NO']))
