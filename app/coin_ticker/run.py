#!/usr/bin/python

from time import sleep
from updater import Updater
import logging
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
config = sys.argv[1]
UPDATER = Updater(config)

try:
    logger.info("Starting Coin Ticker")
    UPDATER.start()
    while True:
        sleep(60)
except KeyboardInterrupt:
    logger.info("Stopping Coin Ticker")
    UPDATER.stop()
