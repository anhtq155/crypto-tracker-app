from threading import Thread
import json
import os

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp, sp
from kivy.utils import rgba, QueryDict
from kivy.properties import ListProperty, StringProperty, NumericProperty

from kivy.clock import Clock, mainthread
from kivy.garden.graph import LinePlot


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
            a.data = v
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
            a.data = v
            grid.add_widget(a)

    def get_data(self):
        self.get_watchlist()
        # kraken_data = App.get_running_app().kraken.get_balance()
        okcoin_data = App.get_running_app().okcoin.get_balance()

        all_data = []
        # if kraken_data['code'] == 200:
        #     for k,v in kraken_data['result'].items():
        #         all_data.append(v)

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
        total = 0
        for i, b in enumerate(balances_balance):
            symbol = balances_symbols[i].lower()
            if symbol == 'usd':
                total += float(b)
                continue

            tgt_coin = [x for x in coins if x['symbol'] == symbol][0]

            owned = float(b)*float(tgt_coin['current_price'])
            total += owned
        self.current_balance = round(total, 3)

    def refresh(self):
        App.get_running_app().root.get_coins()
        t1 = Thread(target=self.get_data, daemon=True)
        t1.start()
        

    def get_watchlist(self):
        current_list = {}
        upath = App.get_running_app().user_data_dir
        save_path = os.path.join(upath, "watchlist.json")

        if os.path.exists(save_path):
            with open(save_path, "r") as f:
                current_list = json.load(f)

        coins = App.get_running_app().root.coins

        coins = [x for x in coins if x['symbol'].upper() in list(current_list.keys())]

        self.watchlist = coins

        

