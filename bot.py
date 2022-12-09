
from lnm_class import Trading as tr  # acá traemos la clase Trading del modulo lnm_class
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

# en esta line estoy creando el objeto user con todos los metodos de la clase Trading del lnm_class
# los parametros que necesita esta clase para funcionar es la apikey
# esta clase tambien nos permite utilizar los metodos directamente de lnm Api

    user = tr(
        key="",
        secret="", 
        passphrase="")

# de la misma manera creamos el objeto analysis que tiene los metodos de tradingview_ta
    analysis = bitcoin.get_analysis()

# de esta manera obtenemos los datos que queremos, estos estan alojados en un diccionario 
    rsi = analysis.indicators["RSI"]

# aca ya empezariamos a montar la estrategia segun los datos que obtenemos de analysis

    if rsi > 80:
        user.Short(margin=1000, leverage=100, type="m") 

    elif rsi < 30:
        user.long(type="m", margin=1000, leverage=100)
    
