
from lnm_class import Trading as tr
import time
import tradingview_ta 
from tradingview_ta import TA_Handler, Interval, Exchange


def bot():

    bitcoin = TA_Handler(
    symbol="XBTUSD",
    screener="crypto",
    exchange="BITMEX",
    interval=Interval.INTERVAL_15_MINUTES,
    )
    analysis = bitcoin.get_analysis()

    rsi = analysis.indicators["RSI"]

    if rsi > 80:
        tr.Short(margin=1000, leverage=100, type="m")

    elif rsi < 30:
        tr.long(type="m", margin=1000, leverage=100)
    
bot()