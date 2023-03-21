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
    balances = ListProperty([])
    watchlist = ListProperty([])
    current_balance = NumericProperty(0.0)
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
            owned = "".join(["0.0", str(v['symbol']).upper()])

            for b in self.balances:
                if b['currency'] == str(v['symbol']).upper():
                    owned = "%s%s"%(b['balance'], b['currency'])
                    break

            a = Asset()
            a.height = grid.parent.parent.height*.9
            a.text = str(v['symbol']).upper()
            a.source = v['image']
            a.price = v['current_price']
            a.price_change = v['market_cap_change_percentage_24h']

            a.owned = owned
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
        kraken_data = App.get_running_app().kraken.get_balance()
        okcoin_data = App.get_running_app().okcoin.get_balance()

        all_data = []
        if kraken_data['code'] == 200:
            for k,v in kraken_data['result'].items():
                all_data.append(v)

        if okcoin_data['code'] == 200:
            for o in okcoin_data['result']:
                all_data.append(o)

        self.balances = all_data
    
    def on_balances(self, inst, balances):
        balances_symbols = [x['currency'] for x in balances]
        balances_balance = [x['balance'] for x in balances]
        coins = App.get_running_app().root.coins

        coins = [x for x in coins if x['symbol'].upper() in balances_symbols]
        self.assets = coins
        """
            'id': 'bitcoin', 'symbol': 'btc', 'name': 'Bitcoin', 'image': 'https://assets.coingecko.com/coins/images/1/large/bitcoin.png?1547033579', 'current_price': 41219, 'market_cap': 785434733712, 'market_cap_rank': 1, 'fully_diluted_valuation': 867281629120, 'total_volume': 29005677029, 'high_24h': 42859, 'low_24h': 41208, 'price_change_24h': -37.345511788662, 'price_change_percentage_24h': -0.09052, 'market_cap_change_24h': 1340569965, 'market_cap_change_percentage_24h': 0.17097, 'circulating_supply': 19018193.0, 'total_supply': 21000000.0, 'max_supply': 21000000.0, 'ath': 69045, 'ath_change_percentage': -38.13691, 'ath_date': '2021-11-10T14:24:11.849Z', 'atl': 67.81, 'atl_change_percentage': 62890.49777, 'atl_date': '2013-07-06T00:00:00.000Z', 'roi': None, 'last_updated': '2022-04-21T20:15:09.291Z'}
        """
        total = 0
        for i, b in enumerate(balances_balance):
            symbol = balances_symbols[i].lower()
            if symbol == 'usd':
                total += float(b)
                continue

            tgt_coin = [x for x in coins if x['symbol'] == symbol][0]

            owned = float(b)*float(tgt_coin['current_price'])
            total + owned
        self.current_balance = round(total, 3)


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

