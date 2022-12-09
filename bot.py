
import lnm_class as tr  # acá traemos la clase Trading del modulo lnm_class
import time
import tradingview_ta 
from tradingview_ta import TA_Handler, Interval, Exchange
import json


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

    user = tr.Trading(
        key="",
        secret="", 
        passphrase="")

    # de la misma manera creamos el objeto analysis que tiene los metodos de tradingview_ta
    analysis = bitcoin.get_analysis()
    
    while True: #creamos un bucle para que cada x tiempo pida los datos y revise si se cumplen las condiciones


        # de esta manera obtenemos los datos que queremos de tradingview_ta, estos estan alojados en un diccionario 

        rsi = analysis.indicators["RSI"]
    
        bollinger_upper = analysis.indicators["BB.upper"]

        bollinger_lower = analysis.indicators["BB.lower"]

        ema20 = analysis.indicators["EMA20"]

        # aca obtenemos el precio de lnm


        index = user.price_index()

        bid = user.price_bid()

        offer = user.price_offer()


        # hago el print para verificar que me entrega los datos que quiero

        print(rsi)
        print(bollinger_lower)
        print(bollinger_upper)
        print(ema20)
        print(index)
        print(bid)
        print(offer)


    

        # aca ya empezariamos a montar la estrategia segun los datos que obtenemos 

        if (rsi > 70) and (bid > ema20) and (bid >= bollinger_upper):
            # de alguna manera calcular el tp y el sl
            user.Short(margin=1000, leverage=100, type="m") 

        elif (rsi < 30) and (offer > ema20):
            user.long(type="m", margin=1000, leverage=100)
    
        time.sleep(300)
  

