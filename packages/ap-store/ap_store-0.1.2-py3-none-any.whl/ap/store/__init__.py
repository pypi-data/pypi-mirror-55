import click
import sqlite3
import logging
import pathlib
import os
import ap.store.database as database

def configure_verbose(ctx, param, value):
    if ctx.resilient_parsing:
        return

    level = logging.INFO if value else logging.WARNING
    logging.basicConfig(level=level)

    return value

@click.group()
@click.option('--verbose', '-v', is_flag=True, default=False, callback=configure_verbose)
@click.option('--data-file', '-f', 'data_file', type=click.File)
def execute(verbose, data_file):
    """Primary execution context"""
    logger = logging.getLogger('store.execute')
    logger.info('primary execution context')
    logger.info('checking for existing installation')

    if data_file is None:
        data_file = os.environ.get('AP_STORE_DATA_FILE_PATH', None)

    if data_file is None:
        storage_dir = pathlib.Path().home() / '.pstore'
        if not storage_dir.exists():
            storage_dir.mkdir(parents=True)

        data_file = storage_dir / 'pstore.db'

    logger.info(f'using data file path: {data_file}')
    database.initialize(data_file)

@execute.command()
@click.argument('key')
def get(key):
    """store get KEY returns VALUE"""
    logger = logging.getLogger('store.get')
    logger.info(f'store get {key}')
    print(database.get(key))

@execute.command()
@click.argument('partial')
def search(partial):
    """store search PARTIAL returns [VALUE, ...]"""
    logger = logging.getLogger('store.search')
    logger.info(f'store search {partial}')
    print(database.search(partial))

@execute.command()
def list():
    """store list returns [KEY, ...]"""
    logger = logging.getLogger('store.list')
    logger.info('store list')
    print(database.list())

@execute.command()
@click.argument('key', nargs=1)
@click.argument('value', nargs=-1)
def put(key, value):
    """store put KEY VALUE"""
    logger = logging.getLogger('store.put')

    value = ' '.join(value)
    logger.info(f'store put {key} -> {value}')
    database.insert(key, value)

@execute.command()
@click.argument('key')
def delete(key):
    """store delete KEY"""
    logger= logging.getLogger('store.delete')
    logger.info(f'store delete {key}')
    database.delete(key)
