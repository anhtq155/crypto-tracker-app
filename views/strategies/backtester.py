from .database import Hdf5Client

from .utils import resample_timeframe, STRAT_PARAMS
from .strategies_init import obv
from .strategies_init import ichimoku

def run(self, exchange: str, symbol: str, strategy: str, tf: str, from_time: int, to_time: int):

    p = {"type": int}
    params = dict()

    try:
        # params[p_code] = p["type"](input(p["name"] + ": "))
        if (strategy == "obv"):
            params["ma_period"] = p["type"](self.ids.ma_period.text.strip())
        elif (strategy == "ichimoku"):
            params["kijun"] = p["type"](self.ids.kijun.text.strip())
            params["tenkan"] = p["type"](self.ids.tenkan.text.strip())
    except:
        pass
    
    if strategy == "obv":
        h5_db = Hdf5Client(exchange)
        data = h5_db.get_data(symbol, from_time, to_time)
        data = resample_timeframe(data, tf)

        pnl, max_drawdown = obv.backtest(data, ma_period=params["ma_period"])

        return pnl, max_drawdown

    elif strategy == "ichimoku":
        h5_db = Hdf5Client(exchange)
        data = h5_db.get_data(symbol, from_time, to_time)
        data = resample_timeframe(data, tf)

        pnl, max_drawdown = ichimoku.backtest(data, tenkan_period=params["tenkan"], kijun_period=params["kijun"])

        return pnl, max_drawdown
