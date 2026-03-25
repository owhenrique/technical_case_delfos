import logging
import sys


def setup_logging():
    """
    Configura o logging estruturado para a aplicacao.

    Aplica um formato padronizado com timestamp, nivel e mensagem
    em todos os loggers da aplicacao, direcionando a saida para stdout.
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[logging.StreamHandler(sys.stdout)],
    )
