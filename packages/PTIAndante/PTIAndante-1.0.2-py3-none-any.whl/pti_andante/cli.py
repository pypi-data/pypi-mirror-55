import click
import csv
import xlrd
from loguru import logger
import os
import errno

from . import dplib

@click.group()
def cli():
    pass

def makedirs(dirname):
    try:
        os.makedirs(dirname)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

@cli.command()
@click.argument('input_file')
@click.option('--output-dir', help='Output directory')
def writecsv(input_file, output_dir):
    if not output_dir:
        output_dir = os.path.join(os.path.dirname(input_file), 'csv')
        makedirs(output_dir)
        
    logger.info('Loading file: {}'.format(input_file))
    workbook = xlrd.open_workbook(input_file)
    for sheet in workbook.sheets():
        logger.info('Processing sheet {}'.format(sheet.name))
        with open(os.path.join(output_dir, '{}.csv'.format(sheet.name)), 'wt') as f:
            writer = csv.writer(f)
            for row in range(sheet.nrows):
                out = []
                for cell in sheet.row_values(row):
                    try:
                        out.append(cell.encode('utf8').decode('utf8'))
                    except:
                        out.append(cell)
                writer.writerow(out)

@cli.command()
@click.argument('input_file')
@click.option('--output-dir', help='Output directory') 
def pivot(input_file, output_dir):
    if not output_dir:
        output_dir = os.path.join(os.path.dirname(input_file), 'pivot')
        makedirs(output_dir)

    logger.info('Loading file: {}'.format(input_file))
    workbook = xlrd.open_workbook(input_file)
    sheet_names = ['RAW AVGL3M CO REAL', 'RAW AVGL3M CO REAL (MY)']
    for sheet_name in sheet_names:
        sheet = workbook.sheet_by_name(sheet_name)
        if sheet:
            logger.info('Processing sheet {}'.format(sheet.name))
            trans = dplib.pivot_sheet(sheet)
            if trans:
                field_names = [t for t in trans[0]]
                file_name = os.path.join(output_dir, '{} - PIVOT.csv'.format(sheet.name))
                dplib.write_csv_dict(trans, field_names, file_name)


if __name__ == '__main__':
    cli()
