#!/bin/bash

sudo cp cointicker.service /lib/systemd/system/cointicker.service
sudo chmod 644 /lib/systemd/system/cointicker.service
chmod +x /home/pi/CoinTicker/app/coin_ticker/run.py
sudo systemctl daemon-reload
sudo systemctl enable cointicker.service
sudo systemctl start cointicker.service
