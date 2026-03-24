import os
import time

import sqlalchemy

from src.db.repositories.alvo_repository import AlvoRepository
from src.scripts.populate_fonte_db import main as populate_fonte


def wait_for_db(dsn, name, max_retries=30, delay=2):
    """Wait for database to be ready before attempting to connect"""
    engine = sqlalchemy.create_engine(dsn)

    for i in range(max_retries):
        try:
            with engine.connect():
                print(f'[{name}] Successfully connected to database!')
                return True
        except sqlalchemy.exc.OperationalError:
            print(f'[{name}] Database not ready, waiting {delay}s...')
            time.sleep(delay)

    raise Exception(f'Failed to connect to {name} after {max_retries} retries')


def init_all():
    alvo_dsn = os.getenv('DB_ALVO_DSN')
    fonte_dsn = os.getenv('DB_FONTE_DSN')

    if alvo_dsn:
        print('Waiting for Alvo database...')
        wait_for_db(alvo_dsn, 'Alvo')
        print('Inicializando banco Alvo...')
        alvo_repo = AlvoRepository(alvo_dsn)
        alvo_repo.setup_database()
        print('Tabelas do banco Alvo criadas.')

    if fonte_dsn:
        print('Waiting for Fonte database...')
        wait_for_db(fonte_dsn, 'Fonte')
        print('Inicializando e populando banco Fonte...')
        # A funcao main() do populate_fonte ja pega o DSN via dotenv/ambiente
        populate_fonte()
        print('Banco Fonte inicializado.')


if __name__ == '__main__':
    init_all()
