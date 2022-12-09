
from lnm_class import Trading as tr
import tracker as tracker
import time
import tradingview_ta 
from tradingview_ta import TA_Handler, Interval, Exchange


def bot():

    bitcoin = TA_Handler(
    symbol="XBTUSDTU22",
    screener="crypto",
    exchange="BITMEX",
    interval=Interval.INTERVAL_15_MINUTES,
    )
    analysis = bitcoin.get_analysis()
    print(analysis)
    
bot()