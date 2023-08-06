import logging.config

# Say i have saved my configuration under ./myconf.conf
logging.config.fileConfig('myconf.conf')
logger = logging.getLogger('superAwesomeLogzioLogger')


logger.info('Test log')
logger.warn('Warning')

try:
    1/0
except:
    logger.exception("Supporting exceptions too!")
