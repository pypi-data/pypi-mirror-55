import logging
from copy import copy
from logging import Formatter

MAPPING = {
    'DEBUG': 37,  # white
    'INFO': 36,  # cyan
    'WARNING': 33,  # yellow
    'ERROR': 31,  # red
    'CRITICAL': 41,  # white on red bg
}

PREFIX = '\033['
SUFFIX = '\033[0m'


class ColoredFormatter(Formatter):
    def __init__(self, patern):
        Formatter.__init__(self, patern)

    def format(self, record):
        colored_record = copy(record)
        levelname = colored_record.levelname
        seq = MAPPING.get(levelname, 37)  # default white
        colored_levelname = ('{0}{1}m{2}{3}') \
            .format(PREFIX, seq, levelname, SUFFIX)
        colored_record.levelname = colored_levelname
        return Formatter.format(self, colored_record)


# Create top level logger
logger = logging.getLogger('lightdo')

# Add console handler using our custom ColoredFormatter
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
cf = ColoredFormatter("[%(name)s][%(levelname)s]  %(message)s")
ch.setFormatter(cf)
logger.addHandler(ch)

# Add file handler
fh = logging.FileHandler('log.log', encoding='utf-8')
fh.setLevel(logging.DEBUG)
ff = logging.Formatter(
    '[%(asctime)s] - [%(name)s] - [%(levelname)s] - %(message)s (%(filename)s:%(lineno)d)'
)
fh.setFormatter(ff)
logger.addHandler(fh)

# Set log level
logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    logger.debug('A debug message')
    logger.info('An info message')
    logger.warning('Something is not right.')
    logger.error('A Major error has happened.')
    logger.critical('Fatal error. Cannot continue')
