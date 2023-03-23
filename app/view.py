
from tokenize import String
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty, StringProperty
from kivy.clock import Clock

from pycoingecko import CoinGeckoAPI
from threading import Thread

class MainWindow(BoxLayout):
    coins = ListProperty([])
    username = StringProperty("")
    def __init__(self, **kw):
        super().__init__(**kw)
        self.cg = CoinGeckoAPI()
        try:
            self.get_coins()
        except:
            pass
    
    def get_coins(self):
        mkts = self.cg.get_coins_markets(vs_currency="usd", per_page=50)
        self.coins = mkts

        # Set coins for all screens
        self.ids.home.ids.overview.get_watchlist()
        Clock.schedule_once(self.ids.home.ids.currency.render, .1)
