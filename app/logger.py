import logging


FORMAT = '%(asctime)s [%(levelname)s] %(message)s'

logging.basicConfig(
    format=FORMAT,
    level=logging.INFO,
    filename='flask.log'
)
logger = logging.getLogger(__name__)