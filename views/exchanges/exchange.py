import os
import json

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView
from kivy.metrics import dp, sp
from kivy.utils import rgba, QueryDict
from kivy.clock import Clock, mainthread
from kivy.properties import ListProperty
from kivy.core.window import Window
from kivy.properties import ColorProperty, ObjectProperty, BooleanProperty, ListProperty, StringProperty, NumericProperty

from pycoingecko import CoinGeckoAPI
from threading import Thread

from widgets.cards import ListTile, Asset

Builder.load_file('views/exchanges/exchange.kv')
class Exchange(BoxLayout):
    coins = ListProperty([])
    popular = ListProperty(['btc', 'eth', 'doge', 'ltc', 'dash', 'shib'])
    def __init__(self, **kw) -> None:
        super().__init__(**kw)
        self.cg = CoinGeckoAPI()

        Clock.schedule_once(self.render, .2)

    def render(self, _):
        exchanges = [
            {
                "id": "35235",
                "title": "KRAKEN",
                "source": "assets/imgs/kraken_logo.png",
                "connected": False,
                "keys": {
                    "key": "/sk12162sZfc6L7kohoUg7dpPOQfV88ejSwNUpLHvi2UhaX4HwmzT0BX",
                    "secret": "ejLSo7/JmSeBeBW5y33vxJC7QoK/o7yJyYyl9eHyXONJn45Wt/Q639xboW399BJiWf2eiefFuEqQ0qOZ8Pi/mQ=="
                }
            },
            {
                "id": "35215",
                "title": "OKCOIN",
                "source": "assets/imgs/ok-coin.png",
                "connected": False,
                "keys": {
                    "key": "2b8248a6-3dfb-4f40-b44f-cfa32f18e195",
                    "secret": "66072F864FC529751ED9A0BA9049067E",
                    "passphrase": "#hash537/OK"
                }
            },
        ]

        grid = self.ids.gl_connected
        exc = self.ids.gl_exchanges
        grid.clear_widgets()
        exc.clear_widgets()

        for e in exchanges:
            if e['connected']:
                ex = ConnectedExchange()
                ex.title = e['title']
                ex.source = e['source']
                ex.connected = e['connected']
                ex.keys = e['keys']

                grid.add_widget(ex)

            ev = ExchangeTile()
            ev.title = e['title']
            ev.source = e['source']
            ev.connected = e['connected']
            ev.keys = e['keys']

            exc.add_widget(ev)


class BaseExchange(BoxLayout):
    title = StringProperty("")
    source = StringProperty("")
    connected = BooleanProperty(False)
    keys = ObjectProperty(allownone=True)
    def __init__(self, **kw) -> None:
        super().__init__(**kw)

class ConnectedExchange(BaseExchange):
    def __init__(self, **kw) -> None:
        super().__init__(**kw)

class ExchangeTile(BaseExchange):
    def __init__(self, **kw) -> None:
        super().__init__(**kw)

    def get_connect(self):
        if self.connected:
            return

        ne = NewExchange()
        ne.source = self.source
        ne.title = self.title

        if self.keys.get("passphrase"):
            ne.passphrase = True
        ne.open()

class NewExchange(ModalView):
    passphrase = BooleanProperty(False)
    source = StringProperty("")
    title = StringProperty("")
    def __init__(self, **kw) -> None:
        super().__init__(**kw)

    def add_account(self):
        api_key = self.ids.key.text.strip()
        api_secret = self.ids.secret.text.strip()
        password = ""

        if self.passphrase:
            password = self.ids.password.text.strip()

        if api_key == "" or api_secret == "":
            print("Invalid api keys")
            return

        if self.passphrase:
            if password == "":
                print("Invalid passphrase")
                return
        
        data = {
            "title": self.title,
            "source": self.source,
            "connected": True,
            "keys": {
                "key": api_key,
                "secret": api_secret
            }
        }
        
        if self.passphrase:
            data['keys']['passphrase'] = password

        if os.path.exists("keys.json"):
            with open("keys.json", "r") as f:
                all_keys = json.load(f)
        else:
            all_keys = {}

        all_keys[self.title] = data
        with open("keys.json", "w") as f:
            json.dump(all_keys, f)

        App.get_running_app().kraken.api_key = api_key
        App.get_running_app().kraken.api_sec = api_secret
        
        self.dismiss()