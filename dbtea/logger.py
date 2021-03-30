import logging

LOG_FILENAME = 'dbtea.log'
logger = logging.getLogger('dbtea')
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
logger.addHandler(console_handler)

DBTEA_LOGGER = logger
