import logging
import sys

def setup_logging(name: str = 'mimir_syncer') -> logging.Logger:
    '''Configures and returns a logger.'''
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        handlers=[logging.StreamHandler(sys.stdout)]
    )
    return logging.getLogger(name)

logger = setup_logging()
