import logging
import sys
import time
from logging import Logger
from logging.handlers import TimedRotatingFileHandler


def singleton(cls):
    instances = {}
    def _singleton():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return _singleton




logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='inventory.log',
                filemode='w')


console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
logger = logging.getLogger('inventory')
logger.addHandler(console)
