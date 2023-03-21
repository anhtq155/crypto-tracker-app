
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty

from pycoingecko import CoinGeckoAPI
from threading import Thread

class MainWindow(BoxLayout):
    coins = ListProperty([])
    def __init__(self, **kw):
        super().__init__(**kw)
        self.cg = CoinGeckoAPI()
        self.get_coins()
        # t1 = Thread(target=self.get_coins, daemon=True)
        # t1.start()
    
    def get_coins(self):
        mkts = self.cg.get_coins_markets(vs_currency="usd", per_page=10)
        self.coins = mkts
