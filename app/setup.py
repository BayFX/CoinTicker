from setuptools import setup
from setuptools import Command

from coin_ticker.display import Display
from coin_ticker.data_source import DataSource

class UpdateDisplayCommand(Command):
    user_options = []

    def initialize_options(self):
        """Abstract method that is required to be overwritten"""

    def finalize_options(self):
        """Abstract method that is required to be overwritten"""

    def run(self):
        print("Updating display ...")
        display = Display()
        data_source = DataSource("../trades.yml")
        data = data_source.get()
        display.update(data)

config = {
    'description': 'Monitor your cryptocoin portfolio on a raspberry pi e-ink display',
    'author': 'Revax Znarf',
    'url': 'https://github.com/RevaxZnarf/CoinTicker',
    'author_email': '',
    'version': '0.1',
    'tests_require': ['pylint'],
    'setup_requires': ['setuptools-lint', 'requests'],
    'install_requires': ['nose', 'requests'],
    'test_suite': 'nose.collector',
    'packages': ['coin_ticker'],
    'scripts': [],
    'name': 'Coin Ticker',
    'cmdclass': {'update_display': UpdateDisplayCommand},
}

setup(**config)
