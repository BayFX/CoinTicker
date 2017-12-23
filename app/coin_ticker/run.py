#!/usr/bin/python

from time import sleep
from updater import Updater

UPDATER = Updater()

try:
    print "Starting Coin Ticker"
    UPDATER.start()
    while True:
        sleep(60)
except KeyboardInterrupt:
    print "Stopping Coin Ticker"
    UPDATER.stop()
