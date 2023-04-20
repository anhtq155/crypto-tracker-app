import datetime

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label

from .optimizer import Nsga2
from .utils import TF_EQUIV
from .cexchanges.binance import BinanceClient
from .cexchanges.ftx import FtxClient

from widgets.box import BackBox
from widgets.labels import Text

Builder.load_file('views/strategies/optimize.kv')
class Optimize(BoxLayout):
    def __init__(self, **kw) -> None:
        super().__init__(**kw)

    def optimize(self):
        # mode = "optimize"
        while True:
            exchange = self.ids.cex.text.strip()
            # exchange = input("Choose an exchange: ").lower()
            if exchange in [".", "Binance"]:
                break

        if exchange == "Binance":
            client = BinanceClient(True)
        elif exchange == ".":
            client = FtxClient()

        while True:
            # symbol = self.ids.symbol.text.strip()
            symbol = "BTCUSDT"
            # symbol = input("Choose a symbol: ").upper()
            if symbol in client.symbols:
                break

        # Strategy
        available_strategies = ["obv", "ichimoku"]
        
        while True:
            _strategy = self.ids.strategy.text.strip()
            if _strategy == "On-balance volume":
                strategy = "obv"
            elif _strategy == "Ichimoku Kinko Hyo":
                strategy = "ichimoku"

            # strategy = input(f"Choose a strategy ({', '.join(available_strategies)}): ").lower()
            if strategy in available_strategies:
                break

        # Timeframe

        while True:
            # tf = self.ids.timeframe.text.strip()
            tf = "15m"
            # tf = input(f"Choose a timeframe ({', '.join(TF_EQUIV.keys())}): ").lower()
            if tf in TF_EQUIV.keys():
                break

        # From

        while True:
            from_time = self.ids.from_time.text.strip()
            # from_time = input("Backtest from (yyyy-mm-dd or Press Enter): ")
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
            to_time = self.ids.to_time.text.strip()
            # to_time = input("Backtest to (yyyy-mm-dd or Press Enter): ")
            if to_time == "":
                to_time = int(datetime.datetime.now().timestamp() * 1000)
                break

            try:
                to_time = int(datetime.datetime.strptime(to_time, "%Y-%m-%d").timestamp() * 1000)
                break
            except ValueError:
                continue

        # Population Size

        while True:
            try:
                # pop_size = int(input(f"Choose a population size: "))
                # pop_size = int(self.ids.popsize.text.strip())
                pop_size = 20
                break
            except ValueError:
                continue

        # Iterations

        while True:
            try:
                # generations = int(input(f"Choose a number of generations: "))
                # generations = int(self.ids.gennum.text.strip())
                generations = 8
                break
            except ValueError:
                continue

        nsga2 = Nsga2(exchange, symbol, strategy, tf, from_time, to_time, pop_size)

        p_population = nsga2.create_initial_population()
        p_population = nsga2.evaluate_population(p_population)
        p_population = nsga2.crowding_distance(p_population)

        g = 0
        while g < generations:

            q_population = nsga2.create_offspring_population(p_population)
            q_population = nsga2.evaluate_population(q_population)

            r_population = p_population + q_population

            nsga2.population_params.clear()

            i = 0
            population = dict()
            for bt in r_population:
                bt.reset_results()
                nsga2.population_params.append(bt.parameters)
                population[i] = bt
                i += 1

            fronts = nsga2.non_dominated_sorting(population)
            for j in range(len(fronts)):
                fronts[j] = nsga2.crowding_distance(fronts[j])

            p_population = nsga2.create_new_population(fronts)

            print(f"\r{int((g + 1) / generations * 100)}%", end='')

            g += 1

        # open a popup
        popup_content = BoxLayout(orientation = 'vertical', spacing = 8, padding = 8)
        label = Label(text = 'R PNL  MaxDD    Params                     CD     ', halign = 'left')
        label.texture_update()
        label.text_size = label.texture_size
        popup_content.add_widget(label)
        for individual in p_population:
            _label = Label(text = str(individual), color = '#f9b17a', halign = 'left')
            _label.texture_update()
            _label.text_size = label.texture_size
            popup_content.add_widget(_label)
            print(individual)
            
        popup = Popup(title='Results', content=popup_content, size_hint=(1, 0.9))
        popup.open()


        

        

