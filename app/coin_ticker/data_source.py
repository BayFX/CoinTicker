import requests
import yaml
import logging
import datetime


class Trade(object):
    def __init__(self, name, symbol, volume, cost, trade_type):
        self.name = name
        self.symbol = symbol
        self.volume = volume
        self.cost = cost
        self.trade_type = trade_type


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
        trades = []
        if 'coins' in config['trades']:
            for trade in config['trades']['coins']:
                trades.append(Trade(trade['name'],
                                    trade['symbol'],
                                    trade['volume'],
                                    trade['cost'],
                                    'coin'))
        if 'stocks' in config['trades']:
            for trade in config['trades']['stocks']:
                trades.append(Trade(trade['name'],
                                    trade['symbol'],
                                    trade['volume'],
                                    trade['cost'],
                                    'stock'))
        return trades

    def fetch_coin_prices(self):
        prices = {}
        coin_trades = filter(lambda t: t.trade_type == 'coin', self.trades)
        required_symbols = map(lambda t: t.symbol, coin_trades)
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

    def fetch_stock_prices(self):
        prices = {}
        stock_trades = filter(lambda t: t.trade_type == 'stock', self.trades)
        required_symbols = map(lambda t: t.symbol, stock_trades)
        for symbol in required_symbols:
            try:
                url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=%s&outputsize=compact&datatype=json&interval=1min&apikey=24IXEF00K07P6PGQ" % symbol
                response = requests.get(url)
                response.raise_for_status()
                responseJson = response.json()
                if "Time Series (1min)" in responseJson:
                    timeseries = responseJson["Time Series (1min)"]
                    first = timeseries[timeseries.keys()[0]]
                    prices[symbol] = float(first["1. open"])
                else:
                    self._logger.error("Unable to fetch data for symbol %s", symbol)
            except requests.exceptions.RequestException:
                self._logger.exception('Unable to fetch symbol %s', symbol)
        return prices

    def calculate_data(self):
        coin_prices = self.fetch_coin_prices()
        stock_prices = self.fetch_stock_prices()
        total_value = 0
        total_cost = 0
        for trade in self.trades:
            prices = coin_prices if trade.trade_type == 'coin' else stock_prices
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
