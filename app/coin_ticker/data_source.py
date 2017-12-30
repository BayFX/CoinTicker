import requests
import yaml
import logging
import datetime


class Trade(object):
    def __init__(self, name, symbol, volume, cost):
        self.name = name
        self.symbol = symbol
        self.volume = volume
        self.cost = cost


class Data(object):
    def __init__(self, gain, timestamp):
        self.__gain = gain
        self.__timestamp = timestamp

    def gain(self):
        return self.__gain

    def timestamp(self):
        return self.__timestamp


class DataSource(object):
    def __init__(self, config):
        self._logger = logging.getLogger(__name__)
        self.trades = self.load_trades(config)
        self.__history = []

    def load_trades(self, config):
        self._logger.info('Loading trades from %s', config)
        stream = open(config, "r")
        config = yaml.load(stream)
        trades_config = config['trades']
        trades = []
        for trade in trades_config:
            trades.append(Trade(trade['name'],
                                trade['symbol'],
                                trade['volume'],
                                trade['cost']))
        return trades

    def fetch_coinmarketcap_prices(self, prices):
        url = "https://api.coinmarketcap.com/v1/ticker"
        raw_prices = requests.get(url).json()
        for item in raw_prices:
            prices[item['symbol']] = float(item['price_usd'])
        return prices

    def calculate_data(self):
        prices = self.fetch_coinmarketcap_prices({})
        total_value = 0
        total_cost = 0
        for trade in self.trades:
            price = prices[trade.symbol]
            value = trade.volume * price
            total_cost += trade.cost
            total_value += value
        total_profit = total_value - total_cost
        gain = (total_profit / total_cost) * 100.0
        return Data(gain, datetime.datetime.now())

    def add_to_history(self, data):
        self.__history.append(data)
        max_history = 50
        if len(self.__history)>max_history:
                self.__history = self.__history[:max_history]

    def get(self):
        data = self.calculate_data()
        self.add_to_history(data)
        return self.__history
