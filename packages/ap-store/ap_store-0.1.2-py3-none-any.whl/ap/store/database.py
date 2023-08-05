import sqlite3
from contextlib import contextmanager
import logging

logger = logging.getLogger('ap.store.database')
DATA_FILE_PATH = None

@contextmanager
def connect():
    conn = sqlite3.connect(DATA_FILE_PATH)
    conn.row_factory = sqlite3.Row

    yield conn
    conn.close()

@contextmanager
def cursor():
    with connect() as conn:
        yield conn.cursor()

def get(key):
    with cursor() as cur:
        cur.execute('SELECT * FROM apstore_kvps WHERE name = ?', (key,))
        row = cur.fetchone()

    return None if not row else row['value']

def list():
    with cursor() as cur:
        cur.execute('SELECT name FROM apstore_kvps')
        rows = cur.fetchall()

    return [row['name'] for row in rows]

def search(key):
    with cursor() as cur:
        cur.execute('SELECT * FROM apstore_kvps WHERE name LIKE ?', (f'%{key}%',))
        rows = cur.fetchall()

    return [row['name'] for row in rows]

def insert(key, value):
    with connect() as conn:
        cur = conn.cursor()
        cur.execute('INSERT INTO apstore_kvps VALUES (?, ?)', (key, value))
        conn.commit()

def delete(key):
    with connect() as conn:
        cur = conn.cursor()
        cur.execute('DELETE FROM apstore_kvps WHERE name = ?', (key,))
        conn.commit()

def initialize(data_file_path):
    global DATA_FILE_PATH
    logger.info(f'setting data file path to: {data_file_path}')
    DATA_FILE_PATH = data_file_path

    with connect() as conn:
        logger.info('verifying installation')
        cur = conn.cursor()
        cur.execute("SELECT COUNT(name) FROM sqlite_master WHERE type='table' AND name='apstore_kvps'")
        if cur.fetchone()[0] != 1:
            logger.info('table not found. creating...')
            conn.execute('CREATE TABLE IF NOT EXISTS apstore_kvps (name text, value text)')
            conn.commit()

        row = get('ap:store:configured')
        if not row:
            logger.info('not configured, configuring...')
            insert('ap:store:configured', 'true')
