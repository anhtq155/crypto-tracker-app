from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp, sp
from kivy.utils import rgba, QueryDict
from kivy.properties import ListProperty, StringProperty, NumericProperty

from kivy.clock import Clock, mainthread
from kivy.garden.graph import LinePlot

from threading import Thread
import json

from widgets.cards import ListTile, Asset

Builder.load_file('views/overview/overview.kv')
class Overview(BoxLayout):
    assets = ListProperty([])
    watchlist = ListProperty([])
    def __init__(self, **kw) -> None:
        super().__init__(**kw)
        Clock.schedule_once(self.render, .2)

    def render(self, _):
        t1 = Thread(target=self.get_data, daemon=True)
        t1.start()

    @mainthread
    def on_assets(self, inst, value):
        grid = self.ids.gl_my_assets
        grid.clear_widgets()

        for v in value:
            a = Asset()
            a.height = grid.parent.parent.height*.9
            a.text = str(v['symbol']).upper()
            a.source = v['image']
            a.price = v['current_price']
            a.price_change = v['market_cap_change_percentage_24h']
            grid.add_widget(a)

    @mainthread
    def on_watchlist(self, inst, value):
        grid = self.ids.gl_watchlist
        grid.clear_widgets()

        for v in value:
            a = ListTile()
            a.text = str(v['symbol']).upper()
            a.source = v['image']
            a.price = v['current_price']
            a.price_change = v['market_cap_change_percentage_24h']
            grid.add_widget(a)

    def get_data(self):
        self.assets = self.get_assets()
        self.watchlist = self.get_watchlist()

    def get_assets(self):
        assets = [
            {
                "symbol": 'btc',
                "image": "",
                "current_price": 423490,
                "market_cap_change_percentage_24h": 2.52
            },
            {
                "symbol": 'eth',
                "image": "",
                "current_price": 23655,
                "market_cap_change_percentage_24h": 1.23
            },
            {
                "symbol": 'ltc',
                "image": "",
                "current_price": 124.8,
                "market_cap_change_percentage_24h": 2.35
            },
            {
                "symbol": 'dash',
                "image": "",
                "current_price": 42.98,
                "market_cap_change_percentage_24h": 1.32
            },
        ]
        return assets

    def get_watchlist(self):
        assets = [
            {
                "symbol": 'btc',
                "image": "",
                "current_price": 423490,
                "market_cap_change_percentage_24h": 2.52
            },
            {
                "symbol": 'eth',
                "image": "",
                "current_price": 23655,
                "market_cap_change_percentage_24h": 1.23
            },
            {
                "symbol": 'ltc',
                "image": "",
                "current_price": 124.8,
                "market_cap_change_percentage_24h": 2.35
            },
            {
                "symbol": 'dash',
                "image": "",
                "current_price": 42.98,
                "market_cap_change_percentage_24h": 1.32
            },
        ]
        return assets