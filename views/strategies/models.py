import typing


class BacktestResult:
    def __init__(self):
        self.pnl: float = 0.0
        self.max_dd: float = 0.0
        self.parameters: typing.Dict = dict()
        self.dominated_by: int = 0
        self.dominates: typing.List[int] = []
        self.rank: int = 0
        self.crowding_distance: float = 0.0

    def __repr__(self):
        return f"{self.rank} {round(self.pnl * 100, 1)}% {round(self.max_dd *100, 1)}% {self.parameters}  " \
               f"{round(self.crowding_distance, 2)}"

    def reset_results(self):
        self.dominated_by = 0
        self.dominates.clear()
        self.rank = 0
        self.crowding_distance = 0.0
