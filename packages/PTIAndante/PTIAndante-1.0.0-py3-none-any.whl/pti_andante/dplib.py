"""
dplib.py

Demand planner library
"""

import csv
from loguru import logger

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

    # Now read data
    result = []
    for row in range(header_row+1, sheet.nrows):
        cells = sheet.row_values(row)
        for serie in range(18):
            result.append({
                    'BRAND': cells[columns['BRAND']],
                    'NO': cells[columns['NO']],
                    'KOITEM': cells[columns['KOITEM']],
                    'Rev Baseline': cells[columns['1BASELINE'] + serie],
                    'Rev Uplift': cells[columns['1UPLIFT'] + serie],
                    'Rev Uplift NPD': cells[columns['1NPD'] + serie],
                    'Rev Uplift NOO': cells[columns['1Uplift NOO'] + serie]
            })

    return result
