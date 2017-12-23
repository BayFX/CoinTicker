
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

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
    'name': 'Coin Ticker'
}

setup(**config)
