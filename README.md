# Coin Ticker
Monitor your cryptocoin portfolio on a raspberry pi e-ink display.

[![](https://raw.githubusercontent.com/RevaxZnarf/CoinTicker/resources/resources/cointicker1_small.jpg?raw=true)](https://raw.githubusercontent.com/RevaxZnarf/CoinTicker/resources/resources/cointicker1.jpg?raw=true)
[![](https://raw.githubusercontent.com/RevaxZnarf/CoinTicker/resources/resources/cointicker2_small.jpg?raw=true)](https://raw.githubusercontent.com/RevaxZnarf/CoinTicker/resources/resources/cointicker2.jpg?raw=true)
[![](https://raw.githubusercontent.com/RevaxZnarf/CoinTicker/resources/resources/cointicker3_small.jpg?raw=true)](https://raw.githubusercontent.com/RevaxZnarf/CoinTicker/resources/resources/cointicker3.jpg?raw=true)

Coin Ticker displays the [profit percentage](https://en.wikipedia.org/wiki/Profit_margin) and history of your cryptocoin portfolio on a e-ink display. The information is updated every 30 minutes.

## Hardware

* [Raspberry Pi Zero W](https://www.raspberrypi.org/products/raspberry-pi-zero-w/)
* [2.13 inch e-Paper display](https://www.waveshare.com/wiki/2.13inch_e-Paper_HAT_(B))
* 2x20-pin Strip Dual Male Header
* Micro SDHC card
* USB power supply

Assemble the Coin Ticker by [soldering](https://www.raspberrypi.org/blog/getting-started-soldering/) the pin strip to the Raspberry Pi and attaching the display.

## Installation

Here's how to install Coin Ticker on a Raspberry Pi Zero W using a MacOS host.

### Prepare SD Card

1. Download [Raspbian lite image](https://downloads.raspberrypi.org/raspbian_lite/images/raspbian_lite-2016-11-29/2016-11-25-raspbian-jessie-lite.zip)
2. Umount the SD Card: `sudo diskutil unmount /dev/disk2s1` (Note that /dev/disk2s1 may be different on yout host)
3. Copy the image: `sudo dd bs=1m if=~/Downloads/2017-11-29-raspbian-stretch-lite.img  of=/dev/rdisk2 conv=sync`
4. Enable ssh on boot: `touch /Volumes/boot/ssh`
5. Enable spi: `nano /Volumes/boot/config.txt` and uncomment `dtparam=spi=on`
6. Setup wifi: `nano /Volumes/boot/wpa_supplicant.conf` and insert the config below. Replace the ssid and psk with your wifi credentials.
```
country=US
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
    ssid="your_real_wifi_ssid"
    scan_ssid=1
    psk="your_real_password"
    key_mgmt=WPA-PSK
}
```


### Connect to the Raspberry Pi

1. Boot the Raspberry Pi with the prepared SD Card
2. Discover the Raspberry Pi: `sudo nmap -sS -p 22 192.168.0.0/24`. Note: `192.168.0.0` may be different in your network.
3. Check if ssh works: `ssh pi@192.168.0.10` (the default password is `raspberry`)


### Install Coin Ticker on the Raspberry Pi

1. Clone this repo to your host machine
2. Copy `trades.yml.example` to `trades.yml` and modify your portfolio
3. Install ansible: `brew install ansible`
4. Navigate to the ansible directory of this repo and run: `./install.sh 192.168.0.10` (this will take some minutes)
5. Coin Ticker should now be updating the display. You can check if it worked by running `sudo systemctl status cointicker` on the Raspberry Pi


## Contribute

If you can think of other features or find bugs feel free to fork, open a PR or open an issue.

Donations are always welcome :)

Etherium: 0x0C9Da9FF04f0171Bc62a3c2142be0BBeE01bd488   
Neo: AHy4xYMW5nMFpRNEePP7eb73owKiLJHfy8   
Bitcoin: 1CN4omapW9X1AaodzqdecFyEvoTE8YoksB   
