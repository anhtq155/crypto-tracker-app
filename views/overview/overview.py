from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp, sp
from kivy.utils import rgba, QueryDict
from kivy.properties import ListProperty

from kivy.clock import Clock, mainthread

from threading import Thread

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
            grid.add_widget(a)

    @mainthread
    def on_watchlist(self, inst, value):
        grid = self.ids.gl_watchlist
        grid.clear_widgets()

        for v in value:
            a = ListTile()
            grid.add_widget(a)

    def get_data(self):
        self.assets = self.get_assets()
        self.watchlist = self.get_watchlist()

    def get_assets(self):
        assets = ["BTC", "ETH", "DOGE", "LTC"]
        return assets

    def get_watchlist(self):
        assets = ["BTC", "ETH", "DOGE", "LTC"]
        return assets

class Asset(BoxLayout):
    def __init__(self, **kw) -> None:
        super().__init__(**kw)

class ListTile(BoxLayout):
    def __init__(self, **kw) -> None:
        super().__init__(**kw)
