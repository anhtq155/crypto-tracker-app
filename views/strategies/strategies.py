from threading import Thread
import datetime

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp, sp
from kivy.utils import rgba, QueryDict
from kivy.properties import ListProperty, StringProperty, NumericProperty

from .backtester import run
from .utils import TF_EQUIV
from .data_collector import collect_all
from .cexchanges.binance import BinanceClient
from .cexchanges.ftx import FtxClient

Builder.load_file('views/strategies/strategies.kv')
class Strategy(BoxLayout):
    def __init__(self, **kw) -> None:
        super().__init__(**kw)

    def render(self):
        mode = input("Choose the program mode (data / backtest): ").lower()

        while True:
            exchange = input("Choose an exchange: ").lower()
            if exchange in ["ftx", "binance"]:
                break

        if exchange == "binance":
            client = BinanceClient(True)
        elif exchange == "ftx":
            client = FtxClient()

        while True:
            symbol = input("Choose a symbol: ").upper()
            if symbol in client.symbols:
                break

        if mode == "data":
            collect_all(client, exchange, symbol)

        elif mode == "backtest":

            # Strategy

            available_strategies = ["obv", "ichimoku", "sup_res"]

            while True:
                strategy = input(f"Choose a strategy ({', '.join(available_strategies)}): ").lower()
                if strategy in available_strategies:
                    break

            # Timeframe

            while True:
                tf = input(f"Choose a timeframe ({', '.join(TF_EQUIV.keys())}): ").lower()
                if tf in TF_EQUIV.keys():
                    break

            # From

            while True:
                from_time = input("Backtest from (yyyy-mm-dd or Press Enter): ")
                if from_time == "":
                    from_time = 0
                    break

                try:
                    from_time = int(datetime.datetime.strptime(from_time, "%Y-%m-%d").timestamp() * 1000)
                    break
                except ValueError:
                    continue

            # To

            while True:
                to_time = input("Backtest to (yyyy-mm-dd or Press Enter): ")
                if to_time == "":
                    to_time = int(datetime.datetime.now().timestamp() * 1000)
                    break

                try:
                    to_time = int(datetime.datetime.strptime(to_time, "%Y-%m-%d").timestamp() * 1000)
                    break
                except ValueError:
                    continue

            print("(Profit & Lost, Maximum DrawDown", run(exchange, symbol, strategy, tf, from_time, to_time))
                

        

        

