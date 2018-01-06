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
        logging.basicConfig()
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

    def fetch_coin_prices(self):
        prices = {}
        required_symbols = map(lambda t: t.symbol, self.trades)
        for symbol in required_symbols:
            try:
                url = "https://api.cryptonator.com/api/ticker/%s-usd" % symbol
                response = requests.get(url)
                response.raise_for_status()
                responseJson = response.json()
                if "ticker" in responseJson:
                    prices[symbol] = float(responseJson["ticker"]["price"])
                else:
                    self._logger.error("Unable to fetch data for symbol %s", symbol)
            except requests.exceptions.RequestException:
                self._logger.exception('Unable to fetch symbol %s', symbol)
        return prices

    def calculate_data(self):
        prices = self.fetch_coin_prices()
        total_value = 0
        total_cost = 0
        for trade in self.trades:
            if (trade.symbol in prices):
                price = prices[trade.symbol]
                value = trade.volume * price
                total_cost += trade.cost
                total_value += value
            else:
                self._logger.error("No price available for %s", trade.symbol)
        total_profit = total_value - total_cost
        gain = (total_profit / total_cost) * 100.0
        return Data(gain, datetime.datetime.now())

    def add_to_history(self, data):
        self.__history.append(data)
        max_history = 50
        if len(self.__history) > max_history:
                self.__history = self.__history[max_history:]

    def get(self):
        data = self.calculate_data()
        self.add_to_history(data)
        return self.__history
