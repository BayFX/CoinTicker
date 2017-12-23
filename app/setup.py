from setuptools import setup
from setuptools import Command

import subprocess
from coin_ticker.display import Display

class UpdateDisplayCommand(Command):
    user_options = []

    def initialize_options(self):
        """Abstract method that is required to be overwritten"""

    def finalize_options(self):
        """Abstract method that is required to be overwritten"""

    def run(self):
        print("Updating display ...")
        display = Display() 
        display.update()

config = {
    'description': 'Monitor your cryptocoin portfolio on a raspberry pi e-ink display',
    'author': 'Revax Znarf',
    'url': 'https://github.com/RevaxZnarf/CoinTicker',
    'author_email': '',
    'version': '0.1',
    'tests_require': ['pylint'],
    'setup_requires': ['setuptools-lint'],
    'install_requires': ['nose'],
    'packages': ['coin_ticker'],
    'scripts': [],
    'name': 'Coin Ticker',
    'cmdclass': {'update_display': UpdateDisplayCommand},
}

setup(**config)
